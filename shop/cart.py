from decimal import Decimal
from django.conf import settings
from .models import Item


class Cart(object):
	def __init__(self, request):
		self.session = request.session
		cart = self.session.get(settings.CART_SESSION_ID)
		if not cart:
			cart = self.session[settings.CART_SESSION_ID] = {}
		self.cart = cart

	def add(self, item, quantity=1, update_quantity=False, size=""):
		item_id = str(item.id)

		if str(item_id + ":" + size) not in self.cart:
			self.cart[item_id + ":" + size] = {'quantity': 0, 'price': str(item.price), 'size': size}
		
		if update_quantity:
			self.cart[item_id + ":" + size]['quantity'] = quantity
		else:
			self.cart[item_id + ":" + size]['quantity'] += quantity
		self.save()

	def save(self):
		self.session[settings.CART_SESSION_ID] = self.cart
		self.session.modified = True

	def remove(self, item, size=""):
		item_id = str(item.id)
		if str(item_id + ":" + size) in self.cart:
			del self.cart[item_id + ":" + size]
			self.save()

	def __iter__(self):
		item_ids = [i.split(":")[0] for i in self.cart.keys()] #get just the ids of all of the items in the cart
		item_ids = list( dict.fromkeys(item_ids) ) #remove repeat values
		items = Item.objects.filter(id__in=item_ids) #get a list of all of the items in the cart (the actual objects of them)
		id_item_dict = dict(zip(item_ids, items)) #get a dictionary where the keys are the items and the values are the item ids

		for i in self.cart:
			self.cart[i]['item'] = id_item_dict[i.split(":")[0]]

		for item in self.cart.values():
			item['price'] = Decimal(item['price'])
			item['total_price'] = item['price'] * item['quantity']
			yield item

	def __len__(self):
		return sum(item['quantity'] for item in self.cart.values())

	def get_total_price(self):
		return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

	def clear(self):
		del self.session[settings.CART_SESSION_ID]
		self.session.modified = True
