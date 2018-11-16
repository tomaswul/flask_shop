"""__author__=wuliang"""
from django.contrib.auth.hashers import check_password
from django.http import HttpResponseRedirect
from django.urls import reverse

from cart.models import ShoppingCart
from goods.models import Goods
from user.models import User


def login_required(func):

	def check_logined(request):
		try:
			id = request.session['user_id']
			request.user = User.objects.filter(pk=id).first()
		except Exception as e:
			return HttpResponseRedirect(reverse('user:login'))
		return func(request)

	return check_logined


def add_cart_no_login(func):
	def add_cart(request):
		user_id = request.session.get('user_id')
		goods_list = request.session.get ('goods_list')
		if not user_id:
			# 用户未登录
			if not goods_list:
				# session里面没有数据
				goods_list = []
			# 获取ajax提交的数据
			id = request.POST.get('goods_id')
			num = request.POST.get('goods_nums')
			add = request.POST.get('add')

			if id != None and num != None:
				# 判断提交的数据是否为空
				num = int(num)
				for goods_dicts in goods_list:
					for gid,gnum in goods_dicts.items():
						# 判断购物车中的数据是否有一样的
						if gid == id:
							if add:
								t = num
								num = t
							else:
								num += int(gnum)
							goods_list.remove(goods_dicts)
				goods_dict = {id:str(num)}
				goods_list.insert(0,goods_dict)
			request.session['goods_list'] = goods_list
		else:
			# 用户已经登录，则保存到数据库中
			id = request.POST.get ('goods_id')
			num = request.POST.get ('goods_nums')
			if id != None and num != None:
				goods = Goods.objects.filter(pk=id).first()
				cart = ShoppingCart.objects.filter(goods=goods, user=request.user).first()
				if not cart:
					ShoppingCart.objects.create (goods=goods, nums=int (num), user=request.user)

				else:
					if cart.nums != num:
						cart.nums = num
						cart.save ()
		return func(request)
	return add_cart