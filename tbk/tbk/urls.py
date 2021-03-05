"""tbk URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf import settings
from django.contrib import admin
from django.contrib.admin import AdminSite
from django.urls import path
from django_qiyu_utils.settings import SERVE_FILE_URLS

from core.views import (
    taobao,
    PingView,
    PrivacyView,
)
from web import views as web_views

assert isinstance(admin.site, AdminSite)
if settings.DEBUG:
    admin.site.site_header = "奇遇淘客 [测试环境]"
    admin.site.index_title = "奇遇淘客 [测试环境]"
    admin.site.site_title = "奇遇淘客 [测试环境]"
else:
    admin.site.site_header = "奇遇淘客 [线上环境]"
    admin.site.index_title = "奇遇淘客 [线上环境]"
    admin.site.site_title = "奇遇淘客 [线上环境]"

urlpatterns = [
    # 首页
    path("", web_views.IndexView.as_view(), name="index"),
    path("detail/<str:item_id>", web_views.DetailView.as_view(), name="detail"),
    path("search/", web_views.SearchView.as_view(), name="search"),
    path("privacy/", PrivacyView.as_view(), name="privacy"),
    path("taobao/cb", taobao.TaoBaoCB.as_view()),
    path("ping/", PingView.as_view(), name="ping"),
    # 管理后台
    path("admin/", admin.site.urls),
]

urlpatterns += SERVE_FILE_URLS
