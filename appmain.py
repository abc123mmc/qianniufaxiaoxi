from tkinter import * #界面
import pyautogui#模拟鼠标键盘操作
import time#时间模块
import weiabc123
import sendmsg
pyautogui.FAILSAFE = False


class jieMian(sendmsg.qianniu):
    def __init__(self):
        banBengYanZheng0=weiabc123.yanZheng('版本验证20190907').banBengYanZheng()
        if not banBengYanZheng0:
            return
        weiabc123.weiThreading().wei_start(self.runabc)#通过版本验证即运行界面
        super().__init__()
        self.xianCheng=weiabc123.weiThreading()#调用weiabc123下的xianCheng类
    def runabc(self):        
        self.root =Tk()
        self.root.title("千牛批量自动发消息")#标题
        self.root.geometry("523x257+600+250")#参数'600x600'是x 不是*,“无参数默认是撑开.横x纵+左边距+上边距”
        self.root.resizable(width=True, height=True) #False不可变, True可变,默认为True
        self.Label1=Label(self.root,text=u'请输入发送消息内容：',padx=0,anchor = 'w',
                     font = ('', '10', 'bold'),foreground = '#080808',wraplength = 400,justify= 'left')
        self.Label1.place(x=10,y=7,width=130,height=16)
        self.Label2=Label(self.root,text=u'使用说明(点击查看详细内容)：',padx=0,anchor = 'w',font = ('', '10', 'bold'),
                     foreground = '#080808',wraplength = 400,justify= 'left')
        self.Label2.place(x=270,y=5,width=200,height=20)
        self.Label3=Label(self.root,text=u'输入千牛帐号：',padx=0,anchor = 'w',font = ('', '10', 'bold'),
                     foreground = '#080808',wraplength = 400,justify= 'left')
        self.Label3.place(x=10,y=226,width=84,height=12)
        text=sendmsg.setingwei.appmain['Instructions']
        self.Label4=Label(self.root,text=text,padx=0,anchor = 'nw',font = ('', '10'),
                     foreground = '#080808',wraplength = 246,justify= 'left')
        self.Label4.place(x=270,y=30,width=246,height=180)
        text=weiabc123.weiConfig(r'cof\peizhi').wei_read('config','发送内容')
        self.Text1=Text(self.root,padx=0,font = ('', '10'),foreground = '#080808')
        self.Text1.place(x=10,y=30,width=246,height=180)
        
        self.Text1.insert(END,text)#END表示在末尾处插入,INSERT表示在光标位置插入
        self.Entry1_1=StringVar()
        self.Entry1=Entry(self.root,textvariable=self.Entry1_1,font = ('', '10'))
        self.Entry1.place(x=100, y=224,width=300,height=16)
        self.Entry1_1.set(weiabc123.weiConfig(r'.\cof\peizhi').wei_read('config','发送帐号'))

        self.Text1.bind("<Enter>", self.jingRu)#绑定事件
        self.Text1.bind("<Leave>", self.yiChu)
        self.Entry1.bind("<Enter>", self.jingRu)#绑定事件
        self.Entry1.bind("<Leave>", self.yiChu)
        self.Label2.bind("<Button-1>", self.dianJi)
        
        self.Button2=Button(self.root, text="开始",font = ('', '14', 'bold'), command=self.kaishiFaXiaoXi)
        self.Button2.place(x=410, y=220,width=45,height=23)    
        self.Button2=Button(self.root, text="结束",font = ('', '14', 'bold'), command=self.jieShu)
        self.Button2.place(x=460, y=220,width=45,height=23) 
        self.root.mainloop() # 进入消息循环
        self.jieShu()

    def jingRu(self,event):
        '''鼠标进入事件'''
        self.Label2=Label(self.root,text=u'使用说明(点击查看详情)：',padx=0,anchor = 'w',font = ('', '10', 'bold'),
                     foreground = 'red',wraplength = 400,justify= 'left')
        self.Label2.place(x=270,y=5,width=200,height=20)
        
    def yiChu(self,event):
        '''鼠标移出事件'''
        time.sleep(0.2)
        self.Label2=Label(self.root,text=u'使用说明(点击查看详情)：',padx=0,anchor = 'w',font = ('', '10', 'bold'),
                     foreground = 'blue',wraplength = 400,justify= 'left')
        self.Label2.place(x=270,y=5,width=200,height=20)
        self.Label2.bind("<Button-1>", self.dianJi)
        
    def dianJi(self,event):
        '''跳转到网站'''
        weiabc123.yanZheng().wangZhi()

    def kaishiFaXiaoXi(self):
        '''线程'''
        self.xierupeizwj()#把界面内容写入配置文件
        try:
            if self.fxx1:
                if self.a021.panDuan:self.a021.panDuan=0
                else:self.a021.panDuan=1
        except:
            self.fxx1=1
            self.xianCheng.wei_start(self.Control)

    def jieShu(self):
        '''线程'''
        self.a021.panDuan='out'
        pyautogui.hotkey('altleft','F7')
        self.root.quit()

    def xierupeizwj(self):#把界面内容写入配置文件
        qianniuzhanghao=self.Entry1.get()#获取lineEdit文本值
        qianniuzhanghao=qianniuzhanghao.replace(' ','')#去除空格
        qianniuzhanghao=qianniuzhanghao.replace('\n','')#去除换行
        fslr001=self.Text1.get('1.0',END)
        xr=weiabc123.weiConfig(r'.\cof\peizhi')
        xr.wei_change('config',{'发送内容':fslr001,'发送帐号':qianniuzhanghao})
        xr.wei_change('config',{'发送内容':fslr001,'发送内容':fslr001})
        
if __name__=="__main__":
    try:
        jieMian01=jieMian()
        try:jieMian01.root.quit()
        except:pass
    except:weiabc123.weiLog(r'.\cof\error_log').wei_error()








