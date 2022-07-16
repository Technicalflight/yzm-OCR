import ddddocr
import pyperclip
import requests
import pytesseract
from PIL import Image
import os
import cv2
#死循环
while True:
    cz = input("数字字母验证码请按1,滑块验证码请按2,点选请按3,按n退出)：")
    if cz == '1':
        #获取验证码
        yzm = input("请将验证码图片链接拖入到当前窗口(或者直接输入验证码图片链接)：")
        yzm = requests.get(yzm)
        ocr = ddddocr.DdddOcr()
        image_yzm = ocr.classification(yzm.content)
        pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"  # 设置你下载的tesseract.exe位置路径,类似于
        #判断是否存在yzm.png文件
        if os.path.exists('yzm.png'):
            os.remove('yzm.png')
        #下载验证码图片
        with open('yzm.png', 'wb') as f:
            f.write(yzm.content)
        text = pytesseract.image_to_string('yzm.png', lang='eng')  # 识别
        print(f'Google tesseract识别的验证码为:{text}')
        print(f'ddddocr识别的验证码为:{image_yzm}')
        #复制到剪贴板
        pyperclip.copy(image_yzm)
        print("验证码已复制到剪贴板(默认复制ddddocr识别的验证码)")
        #等待下一次循环
        input("按回车键继续")
        continue
    elif cz == "2":
        huakuai = input("请输入滑块图片链接：")
        back = input("请输入滑块图片背景链接：")
        huakuai = requests.get(huakuai)
        back = requests.get(back)
        #判断是否存在huakuai.png文件
        if os.path.exists('huakuai.png'):
            os.remove('huakuai.png')
        #判断是否存在back.png文件
        if os.path.exists('back.png'):
            os.remove('back.png')
        #下载滑块图片
        #保存滑块图片
        with open('huakuai.png', 'wb') as f:
            f.write(huakuai.content)
        #保存滑块图片背景
        with open('back.png', 'wb') as f:
            f.write(back.content)
        #调用滑块验证码识别
        det = ddddocr.DdddOcr(det=False, ocr=False)
        with open('huakuai.png', 'rb') as f:
            target_bytes = f.read()
        with open('back.png', 'rb') as f:
            background_bytes = f.read()
        res = det.slide_match(target_bytes, background_bytes)
        print(res)
        print("滑块验证码识别完成")
        print(res['target_y'])
        if res['target_y'] < res['target'][1] + 5 or res['target_y'] > res['target'][1] - 5 or res['target_y'] == res['target'][1]:
            print('移动的x轴为：',res['target'][0])
            #用js模拟移动滑块
            js = 'var q=document.getElementsByClassName("检查滑块的classname填入此处")[0];q.style.left="'+str(res['target'][0])+'px";'
            print("滑块验证码识别完成")
            print('请在浏览器控制台执行:' + js)
            input("按回车键继续")
            continue
        if res['target_y'] < res['target'][3] + 5 or res['target_y'] > res['target'][3] - 5 or res['target_y'] == res['target'][3]:
            print('移动的x轴为：',res['target'][2])
            #用js模拟移动滑块
            js = 'var q=document.getElementsByClassName("检查滑块的classname填入此处")[0];q.style.left="'+str(res['target'][2])+'px";'
            print(js)
            print("滑块验证码识别完成")
            print('请在浏览器控制台执行:' + js)
            input("按回车键继续")
            continue
        print(res['target'])
        input("按回车键继续")
        continue
    elif cz == "3":
        test = input("请输入点选图片链接：")
        #判断是否存在test.png文件
        if os.path.exists('test.png'):
            os.remove('test.png')
        #下载点选图片
        test = requests.get(test)
        #保存点选图片
        with open('test.png', 'wb') as f:
            f.write(test.content)
        #调用点选验证码识别
        det = ddddocr.DdddOcr(det=True)
        with open("test.png", 'rb') as f:
            image = f.read()
        poses = det.detection(image)
        print(poses)
        im = cv2.imread("test.png")
        for box in poses:
            x1, y1, x2, y2 = box
            im = cv2.rectangle(im, (x1, y1), (x2, y2), color=(0, 0, 255), thickness=2)
        cv2.imwrite("result.png", im)
        #js模拟点选验证码
        print("点选验证码识别完成")
        #等待下一次循环
        input("按回车键继续")
        continue
    #退出循环
    if cz == "n":
        break