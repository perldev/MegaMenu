# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.contrib.admin  import TabularInline, StackedInline

from django.contrib import admin
from django.contrib.admin  import TabularInline, StackedInline

from django.db import models

# Create your models here.

class Brand(models.Model):
    order = models.IntegerField(verbose_name = u"порядок", default=0)
    title = models.CharField(max_length=255,
                             verbose_name=u"Brand",
                             null=True, blank=True, )
    class Meta:
        verbose_name = u"Brand"
        verbose_name_plural = u"Brand-ы"

    def __unicode__(self):
        return self.title

class Category(models.Model):
    title = models.CharField(max_length=255,
                             verbose_name=u"Каталог",
                             null=True, blank=True, )

    class Meta:
        verbose_name = u"Каталог"
        verbose_name_plural = u"Каталоги"
                             
    def __unicode__(self):
        return self.title                         

                             
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

    class Meta:
        verbose_name = u"Категория каталога"
        verbose_name_plural = u"Категории каталога"

                                   
    def __unicode__(self):
        return "%s -> %s -> %s -> %s" % (self.catalog.title, self.opt1_typ,
                                         self.opt2_spec,
                                         self.opt3_brand.title)


                                   
class Product(models.Model):
    order = models.IntegerField(verbose_name = u"порядок", default=0)

    title = models.CharField(max_length=255,
                               verbose_name=u"Название товара",
                               null=True, blank=True, )
    
    catalog_item = models.ForeignKey(CatItem, verbose_name = u"Каталог")  
    
    file1 = models.FileField(upload_to='file1', max_length=254,
                             verbose_name = u"Спецификация")
    
    file2 = models.FileField(upload_to='file1', max_length=254,
                            verbose_name = u"Каталог pdf")
    
    rate = models.DecimalField(default="2.5", max_digits=2, decimal_places=1,
                                      verbose_name=u"Рейтинг")

    price = models.DecimalField(default="0.0", max_digits=6, decimal_places=2,
                                      verbose_name=u"Цена")

    is_discont = models.NullBooleanField(verbose_name=u"Акционный")

    ext_desc = models.CharField(max_length=255,
                                verbose_name=u"Дополнительное описание",
                                null=True, blank=True, )
                                      
    keywords = models.CharField(max_length=255,
                                verbose_name=u"KeyWords",
                                null=True, blank=True, )
                                
    description = models.CharField(max_length=255,
                                   verbose_name=u"Desciption",
                                   null=True, blank=True, )

    class Meta:
        verbose_name = u"Товар"
        verbose_name_plural = u"Товары"

                                   
class Image(models.Model):
    order = models.IntegerField(verbose_name = u"порядок", default=0)
    product = models.ForeignKey(Product, verbose_name=u"Продукт" )
    image = models.ImageField(upload_to='photos', max_length=254)

    class Meta:
        verbose_name = u"Картинка"
        verbose_name_plural = u"Картинки"

    
class ImagesInline(StackedInline):
    model = Image
    extra = 0


class Package(models.Model):
    order = models.IntegerField(verbose_name = u"порядок", default=0)
    title = models.CharField(max_length=255,
                             verbose_name=u"Название",
                             null=True, blank=True, )

    class Meta:
        verbose_name = u"Акционный пакет"
        verbose_name_plural = u"Акционный пакеты"
                             
    def __unicode__(self):
        return self.title
        
        
class PackageItem(models.Model):
    order = models.IntegerField(verbose_name = u"порядок", default=0)
    package = models.ForeignKey(Package, verbose_name = u"Пакет", null=True)
    product = models.ForeignKey(Product, verbose_name = u"Продукт")
    price = models.DecimalField(default="0.0", max_digits=6, decimal_places=2,
                                      verbose_name=u"Цена в пакете")

    class Meta:
        verbose_name = u"Позиция в акционном пакете"
        verbose_name_plural = u"Позиции в акционном пакете"

                                      
    def __unicode__(self):
        return str(self.product)
                                      


class PackageItemInline(StackedInline):
    model = PackageItem
    extra = 0

class PackageAdmin(admin.ModelAdmin):
    inlines = [ PackageItemInline ]
    list_display = ['title']


class ProductAdmin(admin.ModelAdmin):
    inlines = [ ImagesInline ]
    list_display = ['title', 'rate', 'price', 'catalog_item']
