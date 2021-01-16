from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

browser = webdriver.Chrome()
wait = WebDriverWait(browser, 10)

def index_page(page):
    