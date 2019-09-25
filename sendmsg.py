##import sys
##from sys import path
##path.append(r'D:\weiabc123')  # 添加路径
import weiabc123

import pyperclip#剪切板操作
import xlrd#excel读取
import time#时间模块
import ctypes  #弹出框
import win32api
import win32con
import win32gui
import setingwei
import pyautogui
import re,os
import videotape
from PIL import ImageGrab

class qianniu:
    def zhidingfasong(func):    
        def _deco(self,*arg):
            win32gui.SetWindowPos(self.hwnd0,-1, 0, 0, 0, 0,3)#置顶窗口
            func(self,*arg)
            win32gui.SetWindowPos(self.hwnd0,-2, 0, 0, 0, 0,3)#取消置顶
        return _deco

    def __init__(self):
        '''实例热键、线程类，并通过线程启动热键'''
        self.a021=weiabc123.weiHotkey()
        self.xian4cheng21=weiabc123.weiThreading()
        self.xian4cheng21.t_start(self.a021.h_start,1,118)

    def find_jb(self):#7.0版本
        '''获取需要的句柄'''
        self.wwsskjb=self.juBingChuangKou.hw_childrenHandle(self.juBingChuangKou.hw_childrenHandle(self.hwnd)[5])[0]#旺旺搜索框
        self.wwsskscjb=self.juBingChuangKou.hw_childrenHandle(self.juBingChuangKou.hw_childrenHandle(self.hwnd)[5])[2]#旺搜索框关闭（右）
        #self.djss=self.juBingChuangKou.hw_childrenHandle(self.hwnd)[2]#点击搜索
        guodu=win32gui.FindWindowEx(self.juBingChuangKou.hw_childrenHandle(self.hwnd)[3], None, 'SplitterBar',None)
        self.xxsrkjb=win32gui.FindWindowEx(self.juBingChuangKou.hw_childrenHandle(guodu)[1], None, 'RichEditComponent',None)
        self.fsjb=win32gui.FindWindowEx(self.juBingChuangKou.hw_childrenHandle(guodu)[1], None, 'StandardButton','发送')
        self.gbjb=win32gui.FindWindowEx(self.juBingChuangKou.hw_childrenHandle(guodu)[1], None, 'StandardButton','关闭')
        self.liaoTianChuangKou=self.juBingChuangKou.hw_childrenHandle(guodu)[0]

    def duqupeiz(self):#读取配置
        self.sffswcgb=eval(weiabc123.weiConfig(r'.\cof\peizhi').c_read('config','是否发送完成关闭'))
        self.jzcffs=eval(weiabc123.weiConfig(r'.\cof\peizhi').c_read('config','禁止重复发送'))
        self.huinr01=weiabc123.weiConfig(r'.\cof\peizhi').c_read('config','发送内容')
        self.fssd01=float(weiabc123.weiConfig(r'.\cof\peizhi').c_read('config','发送速度'))
        self.qianniuzhanghao=weiabc123.weiConfig(r'.\cof\peizhi').c_read('config','发送帐号')
        self.zhiding=eval(weiabc123.weiConfig(r'.\cof\peizhi').c_read('config','发送时窗口是否置顶'))



    @zhidingfasong
    def fasong(self):
        '''发送一条'''
        self.juBingChuangKou.hw_current(self.hwnd)
        for i in range(10):
            self.juBingChuangKou.hw_click_Handle(self.wwsskjb,clicks=2)
            if win32gui.GetWindowLong(self.wwsskscjb,win32con.GWL_STYLE)==1342242816:break
        win32gui.SendMessage(self.wwsskjb, win32con.WM_SETTEXT, None,self.dangQianWangWang)
        win32gui.PostMessage(self.wwsskjb, 256, 13,None)
        win32gui.PostMessage(self.wwsskjb, 257, 13,None)
        dksb=False
        for i in range(16):#判定旺旺是否打开成功
            time.sleep(0.1/1.3*self.fssd01)
            win32gui.PostMessage(self.wwsskjb, 256, 13,None)
            win32gui.PostMessage(self.wwsskjb, 257, 13,None)
            if win32gui.GetWindowLong(self.wwsskscjb,win32con.GWL_STYLE)==1073807360:break
            elif i==15:dksb=True
        if dksb:
            shibai='%s			旺旺名错误、其他干扰、网络延时、发送过程中人为操作鼠标键盘等，导致打开失败'%(self.dangQianWangWang)
            weiabc123.weiLog('发送失败日志.txt').l_write(shibai)
            print(shibai)
            return
        time.sleep(0.32/1.3*self.fssd01)##时间 打开之后
        quxiao1=win32gui.FindWindow(None,'千牛')
        if quxiao1:
            win32gui.PostMessage(quxiao1, win32con.WM_CLOSE, 0, 0)#关闭句柄
            shibai='%s			    拒绝接收陌生人消息'%(self.dangQianWangWang)
            weiabc123.weiLog('发送日志.txt').l_write(shibai)
            return
        quxiao=win32gui.FindWindow(None,'添加好友')
        if quxiao:
            win32gui.PostMessage(quxiao, win32con.WM_CLOSE, 0, 0)#关闭句柄
            shibai='%s			需添加好'%(self.dangQianWangWang)
            weiabc123.weiLog('发送日志.txt').l_write(shibai)
            return
        
        pyperclip.copy('')
        self.juBingChuangKou.hw_click_Handle(jb=self.liaoTianChuangKou,wz=1,py_x=1,py_y=5)
        time.sleep(0.08/1.3*self.fssd01)##时间 复制之后
        weiabc123.weiShortcutKeys(17,65,67)
        jianqie1=pyperclip.paste()
        print(len(jianqie1),self.dangQianWangWang)
        
        hang001=self.wwid1.index(self.dangQianWangWang)
        hang001lie1=str(self.biaoge.cell(hang001,1).value)#获取hang001行1列的值
        if not hang001lie1:hang001lie1=str(self.biaoge.cell(1,1).value)
        self.huinr01=self.huinr01.replace('｛动态值｝',hang001lie1)
        h1=''.join(re.findall('[\u2E80-\u9FFF]',self.huinr01))
        jq1=''.join(re.findall('[\u2E80-\u9FFF]',jianqie1))
        if h1 in jq1 and self.jzcffs:
            shibai='%s			网络延时未加载、已经发送过类似消息或者旺旺不存在'%(self.dangQianWangWang)
            weiabc123.weiLog('发送日志.txt').w_write(shibai)
            return

        win32gui.SendMessage(self.xxsrkjb, win32con.WM_SETTEXT, None,self.huinr01)
        time.sleep(0.02/1.3*self.fssd01)

        win32gui.PostMessage(self.fsjb, 256, 13,None)
        win32gui.PostMessage(self.fsjb, 257, 13,None)
        if self.sffswcgb:
            win32gui.PostMessage(self.gbjb, 256, 13,None)
            win32gui.PostMessage(self.gbjb, 257, 13,None)
        shibai='%s			    发送成功'%(self.dangQianWangWang)
        weiabc123.weiLog('发送日志.txt').l_write(shibai)


    def Control(self):#操控方法
        '''验证，和执行发送循环'''
        benggongsi=setingwei.sendmsg['benggongsi']
        benggongsi=[i for i in benggongsi if i in self.qianniuzhanghao]
        if benggongsi:
            if time.time()>1596938898:
                win32api.MessageBox(0, 'bgs应用已更新，或者配置错误，详情联系开发者QQ：1043014552',u'提示框',win32con.MB_SYSTEMMODAL)
                return 1
        else:
            yanZheng009=weiabc123.weiVerification(self.qianniuzhanghao).v_account_verification()
            if not yanZheng009 : return 1
        titlename =self.qianniuzhanghao+' - 接待中心'
        try:self.biaoge=xlrd.open_workbook(r'旺旺名.xls').sheets()[0]#接收消息的旺旺表
        except:
            win32api.MessageBox(0, '检查 旺旺名.xls 是否存在或异常！！',u'提示框',win32con.MB_SYSTEMMODAL)
            return 1
        self.hwnd0=win32gui.FindWindow("StandardFrame",titlename)
        self.hwnd=weiabc123.weiHandleWindow().hw_childrenHandle(self.hwnd0)[0]#发送旺旺窗口句柄
        print(self.hwnd,win32gui.GetWindowText(self.hwnd),104)
        self.wwid1=self.biaoge.col_values(0)#表格读取的接收消息旺旺号
        self.wwid=list(set(self.wwid1))
        self.wwid.sort(key=self.wwid1.index)
        del self.wwid[0]
        readrizhi=weiabc123.weiBigFileRead().bfr_read('发送日志.txt')
        if readrizhi:
            fsdww=re.findall('(.*?)\t\t\t',readrizhi)[-1]#发送到的旺旺
            if fsdww in self.wwid:
                bb001=ctypes.windll.user32.MessageBoxW(0, '部分接收消息的旺旺今天已经发送过消息\，是否接着上次发送到的旺旺号开始发送？\
                    \n继续上次发送按确定，从第一个旺旺开始按发送按取消。','提示',1)
                if bb001==1:self.wwid=self.wwid[self.wwid.index(fsdww)+1:]

        self.wwid=iter(self.wwid)

        if not win32gui.IsWindowVisible(self.hwnd):
            win32api.MessageBox(0, '千牛聊天窗口未打开，请打开千牛聊天窗口再执行发送！！',u'提示框',win32con.MB_SYSTEMMODAL)
            return 1
        self.juBingChuangKou=weiabc123.weiHandleWindow()#实例句柄处理
        self.juBingChuangKou.hw_current(self.hwnd)#

    def main(self):
        self.duqupeiz()##########读取配置，获取千牛帐号
        if self.Control():##########
            print('Control函数内部跳出条件跳出')
            return
        try:self.find_jb()##########取需要的句柄
        except:
            win32api.MessageBox(0, '应用已更新，或者配置错误，详情请联系开发者QQ：1043014552',u'提示框',win32con.MB_SYSTEMMODAL)
            weiabc123.weiLog(r'.\cof\error_log').l_error()
            return
        #t012=time.time()#启动开始时间
        while True:
            if self.a021.panDuan:
                pass
            else:
                self.dangQianWangWang=next(self.wwid,'')
                if not self.dangQianWangWang:
                    print('发送完成')
                    break
                try:
                    self.duqupeiz()##########读取配置，保证配置内容为最新
                    self.fasong()##########
                except:
                    weiabc123.weiLog(r'.\cof\error_log').l_error()
                    break
        #win32api.MessageBox(0,'发送完成，总耗时%s'%(time.time()-t012), u'提示框',win32con.MB_SYSTEMMODAL)


if __name__=="__main__":
    ee11=qianniu()
    ee11.main()
    pass







