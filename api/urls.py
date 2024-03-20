from django.urls import path
from api.views import *

urlpatterns = [
    path('', index, name='index'),
    path('api_login/', api_login, name='api_login'),
    path('logout/', logout_view, name='logout'),
    
    path('category/list', category_list, name='category-list'),
    path('category/add', category_add, name='category-add'),
    path('category/<int:category_id>/view/', category_view, name='category-view'),
    path('category/<int:category_id>/delete/', category_delete, name='category-delete'),
    path('category/<int:category_id>/edit/', category_edit, name='category-edit'),

    path('category/<int:category_id>/products/',  CategoryWithProduct.as_view(), name='category-with-product'),

    path('product/list', ProductList.as_view(), name='product-list'),
    path('product/add/', ProductAdd.as_view(), name='product-add'),
    path('product/<int:product_id>/delete/', ProductDelete.as_view(), name='product-delete'),
    path('product/<int:product_id>/edit/', ProductEdit.as_view(), name='product-edit'),

    path('product/<int:product_id>/variants/', ProductWithVariants.as_view(), name='product-with-variants'),

    path('productvariants/', ProductVariantList.as_view(), name='productvariant-list'),
    path('productvariants/add/', ProductVariantAdd.as_view(), name='productvariant-add'),
    path('productvariants/<int:productvariant_id>/delete//', ProductVariantDelete.as_view(), name='productvariant-delete'),
    path('productvariants/<int:productvariant_id>/edit/', ProductVariantEdit.as_view(), name='productvariant-edit'),
    
    path('personalinformation/list', personalinformation_list, name='personalinformation-list'),
    path('personalinformation/add', personalinformation_add, name='personalinformation-add'),
    path('personalinformation/<int:personalinformation_id>/view/', personalinformation_view, name='personalinformation-view'),
    path('personalinformation/<int:personalinformation_id>/delete/', personalinformation_delete, name='personalinformation-delete'),
    path('personalinformation/<int:personalinformation_id>/edit/', personalinformation_edit, name='personalinformation-edit'),
    
    
    path('user/list', user_list, name='user-list'),
    path('register/', user_register, name='user_register'),
    path('login/', user_login, name='user_login'),
    path('logout/', user_logout, name='user_logout'),
    path('change_password/', change_password, name='change_password'),
    path('current_user/', current_user, name='current_user'),
]