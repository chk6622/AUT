#!/usr/bin/env python
#coding: utf-8
'''
Created on Sep 2, 2018

@author: xingtong
'''
import sys
from django.shortcuts import render_to_response
from Common.ViewTools import *
from Common.UploadFileTools import *
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext
from models import *
import ResearchMethodProject.ResearchMethodProject.settings as settings
import time
from django.contrib.auth.models import User
from django.contrib import auth
from django.http.response import HttpResponseRedirect
from django.contrib import messages



def index(request):
    return render_to_response('index.html',locals(),context_instance=RequestContext(request))

def loginSuccess(request):
    return render_to_response('main.html',locals(),context_instance=RequestContext(request))

def changePasswordDone(request):
    messages.info(request,'Reset password success！')
    form = PasswordChangeForm(user=request.user)
    return render_to_response('sys/passwordChange.html',locals(),context_instance=RequestContext(request))
# 
# 
# def mylogin(request):
#     templateDir='index.html'
#     messages=[]
#     if request.method == 'POST':
#         username=request.POST.get('username',None)
#         password=request.POST.get('password',None)
#         if not username:
#             messages.append('请输入用户名')
#         elif not password:
#             messages.append('请输入密码')
#         else:
#             user=auth.authenticate(username=username,password=password)
#             if user:
#                 if user.is_active:
#                     auth.login(request,user)
#                     print request.user.cid
#                     templateDir='welcome.html'
#                 else:
#                     messages.append('该用户已失效!')
#             else:
#                 messages.append('用户名或密码错误！')
#     return render_to_response(templateDir,locals(),context_instance=RequestContext(request))
# 
# def mylogout(request):
#     auth.logout(request)
#     return HttpResponseRedirect('/')












