"""CodePedia URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
import xadmin
from django.views.generic import TemplateView
from users.views import ActiveView
from django.views.static import serve
from CodePedia.settings import MEDIA_ROOT, STATIC_ROOT
from projects.views import FileListlView, FunctionListlView

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^$', FileListlView.as_view(), name='index'),
    # 验证码插件
    url(r'^captcha/', include('captcha.urls')),
    # 配置上传文件的访问函数
    url(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve, {'document_root': STATIC_ROOT}),
    url(r'^users/', include('users.urls', namespace='users')),
    url(r'^projects/', include('projects.urls', namespace='projects')),
    # 所有文件
    url(r'^files/$', FileListlView.as_view(), name='file_list'),
    # 所有方法
    url(r'^methods/$', FunctionListlView.as_view(), name='method_list'),
    url(r'^qa/', include('qa.urls', namespace='qa')),
    url(r'^operations/', include('operations.urls', namespace='operations')),

]

handler404 = 'users.views.page_not_found'
handler500 = 'users.views.page_error'
