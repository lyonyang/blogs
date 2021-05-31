#!/usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ = "lyonyang"
# Date: 2018/5/27

from django.contrib.auth.models import User, Group
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """ 用户序列化器 """
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    """ 组序列化器 """
    class Meta:
        model = Group
        fields = ('url', 'name')