from django.db import models
from django.utils import timezone

# Create your models here.
class MeasureUnit(models.Model):
  name          = models.CharField(max_length=50)
  abbreviation  = models.CharField(max_length=25, blank=True, null=True)
  active        = models.BooleanField(default=True)
  count         = models.BooleanField(default=False)


class Ingredient(models.Model):
  name          = models.CharField(max_length=120)
  description   = models.TextField(blank=True, null=True)
  measure_unit  = models.ForeignKey(MeasureUnit, null=True, on_delete=models.PROTECT)
  image         = models.ImageField(upload_to='ingredient_images/', blank=True, null=True)


class Type(models.Model):
  name        = models.CharField(max_length=50)
  annotations = models.TextField(blank=True, null=True)
  time        = models.TimeField()


class Dish(models.Model):
  name        = models.CharField(max_length=255, blank=True, null=True)
  description = models.TextField(blank=True, null=True)
  type        = models.ForeignKey(Type, on_delete=models.PROTECT)
  image       = models.ImageField(upload_to='dish_images/', blank=True, null=True)


class MealGroupType(models.Model):
  name        = models.CharField(max_length=120)
  description = models.TextField(blank=True, null=True)
  active      = models.BooleanField(default=True)


class MealGroupDetail(models.Model):
  ingredient    = models.ForeignKey(Ingredient, on_delete=models.PROTECT)
  quantity      = models.FloatField(default=0)
  measure_unit  = models.ForeignKey(MeasureUnit, on_delete=models.PROTECT)
  dish          = models.ForeignKey(Dish, on_delete=models.CASCADE, blank=True, null=True)
  annotations   = models.TextField(blank=True, null=True)
  meal_group_type = models.ForeignKey(
    MealGroupType,
    blank=True,
    null=True,
    on_delete=models.PROTECT
  )


class Meal(models.Model):
  date  = models.DateTimeField(default=timezone.localtime)
  dish  = models.ForeignKey(Dish, on_delete=models.CASCADE)
  type  = models.ForeignKey(Type, on_delete=models.PROTECT)
  image = models.ImageField(upload_to='meal_photos/', blank=True, null=True)
