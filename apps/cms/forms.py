from apps.forms import FormMixin
from django import forms
from apps.articles.models import Articles

class EditArticlesCategoryForm(forms.Form):
    pk = forms.IntegerField(error_messages={"required":"必须传入分类的id！"})
    name = forms.CharField(max_length=100)


class WriteArticlesForm(forms.ModelForm,FormMixin):
    category = forms.IntegerField()
    class Meta:
        model = Articles
        exclude =['category','author','pub_time']
        error_messages ={
            'title':{"required":"请输入标题"},
            'desc':{"required":"请输入描述"},
            'content':{"required":"请输入内容"},
        }

class EditArticlesForm(forms.ModelForm,FormMixin):
    category = forms.IntegerField()
    pk = forms.IntegerField()
    class Meta:
        model = Articles
        exclude = ['category','author','pub_time']
        error_messages = {
            'title': {"required": "请输入标题"},
            'desc': {"required": "请输入描述"},
            'content': {"required": "请输入内容"},
        }