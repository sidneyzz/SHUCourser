'''
author:sindeyzz
readmymailplz@gmail.com
2021/1/18

'''

import re
import requests
import random
import sys
import time as t
import tkinter as tk
from bs4 import BeautifulSoup

class SHUCourser:
    def __init__(self):
        
        hostNum = str(random.randint(2, 9))
        self.cid = []
        self.session = requests.Session()
        self.session.headers = {
            'Host': 'ap' + hostNum + '.shu.edu.tw', #ap 2~9
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'sec-ch-ua': '"Google Chrome";v="87", " Not;A Brand";v="99", "Chromium";v="87"',
            'sec-ch-ua-mobile': '?0',
            'Upgrade-Insecure-Requests': '1',
            'Origin': 'https://ap' + hostNum + '.shu.edu.tw',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Sec-Fetch-Dest': 'document',
            'Referer': 'https://ap' + hostNum + '.shu.edu.tw/stu2/main.aspx',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
            'Cookie':''
        }
        
        self.postData = {
            #'__EVENTTARGET': '',
            #'__EVENTARGUMENT': '',
            #'__VIEWSTATE': '',
            #'__VIEWSTATEGENERATOR': '',
            #'__EVENTVALIDATION': '',
        }
        
        self.loginUrl = 'https://ap' + hostNum + '.shu.edu.tw/stu2/login.aspx'
        self.captchaUrl = 'https://ap' + hostNum + '.shu.edu.tw/STU2/CAPTCHA.ashx'
        self.queryCidUrl = 'https://ap' + hostNum + '.shu.edu.tw/STU2/SL01.aspx'
        self.chkinCidUrl = 'https://ap' + hostNum + '.shu.edu.tw/STU2/SL02.aspx'
        self.dashbroadUrl = 'https://ap' + hostNum + '.shu.edu.tw/STU2/SL00.aspx'
        
    def login(self, sid, pwd):
        self.sid = sid
        self.pwd = pwd
        del self.session.headers['Cookie']
        self.postData.clear()
        self.session.cookies.clear()
        self.session.get(self.captchaUrl)
        loginHtml = self.session.get(self.loginUrl)
        getCookies = requests.utils.dict_from_cookiejar(self.session.cookies)# 把cookie轉成字典
        self.session.headers['Cookie'] = "ASP.NET_SessionId="+ getCookies['ASP.NET_SessionId'] + "; " + "CAPTCHA=" + getCookies['CAPTCHA']
        #將session 加入cookie中
        
        
        if '系統關閉：目前非系統開放時間!!' in loginHtml.text:
                return '系統關閉：目前非系統開放時間!'
        
        parser = BeautifulSoup(loginHtml.text, 'lxml')
        self.postData['__EVENTTARGET'] = parser.select("#__EVENTTARGET")[0]['value']
        self.postData['__EVENTARGUMENT'] = parser.select("#__EVENTARGUMENT")[0]['value']
        self.postData['__VIEWSTATE'] = parser.select("#__VIEWSTATE")[0]['value']
        self.postData['__VIEWSTATEGENERATOR'] = parser.select("#__VIEWSTATEGENERATOR")[0]['value']
        self.postData['__EVENTVALIDATION'] = parser.select("#__EVENTVALIDATION")[0]['value']
        
        self.postData.update( {
        '__EVENTTARGET':'Login_Submit',
        'Login_UserId': self.sid,
        'Login_Passwd': self.pwd,
        'LoginConfirm_Passwd': getCookies["CAPTCHA"],
        })
        
        loginResult = self.session.post(self.loginUrl, data = self.postData , headers = self.session.headers)
        showResult = BeautifulSoup(loginResult.text, 'lxml')
        
        #print(self.postData)
        #print(showResult.title.text)
        
        if  '世新大學Web選課系統' in showResult.title.text :
            print('登入成功')
            return True 
        elif showResult != None and '執行階段錯誤' not in showResult.title.text :
            #print(showResult.select("#Login_ValidationSummary")[0].get_text())
            return showResult.select("#Login_ValidationSummary")[0].get_text()
        else:
            #print(showResult.find(string = re.compile('錯誤')))
            return showResult.find(string = re.compile('錯誤'))
    
    def checkInCourse(self, cid):
    
        self.postData.clear()
        
        chkInHtml = self.session.get(self.chkinCidUrl)
        
        if '您尚未登入或已逾登入有效時限!' in chkInHtml.text:
                #print('加選錯誤：您尚未登入或已逾登入有效時限')
                return '加選錯誤：您尚未登入或已逾登入有效時限'
        
        parser = BeautifulSoup(chkInHtml.text, 'lxml')
        self.postData['__EVENTTARGET'] = parser.select("#__EVENTTARGET")[0]['value']
        self.postData['__EVENTARGUMENT'] = parser.select("#__EVENTARGUMENT")[0]['value']
        self.postData['__VIEWSTATE'] = parser.select("#__VIEWSTATE")[0]['value']
        self.postData['__VIEWSTATEGENERATOR'] = parser.select("#__VIEWSTATEGENERATOR")[0]['value']
        self.postData['__EVENTVALIDATION'] = parser.select("#__EVENTVALIDATION")[0]['value']
        
        cids = cid.split('-')
    
        courseID = {
        'REC_type_no':cids[0],
        'REC_subj_code':cids[1],
        'REC_cr_seq':cids[2],
        'REC_class_type':cids[3],
        'REC_Insert':'加選',
        }


        self.postData.update(courseID)
        chkInResult = self.session.post(self.chkinCidUrl, data = self.postData , headers = self.session.headers)
        showResult = BeautifulSoup(chkInResult.text, 'lxml')
        print(showResult.select("#REC_ValidationSummary")[0].get_text())#加選學科已經存在/衝堂，加選失敗!!＊
        
        #try:
        if  '加選成功' in chkInResult.text :
            return True
        else:
            return showResult.select("#REC_ValidationSummary")[0].get_text()
                
        #except:
              #print("Unexpected error:", sys.exc_info()[0])
        
    def serachCourse(self,fixcid):
        
        cid = list(set(fixcid))
        cid.sort(key=fixcid.index)#set會失去排序，這裡重新恢復原list排序
        
        while len(cid) > 0:
            for i in cid[:]:
                majr = self.getMajrno(i)
                if 'error' in majr:
                    #print('課程代碼輸入有誤,或未開放此課程代碼')
                    return '課程代碼輸入有誤,或未開放此課程代碼'
                
                queryUrl = self.queryCidUrl + '?majr_no='+ majr +'&disp_cr_code=' + i + '&class_status=1'
                #disp_cr_code 課程代碼 class_status 課程額滿狀態
                r = (random.randint(1,5)/10)
                t.sleep(r)
                
                queryHtml = self.session.get(queryUrl)
                queryResult = BeautifulSoup(queryHtml.text, 'lxml')
                '''
                if '您尚未登入或已逾登入有效時限!' in queryHtml.text:
                    if self.login(self.sid, self.pwd) != True :
                        return '搜尋錯誤：您尚未登入或已逾登入有效時限,重新登入失敗'
                        '''
                #cid[i] in queryHtml.text and queryResult.select("#BAT_NoRecords") == []
                if True :
                    print('搜尋到課程 :',i)
                    result = self.checkInCourse(i)
                    if result == True:
                        #print('成功加選',i)
                        return '成功加選:' + i
                    else:
                        #print('加選失敗',i)
                        return '加選失敗:' + i +' Reason: ' + result +',移除此課程'
                    
                    cid.remove(i)
        print('願望課程列表已清空！')
        
    def getMajrno(self,cid):
        tar = cid.split('-')[0]
        majr = self.cData(tar)
        return majr
    
    def cData(self,var):
        return {
            'GENS': 'A00',
            'JOUR': 'A01',
            'RTF': 'A03',
            'GRP': 'A04',
            'PRAD': 'A05',
            'SPCM': 'A06',
            'INFO': 'A07',
            'MULT': 'A08',
            'CMD': 'A21',
            'INF': 'A22',
            'FIN': 'A23',
            'PPM': 'A24',
            'TOUR': 'A25',
            'ECON': 'A26',
            'DBA': 'A27',
            'SOPS': 'A31',
            'ENG': 'A32',
            'CHI': 'A33',
            'JALL': 'A34',
            'LAW': 'A40',
            'MILI': 'A98',
            'SPE': 'A99',
        }.get(var,'error')
    
    def tkhandler(gui, req, parm):
        pass