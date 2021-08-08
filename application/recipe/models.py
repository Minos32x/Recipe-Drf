from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings


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

    def __str__(self):
        return self.title
