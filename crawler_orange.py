import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
driver = webdriver.Chrome()    # 指向 chromedriver 的位置
urlmomo='https://www.momoshop.com.tw/main/Main.jsp'
urlpchome='https://24h.pchome.com.tw/?utm_source=google&utm_medium=cpc&utm_campaign=awo_mkt_conversion_n3c_all_all_gg_pmax_mix_mktcampaign&gad_source=1&gclid=Cj0KCQiA_Yq-BhC9ARIsAA6fbAjK5ebttgSVf5N8XE01ycPc1IXhO8csNkk59OycY8DT4kGhwkrbWIAaAiNPEALw_wcB'
urlorange='https://shopping.gamania.com/index.html'
urletmall='https://www.etmall.com.tw/?utm_source=google&utm_medium=cpc&utm_campaign=etmall&gad_source=1&gclid=Cj0KCQiA_Yq-BhC9ARIsAA6fbAhHZXNWmODZxQG0k8_ocHq64SpfOm6LwuRtQCUIgkZHMMeUuDJdNzcaAiigEALw_wcB'
urlcoupang='https://www.tw.coupang.com/?pageType=HOME&pageValue=HOME&wPcid=17408893188390465333865&wRef=www.google.com&wTime=20250302122158&redirect=landing&mcid=ebe32247d79c4640a695a0ee80addd02&src=1043016&campaignid=19736900821&spec=10304001&network=g&addtag=900&lptag=%E7%81%AB%E7%AE%AD%E9%80%9F%E9%85%8D&link_click_id=1407616168912724060&gclid=Cj0KCQiA_Yq-BhC9ARIsAA6fbAj0E2eLDbwgm4vMF63gQXgA3W5PV_8BrE2-09U1d0Oa6AXdizrDMIsaAsxyEALw_wcB&adgroupid=143668844582&gbraid=&ctag=home&campaign=SA_GSA_BRA_WEB_REA_NAT&adgroup=Coupang_ZH_e'
urlruten='https://www.ruten.com.tw/?srsltid=AfmBOoot3yoK7YQae_xsKIBfmV-__iKmT302dQkeDQkyCG8SmGkS4SWI'
"""
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
WebDriverWait(driver,2).until(EC.presence_of_all_elements_located((By.XPATH,'/html/body/div[1]/div[4]/div[3]/section/div[2]/a')))
find_pricebtn=driver.find_element(By.XPATH,'/html/body/div[1]/div[4]/div[3]/section/div[2]/a')
find_pricebtn.click()
print('確認價格')
#爬符合的商品資料
find_page=driver.find_element(By.XPATH,'/html/body/div[1]/div[4]/div[2]/div/div[1]/span[2]').text[-1]
last_page=int(find_page)
time.sleep(5)
#確認頁數
pagecounter=1
href=[]
titles=[]
prices=[]
while pagecounter<=last_page:
    WebDriverWait(driver,2).until(EC.presence_of_all_elements_located((By.XPATH,'/html/body/div[1]/div[4]/div[3]/div')))
    time.sleep(2)
    product=driver.find_element(By.XPATH,'/html/body/div[1]/div[4]/div[3]/div')
    products=product.find_elements(By.CLASS_NAME,'listAreaLi')
    #爬頁面商品
    for select in products:
        link=select.find_element(By.CLASS_NAME,'goods-img-url').get_attribute('href')
        title=select.find_element(By.CLASS_NAME,'prdName').text
        money=select.find_element(By.CLASS_NAME,'price')
        price=money.find_element(By.XPATH,'./b').text
        href.append(link)
        titles.append(title)
        prices.append(price)
        #放入list
    try:
        control=driver.find_element(By.CLASS_NAME,'page-control')
        next_page=control.find_element(By.CLASS_NAME,'page-btn page-next')
        next_page.click()
    except:
        print('最後一頁了')
    pagecounter+=1


momodata={'href':href,'titles':titles,'prices':prices}
momodata_df=pd.DataFrame(momodata)
momodata_df.to_csv('momodata_df.csv',index=False)

time.sleep(3)
"""
#pchome
driver.get(urlpchome)
driver.maximize_window()
time.sleep(2)
#等待元素出現
WebDriverWait(driver,5).until(EC.presence_of_all_elements_located((By.CLASS_NAME,'c-search__input')))
#搜尋商品名稱(越仔細越好)
#找到搜尋框
find_search=driver.find_element(By.CLASS_NAME,'c-search__input')
print('找到搜尋框')#<input autocomplete="off" aria-autocomplete="list" aria-controls="react-autowhatever-1" class="c-search__input" placeholder="iphone 16e" type="search" value="sony 手機">
#輸入商品名稱
find_search.send_keys('sony 耳機'+Keys.ENTER)
print('輸入商品名稱')
print('搜尋')
time.sleep(5)
#找到價格範圍框
WebDriverWait(driver,2).until(EC.presence_of_all_elements_located((By.CLASS_NAME,'c-input__inner')))
find_priceS=driver.find_element(By.CLASS_NAME,'c-input__inner')
print('找到價格範圍框')#<input placeholder="最低價" class="c-input__inner" maxlength="8" inputmode="numeric" type="text" value="">
#下限輸入3000
find_priceS.send_keys('3000')
print('下限輸入3000')
#確認價格
WebDriverWait(driver,2).until(EC.presence_of_all_elements_located((By.XPATH,'/html/body/div[1]/main/div[1]/div/div/section[2]/div/div/section/div/div[2]/div[2]/div[1]/div/div[1]/div/ul[2]/li[3]/button')))
find_pricebtn=driver.find_element(By.XPATH,'/html/body/div[1]/main/div[1]/div/div/section[2]/div/div/section/div/div[2]/div[2]/div[1]/div/div[1]/div/ul[2]/li[3]/button')
find_pricebtn.click()#<button class="btn btn--smAuto gtmClickV2" type="button" tabindex="0"><span class="btn__outLine btn__outLine--grayDarkestSelect"><span class="btn__text">確定</span></span></button>
time.sleep(5)
#爬符合的商品資料

find_pagebar=driver.find_element(By.CLASS_NAME,'c-pagination__pagesBar')
print('找到pagebar')
list_page=[]
pages=find_pagebar.find_elements(By.CLASS_NAME,'c-pagination__item')#<li class="c-pagination__item"><a class="c-pagination__link" href="/search/?q=%E5%90%89%E4%BB%96&amp;srsltid=AfmBOoqexD6sdJdlC43WZkEey6_gQRNtLrlIZu4OweT7ZMcIEu2QmoDw&amp;min=3000&amp;p=1">1</a></li>
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
href=[]
titles=[]
prices=[]
while pagecounter<=last_page:
    time.sleep(5)
    WebDriverWait(driver,2).until(EC.presence_of_all_elements_located((By.CLASS_NAME,'c-listInfoGrid__body')))
    allproduct=driver.find_element(By.CLASS_NAME,'c-listInfoGrid__body')#<ul class="c-listInfoGrid__list c-listInfoGrid__list--wrapProdCard
    product=allproduct.find_elements(By.XPATH,'./ul')
    for body in product:
        products=body.find_elements(By.XPATH,'./li')  
        #爬頁面商品 /html/body/div[1]/main/div[1]/div/div/section[2]/div/div/section/div/div/div[2]/div[1]/div/div/ul[1]/li[1]
        for select in products:#/html/body/div[1]/main/div[1]/div/div/section[2]/div/div/section/div/div/div[2]/div[1]/div/div/ul[1]/li[1]/div/a
            link=select.find_element(By.XPATH,'./div/a').get_attribute('href')
            selectp=select.find_element(By.CLASS_NAME,'c-prodInfoV2__priceBar')
            title=select.find_element(By.CLASS_NAME,'c-prodInfoV2__title').text
            price=selectp.find_element(By.XPATH,'./div/div[1]').text
            href.append(link)#/div/div[2]/div[1]/div[3]/div/div
            titles.append(title)
            prices.append(price)
        #放入list
    try:#<div class="c-pagination__button is-next"><button class="btn btn--sm gtmClickV2"
        control=driver.find_element(By.CLASS_NAME,'c-pagination__button.is-next')
        control.click()
    except:
        print('最後一頁了')
    pagecounter+=1


pchomedata={'href':href,'titles':titles,'prices':prices}
pchomedata_df=pd.DataFrame(pchomedata)
pchomedata_df.to_csv('pchomedata_df.csv',index=False)
