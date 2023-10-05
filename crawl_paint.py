import requests
import nest_asyncio
import asyncio
import pyppeteer
from pyppeteer import launch
from pyppeteer_stealth import stealth
from bs4 import BeautifulSoup
from datetime import datetime
import time
import pandas as pd

async def main():
    browser = await launch({'headless':True})
    page = await browser.newPage()
    
    await stealth (page)
    await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36')
    await page.goto(url)
    
    ## Get HTML
    html = await page.content()
    await browser.close()
    return html

nest_asyncio.apply()
start_time = time.time()
df = pd.DataFrame()
material_bangunan = ['cat%20kayu','cat%20pelapis','cat%20semprot','cat%20tembok','kuas%20cat','plamir','roller%20cat','thinner','wallpaper']
for n,subcat in enumerate(material_bangunan):
    for page in range(1,11):
        url = 'https://www.tokopedia.com/search?navsource=&page={}&q={}&sc=4079&srp_component_id=04.06.00.00&srp_page_id=&srp_page_title=&st=&fcity=144,146,150,151,167,168,171,174,175,176,177,178,179,463,174,175,176,177,178,179,165,156'.format(page,subcat)
        print('crawling {}/{} subcategory cat'.format(n+1, len(material_bangunan)))
        print('crawling {} page {} ...'.format(subcat, page))
        html_response = asyncio.get_event_loop().run_until_complete(main())
        
        ## Load HTML Response Into BeautifulSoup
        soup = BeautifulSoup(html_response, "html.parser")

        lst = []
        for item in soup.find_all("div", class_="css-llwpbs"):
            try:
                nama_produk = item.find_all("div", class_="css-3um8ox")[0].text
                harga = item.find_all("div", class_="css-h66vau")[0].text.replace('Rp', '').replace('.', '')
                kota = item.find_all("span", class_="css-1kdc32b")[0].text
                toko = item.find_all("span", class_="css-1kdc32b")[1].text
                rating_produk = item.find_all("span", class_="css-t70v7i")[0].text 
                terjual = item.find_all("span", class_="css-1sgek4h")[0].text.replace('Terjual ','')
                url = item.find_all("a", class_="css-gwkf0u")[0].get('href')

                d = datetime.now()

                lst.append({'nama_produk' : nama_produk,
                        'harga' : harga,
                        'kota' : kota,
                        'toko' : toko,
                        'rating_produk' : rating_produk,
                        'terjual' : terjual,
                        'url_produk' : url,
                        'get_date' : time.strftime('%Y-%m-%d %H:%M:%S')})
            except:
                pass
                # print('-------page {} failed ---------'.format(page))
                # print('-------failed------------')
        df_temp = pd.DataFrame(lst)
        df_temp['subcat'] = subcat
        # print(df_temp)
        df = pd.concat([df,df_temp])
        if len(df) <= 3:
            print('data crawling is failed, maybe the website changes its format ...')
        else:
            pass
df.to_csv('result_crawl_{}_cat.csv'.format(time.strftime('%Y_%m_%d_%H_%M_%S')),index=False)
print("data cat for {} is done".format(time.strftime('%Y_%m_%d')))
print("--- %s minutes processing time ---" % (int(time.time() - start_time)/60))