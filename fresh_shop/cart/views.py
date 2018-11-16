import random
import time

from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from cart.models import ShoppingCart
from goods.models import Goods
from utils.functions import add_cart_no_login


@add_cart_no_login
def addcart(request):
	if request.method == 'GET':
		# 加入到购物车，需判断用户是否登录
		# 如果登录，加入到购物车中的数据，其实是加入到数据库中购物车表里
		# 如果没有登录，则加入到购物车中的数据，是加入到session中


		# 如果登录，则加入到购物车中的数据，是加入到session中
		# session中存储数据：商品id,商品数量，商品选择状态
		# 如果登录，则把session中的数据同步到数据库中(中间件同步数据)
		goods_list = request.session.get('goods_list')
		cart_list = []
		s = '1234abcd'
		if goods_list:
			for goods_dict in goods_list:
				cart_dict = {}

				for key, value in goods_dict.items():
					id = ''
					# 获取session所有商品信息
					goods = Goods.objects.filter(pk=key).first()
					cart_dict['goods'] = goods
					cart_dict['nums'] = value
					for _ in range(4):
						id = random.choice(s)
					cart_dict['id'] = id

				cart_list.append(cart_dict)
			num = len(cart_list)

			return render(request,'cart.html',{'cart_list':cart_list,'len':num})

		else:
			user_id = request.session.get ('user_id')
			if user_id:
				return HttpResponseRedirect(reverse('cart:show_cart'))
			else:
				return render(request,'cart.html')

	if request.method == 'POST':
		goods_list = request.session.get ('goods_list')
		if goods_list:
			num = len(goods_list)
		else:
			user = request.user
			if user:
				num = ShoppingCart.objects.filter(user=user).count()
		return JsonResponse({'code':200,'msg':'添加成功','len':num})


def show_cart(request):
	if request.method == 'GET':
		user_id = request.session.get('user_id')
		if not user_id:
			return HttpResponseRedirect(reverse('cart:addcart'))
		else:
			cart = ShoppingCart.objects.filter(user=request.user)
			len = cart.all().count()

			return render(request, 'cart.html',{'cart_list': cart,'len': len})

def delcart(request):
	if request.method == 'POST':
		id = request.POST.get('goods_id')
		user_id = request.session.get('user_id')
		if not user_id:
			# 没登录
			goods_list = request.session.get('goods_list')
			for goods_dict in goods_list:
				for key in goods_dict:
					if key == id:
						goods_list.remove(goods_dict)
			request.session['goods_list'] = goods_list

		else:
			goods = Goods.objects.filter(pk=id).first()
			ShoppingCart.objects.filter(user=request.user, goods=goods).delete()

		return JsonResponse({'code':200, 'msg':'删除成功'})




