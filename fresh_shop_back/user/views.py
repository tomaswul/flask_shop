from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from user.forms import LoginForm


def login(request):
	if request.method == 'GET':
		# get请求返回登录页面
		return render(request, 'login.html')
	if request.method == 'POST':
		form = LoginForm(request.POST)
		# 验证登录表单是否满足规则
		if form.is_valid():
			# 验证指定用户名和密码的用户是否存在
			user = auth.authenticate(
				username=form.cleaned_data.get('username'),
				password=form.cleaned_data.get('password'))
			if not user:
				# 该用户不存在，返回登录页面
				return render(request, 'login.html',{'msg': '密码错误'})
			# 该用户存在，执行登录操作，并生成相应的cookie和session
			auth.login(request, user)
			# 返回后台主页
			return HttpResponseRedirect(reverse('user:index'))

		else:
			return render(request, 'login.html', {'error': form.errors})


@login_required
def logout(request):
	if request.method == 'GET':
		auth.logout(request)
		return HttpResponseRedirect(reverse('user:login'))



def index(request):
	if request.method == 'GET':
		return render(request, 'index.html')


def create_user(request):
	if request.method == 'GET':
		username = 'tom'
		password = '123123'
		password = make_password(password)

		User.objects.create(username=username, password=password)

		return HttpResponse('创建用户成功')