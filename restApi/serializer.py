from erp_app.models import *
from rest_framework import serializers 

# class NotificationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Notification
#         fields ='__all__'


class PromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = '__all__'
    # notifications = NotificationSerializer(many=True, read_only=True)



# Serializer for the Product model
class ProductSerializer(serializers.ModelSerializer):
    # Define each field in the serializer
    name = serializers.CharField(max_length=255)
    image = serializers.ImageField(use_url=True)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    quantity = serializers.IntegerField()
    category = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=400)
    discounted_price = serializers.SerializerMethodField()
    

    
    # Method to get the discounted price for the product
    def get_discounted_price(self, obj):
        return obj.get_discounted_price()
    
    class Meta:
        model = Product  # Replace "Product" with your actual model name
        ref_name = 'RestApiProductSerializer'
        fields = '__all__'

# Serializer for the Category model
class CategorySerializer(serializers.ModelSerializer):
    # Define each field in the serializer
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=400)

    class Meta:
        model = Category
        fields = '__all__'

class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'



# class ShippingSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Shipping
#         fields = '__all__'

# class ShippingUpdateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Shipping
#         fields = ['state','address']



class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)
    class Meta:
        ref_name = 'RestApiPasswordChangeSerializer'