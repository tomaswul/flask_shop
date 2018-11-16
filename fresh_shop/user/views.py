from django.contrib.auth.hashers import make_password, check_password
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from order.models import OrderInfo
from user.forms import RegisterForm, LoginForm, AddressForm
from user.models import User, UserAddress
from utils.functions import login_required


def login(request):
	if request.method == 'GET':
		return render(request, 'login.html')

	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			# 通过合理性校验
			user = User.objects.filter(username=form.cleaned_data.get('username')).first()
			if not user:
				# 用户不存在
				return render(request, 'login.html', {'msg1': '该账号不存在'})

			flag = check_password(form.cleaned_data.get('pwd'), user.password)
			if not flag:
				# 密码错误
				return render (request, 'login.html', {'msg2': '密码错误'})

			# 向cookie中设置sessionid值
			# 向django_session表中存sessionid值
			if request.user.id:
				return render(request, 'login.html', {'msg3': '一个浏览器只能等录一个账号'})
			request.session['user_id'] = user.id

			return HttpResponseRedirect(reverse('goods:index'))



		else:
			return render(request, 'login.html', {'errors': form.errors})


def register(request):
	if request.method == 'GET':
		return render(request, 'register.html')
	if request.method == 'POST':
		form = RegisterForm(request.POST)

		if form.is_valid():
			# 表单验证通过，允许注册
			password = make_password(form.cleaned_data.get('pwd'))
			User.objects.create(username=form.cleaned_data.get('user_name'),
								password=password,
								email=form.cleaned_data.get('email'))

			return HttpResponseRedirect(reverse('user:login'))
		else:
			return render(request, 'register.html', {'errors': form.errors})


def logout(request):
	if request.method == 'GET':
		del request.session['user_id']
		return render(request, 'login.html')


def user_center_info(request):
	if request.method == 'GET':

		return render(request, 'user_center_info.html')



def user_center_site(request):
	if request.method == 'GET':
		user_addr = UserAddress.objects.filter(user=request.user).first()
		return render(request, 'user_center_site.html',{'user_addr': user_addr})
	if request.method == 'POST':
		form = AddressForm(request.POST)
		if form.is_valid():
			user_addr = UserAddress.objects.create(user=request.user,
									   signer_mobile=form.cleaned_data.get('phone'),
									   signer_name=form.cleaned_data.get('addressee'),
									   signer_postcode=form.cleaned_data.get('zip_code'),
									   address=form.cleaned_data.get('detailed_address'))
			if user_addr:
				return render(request, 'user_center_site.html',{'user_addr': user_addr})
		else:
			return render(request, 'user_center_site.html', {'errors': form.errors})



def user_center_order(request):
	if request.method == 'GET':

		orders_all = OrderInfo.objects.filter(user=request.user)
		pg = Paginator(orders_all, 5)
		page = request.GET.get('page')
		if page:
			page = int(page)
		else:
			page = 1
		orders = pg.page(page)
		return render(request, 'user_center_order.html',{'orders': orders, 'page': page})
