from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer  , UserDetailsSerializer ,PasswordResetSerializer
from rest_framework import serializers
from erp_app.models import *
from allauth.account.utils import setup_user_email
# import django.contrib.auth.password_validation as validators
from django.core.exceptions import ValidationError
from django.core import validators
from email_validator import validate_email as VE , EmailNotValidError
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model,authenticate
from dj_rest_auth.models import TokenModel
from restApi.serializer import *

try:
    from allauth.account.adapter import get_adapter
    from allauth.utils import email_address_exists
except ImportError:
    raise ImportError('allauth needs to be added to INSTALLED_APPS.')

from dj_rest_auth.serializers import TokenSerializer


user=get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = user
        exclude = ("password","groups", "user_permissions")

class TokenSerializer(TokenSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = TokenModel
        fields = ('key', 'user')

# Custom registration serializer
# django-rest-auth’s default register serializer (RegisterSerializer) only recognizes fields for django built-in user model
# the fields in the custom serializer are gonna appear in registration form in addition to the base user model fields (username , email ,psswd1,psswd2)
class CustomRegisterSerializer(RegisterSerializer):
    username=None
    first_name = serializers.CharField(required=True, write_only=True)
    last_name = serializers.CharField(required=True, write_only=True)
    phone = serializers.CharField(max_length=10,required=True,validators=[phone_regex])
    adress =serializers.CharField(max_length=300,required=True,write_only=True)
    sex = serializers.CharField(required=True, write_only=True)
    date_of_birth = serializers.DateField(required=True, write_only=True)
    password1 = serializers.CharField( write_only=True, required=True, style={'input_type': 'password', })
    password2 = serializers.CharField( write_only=True, required=True, style={'input_type': 'password' })
    
    """
    the following methods are instance methods of the predefined RegisterSerializer class , which we will override
    
    """   
    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        try:
            emailobject=VE(email)
            email=emailobject.email
        except EmailNotValidError as errorMsg:
            raise ValidationError(_(str(errorMsg)))
        """    
        If `email` is not valid
        we print a human readable error message  
        """
        if email and email_address_exists(email):
            raise ValidationError(_('A user is already registered with this e-mail address.'))
        return email 
    
    # "password" and "password confirmation match" validator
    def validate(self,data):
        if data['password1'].isdigit():
            raise serializers.ValidationError(
                _(" password must contain at least one letter") )     
        if data['password1'].isalpha():
            raise serializers.ValidationError(_('Password must contain digits.'))                     
        if data['password1'] != data['password2']:
            raise serializers.ValidationError(
               _("The two password fields didn't match."))
        return data

       # clean the data
    def get_cleaned_data(self):
        super(CustomRegisterSerializer, self).get_cleaned_data()
        return {
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'email': self.validated_data.get('email', ''),
            'phone': self.validated_data.get('phone', ''),
            'address':self.validated_data.get('address', ''),
            'profil_image':self.validated_data.get('profil_image',''),
            'password1': self.validated_data.get('password1', ''),
            'password2': self.validated_data.get('password2', ''),
            'date_of_birth': self.validated_data.get('date_of_birth', ''),
            'sex': self.validated_data.get('sex', ''),
        }
    # save a user instance
    def save(self, request):
        user = super().save(request)
        self.cleaned_data = self.get_cleaned_data()
        user.phone = self.cleaned_data['phone']
        user.sex = self.cleaned_data['sex']
        user.date_of_birth = self.cleaned_data['date_of_birth']
        user.save()
        return user

class CustomLoginSerializer(LoginSerializer):
    username = None

    def authenticate(self, **options):
        return authenticate(self.context["request"], **options)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")
        if email and password:
            user = authenticate(
                email=email,
                pasword=password,
            )
            if not user:
                msg = "Incorrect credentials."
                raise serializers.ValidationError(msg, code="authorization")
        else:
            msg = _("Must include either 'username' or 'email' and 'password'.")
            raise serializers.ValidationError(msg, code="authorization")
        attrs["user"] = user
        return attrs

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = user
        read_only_fields = [
            "id",
            "is_superuser",
            "email",
            "date_joined",
        ]
        exclude = ("password","groups", "user_permissions")

# class ProductSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Product
#         fields = '__all__'
#     class Meta:
#         ref_name = 'ApiProductSerializer'

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = Order
        fields = '__all__'

class CheckoutSerializer(serializers.ModelSerializer):
    orders = OrderSerializer(many=True, read_only=True)

    class Meta:
        model = Checkout
        fields = '__all__'

class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
