"""doors URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.views import login
from django.contrib.auth.views import logout
from rest_framework.reverse import reverse
from catalog.views import *
from catalog  import views
from django.conf.urls.static import static
import os


@api_view(['GET'])
def api_root(request, format=None):
    """
    The entry endpoint of our API.
    """
    return Response({
        'brands': reverse('brands', request=request),
        'cats': reverse('cats', request=request),
        'cats_item': reverse('cats_item', request=request),
        'product': reverse('product', request=request),
        'packages': reverse('packages', request=request),
        'image': reverse('image', request=request),
        'package-item': reverse('package-item', request=request),
    })


urlpatterns = [
    url('^$', index, name="index"),
    url('^faq$', faq, name="faq"),
    url('^contacts$', contacts, name="contacts"),
    url('^product_([\d]+)$', product, name="product_profile"),
    
    url(r'^api/$', api_root),

    url(
        regex=r'^accounts/login/$',
        view=login,
        kwargs={'template_name': 'login.html'},
        name='login'
    ),
    url(
        regex=r'^accounts/logout/$',
        view=logout,
        kwargs={'next_page': '/'},
        name='logout'
    ),


     
    url(r'^api/brands/$', BrandDetail.as_view(), name='api_brands'),
    url(r'^api/cats/$', CategoryDetail.as_view(), name='cats'),
    url(r'^api/cats_item/$', CatItemDetail.as_view(), name='cats_item'),
    url(r'^api/product/$', ProductDetail.as_view(), name='product'),
    url(r'^api/image/$', ImageDetail.as_view(), name='image'),
    url(r'^api/package-item/$', BrandDetail.as_view(), name='packages'),
    url(r'^api/packages/$', BrandDetail.as_view(), name='package-item'),
    
    url('^catalog$', catalog, name="catalog"),
    url(r'^cat_type_([\d]+)$', catalog_sub_cat, name='cat-item'),   
    url(r'^cat_([\w]+)$', catalog, name='catalog'),



    url(r'^brands$', views.brands, name="brands"),
    url(r'^send_marina$', views.send_marina, name="send_marina"),
    url(r'^page_([\w]+)$', views.custom_page, name="custom_page"),

    url(r'^blog$', views.blog, name="blog"),
    url(r'^blog_item_([\d]+)$', views.blog_item, name="blog-item"),
    url(r'^blog_([\d]+)$', views.blog_cat, name="blog-cat"),
    url(r"^subscribe/add", views.subscribe_add, name="subscribe-add" ),
    url(r'^chanel/delete/([\.\d]+)', views.delete_chanel, name="chanel-delete"),
    url(r'^chanel/edit', views.edit_chanel, name="chanel-edit"),
    url(r'^chanel/add', views.add_chanel, name="chanel-add"), 
    url(r'^cart/add/([\d]+)/([\d]+)', views.cart_add_item, name="cart_add_item"),
    url(r'^cart/add_package/([\d]+)', views.cart_add_package, name="cart_add_package"),
    url(r'^cart/del/item/([\d]+)', views.cart_del_item, name="cart_del_item"), 
    url(r'^cart/change/item/([\d]+)/([\d]+)', views.cart_change_item, name="cart_change_item"), 
    url(r'^cart_confirm$', views.cart_confirm, name="cart_confirm"), 
    url(r'^cart_approve$', views.cart_approve, name="cart_approve"), 
    url(r'^cart$', views.cart, name="cart"),
    
    url(r'^search_product$', views.search_product, name="search"),
    url(r'^search$', views.search, name="search"),
    
    url(r'^admin/', admin.site.urls),

] 


if settings.DEBUG:    
   urlpatterns += static("js", document_root=os.path.join(settings.BASE_DIR,"js"))
   urlpatterns += static("img", document_root=os.path.join(settings.BASE_DIR,"img"))
   urlpatterns += static("media", document_root=os.path.join(settings.BASE_DIR,"media"))
   urlpatterns += static("css", document_root=os.path.join(settings.BASE_DIR, "css"))
   urlpatterns += static("fonts", document_root=os.path.join(settings.BASE_DIR,"fonts"))
   urlpatterns += static("icon", document_root=os.path.join(settings.BASE_DIR,"icon"))

   
    
