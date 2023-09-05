from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import bs4 as bs
import csv
from datetime import datetime
import pandas as pd

PATH = "chromedriver.exe"
driver = webdriver.Chrome(PATH)

material_bangunan = ['asbes','baja','batako','batu','batu-bata','besi','beton','engsel','gagang-Pintu','gembok','genteng','granit','grendel','jendela','kaca','kawat','kayu','keramik-lantai','kusen-pintu','lantai-kayu','paku','pasir','semen','tanah','triplek']

df = pd.DataFrame()
start_time = time.time()
for subcat in material_bangunan:
    for page in range(1,11):
        driver.get('https://www.tokopedia.com/search?navsource=&page={}&q={}&sc=4078&srp_component_id=04.06.00.00&srp_page_id=&srp_page_title=&st=&fcity=144,146,150,151,167,168,171,174,175,176,177,178,179,463,174,175,176,177,178,179,165,156'.format(page,subcat))
        driver.implicitly_wait(5)
        print('crawling {} page {} ...'.format(subcat, page))

        i = 300
        while True:
            time.sleep(0.5)
            driver.execute_script(f"window.scrollTo(0, {i});")
            new_height = driver.execute_script("return document.body.scrollHeight") 

            i += 400
            if i > new_height:
                break

        pagesource = driver.page_source
        soup = bs.BeautifulSoup(pagesource, "html.parser")

        lst = []
        for item in soup.find_all("div", class_="css-974ipl"): 
            try:
                nama_produk = item.find_all("div", class_="css-3um8ox")[0].text
                harga = item.find_all("div", class_="css-1ksb19c")[0].text.replace('Rp', '').replace('.', '')
                kota = (item.find_all("span", class_="css-1kdc32b")[0]).text
                toko = item.find_all("span", class_="css-1kdc32b")[1].text
                rating_produk = item.find_all("span", class_="css-t70v7i")[0].text 
                terjual = item.find_all("span", class_="css-1duhs3e")[0].text.replace('Terjual ','')
                url = item.find_all("a", class_="css-gwkf0u")[0].get('href')

                d = datetime.now()

                lst.append({'nama_produk' : nama_produk,
                        'harga' : harga,
                        'kota' : kota,
                        'toko' : toko,
                        'rating_produk' : rating_produk,
                        'terjual' : terjual,
                        'url_produk' : url,
                        'get_date' : d.strftime('%Y-%m-%d %H:%M:%S')})
            except:
                pass
                print('-------page {} failed ---------'.format(page))

        # print(lst)
        df_temp = pd.DataFrame(lst)
        df_temp['subcat'] = subcat
        # print(df_temp)
        df = pd.concat([df,df_temp])
df.to_csv('result_crawl_{}_material_bangunan.csv'.format(d.strftime('%Y_%m_%d_%H_%M_%S')),index=False)
print("--- %s minutes processing time ---" % (int(time.time() - start_time)/60))
print("data for {} is done".format(d.strftime('%Y_%m_%d')))
driver.close()