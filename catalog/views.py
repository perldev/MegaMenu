from django.shortcuts import render

# Create your views here.
from rest_framework import generics

from .models import Product, Brand, Image,  Category, CatItem
from .serializers import ProductSerializer, BrandSerializer, ImageSerializer
from .serializers import CategorySerializer, CatItemSerializer

from django.conf import settings
from django.shortcuts import render_to_response, get_object_or_404, redirect, render


def index(request):
    context = {}
    return render(request, 'index.html', context)

def catalog(request):
    context = {}
    return render(request, 'catalog.html', context)

def contacts(request):
    context = {}
    return render(request, 'contacts.html', context)

def faq(request):
    context = {}
    return render(request, 'faq.html', context)




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