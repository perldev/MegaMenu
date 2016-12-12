# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.shortcuts import render
from rest_framework import serializers

# Create your views here.
from rest_framework import generics

from .models import Product, Brand, Category, CatItem, Image, Package, PackageItem


from django.db import models

# Create your models here.
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'title', 'catalog_item',
                  'file1', 'file2', 'rate', 'price',
                  'is_discont', 'ext_desc', 'description', 'keywords',
                  )


class BrandSerializer(serializers.ModelSerializer):

    class Meta:
        model = Brand
        fields = ('id', 'title' )


class CategorySerializer(serializers.ModelSerializer):


    class Meta:
        model = Category
        fields = ('id', 'title' )


class CatItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = CatItem
        fields = ('id', 'catalog', 'opt1_typ', 'opt2_spec', 'opt3_brand' )




class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('id', 'product', 'image')


class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = ('id', 'title' )



class PackageItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackageItem
        fields = ('id', 'product','price' )
    
