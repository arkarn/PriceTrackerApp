from selenium import webdriver
import datetime
import time
import telegram_send
import os
import pymysql

os.system('printf "1782618485:AAGk6TxOkq0FyW7YWlpDu5lo3aAnszd_uDM\npub\nt.me/amazPT" | telegram-send --configure-channel')

def get_driver():
    """Start web driver"""
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.implicitly_wait(10)
    return driver

def fetch_table():
    rows = []
    conn = pymysql.connect(host='mysqldb', port=3306, user='root', passwd='password', db='proddb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM product")
    for r in cur:
        rows.append(r)
    cur.close()
    conn.close()
    print(f"rows={rows}")
    return rows


# chromeWebDriverPath = './chromedriver'
# priceXPath = '//*[@id=\"priceblock_ourprice\"]'
priceXPath = '//*[@id="tp-tool-tip-price"]/span[2]/span[3]/*'
# priceXPath2 = '//*[@id="tp_price_block_total_price_ww"]/span[1]'

# driver = webdriver.Chrome('/Users/ashish.ranjan/Documents/chromedriver')
driver = get_driver()  # use this if using docker
# productFile = open('products.txt', 'r')
# Lines = productFile.readlines()


import re
import locale
def clean_price_string(s):
    decimal_point_char = locale.localeconv()['decimal_point']
    clean = re.sub(r'[^0-9'+decimal_point_char+r']+', '', str(s))
    return float(clean)

# outputFile = open('prices.txt', 'a')
telegram_send.send(messages=["deployed model..."])
while True:
    for productName, productUrl, productThresh in fetch_table():
        print(f"got {productName}, {productUrl}, {productThresh}")
        try:
            driver.get(productUrl)
            print('got producturl')
            element = driver.find_element_by_xpath(priceXPath)
            # element2 = driver.find_element_by_xpath(priceXPath2)
            print(f"element = {element}")
            print(f"element = {element.text}")
            print(f"cleaned element = {clean_price_string(element.text)}")
            # print(f"element2 = {element2}")
            # print(f"element2 = {element2.text}")
            # print(f"cleaned element2 = {clean_price_string(element2.text)}")
            price = float(clean_price_string(element.text))  #element.text.split(' ')[1]
            if price <= productThresh:
                telegram_send.send(messages=[str(productName) + ': ' + str(price)])
            print(productName, price)
        except Exception as e:
            print(e)
            pass
        # outputFile.write(str(datetime.datetime.now()) + ': ' + productName+'@'+str(price)+'\n')
    time.sleep(30)

# productFile.close()
# outputFile.close()
driver.close()

