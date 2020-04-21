from django.urls import path
from . import views

app_name = 'cms'

urlpatterns = [
    path('',views.index,name='index'),
    path('articles_category/',views.articles_category,name='articles_category'),
    path('add_articles_category/',views.add_articles_category,name='add_articles_category'),
    path('delete_articles_category/',views.delete_articles_category,name='delete_articles_category'),
    path('edit_articles_category/',views.edit_articles_category,name='edit_articles_category'),
    path('write_articles/', views.WriteArticles.as_view(),name='write_articles'),
    path('articles_list/', views.ArticlesListView.as_view(),name='articles_list'),
    path('edit_articles/', views.EditArticlesView.as_view(),name='edit_articles'),
    path('delete_articles/', views.delete_articles,name='delete_articles'),
]