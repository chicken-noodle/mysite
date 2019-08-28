from django.urls import path
from . import views

#start with blog
urlpatterns = [
	#http://localhost:8000/
	path('', views.home, name='home'),
	path('home/', views.home, name='home'),
	path('login/', views.login, name='login'),
	path('logout/', views.logout, name='logout'),
]