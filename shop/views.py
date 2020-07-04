from django.utils import timezone
from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.urls import reverse
from django.http import HttpResponse, Http404
from django.core.exceptions import PermissionDenied
from django.contrib import messages

from .models import Item, Address, Size, OrderItem, Order
from .forms import *
from .cart import Cart

from django.core.mail import mail_admins, send_mail
from django.template.loader import render_to_string

import stripe
from django.conf import settings
stripe.api_key = settings.STRIPE_SECRET_KEY

category_reverse = dict((v, k) for k, v in Item.TYPES) #This is used for multiple things, so I write it here
category_names = list(category_reverse.keys())

def checkout_js(request):
	return render(request, 'shop/checkout.js', {'stripe_pub_key': settings.STRIPE_PUBLIC_KEY}, content_type="application/x-javascript")


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

def order_create(request):
	cart = Cart(request)
	if len(cart) == 0:
		messages.error(request, 'Add items to your cart before you check out')
		return redirect('shop:cart')
	form = CheckoutForm()

	context = {
		'form': form,
		'cart': cart, 
	}

	if request.method == "GET":
		try:
			intent = stripe.PaymentIntent.create(
				amount=int(cart.get_total_price() * 100),
				currency='usd',
				payment_method_types=['card']
			)
			context['client_secret'] = intent.client_secret
		except Exception as e:
			messages.error(request, "Whoops: %s" %(str(e)))
			raise PermissionDenied
	#^-----Get the client secret and create some basic context. Intent only created on 'gets', because otherwise it double creates them.

	if request.method == 'POST':
		form = CheckoutForm(request.POST)
		
		if form.is_valid():
			d = form.cleaned_data

			# Find or create a new address:
			shipping_address_search = Address.objects.filter(street_address = d['shipping_address'], apartment_address = d.get('shipping_address2'), city = d['shipping_city'], state=d['shipping_state'], zip_code = d['shipping_zip'], country = d['shipping_country'], address_type = 'S')
			if len(shipping_address_search) > 0:
				shipping_address = shipping_address_search[0]
			else:
				shipping_address = Address(street_address = d['shipping_address'], apartment_address = d.get('shipping_address2'), city = d['shipping_city'], state=d['shipping_state'], zip_code = d['shipping_zip'], country = d['shipping_country'], address_type = 'S')
			shipping_address.save()

			if d.get('same_billing_address'):
				billing_address_search = Address.objects.filter(street_address = d['shipping_address'], apartment_address = d.get('shipping_address2'), city = d['shipping_city'], state=d['shipping_state'], zip_code = d['shipping_zip'], country = d['shipping_country'], address_type = 'B')
				if len(billing_address_search) > 0:
					billing_address = billing_address_search[0]
				else:
					billing_address = Address(street_address = d['shipping_address'], apartment_address = d.get('shipping_address2'), city = d['shipping_city'], state=d['shipping_state'], zip_code = d['shipping_zip'], country = d['shipping_country'], address_type = 'B')
			else:
				billing_address_search = Address.objects.filter(street_address = d['billing_address'], apartment_address = d.get('billing_address2'), city = d['billing_city'], state=d['billing_state'], zip_code = d['billing_zip'], country = d['billing_country'], address_type = 'B')
				if len(billing_address_search) > 0:
					billing_address = billing_address_search[0]
				else:
					billing_address = Address(street_address = d['billing_address'], apartment_address = d.get('billing_address2'), city = d['billing_city'], state=d['billing_state'], zip_code = d['billing_zip'], country = d['billing_country'], address_type = 'B')
			billing_address.save()
			# End address creation/search

			order = Order(name = d['name'], email = d['email'], shipping_address=shipping_address, billing_address=billing_address, notes=d.get('notes'))
			order.paid = True if d.get('paid') == True else False
			order.save()

			for i in cart:
				try:
					size = Size.objects.filter(name = i['size'])[0]
				except:
					size = None
				orderitem = OrderItem(order=order, item=i['item'], quantity=i['quantity'], size=size)
				orderitem.save()
			cart.clear()

			if order.paid:
				for orderitem in order.item.all():
					orderitem.item.purchased_count += 1;
					orderitem.item.save();
				html = render_to_string('shop/order_email_admin.html', {'order': order})
				mail_admins(subject = 'New order created',  message = 'A new order is created', fail_silently=True, html_message = html)

				html = render_to_string('shop/order_email.html', {'order': order})
				send_mail(subject = 'New order created',  message = 'Your new order at Abulti Apparel', fail_silently=True, html_message = html, from_email = 'abultiapparel@gmail.com', recipient_list = [order.email])
				#^ If the order is paid (it really should be at this point, this is just a dummy check kind of),
				# Then increase the purchased_counts of our stock and send an email to the admin and user
		else:
			messages.error(request, "Please correct your form below")
			return render(request, 'shop/order_create.html', context)

		#return render(request, 'shop/order_created.html', {'order': order})
		return redirect(reverse('shop:order_created', kwargs={'order_token':order.token}))
	return render(request, 'shop/order_create.html', context)

def order_created(request, order_token):
	search = Order.objects.filter(token=order_token)
	if len(search) > 0:
		order = search[0]
	else:
		raise Http404 
	return render(request, 'shop/order_created.html', {'order': order})