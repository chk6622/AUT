#!/usr/bin/env python
#coding: utf-8
'''
Created on Sep 2, 2018

@author: xingtong
'''
from django.db import models
from django.db.models.fields.related import ForeignKey
from django.contrib import admin
from django.forms import ModelForm
from django import forms
from django.forms.widgets import Widget
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django import forms
from django.contrib.auth.forms import *

# Create your models here.

user_role=[
               ('1',u'ProjectLeader'),
               ('2',u'GeneralStaff'),
               ('3',u'Researcher'),
               ]

def getChoice(choiceList,hasBlank=False):
    returnList=[]
    if choiceList and isinstance(choiceList,list):
        if hasBlank:
            returnList.append(('',u'-'*25))
            returnList.extend(choiceList)
        else:
            returnList.extend(choiceList)
    return returnList

class MyProfileForm(UserChangeForm):
    role=forms.ChoiceField(label=u'Role',help_text=u'',required=True,choices=getChoice(user_role,True),widget=forms.Select)

class ProfileBase(type):
    def __new__(cls,name,bases,attrs):
        module=attrs.pop('__module__')
        parents=[b for b in bases if isinstance(b,ProfileBase)]
        if parents:
            fields=[]
            for (obj_name,obj) in attrs.items():
                if isinstance(obj,models.Field):
                    fields.append(obj_name)
                User.add_to_class(obj_name,obj)
            formList=list(UserAdmin.fieldsets)
            formList.append((name,{'fields':fields}))
            UserAdmin.fieldsets=formList
            UserAdmin.form=MyProfileForm
        return super(ProfileBase,cls).__new__(cls, name,bases,attrs)

class Profile(object):
    __metaclass__=ProfileBase
    
class MyProfile(Profile):
    role=models.CharField(u'Role',choices=user_role,max_length=20,null=True,blank=True)

                    


