from django.db import models


# Create your models here.
# 职称信息
class profess_info(models.Model):
	profess_name = models.CharField(max_length=10, primary_key=True)


# 指导教师基本信息
class teach_basic_info(models.Model):
	tea_number = models.CharField(max_length=25, primary_key=True, default='0')
	tea_name = models.CharField(max_length=25)
	profess = models.ForeignKey('profess_info', to_field='profess_name', on_delete=models.DO_NOTHING)
	department = models.ForeignKey('all.depart_info', to_field='depart_name', on_delete=models.DO_NOTHING)
	major = models.ForeignKey('all.major_info', to_field='major_name', on_delete=models.DO_NOTHING)
	ID_number = models.CharField(max_length=25)
	email = models.EmailField(max_length=255, null=True, blank=True)
	phone_number = models.CharField(max_length=25, null=True, blank=True)
	photo = models.ImageField(upload_to='photo', null=True, blank=True)


# 竞赛指导老师信息
class com_teach_info(models.Model):
	com_id = models.ForeignKey('competition.com_basic_info', to_field='com_id', on_delete=models.DO_NOTHING)
	group_id = models.ForeignKey('competition.com_group_basic_info', to_field='group_id', on_delete=models.DO_NOTHING)
	teach_id = models.ForeignKey('teach_basic_info', to_field='tea_number', on_delete=models.DO_NOTHING)


# 报名修改信息-教师
class temp_com_teach_info(models.Model):
	temp_id = models.ForeignKey('competition.temp_com_group_basic_info', to_field='temp_id', on_delete=models.CASCADE)
	teach_id = models.ForeignKey('teach_basic_info', to_field='tea_number', on_delete=models.CASCADE)
