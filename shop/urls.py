from django.urls import path

from . import views

app_name = 'shop'
urlpatterns = [
	path('', views.shop_all, name='shop_all'),
	path('new', views.shop_new, name='shop_new'),
	path('<slug:category>', views.by_category, name='by_category'),
	path('<str:category>/<slug:slug>', views.detail, name='detail'),
]