"""__author__=wuliang"""
from django import forms

from goods.models import Goods, GoodsCategory


class GoodsForm(forms.Form):
	name = forms.CharField(required=True, max_length=20,
						   error_messages={
							   'required': '商品名称不能为空',
							   'max_length': '商品名称不能超过20个字符',
						   }
						   )

	goods_sn = forms.CharField(required=True,min_length=6,max_length=10,
							   error_messages={
								   'required': '商品号必须说明',
								   'max_length': '商品号最大10位',
								   'min_length': '商品号最小6位',
							   }
							   )

	category = forms.CharField(required=True,
							   error_messages={
								   'required': '商品分类必填'
							   }
							   )

	goods_nums = forms.IntegerField(required=True, error_messages={
		'required': '商品库存必须指定'
	})

	market_price = forms.FloatField(required=True, error_messages={
		'required': '市场价格必须指定'
	})

	shop_price = forms.FloatField(required=True, error_messages={
		'required': '本店价格必须指定'
	})

	goods_brief = forms.CharField(required=True,min_length=10,max_length=50,
	error_messages = {
		'required': '商品描述不能为空',
		'max_length': '商品名称不能超过50个字符',
		'min_length': '商品名称不能小于10个字符',
	}
	)

	goods_front_image = forms.ImageField(required=True,
										 error_messages={
											 'required':'图片必传'
										 })



	def clean_category(self):
		id = self.cleaned_data.get('category')
		category = GoodsCategory.objects.filter(pk=id).first()
		return category


	def clean(self):
		goods_sn = self.cleaned_data.get('goods_sn')
		goods = Goods.objects.filter(goods_sn=goods_sn).first()
		if goods:
			self.cleaned_data['id'] = goods.id

		return self.cleaned_data

