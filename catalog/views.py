from django.shortcuts import render

from django.db.models import Q

# Create your views here.
from rest_framework import generics

from .models import Product, Brand, Image,  Category, CatItem
from .serializers import ProductSerializer, BrandSerializer, ImageSerializer
from .serializers import CategorySerializer, CatItemSerializer

from django.contrib.auth.models import User
from .models import Content, Chanel

from django.conf import settings
from django.shortcuts import render_to_response, get_object_or_404, redirect, render
from helpers import http403json, http200json
from django.forms import ModelForm



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
            context["current_brand"] = brand


        context["current"] = catalog_id
        context["cat_title"] = cats_title[context["current"]]
        context["current_chanel"] = CatItem.objects.get(id=context["current"])
        context["current_list"] = Product.objects.filter(q_list)
        
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
            context["current_brand"] = brand

        context["current_list"] = Product.objects.filter(q_list).order_by("-pub_date")
        
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
        context["current_brand"] = brand
    context["current_list"] = Product.objects.filter(q_list)

    
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
  return []

def get_last_products(num):
  return []
    
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
    resp = requests.post(API_MAIL_URL, auth=HTTPBasicAuth('api', API_MAIL_GUN),
                        data= {"from": "site@bazis.com",
                               "to":"savemymind@gmail.com",
                               "subject": u"mail from site %s %s" % (request.POST.get("name",""),
                               request.POST.get("email","")),
                               "html": request.POST.get("text","")})
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


class ContentForm(ModelForm):
    class Meta:
        model = Content
        fields = [ 'title', 'content', 'image','ordering']


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
    COMPANY_ID = 1
    context["catalog_current_discont"] = context["current_discont"][0]
    context["about_company"] = [Content.objects.get(id=COMPANY_ID)]
    if request.user.is_authenticated() and request.user.is_staff:
        return {"cats":cats,
                'chanels': context,
                "discont_count": discont_count,
                'is_admin': True,
                "cart_count":0
                }
    else:
        return {"cats":cats,
                'chanels': context,
                "discont_count": discont_count,
                "cart_count":0
                 }
