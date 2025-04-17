import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pymysql
import time
driver = webdriver.Chrome()    # 指向 chromedriver 的位置
urlpchome='https://24h.pchome.com.tw/?utm_source=google&utm_medium=cpc&utm_campaign=awo_mkt_conversion_n3c_all_all_gg_pmax_mix_mktcampaign&gad_source=1&gclid=Cj0KCQiA_Yq-BhC9ARIsAA6fbAjK5ebttgSVf5N8XE01ycPc1IXhO8csNkk59OycY8DT4kGhwkrbWIAaAiNPEALw_wcB'
db_setting={
    "host":"localhost",
    "port":3306,
    "user":"root",
    "password":"Ah03Da11La02",
    "db":"goods",
    "charset":"utf8"
}
#pchome
driver.get(urlpchome)
driver.maximize_window()
time.sleep(2)
#等待元素出現
WebDriverWait(driver,5).until(EC.presence_of_all_elements_located((By.CLASS_NAME,'c-search__input')))
#搜尋商品名稱(越仔細越好)
#找到搜尋框
find_search=driver.find_element(By.CLASS_NAME,'c-search__input')
print('找到搜尋框')
#輸入商品名稱
find_search.send_keys('switch'+Keys.ENTER)
print('輸入商品名稱')
print('搜尋')
time.sleep(3)
#找到價格範圍框
WebDriverWait(driver,2).until(EC.presence_of_all_elements_located((By.CLASS_NAME,'c-input__inner')))
find_priceS=driver.find_element(By.CLASS_NAME,'c-input__inner')
print('找到價格範圍框')
#下限輸入3000
find_priceS.send_keys('3000')
print('下限輸入3000')
#確認價格
WebDriverWait(driver,2).until(EC.presence_of_all_elements_located((By.XPATH,'/html/body/div[1]/main/div[1]/div/div/section[2]/div/div/section/div/div[2]/div[2]/div[1]/div/div[1]/div/ul[2]/li[3]/button')))
find_pricebtn=driver.find_element(By.XPATH,'/html/body/div[1]/main/div[1]/div/div/section[2]/div/div/section/div/div[2]/div[2]/div[1]/div/div[1]/div/ul[2]/li[3]/button')
find_pricebtn.click()
time.sleep(3)
#爬符合的商品資料

find_pagebar=driver.find_element(By.CLASS_NAME,'c-pagination__pagesBar')
print('找到pagebar')
list_page=[]
pages=find_pagebar.find_elements(By.CLASS_NAME,'c-pagination__item')
for page in pages:
    try:
        pagetext=page.find_element(By.XPATH,'./a').text
        pagenumber=int(pagetext)
        list_page.append(pagenumber)
    except:
        nullnum=0
        list_page.append(nullnum)
#確認頁數
last_page=list_page[-1]
pagecounter=1
datas={}
pchomedatas=[]
skipcounter=0
while pagecounter<=last_page:
    time.sleep(5)
    WebDriverWait(driver,2).until(EC.presence_of_all_elements_located((By.CLASS_NAME,'c-listInfoGrid__body')))
    allproduct=driver.find_element(By.CLASS_NAME,'c-listInfoGrid__body')
    product=allproduct.find_elements(By.XPATH,'./ul')
    for body in product:
        products=body.find_elements(By.XPATH,'./li')  
        #爬頁面商品
        for select in products:
            try:
                link=select.find_element(By.XPATH,'./div/a').get_attribute('href')
                selectp=select.find_element(By.CLASS_NAME,'c-prodInfoV2__priceBar')
                title=select.find_element(By.CLASS_NAME,'c-prodInfoV2__title').text
                price=selectp.find_element(By.XPATH,'./div/div[1]').text
                datas={"link":link,"title":title,"price":price}
                pchomedatas.append(datas)
            except:
                skipcounter=skipcounter+1
                print("跳過商品第"+str(skipcounter)+"次")

        #放入list
    try:
        control=driver.find_element(By.CLASS_NAME,'c-pagination__button.is-next')
        control.click()
    except:
        print('最後一頁了')
    pagecounter+=1
try:
    # 建立Connection物件
    conn = pymysql.connect(**db_setting)
    # 建立Cursor物件
    with conn.cursor() as cursor:
        clear="TRUNCATE TABLE pchome"
        command = "INSERT INTO pchome(pchomelink, pchomename,pchomeprice)VALUES(%s, %s,%s)"
        cursor.execute(clear)
        for inputdata in pchomedatas:
            cursor.execute(command,(inputdata["link"],inputdata["title"],inputdata["price"]))    
        conn.commit()
except Exception as ex:
    print(ex)


