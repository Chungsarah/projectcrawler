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
urlmomo='https://www.momoshop.com.tw/main/Main.jsp'
db_setting={
    "host":"localhost",
    "port":3306,
    "user":"root",
    "password":"Ah03Da11La02",
    "db":"goods",
    "charset":"utf8"
}

driver.get(urlmomo)
driver.maximize_window()
time.sleep(2)
#等待元素出現
WebDriverWait(driver,5).until(EC.presence_of_all_elements_located((By.XPATH,'//*[@id="keyword"]')))
#搜尋商品名稱(越仔細越好)
#找到搜尋框
find_search=driver.find_element(By.XPATH,'//*[@id="keyword"]')
print('找到搜尋框')
#輸入商品名稱
find_search.send_keys('sony 手機'+Keys.ENTER)
print('輸入商品名稱')
print('搜尋')
time.sleep(5)
#找到價格範圍框//*[@id="priceS"]
WebDriverWait(driver,2).until(EC.presence_of_all_elements_located((By.XPATH,'//*[@id="priceS"]')))
find_priceS=driver.find_element(By.XPATH,'//*[@id="priceS"]')
print('找到價格範圍框')
#下限輸入3000
find_priceS.send_keys('3000')
print('下限輸入3000')
#確認價格
WebDriverWait(driver,2).until(EC.presence_of_all_elements_located((By.CLASS_NAME,'priceBtn')))
find_pricebtn=driver.find_element(By.CLASS_NAME,'priceBtn')
find_pricebtn.click()
print('確認價格')
#爬符合的商品資料
time.sleep(3)
find_page=driver.find_element(By.CLASS_NAME,'page-number').text
number=find_page.split("/")
last_page=int(number[-1])#<span class="page-number">頁數<b>1</b>/3</span>
print(last_page)
time.sleep(5)
#確認頁數
pagecounter=1
datas={}
momodatas=[]
while pagecounter<=last_page:
    WebDriverWait(driver,2).until(EC.presence_of_all_elements_located((By.CLASS_NAME,'listAreaUl')))#<ul class="listAreaUl
    time.sleep(2)
    product=driver.find_element(By.CLASS_NAME,'listAreaUl')
    products=product.find_elements(By.CLASS_NAME,'listAreaLi')
    #爬頁面商品
    for select in products:
        link=select.find_element(By.CLASS_NAME,'goods-img-url').get_attribute('href')
        title=select.find_element(By.CLASS_NAME,'prdName').text
        money=select.find_element(By.CLASS_NAME,'price')
        price=money.find_element(By.XPATH,'./b').text
        datas={"link":link,"title":title,"price":price}
        momodatas.append(datas)
        #放入list
    try:
        control=driver.find_element(By.CLASS_NAME,'page-control')
        next_page=control.find_element(By.CLASS_NAME,'page-btn.page-next')
        next_page.click()
    except:
        print('最後一頁了')
    pagecounter+=1
try:
    # 建立Connection物件
    conn = pymysql.connect(**db_setting)
    # 建立Cursor物件
    with conn.cursor() as cursor:
        clear="TRUNCATE TABLE momo"
        command = "INSERT INTO momo(momolink, momoname,momoprice)VALUES(%s, %s,%s)"
        cursor.execute(clear)
        for inputdata in momodatas:
            cursor.execute(command,(inputdata["link"],inputdata["title"],inputdata["price"]))    
        conn.commit()
except Exception as ex:
    print(ex)


