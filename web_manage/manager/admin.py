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

@admin.register(profess_info)
class profess_info_Admin(admin.ModelAdmin):
	list_display=('profess_name',)

@admin.register(teach_basic_info)
class teach_basic_info_Admin(admin.ModelAdmin):
	list_display=('tea_number','tea_name','profess','department','major','ID_number','email','phone_number','photo',)

@admin.register(com_basic_info)
class com_basic_info_Admin(admin.ModelAdmin):
	list_display=('com_id','com_name','begin_regit','end_regit','begin_time','end_time','num_stu','need_full','same_stu','com_sort_num','com_web','if_web','num_teach',)

@admin.register(com_group_basic_info)
class com_group_basic_info_Admin(admin.ModelAdmin):
	list_display=('com_id','group_id','group_name','group_num',)

@admin.register(com_stu_info)
class com_stu_info_Admin(admin.ModelAdmin):
	list_display=('com_id','group_id','stu_id',)

@admin.register(com_sort_info)
class com_sort_info_Admin(admin.ModelAdmin):
	list_display=('com_id','sort_name',)

@admin.register(com_teach_info)
class com_teach_info_Admin(admin.ModelAdmin):
	list_display = ('com_id', 'group_id','teach_id',)

