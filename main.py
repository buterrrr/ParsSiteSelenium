import requests
from bs4 import BeautifulSoup
import time
from selenium import webdriver
import pandas as pd


def parametrs(link):
    response = requests.get(link)
    soup = BeautifulSoup(response.text, 'lxml')
    name=eval(soup.find('script',type='application/ld+json').text)['name']
    description=eval(soup.find('script',type='application/ld+json').text)['description']
    low_price=eval(soup.find('script',type='application/ld+json').text)['offers']['lowPrice']
    high_price=eval(soup.find('script',type='application/ld+json').text)['offers']['highPrice']
    return name,description,low_price,high_price

driver = webdriver.Chrome(executable_path=r'C:\Users\Buter\PycharmProjects\ParsSamKWORK\chromedriver.exe')
driver.maximize_window()
driver.get('https://gradus72.ru/')
time.sleep(3)

responce = driver.page_source

soup = BeautifulSoup(responce, 'lxml')

category = soup.find('div', class_='sidebar-block-content').find_all('div',
                                                                     class_='dropdown__control menu-item__controls')

data=pd.DataFrame(columns=['Category','Name','high_price','low_price','discription','link'])

for item in category:
    category_name = item.find('a').text.strip()
    link_category = 'https://gradus72.ru' + item.find('a').get('href')
    driver.get(link_category)
    time.sleep(1)
    pagination=driver.page_source

    soup=BeautifulSoup(pagination, 'lxml')
    if len(soup.find_all('div',class_='grid__cell pagination__item'))==0:
        tovary = soup.find_all('div',
                               class_='grid__cell product-list__elem grid__cell_3 grid__cell_3-md grid__cell_12-xs')
        print(len(tovary))
        for j in tovary:
            link_product='https://gradus72.ru'+j.find('div',class_='grid__cell product-card__image').find('a').get('href')
            a=parametrs(link_product)
            tmp=pd.DataFrame(data=[[category_name,
                                    a[0],
                                    a[3],
                                    a[2],
                                    a[1],
                                    link_product]],
                             columns=data.columns)
            data=data.append(tmp)


    else:
        for i in range(1,int(soup.find_all('div',class_='grid__cell pagination__item')[len(soup.find_all('div',class_='grid__cell pagination__item'))-1].text.strip())+1):
            driver.get(link_category+'?page='+str(i))
            time.sleep(1)
            soup2=BeautifulSoup(driver.page_source,'lxml')
            tovary = soup.find_all('div',
                                   class_='grid__cell product-list__elem grid__cell_3 grid__cell_3-md grid__cell_12-xs')
            print(len(tovary))
            for j in tovary:
                link_product = 'https://gradus72.ru' + j.find('div', class_='grid__cell product-card__image').find('a').get('href')
                a = parametrs(link_product)
                tmp = pd.DataFrame(data=[[category_name,
                                          a[0],
                                          a[3],
                                          a[2],
                                          a[1],
                                          link_product]],
                                   columns=data.columns)
                data=data.append(tmp)

data=data.drop_duplicates().reset_index(drop=True)
data.to_excel('grad72.xls')


