"""Blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path,include
from apps.articles import views
from django.views import static
from django.conf import settings
from django.conf.urls import url



urlpatterns = [
    path('',views.index,name='index' ),
    path('about',views.aboutme,name='aboutme'),
    path('cms/', include('apps.cms.urls')),
    path('account/', include('apps.blogauth.urls')),
    path('ueditor/', include('apps.ueditor.urls')),
    path('articles/', include('apps.articles.urls')),
    path('date/<int:year>/<int:month>/<int:day>/',views.timecate,name='date'),
    url(r'^static/(?P<path>.*)$', static.serve,{'document_root': settings.STATIC_ROOT}, name='static'),
]

