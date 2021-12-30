#!/usr/bin/env python
# coding: utf-8

# ## Data Crwaling

# In[ ]:


import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pandas as pd
import numpy as np

import warnings
warnings.filterwarnings(action= "ignore")

pd.options.display.max_rows=100
pd.options.display.max_columns=100


# In[ ]:


# 크롬창 열기
driver = webdriver.Chrome('./chromedriver')


# In[ ]:


list208 = pd.read_csv('list208.csv')


# In[ ]:


# 스크롤 다운 함수 정의
import datetime
    
def doScrollDown(whileSeconds):
    start = datetime.datetime.now()
    end = start + datetime.timedelta(seconds=whileSeconds)
    while True:
        itemlist = driver.find_element_by_class_name("price_body")
        driver.execute_script("arguments[0].scrollBy(0, -100)", itemlist)
        driver.execute_script("arguments[0].scrollBy(0, document.body.scrollHeight)", itemlist)
        time.sleep(1)
        if datetime.datetime.now() > end:
            break


# In[ ]:


# 크롤링 함수
def crawler(number, seconds):
    # list360 신발 선택
    url = 'https://kream.co.kr/products/{0}'.format(number)
    driver.get(url)
#     # 암시적 대기, 웹페이지 전체가 뜰때까지 대기
#     driver.implicitly_wait(5)
    # 명시적 대기, 특정 Xpath가 뜰때까지 대기
    element = WebDriverWait(driver, 8).until(EC.presence_of_element_located((By.XPATH,'//*[@id="panel1"]/div/table/tbody/tr[1]/td[3]')))
    # 이름 뽑기
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    item = soup.select('div.main_title_box > p.title')
    product_name = item[0].text
    # 컬럼 뽑기
    item = soup.select('dl.detail_product')
    cols = item[0].text.replace('\n', '').replace(' ','')
    r1 = cols.find('출시일')
    r2 = cols.find('컬러')
    r3 = cols.find('발매가')
    release_date = cols[r1+3:r2]
    color = cols[r2+2:r3]
    release_price = cols[r3+3:]
    # end_date
    end_date = soup.select('td.table_td.align_right')[1].text.replace('\n','').replace(' ','')
    # 체결 내역 더보기 클릭 (copy Xpath)
    driver.find_element_by_xpath('//*[@id="panel1"]/a').click()
    driver.find_element_by_xpath('//*[@id="panel1"]/div/div/div[1]/div/div[3]/a').click()
    # 체결 내역 더보기 스크롤 다운
    doScrollDown(seconds)
    # 데이터 추출
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    size_list = []
    price_list = []
    date_list = []
    for i in range(len(soup.select('div.body_list > div.list_txt'))):
        item = soup.select('div.body_list > div.list_txt')[i].text.replace('\n', '').replace(' ','')
        if i%3 == 0:
            size_list.append(item)
        elif i%3 == 1:
            price_list.append(item)
        elif i%3 == 2:
            date_list.append(item)
    df = pd.DataFrame({'size': size_list, 'price': price_list, 'date': date_list})
    df['product'] = product_name
    df['release_date'] = release_date
    df['color'] = color
    df['release_price'] = release_price
    file_name = product_name.replace(' ','_')
    df.to_csv('Data/{0}.csv'.format(file_name))
    if df['date'].max() == end_date :
        print('<<크롤링 완벽히 성공>>')
    print('{0} ~ {1} ({2})'.format(df['date'].min(), df['date'].max(), end_date))
    print(f'{file_name} 저장완료!')
    print('----'*10)


# In[ ]:


for i in range(len(list312['number'])):
        number = list312['number'][i]
        crawler(number, 5)
        print(f'{i}번째 {number} 크롤링 완료')
        print('===='*10)
"""
for i in range(len(list208['number'])):
    if i >= :
        number = list208['number'][i]
        crawler(number, 25)
         print(f'{i}번째 {number} 크롤링 완료')
         print('===='*10)
    else:
        continue """ 


# ### 데이터 병합 및 불러오기 

# In[ ]:


import os  
os.getcwd() # 현재 경로 확인 


# In[ ]:


path =  'Data/'
file_list = os.listdir(path)
file_list_py = [file for file in file_list if file.endswith('.csv')] ## 파일명 끝이 .csv인 경우


# In[ ]:


df = pd.DataFrame()
for i in file_list_py:
    data = pd.read_csv(path + i)
    df = pd.concat([df,data], ignore_index  = True)


# In[ ]:


df.to_csv('list_208_Data.csv')

