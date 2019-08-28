from django.shortcuts import render_to_response, get_object_or_404, redirect, render
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, Http404, FileResponse
from django.conf import settings
import datetime
from . import models
import os
import all.models as all_model
import competition.models as competition_model
import teacher.models as teacher_model


# Create your views here.
# 学生修改个人信息
def alter_info_stu(request):
	context = {}
	nid = request.session.get('user_number', None)
	stu_info = get_object_or_404(models.stu_basic_info, stu_number=nid)
	depart_info = all_model.depart_info.objects.all()
	major_info = all_model.major_info.objects.all()
	grade_info = all_model.grade_info.objects.all()
	class_info = all_model.class_info.objects.all()

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
			return render(request, 'student/alter_info_stu.html', context)

		bank_number = request.POST.get('bank_number')
		phone_number = request.POST.get('phone_number')

		if phone_number == None or phone_number == "":
			context['message'] = "请务必填写手机号码！"
			return render(request, 'student/alter_info_stu.html', context)

		email = request.POST.get('email')

		if email == None or email == "":
			context['message'] = "请务必填写邮箱！"
			return render(request, 'student/alter_info_stu.html', context)

		photo = request.FILES.get("photo")
		# print(photo)

		stu_info = models.stu_basic_info.objects.get(stu_number=nid)
		# stu_info.stu_number = stu_number
		# stu_info.stu_name = stu_name

		stu_info.department = get_object_or_404(all_model.depart_info, depart_name=department)
		stu_info.major = get_object_or_404(all_model.major_info, major_name=major)
		stu_info.grade = get_object_or_404(all_model.grade_info, grade_name=grade)
		stu_info.stu_class = get_object_or_404(all_model.class_info, class_name=stu_class)
		stu_info.ID_number = ID_number
		stu_info.bank_number = bank_number
		stu_info.phone_number = phone_number
		stu_info.email = email
		if photo != None:
			f_name = photo.name
			f_name = f_name.split('.')[-1].lower()
			# 重命名照片
			stu_info.photo = "stu_photo\\" + nid + "\\" + 'head' + '.' + f_name
			url = settings.MEDIA_ROOT + 'stu_photo\\' + nid
			# 判断路径是否存在
			isExists = os.path.exists(url)
			if not isExists:
				os.makedirs(url)
			photo_url = open(settings.MEDIA_ROOT + "stu_photo\\" + nid + "\\" + 'head' + '.' + f_name,
			                 'wb')
			for chunk in photo.chunks():
				photo_url.write(chunk)
			photo_url.close()

		stu_info.save()
		# 更改修改状态

		user_login = get_object_or_404(all_model.user_login_info, account=request.session['user_number'])
		user_login.have_login = '1'
		user_login.have_alter = '1'
		user_login.save()

		return redirect('/home/')
	# stu_info = stu_basic_Form()
	return render(request, 'student/alter_info_stu.html', context)


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
			com = get_object_or_404(competition_model.com_basic_info, com_id=apply.com_id.com_id)
			com_list.append(com)
			teach_info = teacher_model.com_teach_info.objects.filter(com_id=com.com_id, group_id=apply.group_id)
			temp = []
			for teach in teach_info:
				teach = get_object_or_404(teacher_model.teach_basic_info, tea_number=teach.teach_id.tea_number)
				temp.append(teach)
			teach_list.append(temp)
		apply_info = zip(com_list, teach_list, group_list)
		context['apply_info'] = apply_info
		return render(request, 'student/personal_center/my_apply.html', context)

	return render(request, 'student/personal_center/overview.html', context)


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
	info_list = get_object_or_404(competition_model.com_need_info, com_id=com_id)
	# 获取竞赛id和小组id，通过这两个id确定具体比赛具体小组
	com_info = get_object_or_404(competition_model.com_basic_info, com_id=com_id)
	group_info = get_object_or_404(competition_model.com_group_basic_info, group_id=group_id)

	stu_list = []
	stu_id_list = models.com_stu_info.objects.filter(group_id=group_info, com_id=com_info)
	for stu_info in stu_id_list:
		temp = get_object_or_404(models.stu_basic_info, stu_number=stu_info.stu_id.stu_number)
		stu_list.append((temp))

	teach_list = []
	teach_id_list = teacher_model.com_teach_info.objects.filter(group_id=group_info, com_id=com_info)
	for teach_info in teach_id_list:
		temp = get_object_or_404(teacher_model.teach_basic_info, tea_number=teach_info.teach_id.tea_number)
		teach_list.append(temp)

	com_group = competition_model.com_group_basic_info.objects.filter(group_id=int(group_id), com_id=com_info)
	for competition in com_group:
		com_group_info = competition

	context['stu_list'] = stu_list
	context['info_list'] = info_list
	context['teach_list'] = teach_list
	context['com_group_info'] = com_group_info

	return render(request, "student/personal_center/apply_detail.html", context)


# 学生个人中心-修改报名信息
def stu_apply_edit(request):
	context = {}
	com_id = request.GET.get('p1')
	group_id = request.GET.get('p2')
	com_info = get_object_or_404(competition_model.com_basic_info, com_id=com_id)
	group_info = get_object_or_404(competition_model.com_group_basic_info, group_id=group_id)
	depart_list = all_model.depart_info.objects.all()

	info_list = get_object_or_404(competition_model.com_need_info, com_id=com_id)
	stu_list = models.com_stu_info.objects.filter(group_id=group_info)
	teach_list = teacher_model.com_teach_info.objects.filter(group_id=group_info)
	sort_list = competition_model.com_sort_info.objects.filter(com_id=com_info)

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
				return render(request, 'student/personal_center/stu_apply_edit.html', context)
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
			return render(request, 'student/personal_center/stu_apply_edit.html', context)
		# 判断满员
		student_num = com_info.num_stu
		len_stu = len(stu_info_list)
		if flag_full == 1:
			if len_stu != student_num:
				context['message'] = "人数不符合规定"
				return render(request, 'student/personal_center/stu_apply_edit.html', context)
		# 判断学号重复
		list1 = stu_info_list
		list2 = list(set(list1))
		if len(list1) != len(list2):
			# 回到first页面
			context['message'] = '有重复人员的哦 :('
			return render(request, 'student/personal_center/stu_apply_edit.html', context)
		# 判断作品名称是否为空
		if flag_proname == 1:
			prodect_name = request.POST.get('product_name')
			prodect_name = prodect_name.strip()
			if prodect_name == "":
				context['message'] = "作品名称没有填哦 X D "
				return render(request, 'student/personal_center/stu_apply_edit.html', context)
		# 判断小组名称是否为空
		if flag_groupname == 1:
			group_name = request.POST.get('group_name')
			group_name = group_name.strip()
			if not group_name:
				context['message'] = "小组名称没有填哦 X D "
				return render(request, 'student/personal_center/stu_apply_edit.html', context)
		# 获取教师信息
		teach_list = []
		if flag_teanum:
			for i in range(1, flag_teanum + 1):
				teach = request.POST.get(str('tea_name' + str(i))).strip()
				depart = request.POST.get(str('depart' + str(i)))
				teacher = teacher_model.teach_basic_info.objects.filter(tea_name=teach, department=depart)
				if not teacher:
					context['message'] = "指导教师信息不正确哦 X D "
					return render(request, 'student/personal_center/stu_apply_edit.html', context)
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
			pre_teach_list = teacher_model.com_teach_info.objects.filter(group_id=group_info)
			for pre_teach in pre_teach_list:
				pre_teach.delete()
			pre_group_info = competition_model.com_group_basic_info.objects.get(group_id=group_info.group_id)
			pre_group_info.delete()
			com_group = competition_model.com_group_basic_info()
			com_group.com_id = com_info
			if flag_groupname == 1:
				com_group.group_name = group_name
			com_group.group_num = len_stu
			if flag_group == 1:
				sort_list = competition_model.com_sort_info.objects.filter(com_id=com_info, sort_name=sort)
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
				stu.group_id = get_object_or_404(competition_model.com_group_basic_info, group_id=now_group_id)
				stu.stu_id = i
				if number == 1:
					stu.is_leader = 1
				number += 1
				stu.save()
			for i in teach_list:
				teach = teacher_model.com_teach_info()
				teach.com_id = com_info
				teach.group_id = get_object_or_404(competition_model.com_group_basic_info, group_id=now_group_id)
				teach.teach_id = i
				teach.save()
			return redirect('/student/personal_center_stu/?tag=2')
		# 其他状态 - 提交申请
		else:
			temp_group = competition_model.temp_com_group_basic_info()
			temp_group.temp_type = "报名信息"
			temp_group.group_id = group_info
			temp_group.com_id = com_info
			if flag_groupname == 1:
				temp_group.group_name = group_name
				temp_group.group_num = len_stu
			if flag_group == 1:
				sort_list = competition_model.com_sort_info.objects.filter(com_id=com_info, sort_name=sort)
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
				stu.temp_id = get_object_or_404(competition_model.temp_com_group_basic_info, temp_id=temp_id)
				stu.stu_id = i
				if number == 1:
					stu.is_leader = 1
				number += 1
				stu.save()

			for i in teach_list:
				teach = teacher_model.temp_com_teach_info()
				teach.temp_id = get_object_or_404(competition_model.temp_com_group_basic_info, temp_id=temp_id)
				teach.teach_id = i
				teach.save()
		return redirect('/student/personal_center_stu?tag=2')
	return render(request, 'student/personal_center/stu_apply_edit.html', context)


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
	com_info = get_object_or_404(competition_model.com_basic_info, com_id=com_id)
	group_info = get_object_or_404(competition_model.com_group_basic_info, group_id=group_id)

	stu_id_list = models.com_stu_info.objects.filter(group_id=group_info, com_id=com_info)
	stu_id_list.delete()

	teach_id_list = teacher_model.com_teach_info.objects.filter(group_id=group_info, com_id=com_info)
	teach_id_list.delete()

	com_group = competition_model.com_group_basic_info.objects.filter(group_id=int(group_id), com_id=com_info)
	com_group.delete()

	return redirect('/student/personal_center_stu/?tag=2')
