
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
urletmall='https://www.etmall.com.tw/?utm_source=google&utm_medium=cpc&utm_campaign=etmall&gad_source=1&gclid=Cj0KCQiA_Yq-BhC9ARIsAA6fbAhHZXNWmODZxQG0k8_ocHq64SpfOm6LwuRtQCUIgkZHMMeUuDJdNzcaAiigEALw_wcB'
db_setting={
    "host":"localhost",
    "port":3306,
    "user":"root",
    "password":"Ah03Da11La02",
    "db":"goods",
    "charset":"utf8"
}

driver.get(urletmall)
driver.maximize_window()
time.sleep(2)
#等待元素出現
WebDriverWait(driver,5).until(EC.presence_of_all_elements_located((By.XPATH,'//*[@id="txtSearchKeyword"]')))
#搜尋商品名稱(越仔細越好)
#找到搜尋框
find_search=driver.find_element(By.XPATH,'//*[@id="txtSearchKeyword"]')
print('找到搜尋框')
#輸入商品名稱
find_search.send_keys('sony 耳機'+Keys.ENTER)
print('輸入商品名稱')
print('搜尋')
time.sleep(5)
#找到價格範圍框
WebDriverWait(driver,2).until(EC.presence_of_all_elements_located((By.XPATH,'//*[@id="SearchProductList"]/div/div[2]/div[1]/div/input[1]')))
find_priceS=driver.find_element(By.XPATH,'//*[@id="SearchProductList"]/div/div[2]/div[1]/div/input[1]')
print('找到價格範圍框')
#下限輸入3000
find_priceS.send_keys('3000')
print('下限輸入3000')
#確認價格
WebDriverWait(driver,2).until(EC.presence_of_all_elements_located((By.XPATH,'//*[@id="SearchProductList"]/div/div[2]/div[1]/div/button')))
find_pricebtn=driver.find_element(By.XPATH,'//*[@id="SearchProductList"]/div/div[2]/div[1]/div/button')
find_pricebtn.click()
print('確認價格')
#爬符合的商品資料
time.sleep(5)
findfinal=driver.find_element(By.CLASS_NAME,"n-pager--last.n-pager--active")
findfinal.click()
time.sleep(2)
current=driver.find_element(By.CLASS_NAME,"pagenum.sendGA.current").text
pagenumber=int(current)
time.sleep(2)
fristfinal=driver.find_element(By.CLASS_NAME,"n-pager--first")
fristfinal.click()
pagecounter=1
datas={}
etmalldatas=[]
while pagecounter<=pagenumber:
    WebDriverWait(driver,2).until(EC.presence_of_all_elements_located((By.XPATH,'//*[@id="searchResult"]')))
    time.sleep(2)
    product=driver.find_element(By.CLASS_NAME,'n-hover--img.n-m-bottom--sm.n-card__list.fun-searchResult-list')
    products=product.find_elements(By.CLASS_NAME,'product')
    #爬頁面商品
    for select in products:
        link=select.find_element(By.CLASS_NAME,'n-pic').get_attribute('href')
        title=select.find_element(By.CLASS_NAME,'n-name').text
        price=select.find_element(By.CLASS_NAME,'n-final-price').text
        datas={"link":link,"title":title,"price":price}
        etmalldatas.append(datas)
        #放入list
    try:
        next_page=driver.find_element(By.CLASS_NAME,'n-pager--active')
        next_page.click()
    except:
        print('沒找到下一頁')
    pagecounter+=1
try:
    # 建立Connection物件
    conn = pymysql.connect(**db_setting)
    # 建立Cursor物件
    with conn.cursor() as cursor:
        clear="TRUNCATE TABLE etmall"
        command = "INSERT INTO etmall(etmalllink, etmallname,etmallprice)VALUES(%s, %s,%s)"
        cursor.execute(clear)
        for inputdata in etmalldatas:
            cursor.execute(command,(inputdata["link"],inputdata["title"],inputdata["price"]))    
        conn.commit()
except Exception as ex:
    print(ex)