from django.shortcuts import render
from rest_framework import viewsets, generics, status
from .models import Ingredient, MeasureUnit, Type, Dish, MealGroupType, MealGroupDetail, Meal
from .serializers import (IngredientSerializer, MeasureUnitSerializer, TypeSerializer, DishSerializer,
                          MealGroupTypeSerializer, MealSerializer)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
import json

# Create your views here.


class IngredientViewSet(viewsets.ModelViewSet):
  queryset = Ingredient.objects.all()
  serializer_class = IngredientSerializer
  parser_classes = (MultiPartParser, FormParser)


class MeasureUnitViewSet(viewsets.ModelViewSet):
  queryset = MeasureUnit.objects.all()
  serializer_class = MeasureUnitSerializer


class TypeViewSet(viewsets.ModelViewSet):
  queryset = Type.objects.all()
  serializer_class = TypeSerializer


class MealGroupTypeViewSet(viewsets.ModelViewSet):
  queryset = MealGroupType.objects.all()
  serializer_class = MealGroupTypeSerializer


class DishViewSet(viewsets.ModelViewSet):
  queryset          = Dish.objects.all()
  serializer_class  = DishSerializer


class DishCreateView(APIView):
  
  @staticmethod
  def post(request, *args, **kwargs):
    name        = request.POST.get('name', None)
    description = request.POST.get('description', None)
    type_id     = request.POST.get('type', None)
    image       = request.FILES.get('image', None)
    data        = request.POST.get('data', [])
    obj_dish    = Dish.objects.create(
      name=name,
      description=description,
      type_id=type_id,
      image=image
    )
    data = json.loads(data)
    
    for _mg in data:
      group   = _mg.get('group')
      items   = _mg.get('item')
      obj_group_type = MealGroupType.objects.get(id=group.get('id'))
      for item in items:
        ingredient_id = item.get('ingredient').get('id')
        measure_unit_id = item.get('measure_unit').get('id')
        quantity        = float(item.get('quantity'))
        obj_dish.mealgroupdetail_set.create(
          ingredient_id=ingredient_id,
          measure_unit_id=measure_unit_id,
          quantity=quantity,
          meal_group_type=obj_group_type
        )
    
    return Response({
      "success": True,
      "data": DishSerializer(obj_dish).data
    }, status=status.HTTP_201_CREATED)


class MealViewSet(viewsets.ModelViewSet):
  queryset = Meal.objects.all()
  serializer_class = MealSerializer
  parser_classes = (MultiPartParser, FormParser)
