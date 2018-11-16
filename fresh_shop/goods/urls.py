"""__author__=wuliang"""

from django.conf.urls import url

from goods import views

urlpatterns = [
	url(r'^index/', views.index, name='index'),
	url(r'^detail/(\d+)', views.detail, name='detail'),
	url(r'^show_list/', views.show_list, name='show_list'),
]