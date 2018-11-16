"""__author__=wuliang"""
from django.conf.urls import url

from cart import views

urlpatterns = [
	url(r'^addcart/', views.addcart, name='addcart'),
	url(r'^show_cart/', views.show_cart, name='show_cart'),

	url(r'^delcart/', views.delcart, name='delcart'),
]