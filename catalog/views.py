# -*- coding: utf-8 -*-

from django.shortcuts import render

from django.db.models import Q

# Create your views here.
from rest_framework import generics

from .models import Product, Brand, Image,  Category, CatItem
from .serializers import ProductSerializer, BrandSerializer, ImageSerializer
from .serializers import CategorySerializer, CatItemSerializer

from django.contrib.auth.models import User
from .models import Content, Chanel, Cart, CartItem, Package, PackageItem, Subscribing, Question, Brand


from django.conf import settings
from django.shortcuts import render_to_response, get_object_or_404, redirect, render
from helpers import http403json, http200json
from django.forms import ModelForm
from django.http import Http404
import random



def index(request):
    context = {}
    return render(request, 'index.html', context)

def catalog(request, catalog_id=None):
  
    if catalog_id == "window":
      catalog_id = 1
    
    if catalog_id == "doors": 
      catalog_id = 2
      
    context = {}
    i = 1
    cats_title = {}
    cats = []
    cats_discont = []
    for ch in Category.objects.all().order_by("id"):
        art_cats = []
        arts_discont = []
        count_discont = 0
        count = 0
        for item in CatItem.objects.filter(opt1_typ = ch).order_by("order"):
            count_tmp = Product.objects.filter(catalog_item=item.id).count()
            count_tmp_discont = Product.objects.filter(catalog_item=item.id,
                                                      is_discont=True).count()

            if count_tmp_discont>0:
                arts_discont.append({"item": item,
                                     "title": item.opt2_spec,
                                     "count": count_tmp_discont})
                count_discont+=count_tmp_discont

            art_cats.append({"item": item,
                             "title": item.opt2_spec,
                             "count": count_tmp})
                             
            count += count_tmp
            cats_title[item.id] = item.opt2_spec
            
        
        cats.append({"sub":art_cats, "title": ch.title, "count": count})
        if count_discont>0:
            cats_discont.append({"sub":arts_discont,
                                 "title": ch.title,
                                 "count": count_discont
                                 })


    context["menu"]=cats
    context["discont_menu"] = cats_discont
    
    cat_title = None
    sorting = "-pub_date"
    if request.GET.get("price_desc", None):
      context["price_sorting"] = "price_desc"
      sorting = "-price"
      
    if request.GET.get("price_asc", None):
      context["price_sorting"] = "price_asc"  
      sorting="price"
    
    if catalog_id:
        q_list = Q(status=True)
        q_list &= Q(catalog_item__opt1_typ_id=catalog_id)
        is_discont = request.GET.get("discont", None)
        if is_discont:
            q_list &= Q(is_discont=True)
            context["is_discont"] = True
            
        brand = request.GET.get("brand", None)
        if brand:
            q_list &= Q(brand_id=brand)
            context["current_brand"] = int(brand)


        context["current"] = catalog_id
        context["cat_title"] = cats_title[context["current"]]
        context["current_chanel"] = CatItem.objects.get(id=context["current"])

        context["current_list"] = Product.objects.filter(q_list).order_by(sorting)
        
    else:
        our_list = get_last_products(6)
        q_list = Q(status=True)
        is_discont = request.GET.get("discont", None)
        if is_discont:
            q_list &= Q(is_discont=True)
            context["is_discont"] = True


        brand = request.GET.get("brand", None)
        if brand:
            q_list &= Q(brand_id=brand)
            context["current_brand"] = int(brand)



        context["current_list"] = Product.objects.filter(q_list).order_by(sorting)
    return render(request, 'catalog.html', context)


def catalog_sub_cat(request, cat_id):
    context = {}

    fill_product_context(cat_id, context)
    q_list = Q(status=True) & Q(catalog_item_id=context["current"])

    is_discont = request.GET.get("discont", None)
    if is_discont:
        q_list &= Q(is_discont=True)
        context["is_discont"] = True

    brand = request.GET.get("brand", None)
    if brand:
        q_list &= Q(brand_id=brand)
        context["current_brand"] = int(brand)
        
    sorting = "-pub_date"
    if request.GET.get("price_desc", None):
      context["price_sorting"] = "price_desc"
      sorting = "-price"
      
    if request.GET.get("price_asc", None):
      context["price_sorting"] = "price_asc"  
      sorting="price"
      
    context["current_list"] = Product.objects.filter(q_list).order_by(sorting)

    
    return render(request, 'catalog.html', context)

def fill_product_context(cat_id, context):
    i = 1
    cats = []
    cats_title = {}
    context["current"] = int(cat_id)
    cats_discont = []

    for ch in Category.objects.all().order_by("id"):
        art_cats = []
        count = 0
        arts_discont = []
        count_discont = 0
        for item in CatItem.objects.filter(opt1_typ = ch).order_by("order"):
                count_tmp = Product.objects.filter(catalog_item=item.id).count()
                art_cats.append({"item": item,
                                "title": item.opt2_spec,
                                "count": count_tmp})
                count += count_tmp
                count_tmp_discont = Product.objects.filter(catalog_item=item.id,
                                                        is_discont=True).count()

                if count_tmp_discont>0:
                    arts_discont.append({"item": item,
                                        "title": item.opt2_spec,
                                        "count": count_tmp_discont
                                        })
                    count_discont+=count_tmp_discont

                cats_title[item.id] = item.opt2_spec

        if count_discont>0:
            cats_discont.append({"sub":arts_discont, "title": ch.title, "count":count_discont})

        cats.append({"sub":art_cats, "title": ch.title, "count": count})

    context["menu"] = cats
    context["discont_menu"] = cats_discont
    context["cat_title"] = cats_title[context["current"]]
    context["current_chanel"] = CatItem.objects.get(id=context["current"])


def brands(request):
    context = {}
    return render(request, 'brands.html', context)
    
def contacts(request):
    context = {}
    return render(request, 'contacts.html', context)
    
def product(request, pk):
    context = {}
    product = get_object_or_404(Product, id=pk)
    cat_id = product.catalog_item.id
    fill_product_context(cat_id, context)
    
    
    context["product"] = product
    context["product_images"] = Image.objects.filter(product=product).order_by("order")
    context["seemed_prod"] = get_last_products(3, cat_id)
    context["meta_description"] = product.description
    context["meta_keywords"] = product.keywords    
    context["pagetitle"] = product.title   
    return render(request, 'product.html', context)
    
def faq(request):
    context = {}
    return render(request, 'faq.html', context)

def blog_cat(request, cat_id):
    return blog(request, cat_id)


def blog(request, cat_id=None):
    context = {}
    i = 1
    cats = []
    cats_title = {}
    for ch in Category.objects.all().order_by("id"):
       art_cats = []
       
       for item in CatItem.objects.filter(opt1_typ = ch).order_by("order"):
            art_cats.append({"item": item,
                             "title": item.opt2_spec,
                             "count": Content.objects.filter(chanel__ext_id=item.id).count()})
            cats_title[item.id] = item.opt2_spec
            
       cats.append({"sub":art_cats, "title": ch.title})

    context["menu"]=cats
    
    cat_title = None
    if cat_id:
        context["current"] = int(cat_id)
        context["cat_title"] = cats_title[context["current"]]
        context["current_chanel"] = Chanel.objects.get(ext_id=context["current"])
        our_list = list(Content.objects.filter(chanel__ext_id=context["current"]))
        res_list =  zip(*[iter(our_list)]*2)
        if len(our_list) % 2 >0:
          res_list.append((our_list[-1:][0], None))         
        
        context["current_list"] = res_list 
    else:
        our_list = get_last_articles(6)
        res_list =  zip(*[iter(our_list)]*2)
        if len(our_list) % 2 >0:
          res_list.append((our_list[-1:][0], None))         
        
        context["current_list"] = res_list 
    return render(request, 'blog.html', context)
  
def get_last_articles(num):
  art_cats = []

  for ch in Category.objects.all().order_by("id"):
      for item in CatItem.objects.filter(opt1_typ = ch).order_by("order"):
	art_cats.append(item.id)
      
  
  return list(Content.objects.filter(chanel__ext_id__in=art_cats)[:num])
      
            
      

def get_last_products(num, cat_id=None):
  if cat_id is None:
    return Product.objects.filter(status=True)[:num]
  else:
    return Product.objects.filter(status=True, catalog_item_id=cat_id)[:num]

def blog_item(request, item_id):

    context = {}
    content = Content.objects.get(id=item_id)
    context["current"] = content.chanel.id
    context["article"] = content
    i = 1
    cats = []
    cats_title = {}
    
    for ch in Category.objects.all().order_by("id"):
       art_cats = []
       for item in CatItem.objects.filter(opt1_typ = ch).order_by("order"):
            art_cats.append({"item": item,
                             "title": item.opt2_spec,
                             "count": Content.objects.filter(chanel__ext_id=item.id).count()})
            
            cats_title[item.id] = item.opt2_spec
            
       cats.append({"sub":art_cats, "title": ch.title})

    context["menu"]= cats   
    context["cat_title"] = cats_title[context["current"]]
    context["current_chanel"] = Chanel.objects.get(ext_id=context["current"])

    return render(request, 'article.html', context)

    
def custom_page(request, name):
    context = {}
    
    if name == "company":
        return render(request, 'company.html', context)
    

# TODO add captcha
def send_marina(request):
    
    f = AskForm(request.POST, request.FILES)
    content_item = f.save()
    return http200json(request, {"status": True})

    
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


class AskForm(ModelForm):
    class Meta:
        model = Question
        fields = [ 'contact', 'name', 'question']
        

class ContentForm(ModelForm):
    class Meta:
        model = Content
        fields = [ 'title', 'content', 'image','ordering']

## working with cart
def add_product2cart(request, product, price, count, package=None, group=None):
  
    cart_id = request.session.get('cart_id')
    cart = None
    if request.session.get('cart_id', False):
      try:
        cart = Cart.objects.get(id=cart_id)
      except Cart.DoesNotExist:
        cart = Cart(count=count)
        cart.save()
        request.session["cart_id"] = cart.id
    
    else:
      cart = Cart(count=count)
      cart.save()
      request.session["cart_id"] = cart.id
    
    if package is None:
      item = CartItem(count=count, product=product, price=price, is_package=False, cart=cart)
      item.save()	 
    else:
      item = CartItem(count=count, product=product, price=price, is_package=True, 
                      package=package.id, cart=cart, group=group)
      item.save()	 
    
    return True


def get_group4cart(cart):
   for i in range(1, 5):
      group = random.choice(
                (
                    "azure",
                    "AliceBlue",
                    "Bisque",
                    "FloralWhite",
                    "HoneyDew"
                )
            )
      try:
          CartItem.objects.get(group=group, cart=cart)
      except CartItem.DoesNotExist:
          return group

  
  
      
      
      
def cart_add_item(request, item_id, count):
  product = get_object_or_404(Product, pk=item_id)
  add_product2cart(request, product, product.price, int(count))
  return http200json(request, {"status": True})


def cart_add_package(request, package_id):
    cart_id = request.session.get('cart_id', False)
    if cart_id:
      cart = get_object_or_404(Cart, pk=cart_id)
      package = get_object_or_404(Package, pk=package_id)
      group = get_group4cart(cart)
      for package_item in PackageItem.objects.filter(package_id=package_id):
          add_product2cart(request,
                           package_item.product, 
                           package_item.price, 1, package, group)
    
      context = {}
      context["cart"] = cart
      context["cart_item_list"] = CartItem.objects.filter(cart=cart)
      return http200json(request, {"status": True}) 
    else:
      return http403json(request)

def subscribe_add(request):
  email =  request.GET.get("email", None)
  if email:
    Subscribing(email=email).save()
    return http200json(request,  {"status": True})
  else:
    return http403json(request)


def change_count_item(request, item_id, count):
   if request.session.get('cart_id', False):
      cart = get_object_or_404(Cart, pk=cart_id)
      context = {}
      cart_item = CartItem.objects.get(id=item_id)
      cart_item.count = count
      cart_item.save()
      
      return render_to_response(request, "confirm_order.html", context) 
   else:
      raise Http404(u"Заказ не найден")


def cart_change_item(request, item_id, count):
    cart_id = request.session.get('cart_id', False)

    if cart_id:
      cart = get_object_or_404(Cart, pk=cart_id)
      context = {}
      item = get_object_or_404(CartItem, pk=item_id)
      item.count = int(count)
      item.save()
      count = 0
      total_price = 0
      for i in CartItem.objects.filter(cart=cart):
          count += i.count
          total_price += i.count*i.price
      cart.count = count      
      cart.save() 
      return http200json(request, {"status": True,
                                  "count": count,
                                  "price": str(total_price)}) 
    else:
      raise Http404(u"Заказ не найден")
  
def cart_del_item(request, item_id):

    cart_id = request.session.get('cart_id', False)

    if cart_id:
      cart = get_object_or_404(Cart, pk=cart_id)
      context = {}
      item = CartItem.objects.get(id=item_id)
      if item.is_package:
         CartItem.objects.filter(group=item.group).delete()
      else:
         item.delete()

      count = 0
      total_price = 0
      for i in CartItem.objects.filter(cart=cart):
        count += i.count
        total_price += i.count*i.price
      cart.count = count
      cart.save() 
     
      return http200json(request, {"status": True,
                                   "count": count,
                                   "price": str(total_price)}) 
    else:
      raise Http404(u"Заказ не найден")

def cart(request):
    cart_id = request.session.get('cart_id', False)
    if cart_id:
      cart = get_object_or_404(Cart, pk=cart_id)
      
      context = {}
      context["cart"] = cart
      context["cart_item_list"] = CartItem.objects.filter(cart=cart).order_by("package")
      
    else:
      cart = Cart(count=0)
      cart.save()
      request.session["cart_id"] = cart.id
      context = {}
      context["cart"] = cart
      context["cart_item_list"] = []
      
      
    return render(request, "cart.html", context)   
      
  
def cart_confirm(request):
    cart_id = request.session.get('cart_id', False)
    if cart_id:
      cart = get_object_or_404(Cart, pk=cart_id)
      
      context = {}
      context["cart"] = cart
      context["cart_item_list"] = CartItem.objects.filter(cart=cart)
      return render(request, "cart_confirm.html", context) 
    else:
      raise Http404(u"Заказ не найден")



def cart_approve(request):
    context = {}
    cart_id = request.session.get('cart_id', False)
    if cart_id:
      cart = Cart.objects.get(id=cart_id)
      phone = request.POST.get("phone", None)
      fio = request.POST.get("fio", None)
      full_desc = request.POST.get("full_desc", None)
      cart.phone = phone
      cart.fio = fio
      cart.full_desc = full_desc
      cart.status="processing"
      cart.save()
      context["cart_item_list"] = CartItem.objects.filter(cart=cart)
      request.session["cart_id"] = None
      context["cart"] = cart
      return render(request, "approve_order.html", context) 
    else:
      raise Http404(u"Заказ не найден")




def delete_chanel(request, cat):

    try:
        chanel = request.POST.get("id_chanel", None)
        content_item = Content.objects.get(id=cat)
        content_item.delete()

    except Content.DoesNotExist:
        return http403json(request)

    return http200json(request, {"status": True})


def edit_chanel(request):
    content_item = None
    try:
        chanel = request.POST.get("id_chanel", None)
        content_item = Content.objects.get(id=chanel)
    except Content.DoesNotExist:
        return http403json(request)


    f = ContentForm(request.POST, request.FILES, instance=content_item)
    f.save()
    return http200json(request, {"status": True})

def add_chanel(request):
    chanel = None

    try:
        chanel = request.POST.get("id_chanel", None)
        chanel = Chanel.objects.get(title=chanel)
    except Chanel.DoesNotExist:
        return http403json(request)

    f = ContentForm(request.POST, request.FILES)

    content_item = f.save()
    content_item.chanel = chanel
    content_item.save()
    return http200json(request, {"status": True})


def setup_custom_meta(req, NewContext):
    Path = req.get_full_path()
    try:
        custom_meta = Meta.objects.get(url=Path)
        NewContext["meta_description"] = custom_meta.desc
        NewContext["meta_keywords"] = custom_meta.keywords
        return NewContext
    except:
        return NewContext
      

def search(request):
  search_str = request.GET.get("str", None)
  context = {}
  found  = Content.objects.filter(Q(title__contains=search_str)|
                                  Q(content__contains=search_str)).order_by("-pub_date")
  found_product  = Product.objects.filter(Q(title__contains=search_str)|
                                          Q(full_desc__contains=search_str)|
                                          Q(description__contains=search_str)
                                          ).order_by("rate")
  result = []
  for item in found_product:
    result.append({"url": "/product_%i" % item.id,
                   "title":item.title, "content":item.full_desc, "product": True })
   
  for item in found:
    result.append({"url": "/blog_item_%i" % item.id,
                   "title":item.title, "product": False,  })
    
  context["search_list"] = result
  return render(request, 'search_list.html', context)


def search_product(request):
    search_str = request.GET.get("str", None)

    found_product  = Product.objects.filter(Q(title__contains=search_str)|
                                            Q(full_desc__contains=search_str)|
                                            Q(description__contains=search_str)
                                            ).order_by("rate")

    context = {}
    i = 1
    cats_title = {}
    cats = []
    cats_discont = []
    for ch in Category.objects.all().order_by("id"):
        art_cats = []
        arts_discont = []
        count_discont = 0
        count = 0
        for item in CatItem.objects.filter(opt1_typ = ch).order_by("order"):
            count_tmp = Product.objects.filter(catalog_item=item.id).count()
            count_tmp_discont = Product.objects.filter(catalog_item=item.id,
                                                      is_discont=True).count()

            if count_tmp_discont>0:
                arts_discont.append({"item": item,
                                     "title": item.opt2_spec,
                                     "count": count_tmp_discont})
                count_discont+=count_tmp_discont

            art_cats.append({"item": item,
                             "title": item.opt2_spec,
                             "count": count_tmp})
                             
            count += count_tmp
            cats_title[item.id] = item.opt2_spec
            
        
        cats.append({"sub":art_cats, "title": ch.title, "count": count})
        if count_discont>0:
            cats_discont.append({"sub":arts_discont,
                                 "title": ch.title,
                                 "count": count_discont
                                 })


    context["menu"]=cats
    context["discont_menu"] = cats_discont
    context["current_list"] = found_product
    return render(request, 'catalog.html', context)


def content_chanels(request):
    context = {}
    for ch in Chanel.objects.all():
        context[ch.title] = Content.objects.filter(chanel = ch).order_by('ordering')
  
    cats = {}
    discont_cats = {}
    num2name = {1:"cat_window", 2:"cat_doors"}
    i = 1
    for ch in Category.objects.all():
        
       cats[num2name[i]] = [ item for item in CatItem.objects.filter(opt1_typ = ch).order_by("order")]
       cats[num2name[i]+"_title"] = ch.title
       i+=1

    discont_count = Product.objects.filter(is_discont=True).count()    
    cart_count = 0
    cart_id = request.session.get('cart_id', False)
    if cart_id:
      cart = Cart.objects.get(id=cart_id)
      count = 0
      for i in CartItem.objects.filter(cart=cart):
          count += i.count
      cart.count = count
      cart.save()
      
      cart_count = cart.count
      
    
    COMPANY_ID = 1
    context["catalog_current_discont"] = context["current_discont"][0]
    context["about_company"] = [Content.objects.get(id=COMPANY_ID)]
    popular = [] 
    
    
    discont_products = []
    
    
    
    
    product = Product.objects.random_discont()
    discont_products.append(product)
    product = Product.objects.random_discont()   
    discont_products.append(product)
    product = Product.objects.random_discont()   
    discont_products.append(product)

    
    
    
    product = Product.objects.random()
    popular.append(product)
    product = Product.objects.random()
    popular.append(product)
    product = Product.objects.random()   
    popular.append(product)
    
    product = Product.objects.random()   
    popular.append(product)
    
    
    res_contex = None
    if request.user.is_authenticated() and request.user.is_staff:
        res_context = {"cats":cats,
                      'chanels': context,
                      "discont_count": discont_count,
                      'is_admin': True,
                      "cart_count": cart_count,
                      
                      }
    else:
        res_context = {"cats":cats,
                      'chanels': context,
                      "discont_count": discont_count,
                      "cart_count": cart_count
                      }
    res_context = setup_custom_meta(request, res_context)
    res_context["popular"] = popular[:3]
    res_context["popular1"] = popular

    res_context["discont_products"] = discont_products
    pack = Package.objects.random()
    pack_sum = 0
    pack_list = []
    for packitem in PackageItem.objects.filter(package = pack).order_by("order"):
      pack_sum+= packitem.price
      pack_list.append(packitem)
      
    res_context["random_package"] = {"package_items": pack_list,
                                     "sum": pack_sum,
                                     "id": pack.id}
    
    res_context["last_articles"] = get_last_articles(3)
    res_context["brands"] = Brand.objects.all()


    return res_context

