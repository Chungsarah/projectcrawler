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
urlcoupang='https://www.tw.coupang.com/?pageType=HOME&pageValue=HOME&wPcid=17408893188390465333865&wRef=www.google.com&wTime=20250302122158&redirect=landing&mcid=ebe32247d79c4640a695a0ee80addd02&src=1043016&campaignid=19736900821&spec=10304001&network=g&addtag=900&lptag=%E7%81%AB%E7%AE%AD%E9%80%9F%E9%85%8D&link_click_id=1407616168912724060&gclid=Cj0KCQiA_Yq-BhC9ARIsAA6fbAj0E2eLDbwgm4vMF63gQXgA3W5PV_8BrE2-09U1d0Oa6AXdizrDMIsaAsxyEALw_wcB&adgroupid=143668844582&gbraid=&ctag=home&campaign=SA_GSA_BRA_WEB_REA_NAT&adgroup=Coupang_ZH_e'
db_setting={
    "host":"localhost",
    "port":3306,
    "user":"root",
    "password":"Ah03Da11La02",
    "db":"goods",
    "charset":"utf8"
}

driver.get(urlcoupang)
driver.maximize_window()
time.sleep(2)
#等待元素出現
WebDriverWait(driver,5).until(EC.presence_of_all_elements_located((By.XPATH,'//*[@id="__next"]/div[2]/header/div/div/span[2]/div[1]/div[1]/div/input')))
#搜尋商品名稱(越仔細越好)
#找到搜尋框
find_search=driver.find_element(By.XPATH,'//*[@id="__next"]/div[2]/header/div/div/span[2]/div[1]/div[1]/div/input')
print('找到搜尋框')
#輸入商品名稱
find_search.send_keys('sony 耳機'+Keys.ENTER)
print('輸入商品名稱')
print('搜尋')
time.sleep(5)


datas={}
coupangdatas=[]
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
result=driver.find_element(By.CLASS_NAME,"SearchResult_searchResult__zAjJa")
products=result.find_elements(By.CLASS_NAME,"SearchResult_searchResultProduct___h6E9")
for product in products:
    link=product.find_element(By.XPATH,"./a").get_attribute('href')
    title=product.find_element(By.CLASS_NAME,'Product_title__8K0xk').text
    price=product.find_element(By.CLASS_NAME,'Product_salePricePrice__2FbsL').text
    datas={"link":link,"title":title,"price":price}
    coupangdatas.append(datas)


try:
    # 建立Connection物件
    conn = pymysql.connect(**db_setting)
    # 建立Cursor物件
    with conn.cursor() as cursor:
        clear="TRUNCATE TABLE coupang"
        command = "INSERT INTO coupang(coupanglink, coupangname,coupangprice)VALUES(%s, %s,%s)"
        cursor.execute(clear)
        for inputdata in coupangdatas:
            cursor.execute(command,(inputdata["link"],inputdata["title"],inputdata["price"]))    
        conn.commit()
except Exception as ex:
    print(ex)