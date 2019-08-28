from django.urls import path
from . import views

urlpatterns = [
	path('alter_info_teach/', views.alter_info_teach, name='alter_info_teach'),
	path('personal_center_teach/', views.personal_center_teach, name='personal_center_teach'),
	path('teach_apply_deatil/', views.teach_apply_deatil, name='teach_apply_deatil'),
	path('reject_apply/', views.reject_apply, name='reject_apply'),
]