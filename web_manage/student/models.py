from django.db import models

# Create your models here.
# 学生基本信息
class stu_basic_info(models.Model):
	stu_number = models.CharField(max_length=25, primary_key=True, default='0')
	stu_name = models.CharField(max_length=25)
	department = models.ForeignKey('all.depart_info', to_field='depart_name', on_delete=models.DO_NOTHING)
	major = models.ForeignKey('all.major_info', to_field='major_name', on_delete=models.DO_NOTHING)
	grade = models.ForeignKey('all.grade_info', to_field='grade_name', on_delete=models.DO_NOTHING)
	stu_class = models.ForeignKey('all.class_info', to_field='class_name', on_delete=models.DO_NOTHING)
	sex = models.CharField(max_length=10, choices=(("男", "男"), ("女", "女")))
	ID_number = models.CharField(max_length=25)
	bank_number = models.CharField(max_length=25, null=True, blank=True)
	phone_number = models.CharField(max_length=25, null=True, blank=True)
	email = models.EmailField(max_length=255, null=True, blank=True)
	photo = models.ImageField(upload_to='photo', null=True, blank=True)
	stu_card_photo = models.ImageField(upload_to='stu_card_photo', null=True, blank=True)


# 竞赛学生信息
class com_stu_info(models.Model):
	com_id = models.ForeignKey('competition.com_basic_info', to_field='com_id', on_delete=models.DO_NOTHING)
	group_id = models.ForeignKey('competition.com_group_basic_info', to_field='group_id', on_delete=models.DO_NOTHING)
	stu_id = models.ForeignKey('stu_basic_info', to_field='stu_number', on_delete=models.DO_NOTHING)
	is_leader = models.BooleanField(default=0)


# 报名修改信息-学生
class temp_com_stu_info(models.Model):
	temp_id = models.ForeignKey('competition.temp_com_group_basic_info', to_field='temp_id', on_delete=models.CASCADE)
	stu_id = models.ForeignKey('stu_basic_info', to_field='stu_number', on_delete=models.CASCADE)
	is_leader = models.BooleanField(default=0)


# 关注比赛表
class stu_fllow_com_info(models.Model):
	stu_id = models.ForeignKey('stu_basic_info', to_field='stu_number', on_delete=models.DO_NOTHING)
	com_id = models.ForeignKey('competition.com_basic_info', to_field='com_id', on_delete=models.DO_NOTHING)
	status = models.BooleanField(default=0)
