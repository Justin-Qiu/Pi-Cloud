#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb
import os
import os.path
import time

from Crypto.Hash import MD5

'''
用户注册函数

输入参数
    用户名，人脸token
返回值
    注册成功：1
    用户名已存在：2
'''
def register(username, token):
        
    # 连接MySQL数据库
    conn = MySQLdb.connect(
            host='localhost',
            user='admin',
            passwd='123456',
            db='pi',
            charset='utf8'
            )
    cur = conn.cursor()
    
    # 对用户名作MD5哈希
    h = MD5.new()
    h.update(b'' + username)
    username = h.hexdigest()
    
    # 检测用户名是否重复
    sql_search = "SELECT * FROM users WHERE username = '%s'" % username
    if cur.execute(sql_search) == 0L:
    
        # 插入信息到数据库完成注册
        sql = "insert into users(username, token) values('%s', '%s')" % (username, token) 
        cur.execute(sql)
        conn.commit()
        cur.close()
        conn.close()
        
        # 创建用户文件夹
        os.mkdir('files/%s' % username)
        
        return 1
    
    # 注册失败
    else:
        return 2
        
'''
用户登录函数：

输入参数
    用户名，人脸token
返回值
    登录成功：1, 文件信息列表（文件名，修改日期）
    密码错误：2, []
    用户名不存在：3, []
'''
def log_in(username, token):

    #连接MySQL数据库
    conn = MySQLdb.connect(
            host='localhost', 
            user='admin', 
            passwd='123456', 
            db='pi',
            charset='utf8'
            )
    cur = conn.cursor()
    
    # 对用户名作MD5哈希
    h = MD5.new()
    h.update(b'' + username)
    username = h.hexdigest()

    # SQL查询语句
    sql = "SELECT * FROM users WHERE username = '%s'" % username
    
    # 执行SQL语句
    cur.execute(sql)
    
    # 获取用户信息
    results = cur.fetchall()
    for row in results:
        token_db = row[2]
        if token == token_db: # 调用人脸token匹配接口
            
            # 获取用户文件信息
            files = []
            for i in os.walk('files/%s' % username):
                i[2].sort()
                for j in i[2]:
                    
                    # 获取文件名
                    file_name = j
                    
                    # 获取文件最后修改时间
                    file_time = os.stat('files/%s/%s' % (username, j)).st_mtime
                    struct_time = time.localtime(file_time)
                    if struct_time.tm_mon < 10:
                        mon = '0' + str(struct_time.tm_mon)
                    else:
                        mon = str(struct_time.tm_mon) 
                    if struct_time.tm_mday < 10:
                        mday = '0' + str(struct_time.tm_mday)
                    else:
                        mday = str(struct_time.tm_mday) 
                    if struct_time.tm_hour < 10:
                        hour = '0' + str(struct_time.tm_hour)
                    else:
                        hour = str(struct_time.tm_hour) 
                    if struct_time.tm_min < 10:
                        mins = '0' + str(struct_time.tm_min)
                    else:
                        mins = str(struct_time.tm_min)
                    if struct_time.tm_sec < 10:
                        sec = '0' + str(struct_time.tm_sec)
                    else:
                        sec = str(struct_time.tm_sec)
                    file_time = (str(struct_time.tm_year) + '-' + 
                                 mon + '-' + mday + ' ' + hour + ':' + mins + ':' + sec)
                    
                    files.append([file_name, file_time])
            
            # 返回信息
            return 1, files
        else:
        
            # 人脸匹配失败
            return 2, []
       
    # 用户不存在
    return 3, [[]]

    # 关闭数据库连接
    conn.close()
