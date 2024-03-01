from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from api.models import *
from api.serializers import *


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404


# -------------------------------------- Category ------------------------------------- #

@api_view(['GET'])
def category_list(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def category_add(request):
    # Handle GET requests here
    if request.method == 'GET':
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def category_view(request, category_id):
    category = Category.objects.get(id=category_id)
    if request.method ==  'GET':
        serializer = CategorySerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'DELETE'])
def category_delete(request, category_id):
    category = Category.objects.get(id=category_id)
    if request.method ==  'GET':
        serializer = CategorySerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'DELETE':
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PATCH'])
def category_edit(request, category_id):
    try:
        category = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        return Response({'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CategorySerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    elif request.method == 'PATCH':
        serializer = CategorySerializer(category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ------------------------------------Category and Product ------------------------------------- #

   
class CategoryWithProduct(APIView):
    def get(self, request, category_id, format=None):
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return Response({'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)

        category_serializer = CategorySerializer(category)
        products = Product.objects.filter(category=category)
        products_serializer = ProductSerializer(products, many=True)

        product_variants = ProductVariant.objects.filter(product__in=products)
        variant_serializer = ProductVariantSerializer(product_variants, many=True)

        response_data = {
            'category': category_serializer.data,
            'products': products_serializer.data,
            'variants': variant_serializer.data
        }

        return Response(response_data, status=status.HTTP_200_OK)

    
# ------------------------------------ Product and ProductVAriant ---------------------------------- #
    


class ProductList(APIView):
    def get(self, request, format=None):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ProductAdd(APIView):
    def get(self, request, format=None):
        products = Product.objects.all() 
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductDelete(APIView):
    def get(self, request, product_id, format=None):
        product = Product.objects.get(id=product_id)
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, product_id, format=None):
        product = Product.objects.get(id=product_id)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ProductEdit(APIView):
    def get(self, request, product_id, format=None):
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, product_id, format=None):
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    
class ProductWithVariants(APIView):
    def get(self, request, product_id, format=None):
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        product_serializer = ProductSerializer(product)
        productvariants = ProductVariant.objects.filter(product=product)
        variant_serializer = ProductVariantSerializer(productvariants, many=True)

        response_data = {
            'product': product_serializer.data,
            'variants': variant_serializer.data
        }

        return Response(response_data, status=status.HTTP_200_OK)
    


class ProductVariantList(APIView):
    def get(self, request, format=None):
        productvariants = ProductVariant.objects.all()
        serializer = ProductVariantSerializer(productvariants, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ProductVariantAdd(APIView):
    def get(self, request, format=None):
        productvariants = ProductVariant.objects.all() 
        serializer = ProductVariantSerializer(productvariants, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = ProductVariantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductVariantDelete(APIView):
    def get(self, request, productvariant_id, format=None):
        productvariant = ProductVariant.objects.get(id=productvariant_id)
        serializer = ProductVariantSerializer(productvariant)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, productvariant_id, format=None):
        productvariant = ProductVariant.objects.get(id=productvariant_id)
        productvariant.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ProductVariantEdit(APIView):
    def get(self, request, productvariant_id, format=None):
        try:
            productvariant = ProductVariant.objects.get(id=productvariant_id)
        except ProductVariant.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductVariantSerializer(productvariant)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, productvariant_id, format=None):
        try:
            productvariant = ProductVariant.objects.get(id=productvariant_id)
        except ProductVariant.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductVariantSerializer(productvariant, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)