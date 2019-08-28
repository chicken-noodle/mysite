from django.shortcuts import render_to_response, get_object_or_404, redirect, render
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, Http404, FileResponse
from django.conf import settings
import datetime
from . import models
import os


# Create your views here.
def home(request):
	context = {}
	return render(request, 'home/home.html', context)


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
			return render(request, 'home/login.html', context)
		if t_psword == "":
			context['message'] = "？？？倒是输密码啊"
			return render(request, 'home/login.html', context)
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
						return redirect('/student/alter_info_stu')
					# 指导老师
					if user.have_alter == '0' and user.jurisdiction == '2':
						return redirect('/teacher/alter_info_teach')
					if user.have_alter == '0' and user.jurisdiction == '3':
						return redirect('/teacher/alter_info_teach')
					return redirect('/home')
				else:
					context['message'] = "???连密码都输不对吗？？？"
					return render(request, 'home/login.html', context)
			except:
				context['message'] = "账号不存在！"
				return render(request, 'home/login.html', context)
		return render(request, 'home/home.html', context)
	return render(request, 'home/login.html', context)


# 注销
def logout(request):
	if not request.session.get('is_login', None):
		return redirect("/home/")
	request.session.flush()
	return redirect("/home/")
