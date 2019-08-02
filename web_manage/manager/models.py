from django.db import models

# Create your models here.
"""
登录信息表（账号，密码，ip地址，权限）
"""

class depart_info(models.Model):
	depart_name = models.CharField(max_length=25, primary_key=True)

class major_info(models.Model):
	major_name = models.CharField(max_length=25, primary_key=True)

class grade_info(models.Model):
	grade_name = models.CharField(max_length=25, primary_key=True)

class class_info(models.Model):
	class_name = models.CharField(max_length=10, primary_key=True)

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

class user_login_info(models.Model):
	account = models.CharField(max_length=25, primary_key=True)
	psword = models.CharField(max_length=25)
	have_login = models.CharField(max_length=5,default='0')
	have_alter = models.CharField(max_length=5,default='0')
	ip = models.CharField(max_length=25)
	jurisdiction = models.CharField(max_length=5)

class profess_info(models.Model):
	profess_name = models.CharField(max_length=10, primary_key=True)

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
