import re
import os,time
import fnmatch
import traceback#用于错误处理

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
        except:
            pass

def iterfindfiles(path, filename):
    li=[]
    for root, dirs, files in os.walk(path):
        if filename in files:
            li +=[os.path.join(root, filename)]
    return li

def get_path(wangwangming):
    t=time.time()
    b=[chr(i) + ':' for i in range(65,91) if os.path.isdir(chr(i) + ':')]
    li=[]
    for j in b:
        if 'F' not in j : print('正在获取中，请耐心等待......')
        l=[i for i in iterfindfiles(j, "topuser.xml") if wangwangming in i]
        li+=l
    print(f'获取耗时{time.time()-t}秒')

    return li[0]

def get_data(path):
    with open(path,'r',encoding='utf-8') as ff:
        text=ff.read()
        #返回数组（旺旺名，标星类型，标星的时间戳）,标星类型1：黄星，2：红星，3：蓝星，4.绿星
        text0=re.findall('item id="cntaobao(.*?)" type="(\d)">(\d*?)<',text)
        text0={i[2]:i[:2] for i in text0}
        text1=sorted(text0,reverse = True)#时间戳的列表
    return text1,text0

def write_txt(text1,text0,file_name='标星用户.txt'):
    for i in  text1:
        if i[1]=='1':
        with open(file_name, 'a') as ff:ff.write(text0[i][0]+'\n')

def main():
    try:
        wangwangming='游戏8=林克'
        print('开始获取标星用户')
        path=get_path(wangwangming)
        print('开始保存标星用户')
        text1,text0 = get_data(path)
        write_txt(text1)
        print('处理完成')
        time.sleep(10)
    except:
        print('发生异常，详情请查看日志')
        weiLog('error').l_error()

if __name__ == '__main__':
    #main()
    pass













