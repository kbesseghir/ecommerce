from django.contrib import admin
from .models import *  
from api.admin import *

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('username', 'department')

class FournisseurAdmin(admin.ModelAdmin):    
    list_display =('nom','prenom','type_matiere')
        
class Facture_ShowroomAdmin(admin.ModelAdmin): 
    list_display = ('nom', 'prenom', 'date', 'Total_price','id')

class PanierAdmin(admin.ModelAdmin):   
    list_display =('product','quantity')
    
admin.site.register(Facture_Showroom,Facture_ShowroomAdmin)    
admin.site.register(Employee, EmployeeAdmin)   
admin.site.register(Fournisseur,FournisseurAdmin)     
admin.site.register(User, UserAdmin)      
admin.site.register(Product)
admin.site.register(Order)       
admin.site.register(Checkout)        
admin.site.register(Review)
admin.site.register(Panier, PanierAdmin)

admin.site.register(Category)
admin.site.register(Promotion)

