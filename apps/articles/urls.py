from django.urls import path
from . import views

app_name = 'articles'

urlpatterns = [
    path('list/',views.articles_list,name='articles_list'),
    path('<int:articles_id>/',views.articles_detail,name='articles_detail'),
    path('comment/',views.comment,name = 'comment'),
]