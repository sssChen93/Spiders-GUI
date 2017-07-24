#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from tkinter import *
import requests
import re
from tkinter.messagebox import *
import urllib.request
import os
from PIL import Image, ImageTk
import threading


def read_url():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)\ '
                      'Chrome/59.0.3071.115 Safari/537.36'}
    url = r'^((https|http|ftp)?:\/\/)[^\s]+'
    s = ent_1.get()
    if re.match(url, s):
        try:
            r = requests.get(s, headers=headers, timeout=10)
            r.raise_for_status()
            txt_1.insert(1.0, r.text)
        except:
            showinfo(title='超时', message='请求超时,请检查网址是否正确')
    else:
        showinfo(title='error', message='请输入正确的rul')


def del_url():
    global var
    txt_1.delete(1.0, END)
    txt_2.delete(1.0, END)
    var = 0
    lab_2.configure(text='下载进度：%.2f%%' % var)


def get_pic():
    html = txt_1.get(0.0, END)
    pic_list = re.findall(r'<img[^>]*src[=\"\']+([^\"\']*)[\"\'][^>]*>', html)
    for pic in pic_list:
        txt_2.insert(1.0, pic + '\n')


def thr():
    i = 0
    name = ent_1.get().split('.')
    pic_adr_list = txt_2.get(0.0, END).split('\n')
    reg = r'^http:.*'
    t = 1
    for pic_adr in pic_adr_list:
        try:
            if not os.path.exists(r'D:\Python\pictures\%s' % name[1]):
                os.makedirs(r'D:\Python\pictures\%s' % name[1])
                os.chdir(r'D:\Python\pictures\%s' % name[1])
            address = r'D:\Python\pictures\%s' % name[1]
            if not re.match(reg, pic_adr):
                pic_adr = 'http:' + pic_adr
            global var
            var = t * 100 / len(pic_adr_list)
            lab_2.configure(text='下载进度：%.2f%%' % var)
            urllib.request.urlretrieve(pic_adr, address + '\%d.jpg' % i)
            t += 1
        except:
            continue
        i += 1
    lab_2.configure(text='下载进度：完成')


def on_save():
    t = threading.Thread(target=thr)
    t.start()


def show_pic():
    top = Toplevel()
    top.title('显示图片')
    top.minsize(480, 400)
    i = 0
    name = ent_1.get().split('.')
    address = r'D:\Python\pictures\%s' % name[1]

    def change():
        global image_2
        global img_2
        nonlocal i
        try:
            i = i + 1
            image_2 = Image.open(address + '\%d.jpg' % i)
            img_2 = ImageTk.PhotoImage(image_2)
            lab_3.configure(image=img_2)
        except:
            i = -1
            i = i + 1
            image_2 = Image.open(address + '\%d.jpg' % i)
            img_2 = ImageTk.PhotoImage(image_2)
            lab_3.configure(image=img_2)
        return change

    def open_file():
        os.startfile(address)

    image_1 = Image.open(address + '\%d.jpg' % i)
    img_1 = ImageTk.PhotoImage(image_1)
    image_2 = 0
    img_2 = 0
    lab_3 = Label(top, image=img_1, width=480, height=300)
    lab_3.grid(row=0, columnspan=2)
    but_6 = Button(top, text='切换图片', command=change)
    but_6.grid(row=1, column=0, sticky=S, pady=10)
    but_7 = Button(top, text='打开图片目录', command=open_file)
    but_7.grid(row=1, column=1, sticky=S, pady=10)
    top.mainloop()


if __name__ == '__main__':
    root = Tk()
    root.title('获取网站源码程序')
    root.minsize(800, 700)
    lab_1 = Label(root, text='请输入网站url：', font='100')
    lab_1.grid(row=0, columnspan=3)
    ent_1 = Entry(root, width=100)
    ent_1.grid(row=1, columnspan=2)
    but_1 = Button(root, text='获取网站源码', command=read_url)
    but_1.grid(row=1, column=2, padx=20)
    txt_1 = Text(root, width=100)
    txt_1.grid(row=2, columnspan=2)
    but_2 = Button(root, text='清空源码内容', command=del_url)
    but_2.grid(row=2, column=2, padx=20)
    txt_2 = Text(root, width=100)
    txt_2.grid(row=3, columnspan=2)
    but_3 = Button(root, text='获取图片地址', command=get_pic)
    but_3.grid(row=3, column=2, padx=20)
    but_4 = Button(root, text='下载并保存图片', command=on_save)
    but_4.grid(row=4, column=0, padx=100)
    var = 0
    lab_2 = Label(root, text='下载进度：%.2f%%' % var)
    lab_2.grid(row=4, column=1, ipadx=100)
    but_5 = Button(root, text='显示图片', command=show_pic)
    but_5.grid(row=4, column=2, padx=20)
    root.mainloop()
