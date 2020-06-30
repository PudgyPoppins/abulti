from django.utils import timezone
from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.http import HttpResponse, Http404

from .models import Item
from .forms import *
from .cart import Cart

category_reverse = dict((v, k) for k, v in Item.TYPES) #This is used for multiple things, so I write it here
category_names = list(category_reverse.keys())


def shop_all(request):
	shop_list = get_list_or_404(Item)

	context = {
		"list": shop_list,
		'category_names': category_names,
	}
	return render(request, 'shop/list.html', context)

def shop_new(request):
	shop_list = Item.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')
	context = {
		"list": shop_list,
		'category_names': category_names,
	}
	return render(request, 'shop/list.html', context)

def by_category(request, category):
	try:
		category_list = Item.objects.filter(category=category_reverse[category])
		context = {
			#"list": category_list,
			'list': get_list_or_404(Item),
			"category": category,
			'category_names': category_names,
		}
		return render(request, 'shop/list.html', context)
	except KeyError:
		raise Http404

def detail(request, category, slug):
	try:
		item = get_object_or_404(Item, category=category_reverse[category], slug=slug)
		shop_other_list = Item.objects.order_by('purchased_count').exclude(id=item.id)[:3]
		context = {
			"item": item,
			'shop_other_list': shop_other_list,
		}

		return render(request, 'shop/detail.html', context)
	except KeyError:
		raise Http404

def cart_add(request, item_id):
	cart = Cart(request)
	item = get_object_or_404(Item, id=item_id)
	form = AddItemForm()
	if request.method == "POST":
		form = AddItemForm(request.POST)
		if form.is_valid():
			data = form.cleaned_data
			cart.add(item=item, quantity=data['quantity'], update_quantity=data['update'], size=data['size'])
	return redirect('shop:cart')


def cart_remove(request, item_id):
	cart = Cart(request)
	item = get_object_or_404(Item, id=item_id)
	form = RemoveItemForm()
	if request.method == "POST":
		form = RemoveItemForm(request.POST)
		if form.is_valid():
			data = form.cleaned_data
			cart.remove(item = item, size = data['size'])
	return redirect('shop:cart')


def cart_detail(request):
	cart = Cart(request)
	for item in cart:
		item['update_quantity_form'] = AddItemForm(initial={'quantity': item['quantity'], 'update': True, 'size': item['size'],})
	return render(request, 'shop/cart_detail.html', {'cart': cart})