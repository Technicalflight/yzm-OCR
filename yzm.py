import ddddocr
import pyperclip
import requests
import pytesseract
from PIL import Image
import os
#死循环
while True:
    yzm = input("请将验证码图片链接拖入到当前窗口(或者直接输入验证码图片链接)：")
    yzm = requests.get(yzm)
    ocr = ddddocr.DdddOcr()
    image_yzm = ocr.classification(yzm.content)
    pytesseract.pytesseract.tesseract_cmd = r"xxx"  # 设置你下载的tesseract.exe位置路径,类似于C:\Program Files\Tesseract-OCR\tesseract.exe
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
    #退出循环
    cz = 'y'
    cz = input("是否继续？(y/n)(默认继续)：")
    if cz == "n":
        break