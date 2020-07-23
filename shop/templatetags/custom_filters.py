import datetime

from django import template
register = template.Library()

@register.filter
def is_new_arrival(value):
	return value >= datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=30)

@register.filter
def minus_stars(value):
	return 5 - int(value)
