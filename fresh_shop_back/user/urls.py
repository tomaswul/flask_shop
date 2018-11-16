"""__author__=wuliang"""

from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from user import views

urlpatterns = [
	#登录
	url(r'^login/', views.login, name='login'),
	# 后台主页,直接把装饰器写在这儿
	url(r'^index/', login_required(views.index), name='index'),
	#创建用户
	url(r'^create_user/', views.create_user, name='create_user'),
	url(r'^logout/', views.logout, name='logout'),
]