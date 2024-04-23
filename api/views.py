from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib import messages
from django.contrib.auth import logout

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from api.models import *
from api.serializers import *


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm


@user_passes_test(lambda u: u.is_superuser, login_url='/api_login/')
def index(request):
    return render(request, 'index.html')

def api_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, 'Username does not exist.')
            return redirect('api_login')

        if user.check_password(password):
            authenticated_user = authenticate(request, username=username, password=password)
            if authenticated_user is not None:
                login(request, authenticated_user)
                messages.success(request, 'Login Successfully')
                return redirect('index')
            else:
                messages.error(request, 'Invalid login credentials.')
        else:
            messages.error(request, 'Incorrect password.')

        return redirect('api_login')
    # else:
    #     messages.error(request, 'Invalid user!')
        
    return render(request, 'api_login.html')

def logout_view(request):
    logout(request)
    return redirect('index')


def custom_404_view(request, exception):
    return render(request, '404.html', status=404)

def custom_500_view(request):
    return render(request, '500.html', status=500)

# -------------------------------------- Category ------------------------------------- #

# @api_view(['GET'])
# def category_list(request):
#     if request.method == 'GET':
#         categories = Category.objects.all()
#         serializer = CategorySerializer(categories, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def category_list(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def category_add(request):
    # Handle GET requests here
    if request.method == 'GET':
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True, context={'request': request})
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
        serializer = CategorySerializer(category, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'DELETE'])
def category_delete(request, category_id):
    category = Category.objects.get(id=category_id)
    if request.method ==  'GET':
        serializer = CategorySerializer(category, context={'request': request})
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
        serializer = CategorySerializer(category, context={'request': request})
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



# class CategoryWithProduct(APIView):
#     def get(self, request, category_id, format=None):
#         try:
#             # Attempt to fetch the category with the given category_id
#             category = Category.objects.get(id=category_id)
#         except Category.DoesNotExist:
#             # If the category does not exist, return a 404 response
#             return Response({'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)

#         # Serialize the category object
#         category_serializer = CategorySerializer(category)

#         # Fetch all products belonging to the category
#         products = Product.objects.filter(category=category)
#         products_data = []

#         # Iterate over each product to fetch its details and associated variants
#         for product in products:
#             # Serialize the product object
#             product_serializer = ProductSerializer(product)
            
#             # Fetch all variants associated with the current product
#             variants = ProductVariant.objects.filter(product=product)
            
#             # Serialize the variants
#             variant_serializer = ProductVariantSerializer(variants, many=True)
            
#             # Create a dictionary containing product details
#             product_data = product_serializer.data
            
#             # Add serialized variants to the product data under the key 'variants'
#             product_data['variants'] = variant_serializer.data
            
#             # Append the product data to the list of products
#             products_data.append(product_data)

#         # Create the response data containing the serialized category and products
#         response_data = {
#             'category': category_serializer.data,
#             'products': products_data,
#         }

#         # Return the response data along with a 200 OK status code
#         return Response(response_data, status=status.HTTP_200_OK)





# class CategoryWithProduct(APIView):
#     def get(self, request, category_id, format=None):
#         try:
#             category = Category.objects.get(id=category_id)
#         except Category.DoesNotExist:
#             return Response({'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)

#         category_serializer = CategorySerializer(category)

#         products = Product.objects.filter(category=category)
#         products_data = []

#         for product in products:
#             product_serializer = ProductSerializer(product)
#             variants = ProductVariant.objects.filter(product=product)
#             variant_serializer = ProductVariantSerializer(variants, many=True)
#             product_data = product_serializer.data
#             product_data['variants'] = variant_serializer.data
#             products_data.append(product_data)
            
#         response_data = {
#             'category': category_serializer.data,
#             'products': products_data,
#         }

#         return Response(response_data, status=status.HTTP_200_OK)
    
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
    
    
 # ------------------------------------ Personal Information ------------------------------------- #   
    
@api_view(['GET'])
def personalinformation_list(request):
    if request.method == 'GET':
        categories = PersonalInformation.objects.all()
        serializer = PersonalInformationSerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def personalinformation_add(request):
    # Handle GET requests here
    if request.method == 'GET':
        categories = PersonalInformation.objects.all()
        serializer = PersonalInformationSerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        serializer = PersonalInformationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
   
@api_view(['GET'])
def personalinformation_view(request, personalinformation_id):
    personalinformation = PersonalInformation.objects.get(id=personalinformation_id)
    if request.method ==  'GET':
        serializer = PersonalInformationSerializer(personalinformation)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'DELETE'])
def personalinformation_delete(request, personalinformation_id):
    personalinformation = PersonalInformation.objects.get(id=personalinformation_id)
    if request.method ==  'GET':
        serializer = PersonalInformationSerializer(personalinformation)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'DELETE':
        personalinformation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PATCH'])
def personalinformation_edit(request, personalinformation_id):
    try:
        personalinformation = PersonalInformation.objects.get(id=personalinformation_id)
    except personalinformation.DoesNotExist:
        return Response({'error': 'personalinformation not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PersonalInformationSerializer(personalinformation)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    elif request.method == 'PATCH':
        serializer = PersonalInformationSerializer(personalinformation, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

 # ------------------------------------ Auth ------------------------------------- #
    
@api_view(['GET'])
def user_list(request):
    if request.method == 'GET':
        categories = User.objects.all()
        serializer = UserSerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


@api_view(['POST'])
def user_register(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
@api_view(['POST'])
def user_login(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')
        if username is None or password is None:
            return Response({'error': 'Please provide both username and password'}, status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)



@api_view(['POST'])
def user_logout(request):
    if request.method == 'POST':
        logout(request)
        return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
    

@api_view(['POST'])
def change_password(request):
    if request.method == 'POST':
        user = request.user
        data = request.data
        form = PasswordChangeForm(user, data)
        if form.is_valid():
            user = form.save()
            # This line ensures that the user stays logged in after changing their password
            update_session_auth_hash(request, user)
            return Response({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)
        else:
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
        
@api_view(['GET'])
def current_user(request):
    if request.method == 'GET':
        user = request.user
        if user.is_authenticated:
            # Assuming you have a serializer for the User model
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'User is not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)