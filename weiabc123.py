import ctypes.wintypes
import win32con
import time#时间模块
import threading #线程
import traceback#用于错误处理
import requests
import re
import base64
import win32api
import win32con
import win32gui
import win32com.client
import webbrowser#打开默认浏览器
import pyautogui

#--------------------------------------------------------------------------------------------------------------------------------
class weiHotkey:# 自定义全局快捷键arg为数组或者列表[key1,key2]
    def h_start(self,*arg):
        '''win32con.MOD_ALT[Alt键1];win32con.MOD_SHIFT[Shift键4];win32con.MOD_CONTROL[Ctrl键2];0x76[16进制F7键118]'''
        self.panDuan=0#用于终止指定热键，设置为热键值之后再按热键停止
        hotkey_id=5201203
        arg=arg
        user32 = ctypes.windll.user32  # 加载user32.dll
        user32.UnregisterHotKey(None,hotkey_id)
        if user32.RegisterHotKey(None,hotkey_id,*arg):# 注册快捷键*arg 并判断是否成功
            print('热键ID%s注册成功，热键为%s'%(hotkey_id,[str(i) for i in arg]))
        else:
            print('热键ID%s被占用无法注册'% hotkey_id)# 返回一个错误信息Unable to register id
        msg = ctypes.wintypes.MSG()
        while True:# 以下为检测热键是否被按下
            if user32.GetMessageA(ctypes.byref(msg), None, 0, 0) != 0 and msg.message == win32con.WM_HOTKEY:
                if msg.wParam==hotkey_id:
                    if self.panDuan=='out':
                        user32.UnregisterHotKey(None,hotkey_id)
                        print('热键%s已释放'% hotkey_id)
                        break
                    else:
                        print('热键%s被触发'% hotkey_id)
                        if self.panDuan:self.panDuan=0
                        else:self.panDuan=1
#--------------------------------------------------------------------------------------------------------------------------------
class weiThreading:
    def t_start(self,fun,*args):
        '''传入函数名和参数，启动函数线程'''
        try:
            self.t1 = threading.Thread(target=lambda:fun(*args))
            self.t1.start()
        except:
            print('出错了,详情查看日志')
            weiLog().l_error('error_log')
    def t_close(self):
        '''终止线程'''
        xcid=self.t1.ident#线程id[线程标识符]
        ctypes.c_long(xcid)#tid对应的C中的类型，返回c_long(xcid)
        #pythonapi是一个预定义的符号用来访问python C api.
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(xcid, ctypes.py_object(SystemExit))#结束线程
        if res == 0:
            print('无效线程')
            #raise ValueError('无效的线程')#抛出类型为ValueError的异常，异常内容为invalid thread id(无效的线程)
        elif res != 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(xcid, None)
            raise SystemError('Py线程状态设置异步Exc失败了')#Py线程状态设置异步Exc失败了,PyThreadState_SetAsyncExc failed
#--------------------------------------------------------------------------------------------------------------------------------
class weiLog:
    def __init__(self,fn):
        '''传入文件名，初始化文件名和当前时间'''
        self.otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        self.fn=fn
    def l_error(self):
        '''错误内容写入文件'''
        with open(self.fn,'a') as f:
            traceback.print_exc(file=f)
            f.write('**************'+self.otherStyleTime+'*************\n\n')
    def l_write(self,nr):
        '''传入写入内容，写入内容到文件'''
        with open(self.fn,'a',encoding='UTF-8') as f:f.write(nr+'\n')
    def l_read(self):
        '''读取文件内容'''
        try:
            with open(self.fn,'r') as f:return f.readlines()
        except:pass#win32api.MessageBox(0,u'文件【%s】不存在'% self.fn, u'提醒',win32con.MB_OK)
#--------------------------------------------------------------------------------------------------------------------------------
class weiEncryptDecrypt:#字符加密和解密 Encrypt
    def ed_encrypt(self,character):
        '''传入字符串，进行加密并返回'''
        '''先转为bytes，对转为bytes的字符串进行base64加密，然后在更改一位数字符'''
        character=character.encode()
        character=base64.b64encode(character)
        character=str(character)[2:-1]
        character=character.replace('=','#')
        character=list(character)
        character.insert(2,'D')
        character=''.join(character)
        return character        
    def ed_decrypt(self,character):
        '''传入加密字符串，进行解密密并返回,函数ed_encrypt反向操作'''
        #print(character)
        character=character[:2]+character[3:]
        character="b'%s'"%(character)
        character=character.replace('#','=')
        character=eval(character)
        character=base64.b64decode(character)
        character=character.decode()
        return character
#--------------------------------------------------------------------------------------------------------------------------------
class weiVerification:#验证
    def __init__(self,qianniuzhanghao=''):
        '''用于判断,因为__init__函数只能返回None,所以不能直接使用__init__函数'''
        csh=weiConfig(r'.\cof\peizhi').c_read('config','初始化')#获取初始化加密字符串
        url=weiEncryptDecrypt().ed_decrypt(csh)#解密初始化字符串
        self.req=requests.get(url).text
        self.req1=re.findall('```1(.*?)1```',self.req)[0]
        self.req1=self.req1.split(',')
        while '' in self.req1:
            self.req1.remove('')
        qianniuzhanghao=qianniuzhanghao.split(':')[0]#执行此句，全店版授权验证，不执行词句为个人版授权验证
        if qianniuzhanghao:self.qjd=weiEncryptDecrypt().ed_encrypt(qianniuzhanghao)

    def v_version_verification(self):
        if self.qjd in self.req: return True
        else:
            win32api.MessageBox(0, '版本已更新，详情联系QQ1043014552',u'提示框',win32con.MB_SYSTEMMODAL)
            return False
    def v_account_verification(self):
        for i in self.req1:
            if self.qjd in i:
                self.req1=i.split('**')[1]
                self.req1=weiEncryptDecrypt().ed_decrypt(self.req1)
                self.req1=time.time()-int(self.req1)
                if self.req1>=0:
                    win32api.MessageBox(0, '授权过期，如需授权联系QQ1043014552',u'提示框',win32con.MB_SYSTEMMODAL)
                    return 0
                elif 0>self.req1>-259200:
                    win32api.MessageBox(0, '授权即将过期，如需授权联系QQ1043014552',u'提示框',win32con.MB_SYSTEMMODAL)
                    return 1
                else:return 1
        win32api.MessageBox(0,'填写的发送消息千牛帐号错误、未填写或者未授权，如需授权联系QQ1043014552',u'提示框',win32con.MB_SYSTEMMODAL)
        return 0
    def v_open_url(self):#用默认浏览器打开百度搜索千牛发消息
        webbrowser.open_new_tab('https://www.baidu.com/s?wd=http://www.51zhaoruanjian.com')
#-------------------------------------------------------------------------------------------------------------------------------- 
class weiShortcutKeys:
    '''快捷键'''
    def __init__(self,*arg):
        '''传入键的ASCII码按下和释放,Ctrl键的ASCII码为17 ,A[65],C[67]'''
        for i in arg:win32api.keybd_event(i,0,0,0)
        time.sleep(0.1)
        for i in arg[::-1]:win32api.keybd_event(i,0,win32con.KEYEVENTF_KEYUP,0)  #释放按键,arg[::-1]元组倒序
#--------------------------------------------------------------------------------------------------------------------------------
class weiHandleWindow:
    '''找子（孙）句柄，点击句柄坐标，句柄窗口到当前'''
    def hw_childrenHandle(self,hwnd):  
        """传入句柄hwnd,返回其所有子句柄的列表"""  
        handle = win32gui.FindWindowEx(hwnd, 0, None, None)
        handlelist=[]
        while handle>0:
            handlelist.append(handle)
            handle = win32gui.FindWindowEx(hwnd, handle, None, None)
        return handlelist
    def hw_allHandle(self,hwnd,btlx=None):
        """ 传入父窗口的句柄,和要查找的标题或者类型（默认为None），寻找父句柄下的所有子孙句柄 """  
        def find_idxSubHandle(hwnd,handlelist=[]):  
            handle = win32gui.FindWindowEx(hwnd, 0, None, None)
            while handle>0:
                pan_xuanze=0
                if btlx:
                    if btlx in win32gui.GetWindowText(handle) or btlx in win32gui.GetClassName(handle):pan_xuanze=1
                else:pan_xuanze=1
                if pan_xuanze:handlelist.append(handle)
                find_idxSubHandle(handle,handlelist)
                handle = win32gui.FindWindowEx(hwnd, handle, None, None)
        handlelist=[]
        find_idxSubHandle(hwnd,handlelist)
        return handlelist
    def hw_get_hnt(self,hwnd):
        """传入句柄，打印并返回句柄的类名和标题"""  
        title = win32gui.GetWindowText(hwnd)
        clsname = win32gui.GetClassName(hwnd)
        print(clsname,title)
        return clsname,title
    def hw_click_Handle(self,jb,wz=5,py_x=0,py_y=0,clicks=1,tp=1):
        '''传入jb句柄,wz位置,py_x便宜x,py_y偏移y,ds单双击,tp点击类型快慢, 按条件点击句柄'''
        left, top, right, bottom = win32gui.GetWindowRect(jb)
        if wz==5:x,y=int((left+right)/2),int((top+bottom)/2)
        elif wz==1:x,y=left,top
        elif wz==2:x,y=right,top
        elif wz==3:x,y=right,bottom
        elif wz==4:x,y=left,bottom
        if tp:pyautogui.click(x=x+py_x,y=y+py_y,clicks=clicks)
        else:
            win32api.SetCursorPos([x+py_x,y+py_y])
            for i in range(clicks):
                win32api.mouse_event(2,0,0,0,0)
                win32api.mouse_event(4,0,0,0,0)
    def hw_current(self,Frame1):
        '''激活窗口把焦点锁定到Frame1句柄的窗口上，第一句针对最小化的窗口'''
        win32gui.ShowWindow(Frame1,win32con.SW_SHOWNORMAL)
        import pythoncom
        pythoncom.CoInitialize()#在多线程里面使用win32com调用com组件的时候，需要用pythoncom.CoInitialize初始化一下
        shell = win32com.client.Dispatch("WScript.Shell")
        shell.SendKeys('%')
        win32gui.SetForegroundWindow(Frame1)
        pythoncom.CoUninitialize()#释放资源

#--------------------------------------------------------------------------------------------------------------------------------
import configparser#配置文件
class weiConfig:
    '''配置文件ini增删改查'''
    def __init__(self,file_path_name):
        self.file_path_name=file_path_name+'.ini'
        content = open(self.file_path_name,'rb').read()
        content=content.decode(encoding='UTF-8')
        content=re.sub('\ufeff','',content)
        open(self.file_path_name,'wb').write(bytes(content, encoding='utf-8'))
        self.config=configparser.ConfigParser()
        self.config.read(self.file_path_name,encoding='UTF-8')#读文件
    def c_read(self,Section,Key):
        '''传入项(Section)和键(Key),查询值(value)'''
        return self.config[Section][Key]
    def c_change(self,Section,dict1):
        '''传入项(Section)和字典(dict1)，进行增和修改'''
        for i in dict1:
            try:self.config.add_section(Section)
            except:pass
            self.config[Section][i]=dict1[i]
        with open(self.file_path_name,'w',encoding='UTF-8') as f:self.config.write(f)
    def c_del(self,Section,Key):
        '''传入项(Section)和键(Key)，进行删除'''
        self.config.remove_option(Section,Key) #删除一个配置项
        with open(self.file_path_name,'w',encoding='UTF-8') as f:self.config.write(f)
#配置文件如果含有换行用TAB缩进就可以。
#--------------------------------------------------------------------------------------------------------------------------------
import win32gui,win32ui,win32con, win32api
import cv2,numpy,aircv
class weiMatchImg:
    '''截屏,比对图片位置'''
    def mi_window_capture(self,filename):
        '''传入保存文件名，截屏并保存'''
        hwnd = 0 # 窗口的编号，0号表示当前活跃窗口
        hwndDC = win32gui.GetWindowDC(hwnd)# 根据窗口句柄获取窗口的设备上下文DC（Divice Context）
        mfcDC = win32ui.CreateDCFromHandle(hwndDC)# 根据窗口的DC获取mfcDC
        saveDC = mfcDC.CreateCompatibleDC()# mfcDC创建可兼容的DC
        saveBitMap = win32ui.CreateBitmap()# 创建bigmap准备保存图片
        MoniterDev = win32api.EnumDisplayMonitors(None, None)# 获取监控器信息
        w = MoniterDev[0][2][2]
        h = MoniterDev[0][2][3]
        saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)# 为bitmap开辟空间
        saveDC.SelectObject(saveBitMap)# 高度saveDC，将截图保存到saveBitmap中
        saveDC.BitBlt((0, 0), (w, h), mfcDC, (0, 0), win32con.SRCCOPY)# 截取从左上角（0，0）长宽为（w，h）的图片
        saveBitMap.SaveBitmapFile(saveDC, filename)
    def mi_matchImg(self,imgobj,imgsrc,confidence=0.5):
            '''传入小图、大图、相似度[confidence],返回小图所在大图的坐标'''
            '''imdecode以二进制流方式读取图片[numpy解决编码问题，避免中文出错]，通过aircv比对两图'''
            imobj = cv2.imdecode(numpy.fromfile(imgobj,dtype=numpy.uint8),-1)
            imsrc = cv2.imdecode(numpy.fromfile(imgsrc,dtype=numpy.uint8),-1)
            #match_result = aircv.find_template(imsrc,imobj,confidence)#
            match_result = aircv.find_all_template(imsrc,imobj,confidence)
            return match_result
#--------------------------------------------------------------------------------------------------------------------------------
from PIL import ImageGrab
class weiScreenshot:
    def __init__(self,fn,l,t,r,b):
        '''传入保存的文件名路径、左上右下坐标，截图并保存'''
        im = ImageGrab.grab((l,t,r,b))
        im.save(fn)
#--------------------------------------------------------------------------------------------------------------------------------
import sqlite3
class weiSqlite3:
    '''sqlite3增删改查'''
    def __init__(self,path):
        self.conn = sqlite3.connect(path)#连接数据库，不存在则创建
        self.cursor = self.conn.cursor()#创建游标
    def s_add_del_dpd(self,*sql):
        '''创建表、添加数据、删除、修改'''
        self.cursor.execute(*sql)
        self.conn.commit()#保存操作
    def s_sel(self,*sql):
        '''查询数据'''
        #return [i for i in self.cursor.execute(*sql)]
        return self.cursor.execute(*sql).fetchall()
    def s_sql(self,tb_name,li):
        '''传入表名和字段名，返回创建表格的sql语句'''
        sql="create table '%s' ('%s' primary key not null default '',"%(tb_name,li[0])
        for i in range(1,len(li)-1):
            sql+="'%s' text not null default '',"% li[i]
        sql+="'%s' text not null default '')"% li[-1]
        return sql
#--------------------------------------------------------------------------------------------------------------------------------
import pymysql
class weiMysql():
    def __init__(self,dataBase='BS_Data_qplxbqjd'):
        self.con=pymysql.connect(host='localhost', user='root',
                          passwd='123456', charset='utf8')
        self.cur=self.con.cursor()
        sql="create database if not exists %s character set utf8mb4;"% dataBase
        self.cur.execute(sql)#建库
        sql="use %s;"% dataBase
        self.cur.execute(sql)#使用库
    def m_add_del_upd(self,*sql):
        self.cur.execute(*sql)
        self.con.commit()#提交
    def m_sel(self,*sql):
        self.cur.execute(*sql)
        return self.cur.fetchall()
    def m_sql(self,tb_name,li):
        sql='''create table %s (%s char(50) primary key,'''%(tb_name,li[0])
        for j in range(1,len(li)-1):
            sql+=li[j]+' varchar(600) default "",'
        sql+='%s varchar(600) default "")'% li[-1]
        return sql
#--------------------------------------------------------------------------------------------------------------------------------
import xlrd
import xlwt
from xlutils.copy import copy
class weiExcel:
    '''在excel的最后一行写入列表DataList，如果excel文件（或者表名）不存在的话会自动创建'''
    def __init__(self,filename,sheet_name):
        '''初始化表：传入filename(Excel文件名及路径)、sheet_name（表名）'''
        self.filename=filename
        self.sheet_name=sheet_name
        try:self.workbook = xlrd.open_workbook(self.filename, formatting_info=True)
        except:
            wk=xlwt.Workbook()
            wk.add_sheet(sheet_name)
            wk.save(self.filename)
            self.workbook = xlrd.open_workbook(self.filename, formatting_info=True)
        self.sheet = self.workbook.sheet_by_name(sheet_name)
    def e_write(self,DataList=None,Header=None):
        if DataList is None:DataList = []
        self.e_nrows_or_ncols()
        newbook = copy(self.workbook)
        newsheet = newbook.get_sheet(self.sheet_name)
        if self.ncols==self.nrows==0:
            for i in range(len(Header)):newsheet.write(0,i,Header[i])
            self.nrows+=1
        for i in range(len(DataList)):newsheet.write(self.nrows,i,DataList[i])# 在末尾增加新行
        newbook.save(self.filename)# 覆盖保存
        self.workbook = xlrd.open_workbook(self.filename, formatting_info=True)
        self.sheet = self.workbook.sheet_by_name(self.sheet_name)
    def e_read(self,num=0,type1='hang'):
        '''传入num(第几行或列)，type1（类型hang或者其他）'''
        if type1=='hang':return self.sheet.row_values(num)#获取整行数据
        else:return self.sheet.col_values(num)#获取整列数据
    def e_nrows_or_ncols(self):
        '''定义刷新最大行数和列数'''
        self.nrows = self.sheet.nrows#获取行数
        self.ncols = self.sheet.ncols#获取列数
#--------------------------------------------------------------------------------------------------------------------------------
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
class weiSelenium:
    '''Selenium启动、验证是否为本公司店铺'''
    def s_run_driver(self):
        #option = webdriver.ChromeOptions()
        #option.add_argument('disable-infobars')
        #option.add_argument("user-data-dir=C:/Users/Administrator/AppData/Local/Google/Chrome/User Data")#设置成用户自己的数据目录
        #self.driver= webdriver.Chrome(chrome_options=option)
        self.driver= webdriver.Chrome()
        self.driver.get('https://login.taobao.com/member/login.jhtml')
        self.driver.maximize_window()
        ctypes.windll.user32.MessageBoxW(0, '初始化成功，请登陆账号进行后续操作','提示',0)
    def s_verification():
        '''验证是否为本公司店铺，是返回True，不是返回False'''
        li111=['七匹狼箱包旗舰店','septwolves美之瑞专卖店','七匹狼雅赋专卖店','SEPTWOLVES雅赋专卖店',
        '少年狼箱包','拼多多美之瑞专卖店','京东七匹狼雅赋专卖店','自然之名旗舰店','evm旗舰店',
        '自然之名雅赋专卖店','nacola旗舰店','汉苑良方海川专卖店','麂翔旗舰店','lucky旗舰店',
        'cosmecontact隐形眼镜旗舰','安娜苏隐形眼镜旗舰店','欧朗睛隐形眼镜旗舰店','洁云家居旗舰店',
        'mia米娅东冠专卖店','mia米娅旗舰店','vancl凡客诚品旗舰店']
        b=self.driver.find_element_by_css_selector('body').text
        b=[i for i in li111 if i in b]
        if not b:
            ctypes.windll.user32.MessageBoxW(0,'未授权或者帐号未登陆[非本公司店铺]，如有疑问联系老钱QQ：1043014552', u'提醒消息',0)
            return False
        else:return True
#--------------------------------------------------------------------------------------------------------------------------------
import chardet
class weiBigFileRead:#大文件读取
    def bfr_read(self,filename,zijie=500):
        '''传入文件名初始文件对象以及其字节数'''
        try:
            with open(filename,'rb') as self.f:
                self.f_len=self.f.seek(0,2)
                '''传入字节数，将文件对象的指针移动到倒数指定的字节数位置'''
                if self.f_len>zijie:self.f.seek(self.f_len-zijie,0)
                else:self.f.seek(0,0)
                '''读取指针移动后的文件对象的内容'''
                str1=self.f.read()
                encoding=chardet.detect(str1)['encoding']#返回字符的编码类型
                if encoding: return str1.decode(encoding,'ignore')
                else: return str1.decode('gbk','ignore')
        except:
            print('文件：%s不存在'% filename)
            return ''
            
#--------------------------------------------------------------------------------------------------------------------------------
if __name__=="__main__":
    #http://bbs.duowan.com/forum.php?mod=viewthread&tid=46820177
    #banBengYanZheng0=yanZheng('试用版20181020').banBengYanZheng()
    crypt=weiEncryptDecrypt()
    print('帐号加密',crypt.ed_encrypt('路易科林'))
    print('时间加密',crypt.ed_encrypt(str(int(time.time())+3600*24*360/24/360/2)))
    print('解密',crypt.ed_decrypt('aHDR0cDovL2Jicy5kdW93YW4uY29tL2ZvcnVtLnBocD9tb2Q9dmlld3RocmVhZCZ0aWQ9NDY4MjAxNzc#'))
    #juBingChuangKou().dangqian(132730)
    

    a001=['5LDiD5Yy554u8566x5YyF5peX6Iiw5bqX**MTDU3MDg1NTI5Ng##', '6IDeq54S25LmL5ZCN5peX6Iiw5bqX**MTDU5MDM4MTA0OA##',
          '5LDiD5Yy554u856em5Yqf5LiT5Y2W5bqX**MTDU3MTk5NDgzOA##', '5aD6J5aic6IuP6ZqQ5b2i55y86ZWc5peX6Iiw5bqX**MTDU3OTg3MTQ3Ng##',
          '5qDyn5pyX552b6ZqQ5b2i55y86ZWc5peX6Iiw5bqX**MTDU3OTg3MjA3NA##', 'bWDlh57Gz5aiF5Lic5Yag5LiT5Y2W5bqX**MTDU3OTg3MjE2Nw##',
          '5rDSB5LqR5a625bGF5peX6Iiw5bqX**MTDU3OTg3MjExNg##', '5LDiD5Yy554u86ZuF6LWL5LiT5Y2W5bqX**MTDU5MTE1NTMxOQ##',
          '6bDqC57+U5peX6Iiw5bqX**MTDU3MzU2MTk0MQ##', 'bHDVja3nml5foiLDlupc#**MTDU3OTg3MjAxNA##',
          'dXDRlbmHkvZHlpKnlhbDml5foiLDlupc#**MTDU3MDg2MTI4OQ##', 'dXDRlbmHkvZHlpKnlhbDmtbflpJbml5foiLDlupc#**MTDU3MDg2MTYwMA##',
          'ZXDZt5peX6Iiw5bqX**MTDU4ODIwNDAyNA##', 'dmDFuY2zlh6HlrqLor5rlk4Hml5foiLDlupc#**MTDU4MjA4OTU3Nw##',
          '5rDGJ6IuR6Imv5pa55rW35bed5LiT5Y2W5bqX**MTDU4NjY3MTExMw##', 'bmDVvY291bGVy6ZqQ5b2i55y86ZWc5peX6Iiw5bqX**MTDU3MTEwNTkyNw##',
          '6ZDqG56yb55S15Zmo5LiT6JCl5bqX**MTDU5NTMyMzA2MQ##', 'NzDNob3Vyc+aXl+iIsOW6lw##**MTDU3MzUzMzk0MA##',
          '5LDyK5Y2h6I6x5bGF5a625pel55So5LiT6JCl5bqX**MTDU3NDMxOTM5MQ##', '5rDi45oiPOA##**MTDU3OTMzNDc1MA##',
          '6YDeR5Yia546L5peX6Iiw5bqX**MTDU4OTAzNzg0OQ##', 'c3DZhcmV55YWs6aaG**MTDU3ODkxMjkyMA##', 'bWDFzdHJvemF2YXR0aeaXl+iIsOW6lw##**MTDU4OTk5MzQ1MA##']
    a001=[]
    a001=a001
    b01=[i.split('**') for i in a001]
    for i in b01:
        dianm=crypt.ed_decrypt(i[0])
        shij=crypt.ed_decrypt(i[1])
        ee=float(shij)
        if ee>time.time():
            shij=time.localtime(ee)
            shij='%4d%02d%02d %02d:%02d:%02d'%(shij[:6])
            li=[dianm,shij,'%s**%s,'% tuple(i)]
            print(li)





#```15LDiD5Yy554u8566x5YyF5peX6Iiw5bqX**MTDU3MDg1NTI5Ng##,6IDeq54S25LmL5ZCN5peX6Iiw5bqX**MTDU5MDM4MTA0OA##,6ZDqG56yb55S15Zmo5LiT6JCl5bqX**MTDU5NTMyMzA2MQ##,5aD6J5aic6IuP6ZqQ5b2i55y86ZWc5a6Y5pa55peX6Iiw5bqX**MTDU3OTg3MTQ3Ng##,5LDiD5Yy554u86ZuF6LWL5LiT5Y2W5bqX**MTDU5MTE1NTMxOQ##,NzDNob3Vyc+aXl+iIsOW6lw##**MTDU3MzUzMzk0MA##,6bDqC57+U5peX6Iiw5bqX**MTDU3MzU2MTk0MQ##,5LDyK5Y2h6I6x5bGF5a625pel55So5LiT6JCl5bqX**MTDU3NDMxOTM5MQ##,bHDVja3nml5foiLDlupc#**MTDU4ODIwNDAyNA##,5rDi45oiPOA##**MTDU3OTMzNDc1MA##,54Dix5py65pWw56CB5LiT6JCl5bqX**MTDU4OTAzNzg0OQ##,dXDRlbmHkvZHlpKnlhbDml5foiLDlupc#**MTDU3MDg2MTI4OQ##,dXDRlbmHkvZHlpKnlhbDmtbflpJbml5foiLDlupc#**MTDU3MDg2MTYwMA##,ZXDZt5peX6Iiw5bqX**MTDU4ODIwNDAyNA##,c3DZhcmV55YWs6aaG**MTDU3ODkxMjkyMA##,dmDFuY2zlh6HlrqLor5rlk4Hml5foiLDlupc#**MTDU4MjA4OTU3Nw##,5rDGJ6IuR6Imv5pa55rW35bed5LiT5Y2W5bqX**MTDU4NjY3MTExMw##,bWDFzdHJvemF2YXR0aeaXl+iIsOW6lw##**MTDU4OTk5MzQ1MA##,bmDVvY291bGVy6ZqQ5b2i55y86ZWc5peX6Iiw5bqX**MTDU3MTEwNTkyNw##,5LDiD5Yy554u856em5Yqf5LiT5Y2W5bqX**MTDU3MTk5NDgzOA##,cGDVkaWFraWTmtbflpJbml5foiLDlupc65r2Y5aSa5ouJ**MTDU3MDA3MTQyMA##,6LDev5piT56eR5p6X5pav5peX6Iiw5bqXOuWGrOWGrA##**MTDU2ODcxNjA2My4w,,,,,,,,,,,,,,,,,,,,,,,,54DmI5pys6aqM6K+BMjAxOTA5MDc#1```



