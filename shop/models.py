from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django_countries.fields import CountryField

import random, string
def create_token():
	chars = string.ascii_lowercase+string.ascii_uppercase+string.digits
	token = ''.join(random.choice(chars) for _ in range(5))
	token_list = Order.objects.filter(token=token)
	while token_list:
		token = ''.join(random.choice(chars) for _ in range(5))
		token_list = Order.objects.filter(token=token)
	return token

# Create your models here.

class Tag(models.Model): #tags are created here so that we can expand them really easily
	name = models.CharField(max_length=50)
	def __str__(self): 
		return self.name

class Size(models.Model): #sizes are created here so that items can come in multiple sizes
	name = models.CharField(max_length=50)
	def __str__(self): 
		return self.name

class Image(models.Model): #images are created here to that items can have multiple images attatched
	img = models.ImageField(upload_to='item_images/', height_field=None, width_field=None, max_length=100)
	alt_text = models.CharField(max_length=50)
	def __str__(self): 
		return self.alt_text

class Item(models.Model):
	name = models.CharField(max_length=50)
	description = models.CharField(max_length=500)
	price = models.DecimalField(max_digits=5, decimal_places=2)
	in_stock = models.BooleanField(default=True) #items default to be in stock
	number_in_stock = models.PositiveSmallIntegerField(null=True, blank=True) #optional field that we may not use, but here it is just in case
	purchased_count = models.PositiveSmallIntegerField(default=0) #can be used for determining popularity
	pub_date = models.DateTimeField('date published', default=timezone.now) #can be used for determining new releases

	tag = models.ManyToManyField(Tag, related_name="tag", blank=True) #tags are added in a separate area, are optional
	size = models.ManyToManyField(Size, related_name="size", blank=True) #optional
	image = models.ManyToManyField(Image, related_name="image", blank=True) #optional

	TYPES = (
		('TS', 'T-Shirt'),
		('LS', 'Long-Sleeve'),
		('ST', 'Sticker'),
	)
	category = models.CharField(max_length=2, choices=TYPES)

	FITS = (
		('F', "Women's"),
		('M', "Men's"),
		('U', 'Unisex'),
	)
	fit = models.CharField(max_length=1, choices=FITS, null=True, blank=True) #optional

	slug = models.SlugField(max_length=65, blank=True, null=True, unique=True)

	def __str__(self): 
		return self.name
	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.name)
		super(Item, self).save(*args, **kwargs)

class Order(models.Model):
	token = models.CharField(max_length=5, null=True, blank=True)

	name = models.CharField(max_length=100, blank=True, null=True)
	email = models.EmailField(null=True)

	order_date = models.DateTimeField('date ordered', default=timezone.now)

	shipping_address = models.ForeignKey('Address', related_name='shipping_address', on_delete=models.SET_NULL, blank=True, null=True)
	billing_address = models.ForeignKey('Address', related_name='billing_address', on_delete=models.SET_NULL, blank=True, null=True)
	
	being_processed = models.BooleanField(default=False)
	being_delivered = models.BooleanField(default=False)
	received = models.BooleanField(default=False)
	refund_requested = models.BooleanField(default=False)
	refund_granted = models.BooleanField(default=False)

	paid = models.BooleanField(default=False)

	notes = models.CharField(max_length=1000, blank=True, null=True)

	class Meta:
		ordering = ('-order_date', )

	def __str__(self):
		return 'Order {}'.format(self.id)

	def get_total_price(self):
		total = 0
		for order_item in self.item.all():
			total += order_item.get_total_price()
		return total

	def save(self, *args, **kwargs):
		if not self.token:
			self.token = create_token() #set the token on save
		return super(Order, self).save(*args, **kwargs)

class OrderItem(models.Model):
	item = models.OneToOneField(Item, on_delete=models.CASCADE)
	quantity = models.IntegerField(default=1)
	size = models.ForeignKey(Size, on_delete=models.SET_NULL, null=True, blank=True)
	order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="item", null=True)
	
	def __str__(self):
		if self.size:
			return str(self.quantity) + " " + str(self.size) +  " " + self.item.name
		else:
			return str(self.quantity) +  " " + self.item.name

	def get_total_price(self):
		return self.quantity * self.item.price


ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)
class Address(models.Model):
	street_address = models.CharField(max_length=100)
	apartment_address = models.CharField(max_length=100)
	city = models.CharField(max_length=100, null=True)
	state = models.CharField('State / Province', max_length=100, null=True)
	zip_code = models.CharField('Zip / Postal Code', max_length=100)
	country = CountryField(multiple=False)
	address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)

	def __str__(self):
		return self.address_type + " " + self.street_address

	class Meta:
		verbose_name_plural = 'Addresses'