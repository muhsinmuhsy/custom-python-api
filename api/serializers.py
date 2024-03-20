from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User


        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class CategorySerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image:
            return request.build_absolute_uri(obj.image.url)
        return None

    class Meta:
        model = Category
        fields = '__all__'

class PersonalInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalInformation
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = '__all__'



class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = '__all__'

# class ProductSerializer(serializers.ModelSerializer):
#     product_variants = ProductVariantSerializer(many=True, required=False)

#     class Meta:
#         model = Product
#         fields = '__all__'

#     def create(self, validated_data):
#         product_variants_data = validated_data.pop('product_variants', [])
#         product = Product.objects.create(**validated_data)

#         for product_variant_data in product_variants_data:
#             ProductVariant.objects.create(product=product, **product_variant_data)

#         return product
    
#     def update(self, instance, validated_data):
#         # Update Product fields
#         instance.name = validated_data.get('name', instance.name)
#         instance.image = validated_data.get('image', instance.image)
#         # Update other fields as needed

#         # Update ProductVariant instances
#         product_variants_data = validated_data.pop('product_variants', [])
#         product_variants = instance.product_variants.all()

#         for index, product_variant_data in enumerate(product_variants_data):
#             product_variant_instance = product_variants[index]
#             product_variant_instance.name = product_variant_data.get('name', product_variant_instance.name)
#             product_variant_instance.actual_price = product_variant_data.get('actual_price', product_variant_instance.actual_price)
#             # Update other fields as needed
#             product_variant_instance.save()

#         instance.save()
#         return instance