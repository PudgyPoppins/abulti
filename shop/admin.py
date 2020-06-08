from django.contrib import admin

# Register your models here.
from .models import *

class TagInline(admin.TabularInline):
	model = Tag
	#extra = 1 #1 extra

class SizeInline(admin.TabularInline):
	model = Size

class ImageInline(admin.TabularInline):
	model = Image
	readonly_fields = ["image_display"]

	def image_display(self, obj):
		return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
			url = obj.img.url,
			width=obj.img.width,
			height=obj.img.height,
			)
	)

def make_out_of_stock(modeladmin, request, queryset):
	queryset.update(in_stock = False)
make_out_of_stock.short_description = "Make out of stock"

class ItemAdmin(admin.ModelAdmin):
	date_hierarchy = 'pub_date'
	list_display = ('name', 'price', 'in_stock', 'clothing_type')
	list_filter = ['clothing_type', 'purchased_count']
	search_fields = ['name', 'clothing_type']
	actions = [make_out_of_stock]
	inlines = [
		TagInline,
		SizeInline,
		ImageInline,
	]

	'''readonly_fields = ["image_display"]

	def image_display(self, obj):
		return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
			url = obj.image.url,
			width=obj.image.width,
			height=obj.image.height,
			)
	)'''


admin.site.register(Item)
admin.site.register(Tag)
admin.site.register(Size)
admin.site.register(Image)