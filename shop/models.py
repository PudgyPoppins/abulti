from django.db import models
from django.utils import timezone
from django.utils.text import slugify

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