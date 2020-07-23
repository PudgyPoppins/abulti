from django.urls import path

from . import views

app_name = 'shop'
urlpatterns = [
	path('resources/checkout.js', views.checkout_js, name='checkout_js'),

	path('shop/', views.shop_all, name='shop_all'),
	path('shop/new', views.shop_new, name='shop_new'),
	path('shop/<slug:category>', views.by_category, name='by_category'),
	path('shop/<str:category>/<slug:slug>', views.detail, name='detail'),

	path('shop/<str:category>/<slug:slug>/review', views.review, name='review'),
	path('review/<int:review_id>/delete', views.delete_review, name='delete_review'),
	path('review/<int:review_id>/verify', views.verify_review, name='verify_review'),
	path('review/<int:review_id>/unverify', views.unverify_review, name='unverify_review'),

	path('cart/add/<item_id>', views.cart_add, name='cart_add'),
	path('cart/remove/<item_id>', views.cart_remove, name='cart_remove'),
	path('cart/', views.cart_detail, name='cart'),
	path('cart/checkout', views.order_create, name='order_create'),

	path('order/<order_token>', views.order_created, name='order_created')
]