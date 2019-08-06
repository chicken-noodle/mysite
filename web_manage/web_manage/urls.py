"""web_manage URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib import admin
from django.conf import settings
from django.urls import path,re_path
from django.views.static import serve
from manager import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home),
    path('home/', views.home),
    path('login/', views.login),
    path('logout/', views.logout),
    path('alter_info_stu/', views.alter_info_stu),
    path('alter_info_teach/', views.alter_info_teach),
    path('com_list/', views.com_list),
    path('com_detail/', views.com_detail),
    path('com_apply_first/', views.com_apply_first),
    path('com_apply_second/', views.com_apply_second),
    path('personal_center_stu/',views.personal_center_stu),
    re_path(r'^media/(?P<path>.*)$', serve, {"document_root": settings.MEDIA_ROOT}),
]
