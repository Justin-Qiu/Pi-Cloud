#!/usr/bin/python
# -*- coding: utf-8 -*-
# gui.py

import sys
from PyQt4 import QtGui, QtCore
#import ui

import resource_rc

import os
import os.path
import MySQLdb
from functools import partial

from Crypto.Hash import MD5
from Crypto.Cipher import AES
from Crypto import Random

from suds.client import Client 
client = Client('http://192.168.40.129:7789/?wsdl', cache=None)

import requests
from json import JSONDecoder

key = "Vh5bg8h5xy7RHdogasG1Mb7rixDeq8yE"
secret = "dai9NgPaIcbkhzA8m9LKQngT8R0l-bN0"

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        self.setupUi(self)
        self.center()
        self.retranslateUi(self)
        
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(450, 320)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/icon/icons/cloud128.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayoutWidget = QtGui.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(100, 10, 242, 161))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.cloudIcon = QtGui.QLabel(self.verticalLayoutWidget)
        self.cloudIcon.setObjectName(_fromUtf8("cloudIcon"))
        self.verticalLayout.addWidget(self.cloudIcon)
        self.piCloud = QtGui.QLabel(self.verticalLayoutWidget)
        self.piCloud.setObjectName(_fromUtf8("piCloud"))
        self.verticalLayout.addWidget(self.piCloud)
        self.gridLayoutWidget = QtGui.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(110, 170, 221, 101))
        self.gridLayoutWidget.setObjectName(_fromUtf8("gridLayoutWidget"))
        self.gridLayout = QtGui.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.regButton = QtGui.QPushButton(self.gridLayoutWidget)
        self.regButton.setObjectName(_fromUtf8("regButton"))
        self.gridLayout.addWidget(self.regButton, 2, 2, 1, 1)
        self.logButton = QtGui.QPushButton(self.gridLayoutWidget)
        self.logButton.setObjectName(_fromUtf8("logButton"))
        self.gridLayout.addWidget(self.logButton, 2, 1, 1, 1)
        self.usernameEdit = QtGui.QLineEdit(self.gridLayoutWidget)
        self.usernameEdit.setObjectName(_fromUtf8("usernameEdit"))
        self.gridLayout.addWidget(self.usernameEdit, 1, 1, 1, 2)
        self.username = QtGui.QLabel(self.gridLayoutWidget)
        self.username.setObjectName(_fromUtf8("username"))
        self.gridLayout.addWidget(self.username, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 450, 31))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.logButton, QtCore.SIGNAL(_fromUtf8("clicked()")), self.log)
        QtCore.QObject.connect(self.regButton, QtCore.SIGNAL(_fromUtf8("clicked()")), self.reg)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
    def reg(self): 
        user = self.usernameEdit.text()
        # 对用户名作MD5哈希
        h = MD5.new()
        h.update(b'' + user)
        user = h.hexdigest()
        result = client.service.search(user)
        if result == 1:
            http_url = "https://api-cn.faceplusplus.com/facepp/v3/detect"
            filepath = "image/temp.jpg"
            data = {"api_key": key, "api_secret": secret}
            files = {"image_file": open(filepath, "rb")}
            response = requests.post(http_url, data = data, files = files)
            req_con = response.content.decode('utf-8')
            req_dict = JSONDecoder().decode(req_con)
            facetoken = req_dict["faces"][0]["face_token"]
            result = client.service.reg(user, facetoken)
            if result == 1:
                QtGui.QMessageBox.information(self, u"消息", u"注册成功！")
            elif result == 2:
                QtGui.QMessageBox.information(self, u"消息", u"用户名已存在！")
        elif result == 2:
            QtGui.QMessageBox.information(self, u"消息", u"用户名已存在！")
            
    def log(self): 
        user = self.usernameEdit.text()
        # 对用户名作MD5哈希
        h = MD5.new()
        h.update(b'' + user)
        user = h.hexdigest()
        result = client.service.search(user)
        if result == 2:
            http_url = "https://api-cn.faceplusplus.com/facepp/v3/detect"
            filepath = "image/temp.jpg"
            data = {"api_key": key, "api_secret": secret}
            files = {"image_file": open(filepath, "rb")}
            response = requests.post(http_url, data = data, files = files)
            req_con = response.content.decode('utf-8')
            req_dict = JSONDecoder().decode(req_con)
            facetoken = req_dict["faces"][0]["face_token"]
            result = client.service.log(user, facetoken)
            if result == 1:
                #QtGui.QMessageBox.information(self, u"消息", u"认证成功！")
                self.fileTable = Ui_Form()
                self.fileTable.show()
                self.hide()
            elif result == 2:
                QtGui.QMessageBox.information(self, u"消息", u"认证失败！")
            elif result == 3:
                QtGui.QMessageBox.information(self, u"消息", u"用户名不存在！")
        elif result == 1:
            QtGui.QMessageBox.information(self, u"消息", u"用户名不存在！")
            
    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "派云", None))
        self.cloudIcon.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><img src=\":/icon/icons/cloud128.png\"/></p></body></html>", None))
        self.piCloud.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:20pt; font-weight:600;\">树莓派安全云存储</span></p></body></html>", None))
        self.regButton.setText(_translate("MainWindow", "注册", None))
        self.logButton.setText(_translate("MainWindow", "人脸认证", None))
        self.username.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:12pt;\">用户名：</span></p></body></html>", None))
        
    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, u'消息', u"是否确认退出？", QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
            
    def center(self):
        screen = QtGui.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)

class Ui_Form(QtGui.QWidget):
    def __init__(self):
        super(Ui_Form, self).__init__()
        self.setupUi(self)
        self.center()
        self.retranslateUi(self)
        
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(450, 320)
        self.username = QtGui.QLabel(Form)
        self.username.setGeometry(QtCore.QRect(20, 10, 211, 21))
        self.username.setObjectName(_fromUtf8("username"))
        self.tableWidget = QtGui.QTableWidget(Form)
        self.tableWidget.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers) 
        self.tableWidget.setGeometry(QtCore.QRect(10, 40, 431, 261))
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setColumnWidth(0,160)
        self.tableWidget.setColumnWidth(1,150)
        self.tableWidget.setColumnWidth(2,50)
        self.tableWidget.setColumnWidth(3,50)
        
        self.user = main.usernameEdit.text()
        # 对用户名作MD5哈希
        h = MD5.new()
        h.update(b'' + self.user)
        self.user = h.hexdigest()
        
        result = client.service.files(self.user)
        file_num = 0
        if result != '':
            file_num = len(result[0])
        
        self.tableWidget.setRowCount(file_num)
        
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        
        dict = locals()
        
        #self.key = b'Sixteen byte key'
        #self.iv = Random.new().read(AES.block_size)
        
        # 连接MySQL数据库
        conn = MySQLdb.connect(
                host='localhost',
                user='admin',
                passwd='123456',
                db='client',
                charset='utf8'
                )
        cur = conn.cursor()
        
        filename = []
        
        for i in range(file_num):           
            # 检测文件名是否重复
            sql_search = "SELECT * FROM files WHERE hash = '%s'" % result[0][i][0][0]
            cur.execute(sql_search)
            results = cur.fetchall()
            for row in results:
                filename.append(row[1])

            newItem = QtGui.QTableWidgetItem(u"%s" % filename[i])  
            self.tableWidget.setItem(i, 0, newItem)  
            newItem = QtGui.QTableWidgetItem(u"%s" % result[0][i][0][1])  
            self.tableWidget.setItem(i, 1, newItem) 
            
            #self.downButton = QtGui.QPushButton(Form)
            dict['self.downButton%s' % i] = QtGui.QPushButton(Form)
            self.tableWidget.setCellWidget(i, 2, dict['self.downButton%s' % i]) 
            dict['self.downButton%s' % i].setText(u"下载")
            
            #self.delButton = QtGui.QPushButton(Form)
            dict['self.delButton%s' % i] = QtGui.QPushButton(Form)
            self.tableWidget.setCellWidget(i, 3, dict['self.delButton%s' % i])
            dict['self.delButton%s' % i].setText(u"删除")
        
        cur.close()
        conn.close()
        
        for i in range(file_num):
            QtCore.QObject.connect(dict['self.downButton%s' % i], QtCore.SIGNAL(_fromUtf8("clicked()")), partial(self.download, filename[i]))
            QtCore.QObject.connect(dict['self.delButton%s' % i], QtCore.SIGNAL(_fromUtf8("clicked()")), partial(self.delete, filename[i]))

        self.quitButton = QtGui.QPushButton(Form)
        self.quitButton.setGeometry(QtCore.QRect(360, 6, 80, 30))
        self.quitButton.setObjectName(_fromUtf8("quitButton"))
        self.uploadButton = QtGui.QPushButton(Form)
        self.uploadButton.setGeometry(QtCore.QRect(280, 6, 80, 30))
        self.uploadButton.setObjectName(_fromUtf8("uploadButton"))
        self.keyButton = QtGui.QPushButton(Form)
        self.keyButton.setGeometry(QtCore.QRect(200, 6, 80, 30))
        self.keyButton.setObjectName(_fromUtf8("keyButton"))

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        
        QtCore.QObject.connect(self.quitButton, QtCore.SIGNAL(_fromUtf8("clicked()")), self.quit)
        
        QtCore.QObject.connect(self.uploadButton, QtCore.SIGNAL(_fromUtf8("clicked()")), self.upload)
        
        QtCore.QObject.connect(self.keyButton, QtCore.SIGNAL(_fromUtf8("clicked()")), self.keygen)
    
    def keygen(self):
        if os.path.exists('keys/%s.key' % self.user): 
            QtGui.QMessageBox.information(self, u"消息", u"您已经生成过密钥！")
        else: 
            #self.key = b'Sixteen byte key'
            self.key = Random.new().read(AES.block_size)
            with open('keys/%s.key' % self.user, 'w') as f:
                f.write('%s' % self.key)
            QtGui.QMessageBox.information(self, u"消息", u"您的AES密钥是：%s" % self.key.encode('hex'))
    
    def delete(self, filename):   
        
        filename = filename.encode('utf-8')
        # 对文件名作MD5哈希
        h = MD5.new()
        h.update(b'' + filename)
        file_hash = h.hexdigest()
        client.service.delete(self.user, file_hash)
        QtGui.QMessageBox.information(self, u"消息", u"删除成功！")
        self.fileTable = Ui_Form()
        self.fileTable.show()
        self.hide()
    
    def download(self, filename):
        file_path = QtGui.QFileDialog.getSaveFileName(self, u"保存文件", filename)    
        file_path = unicode(file_path.toUtf8(), 'utf-8', 'ignore')
        with open('keys/%s.key' % self.user, 'r') as f:
            self.key = f.read()
        if file_path != u'':
            filename = filename.encode('utf-8')
            # 对文件名作MD5哈希
            h = MD5.new()
            h.update(b'' + filename)
            file_hash = h.hexdigest()
        
            result = client.service.download(self.user, file_hash)
        
            if result[0][0] == '1':
                msg = result[0][1]
                msg = msg.decode('hex')
                cipher = AES.new(self.key, AES.MODE_CFB, msg[:16])
                msg = cipher.decrypt(msg[16:])
                with open(file_path, 'w') as f:
                    f.write('%s' % msg) 
                QtGui.QMessageBox.information(self, u"消息", u"下载成功！")

            elif result[0][0] == '2':
                QtGui.QMessageBox.information(self, u"消息", u"下载失败！")
        
    def upload(self):
        if os.path.exists('keys/%s.key' % self.user): 
            with open('keys/%s.key' % self.user, 'r') as f:
                self.key = f.read()   
            self.iv = Random.new().read(AES.block_size) 
            file_name = QtGui.QFileDialog.getOpenFileName(self, u"选择文件")
            file_name = unicode(file_name.toUtf8(), 'utf-8', 'ignore') 
            
            if file_name != u'':
                with open(file_name, 'r') as f:
                    txt = f.read()
                file_name = os.path.split(file_name)[-1]
                file_name = file_name.encode('utf-8')
            
                # 对文件名作MD5哈希
                h = MD5.new()
                h.update(b'' + file_name)
                file_hash = h.hexdigest()
            
                # 连接MySQL数据库
                conn = MySQLdb.connect(
                        host='localhost',
                        user='admin',
                        passwd='123456',
                        db='client',
                        charset='utf8'
                        )
                cur = conn.cursor()
                # 检测文件名是否重复
                sql_search = "SELECT * FROM files WHERE filename = '%s'" % file_name
                if cur.execute(sql_search) == 0L:
        
                    # 插入文件信息到数据库
                    sql = "insert into files(filename, hash) values('%s', '%s')" % (file_name, file_hash) 
                    cur.execute(sql)
                    conn.commit()
                    cur.close()
                    conn.close()
            
                cipher = AES.new(self.key, AES.MODE_CFB, self.iv)
                msg = self.iv + cipher.encrypt(b'' + txt)
                msg = msg.encode('hex')
            
                #txt = txt.decode('utf-8')
                result = client.service.upload(self.user, file_hash, msg)
            
                if result == 1:
                    QtGui.QMessageBox.information(self, u"消息", u"上传成功！")
                    self.fileTable = Ui_Form()
                    self.fileTable.show()
                    self.hide()
                elif result == -1:
                    QtGui.QMessageBox.information(self, u"消息", u"文件名已存在！")
        else:
            QtGui.QMessageBox.information(self, u"消息", u"你还未生成密钥！")
        
    def quit(self):
        self.main = Ui_MainWindow()
        self.main.show()
        self.hide()
        
    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "文件", None))
        self.username.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:12pt;\">用户名：%s</span></p></body></html>" % str(main.usernameEdit.text()), None))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Form", "文件名", None))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Form", "上传时间", None))
        #item = self.tableWidget.horizontalHeaderItem(2)
        #item.setText(_translate("Form", "操作", None))
        self.quitButton.setText(_translate("Form", "退出登录", None))
        self.uploadButton.setText(_translate("Form", "上传文件", None))
        self.keyButton.setText(_translate("Form", "生成密钥", None))    
        
    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, u'消息', u"是否确认退出？", QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()   
                   
    def center(self):
        screen = QtGui.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)

app = QtGui.QApplication(sys.argv)

#main = ui.Ui_MainWindow()
main = Ui_MainWindow()
main.show()

sys.exit(app.exec_())
