from django.contrib import admin

# Register your models here.
from .models import *
class CategoryAdmin(admin.ModelAdmin):
    list_display=('name','image','description')

admin.site.register(Category,CategoryAdmin)
admin.site.register(Products)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Profile)
