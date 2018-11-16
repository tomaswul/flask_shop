import random

from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from cart.models import ShoppingCart
from goods.models import Goods
from order.models import OrderInfo, OrderGoods


def place_order(request):
	if request.method == 'GET':
		user_id = request.session.get('user_id')
		carts = ShoppingCart.objects.filter(user_id=user_id,is_select=1).all()
		total_price = 0

		for cart in carts:
			cart.total_price = cart.nums * cart.goods.shop_price
		for c2 in carts:
			total_price += c2.total_price
		return render(request, 'place_order.html', {'carts':carts,'total_price':total_price,'user':request.user})




def add_order(request):
	if request.method == 'GET':
		user_id = request.session.get('user_id')
		carts = ShoppingCart.objects.filter(user_id=user_id,is_select=1)

		order_mount = 0
		s = '123456abcdef'
		order_sn = ''
		for _ in range(5):
			order_sn += random.choice(s)
		if carts:
			for cart in carts:
				order_mount += cart.nums * cart.goods.shop_price
			order = OrderInfo.objects.create(user_id=user_id,
										 order_sn=order_sn,
										 order_mount=order_mount)


			for cart in carts:
				OrderGoods.objects.create(goods=cart.goods,
										  order=order,
										  goods_nums=cart.nums
										  )
				goods_num = Goods.objects.filter(pk=cart.goods.id).first().goods_nums
				Goods.objects.filter(pk=cart.goods.id).update(goods_nums=goods_num-cart.nums)

			ShoppingCart.objects.filter(user_id=user_id).delete()

			return JsonResponse({'code': 200,'msg':'订单添加成功'})
		else:
			return JsonResponse({'code': 401, 'msg': '购物车中无数据'})
