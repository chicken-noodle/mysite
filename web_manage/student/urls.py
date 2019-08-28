from django.urls import path
from . import views

urlpatterns = [
	path('alter_info_stu/', views.alter_info_stu, name='alter_info_stu'),
	path('personal_center_stu/', views.personal_center_stu, name='personal_center_stu'),
	path('apply_detail/', views.apply_detail, name='apply_detail'),
	path('delete_apply/', views.delete_apply, name='delete_apply'),
	path('stu_apply_edit/', views.stu_apply_edit, name='stu_apply_edit'),
]
