from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

import uuid
import os


class Tag(models.Model):
    class Meta:
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')
        ordering = ('id',)

    def __str__(self):
        return '{}'.format(self.name)

    name = models.CharField(_('Name'), max_length=255, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Ingredient(models.Model):
    class Meta:
        verbose_name = _('Ingredient')
        verbose_name_plural = _('Ingredients')
        ordering = ('name',)

    name = models.CharField(_('Name'), max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


def recipe_image_file_path(instance, filename):
    """
    Generate file path for recipe images
    """
    file_extension = filename.split('.')[-1]

    filename = f'{uuid.uuid4()}.{file_extension}'
    print("FILENAME -> ", filename)

    final_path = os.path.join('uploads/recipe/', filename)
    print("FINAL PATH -> ", final_path)

    return final_path


class Recipe(models.Model):
    class Meta:
        verbose_name = _('Recipe')
        verbose_name_plural = _('Recipes')
        ordering = ('-id',)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(_('Title'), max_length=255)
    time_in_minutes = models.SmallIntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    link = models.GenericIPAddressField(blank=True, null=True)
    ingredients = models.ManyToManyField('ingredient')
    tags = models.ManyToManyField('tag')
    image = models.ImageField(null=True, upload_to=recipe_image_file_path)

    def __str__(self):
        return self.title
