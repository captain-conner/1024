
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time
import re
import datetime
from bs4 import BeautifulSoup

def catch_links():

    #由于1024游客限制100页,所以默认就抓100页了
    browser = webdriver.Firefox(executable_path="/home/conner/Desktop/python/1024/driver/geckodriver")
    #url = "http://dz.x8h.biz/thread0806.php?fid=21&search=&page=100"
    all_links = []
    for x in range(2,101):
        url = 'http://dz.x8h.biz/thread0806.php?fid=21&search=&page=' + str(x)

        browser.get(url)


        soup = BeautifulSoup(browser.page_source, "lxml")
        #图片下载
        linklist = []

        for links in soup.find_all('td',style="text-align:left;padding-left:8px"):
            img_srcs= links.find_all('a')
            for each_href in img_srcs:
                href = "http://dz.x8h.biz/" + each_href.get("href")
                linklist.append(href)

        print(linklist)
        all_links.extend(linklist)
    return all_links


catch_links()
