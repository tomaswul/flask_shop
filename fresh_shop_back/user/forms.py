"""__author__=wuliang"""
from django import forms
from django.contrib.auth.models import User


class LoginForm(forms.Form):
	username = forms.CharField(
		max_length=16,min_length=2,required=True,
			error_messages={
				'max_length': '账号不能超过16位',
				'min_length': '账号不能小于2位',
				'required': '账号不能为空'
 							   }
							   )
	password = forms.CharField(
		max_length=16, min_length=6, required=True,
		error_messages={
			'max_length': '密码不能超过16位',
			'min_length': '密码不能小于6位',
			'required': '密码不能为空'
		}
	)

	def clean(self):
		# 使用django自带的User模块进行验证
		user = User.objects.filter(username=self.cleaned_data.get('username')).first()
		if not user:
			raise forms.ValidationError({'username': '该账号未注册，无法登录'})

		return self.cleaned_data