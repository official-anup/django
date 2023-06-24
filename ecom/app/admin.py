from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Products,OrderPlaced,Customer,Cart
# Register your models here.

@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display=["id","user","name","locality","city","zipcode","state"]
 
@admin.register(Products)
class ProductModelAdmin(admin.ModelAdmin):
    list_display=["id","title","selling_price","discounted_price","description","brand","category","product_image"]   
    

# @admin.register(Cart)
# class CartModelAdmin(admin.ModelAdmin):
#     list_display=["id","user","Product","quantity"] 
admin.site.register(Cart)

@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display=["id","user","customer","customer_info","Product","quantity","ordered_date","status"] 
  
  #This is to generate link in admin panel in orderplaced section
    def customer_info(self,obj):
        link=reverse("admin:app_customer_change",args=[obj.customer.pk])
        return format_html('<a href="{}">{}</a>',link,obj.customer.name)
    
    def product_info(self,obj):
        link=reverse("admin:app_products_change",args=[obj.products.pk])
        return format_html('<a href="{}">{}</a>',link,obj.products.title)