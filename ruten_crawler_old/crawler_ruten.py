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
urlruten='https://www.ruten.com.tw/?srsltid=AfmBOoot3yoK7YQae_xsKIBfmV-__iKmT302dQkeDQkyCG8SmGkS4SWI'
db_setting={
    "host":"localhost",
    "port":3306,
    "user":"root",
    "password":"Ah03Da11La02",
    "db":"goods",
    "charset":"utf8"
}
driver.get(urlruten)
driver.maximize_window()
time.sleep(2)
#等待元素出現
WebDriverWait(driver,5).until(EC.presence_of_all_elements_located((By.XPATH,'//*[@id="searchKeyword"]')))
#搜尋商品名稱(越仔細越好)
#找到搜尋框
find_search=driver.find_element(By.XPATH,'//*[@id="searchKeyword"]')
print('找到搜尋框')
#輸入商品名稱
find_search.send_keys('sony 手機'+Keys.ENTER)
print('輸入商品名稱')
print('搜尋')
time.sleep(3)
#找到價格範圍框
WebDriverWait(driver,2).until(EC.presence_of_all_elements_located((By.CLASS_NAME,"rt-form-input")))
find_priceS=driver.find_element(By.CLASS_NAME,"rt-form-input")
print('找到價格範圍框')
#下限輸入3000
find_priceS.send_keys('3000')
print('下限輸入3000')
#確認價格
WebDriverWait(driver,2).until(EC.presence_of_all_elements_located((By.ID,'btnFilter')))
find_pricebtn=driver.find_element(By.ID,'btnFilter')
find_pricebtn.click()
while True:
    try:
        test=driver.find_element(By.CLASS_NAME,'rt-pager')
        break
    except:
        time.sleep(2)
scroll_pause_time = 2  # 每次滾動後的等待時間
last_height = driver.execute_script("return document.body.scrollHeight")  # 獲取滾動條初始高度
while True:
     # 滾動到底部
     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
     time.sleep(scroll_pause_time)  # 等待新內容加載
     # 獲取新高度並檢查是否到達底部
     new_height = driver.execute_script("return document.body.scrollHeight")
     if new_height == last_height:
        break  # 如果滾動條高度未變化，說明已經到底部
     last_height = new_height

find_pagebar=driver.find_element(By.CLASS_NAME,'rt-pager')
print('找到pagebar')
pagesnumber=[]
pages=find_pagebar.find_elements(By.CLASS_NAME,'rt-pager-button')
for page in pages:
    try:
        pagenum=page.text
        pagesnumber.append(int(pagenum))
    except:
        continue

#確認頁數
last_page=pagesnumber[-1]
print(last_page)
pagecounter=1
datas={}
rutendatas=[]
skipcounter=0
while pagecounter<=last_page:
    time.sleep(2)
    while True:
     # 滾動到底部
     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
     time.sleep(scroll_pause_time)  # 等待新內容加載
     # 獲取新高度並檢查是否到達底部
     new_height = driver.execute_script("return document.body.scrollHeight")
     if new_height == last_height:
        break  # 如果滾動條高度未變化，說明已經到底部
     last_height = new_height
    time.sleep(2)
    WebDriverWait(driver,2).until(EC.presence_of_all_elements_located((By.XPATH,'/html/body/div[1]/div[1]/main/div[2]/div/div[2]/div[2]/div[3]/div')))
    allproduct=driver.find_element(By.XPATH,'/html/body/div[1]/div[1]/main/div[2]/div/div[2]/div[2]/div[3]/div')
    product=allproduct.find_elements(By.CLASS_NAME,'product-item')
    print(product)#檢查有沒有抓到elements
    for select in product:
        try:
            link=select.find_element(By.CLASS_NAME,'rt-product-card-name-wrap').get_attribute('href')
            title=select.find_element(By.CLASS_NAME,'rt-product-card-name').text
            price=select.find_element(By.CLASS_NAME,'rt-text-price.rt-text-bold.text-price-dollar').text
            datas={"link":link,"title":title,"price":price}
            rutendatas.append(datas)
        except:
            skipcounter=skipcounter+1
            print("跳過商品第"+str(skipcounter)+"次")
    try:
        control=driver.find_element(By.CLASS_NAME,'rt-pagination-icon-button.rt-button.rt-button-text.rt-ml-2x')
        control.click()
    except:
        print('最後一頁了')
    pagecounter+=1
print(rutendatas)#抓到的資料
"""用來存入資料庫的程式
try:
    # 建立Connection物件
    conn = pymysql.connect(**db_setting)
    # 建立Cursor物件
    with conn.cursor() as cursor:
        clear="TRUNCATE TABLE ruten"
        command = "INSERT INTO ruten(rutenlink, rutenname,rutenprice)VALUES(%s, %s,%s)"
        cursor.execute(clear)
        for inputdata in rutendatas:
            try:
             cursor.execute(command,(inputdata["link"],inputdata["title"],inputdata["price"]))    
            except:
                print(inputdata["link"],inputdata["title"],inputdata["price"])
                continue
        conn.commit()
except Exception as ex:
    print(ex)
"""