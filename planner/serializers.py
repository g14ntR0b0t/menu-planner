from rest_framework import serializers

from .models import Ingredient, MeasureUnit, Type, Dish, MealGroupDetail, MealGroupType, Meal


class IngredientSerializer(serializers.ModelSerializer):
  measure_unit__name = serializers.CharField(source="measure_unit.name", read_only=True)
  
  class Meta:
    model = Ingredient
    fields = [
      'id',
      'name',
      'description',
      'measure_unit',
      'measure_unit__name',
      'image',
    ]
  
  def to_representation(self, instance):
    data = super().to_representation(instance)
    request = self.context.get('request')
    
    if instance.image and request:
      data['image'] = request.build_absolute_uri(instance.image.url)
    
    return data


class MeasureUnitSerializer(serializers.ModelSerializer):
  class Meta:
    model = MeasureUnit
    fields = '__all__'


class TypeSerializer(serializers.ModelSerializer):
  class Meta:
    model = Type
    fields = '__all__'


class MealGroupTypeSerializer(serializers.ModelSerializer):
  class Meta:
    model   = MealGroupType
    fields  = '__all__'


class MealGroupDetailSerializer(serializers.ModelSerializer):
  ingredient_id = serializers.PrimaryKeyRelatedField(
    queryset=Ingredient.objects.all(), source='ingredient'
  )
  measure_unit_id = serializers.PrimaryKeyRelatedField(
    queryset=MeasureUnit.objects.all(), source='measure_unit'
  )
  meal_group_type_id = serializers.PrimaryKeyRelatedField(
    queryset=MealGroupType.objects.all(), source='meal_group_type'
  )
  ingredient__name          = serializers.CharField(source='ingredient.name', read_only=True)
  measure_unit__name        = serializers.CharField(source='measure_unit.name', read_only=True)
  meal_group_type__name     = serializers.CharField(source='meal_group_type.name', read_only=True)
  ingredient__image__url    = serializers.SerializerMethodField()
  
  class Meta:
    model = MealGroupDetail
    fields = [
      'ingredient_id',
      'ingredient__name',
      'ingredient__image__url',
      'measure_unit_id',
      'measure_unit__name',
      'meal_group_type_id',
      'meal_group_type__name',
      'quantity',
      'annotations',
    ]
  
  def get_ingredient__image__url(self, obj):
    request = self.context.get('request')
    if obj.ingredient and obj.ingredient.image and hasattr(obj.ingredient.image, 'url'):
      return request.build_absolute_uri(obj.ingredient.image.url) if request else obj.ingredient.image.url
    return None
  

class DishSerializer(serializers.ModelSerializer):
  meal_group_details = MealGroupDetailSerializer(source='mealgroupdetail_set', many=True, read_only=True)
  image = serializers.SerializerMethodField()
  type_id = serializers.PrimaryKeyRelatedField(
    queryset=Type.objects.all(), source='type'
  )
  type__name  = serializers.CharField(source='type.name', read_only=True)
  
  class Meta:
    model = Dish
    fields = ['id', 'name', 'description', 'type_id', 'type__name', 'image', 'meal_group_details']
  
  def get_image(self, obj):
    request = self.context.get('request')
    if obj.image and hasattr(obj.image, 'url'):
      return request.build_absolute_uri(obj.image.url) if request else obj.image.url
    return None


class MealSerializer(serializers.ModelSerializer):
  type_id = serializers.PrimaryKeyRelatedField(
    queryset=Type.objects.all(), source='type'
  )
  type__name = serializers.CharField(source='type.name', read_only=True)
  dish_id = serializers.PrimaryKeyRelatedField(
    queryset=Dish.objects.all(), source='dish'
  )
  dish__name = serializers.CharField(source='dish.name', read_only=True)
  dish__description = serializers.CharField(source='dish.description', read_only=True)
  
  class Meta:
    model = Meal
    fields = [
      'id',
      'dish_id',
      'dish__name',
      'dish__description',
      'type_id',
      'type__name',
      'image',
      'date',
    ]
  
  def to_representation(self, instance):
    data = super().to_representation(instance)
    request = self.context.get('request')
    
    if instance.image and request:
      data['image'] = request.build_absolute_uri(instance.image.url)
    
    return data
