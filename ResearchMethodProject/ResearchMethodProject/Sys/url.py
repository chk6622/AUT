#!/usr/bin/env python
#coding: utf-8
'''
Created on Sep 2, 2018

@author: xingtong
'''
import sys
from django.conf.urls import include, url
from SysView import index
from django.contrib import admin
from django.contrib.auth.views import *
from SysView import changePasswordDone


urlpatterns = [
#     url(r'^login/', mylogin), 
#     url(r'^logout/', mylogout), 
#     url(r'^login/',login,{'template_name':'index.html'}),
#     url(r'^logout/',logout),
#     url(r'^$', login,{'template_name':'index.html'}), 
    url(r'^passwordChange/$', password_change, {'template_name':'sys/passwordChange.html',
                                                'post_change_redirect':'/Sys/passwordChangeDone/'}), #修改密码，template_name:修改密码的模板,post_change_redirect:修改成功后跳转的路径
    url(r'^passwordChangeDone/$', changePasswordDone),
    
    url(r'^password_reset/$', password_reset, name='password_reset'),
    url(r'^password_reset/done/$', password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', password_reset_complete, name='password_reset_complete'),

]