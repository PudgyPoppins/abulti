from django.urls import path

from . import views

app_name = 'shop'
urlpatterns = [
	path('resources/checkout.js', views.checkout_js, name='checkout_js'),

	path('shop/', views.shop_all, name='shop_all'),
	path('shop/new', views.shop_new, name='shop_new'),
	path('shop/<slug:category>', views.by_category, name='by_category'),
	path('shop/<str:category>/<slug:slug>', views.detail, name='detail'),

	path('cart/add/<item_id>', views.cart_add, name='cart_add'),
	path('cart/remove/<item_id>', views.cart_remove, name='cart_remove'),
	path('cart/', views.cart_detail, name='cart'),
	path('cart/checkout', views.order_create, name='order_create'),

	path('order/<order_token>', views.order_created, name='order_created')
]