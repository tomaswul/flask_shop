import django
from django.core.paginator import Paginator
from django.shortcuts import render

# Create your views here.
from cart.models import ShoppingCart
from goods.models import GoodsCategory, Goods
from order.models import OrderInfo
from utils.functions import login_required


def index(request):
	if request.method == 'GET':
		# 也可以把取出的数据分类封装成对象，之后再分类取出每个种类的对象
		'''
		{
			category1: [Goods object, Goods object],
			category2: [Goods object, Goods object],
			category3: [Goods object, Goods object],
			category4: [Goods object, Goods object],
			category5: [Goods object, Goods object],
			category6: [Goods object, Goods object],

		}
		'''
		'''
		# 分类封装对象
		categorys = GoodsCategory.CATEGORY_TYPE
		goods = Goods.objects.all()
		goods_dict = {}
		for category in categorys:
			goods_list = []
			count = 0
			for good in goods:
				# 统计没类商品的次数,小于4次才执行添加商品的操作
				if count < 4:
					# 判断商品分类和商品对象
					if good.category_id == category[0]:
						goods_list.append(good)
						count += 1
						
			goods_dict[category[1]] = goods_list
		
		'''


		types = GoodsCategory.CATEGORY_TYPE
		categorys = GoodsCategory.objects.all()
		goods_list = request.session.get ('goods_list')
		if goods_list:
			num = len(request.session.get ('goods_list'))
		else:
			cart = ShoppingCart.objects.filter(user_id=request.user.id)
			if cart:
				num = cart.count()
			else:
				num = 0
		return render(request, 'index.html', {'types': types,
											  'categorys': categorys,
											  'len': num})




def detail(request, id):
	if request.method == 'GET':
		goods = Goods.objects.get(pk=id)
		goods_list = request.session.get('goods_list')
		if goods_list:
			num = len(goods_list)
		else:
			cart = ShoppingCart.objects.filter(user_id=request.user.id)
			if cart:
				num = cart.count()
			else:
				num = 0
		return render(request, 'detail.html',{'goods': goods, 'len': num})

# 查看更多
def show_list(request):
	if request.method == 'GET':
		type = request.GET.get('type')
		category = GoodsCategory.objects.filter(id=type).first()


		price = request.GET.get('price')
		hot = request.GET.get('hot')
		if price:
			# 按价格排行
			goods = Goods.objects.filter(category=category).order_by('shop_price')
		elif hot:
			# 按热度排行，实际是按销量从高到低排行
			sql = 'select * from f_goods,' \
				  '(select sum(goods_nums) as nums,goods_id from f_order_goods GROUP BY goods_id order by nums desc) tb_g' \
				  ' where tb_g.goods_id=f_goods.id';
			goods = Goods.objects.raw (sql)
			temp = []
			for good in goods:
				if good.category.id == int(type):
					temp.append(good)
			goods = temp
		else:
			# 正常排行
			goods = Goods.objects.filter(category=category)
		page = int (request.GET.get ('page', 1))
		paginator = Paginator (goods, 4)
		goodses = paginator.page (page)
		if request.user.id:
			num = ShoppingCart.objects.count()
		else:
			s = request.session.get ('goods_list')
			if s:
				num = len(s)
			else:
				num = 0
		typename = GoodsCategory.CATEGORY_TYPE
		for tp in typename:
			if type:
				if tp[0] == int(type):
					typename = tp[1]
		return render(request, 'list.html', {'paginator': paginator,
											 'goodses': goodses,
											 'type':type,
											 'price':price,
											 'hot':hot,
											 'len':num,
											 'typename':typename})