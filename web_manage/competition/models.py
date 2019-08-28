from django.db import models


# Create your models here.
# 竞赛基本信息
class com_basic_info(models.Model):
	com_id = models.AutoField(primary_key=True)
	com_name = models.CharField(max_length=50, unique=True)
	begin_regit = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
	end_regit = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
	begin_time = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
	end_time = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
	num_stu = models.IntegerField(default=1)
	need_full = models.BooleanField(default=0)
	same_stu = models.BooleanField(default=0)
	com_sort_num = models.IntegerField(default=0)
	com_web = models.CharField(max_length=225, null=True, blank=True)
	if_web = models.IntegerField(default=0)
	num_teach = models.IntegerField(default=1)
	com_status = models.IntegerField(default=0)


# 竞赛发布信息
class com_publish_info(models.Model):
	com_id = models.ForeignKey('com_basic_info', to_field='com_id', on_delete=models.DO_NOTHING)
	apply_announce = models.TextField(null=True, blank=True)
	apply_step = models.TextField(null=True, blank=True)
	com_attachment = models.FileField(upload_to='com_attach', null=True, blank=True)


# 竞赛组别信息
class com_sort_info(models.Model):
	id = models.AutoField(primary_key=True)
	com_id = models.ForeignKey('com_basic_info', to_field='com_id', on_delete=models.DO_NOTHING)
	sort_name = models.CharField(max_length=50)


# 竞赛小组信息
class com_group_basic_info(models.Model):
	group_id = models.AutoField(primary_key=True)
	com_id = models.ForeignKey('com_basic_info', to_field='com_id', on_delete=models.DO_NOTHING, default='')
	group_name = models.CharField(max_length=25, null=True, blank=True)
	group_num = models.IntegerField(default=1)
	com_group = models.ForeignKey('com_sort_info', to_field='id', on_delete=models.SET_NULL, null=True, blank=True)
	product_name = models.CharField(max_length=50, null=True, blank=True)
	else_info = models.TextField(default='', null=True, blank=True)


# 竞赛报名表所需信息信息
class com_need_info(models.Model):
	com_id = models.IntegerField(primary_key=True)
	stu_num = models.BooleanField(default=0)
	stu_name = models.BooleanField(default=0)
	ID_number = models.BooleanField(default=0)
	sex = models.BooleanField(default=0)
	depart = models.BooleanField(default=0)
	major = models.BooleanField(default=0)
	grade = models.BooleanField(default=0)
	stu_class = models.BooleanField(default=0)
	email = models.BooleanField(default=0)
	phone_num = models.BooleanField(default=0)
	com_group = models.BooleanField(default=0)
	group_name = models.BooleanField(default=0)
	product_name = models.BooleanField(default=0)
	tea_num = models.IntegerField(default=0)
	bank_number = models.BooleanField(default=0)
	else_info = models.BooleanField(default=0)


# 学生申请修改报名信息
class temp_com_group_basic_info(models.Model):
	temp_id = models.AutoField(primary_key=True)
	group_id = models.ForeignKey('com_group_basic_info', to_field='group_id', on_delete=models.CASCADE,
	                             default='')
	com_id = models.ForeignKey('com_basic_info', to_field='com_id', on_delete=models.CASCADE, default='')
	group_name = models.CharField(max_length=25, null=True, blank=True)
	group_num = models.IntegerField(default=1)
	com_group = models.ForeignKey('com_sort_info', to_field='id', on_delete=models.SET_NULL, null=True,
	                              blank=True)
	product_name = models.CharField(max_length=50, null=True, blank=True)
	else_info = models.TextField(default='', null=True, blank=True)
