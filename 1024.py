#caoliu的主要功能区:
#亚洲无码原创区 亚洲有码原创区 欧美原创区 动漫原创区域 HTTP下载区域

'''
python 3.x中urllib库和urilib2库合并成了urllib库。。
其中urllib2.urlopen()变成了urllib.request.urlopen()
    urllib2.Request()变成了urllib.request.Request()
'''
import os
import re
import time
from bs4 import BeautifulSoup
import random
from PIL import Image
import urllib.request #urllib2.urlopen()使用
import numpy as np
from selenium import webdriver
import requests
#模拟头文件
my_headers=["Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0"
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
"Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)"
]

#这是我当时用的代理IP，请更新能用的IP
proxy_list=[
    '121.40.108.76:80',
    '101.200.144.37:3128',
    '121.18.230.46:8088',
    '202.202.90.20:8080',
    '211.140.151.220:80',
    '115.182.92.87:8080',
    '122.70.135.102:80',
    '210.51.21.234:80',
    '123.59.55.122:80',
    '221.211.110.34:3128',
        ]


#截取html代码
def getHtml(url,headers):

    #proxy = random.choice(proxy_list)
    #urlhandle   = urllib.request.ProxyHandler({'http':proxy})
    #opener      = urllib.request.build_opener(urlhandle)
    #urllib.request.install_opener(opener)



    randdom_header=random.choice(headers)
    req=urllib.request.Request(url)
    req.add_header("User-Agent","Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/55.0.2883.87 Chrome/55.0.2883.87 Safari/537.36")
    req.add_header("Host","dz.x8h.biz")
    req.add_header("Referer","http://dz.x8h.biz/thread0806.php?fid=21")
    req.add_header("GET",url)
    req.add_header("Accept","text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8")
    content=urllib.request.urlopen(req,timeout=3).read()
    #content = content.decode('utf-8')
    #content = content.decode('utf-8')
    return content


#抓取版块内100页地址 返回所有链接
def getAllLinks():

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


#下载图片(BeautifulSoup 方法) 返回 [addresslist,imglist] 应该返回的是 [{"名称":地址}] 后面再改吧
def getImage_and_address(html):
    browser = webdriver.Firefox(executable_path="/home/conner/Desktop/python/1024/driver/geckodriver")
    #options = webdriver.ChromeOptions()
    #options.add_argument("--test-type")
    #browser = webdriver.Chrome(executable_path="/home/conner/Desktop/python/1024/driver/chromedriver",chrome_options=options)

    browser.get(html)
    soup = BeautifulSoup(browser.page_source, "lxml")
    #图片下载
    imglist = []
    addresslist = []
    #进行查询,因为图片和下载链接是包含在div标签中.
    for Imgs in soup.find_all('div',class_="tpc_content do_not_catch"):
        img_srcs= Imgs.find_all('img')
        address_href = Imgs.find_all('a')

        for eachsrc in img_srcs:
            imglist.append(eachsrc.get("src"))

        for href in address_href:
            addresslist.append(href.get('href'))
    print(imglist)
    print("地址是:")
    print(addresslist)
    #content = requests.get(big_img_url).content
    os.chdir(os.path.join(os.getcwd(), 'images'))
    x = 0
    for imgurl in imglist:
        content = requests.get(imgurl).content
        filename = "%d.jpg" % x
        with open(filename, "wb") as f:
                f.write(content)
        x+=1


    return [addresslist,imglist]


#横向合成图片 参数 :files文件名集合 output_file合成的文件名
def mergei(files, output_file):
    tot = len(files)
    img = Image.open(files[0])
    #合成底片的大小,默认第一张,可自定义.
    #w, h = img.size[0], img.size[1]
    w = 800;h = 600
    merge_img = Image.new('RGB', (w * tot, h), 0xffffff)
    i = 0
    for f in files:
        print(f)
        img = Image.open(f)
        merge_img.paste(img, (i, 0))
        i += w
    merge_img.save(output_file)


#第二种合成方法 参数: files图片的名字集合
def merge(files):

    num=len(files)

    filename_lens=[len(x) for x in files] #length of the files
    min_len=min(filename_lens) #minimal length of filenames
    max_len=max(filename_lens) #maximal length of filenames
    if min_len==max_len:#the last number of each filename has the same length
        files=sorted(files) #sort the files in ascending order
    else:#maybe the filenames are:x_0.png ... x_10.png ... x_100.png
        index=[0 for x in range(num)]
        for i in range(num):
            filename=files[i]
            start=filename.rfind('_')+1
            end=filename.rfind('.')
            file_no=int(filename[start:end])
            index[i]=file_no
        index=sorted(index)
        files=[str(x)+'.jpeg' for x in index]

    print(files[0])
    baseimg=Image.open(files[0])
    sz=baseimg.size
    basemat=np.atleast_2d(baseimg)
    for i in range(1,num):
        file=files[i]
        im=Image.open(file)
        im=im.resize(sz,Image.ANTIALIAS)
        mat=np.atleast_2d(im)
        print(file)
        basemat=np.append(basemat,mat,axis=0)
    final_img=Image.fromarray(basemat)
    final_img.save('merged.png')


#地址写入html
def address_to_HTML(address_list):

    os.chdir(os.path.pardir)
    print("现在的目录是 %s" % os.getcwd())
    file = open("model.html")
    content = file.read()
    old_content = content.split('\n')
    for address in address_list:
        a = '<a href="' + address + '">baidu</a>'
        old_content.insert(6, a)

    new_content = '\n'.join(old_content)
    file.close()
    file = open("address.html",'w')
    file.write(new_content)
    file.close()


#老司机开车,坐稳了.
def Old_drivers_drive():
    getAllLinks()
    for link in getAllLinks():
        getImage_and_address(link)


#----------------------------------------------
'''
目的,直接浏览所有离线图片,省去翻页烦恼.找到对应地址,点击就能下载 啊西吧.
1获取抓取的版块的首地址
2对版块的图片进行截取,以及图片下方的bt地址
3对每个视频版块合成图片
4对每个bt写入html地址.

'''


addresslistANDimglist = getImage_and_address("http://dz.x8h.biz/htm_data/2/1701/2213536.html")

arr = []
for x in range(len(addresslistANDimglist[1])):
    arr.append("%d.jpg" % x)

#arr = ["0.jpg","1.jpg","2.jpg","3.jpg","4.jpg",]
mergei(arr,"m.png")

#address_to_HTML(address_list)
