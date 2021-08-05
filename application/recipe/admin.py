from django.contrib import admin
from .models import Tag, Ingredient


@admin.register(Tag)
class AdminTag(admin.ModelAdmin):
    pass


@admin.register(Ingredient)
class AdminIngredient(admin.ModelAdmin):
    pass
