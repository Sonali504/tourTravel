from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register([Cart,CartProduct,Product,Order,Customer,Category, ProductImage])