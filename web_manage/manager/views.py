from django.shortcuts import render_to_response,get_object_or_404,redirect,render
from django.core.paginator import Paginator
from django.conf import settings
from . import models
from . import forms 
import os

# Create your views here.
#主页
def home(request):
	context = {}
	return render(request,'home.html',context)

def login(request):
	context = {}
	if request.session.get('is_login',None):
		return redirect('/home')

	if request.method == "POST":
		t_account = request.POST.get('account', None)
		t_psword = request.POST.get('psword', None)
		context = {}
		message = "请填写正确的账号和密码！"
		if t_account and t_psword:
			t_account = t_account.strip()
			try:
				user = get_object_or_404(models.user_login_info,account=t_account)
				#权限说明（学生：1，指导老师：2，竞赛委员：3，辅导员：4）
				if user.psword == t_psword:
					request.session['is_login'] = True
					request.session['user_number'] = user.account
					#print(user.have_login)
					#初次登录需要修改个人信息
					#学生
					if user.have_login == '0' and user.jurisdiction == '1':
						return redirect('/alter_info_stu')
					#指导老师
					if user.have_login == '0' and user.jurisdiction == '2':
						return redirect('/alter_info_teach')
					return redirect('/home')
				else:
					message = "密码不正确！"
			except:
				message = "账号不存在！"
		context['message'] = message
		return render(request,'home.html',context)
	return render(request,'home.html',context)

def logout(request):
	if not request.session.get('is_login', None):
		return redirect("/home/")
	request.session.flush()
	return redirect("/home/")

def alter_info_stu(request):
	context = {}
	nid = request.session.get('user_number',None)
	stu_info = get_object_or_404(models.stu_basic_info,stu_number=nid)
	depart_info = models.depart_info.objects.all()
	major_info = models.major_info.objects.all()
	grade_info = models.grade_info.objects.all()
	class_info = models.class_info.objects.all()

	context = {}
	context['stu'] = stu_info
	context['depart_info'] = depart_info
	context['major_info'] = major_info
	context['grade_info'] = grade_info
	context['class_info'] = class_info

	#print(context['stu'][0])
	if request.method == "POST":
		stu_number = request.POST.get('stu_number')
		stu_name = request.POST.get('stu_name')
		department = request.POST.get('department')
		major = request.POST.get('major')
		grade = request.POST.get('grade')
		stu_class = request.POST.get('stu_class')
		ID_number = request.POST.get('ID_number')
		print(ID_number)

		if ID_number == None or ID_number == "" :
			context['message'] = "请务必填写身份证号！"
			return render(request,'alter_info_stu.html',context)

		bank_number = request.POST.get('bank_number')
		phone_number = request.POST.get('phone_number')

		if phone_number == None or phone_number == "":
			context['message'] = "请务必填写手机号码！"
			return render(request,'alter_info_stu.html',context)

		email = request.POST.get('email')

		if email == None or email == "":
			context['message'] = "请务必填写邮箱！"
			return render(request,'alter_info_stu.html',context)

		photo = request.FILES.get("photo")
		#print(photo)

		stu_info = models.stu_basic_info.objects.get(stu_number=nid)
		stu_info.stu_number = stu_number
		stu_info.stu_name = stu_name

		stu_info.department = get_object_or_404(models.depart_info,depart_name=department)
		stu_info.major = get_object_or_404(models.major_info,major_name=major)
		stu_info.grade = get_object_or_404(models.grade_info,grade_name=grade)
		stu_info.stu_class = get_object_or_404(models.class_info,class_name=stu_class)
		stu_info.ID_number = ID_number
		stu_info.bank_number = bank_number
		stu_info.phone_number = phone_number
		stu_info.email = email
		if photo != None:
			stu_info.photo = photo.name 
			url = settings.MEDIA_ROOT + 'stu_photo\\'+nid
			#判断路径是否存在
			isExists=os.path.exists(url)
			if not isExists:
				os.makedirs(url) 
			photo_url = open(settings.MEDIA_ROOT + 'stu_photo\\'+ nid +"\\" + photo.name, 'wb')
			for chunk in photo.chunks():
				photo_url.write(chunk)

		stu_info.save()
		#更改修改状态
		"""
		user_login = get_object_or_404(models.user_login_info,account=stu_number)
		user_login.have_login = 1
		user_login.have_alter = 1
		user_login.save()
		"""
		return redirect('/home/')  
	#stu_info = stu_basic_Form()
	return render(request,'alter_info_stu.html',context)
"""
		cnt = 0
		for f in photo:
			if cnt == 0:
				stu_info.photo = f.name
				print(f.name)
				cnt = cnt + 1
			else:
				stu_info.stu_card_photo = f.name
				print(f.name)

		cnt = 0
		for f in photo:
			if cnt == 0:
				photo_url = open(settings.MEDIA_ROOT + 'photo/' + f.name, 'wb')
				print(f.name)
				for chunk in f.chunks():
					photo_url.write(chunk)
				cnt = cnt + 1
			else:
				photo_url = open(settings.MEDIA_ROOT + 'stu_card_photo/' + f.name, 'wb')
				print(f.name)
				for chunk in f.chunks():
					photo_url.write(chunk)
"""

def alter_info_teach(request):
	context = {}
	nid = request.session.get('user_number',None)
	teach_info = get_object_or_404(models.teach_basic_info,tea_number=nid)
	profess_info = models.profess_info.objects.all()
	depart_info = models.depart_info.objects.all()
	major_info = models.major_info.objects.all()

	context['teach'] = teach_info
	context['profess_info'] = profess_info
	context['depart_info'] = depart_info
	context['major_info'] = major_info

	if request.method == "POST":
		tea_number = request.POST.get('tea_number')
		tea_name = request.POST.get('tea_name')
		profess = request.POST.get('profess')
		department = request.POST.get('department')
		major = request.POST.get('major')
		ID_number = request.POST.get('ID_number')
		phone_number = request.POST.get('phone_number')
		email = request.POST.get('email')
		photo = request.POST.get('photo')

		if ID_number == 'None' or ID_number == "":
			context['message'] = "请务必填写身份证号！"
			return render(request,'alter_info_teach.html',context)

		if phone_number == 'None' or phone_number == "":
			context['message'] = "请务必填写手机号码！"
			return render(request,'alter_info_teach.html',context)

		if email == 'None' or email == "":
			context['message'] = "请务必填写邮箱！"
			return render(request,'alter_info_stu.html',context)

		photo = request.FILES.get("photo")
		#print(photo)

		tea_info = models.teach_basic_info.objects.get(tea_number=nid)
		tea_info.tea_number = tea_number
		tea_info.tea_name = tea_name
		tea_info.profess = get_object_or_404(models.profess_info,profess_name=profess)
		tea_info.department = get_object_or_404(models.depart_info,depart_name=department)
		tea_info.major = get_object_or_404(models.major_info,major_name=major)
		tea_info.ID_number = ID_number
		tea_info.phone_number = phone_number
		tea_info.email = email

		if photo != None:
			tea_info.photo = photo.name 
			url = settings.MEDIA_ROOT + 'teach_photo\\'+nid
			#判断路径是否存在
			isExists=os.path.exists(url)
			if not isExists:
				os.makedirs(url) 
			photo_url = open(settings.MEDIA_ROOT + 'teach_photo\\'+ nid +"\\" + photo.name, 'wb')
			for chunk in photo.chunks():
				photo_url.write(chunk)

		tea_info.save()
		#更改修改状态
		"""
		user_login = get_object_or_404(models.user_login_info,account=tea_number)
		user_login.have_login = 1
		user_login.have_alter = 1
		user_login.save()
		"""
		return redirect('/home/')  

	return render(request,'alter_info_teach.html',context)

def com_list(request):
	context = {}
	com_basic_info = models.com_basic_info.objects.all()
	context['com_list'] = com_basic_info

	return render(request, 'com_list.html',context)

def com_detail(request):
	context = {}
	if request.method == 'GET':
		id = request.GET.get('id')
		#print(id)
		com_info = get_object_or_404(models.com_basic_info,com_id=id)
		#插入竞赛公告
		context['inform'] = str("[通知]竞赛通知")
		#插入报名流程
		context['flow'] = str("报名流程")
		context['com_info'] = com_info
	return render(request, 'com_detail.html', context)

def com_apply(request):
	context = {}
	if request.method == 'GET':
		id = request.GET.get('id')
		#print(id)
		com_info = get_object_or_404(models.com_basic_info,com_id=id)
		# 插入竞赛公告
		context['com_info'] = com_info
	return render(request, 'com_apply.html', context)