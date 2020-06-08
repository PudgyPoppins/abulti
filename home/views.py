from django.shortcuts import render
from django.http import HttpResponse
from shop.models import Item

def index(request):
	context = {
		"popular_list": Item.objects.order_by('purchased_count')[:3], #get the top 3 most purchased items
		"recent_list": Item.objects.order_by('-pub_date')[:3], #get the 3 most recent arrivals
	}

	return render(request, 'home/index.html', context)


