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
    #修改信息
    path('alter_info_stu/', views.alter_info_stu),
    path('alter_info_teach/', views.alter_info_teach),
    #竞赛报名
    path('com_list/', views.com_list),
    path('com_detail/', views.com_detail),
    path('com_attach_download',views.com_attach_download),
    path('com_apply_first/', views.com_apply_first),
    path('com_apply_second/', views.com_apply_second),
    #学生个人中心
    path('personal_center_stu/',views.personal_center_stu),
    path('apply_detail/',views.apply_detail),
    path('delete_apply/',views.delete_apply),
    #知道教师个人中心
    path('personal_cnter_teach/',views.personal_center_teach),
    path('reject_apply/',views.reject_apply),
    path('teach_apply_deatil/',views.teach_apply_deatil),
    #竞赛委员
    path('com_manage/',views.com_manage),
    path('set_com_status/',views.set_com_status),
    path('com_detail_manage/', views.com_detail_manage),
    path('com_edit/',views.com_edit),
    path('add_com/',views.add_com),
    path('add_com_complete/',views.add_com_complete),
    #静态资源
    re_path(r'^media/(?P<path>.*)$', serve, {"document_root": settings.MEDIA_ROOT}),
]
