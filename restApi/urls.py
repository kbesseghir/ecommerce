from django.urls import path 
from . import views 
from .views import *

urlpatterns = [
    path('all-products/',views.Productcreate.as_view(),name ='get'),
     path('create/',views.Productcreate.as_view(),name ='create'),
    path('product/<int:id>/', views.ProductDetail.as_view(), name=' get product_detail'),
    path('update/<int:id>/', views.ProductDetail.as_view(), name=' update product_detail'),
    path('delete/<int:id>/', views.ProductDetail.as_view(), name=' delete product_detail'),
    path('categories/<str:name>', views.FilterProductsView.as_view(), name='list_categories'), # Retrieve all products by category

    path('filtring-products/',views.FilterProductsByPrice.as_view(),name='filter_price'), #filtring by price 
    path('search/',views.SearchProducts.as_view(),name='Search'),  #.....
    path('categories/', CategoryList.as_view(), name='category_list'),
    path('categories/<int:id>/', CategoryDetail.as_view(), name='category_detail'),
    path('categories/<int:id>/products/', CategoryProductList.as_view(), name='category_product_list'),
    path('add_favorite/', AddFavoriteView.as_view(), name='add_favorite'),
    path('remove_favorite/<int:product>/', RemoveFavoriteView.as_view(), name='remove_favorite'),
    # path('promotions/', PromotionList.as_view(), name='promotion-list'),
    # path('shipping/', ShippingListAPIView.as_view(), name='shipping-list'),
    # path('shipping/create/', ShippingCreateAPIView.as_view(), name='shipping-create'),
    # path('shipping/<int:pk>/', ShippingDetailAPIView.as_view(), name='shipping-detail'),
    # path('shipping/<int:pk>/update/', ShippingUpdateAPIView.as_view(), name='shipping-update'),
    # path('shipping/<int:pk>/delete/', ShippingDeleteAPIView.as_view(), name='shipping-delete'),
    # path('shipping/<int:pk>/update-state/', ShippingStateUpdateAPIView.as_view(), name='shipping-update-state'),
    
    path('Deliveredhistory/', OrderDeliveredHistoryView.as_view(), name='order-history'),
    path('Pendinghistory/', OrderPendingHistoryView.as_view(), name='order-history'),

    # path('MyShippings/', ShippingHistoryView.as_view(), name='shipping-history'),
    path('user-profile/', UserProfileDetailView.as_view(), name='user-profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('recommended-products/', RecommendedProductsView.as_view(), name='recommended-products'),
    path('check-authentication/', CheckAuthenticationView.as_view(), name='check-authentication'),
    path('favorites/', FavoriteListView.as_view(), name='favorite-list'),
    
    
    
    ]



