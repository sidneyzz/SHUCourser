#!/usr/bin/env python
# coding: utf-8

# In[6]:



import tkinter as tk
import time, sys, os, os.path
from SHUCourser import SHUCourser
from connDB import connDB
from tkinter import messagebox

import re
import requests
import random
import sys
import threading
import time as t
from bs4 import BeautifulSoup
from PIL import Image, ImageTk


myBot = SHUCourser()
myDB = connDB()

def nowTime():
    return t.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

class SHUCourserGUI(tk.Tk):
    
    
    def __init__(self):
        tk.Tk.__init__(self)
        self.title('Abracadabra!')
        self.geometry('320x400')
        self._frame = None
        self.switch_frame(StartPage)

    def switch_frame(self, frame_class):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()
    
class StartPage(tk.Frame):
    def __init__(self, master):
        
        def resource_path(relative_path):
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            if hasattr(sys, '_MEIPASS'):
                return os.path.join(sys._MEIPASS, relative_path)
            return os.path.join(os.path.abspath("."), relative_path)
        tk.Frame.__init__(self, master)
        #Frame
        mainFrame = tk.Frame(self)
        mainFrame.pack(pady=5)
        logoFrame = tk.Frame(mainFrame)
        logoFrame.pack(pady=10)
        formFrame = tk.Frame(mainFrame)
        formFrame.pack()
        inputFrame = tk.Frame(formFrame)
        inputFrame.pack()
        leftFormFrame = tk.Frame(inputFrame)
        leftFormFrame.pack(side='left')
        rightFormFrame = tk.Frame(inputFrame)
        rightFormFrame.pack(side='right')
        bottomformFrame = tk.Frame(formFrame)
        bottomformFrame.pack(side='bottom')
        footerFrame = tk.Frame(mainFrame)
        footerFrame.pack(pady=5)
        
        #widge
        imageDirection = "img"
        tk.Label(logoFrame, text='皇家山洞口魔法學院小精靈', font=("Arial", 18)).pack()
        
        def submit():
            global ACCOUNT
            global PASSWORD
            ACCOUNT = accountInput.get().upper() 
            PASSWORD = passwordInput.get()
            if ACCOUNT and PASSWORD:
                loginStatus = myBot.login(ACCOUNT, PASSWORD) ##改回
                loginStatus = True
                if loginStatus == True:
                    if myDB.findusr(ACCOUNT) != True :
                        myDB.initusr(ACCOUNT, False, 1)
                    master.switch_frame(PageOne)
                else:
                    tk.messagebox.showwarning(message=loginStatus)
            else:
                tk.messagebox.showwarning(message='請輸入帳號與密碼！')
    
        tk.Label(leftFormFrame, text='帳號：').pack()
        tk.Label(leftFormFrame, text='密碼：').pack()
        accountInput = tk.Entry(rightFormFrame, width=15)
        accountInput.pack()
        passwordInput = tk.Entry(rightFormFrame, show='*', width=15)
        passwordInput.pack()
        submitButton = tk.Button(bottomformFrame, text='進入', command=submit, width=10)
        submitButton.pack()
        tk.Label(footerFrame, text='免責聲明及注意事項', font=("Arial", 15), fg = "red").pack()
        tk.Label(footerFrame, text='            1.小精靈僅為學術研究用途，請勿拍打\n            2.小精靈可能會秀逗，造成的損失請自行承擔\n            3.公平起見，每學期只能請小精靈幫一次忙\n            4.為了以上目的，小精靈會蒐集你的學號\n            (不包含密碼)、連線及選課資訊\n            5.小精靈出包請email回報\n            6.小精靈有幫上忙可以請他喝咖啡\n            7.繼續使喚小精靈視為同意以上條款', font=("Arial", 12), justify = 'left').pack()
    
        def btnCoffee():
            imageDirection = "img"
            top1 = tk.Toplevel(self)
            top1.title('Donate Coffee!')
            tk.Label(top1, text='街口支付<------------------>歐付寶', font=("Arial", 15)).pack()
            pic = Image.open(resource_path(os.path.join(imageDirection, 'jkpay.png')))
            img = ImageTk.PhotoImage(pic)
            pic1 = Image.open(resource_path(os.path.join(imageDirection, 'opay.png')))
            img1 = ImageTk.PhotoImage(pic1)
            #img = tk.PhotoImage(file=resource_path(os.path.join(imageDirection, 'jkpay.png')))
            #img1 = tk.PhotoImage(file=resource_path(os.path.join(imageDirection, 'opay.png')))
            canvas = tk.Canvas(top1, width = 390 ,height = 200)
            canvas.create_image(0,10,image = img,anchor="nw")
            canvas.create_image(400,113,image = img1,anchor="e")
            canvas.pack(side='top')  
            tk.Label(top1, text='小精靈感謝你的咖啡<(_ _)>', font=("Arial", 15)).pack()
            top1.mainloop()
            
        self.image = tk.PhotoImage(file=resource_path(os.path.join(imageDirection, 'coffee.png'))).subsample(15, 15)
        coffee = tk.Button(footerFrame, 
        text='請小精靈喝咖啡!',
        pady=2,
        padx=10,
        image = self.image,
        compound = 'left',
        command =  btnCoffee
        )
        coffee.pack(side='top')
        tk.Label(footerFrame, text='Bug Report : readmymailplz@gmail.com', font=("Arial", 12), justify = 'left').pack()
        
        
        #tk.Button(self, text="Open page one",command=lambda: master.switch_frame(PageOne)).pack()

class PageOne(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        master.geometry('580x400')
        
        #Frame
        mainFrame = tk.Frame(self)
        mainFrame.pack(pady=5)
        formFrame = tk.Frame(mainFrame)
        formFrame.pack()
        inputFrame = tk.Frame(formFrame)
        inputFrame.pack()
        leftFormFrame = tk.Frame(inputFrame)
        leftFormFrame.pack(side='left')
        rightFormFrame = tk.Frame(inputFrame)
        rightFormFrame.pack(side='right')
        wishFrame = tk.Frame(rightFormFrame)
        wishFrame.pack(side='left')
        selectedFrame = tk.Frame(rightFormFrame)
        selectedFrame.pack(side='right')
        bottomformFrame = tk.Frame(formFrame)
        bottomformFrame.pack(side='bottom')
        
        #widget
        tk.Label(wishFrame , text='願望清單(建議上限五門)').pack()
        tk.Label(selectedFrame, text='已選課程').pack()
        wishList = tk.Listbox(wishFrame )
        wishList.config(width=14,height=12)
        wishList.pack(side='left', padx =10)
        selectedList = tk.Listbox(selectedFrame)
        selectedList.config(width=14,height=12)
        selectedList.pack(side='right', padx = 10)
        tk.Label(bottomformFrame, text='訊息記錄').pack()
        logBox = tk.Listbox(bottomformFrame, relief='ridge')
        logBox.config(width=60, height=8)
        logBox.pack()
        tk.Label(leftFormFrame, text='課程代碼(可用,分隔連續輸入) \n ex. GENS-901-01-A4,GENS-901-01-A5').pack()
        courseInput = tk.Entry(leftFormFrame, width=15)
        courseInput.pack()
        
        def addCourse():
            getCODE = courseInput.get().replace(" ", "").split(',')
            CODE = list(set(getCODE))
            CODE.sort(key=getCODE.index)
            getWishList = wishList.get(0, 'end')
            if "" not in CODE:
                for i in CODE:
                    majr = myBot.getMajrno(i)
                    if 'error' in majr:
                        #print('課程代碼輸入有誤,或未開放此課程代碼')
                        logBox.insert('end', nowTime() + ' :課程代碼<' + i +'>輸入有誤,或未開放此課程代碼\n')
                        logBox.see('end')
                        return
                    if i not in getWishList :
                        wishList.insert('end', i)
                        #myBot.tkhandler(self, 'insert', i)
            else:
                tk.messagebox.showwarning(message='請輸入課程代碼！')
        addBtn = tk.Button(leftFormFrame, text="新增", state='normal', command=addCourse)
        addBtn.pack()
        
        def delCourse():
            if wishList.curselection():
                wishList.delete(wishList.curselection())
                #myBot.tkhandler(self, 'del', i)
                
        delBtn = tk.Button(leftFormFrame, text="刪除", state='normal', command=delCourse)
        delBtn.pack()
        
        def serachCourse():
            switchBtnState()
            self.T = threading.Thread(target=__serachCourse)
            self.T.setDaemon(True)
            self.T.start()
            
        
        def __serachCourse():
            self.SHOULD_TERMINATE = False
            if myDB.chkuse(ACCOUNT):
                tk.messagebox.showwarning(message='已用盡本學期小精靈幫忙次數！')
                return
            
            fixcid = wishList.get(0, 'end')
            cid = list(set(fixcid))
            cid.sort(key=fixcid.index)#set會失去排序，這裡重新恢復原list排序
            
            while len(cid) > 0 :
                for i in cid[:]:
                    if self.SHOULD_TERMINATE:
                        return
                    majr = myBot.getMajrno(i)
                    if 'error' in majr:
                        #print('課程代碼輸入有誤,或未開放此課程代碼')
                        logBox.insert('end', nowTime() + ' :課程代碼輸入有誤,或未開放此課程代碼\n')
                        logBox.see('end')
                        switchBtnState()
                        return '課程代碼輸入有誤,或未開放此課程代碼'
                    queryUrl = myBot.queryCidUrl + '?majr_no='+ majr +'&disp_cr_code=' + i + '&class_status=1'
                    #disp_cr_code 課程代碼 class_status 課程額滿狀態
                    r = (random.randint(1,5)/10)
                    t.sleep(r)
                    
                    queryHtml = myBot.session.get(queryUrl)
                    queryResult = BeautifulSoup(queryHtml.text, 'lxml')##改回
                    #queryResult = open('course.txt', 'r')
                    #f = queryResult.read()
                    #queryResult.close()
                    
                    
                    if '您尚未登入或已逾登入有效時限!' in queryHtml.text:
                        if myBot.login(ACCOUNT,PASSWORD) != True :##改回！＝
                            #print('搜尋錯誤：您尚未登入或已逾登入有效時限,重新登入失敗')
                            logBox.insert('end', nowTime() + ' :搜尋錯誤->您尚未登入或已逾登入有效時限,嘗試重新登入失敗\n')
                            logBox.see('end')
                            return '搜尋錯誤：您尚未登入或已逾登入有效時限,重新登入失敗'
                    
                    if i in queryHtml.text and queryResult.select("#BAT_NoRecords") == [] : ####改回
                    #if i in f : 
                        #print('搜尋到課程 :', i)
                        logBox.insert('end', nowTime() + ' :搜尋到課程->' + i + '\n')
                        logBox.see('end')
                        
                        if myDB.chkuse(ACCOUNT):
                            tk.messagebox.showwarning(message='已用盡本學期小精靈幫忙次數！')
                            logBox.insert('end', nowTime() + ' :搜尋錯誤->已用盡本學期小精靈幫忙次數！\n')
                            logBox.see('end')
                            return
                        
                        result = myBot.checkInCourse(i)
                        if result == True:##改回==
                            myDB.selOK(ACCOUNT, i)
                            #print('成功加選', i)
                            selectedList.insert('end', i)
                            logBox.insert('end', nowTime() + ' :加選成功' + i + '\n')
                            logBox.see('end')
                        else:
                            #print('加選失敗', i)
                            logBox.insert('end', nowTime() + ' :加選失敗' + i + ',移除此課程 ' + '\n')
                            logBox.insert('end', 'Reason:' + result + '\n')
                            logBox.see('end')
                            #return '加選失敗:' + i +' Reason: ' + result +',移除此課程'
                
                        cid.remove(i)
                        wishList.delete(wishList.get(0, 'end').index(i))
            #print('願望課程列表已清空！')
            logBox.insert('end', nowTime() + ' :願望課程列表已清空！\n')
            logBox.see('end')
            switchBtnState()
        
        sBtn = tk.Button(leftFormFrame, text="開始", state='normal', command= serachCourse)
        #lambda:serachCourse(wishList.get(0, 'end'))
        sBtn.pack()
        def stop():
            self.SHOULD_TERMINATE = True
            self.T.join()
            switchBtnState()
        kBtn = tk.Button(leftFormFrame, text="停止", state='disabled', command= stop)
        #lambda:serachCourse(wishList.get(0, 'end'))
        kBtn.pack()
        #['MILI-901-01-A1','CHI-901-01-A2','GENS-901-01-A3','GENS-901-01-A4','GENS-901-01-A4']
        #MILI-901-01-A1,MILI-901-01-A1,CHI-901-01-A2,GENS-901-01-A3,GENS-901-01-A4,GENS-901-01-A4
        
        def switchBtnState():
            if addBtn['state'] == 'normal':
                addBtn.config(state='disabled')
                delBtn.config(state='disabled')
                sBtn.config(state='disabled')
                kBtn.config(state='normal')
            else:
                addBtn.config(state='normal')
                delBtn.config(state='normal')
                sBtn.config(state='normal')
                kBtn.config(state='disabled')

if __name__ == "__main__":
    app = SHUCourserGUI()
    app.mainloop()
    


# In[ ]:





# In[ ]:




