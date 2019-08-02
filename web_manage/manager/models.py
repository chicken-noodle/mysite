from django.db import models

# Create your models here.
#院系信息
class depart_info(models.Model):
	depart_name = models.CharField(max_length=25, primary_key=True)

#专业信息
class major_info(models.Model):
	major_name = models.CharField(max_length=25, primary_key=True)

#年级信息
class grade_info(models.Model):
	grade_name = models.CharField(max_length=25, primary_key=True)

#班级信息
class class_info(models.Model):
	class_name = models.CharField(max_length=10, primary_key=True)

#学生基本信息
class stu_basic_info(models.Model):
	stu_number = models.CharField(max_length=25, primary_key=True)
	stu_name = models.CharField(max_length=25)
	department = models.ForeignKey('depart_info', to_field='depart_name', on_delete=models.DO_NOTHING)
	major = models.ForeignKey('major_info', to_field='major_name', on_delete=models.DO_NOTHING)
	grade = models.ForeignKey('grade_info', to_field='grade_name', on_delete=models.DO_NOTHING)
	stu_class =  models.ForeignKey('class_info', to_field='class_name', on_delete=models.DO_NOTHING)
	sex = models.CharField(max_length=5, choices=(("male", "男"), ("female", "女")))
	ID_number = models.CharField(max_length=25)
	bank_number = models.CharField(max_length=25, null=True, blank=True)
	phone_number = models.CharField(max_length=25, null=True, blank=True)
	email = models.EmailField(max_length=255, unique=True, null=True, blank=True)
	photo = models.ImageField(upload_to='photo', null=True, blank=True)
	stu_card_photo = models.ImageField(upload_to='stu_card_photo', null=True, blank=True)

#用户登录信息
class user_login_info(models.Model):
	account = models.CharField(max_length=25, primary_key=True)
	psword = models.CharField(max_length=25)
	have_login = models.CharField(max_length=5,default='0')
	have_alter = models.CharField(max_length=5,default='0')
	ip = models.CharField(max_length=25)
	jurisdiction = models.CharField(max_length=5)

#职称信息
class profess_info(models.Model):
	profess_name = models.CharField(max_length=10, primary_key=True)

#指导教师基本信息
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

#竞赛基本信息
class com_basic_info(models.Model):
	com_id = models.AutoField(primary_key=True)
	com_name = models.CharField(max_length=50)
	begin_regit = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
	end_regit = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
	begin_time = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
	end_time = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
	num_stu = models.IntegerField(null=True, blank=True)
	need_full = models.IntegerField(null=True, blank=True)
	same_stu = models.IntegerField(null=True, blank=True)
	com_web = models.CharField(max_length=225, null=True, blank=True)
	if_web = models.IntegerField(null=True, blank=True)
	num_teach = models.IntegerField(null=True, blank=True)

#竞赛小组信息
class com_group_basic_info(models.Model):
	com_id = models.ForeignKey('com_basic_info', to_field='com_id', on_delete=models.DO_NOTHING)
	group_id = models.IntegerField()
	group_name = models.CharField(max_length=25,null=True, blank=True)
	group_num = models.IntegerField(null=True, blank=True)
	class Meta:
		unique_together = ('com_id', 'group_id')

#竞赛学生信息
class com_stu_info(models.Model):
	com_id = models.ForeignKey('com_basic_info', to_field='com_id', on_delete=models.DO_NOTHING)
	group_id = models.IntegerField(null=True, blank=True)
	stu_id = models.ForeignKey('stu_basic_info', to_field='stu_number', on_delete=models.DO_NOTHING)