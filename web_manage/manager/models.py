from django.db import models


# Create your models here.
# 院系信息
class depart_info(models.Model):
	depart_name = models.CharField(max_length=25, primary_key=True)


# 专业信息
class major_info(models.Model):
	major_name = models.CharField(max_length=25, primary_key=True)
	depart = models.ForeignKey('depart_info', to_field='depart_name', on_delete=models.DO_NOTHING)


# 年级信息
class grade_info(models.Model):
	grade_name = models.CharField(max_length=25, primary_key=True)


# 班级信息
class class_info(models.Model):
	class_name = models.CharField(max_length=10, primary_key=True)


# 学生基本信息
class stu_basic_info(models.Model):
	stu_number = models.CharField(max_length=25, primary_key=True)
	stu_name = models.CharField(max_length=25)
	department = models.ForeignKey('depart_info', to_field='depart_name', on_delete=models.DO_NOTHING)
	major = models.ForeignKey('major_info', to_field='major_name', on_delete=models.DO_NOTHING)
	grade = models.ForeignKey('grade_info', to_field='grade_name', on_delete=models.DO_NOTHING)
	stu_class = models.ForeignKey('class_info', to_field='class_name', on_delete=models.DO_NOTHING)
	sex = models.CharField(max_length=10, choices=(("男", "男"), ("女", "女")))
	ID_number = models.CharField(max_length=25)
	bank_number = models.CharField(max_length=25, null=True, blank=True)
	phone_number = models.CharField(max_length=25, null=True, blank=True)
	email = models.EmailField(max_length=255, unique=True, null=True, blank=True)
	photo = models.ImageField(upload_to='photo', null=True, blank=True)
	stu_card_photo = models.ImageField(upload_to='stu_card_photo', null=True, blank=True)


# 用户登录信息
class user_login_info(models.Model):
	account = models.CharField(max_length=25, primary_key=True)
	psword = models.CharField(max_length=25)
	have_login = models.CharField(max_length=5, default='0')
	have_alter = models.CharField(max_length=5, default='0')
	ip = models.CharField(max_length=25)
	jurisdiction = models.CharField(max_length=5)


# 职称信息
class profess_info(models.Model):
	profess_name = models.CharField(max_length=10, primary_key=True)


# 指导教师基本信息
class teach_basic_info(models.Model):
	tea_number = models.CharField(max_length=25, primary_key=True)
	tea_name = models.CharField(max_length=25)
	profess = models.ForeignKey('profess_info', to_field='profess_name', on_delete=models.DO_NOTHING)
	department = models.ForeignKey('depart_info', to_field='depart_name', on_delete=models.DO_NOTHING)
	major = models.ForeignKey('major_info', to_field='major_name', on_delete=models.DO_NOTHING)
	ID_number = models.CharField(max_length=25)
	email = models.EmailField(max_length=255, unique=True, null=True, blank=True)
	phone_number = models.CharField(max_length=25, null=True, blank=True)
	photo = models.ImageField(upload_to='photo', null=True, blank=True)


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
	com_id = models.ForeignKey(com_basic_info, to_field='com_id', on_delete=models.DO_NOTHING)
	apply_announce = models.TextField(null=True, blank=True)
	apply_step = models.TextField(null=True, blank=True)
	com_attachment = models.FileField(upload_to='com_attach', null=True, blank=True)


# 竞赛小组信息
class com_group_basic_info(models.Model):
	group_id = models.AutoField(primary_key=True)
	com_id = models.ForeignKey('com_basic_info', to_field='com_id', on_delete=models.DO_NOTHING, default='')
	group_name = models.CharField(max_length=25, null=True, blank=True)
	group_num = models.IntegerField(default=1)
	com_group = models.ForeignKey('com_sort_info', to_field='id', on_delete=models.SET_NULL, null=True, blank=True)
	product_name = models.CharField(max_length=50, null=True, blank=True)
	else_info = models.TextField(default='', null=True, blank=True)


# 竞赛学生信息
class com_stu_info(models.Model):
	com_id = models.ForeignKey('com_basic_info', to_field='com_id', on_delete=models.DO_NOTHING)
	group_id = models.ForeignKey('com_group_basic_info', to_field='group_id', on_delete=models.DO_NOTHING)
	stu_id = models.ForeignKey('stu_basic_info', to_field='stu_number', on_delete=models.DO_NOTHING)
	is_leader = models.BooleanField(default=0)


# 竞赛指导老师信息
class com_teach_info(models.Model):
	com_id = models.ForeignKey('com_basic_info', to_field='com_id', on_delete=models.DO_NOTHING)
	group_id = models.ForeignKey('com_group_basic_info', to_field='group_id', on_delete=models.DO_NOTHING)
	teach_id = models.ForeignKey('teach_basic_info', to_field='tea_number', on_delete=models.DO_NOTHING)


# 学生申请修改报名信息
class temp_com_group_basic_info(models.Model):
	temp_id = models.AutoField(primary_key=True)
	group_id = models.ForeignKey('com_group_basic_info', to_field='group_id', on_delete=models.CASCADE, default='')
	com_id = models.ForeignKey('com_basic_info', to_field='com_id', on_delete=models.CASCADE, default='')
	group_name = models.CharField(max_length=25, null=True, blank=True)
	group_num = models.IntegerField(default=1)
	com_group = models.ForeignKey('com_sort_info', to_field='id', on_delete=models.SET_NULL, null=True, blank=True)
	product_name = models.CharField(max_length=50, null=True, blank=True)
	else_info = models.TextField(default='', null=True, blank=True)


class temp_com_stu_info(models.Model):
	temp_id = models.ForeignKey('temp_com_group_basic_info', to_field='temp_id', on_delete=models.CASCADE)
	stu_id = models.ForeignKey('stu_basic_info', to_field='stu_number', on_delete=models.CASCADE)
	is_leader = models.BooleanField(default=0)


class temp_com_teach_info(models.Model):
	temp_id = models.ForeignKey('temp_com_group_basic_info', to_field='temp_id', on_delete=models.CASCADE)
	teach_id = models.ForeignKey('teach_basic_info', to_field='tea_number', on_delete=models.CASCADE)


# 竞赛组别信息
class com_sort_info(models.Model):
	id = models.AutoField(primary_key=True)
	com_id = models.ForeignKey('com_basic_info', to_field='com_id', on_delete=models.DO_NOTHING)
	sort_name = models.CharField(max_length=50)


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


# 关注比赛表
class stu_fllow_com_info(models.Model):
	stu_id = models.ForeignKey('stu_basic_info', to_field='stu_number', on_delete=models.DO_NOTHING)
	com_id = models.ForeignKey('com_basic_info', to_field='com_id', on_delete=models.DO_NOTHING)
	status = models.BooleanField(default=0)
