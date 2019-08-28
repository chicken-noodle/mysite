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
import student.models as student_model


# Create your views here.
# 教师修改个人信息
def alter_info_teach(request):
	context = {}
	nid = request.session.get('user_number', None)
	teach_info = get_object_or_404(models.teach_basic_info, tea_number=nid)
	profess_info = models.profess_info.objects.all()
	depart_info = all_model.depart_info.objects.all()
	major_info = all_model.major_info.objects.all()

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
			return render(request, 'teacher/alter_info_teach.html', context)

		if phone_number == 'None' or phone_number == "":
			context['message'] = "请务必填写手机号码！"
			return render(request, 'teacher/alter_info_teach.html', context)

		if email == 'None' or email == "":
			context['message'] = "请务必填写邮箱！"
			return render(request, 'teacher/alter_info_teach.html', context)

		photo = request.FILES.get("photo")
		# print(photo)

		tea_info = models.teach_basic_info.objects.get(tea_number=nid)
		# tea_info.tea_number = tea_number
		# tea_info.tea_name = tea_name
		tea_info.profess = get_object_or_404(models.profess_info, profess_name=profess)
		tea_info.department = get_object_or_404(all_model.depart_info, depart_name=department)
		tea_info.major = get_object_or_404(all_model.major_info, major_name=major)
		tea_info.ID_number = ID_number
		tea_info.phone_number = phone_number
		tea_info.email = email

		if photo != None:
			f_name = photo.name
			f_name = f_name.split('.')[-1].lower()
			# 重命名
			tea_info.photo = "teach_photo\\" + nid + "\\" + 'head' + '.' + f_name
			url = settings.MEDIA_ROOT + 'teach_photo\\' + nid
			# 判断路径是否存在
			isExists = os.path.exists(url)
			if not isExists:
				os.makedirs(url)
			photo_url = open(
				settings.MEDIA_ROOT + "teach_photo\\" + nid + "\\" + 'head' + '.' + f_name, 'wb')
			for chunk in photo.chunks():
				photo_url.write(chunk)
			photo_url.close()

		tea_info.save()
		# 更改修改状态
		user_login = get_object_or_404(all_model.user_login_info, account=request.session['user_number'])
		user_login.have_login = '1'
		user_login.have_alter = '1'
		user_login.save()

		return redirect('/home/')

	return render(request, 'teacher/alter_info_teach.html', context)


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
		com = get_object_or_404(competition_model.com_basic_info, com_id=teach.com_id.com_id)
		temp_group_list = competition_model.com_group_basic_info.objects.filter(group_id=teach.group_id.group_id,
		                                                                        com_id=teach.com_id)
		for group in temp_group_list:
			group_list.append(group)
		temp_stu_list = student_model.com_stu_info.objects.filter(group_id=teach.group_id, com_id=teach.com_id)
		temp_list = []
		for stu in temp_stu_list:
			stu_info = get_object_or_404(student_model.stu_basic_info, stu_number=stu.stu_id.stu_number)
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
	return render(request, 'teacher/personal_center/index.html', context)


# 教师个人中心-驳回报名
def reject_apply(request):
	context = {}

	com_id = request.GET.get('p1')
	group_id = request.GET.get('p2')
	com_info = get_object_or_404(competition_model.com_basic_info, com_id=com_id)
	group_info = get_object_or_404(competition_model.com_group_basic_info, group_id=group_id)

	stu_id_list = student_model.com_stu_info.objects.filter(group_id=group_info, com_id=com_info)
	stu_id_list.delete()

	teach_id_list = models.com_teach_info.objects.filter(group_id=group_info, com_id=com_info)
	teach_id_list.delete()

	com_group = competition_model.com_group_basic_info.objects.filter(group_id=int(group_id), com_id=com_info)
	com_group.delete()

	return redirect('/teacher/personal_center_teach/')


# 教师个人中心-竞赛详情
def teach_apply_deatil(request):
	context = {}
	com_id = request.GET.get('p1')
	group_id = request.GET.get('p2')
	# 获取竞赛报名所需信息
	info_list = get_object_or_404(competition_model.com_need_info, com_id=com_id)
	# 获取竞赛id和小组id，通过这两个id确定具体比赛具体小组
	com_info = get_object_or_404(competition_model.com_basic_info, com_id=com_id)
	group_info = get_object_or_404(competition_model.com_group_basic_info, group_id=group_id)

	stu_list = []
	stu_id_list = student_model.com_stu_info.objects.filter(group_id=group_info, com_id=com_info)
	for stu_info in stu_id_list:
		temp = get_object_or_404(student_model.stu_basic_info, stu_number=stu_info.stu_id.stu_number)
		stu_list.append((temp))

	teach_list = []
	teach_id_list = models.com_teach_info.objects.filter(group_id=group_info, com_id=com_info)
	for teach_info in teach_id_list:
		temp = get_object_or_404(models.teach_basic_info, tea_number=teach_info.teach_id.tea_number)
		teach_list.append(temp)

	com_group = competition_model.com_group_basic_info.objects.filter(group_id=int(group_id), com_id=com_info)
	for competition in com_group:
		com_group_info = competition

	context['stu_list'] = stu_list
	context['info_list'] = info_list
	context['teach_list'] = teach_list
	context['com_group_info'] = com_group_info
	return render(request, "teacher/personal_center/apply_detail.html", context)
