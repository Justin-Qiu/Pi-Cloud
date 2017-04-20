#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Tkinter import *
import tkMessageBox

class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        self.homeLabel = Label(self, text='西电睿云')
        self.homeLabel.pack()
        self.usernameInput = Entry(self)
        self.usernameInput.pack()
        self.tokenInput = Entry(self)
        self.tokenInput.pack()
        self.registerButton = Button(self, text='注册', command=self.register)
        self.registerButton.pack()
        self.loginButton = Button(self, text='登录', command=self.login)
        self.loginButton.pack()

    def register(self):
        username = self.usernameInput.get()
        tkMessageBox.showinfo('消息', '注册成功, %s' % username)
        
    def login(self):
        username = self.usernameInput.get()
        tkMessageBox.showinfo('消息', '登录成功, %s' % username)
        
app = Application()

# 设置窗口标题:
app.master.title('西电睿云')

# 主消息循环:
app.mainloop()
