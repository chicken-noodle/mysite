from django.shortcuts import render_to_response, get_object_or_404, redirect, render
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, Http404, FileResponse
from django.conf import settings
import datetime
from . import models
from . import forms
import os


# Create your views here.
# 主页
def home(request):
	context = {}
	return render(request, 'home.html', context)


# 登录
def login(request):
	context = {}
	if request.session.get('is_login', None):
		return redirect('/home')

	if request.method == "POST":
		t_account = request.POST.get('account', None)
		t_psword = request.POST.get('psword', None)
		context = {}
		message = "请填写正确的账号和密码！"
		if t_account == "":
			context['message'] = "？？？输入账号啊"
			return render(request, 'login.html', context)
		if t_psword == "":
			context['message'] = "？？？倒是输密码啊"
			return render(request, 'login.html', context)
		if t_account and t_psword:
			t_account = t_account.strip()
			try:
				user = get_object_or_404(models.user_login_info, account=t_account)
				# 权限说明（学生：1，指导老师：2，竞赛委员：3，辅导员：4）
				if user.psword == t_psword:
					request.session['is_login'] = True
					request.session['user_number'] = user.account
					request.session['user_power'] = user.jurisdiction
					# print(request.session['user_power'])
					# print(type(request.session['user_power']))
					# 初次登录需要修改个人信息
					# 学生
					if user.have_alter == '0' and user.jurisdiction == '1':
						return redirect('/alter_info_stu')
					# 指导老师
					if user.have_alter == '0' and user.jurisdiction == '2':
						return redirect('/alter_info_teach')
					if user.have_alter == '0' and user.jurisdiction == '3':
						return redirect('/alter_info_teach')
					return redirect('/home')
				else:
					context['message'] = "???连密码都输不对吗？？？"
					return render(request, 'login.html', context)
			except:
				context['message'] = "账号不存在！"
				return render(request, 'login.html', context)
		return render(request, 'home.html', context)
	return render(request, 'login.html', context)


# 注销
def logout(request):
	if not request.session.get('is_login', None):
		return redirect("/home/")
	request.session.flush()
	return redirect("/home/")


# 学生修改个人信息
def alter_info_stu(request):
	context = {}
	nid = request.session.get('user_number', None)
	stu_info = get_object_or_404(models.stu_basic_info, stu_number=nid)
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

	# print(context['stu'][0])
	if request.method == "POST":
		# stu_number = request.POST.get('stu_number')
		# stu_name = request.POST.get('stu_name')
		department = request.POST.get('department')
		major = request.POST.get('major')
		grade = request.POST.get('grade')
		stu_class = request.POST.get('stu_class')
		ID_number = request.POST.get('ID_number')

		if ID_number == None or ID_number == "":
			context['message'] = "请务必填写身份证号！"
			return render(request, 'alter_info/alter_info_stu.html', context)

		bank_number = request.POST.get('bank_number')
		phone_number = request.POST.get('phone_number')

		if phone_number == None or phone_number == "":
			context['message'] = "请务必填写手机号码！"
			return render(request, 'alter_info/alter_info_stu.html', context)

		email = request.POST.get('email')

		if email == None or email == "":
			context['message'] = "请务必填写邮箱！"
			return render(request, 'alter_info/alter_info_stu.html', context)

		photo = request.FILES.get("photo")
		# print(photo)

		stu_info = models.stu_basic_info.objects.get(stu_number=nid)
		# stu_info.stu_number = stu_number
		# stu_info.stu_name = stu_name

		stu_info.department = get_object_or_404(models.depart_info, depart_name=department)
		stu_info.major = get_object_or_404(models.major_info, major_name=major)
		stu_info.grade = get_object_or_404(models.grade_info, grade_name=grade)
		stu_info.stu_class = get_object_or_404(models.class_info, class_name=stu_class)
		stu_info.ID_number = ID_number
		stu_info.bank_number = bank_number
		stu_info.phone_number = phone_number
		stu_info.email = email
		if photo != None:
			stu_info.photo = "stu_photo\\" + nid + "\\" + photo.name
			url = settings.MEDIA_ROOT + 'stu_photo\\' + nid
			# 判断路径是否存在
			isExists = os.path.exists(url)
			if not isExists:
				os.makedirs(url)
			photo_url = open(settings.MEDIA_ROOT + 'stu_photo\\' + nid + "\\" + photo.name, 'wb')
			for chunk in photo.chunks():
				photo_url.write(chunk)
			photo_url.close()

		stu_info.save()
		# 更改修改状态

		user_login = get_object_or_404(models.user_login_info, account=request.session['user_number'])
		user_login.have_login = '1'
		user_login.have_alter = '1'
		user_login.save()

		return redirect('/home/')
	# stu_info = stu_basic_Form()
	return render(request, 'alter_info/alter_info_stu.html', context)


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


# 教师修改个人信息
def alter_info_teach(request):
	context = {}
	nid = request.session.get('user_number', None)
	teach_info = get_object_or_404(models.teach_basic_info, tea_number=nid)
	profess_info = models.profess_info.objects.all()
	depart_info = models.depart_info.objects.all()
	major_info = models.major_info.objects.all()

	context['teach'] = teach_info
	context['profess_info'] = profess_info
	context['depart_info'] = depart_info
	context['major_info'] = major_info

	if request.method == "POST":
		# tea_number = request.POST.get('tea_number')
		# tea_name = request.POST.get('tea_name')
		profess = request.POST.get('profess')
		department = request.POST.get('department')
		major = request.POST.get('major')
		ID_number = request.POST.get('ID_number')
		phone_number = request.POST.get('phone_number')
		email = request.POST.get('email')
		photo = request.POST.get('photo')

		if ID_number == 'None' or ID_number == "":
			context['message'] = "请务必填写身份证号！"
			return render(request, 'alter_info/alter_info_teach.html', context)

		if phone_number == 'None' or phone_number == "":
			context['message'] = "请务必填写手机号码！"
			return render(request, 'alter_info/alter_info_teach.html', context)

		if email == 'None' or email == "":
			context['message'] = "请务必填写邮箱！"
			return render(request, 'alter_info/alter_info_teach.html', context)

		photo = request.FILES.get("photo")
		# print(photo)

		tea_info = models.teach_basic_info.objects.get(tea_number=nid)
		# tea_info.tea_number = tea_number
		# tea_info.tea_name = tea_name
		tea_info.profess = get_object_or_404(models.profess_info, profess_name=profess)
		tea_info.department = get_object_or_404(models.depart_info, depart_name=department)
		tea_info.major = get_object_or_404(models.major_info, major_name=major)
		tea_info.ID_number = ID_number
		tea_info.phone_number = phone_number
		tea_info.email = email

		if photo != None:
			tea_info.photo = photo.name
			url = settings.MEDIA_ROOT + 'teach_photo\\' + nid
			# 判断路径是否存在
			isExists = os.path.exists(url)
			if not isExists:
				os.makedirs(url)
			photo_url = open(settings.MEDIA_ROOT + 'teach_photo\\' + nid + "\\" + photo.name, 'wb')
			for chunk in photo.chunks():
				photo_url.write(chunk)

		tea_info.save()
		# 更改修改状态
		user_login = get_object_or_404(models.user_login_info, account=request.session['user_number'])
		user_login.have_login = '1'
		user_login.have_alter = '1'
		user_login.save()

		return redirect('/home/')

	return render(request, 'alter_info/alter_info_teach.html', context)


# 竞赛列表
def com_list(request):
	context = {}
	# 没有登录或者还未修改个人信息都无法报名
	try:
		is_login = request.session['is_login']
	except KeyError:
		context['have_login'] = "赶紧登录啦 :("
	else:
		user_num = request.session['user_number']
		user_info = get_object_or_404(models.user_login_info, account=user_num)
		if user_info.have_alter == '0':
			context['have_alter'] = "客官还没确认个人信息啦 :( 赶紧滚去修改"

	com_basic_info = models.com_basic_info.objects.all()
	context['com_list'] = com_basic_info
	return render(request, 'com_list.html', context)


# 竞赛详情
def com_detail(request):
	context = {}
	# 没有登录或者还未修改个人信息都无法报名
	try:
		is_login = request.session['is_login']
	except KeyError:
		return redirect("/com_list/")
	else:
		user_num = request.session['user_number']
		user_info = get_object_or_404(models.user_login_info, account=user_num)
		if user_info.have_alter == '0':
			return redirect("/com_list/")

	if request.method == 'GET':
		id = request.GET.get('id')
		# print(id)
		com_info = get_object_or_404(models.com_basic_info, com_id=id)
		com_publish = get_object_or_404(models.com_publish_info, com_id=com_info)
		# 插入竞赛公告
		context['inform'] = str("[通知]竞赛通知")
		# 插入发布信息
		context['com_publish'] = com_publish
		context['com_info'] = com_info
	return render(request, 'com_detail.html', context)


# 下载竞赛附件
def com_attach_download(request):
	com_id = request.GET.get('id')
	com_info = get_object_or_404(models.com_basic_info, com_id=com_id)
	com_publish = get_object_or_404(models.com_publish_info, com_id=com_info)
	# 返回下载
	filename = str(com_publish.com_attachment)
	file_path = settings.MEDIA_ROOT + filename

	print(file_path)

	ext = os.path.basename(file_path).split('.')[-1].lower()
	if ext not in ['py', 'db', 'sqlite3']:
		response = FileResponse(open(file_path, 'rb'))
		response['content_type'] = "application/octet-stream"
		response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
		return response
	else:
		raise Http404


# 报名参加比赛第一步
def com_apply_first(request):
	context = {}

	if request.method == 'GET':
		id = request.GET.get('id')
		# 获取竞赛组别信息
		group_list = models.com_sort_info.objects.filter(com_id=id)
		# 获取竞赛报名所需信息
		info_list = get_object_or_404(models.com_need_info, com_id=id)
		# 获取竞赛信息
		com_info = get_object_or_404(models.com_basic_info, com_id=id)

		context['com_info'] = com_info
		context['info_list'] = info_list
		context['group_list'] = group_list
		context['tea_num'] = range(1, info_list.tea_num + 1)
		num = com_info.num_stu
		context['stu_num'] = range(1, num + 1)
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

		# 获取页面学号输入
		stu_list = []
		for i in range(1, num + 1):
			name = str("stu_num" + str(i))
			temp = request.POST.get(name)
			temp = temp.strip()
			if temp != None and temp != "":
				stu_list.append(temp)
		# 获取学生信息
		stu_info_list = []
		for stu in stu_list:
			try:
				name = models.stu_basic_info.objects.get(stu_number=stu)
			except ObjectDoesNotExist:
				# 回到first页面
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

		# 判断是否符合条件，不符合则跳回first页面

		# 判断是够重复报名
		flag = 1
		if flag_same == 0:
			for stu in stu_info_list:
				com_list = models.com_stu_info.objects.filter(stu_id=stu)
				for com in com_list:
					if com.com_id == com_info:
						flag = 0
						break
		elif flag_same == 1:
			num = 1
			for stu in stu_info_list:
				com_list = models.com_stu_info.objects.filter(stu_id=stu)
				if num == 1:
					for com in com_list:
						if com.com_id == com_info:
							flag = 0
							break
				else:
					for com in com_list:
						if com.is_leader == 1:
							flag = 0
							break
				num = num + 1
		if flag == 0:
			# 回到first页面
			context['message'] = '参赛成员不符合规定哦 :('
			context['com_info'] = com_info
			context['info_list'] = info_list
			context['group_list'] = group_list
			context['tea_num'] = range(1, info_list.tea_num + 1)
			num = com_info.num_stu
			context['stu_num'] = range(1, num + 1)
			return render(request, 'com_apply/com_apply_first.html', context)

		# 判断满员
		student_num = com_info.num_stu
		len_stu = len(stu_info_list)
		if flag_full == 1:
			if len_stu != student_num:
				# 回到first页面
				context['message'] = '队伍人数不足 :('
				context['com_info'] = com_info
				context['info_list'] = info_list
				context['group_list'] = group_list
				context['tea_num'] = range(1, info_list.tea_num + 1)
				num = com_info.num_stu
				context['stu_num'] = range(1, num + 1)
				return render(request, 'com_apply/com_apply_first.html', context)
		# 判断学号重复
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
		# 判断作品名称是否为空
		if flag_proname == 1:
			prodect_name = request.POST.get('product_name')
			if prodect_name == "":
				context['message'] = "作品名称没有填哦 X D "
				context['com_info'] = com_info
				context['info_list'] = info_list
				context['group_list'] = group_list
				context['tea_num'] = range(1, info_list.tea_num + 1)
				num = com_info.num_stu
				context['stu_num'] = range(1, num + 1)
				return render(request, 'com_apply/com_apply_first.html', context)
			prodect_name = prodect_name.strip()
			context['product_name'] = prodect_name
		# 判断小组名称是否为空
		if flag_groupname == 1:
			group_name = request.POST.get('group_name')
			if group_name == "":
				context['message'] = "小组名称没有填哦 X D "
				context['com_info'] = com_info
				context['info_list'] = info_list
				context['group_list'] = group_list
				context['tea_num'] = range(1, info_list.tea_num + 1)
				num = com_info.num_stu
				context['stu_num'] = range(1, num + 1)
				return render(request, 'com_apply/com_apply_first.html', context)
			group_name = group_name.strip()
			context['group_name'] = group_name
		# 对指导教师进行判断
		teach_list = []
		if flag_teanum:
			for i in range(1, flag_teanum + 1):
				name = str('tea_name' + str(i))
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
		# 对组别信息进行判断
		if flag_group == 1:
			group = request.POST.get("group")
			group_list = models.com_sort_info.objects.filter(com_id=id, sort_name=group)
			context['group'] = group_list[0]
		# 备注信息
		if flag_else == 1:
			else_info = request.POST.get("else_info")
			else_info = else_info.strip()
			context['else_info'] = else_info

		# 跳转确认页面
		context['stu_list'] = stu_info_list
		context['info_list'] = info_list
		return render(request, 'com_apply/com_apply_second.html', context)

	return render(request, 'com_apply/com_apply_first.html', context)


# 报名参加比赛第二步
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

		# 优化
		stu_list = []
		for i in range(1, num + 1):
			stu_number = request.POST.get('stu_num' + str(i))
			if stu_number != None and stu_number != "":
				stu_list.append(stu_number)
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
		number = 1
		for i in stu_info_list:
			stu = models.com_stu_info()
			stu.com_id = get_object_or_404(models.com_basic_info, com_id=id)
			stu.group_id = get_object_or_404(models.com_group_basic_info, group_id=group_id)
			stu.stu_id = i
			if number == 1:
				stu.is_leader = 1
			number += 1
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
		return redirect('/personal_center_stu/?tag=2')
	return redirect('/personal_center_stu/?tag=2')


# 学生个人中心
def personal_center_stu(request):
	context = {}
	# 获取标签
	tag = request.GET.get('tag')
	# 获取图片
	stu_info = get_object_or_404(models.stu_basic_info, stu_number=request.session['user_number'])
	img_path = stu_info.photo
	context['stu_name'] = stu_info.stu_name
	context['stu_num'] = stu_info.stu_number
	context['photo'] = img_path
	if tag == '2':
		apply_list = models.com_stu_info.objects.filter(stu_id=stu_info.stu_number)
		com_list = []
		teach_list = []
		group_list = []
		for apply in apply_list:
			group_list.append(apply.group_id)
			com = get_object_or_404(models.com_basic_info, com_id=apply.com_id.com_id)
			com_list.append(com)
			teach_info = models.com_teach_info.objects.filter(com_id=com.com_id, group_id=apply.group_id)
			temp = []
			for teach in teach_info:
				teach = get_object_or_404(models.teach_basic_info, tea_number=teach.teach_id.tea_number)
				temp.append(teach)
			teach_list.append(temp)
		apply_info = zip(com_list, teach_list, group_list)
		context['apply_info'] = apply_info
		return render(request, 'personal_center_stu/my_apply.html', context)

	return render(request, 'personal_center_stu/overview.html', context)


# 学生个人中心-竞赛详情
def apply_detail(request):
	context = {}
	com_id = request.GET.get('p1')
	group_id = request.GET.get('p2')
	stu_info = get_object_or_404(models.stu_basic_info, stu_number=request.session['user_number'])
	img_path = stu_info.photo
	context['stu_name'] = stu_info.stu_name
	context['stu_num'] = stu_info.stu_number
	context['photo'] = img_path
	# 获取竞赛报名所需信息
	info_list = get_object_or_404(models.com_need_info, com_id=com_id)
	# 获取竞赛id和小组id，通过这两个id确定具体比赛具体小组
	com_info = get_object_or_404(models.com_basic_info, com_id=com_id)
	group_info = get_object_or_404(models.com_group_basic_info, group_id=group_id)

	stu_list = []
	stu_id_list = models.com_stu_info.objects.filter(group_id=group_info, com_id=com_info)
	for stu_info in stu_id_list:
		temp = get_object_or_404(models.stu_basic_info, stu_number=stu_info.stu_id.stu_number)
		stu_list.append((temp))

	teach_list = []
	teach_id_list = models.com_teach_info.objects.filter(group_id=group_info, com_id=com_info)
	for teach_info in teach_id_list:
		temp = get_object_or_404(models.teach_basic_info, tea_number=teach_info.teach_id.tea_number)
		teach_list.append(temp)

	com_group = models.com_group_basic_info.objects.filter(group_id=int(group_id), com_id=com_info)
	for competition in com_group:
		com_group_info = competition

	context['stu_list'] = stu_list
	context['info_list'] = info_list
	context['teach_list'] = teach_list
	context['com_group_info'] = com_group_info

	return render(request, "personal_center_stu/apply_detail.html", context)


# 学生个人中心-修改报名信息
def stu_apply_edit(request):
	context = {}
	com_id = request.GET.get('p1')
	group_id = request.GET.get('p2')

	com_info = get_object_or_404(models.com_basic_info, com_id=com_id)
	group_info = get_object_or_404(models.com_group_basic_info, group_id=group_id)
	depart_list = models.depart_info.objects.all()

	info_list = get_object_or_404(models.com_need_info, com_id=com_id)
	stu_list = models.com_stu_info.objects.filter(group_id=group_info)
	teach_list = models.com_teach_info.objects.filter(group_id=group_info)
	sort_list = models.com_sort_info.objects.filter(com_id=com_info)

	context['info_list'] = info_list
	context['stu_list'] = stu_list
	context['teach_list'] = teach_list
	context['sort_list'] = sort_list
	context['group_info'] = group_info
	context['depart_list'] = depart_list

	if request.method == 'POST':
		num = com_info.num_stu
		flag_full = com_info.need_full
		flag_same = com_info.same_stu
		flag_proname = info_list.product_name
		flag_teanum = com_info.num_teach
		flag_group = info_list.com_group
		flag_else = info_list.else_info
		flag_groupname = info_list.group_name

		stu_list = []
		for i in range(1, num + 1):
			name = str("stu_num" + str(i))
			temp = request.POST.get(name)
			temp = temp.strip()
			if temp:
				stu_list.append(temp)

		stu_info_list = []
		for stu in stu_list:
			try:
				name = models.stu_basic_info.objects.get(stu_number=stu)
			except ObjectDoesNotExist:
				context['message'] = '无法搜索到学号对应学生信息，请确认学号无误'
				return render(request, 'personal_center_stu/stu_apply_edit.html', context)
			else:
				stu_info_list.append(name)

		# 判断是够重复报名
		flag = 1
		if flag_same == 0:
			for stu in stu_info_list:
				com_list = models.com_stu_info.objects.filter(stu_id=stu)
				for com in com_list:
					if com.com_id == com_info and com.group_id != group_info:
						flag = 0
						break
		elif flag_same == 1:
			num = 1
			for stu in stu_info_list:
				com_list = models.com_stu_info.objects.filter(stu_id=stu)
				if num == 1:
					for com in com_list:
						if com.com_id == com_info and com.group_id != group_info:
							flag = 0
							break
				else:
					for com in com_list:
						if com.com_id == com_info and com.is_leader == 1 and com.group_id != group_info:
							flag = 0
							break
				num = num + 1
		if flag == 0:
			# 回到first页面
			context['message'] = '参赛成员不符合规定哦 :('
			return render(request, 'personal_center_stu/stu_apply_edit.html', context)
		# 判断满员
		student_num = com_info.num_stu
		len_stu = len(stu_info_list)
		if flag_full == 1:
			if len_stu != student_num:
				context['message'] = "人数不符合规定"
				return render(request, 'personal_center_stu/stu_apply_edit.html', context)
		# 判断学号重复
		list1 = stu_info_list
		list2 = list(set(list1))
		if len(list1) != len(list2):
			# 回到first页面
			context['message'] = '有重复人员的哦 :('
			return render(request, 'personal_center_stu/stu_apply_edit.html', context)
		# 判断作品名称是否为空
		if flag_proname == 1:
			prodect_name = request.POST.get('product_name')
			prodect_name = prodect_name.strip()
			if prodect_name == "":
				context['message'] = "作品名称没有填哦 X D "
				return render(request, 'personal_center_stu/stu_apply_edit.html', context)
		# 判断小组名称是否为空
		if flag_groupname == 1:
			group_name = request.POST.get('group_name')
			group_name = group_name.strip()
			if not group_name:
				context['message'] = "小组名称没有填哦 X D "
				return render(request, 'personal_center_stu/stu_apply_edit.html', context)
		# 获取教师信息
		teach_list = []
		if flag_teanum:
			for i in range(1, flag_teanum + 1):
				teach = request.POST.get(str('tea_name' + str(i))).strip()
				depart = request.POST.get(str('depart' + str(i)))
				teacher = models.teach_basic_info.objects.filter(tea_name=teach, department=depart)
				if not teacher:
					context['message'] = "指导教师信息不正确哦 X D "
					return render(request, 'personal_center_stu/stu_apply_edit.html', context)
				else:
					for info in teacher:
						teach_list.append(info)
		# 对组别信息进行判断
		if flag_group == 1:
			sort = request.POST.get("sort")
		# 备注信息
		if flag_else == 1:
			else_info = request.POST.get("else_info")
		if flag_proname == 1:
			product_name = request.POST.get('product_name').strip()

		# 报名中 - 直接修改
		if com_info.com_status == 0:
			pre_stu_list = models.com_stu_info.objects.filter(group_id=group_info)
			for pre_stu in pre_stu_list:
				pre_stu.delete()
			pre_teach_list = models.com_teach_info.objects.filter(group_id=group_info)
			for pre_teach in pre_teach_list:
				pre_teach.delete()
			pre_group_info = models.com_group_basic_info.objects.get(group_id=group_info.group_id)
			pre_group_info.delete()
			com_group = models.com_group_basic_info()
			com_group.com_id = com_info
			if flag_groupname == 1:
				com_group.group_name = group_name
			com_group.group_num = len_stu
			if flag_group == 1:
				sort_list = models.com_sort_info.objects.filter(com_id=com_info, sort_name=sort)
				com_group.com_group = sort_list[0]
			# 作品名字
			if flag_proname == 1:
				com_group.product_name = product_name
			# 备注
			if flag_else == 1:
				com_group.else_info = else_info
			com_group.save()
			now_group_id = com_group.group_id
			number = 1
			for i in stu_info_list:
				stu = models.com_stu_info()
				stu.com_id = com_info
				stu.group_id = get_object_or_404(models.com_group_basic_info, group_id=now_group_id)
				stu.stu_id = i
				if number == 1:
					stu.is_leader = 1
				number += 1
				stu.save()
			for i in teach_list:
				teach = models.com_teach_info()
				teach.com_id = com_info
				teach.group_id = get_object_or_404(models.com_group_basic_info, group_id=now_group_id)
				teach.teach_id = i
				teach.save()
			return redirect('/personal_center_stu/?tag=2')
		# 其他状态 - 提交申请
		else:
			temp_group = models.temp_com_group_basic_info()
			temp_group.temp_type = "报名信息"
			temp_group.group_id = group_info
			temp_group.com_id = com_info
			if flag_groupname == 1:
				temp_group.group_name = group_name
				temp_group.group_num = len_stu
			if flag_group == 1:
				sort_list = models.com_sort_info.objects.filter(com_id=com_info, sort_name=sort)
				temp_group.com_group = sort_list[0]
			# 作品名字
			if flag_proname == 1:
				temp_group.product_name = product_name
			# 备注
			if flag_else == 1:
				temp_group.else_info = else_info
			temp_group.save()

			temp_id = temp_group.temp_id

			number = 1
			for i in stu_info_list:
				stu = models.temp_com_stu_info()
				stu.temp_id = get_object_or_404(models.temp_com_group_basic_info, temp_id=temp_id)
				stu.stu_id = i
				if number == 1:
					stu.is_leader = 1
				number += 1
				stu.save()

			for i in teach_list:
				teach = models.temp_com_teach_info()
				teach.temp_id = get_object_or_404(models.temp_com_group_basic_info, temp_id=temp_id)
				teach.teach_id = i
				teach.save()
		return redirect('/personal_center_stu?tag=2')
	return render(request, 'personal_center_stu/stu_apply_edit.html', context)


# 学生个人中心-撤销报名
def delete_apply(request):
	context = {}
	stu_info = get_object_or_404(models.stu_basic_info, stu_number=request.session['user_number'])
	img_path = stu_info.photo
	context['stu_name'] = stu_info.stu_name
	context['stu_num'] = stu_info.stu_number
	context['photo'] = img_path

	com_id = request.GET.get('p1')
	group_id = request.GET.get('p2')
	com_info = get_object_or_404(models.com_basic_info, com_id=com_id)
	group_info = get_object_or_404(models.com_group_basic_info, group_id=group_id)

	stu_id_list = models.com_stu_info.objects.filter(group_id=group_info, com_id=com_info)
	stu_id_list.delete()

	teach_id_list = models.com_teach_info.objects.filter(group_id=group_info, com_id=com_info)
	teach_id_list.delete()

	com_group = models.com_group_basic_info.objects.filter(group_id=int(group_id), com_id=com_info)
	com_group.delete()

	return redirect('/personal_center_stu/?tag=2')


# 教师个人中心
def personal_center_teach(request):
	context = {}
	teach_id = request.session['user_number']
	# 获取教师信息
	teach_info = get_object_or_404(models.teach_basic_info, tea_number=teach_id)
	# 获取教师竞赛消息
	teach_com_list = models.com_teach_info.objects.filter(teach_id=teach_info)

	com_list = []
	stu_list = []
	group_list = []

	for teach in teach_com_list:
		com = get_object_or_404(models.com_basic_info, com_id=teach.com_id.com_id)
		temp_group_list = models.com_group_basic_info.objects.filter(group_id=teach.group_id.group_id,
		                                                             com_id=teach.com_id)
		for group in temp_group_list:
			group_list.append(group)
		temp_stu_list = models.com_stu_info.objects.filter(group_id=teach.group_id, com_id=teach.com_id)
		temp_list = []
		for stu in temp_stu_list:
			stu_info = get_object_or_404(models.stu_basic_info, stu_number=stu.stu_id.stu_number)
			temp_list.append(stu_info)
		stu_list.append(temp_list)
		com_list.append(com)
	"""
	print(com_list)
	print(stu_list)
	print(group_list)
	"""
	info_list = zip(com_list, stu_list, group_list)
	context['info_list'] = info_list
	return render(request, 'personal_center_teach/index.html', context)


# 教师个人中心-驳回报名
def reject_apply(request):
	context = {}

	com_id = request.GET.get('p1')
	group_id = request.GET.get('p2')
	com_info = get_object_or_404(models.com_basic_info, com_id=com_id)
	group_info = get_object_or_404(models.com_group_basic_info, group_id=group_id)

	stu_id_list = models.com_stu_info.objects.filter(group_id=group_info, com_id=com_info)
	stu_id_list.delete()

	teach_id_list = models.com_teach_info.objects.filter(group_id=group_info, com_id=com_info)
	teach_id_list.delete()

	com_group = models.com_group_basic_info.objects.filter(group_id=int(group_id), com_id=com_info)
	com_group.delete()

	return redirect('/personal_center_teach/')


# 教师个人中心-竞赛详情
def teach_apply_deatil(request):
	context = {}
	com_id = request.GET.get('p1')
	group_id = request.GET.get('p2')
	# 获取竞赛报名所需信息
	info_list = get_object_or_404(models.com_need_info, com_id=com_id)
	# 获取竞赛id和小组id，通过这两个id确定具体比赛具体小组
	com_info = get_object_or_404(models.com_basic_info, com_id=com_id)
	group_info = get_object_or_404(models.com_group_basic_info, group_id=group_id)

	stu_list = []
	stu_id_list = models.com_stu_info.objects.filter(group_id=group_info, com_id=com_info)
	for stu_info in stu_id_list:
		temp = get_object_or_404(models.stu_basic_info, stu_number=stu_info.stu_id.stu_number)
		stu_list.append((temp))

	teach_list = []
	teach_id_list = models.com_teach_info.objects.filter(group_id=group_info, com_id=com_info)
	for teach_info in teach_id_list:
		temp = get_object_or_404(models.teach_basic_info, tea_number=teach_info.teach_id.tea_number)
		teach_list.append(temp)

	com_group = models.com_group_basic_info.objects.filter(group_id=int(group_id), com_id=com_info)
	for competition in com_group:
		com_group_info = competition

	context['stu_list'] = stu_list
	context['info_list'] = info_list
	context['teach_list'] = teach_list
	context['com_group_info'] = com_group_info
	return render(request, "personal_center_teach/apply_detail.html", context)


# 学科委员-比赛管理
def com_manage(request):
	context = {}
	com_list = models.com_basic_info.objects.filter()

	context['com_list'] = com_list
	return render(request, 'personal_center_teach/com_management.html', context)


# 学科委员-设置竞赛状态
def set_com_status(request):
	if request.method == "POST":
		context = {}
		com_id = request.GET.get('p')
		com = get_object_or_404(models.com_basic_info, com_id=com_id)
		status = request.POST.get('status')
		if status != None:
			com.com_status = status
			com.save()
	return redirect('/com_manage/')


# 学科委员-比赛详情
def com_detail_manage(request):
	context = {}
	com_id = request.GET.get('p')
	com_info = get_object_or_404(models.com_basic_info, com_id=com_id)
	com_need = get_object_or_404(models.com_need_info, com_id=com_id)
	com_publish = get_object_or_404(models.com_publish_info, com_id=com_id)
	if com_info.com_sort_num != 0:
		sort_info = models.com_sort_info.objects.filter(com_id=com_info)
		sort_list = ''
		l = len(sort_info)
		t = 1
		for sort in sort_info:
			sort_name = sort.sort_name
			if t < l:
				sort_list += (sort_name + '/')
			else:
				sort_list += (sort_name)
			t += 1
		context['sort_list'] = sort_list
	context['com_info'] = com_info
	context['com_need'] = com_need
	context['com_publish'] = com_publish
	return render(request, 'personal_center_teach/com_detail.html', context)


# 学科委员-比赛编辑
def com_edit(request):
	context = {}
	if request.method == 'GET':
		com_id = request.GET.get('p')
		com_info = get_object_or_404(models.com_basic_info, com_id=com_id)
		com_need = get_object_or_404(models.com_need_info, com_id=com_id)
		com_publish = get_object_or_404(models.com_publish_info, com_id=com_id)
		if com_info.com_sort_num != 0:
			sort_info = models.com_sort_info.objects.filter(com_id=com_info)
			sort_list = ''
			l = len(sort_info)
			t = 1
			for sort in sort_info:
				sort_name = sort.sort_name
				if t < l:
					sort_list += (sort_name + '/')
				else:
					sort_list += (sort_name)
				t += 1
			context['sort_list'] = sort_list
		context['com_info'] = com_info
		context['com_need'] = com_need
		context['com_publish'] = com_publish
		return render(request, 'personal_center_teach/com_edit.html', context)
	if request.method == "POST":
		com_id = request.GET.get('p')
		# 竞赛信息
		name = request.POST.get('com_name')
		begin_regit = request.POST.get('begin_regit', None)
		# begin_regit = datetime.strptime(begin_regit, "%Y-%m-%d %H:%M:%S")
		end_regit = request.POST.get('end_regit', None)
		# end_regit = datetime.strptime(end_regit, "%Y-%m-%d %H:%M:%S")
		begin_time = request.POST.get('begin_time', None)
		# begin_time = datetime.strptime(begin_time, "%Y-%m-%d %H:%M:%S")
		end_time = request.POST.get('end_time', None)
		# end_time = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
		if_com_sort = request.POST.get('if_com_sort', '0')
		print(if_com_sort)
		print(type(if_com_sort))
		sort_list = request.POST.get('sort_list', '0')
		com_web = request.POST.get('com_web', '0')
		num_teach = request.POST.get('num_teach', '0')
		num_stu = request.POST.get('num_stu', '0')
		need_full = request.POST.get('need_full', '0')
		same_stu = request.POST.get('same_stu', '0')

		# 学生信息
		stu_num = request.POST.get('stu_num', '0')
		stu_name = request.POST.get('stu_name', '0')
		ID_number = request.POST.get('ID_number', '0')
		sex = request.POST.get('sex', '0')
		depart = request.POST.get('depart', '0')
		major = request.POST.get('major', '0')
		grade = request.POST.get('grade', '0')
		stu_class = request.POST.get('stu_class', '0')
		email = request.POST.get('email', '0')
		phone_num = request.POST.get('phone_num', '0')
		bank_number = request.POST.get('bank_number', '0')
		else_info = request.POST.get('else_info', '0')

		# 竞赛小组信息
		group_name = request.POST.get('group_name', '0')
		product_name = request.POST.get('product_name', '0')

		# 附件
		com_attach = request.FILES.get("com_attach", None)

		# 报名步骤
		step = request.POST.get('step', None)

		# 竞赛基本信息
		com_info = get_object_or_404(models.com_basic_info, com_id=com_id)
		com_info.com_name = name
		com_info.begin_regit = begin_regit
		com_info.end_regit = end_regit
		com_info.begin_time = begin_time
		com_info.end_time = end_time
		com_info.num_stu = num_stu
		if need_full == '1':
			com_info.need_full = 1
		else:
			com_info.need_full = 0
		if same_stu == '1':
			com_info.same_stu = 1
		else:
			com_info.same_stu = 0
		if sort_list != '0':
			list = sort_list.split("/")
			com_info.com_sort_num = len(list)
		if com_web != '0':
			com_info.if_web = 1
			com_info.com_web = com_web
		com_info.num_teach = num_teach
		com_info.com_status = 0
		com_info.save()

		# 组别信息
		if if_com_sort == '1' and sort_list != '0':
			temp_sort = models.com_sort_info.objects.filter(com_id=com_info)
			for temp in temp_sort:
				temp.delete()
			list = sort_list.split("/")
			for sort in list:
				sort_info = models.com_sort_info.objects.create(com_id=com_info, sort_name=sort)

		com_need = get_object_or_404(models.com_need_info, com_id=com_id)
		com_need.stu_num = stu_num
		com_need.stu_name = stu_name
		com_need.ID_number = ID_number
		com_need.sex = sex
		com_need.depart = depart
		com_need.major = major
		com_need.grade = grade
		com_need.stu_class = stu_class
		com_need.email = email
		com_need.phone_num = phone_num
		if sort_list != '0':
			com_need.com_group = 1
		else:
			com_need.com_group = 0
		com_need.group_name = group_name
		com_need.product_name = product_name
		com_need.tea_num = num_teach
		com_need.bank_number = bank_number
		com_need.else_info = else_info
		com_need.save()

		# 还差公告
		com_publish = get_object_or_404(models.com_publish_info, com_id=com_info)
		if com_attach != None:
			# 取出格式名
			f_name = com_attach.name
			f_name = f_name.split('.')[-1].lower()
			# 重命名文件
			com_publish.com_attachment = "com_attach\\" + str(com_info.com_id) + "\\" + str(
				com_info.com_id) + "." + f_name
			print(com_publish.com_attachment)
			url = settings.MEDIA_ROOT + 'com_attach\\' + str(com_info.com_id)
			# 判断路径是否存在
			isExists = os.path.exists(url)
			if not isExists:
				os.makedirs(url)
			file_url = open(settings.MEDIA_ROOT + "com_attach\\" + str(com_info.com_id) + "\\" + str(
				com_info.com_id) + "." + f_name,
			                'wb')
			for chunk in com_attach.chunks():
				file_url.write(chunk)
			file_url.close()
		if step != None or step != "":
			com_publish.apply_step = step
		com_publish.save()

		return redirect('/com_manage/')


# 学科委员—增加比赛
def add_com(request):
	context = {}
	if request.method == "POST":
		# 竞赛信息
		name = request.POST.get('com_name', None)
		context['name'] = name

		begin_regit = request.POST.get('begin_regit', None)
		print(begin_regit)
		context['begin_regit'] = begin_regit

		end_regit = request.POST.get('end_regit', None)
		context['end_regit'] = end_regit

		begin_time = request.POST.get('begin_time', None)
		context['begin_time'] = begin_time

		end_time = request.POST.get('end_time', None)
		context['end_time'] = end_time

		context['if_com_sort'] = request.POST.get('if_com_sort')
		if request.POST.get('if_com_sort') == '1':
			sort_list = request.POST.get('sort_list')
			context['sort_list'] = sort_list

		context['if_if_web'] = request.POST.get('if_if_web')
		if request.POST.get('if_if_web'):
			com_web = request.POST.get('com_web')
			context['com_web'] = com_web

		num_teach = request.POST.get('num_teach', '0')
		context['num_teach'] = num_teach

		num_stu = request.POST.get('num_stu', '0')
		context['num_stu'] = num_stu

		need_full = request.POST.get('need_full', '0')
		context['need_full'] = need_full

		same_stu = request.POST.get('same_stu', '0')
		context['same_stu'] = same_stu

		# 欠缺处理
		if name == "":
			context['warn'] = "竞赛名称要填写啊kora!"
			return render(request, 'personal_center_teach/add_com/first.html', context)
		if begin_regit == "":
			context['warn'] = "报名开始日期要填写啊kora!"
			return render(request, 'personal_center_teach/add_com/first.html', context)
		if end_regit == "":
			context['warn'] = "报名结束日期要填写啊kora!"
			return render(request, 'personal_center_teach/add_com/first.html', context)
		if begin_time == "":
			context['warn'] = "比赛开始日期要填写啊kora!"
			return render(request, 'personal_center_teach/add_com/first.html', context)
		if num_teach == "":
			context['warn'] = "指导教师人数要填写啊kora!"
			return render(request, 'personal_center_teach/add_com/first.html', context)
		if num_stu == "":
			context['warn'] = "参赛学生人数要填写啊kora!"
			return render(request, 'personal_center_teach/add_com/first.html', context)

		# 学生信息
		stu_num = request.POST.get('stu_num', '0')
		context['stu_num'] = stu_num

		stu_name = request.POST.get('stu_name', '0')
		context['stu_name'] = stu_name

		ID_number = request.POST.get('ID_number', '0')
		context['ID_number'] = ID_number

		sex = request.POST.get('sex', '0')
		context['sex'] = sex

		depart = request.POST.get('depart', '0')
		context['depart'] = depart

		major = request.POST.get('major', '0')
		context['major'] = major

		grade = request.POST.get('grade', '0')
		context['grade'] = grade

		stu_class = request.POST.get('stu_class', '0')
		context['stu_class'] = stu_class

		email = request.POST.get('email', '0')
		context['email'] = email

		phone_num = request.POST.get('phone_num', '0')
		context['phone_num'] = phone_num

		bank_number = request.POST.get('bank_number', '0')
		context['bank_number'] = bank_number

		else_info = request.POST.get('else_info', '0')
		context['else_info'] = else_info

		# 竞赛小组信息
		group_name = request.POST.get('group_name', '0')
		context['group_name'] = group_name

		product_name = request.POST.get('product_name', '0')
		context['product_name'] = product_name

		return render(request, 'personal_center_teach/add_com/second.html', context)
	return render(request, 'personal_center_teach/add_com/first.html', context)


# 学科委员—完成增加比赛
def add_com_complete(request):
	context = {}
	if request.method == "POST":
		# 竞赛信息
		name = request.POST.get('com_name')
		begin_regit = request.POST.get('begin_regit', None)
		end_regit = request.POST.get('end_regit', None)
		begin_time = request.POST.get('begin_time', None)
		end_time = request.POST.get('end_time', None)
		sort_list = request.POST.get('sort_list', '0')
		com_web = request.POST.get('com_web', '0')
		num_teach = request.POST.get('num_teach', '0')
		num_stu = request.POST.get('num_stu', '0')
		need_full = request.POST.get('need_full', '0')
		same_stu = request.POST.get('same_stu', '0')

		# 学生信息
		stu_num = request.POST.get('stu_num', '0')
		stu_name = request.POST.get('stu_name', '0')
		ID_number = request.POST.get('ID_number', '0')
		sex = request.POST.get('sex', '0')
		depart = request.POST.get('depart', '0')
		major = request.POST.get('major', '0')
		grade = request.POST.get('grade', '0')
		stu_class = request.POST.get('stu_class', '0')
		email = request.POST.get('email', '0')
		phone_num = request.POST.get('phone_num', '0')
		bank_number = request.POST.get('bank_number', '0')
		else_info = request.POST.get('else_info', '0')

		# 竞赛小组信息
		group_name = request.POST.get('group_name', '0')
		product_name = request.POST.get('product_name', '0')

		# 附件
		com_attach = request.FILES.get("com_attach", None)

		# 报名步骤
		step = request.POST.get('step', None)

		# 竞赛基本信息
		com_info = models.com_basic_info()
		com_info.com_name = name
		com_info.begin_regit = begin_regit
		com_info.end_regit = end_regit
		com_info.begin_time = begin_time
		com_info.end_time = end_time
		com_info.num_stu = num_stu
		if need_full == '1':
			com_info.need_full = 1
		else:
			com_info.need_full = 0
		if same_stu == '1':
			com_info.same_stu = 1
		else:
			com_info.same_stu = 0
		if sort_list != '0':
			list = sort_list.split("/")
			com_info.com_sort_num = len(list)
		if com_web != '0':
			com_info.if_web = 1
			com_info.com_web = com_web
		com_info.num_teach = num_teach
		com_info.com_status = 0
		com_info.save()

		if sort_list != '0':
			list = sort_list.split("/")
			for sort in list:
				sort_info = models.com_sort_info.objects.create(com_id=com_info, sort_name=sort)

		com_need = models.com_need_info()
		com_need.com_id = com_info.com_id
		com_need.stu_num = int(stu_num)
		com_need.stu_name = int(stu_name)
		com_need.ID_number = int(ID_number)
		com_need.sex = int(sex)
		com_need.depart = int(depart)
		com_need.major = int(major)
		com_need.grade = int(grade)
		com_need.stu_class = int(stu_class)
		com_need.email = int(email)
		com_need.phone_num = int(phone_num)
		if sort_list != '0':
			com_need.com_group = int(1)
		else:
			com_need.com_group = int(0)
		com_need.group_name = int(group_name)
		com_need.product_name = int(product_name)
		com_need.tea_num = int(num_teach)
		com_need.bank_number = int(bank_number)
		com_need.else_info = int(else_info)
		com_need.save()

		# 还差公告
		# 
		# ext = os.path.basename(file_path).split('.')[-1].lower()
		# 
		com_publish = models.com_publish_info()
		com_publish.com_id = com_info
		if com_attach != None:
			# 取出格式名
			f_name = com_attach.name
			f_name = f_name.split('.')[-1].lower()
			# 重命名文件
			com_publish.com_attachment = "com_attach\\" + str(com_info.com_id) + "\\" + str(
				com_info.com_id) + "." + f_name
			print(com_publish.com_attachment)
			url = settings.MEDIA_ROOT + 'com_attach\\' + str(com_info.com_id)
			# 判断路径是否存在
			isExists = os.path.exists(url)
			if not isExists:
				os.makedirs(url)
			file_url = open(settings.MEDIA_ROOT + "com_attach\\" + str(com_info.com_id) + "\\" + str(
				com_info.com_id) + "." + f_name,
			                'wb')
			for chunk in com_attach.chunks():
				file_url.write(chunk)
			file_url.close()
		if step != None:
			com_publish.apply_step = step
		com_publish.save()

		return redirect('/com_manage/')
	return render(request, 'personal_center_teach/add_com/second.html', context)


def apply_application(request):
	context = {}
	apply_application_list = models.temp_com_group_basic_info.objects.all()
	pre_group_list = []
	com_need_list = []
	stu_pre_list = []
	stu_apply_list = []
	teach_pre_list = []
	teach_apply_list = []

	apply_info_list = []
	for apply_application in apply_application_list:
		pre_group_info = apply_application.group_id
		com_need_info = get_object_or_404(models.com_need_info, com_id=apply_application.com_id.com_id)

		temp_stu_list = ''
		temp_student_list = models.temp_com_stu_info.objects.filter(temp_id=apply_application)
		for temp_student in temp_student_list:
			temp_stu_list += str(temp_student.stu_id.stu_name) + ' '

		pre_stu_list = ''
		pre_student_list = models.com_stu_info.objects.filter(group_id=apply_application.group_id)
		for pre_student in pre_student_list:
			pre_stu_list += str(pre_student.stu_id.stu_name) + ' '

		temp_teach_list = ''
		temp_teacher_list = models.temp_com_teach_info.objects.filter(temp_id=apply_application)
		for temp_teacher in temp_teacher_list:
			temp_teach_list += str(temp_teacher.teach_id.tea_name) + ' '

		pre_teach_list = ''
		pre_teacher_list = models.com_teach_info.objects.filter(group_id=apply_application.group_id)
		for pre_teacher in pre_teacher_list:
			pre_teach_list += str(pre_teacher.teach_id.tea_name) + ' '

		pre_group_list.append(pre_group_info)
		com_need_list.append(com_need_info)
		stu_pre_list.append(pre_stu_list)
		stu_apply_list.append(temp_stu_list)
		teach_pre_list.append(pre_teach_list)
		teach_apply_list.append(temp_teach_list)

	apply_info_list = zip(com_need_list, apply_application_list, pre_group_list, stu_pre_list, stu_apply_list,
	                      teach_pre_list, teach_apply_list)
	context['apply_info_list'] = apply_info_list
	return render(request, 'personal_center_teach/apply_application.html', context)


def apply_application_agree(request):
	temp_id = request.GET.get('id')
	temp_info = get_object_or_404(models.temp_com_group_basic_info, temp_id=temp_id)
	group_info = temp_info.group_id

	# 修改小组信息
	group_info.group_name = temp_info.group_name
	group_info.group_num = temp_info.group_num
	group_info.com_group = temp_info.com_group
	group_info.product_name = temp_info.product_name
	group_info.else_info = temp_info.else_info
	group_info.save()

	# 修改小组学生信息
	temp_stu_list = models.temp_com_stu_info.objects.filter(temp_id=temp_info)
	pre_stu_list = models.com_stu_info.objects.filter(group_id=group_info)
	for pre_stu in pre_stu_list:
		pre_stu.delete()
	for temp_stu in temp_stu_list:
		new_stu = models.com_stu_info()
		new_stu.com_id = group_info.com_id
		new_stu.group_id = group_info
		new_stu.stu_id = temp_stu.stu_id
		new_stu.is_leader = temp_stu.is_leader
		new_stu.save()
		temp_stu.delete()

	# 修改指导教师信息
	temp_teach_list = models.temp_com_teach_info.objects.filter(temp_id=temp_info)
	pre_teach_list = models.com_teach_info.objects.filter(group_id=group_info)
	for pre_teach in pre_teach_list:
		pre_teach.delete()
	for temp_teach in temp_teach_list:
		new_teach = models.com_teach_info()
		new_teach.com_id = group_info.com_id
		new_teach.group_id = group_info
		new_teach.teach_id = temp_teach.teach_id
		new_teach.save()
		temp_teach.delete()

	temp_info.delete()

	return redirect('/apply_application/')


def apply_application_disagree(request):
	return
