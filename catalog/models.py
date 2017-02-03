# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.contrib.admin  import TabularInline, StackedInline

from django.contrib import admin
from django.contrib.admin  import TabularInline, StackedInline

from django.db import models
from django.utils.timezone import now

import os
from doors.settings import MEDIA_ROOT


STATUS_ORDER = (
    ("created", u"формируется"),
    ("processing", u"запрошен"),
    ("in_work", u"в работе"),
    ("sended", u"отправлен"),
    ("received", u"получен"),
)

# Create your models here.

def translit(t):
    symbols = (u"абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯій",
                u"abvgdeejzijklmnoprstufhzcssjyjeuaABVGDEEJZIJKLMNOPRSTUFHZCSSJYJEUAii")
    tr = {ord(a):ord(b) for a, b in zip(*symbols)}
    t = t.translate(tr)
    t = t.replace(" ", "_").lower()
    return t

class Question(models.Model):
  pub_date = models.DateTimeField(default=now,
                                  verbose_name=u"Date of adding")
  name = models.EmailField(verbose_name=u"Имя")
  contact = models.CharField(verbose_name=u"Контакт", max_length=255)
  question = models.TextField( verbose_name=u"Сообщение",
                               null=True, blank=True, )
     
  def __unicode__(self):
    return "%s,%s" %  (self.email, str(self.pub_date))


class Subscribing(models.Model):
  pub_date = models.DateTimeField(default=now,
                                  verbose_name=u"Date of adding")
  email = models.EmailField(verbose_name=u"Email")
  
  def __unicode__(self):
    return "%s,%s" %  (self.email, str(self.pub_date))



class Meta(models.Model):
    url = models.CharField(max_length=255,
                             verbose_name=u"URL", null=True, blank=True)
    keywords = models.CharField(max_length=255,
                           verbose_name=u"key words", null=True, blank=True)
    desc = models.CharField(max_length=255,
                           verbose_name=u"description", null=True, blank=True)

    def __unicode__(self):
        return self.url

class Chanel(models.Model):
    title = models.CharField(max_length=255,
                             verbose_name=u"Title", null=True, blank=True)
    ext_id = models.IntegerField(verbose_name=u"out_id", null=True, blank=True)

    def __unicode__(self):
        return self.title


        
class Content(models.Model):

    image = models.ImageField(upload_to='img', max_length=254, null=True, blank=True)

    title = models.CharField(max_length=255,
                             verbose_name=u"Title", null=True, blank=True)
    content = models.TextField(verbose_name=u"Title", null=True, blank=True)

    chanel = models.ForeignKey(Chanel, verbose_name=u"Chanel",
                                       related_name="chanel",
                                       blank=True, null=True)
    pub_date = models.DateTimeField(default=now,
                                    verbose_name=u"Date of adding")

    ordering = models.IntegerField(verbose_name=u"ordering", default=0,blank=True, null=True)

    def __unicode__(self):
        return "%s -> %s -> %s " % (self.chanel.title, self.title, str(self.pub_date) )




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


    opt1_typ = models.ForeignKey(Category, verbose_name = u"Каталог",null=True, blank=True, )
                               
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
        if self.opt3_brand:
            return "%s -> %s -> %s" % (self.opt1_typ,
                                       self.opt2_spec,
                                       self.opt3_brand.title)
        else:
            return "%s -> %s" % (self.opt1_typ,
                                 self.opt2_spec)




class Cart(models.Model):
    phone = models.CharField(verbose_name=u"Телефон", max_length=255, null=True, blank=True)
    fio = models.CharField(verbose_name=u"ФИО", max_length=255, null=True, blank=True)
    full_desc = models.TextField(verbose_name=u"полное описание",
                                 null=True, blank=True, )
    
    status = models.CharField(verbose_name=u"Статус", 
                              max_length=40,
                              choices=STATUS_ORDER, 
                              default='created' )
      
    count = models.IntegerField(verbose_name=u"Кол-во позиций")
    
    def total_price(self):
      total_price = 0
      for i in CartItem.objects.filter(cart=self):
        total_price += i.count*i.price
      return total_price
    
    class Meta:
      verbose_name = u"Заказ"
      verbose_name_plural = u"Заказы"


class CartItem(models.Model):
    count = models.IntegerField(verbose_name=u"Кол-во позиций", default=1)
    product = models.ForeignKey('Product', verbose_name=u"Товар")  
    price = models.DecimalField(default="0.0", max_digits=6, decimal_places=2,
                                verbose_name=u"Цена")
    
    is_package = models.BooleanField(verbose_name=u"Пакетный")  
    package = models.IntegerField(verbose_name=u"Пакет", 
                                  null=True, blank=True) 
    
    group = models.CharField(verbose_name=u"Группа пакета", 
                             null=True, blank=True,
                             max_length=255,
                             )     
    
    cart = models.ForeignKey(Cart, verbose_name="корзина")
    
    def total_price(self):
      return self.count*self.price
    
    def __unicode__(self):
       product = self.product
       return u"%s" % (self.product)
    
    class Meta:
      verbose_name = u"позиция в Корзине"
      verbose_name_plural = u"позиции в Корзине"


    
class CartItemInline(StackedInline):
    model = CartItem
    extra = 0
    class Meta:
      verbose_name = u"позиция в Корзине"
      verbose_name_plural = u"позиции в Корзине"


class CartAdmin(admin.ModelAdmin):
    inlines = [ CartItemInline ]
    list_display = ['phone', "fio", "full_desc", "total_price","count", "status"]
    list_filter = ('status', 'phone')
    
                            
                     
class Product(models.Model):
    order = models.IntegerField(verbose_name = u"порядок", default=0)

    title = models.CharField(max_length=255,
                               verbose_name=u"Название товара",
                               null=True, blank=True, )

    full_desc = models.TextField(
                               verbose_name=u"полное описание",
                               null=True, blank=True, )
    
    catalog_item = models.ForeignKey(CatItem, verbose_name = u"Каталог")  
    
    file1 = models.FileField(upload_to='file1', max_length=254,
                             verbose_name = u"Спецификация", null=True, blank=True )
    
    file2 = models.FileField(upload_to='file2', max_length=254,
                            verbose_name = u"Каталог pdf", null=True, blank=True)
    
    rate = models.IntegerField(default=3, verbose_name=u"Рейтинг")

    price = models.DecimalField(default="0.0", max_digits=6, decimal_places=2,
                                      verbose_name=u"Цена")

    is_discont = models.NullBooleanField(verbose_name=u"Акционный")

    ext_desc = models.TextField(
                                verbose_name=u"Дополнительное описание",
                                null=True, blank=True, )
                                      
    keywords = models.CharField(max_length=255,
                                verbose_name=u"KeyWords",
                                null=True, blank=True, )
                                
    description = models.CharField(max_length=255,
                                   verbose_name=u"Desciption",
                                   null=True, blank=True, )
                                   
    pub_date = models.DateTimeField(default=now,
                                    verbose_name=u"Date of adding")
    
    brand = models.ForeignKey(Brand,
                              verbose_name=u"Бренд",
                              null=True, blank=True, )

    status = models.BooleanField(verbose_name=u"Активный", default=True)
    
    def preview_image(self):
      img = Image.objects.filter(product=self).order_by("order").first()
      path = os.path.join(MEDIA_ROOT, str(img.image)) 
      print path
      if img and os.path.isfile(path):
	return img.url()
      else:
	return "/img/productImg.jpg"
      
    
    def __unicode__(self):
      return "%s -> %s " % (self.catalog_item,
                            self.title)
    
    class Meta:
        verbose_name = u"Товар"
        verbose_name_plural = u"Товары"

                                   
class Image(models.Model):
    order = models.IntegerField(verbose_name = u"порядок", default=0)
    product = models.ForeignKey(Product, verbose_name=u"Продукт" )
    image = models.ImageField(upload_to='photos', max_length=254)
    
    def url(self):
      return self.image.url
  
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
        return u"%s" % (self.title)
        
        
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
        return u"%s" % (self.product.title)
                                      

class CatItemAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        # custom stuff here

        
        obj.save()
        if obj.pk is None:
            new_chanel = Chanel(title=translit(obj.opt2_spec), ext_id=obj.pk)
            new_chanel.save()
        else:
            try:
                chanel = Chanel.objects.get(ext_id=obj.pk)
                chanel.title=translit(obj.opt2_spec)
                chanel.save()
            except Chanel.DoesNotExist:
                new_chanel = Chanel(title=translit(obj.opt2_spec), ext_id=obj.pk)
                new_chanel.save()

                                      

class PackageItemInline(StackedInline):
    model = PackageItem
    extra = 0

class PackageAdmin(admin.ModelAdmin):
    inlines = [ PackageItemInline ]
    list_display = ['title']


class ProductAdmin(admin.ModelAdmin):
    inlines = [ ImagesInline ]
    list_display = ['title', 'rate', 'price', 'catalog_item']
    class Media:
        js = (
            '//cdn.tinymce.com/4/tinymce.min.js',
            '/js/inline_admin.js',
        )


class CatItemInline(StackedInline):
    model = CatItem
    extra = 10

class CategoryAdmin(admin.ModelAdmin):
    inlines = [ CatItemInline ]
    list_display = ['title']
