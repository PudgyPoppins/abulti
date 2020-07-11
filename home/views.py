from django.shortcuts import render
from django.http import HttpResponse
from shop.models import Item
from django.urls import reverse

from django.utils.safestring import mark_safe
from django.contrib import messages

def index(request):
	context = {
		"popular_list": Item.objects.order_by('purchased_count')[:3], #get the top 3 most purchased items
		"recent_list": Item.objects.order_by('-pub_date')[:3], #get the 3 most recent arrivals
	}
	if not request.session.get('has_seen_cookie_warning', False):
		privacy_link = reverse('home:privacy')
		messages.info(request, mark_safe("This site uses cookies! You should read our human-readable <a href='%s'>privacy policy</a> to see how we use your data." %(privacy_link)))
	request.session['has_seen_cookie_warning'] = True

	return render(request, 'home/index.html', context)


def handler403(request, *args, **argv):
	response = render(request, '403.html')
	response.status_code = 403
	return response

def handler404(request, *args, **argv):
	response = render(request, '404.html')
	response.status_code = 404
	return response