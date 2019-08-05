from django.shortcuts import render_to_response,get_object_or_404,redirect,render
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from . import models
from . import forms 
import os

# Create your views here.
#主页
def home(request):
	context = {}
	return render(request,'home.html',context)
#登录
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
#注销
def logout(request):
	if not request.session.get('is_login', None):
		return redirect("/home/")
	request.session.flush()
	return redirect("/home/")
#学生修改个人信息
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
		#stu_number = request.POST.get('stu_number')
		#stu_name = request.POST.get('stu_name')
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
		#stu_info.stu_number = stu_number
		#stu_info.stu_name = stu_name

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
		#tea_number = request.POST.get('tea_number')
		#tea_name = request.POST.get('tea_name')
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
			return render(request,'alter_info_teach.html',context)

		photo = request.FILES.get("photo")
		#print(photo)

		tea_info = models.teach_basic_info.objects.get(tea_number=nid)
		#tea_info.tea_number = tea_number
		#tea_info.tea_name = tea_name
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

def com_apply_first(request):
	context = {}
	if request.method == 'GET':
		id = request.GET.get('id')
		#获取竞赛组别信息
		group_list = models.com_sort_info.objects.filter(com_id=id)
		#获取竞赛报名所需信息
		info_list = get_object_or_404(models.com_need_info, com_id=id)
		#获取竞赛信息
		com_info = get_object_or_404(models.com_basic_info,com_id=id)

		context['com_info'] = com_info
		context['info_list'] = info_list
		context['group_list'] = group_list
		context['tea_num'] = range(1,info_list.tea_num+1)
		num = com_info.num_stu
		context['stu_num'] = range(1,num+1)
		return render(request, 'com_apply/com_apply_first.html', context)
	if request.method == "POST":
		id = request.GET.get('id')
		com_info = get_object_or_404(models.com_basic_info, com_id=id)
		info_list = get_object_or_404(models.com_need_info, com_id=id)
		group_list = models.com_sort_info.objects.filter(com_id=id)

		# 人数
		# 是否需要满员(1；需要， 0：不需要)
		# 成员能否重复（同上）
		# 作品名称不能为空
		# 还有组别信息和备注
		# 小组名称
		num = com_info.num_stu
		flag_full = com_info.need_full
		flag_same = com_info.same_stu
		flag_proname = info_list.product_name
		flag_teanum = com_info.num_teach
		flag_group = info_list.com_group
		flag_else = info_list.else_info
		flag_groupname = info_list.group_name

		#获取页面学号输入
		stu_list = []
		for i in range(1,num+1):
			name = str("stu_num"+str(i))
			temp = request.POST.get(name)
			temp = temp.strip()
			if temp != None and temp != "":
				stu_list.append(temp)
		#获取学生信息
		stu_info_list = []
		for stu in stu_list:
			try:
				name = models.stu_basic_info.objects.get(stu_number=stu)
			except ObjectDoesNotExist:
				#回到first页面
				context['message'] = '无法搜索到学号对应学生信息，请确认学号无误'
				context['com_info'] = com_info
				context['info_list'] = info_list
				context['group_list'] = group_list
				context['tea_num'] = range(1, info_list.tea_num + 1)
				num = com_info.num_stu
				context['stu_num'] = range(1, num + 1)
				return render(request, 'com_apply/com_apply_first.html', context)
			else:
				stu_info_list.append(name)

		#判断是否符合条件，不符合则跳回first页面
		#判断满员
		len_stu = len(stu_info_list)
		if flag_full == 1:
			if len_stu != num:
				# 回到first页面
				context['message'] = '队伍人数不足 :('
				context['com_info'] = com_info
				context['info_list'] = info_list
				context['group_list'] = group_list
				context['tea_num'] = range(1, info_list.tea_num + 1)
				num = com_info.num_stu
				context['stu_num'] = range(1, num + 1)
				return render(request, 'com_apply/com_apply_first.html', context)
		#判断重复
		if flag_same == 0:
			list1 = stu_info_list
			list2 = list(set(list1))
			if len(list1) != len(list2):
				# 回到first页面
				context['message'] = '有重复人员的哦 :('
				context['com_info'] = com_info
				context['info_list'] = info_list
				context['group_list'] = group_list
				context['tea_num'] = range(1, info_list.tea_num + 1)
				num = com_info.num_stu
				context['stu_num'] = range(1, num + 1)
				return render(request, 'com_apply/com_apply_first.html', context)
		#判断作品名称是否为空
		if flag_proname == 1:
			prodect_name = request.POST.get('product_name')
			prodect_name = prodect_name.strip()
			if prodect_name == "":
				context['message'] = "作品名称没有填哦 X D "
				context['com_info'] = com_info
				context['info_list'] = info_list
				context['group_list'] = group_list
				context['tea_num'] = range(1, info_list.tea_num + 1)
				num = com_info.num_stu
				context['stu_num'] = range(1, num + 1)
				return render(request, 'com_apply/com_apply_first.html', context)
			context['product_name'] = prodect_name
		# 判断小组名称是否为空
		if flag_groupname == 1:
			group_name = request.POST.get('group_name')
			group_name = group_name.strip()
			if group_name == "":
				context['message'] = "小组名称没有填哦 X D "
				context['com_info'] = com_info
				context['info_list'] = info_list
				context['group_list'] = group_list
				context['tea_num'] = range(1, info_list.tea_num + 1)
				num = com_info.num_stu
				context['stu_num'] = range(1, num + 1)
				return render(request, 'com_apply/com_apply_first.html', context)
			context['group_name'] = group_name
		#对指导教师进行判断
		teach_list = []
		if flag_teanum:
			for i in range(1,flag_teanum+1):
				name = str('tea_name'+str(i))
				temp = request.POST.get(name)
				temp = temp.strip()
				teach = models.teach_basic_info.objects.filter(tea_name=temp)
				if len(teach) == 0:
					# 回到first页面
					context['message'] = '无法搜索到对应指导教师信息，请确认姓名无误'
					context['com_info'] = com_info
					context['info_list'] = info_list
					context['group_list'] = group_list
					context['tea_num'] = range(1, info_list.tea_num + 1)
					num = com_info.num_stu
					context['stu_num'] = range(1, num + 1)
					return render(request, 'com_apply/com_apply_first.html', context)
				else:
					# 教师信息列表中也是一个列表
					teach_list.append(teach)
			teach_list = zip(teach_list, range(1, info_list.tea_num + 1))
			context['teach_list'] = teach_list
		#对组别信息进行判断
		if flag_group == 1:
			group = request.POST.get("group")
			group_list = models.com_sort_info.objects.filter(com_id=id, sort_name=group)
			context['group'] = group_list[0]
		#备注信息
		if flag_else == 1:
			else_info = request.POST.get("else_info")
			context['else_info'] = else_info

		# 使用session存储报名学生
		request.session['stu_list'] = stu_list
		# 跳转确认页面
		context['stu_list'] = stu_info_list
		context['info_list'] = info_list
		return render(request, 'com_apply/com_apply_second.html', context)

	return render(request, 'com_apply/com_apply_first.html', context)

def com_apply_second(request):
	context = {}
	if request.method == 'POST':
		id = request.GET.get('id')
		com_info = get_object_or_404(models.com_basic_info, com_id=id)
		info_list = get_object_or_404(models.com_need_info, com_id=id)
		group_list = models.com_sort_info.objects.filter(com_id=id)

		num = com_info.num_stu
		flag_full = com_info.need_full
		flag_same = com_info.same_stu
		flag_proname = info_list.product_name
		flag_teanum = com_info.num_teach
		flag_group = info_list.com_group
		flag_else = info_list.else_info
		flag_groupname = info_list.group_name

		stu_list = request.session['stu_list']
		len_stu = len(stu_list)
		stu_info_list = []
		for stu in stu_list:
			name = models.stu_basic_info.objects.get(stu_number=stu)
			stu_info_list.append(name)

		group_name = request.POST.get('group_name')
		group = request.POST.get('group')
		product_name = request.POST.get('product_name')
		else_info = request.POST.get('else_info')


		# 分批保存信息，包括：竞赛小组信息、小组成员信息
		# 保存竞赛小组信息
		com_group = models.com_group_basic_info()
		# id
		com_group.com_id = get_object_or_404(models.com_basic_info, com_id=id)
		# 小组名字
		if flag_groupname == 1:
			com_group.group_name = group_name
		# 小组人数
		com_group.group_num = len_stu
		# 竞赛组别
		if flag_group == 1:
			group_list = models.com_sort_info.objects.filter(com_id=id, sort_name=group)
			com_group.com_group = group_list[0]
		# 作品名字
		if flag_proname == 1:
			com_group.product_name = product_name
		# 备注
		if flag_else == 1:
			com_group.else_info = else_info
		com_group.save()
		group_id = com_group.group_id
		# 保存小组成员信息
		for i in stu_info_list:
			stu = models.com_stu_info()
			stu.com_id = get_object_or_404(models.com_basic_info, com_id=id)
			stu.group_id = get_object_or_404(models.com_group_basic_info, group_id=group_id)
			stu.stu_id = i
			stu.save()

		teach_list = []
		if flag_teanum:
			for i in range(1, flag_teanum + 1):
				name = str('tea_name' + str(i))
				temp = request.POST.get(name)
				if temp != "" and temp != None:
					teach = models.teach_basic_info.objects.get(tea_number=temp)
					teach_list.append(teach)
			for i in teach_list:
				teach = models.com_teach_info()
				teach.com_id = get_object_or_404(models.com_basic_info, com_id=id)
				teach.group_id = get_object_or_404(models.com_group_basic_info, group_id=group_id)
				teach.teach_id = i
				teach.save()

	return render(request, 'com_apply/com_apply_complete.html', context)