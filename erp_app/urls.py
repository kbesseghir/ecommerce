from django.urls import path
from . import views


urlpatterns = [
    path('', views.login, name='login'),
    
    # pages de Gestion de stock
    path('G_stock/home',views.GS_home, name='GS_home'),
    path('G_stock/frn/',views.frn, name='frn'),
    path('G_stock/frn/Gestion_lvn',views.Gestion_lvn, name='Gestion_lvn'),
    path('G_stock/frn/RC',views.RC, name='RC'),
    
    # espace showroom
    path('showroom/', views.showroom, name='showroom'),
     path('ajouter_au_panier/', views.ajouter_au_panier, name='ajouter_au_panier'),
     path('supprimer_du_panier/', views.supprimer_du_panier, name='supprimer_du_panier'),
    
    path('showroom/facture', views.passer_commande, name='passer_commande'),
    #Fin pages de gestion de stock
    path('deco/', views.deco, name='deco'),
    


    
    
    #path('elec/', views.elec, name='elec'),
]
