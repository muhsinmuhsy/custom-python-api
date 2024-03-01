from django.contrib import admin
from api.models import *

#00 Register your models here.

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductVariant)