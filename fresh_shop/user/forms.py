"""__author__=wuliang"""
from django import forms

from user.models import User


class RegisterForm(forms.Form):
	user_name = forms.CharField(max_length=20,min_length=5,required=True,
								error_messages={
									'max_length': '用户名不能超过20位',
									'min_length': '用户名不能少于5位',
									'required': '用户名不能为空'
								})

	pwd = forms.CharField(max_length=20,min_length=8,required=True,
						  error_messages={
							  'max_length': '密码不能超过20位',
							  'min_length': '密码不能少于8位',
							  'required': '密码不能为空'

						  })
	cpwd = forms.CharField(max_length=20,min_length=8,required=True,
						  error_messages={
							  'max_length': '确认密码不能超过20位',
							  'min_length': '确认密码不能少于8位',
							  'required': '确认密码不能为空'

						  })
	email = forms.CharField(required=True,error_messages={'required': '邮箱必填'})


	def clean(self):
		user = User.objects.filter(username=self.cleaned_data.get('user_name')).first()
		if user:
			raise forms.ValidationError({'user_name': '用户名已存在'})

		if self.cleaned_data.get('pwd') != self.cleaned_data.get('cpwd'):
			raise forms.ValidationError({'cpwd': '密码不一致'})

		return self.cleaned_data


class LoginForm(forms.Form):
	username = forms.CharField(max_length=20,min_length=5,required=True,
								error_messages={
									'max_length': '用户名不能超过20位',
									'min_length': '用户名不能少于5位',
									'required': '用户名不能为空'
								})
	pwd = forms.CharField (max_length=20, min_length=8, required=True,
						   error_messages={
							   'max_length': '密码不能超过20位',
							   'min_length': '密码不能少于8位',
							   'required': '密码不能为空'

						   })


class AddressForm(forms.Form):
	addressee = forms.CharField(required=True,min_length=2,error_messages={
		'required': '收件人为必填项',
		'min_length': '收件人姓名不能少于两个字符',

	})
	detailed_address = forms.CharField(required=True,min_length=10,error_messages={
		'required': '收件地址为必填项',
		'min_length': '收件地址不能少于十个字符'
	})
	zip_code = forms.CharField(required=True,min_length=6,max_length=6,error_messages={
		'required': '邮编必填',
		'min_length': '请填写正确的邮编格式',
		'max_length': '请填写正确的邮编格式'
	})
	phone = forms.CharField(required=True,min_length=3,max_length=15,error_messages={
		'required': '电话号码必填',
		'min_length': '电话号码不能短于3位',
		'max_length': '电话号码不能超过15位'
	})

