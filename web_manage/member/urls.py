from django.urls import path
from . import views

urlpatterns = [
	path('com_manage/', views.com_manage, name='com_manage'),
	path('set_com_status/', views.set_com_status, name='set_com_status'),
	path('com_detail_manage/', views.com_detail_manage, name='com_detail_manage'),
	path('com_edit/', views.com_edit, name='com_edit'),
	path('add_com/', views.add_com, name='add_com'),
	path('add_com_complete/', views.add_com_complete, name='add_com_complete'),
	path('apply_application/', views.apply_application, name='apply_application'),
	path('apply_application_agree/', views.apply_application_agree, name='apply_application_agree'),
	path('apply_application_disagree/', views.apply_application_disagree, name='apply_application_disagree'),
]
