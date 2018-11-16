"""__author__=wuliang"""
from django.conf.urls import url

from goods import views

urlpatterns = [
	# 商品分类
	url(r'goods_category_list/', views.goods_category_list, name='goods_category_list'),
	# 编辑商品种类
	url(r'goods_category_detail/(\d+)', views.goods_category_detail, name='goods_category_detail'),

	# 商品列表
	url(r'goods_list/', views.goods_list, name='goods_list'),
	# 商品添加
	url(r'goods_detail/', views.goods_detail, name= 'goods_detail'),
	# 商品删除
	url(r'goods_delete/(\d+)', views.goods_delete, name= 'goods_delete'),
	# 商品详情
	url(r'goods_desc/(\d+)', views.goods_desc, name='goods_desc'),



]