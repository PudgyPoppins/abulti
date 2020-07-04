from django.contrib import admin
from django.utils.safestring import mark_safe

# Register your models here.
from .models import *

def make_out_of_stock(modeladmin, request, queryset):
	queryset.update(in_stock = False)
make_out_of_stock.short_description = "Make out of stock"

class ItemAdmin(admin.ModelAdmin):
	date_hierarchy = 'pub_date'
	list_display = ('name', 'price', 'in_stock', 'category', 'purchased_count')
	list_filter = ['category', 'in_stock']
	search_fields = ['name', 'category']
	actions = [make_out_of_stock]

	readonly_fields = ["image_display"]

	def image_display(self, obj):
		x = "<div>"
		for i in obj.image.all():
			x += "<img src='/media/%s' height='500px'/>" %(i.img)
		x += "</div>"
		return mark_safe(x)

def make_refund_accepted(modeladmin, request, queryset):
	queryset.update(refund_requested=False, refund_granted=True)
make_refund_accepted.short_description = 'Update orders to refund granted'

def make_processed(modeladmin, request, queryset):
	queryset.update(received = True)
make_processed.short_description = 'These orders are being processed'

def make_being_delivered(modeladmin, request, queryset):
	queryset.update(being_delivered = True)
make_being_delivered.short_description = 'These orders are being delivered currently'

def make_received(modeladmin, request, queryset):
	queryset.update(received = True)
make_received.short_description = 'These orders have been received'


class OrderAdmin(admin.ModelAdmin):
	readonly_fields=['token', 'name', 'email', 'order_date', 'shipping_address', 'billing_address', 'notes', 'order' ]
	list_display = [
		'name',
		'email',
		'paid',
		'being_processed',
		'being_delivered',
		'received',
		'refund_requested',
		'refund_granted',
		'shipping_address',
		'billing_address',
	]
	list_filter = [
		'paid',
		'being_processed',
		'being_delivered',
		'received',
		'refund_requested',
		'refund_granted',
	]
	search_fields = [
		'shipping_address',
		'billing_address',
	]
	actions = [make_refund_accepted, make_processed, make_being_delivered, make_received]

	def order(self, obj):
		x = "<p>"
		for i in obj.item.all():
			x += "%s," %(i)
		x += "</p>"
		return mark_safe(x)

admin.site.register(Item, ItemAdmin)
admin.site.register(Tag)
admin.site.register(Size)
admin.site.register(Image)

admin.site.register(Order, OrderAdmin)