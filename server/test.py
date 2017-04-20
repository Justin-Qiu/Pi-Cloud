#!/usr/bin/env python
# -*- coding: utf-8 -*-

from functions import register, log_in

choice = raw_input('请选择您要进行的操作（注册[r]/登录[L]）：')

if choice == 'r':
    username = raw_input('用户名：')
    token = raw_input('人脸信息：')
    result = register(username, token)
    if result == 1:
        print '注册成功！'
    elif result == 2:
        print '用户名被占用！'
else:
    username = raw_input('用户名：')
    token = raw_input('人脸信息：')
    result = log_in(username, token)
    if result[0] == 1:
        print '登录成功！'
        files_info = result[1]
        for i in range(len(files_info)):
            for j in range(2):
                print files_info[i][j],
            print ''
    elif result[0] == 2:
        print '人脸匹配失败！'
    elif result[0] == 3:
        print '用户不存在！'
