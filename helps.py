import os
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from urllib.parse import quote
from pyquery import PyQuery as pq

from store import save_to_mongo

KEYWORD = os.getenv('KEYWORD')

browser = webdriver.Chrome()
wait = WebDriverWait(browser, 10)

def index_page(page):
    print(f"正在抓取第{page}页.....")

    url = os.getenv('BASE_URL') + '?q=' + quote(KEYWORD)
    
    browser.get(url)
    if page > 1:
        input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager div.form > input')))
        submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#mainsrp-pager div.form > .J_Submit')))
        input.clear()
        input.send_keys(page)
        submit.click()
    
    wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, 'ul.items > li.item.active > span'), str(page)))
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.m-itemlist .items .item')))
    get_products()


def login():
    # 设置等待
    login_wait = WebDriverWait(browser, 100)

    # 获得登陆界面
    browser.get(os.getenv('LOGIN_URL'))

    # 等待用户界面加载
    login_wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#refundList')))

def get_products():
    print('正在解析.....')

    html = browser.page_source
    doc = pq(html)
    items = doc('.m-itemlist .items > .item').items()

    for item in items:
        product = {
            'image': 'https:' + item.find('.pic img').attr('data-src'),
            'price': item.find('.price strong').text(),
            'deal': item.find('.deal-cnt').text(),
            'title': item.find('.title').text(),
            'shop': item.find('.shop').text(),
            'location': item.find('.location').text()
        }

        print('正在保存至数据库.....')
        save_to_mongo(product)
        print('保存成功！')

    
