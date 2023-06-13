
from .forms import ProductSearchForm
from .models import *
from .forms import ProductSearchForm
import json
from decimal import Decimal
from django.shortcuts import render, redirect








def login(request):
    if request.method == 'POST':
        
        username = request.POST['username']
        password = request.POST.get('password')
        
        try:
            employee = Employee.objects.get(username=username, password=password)
        except Employee.DoesNotExist:
            employee = None
        if employee:
            request.session['is_authenticated'] = True
            request.session['username'] = username
            request.session['password'] = password
            if employee.department == 'meca':
                return render(request,'meca.html')
            elif employee.department == 'elec':
                return render(request, 'elec.html')
            elif employee.department =='Assemblage':
                return render(request,'Assm.html')
            elif employee.department =='stock':
                return redirect('GS_home')
            else:
                return render(request,'loginn.html')
                
        else:
            return render(request, 'loginn.html', {'error': 'Invalid username or password'})
            
    else:
        return render(request, 'loginn.html')

# Gestion stock function

def frn(request):
    if request.session.get('is_authenticated', False):
        return render(request,'G_stock/frn.html' )
    else : 
        return redirect('login')
def GS_home(request):
    produits=Product.objects.all()
    context = { 
              
              'produits': produits,
              }
    if request.session.get('is_authenticated', False):
        return render(request,'G_stock/index.html',context)
    
    else : 
        return redirect('login')
def Gestion_lvn(request):
    if request.session.get('is_authenticated', False):
        return render(request,'G_stock/Gestion_lvn.html' )
    else : 
        return redirect('login')

def RC(request):
    if request.session.get('is_authenticated', False):
        fournisseurs = Fournisseur.objects.all()
        context = {'fournisseurs': fournisseurs}
        return render(request,'G_stock/RC.html',context )
    else : 
        return redirect('login')
    
#Fin gestion de stock function

#se deconnecter 

def deco(request):
    request.session.pop('is_authenticated',None)
    request.session.clear()
    return redirect('login')         

#Fin se deconnecter 


#  views cree fournisseur 

def creer_fournisseur(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        type_matiere = request.POST.get('matiere')
        numero_rc = request.POST.get('rc')
        numero_nif = request.POST.get('nif')
        numero_nis = request.POST.get('nis')
        numero_telephone = request.POST.get('telephone')

        fournisseur = Fournisseur(nom=nom, prenom=prenom, type_matiere=type_matiere, numero_rc=numero_rc, numero_nif=numero_nif, numero_nis=numero_nis, numero_telephone=numero_telephone)
        fournisseur.save()

        return redirect('frn') # rediriger vers la page des fournisseurs après l'enregistrement

    return render(request, 'G_stock/frn.html')

# fin cree fournisseur
#shoowroom 
def showroom(request):
    products = Product.objects.all()
    panier = Panier.objects.all()
    context = {'products': products, 'panier': panier}
    return render(request, 'showroom/showroom.html', context)
def facture(request):
    cart = request.session.get('cart', [])
    total = 0
    if cart and isinstance(cart, list):
        for item in cart:
            if isinstance(item, dict) and 'product' in item:
                total += item['product'].price * item['quantity']
        if cart[0]['product'] and hasattr(cart[0]['product'], 'client'):
            client = cart[0]['product'].client
        else:
            client = None
        context = {
            'client': client,
            'cart': cart,
            'total': total,
            'date': cart[0]['product'].date_vente if cart and isinstance(cart, list) and cart[0]['product'] else None
        }
        return redirect('facture.html')
    else:
        return redirect('showroom')
        
def ajouter_au_panier(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = request.POST.get('quantity')
        product = Product.objects.get(id=product_id)
        panier = Panier(product=product, quantity=quantity)
        panier.save()
    return redirect('showroom')

def supprimer_du_panier(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        Panier.objects.filter(id=item_id).delete()
    return redirect('showroom')

def passer_commande(request):
    if request.method == 'POST':
        nom = request.POST['nom']
        prenom = request.POST['prenom']
        email = request.POST['email']
        reduction = request.POST['Reduction']
        facture = Facture_Showroom(
            nom=nom,
            prenom=prenom, 
            email=email,
            Reduction=reduction,  
        )
        facture.save()
        derniere_facture = Facture_Showroom.objects.latest('id') 
        panier = Panier.objects.all()
        derniere_facture_id = derniere_facture.id

        context = {
            
            'nom': nom,
            'prenom':prenom,
            'email': email,
            'reduction': reduction,
            'date': derniere_facture.date,
            'Total': derniere_facture.Total_p,
            'panier': panier ,
            'id': derniere_facture_id, 
            'TTC': derniere_facture.Total_price,

        }
        
        return render(request, 'showroom/facture.html', context)
    return render(request, 'showroom/facture.html', context)

#fin showroom

#creation fournisseur 


def frn(request):
    

    if request.method == 'POST':
        # Récupérer les données du formulaire
        nom = request.POST['nom']
        prenom = request.POST['prenom']
        type_matiere = request.POST['matiere']
        numero_rc = request.POST['rc']
        numero_nif = request.POST['nif']
        numero_nis = request.POST['nis']
        numero_telephone = request.POST['telephone']

        # Créer un nouveau fournisseur
        fournisseur = Fournisseur(
            nom=nom,
            prenom=prenom,
            type_matiere=type_matiere,
            numero_rc=numero_rc,
            numero_nif=numero_nif,
            numero_nis=numero_nis,
            numero_telephone=numero_telephone
        )

        # Enregistrer le fournisseur dans la base de données
        fournisseur.save()

        # Rediriger l'utilisateur vers la page hfrn
        return redirect('frn')

    # Si la requête n'est pas de type POST, afficher le formulaire vide
    return render(request, 'G_stock/frn.html')



#fin creation fournisseur


