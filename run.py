import re
import os,time
import fnmatch
def iterfindfiles(path, fnexp):
    for root, dirs, files in os.walk(path):
        for filename in fnmatch.filter(files, fnexp):
            yield os.path.join(root, filename)

t=time.time()
b=[chr(i) + ':' for i in range(65,91) if os.path.isdir(chr(i) + ':')]
li=[]
for j in b:
    l=[i for i in iterfindfiles(j, "topuser.xml") if '游戏8=林克' in i]
    li+=l
print(time.time()-t)


li[0]
f=open(li[0],'r',encoding='utf-8')
text=f.read()
text0=re.findall('item id="cntaobao(.*?)" type="(\d)">(\d*?)<',text)
text0={i[2]:i[:2] for i in text0}
text1=sorted(text0,reverse = True)
for i in  text1:
    if text0[i][1]=='1':
        with open('标星用户.txt','a') as ff:ff.write(text0[i][0]+'\n')



'''
for i in  text0:
    if i[1]=='1':
        with open('标星用户.txt','a') as ff:ff.write('%s	%s'%(i[0],'黄星')+'\n')
    elif i[1]=='2':
        with open('标星用户.txt','a') as ff:ff.write('%s	%s'%(i[0],'红星')+'\n')
    elif i[1]=='3':
        with open('标星用户.txt','a') as ff:ff.write('%s	%s'%(i[0],'蓝星')+'\n')
    elif i[1]=='4':
        with open('标星用户.txt','a') as ff:ff.write('%s	%s'%(i[0],'绿星')+'\n')
'''
