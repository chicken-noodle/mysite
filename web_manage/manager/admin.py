from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(depart_info)
class user_login_info_Admin(admin.ModelAdmin):
	list_display=('depart_name',)

@admin.register(major_info)
class major_info_Admin(admin.ModelAdmin):
	list_display=('major_name',)

@admin.register(grade_info)
class grade_info_Admin(admin.ModelAdmin):
	list_display=('grade_name',)

@admin.register(class_info)
class class_info_Admin(admin.ModelAdmin):
	list_display=('class_name',)

@admin.register(stu_basic_info)
class stu_basic_info_Admin(admin.ModelAdmin):
	list_display=('stu_number','stu_name','department','major','grade'
		,'stu_class','sex','ID_number','bank_number','phone_number','email'
		,'photo','stu_card_photo',)

@admin.register(user_login_info)
class user_login_info_Admin(admin.ModelAdmin):
	list_display=('account','psword','ip','jurisdiction',)

