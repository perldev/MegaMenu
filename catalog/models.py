# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Brand(models.Model):
    order = models.IntegerField(verbose_name = u"порядок", default=0)
    title = models.CharField(max_length=255,
                             verbose_name=u"Brand",
                             null=True, blank=True, )

class Category(models.Model):
    title = models.CharField(max_length=255,
                             verbose_name=u"Каталог",
                             null=True, blank=True, )

                             
class CatItem(models.Model):
    order = models.IntegerField(verbose_name = u"порядок", default=0)

    catalog = models.ForeignKey(Category, verbose_name = u"Каталог")

    opt1_typ = models.CharField(max_length=255,
                               verbose_name=u"Тип товара",
                               null=True, blank=True, )
                               
    opt2_spec = models.CharField(max_length=255,
                               verbose_name=u"Вид товара",
                               null=True, blank=True, )
                               
    opt3_brand = models.ForeignKey(Brand, 
                                   verbose_name=u"Бренд",
                                   null=True, blank=True, )



                                   
class Product(models.Model):
    order = models.IntegerField(verbose_name = u"порядок", default=0)

    title = models.CharField(max_length=255,
                               verbose_name=u"Вид товара",
                               null=True, blank=True, )
    
    catalog_item = models.ForeignKey(CatItem, verbose_name = u"Каталог")  
    
    file1 = models.FileField(upload_to='file1', max_length=254)
    
    file2 = models.FileField(upload_to='file1', max_length=254)
    
    rate = models.DecimalField(default="2.5", max_digits=2, decimal_places=1,
                                      verbose_name=u"Рейтинг")

    price = models.DecimalField(default="0.0", max_digits=6, decimal_places=2,
                                      verbose_name=u"Цена")

    is_discont = models.NullBooleanField(verbose_name=u"Акционный")

    ext_desc = models.CharField(max_length=255,
                                verbose_name=u"Description",
                                null=True, blank=True, )
                                      
    keywords = models.CharField(max_length=255,
                                verbose_name=u"KeyWords",
                                null=True, blank=True, )
                                
    description = models.CharField(max_length=255,
                                   verbose_name=u"Desciption",
                                   null=True, blank=True, )

class Image(models.Model):
    order = models.IntegerField(verbose_name = u"порядок", default=0)
    product = models.ForeignKey(Product, verbose_name=u"Продукт" )
    image = models.ImageField(upload_to='photos', max_length=254)



class Package(models.Model):
    order = models.IntegerField(verbose_name = u"порядок", default=0)
    title = models.CharField(max_length=255,
                             verbose_name=u"Акционный пакет",
                             null=True, blank=True, )

class PackageItem(models.Model):
    order = models.IntegerField(verbose_name = u"порядок", default=0)
    product = models.ForeignKey(Product, verbose_name = u"Продукт")
    price = models.DecimalField(default="0.0", max_digits=6, decimal_places=2,
                                      verbose_name=u"Цена в пакете")

                                      
    
    