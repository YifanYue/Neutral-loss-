# -*- coding: utf-8 -*-
"""
Created on Fri Dec  3 14:13:17 2021

@author: YiFan Yue
"""
#全程用array计算，在我的电脑上用时半分钟，如果是dataframe要一分半多
import tkinter as tk
import numpy as np
import pandas as pd
import time
#建立窗口
window=tk.Tk()
window.title('mass spectrometry data processing')
window.geometry('1500x900')
#标签
l1=tk.Label(window,text='a mass spectrometry data processing software made by Yifan Yue',font=("Times",8,"bold"))#font确定字体为Times，大小为8，字体加粗bold
l1.place(relx=0.5,rely=0.93,relheight=0.1,relwidth=0.5)
#定义输入框
e1=tk.Entry(window)
e1.place(relx=0.25,rely=0.05,relheight=0.08,relwidth=0.5)
e1.insert(0, "Molecular weight of missing fragments;ex:162.05282")
e2=tk.Entry(window)
e2.place(relx=0.25,rely=0.15,relheight=0.08,relwidth=0.5)
e2.insert(0, "Allowable error of molecular weight;ex:0.0002")
e3=tk.Entry(window)
e3.place(relx=0.25,rely=0.25,relheight=0.08,relwidth=0.5)
e3.insert(0, "Allowable error of retention time;ex:0.1")
e4=tk.Entry(window)
e4.place(relx=0.25,rely=0.35,relheight=0.08,relwidth=0.5)
e4.insert(0, "Address and Name of the first input CSV table")
e5=tk.Entry(window)
e5.place(relx=0.25,rely=0.45,relheight=0.08,relwidth=0.5)
e5.insert(0, "Address and Name of the second input CSV table")
e6=tk.Entry(window)
e6.place(relx=0.25,rely=0.55,relheight=0.08,relwidth=0.5)
e6.insert(0, "Address and Name of the first input CSV table")
e7=tk.Entry(window)
e7.place(relx=0.25,rely=0.65,relheight=0.08,relwidth=0.5)
e7.insert(0, "Address and Name of the second output CSV table")
#加入文本框
t=tk.Text(window,height=2)
t.place(relx=0.25,rely=0.75,relheight=0.08,relwidth=0.5)

#运行的程序
def func():
    tic=time.time()
    suipian=float(e1.get())
    wucha=float(e2.get())
    RT=float(e3.get())
    filename=e4.get()
    filename2=e5.get()
    output1=e6.get()
    output2=e7.get()
    iscidselected = []
    index = []
    Mass_down = suipian - wucha
    Mass_up = suipian + wucha
    iscid=pd.read_csv(filename,header=0,index_col=0)
    PeakTable=pd.read_csv(filename2,header=0,index_col=0)
    iscida = np.array(iscid) #转化为array格式
    for i in range(iscida.shape[0]-1):
        for j in range(i+1,iscida.shape[0]):
            if (Mass_down <= abs(iscida[i][0]-iscida[j][0]) <= Mass_up) and (0 <= abs(iscida[i][1]-iscida[j][1]) <= RT):
                if iscida[i][0]>iscida[j][0]:
                   iscidselected.append(iscida[i])
                   index.append(i+1)
                   iscidselected.append(iscida[j])
                   index.append(j+1)
                else:
                   iscidselected.append(iscida[j])
                   index.append(j+1)
                   iscidselected.append(iscida[i])
                   index.append(i+1)
    iscidselected = np.array(iscidselected)
    index = np.array(index)  
    final = pd.DataFrame(iscidselected)
    final.index=index
    final.columns=iscid.columns
    
    
    PeakTableselected=[]
    PeakTablea=np.array(PeakTable)
    index2=[]
    for i in range(0,iscidselected.shape[0],2):
        for j in range(0,PeakTablea.shape[0]):
            if abs(iscidselected[i,0]-PeakTablea[j,0])<=wucha :
                if abs(iscidselected[i,1]-PeakTablea[j,1])<=RT :
                    PeakTableselected.append(PeakTablea[j,:])
                    index2.append(j+1)
    PeakTableselected = pd.DataFrame(PeakTableselected)
    PeakTableselected.index=index2
    PeakTableselected.columns=PeakTable.columns
    final.to_csv(output1,header=True,index=True)
    PeakTableselected.to_csv(output2,header=True,index=True)
    toc=time.time()
    t.insert('insert',"DONE "+str(toc-tic)+"s\n")

#按钮
b1=tk.Button(window,text='search',command=func)
b1.place(relx=0.25,rely=0.85,relheight=0.08,relwidth=0.5)

#建立框
window.mainloop()
