from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from fresh_shop_back.settings import PAGE_NUMBER
from goods.froms import GoodsForm
from goods.models import GoodsCategory, Goods

@login_required
def goods_category_list(request):
	if request.method == 'GET':
		# 返回商品分类对象
		categorys = GoodsCategory.objects.all()
		return render(request, 'goods_category_list.html', {'categorys': categorys,
															'types': GoodsCategory.CATEGORY_TYPE})

@login_required
def goods_category_detail(request, id):
	if request.method == 'GET':
		# 返回商品分类对象和分类枚举信息
		category = GoodsCategory.objects.get(pk=id)
		return render (request, 'goods_category_detail.html', {'category': category,
															 'types': GoodsCategory.CATEGORY_TYPE})
	if request.method == 'POST':
		id = request.POST.get('category_id')
		category_front_image = request.FILES.get('category_front_image')
		if not category_front_image:
			return render(request, 'goods_category_detail.html', {'error': '图片必填'})

		# GoodsCategory.objects.filter().update()
		category = GoodsCategory.objects.get(pk=id)
		category.category_front_image = category_front_image
		category.save()

		return HttpResponseRedirect(reverse('goods:goods_category_list'))

@login_required
def goods_list(request):
	if request.method == 'GET':
		# TODO:查询所有的商品信息，并在goods_list.html页面中解析
		goods = Goods.objects.all()
		paginator = Paginator(goods, PAGE_NUMBER)

		# 算最后一页
		# 也可以是xxx.num_pages
		last_page = int(Goods.objects.count()/PAGE_NUMBER)+1
		types = GoodsCategory.CATEGORY_TYPE
		page = request.GET.get('page')
		try:
			page = int(page)
		except Exception as e:
			page = 1
		one_page_goods = paginator.page(page)
		return render(request, 'goods_list.html',{'one_page_goods': one_page_goods,
												  'page': page,
												'types': types,
												  'last_page': last_page})
@login_required
def goods_detail(request):
	if request.method == 'GET':
		types = GoodsCategory.CATEGORY_TYPE
		id = request.GET.get('id')

		if not id:
			return render(request,'goods_detail.html', {'types': types})
		good = Goods.objects.get(pk=id)
		return render(request, 'goods_detail.html', {'good': good, 'types': types})
	if request.method == 'POST':
		types = GoodsCategory.CATEGORY_TYPE
		form = GoodsForm(request.POST, request.FILES)
		id = request.GET.get('id')

		if form.is_valid():
			# 验证通过
			# 两种情况，一种是修改，一种是创建
			good = Goods.objects.filter(pk=request.GET.get('id')).first()
			if not id:
				if form.cleaned_data.get(id) != id:
					return render(request, 'goods_detail.html', {'good':good,
															 'goods_sn':'商品号已存在',
															 'types': types,
														 })
			if not good:
				good = Goods(**form.cleaned_data)
			img = form.cleaned_data.pop('goods_front_image')
			Goods.objects.filter (pk=request.GET.get ('id')).update(**form.cleaned_data)
			if img:
				# 有图片单独更新图片
				good.goods_front_image = img
				good.save()

			return HttpResponseRedirect(reverse('goods:goods_list'))
		else:
			# 修改验证失败
			good = Goods.objects.filter(pk=request.GET.get ('id')).first()
			return render(request, 'goods_detail.html', {'good':good,
														'errors':form.errors,
														'types': types})
@login_required
def goods_delete(request, id):
	if request.method == 'POST':
		Goods.objects.filter(pk=id).delete()

		return JsonResponse({'code': 200, 'msg': '请求成功'})


@login_required
def goods_desc(request, id):
	if request.method == 'GET':
		goods = Goods.objects.filter(pk=id).first()
		return render(request, 'goods_desc.html', {'goods': goods})
	if request.method == 'POST':
		goods_desc = request.POST.get('goods_desc')
		Goods.objects.filter(pk=id).update(goods_desc=goods_desc)
		return HttpResponseRedirect(reverse('goods:goods_list'))
