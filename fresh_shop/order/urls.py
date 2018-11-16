"""__author__=wuliang"""

from django.conf.urls import  url

from order import views

urlpatterns = [
	url(r'^place_order/', views.place_order, name='place_order'),
	url(r'^add_order/', views.add_order, name='add_order'),
]