from django.urls import path, include,re_path
from .views import (list_tags, view_tag, create_tag, update_tag, delete_tag)
from .views import (IngredientCreate, IngredientList, IngredientRetrieve, IngredientUpdate, IngredientDestroy)
from .views import RecipeViewSet

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('recipe', RecipeViewSet)

app_name = 'recipe'
print(router.urls)
urlpatterns = [
    path('', include(router.urls)),
    # Tag Urls
    path('tag-list', list_tags, name='tag-list'),
    path('tag-create', create_tag, name='tag-create'),
    path('tag-update', update_tag, name='tag-update'),
    re_path('^tag-view/(?P<pk>[^/.]+)/$', view_tag, name='tag-view'),
    path('tag-delete', delete_tag, name='tag-delete'),

    # Ingredient Urls
    path('ingredient-create', IngredientCreate.as_view(), name='ingredient-create'),
    path('ingredient-list', IngredientList.as_view(), name='ingredient-list'),
    path('ingredient-update', IngredientUpdate.as_view(), name='ingredient-update'),
    path('ingredient-view', IngredientRetrieve.as_view(), name='ingredient-view'),
    path('ingredient-delete', IngredientDestroy.as_view(), name='ingredient-delete'),

    # Recipe Urls

    # path('recipe-list',,name='recipe-list'),
]
