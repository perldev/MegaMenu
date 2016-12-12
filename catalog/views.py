from django.shortcuts import render

# Create your views here.
from rest_framework import generics

from .models import Product, Brand, Image,  Category, CatItem
from .serializers import ProductSerializer, BrandSerializer, ImageSerializer
from .serializers import CategorySerializer, CatItemSerializer




class ProductDetail(generics.ListCreateAPIView):
    """
    API endpoint that represents a single user.
    """
    queryset = Product.objects.all()
    model = Product
    serializer_class = ProductSerializer


class BrandDetail(generics.ListCreateAPIView):
    """
    API endpoint that represents a single user.
    """
    model = Brand
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

class CategoryDetail(generics.ListCreateAPIView):
    """
    API endpoint that represents a single user.
    """
    model = Category
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CatItemDetail(generics.ListCreateAPIView):
    """
    API endpoint that represents aCatItem single user.
    """
    model = CatItem
    queryset = CatItem.objects.all()
    serializer_class = CatItemSerializer


class ImageDetail(generics.ListCreateAPIView):
    """
    API endpoint that represents a single user.
    """
    model = Image
    queryset = Image.objects.all()
    serializer_class = ImageSerializer