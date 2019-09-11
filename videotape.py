#发送过程进行录屏，调用慢放分析各个环节，进行优化
from PIL import ImageGrab
import numpy as np
import cv2
def luping(t):
    '''传入录制时间（秒），进行录屏'''
    image = ImageGrab.grab()#获得当前屏幕
    width = image.size[0]
    height = image.size[1]
    print("width:", width, "height:", height)
    print("image mode:",image.mode)
    k=np.zeros((width,height),np.uint8)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')#编码格式
    video = cv2.VideoWriter('test.mp4', fourcc, 24, (width, height))
    #输出文件命名为test.mp4,帧率为16，可以自己设置
    b=0
    while True:
        img_rgb = ImageGrab.grab()
        img_bgr=cv2.cvtColor(np.array(img_rgb), cv2.COLOR_RGB2BGR)#转为opencv的BGR格式
        video.write(img_bgr)
        b+=1
        if b==t*10:#退出录制条件
            print(b)
            break
    video.release()
    cv2.destroyAllWindows()


if __name__=="__main__":
    t=200
    luping(t)
