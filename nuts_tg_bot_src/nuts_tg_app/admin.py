from django.contrib import admin

from django.contrib import admin
from nuts_tg_app.models import Category, CategoryItem


class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    fields = ["name"]
    

class CategoryItemAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "category"]
    fields = ["name", "category"]
    
    
admin.site.register(Category, CategoryAdmin)
admin.site.register(CategoryItem, CategoryItemAdmin)

