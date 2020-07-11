from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = 'home'
urlpatterns = [
    path('', views.index, name='index'),

    path('privacy', TemplateView.as_view(template_name='home/privacy.html'), name='privacy'),
    path('tos', TemplateView.as_view(template_name='home/tos.html'), name='tos'),
    path('about', TemplateView.as_view(template_name='home/about.html'), name='about'),
    path('help', TemplateView.as_view(template_name='home/help.html'), name='help'),
    path('shipping', TemplateView.as_view(template_name='home/shipping.html'), name='shipping'),
    path('return-policy', TemplateView.as_view(template_name='home/returns.html'), name='returns'),
]

