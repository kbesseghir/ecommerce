from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.core import validators
from django.urls import reverse
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.conf import settings
from decimal import Decimal
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime
import hashlib
from os import urandom
from django.utils import timezone


# Create your models here.
DEPARTMENTS = [
        ('meca', 'Mecanique'),
        ('elec', 'Electronique'),
        ('Assemblage','Assemblage'),
        ('Gerant','Gestion'),
        ('Agent_showroom','Showroom'),
        ('stock','Gestion de stock'),
]

# phone number validator
    
phone_regex = RegexValidator(regex=r'^(05|06|07)[0-9]{8}$',
message=_('Invalid phone number ,phone number should be on the format : 05/06/07 (********)'))



class CustomUserManager(BaseUserManager):

    def create_user(self,email,first_name,last_name,phone,address,date_of_birth,sex,password=None,username=None):
        user=self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            address=address,
            sex=sex,
            date_of_birth=date_of_birth,
            )
        
        user.set_password(password)
        user.is_active=True
        user.is_staff=True
        user.is_superuser=True
        user.save(using=self._db)
        return user

        
    def create_superuser(self, email, first_name,last_name,phone,date_of_birth,sex, password,username=None,adress=None,**extra_fields):
        if not email:
            raise ValueError("You must provide an email")
        if not password:
            raise ValueError("You must provide a password")
        if not first_name:
            raise ValueError("You must provide a first name")
        if not last_name :
            raise ValueError("You must provide a last name")    

        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            address=None,
            date_of_birth=date_of_birth,
            sex=sex,
        )
        user.set_password(password)
        user.is_active=True
        user.is_staff=True
        user.is_superuser=True
        user.save(using=self._db)
        return user





""" User model """

class User(AbstractUser):
    username=models.CharField(max_length=10,null=True)
    email = models.EmailField("Email",unique=True)
    phone = models.CharField(max_length=10,validators=[phone_regex])
    address = models.CharField(max_length=300,blank=True,null=True)
    SEX = [("Male", "Male"), ("Female", "Female"), ("Other", "Other")]
    sex = models.CharField(max_length=30, choices=SEX, default="Male")
    date_of_birth = models.DateField(null= True,blank=True)
    profil_image=models.ImageField(null=True,upload_to='uploads/client_images')
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['phone','date_of_birth','sex','first_name','last_name']
    # setting my custom user manager as the default user manager 
    # that takes care of creating user instances and saving them in database

    objects=CustomUserManager()

    def has_perm(self,perm,obj=None):
        return self.is_superuser
    def has_module_perms(self,app_label):
        return True    

 
    class Meta:
        verbose_name_plural = "Users"

    # The __str__() method is the default human-readable representation of the object. 
    # Django will use it in many places, such as the administration site.    

    def __str__(self):
        return f"{self.pk} : {self.first_name} {self.last_name} {self.email}"


class Employee(models.Model):
    department = models.CharField(max_length=20, choices=DEPARTMENTS)
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)

    def __str__(self):
        return self.username

class Fournisseur(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    MATIERE_CHOICES = [
        ('Accessoires', 'Accessoires'),
        ('Matiere premiere Electronique', 'Matière première Électronique'),
        ('Matiere premiere Mecanique', 'Matière première Mécanique'),
    ]
    type_matiere = models.CharField(max_length=30, choices=MATIERE_CHOICES)
    numero_rc = models.CharField(max_length=20)
    numero_nif = models.CharField(max_length=20)
    numero_nis = models.CharField(max_length=20)
    numero_telephone = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.nom} {self.prenom}"





class Promotion(models.Model):
    name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    discount = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(1)])
    def __str__(self):
        return self.name 

    


class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name 


""" Product model """

class Product(models.Model):
    name = models.CharField(max_length=30)


    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    description = models.TextField()
    image = models.ImageField(upload_to='produits_images/', default='produits_images/photo_non_dispo.png')
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    available=models.BooleanField(default=True)
    SOURCE_CHOICES = [
        ('Startup', 'Produit fabriqué par la startup'),
        ('Fournisseur', 'Produit acheté auprès d\'un fournisseur'),
    ]
    source = models.CharField(max_length=30, choices=SOURCE_CHOICES, default='Startup')
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        if self.source == 'Startup':
            return f"{self.name} : produit par la startup"
        elif self.source == 'Fournisseur' and self.fournisseur:
            return f"{self.name} , fournisseur : {self.fournisseur.nom } {self.fournisseur.prenom}"
        else:
            return self.name
        
    promotion = models.ForeignKey(Promotion, null=True, blank=True, on_delete=models.SET_NULL)

    def get_discounted_price(self):
        if self.promotion:
            return self.price - (self.price * self.promotion.discount)
        else:
            return self.price
    # def save(self, *args, **kwargs):
    #     self.discount = self.get_discounted_price()
    #     super().save(*args, **kwargs)

    def __str__(self):
        return self.name 
    class Meta:
        verbose_name_plural = "Products"         
    
    
    
    
""" review model """

    
class Review(models.Model):
    """
    ->Many-to-one relationship.
    -> related_name is used to access the 'review' instances. 
    ex:  product-instance.reviews.all()
    ->related_query_name ' enable you to use "review” as a lookup parameter in a queryset, 
     ex: Product.objects.filter(review='blabla').
   
    -> Here, a product can have none , or many reviews. 
   
    """
    content = models.TextField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews', related_query_name='review')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews', related_query_name='review')
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    def __str__(self):
        return self.content
    class Meta:
        verbose_name_plural = "Reviews"    

""" checkout model """

class Checkout(models.Model):
    SHIPPING_STATES = (
        ('pending', 'Pending'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
    )
    shipping_state = models.CharField(max_length=20, choices=SHIPPING_STATES, default='pending')

    date_checkout= models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    #subtotal of the order, before shipping fees are added.
    subtotal= models.DecimalField(max_digits=10, decimal_places=2)
    shipping_cost= models.DecimalField(max_digits=10, decimal_places=2)
    # store the total cost of the order, including shipping.
    total= models.DecimalField(max_digits=10, decimal_places=2)
    shipping_adress= models.CharField(max_length=200)
    # shipping_state = models.CharField(max_length=20, choices=SHIPPING_STATES, default='pending')
    tracking_number = models.CharField(max_length=100)
    payment_method=models.CharField(max_length=25)
    STATUS=(
        ('paid', 'paid'),
        ('pending', 'pending'),
        ('cancelled', 'cancelled'),
    )
    payment_status=models.CharField(max_length=20,choices=STATUS,default='pending')
    user=models.ForeignKey(User,on_delete=models.CASCADE)

    def get_orders():
        return self.orders.all()
     
""" order model """

class Order(models.Model):

    

    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='orders',related_query_name='order')
    quantity=models.IntegerField(default=1)  
    checkout=models.ForeignKey(Checkout,on_delete=models.CASCADE,related_name='orders',related_query_name='order',blank=True,null=True)
  
    @staticmethod
    def get_all_orders_by_user(user_id): 
        return Order.objects.filter(user=user_id)
    def __str__(self):
        return f"{self.product.name} : {self.quantity} "   

    class Meta:
        verbose_name_plural = "Orders"    

    
# debut models de shiwroom

class Panier(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.product.name



class Facture_Showroom(models.Model):
    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255)
    email = models.EmailField()
    date = models.DateTimeField(auto_now_add=True)
    Reduction = models.IntegerField(null=True,default=0)
    Total_price = models.DecimalField(null=True,default=True,decimal_places=2,max_digits=10)
    Total_p = models.DecimalField(null=True,default=True,decimal_places=2,max_digits=10)

    def save(self, *args, **kwargs):
        total_price = Decimal('0.00')
        total_p = Decimal('0.00')
        paniers = Panier.objects.all()
        for panier in paniers:
           
           quantity=Decimal(panier.quantity)
           total_p +=Decimal(panier.product.sale_price) *quantity
           total_price += Decimal(panier.product.sale_price) *quantity
        
        total_price -= total_price * Decimal(self.Reduction) / 100
        self.Total_price = total_price + total_p* Decimal(19/100)
        self.Total_p =total_p  
        super().save(*args, **kwargs)


# fin models de showroom 



    
class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}'s favorite list"

