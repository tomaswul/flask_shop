"""__author__=wuliang"""
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

from cart.models import ShoppingCart
from goods.models import Goods
from user.models import User


class UserAuthMiddleware(MiddlewareMixin):
	def process_request(self,request):
		#
		# TODO:某些页面需要才能访问，某些页面不需要登录就可以访问
		# TODO:需要登录的页面，当用户没有登录时，该如何处理
		not_need_path = ['/user/login/', '/user/register/',
						 '/goods/index/', '/goods/detail/(.*)/',
						 '/media/(.*)', '/static/(.*)']

		# 没有登录不能访问的页面
		disable_page =[r'/user/user_center_info/',
					   r'/user/user_center_site/',
					   r'/user/user_center_order/',
					   r'/order/place_order/'

		]
		id = request.session.get('user_id')

		if not id:
			if request.path in disable_page:
				return HttpResponseRedirect(reverse('user:login'))
			else:
				return None
		request.user = User.objects.filter(pk=id).first()
		# 登录之后，将session中的购物车数据，迁移到数据库表中，看是否有相同数据
		# 如果有相同的数据，就不迁移
		goods_list = request.session.get('goods_list')
		if goods_list:
			for goods_dict in goods_list:
				for id, num in goods_dict.items():

					# 如果session中商品已经存在于数据库表中，则更新
					# 如果session中商品不存在于数据库中，则添加
					# 如果session中的商品少于数据库表中的商品，则更新session(老师的想法)
					goods = Goods.objects.filter(pk=id).first()
					cart = ShoppingCart.objects.filter(goods=goods,user=request.user).first()
					if not cart:
						ShoppingCart.objects.create(goods=goods,nums=int(num),user=request.user)
						# 删掉当前会话里的购物车记录，当前记录迁移到数据库中
					else:
						if cart.nums < int(num):
							cart.nums = int(num)
							cart.save()

			request.session.pop('goods_list')



		return None