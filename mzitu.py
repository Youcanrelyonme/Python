# coding=utf-8
import urllib2
from bs4 import BeautifulSoup
import re
import os
import socket
import sys
"""
抓取www.mzitu.com的图片
"""
reload(sys)
sys.setdefaultencoding('utf8')


def get_theme_urls(page):
    theme_urls = []
    resp = urllib2.urlopen("http://www.mzitu.com/page/"+str(page))
    html = resp.read()
    soup = BeautifulSoup(html, "lxml")
    lis = soup.find('ul', {'id': 'pins'}).find_all('li')
    for li in lis:
        theme_urls.append(li.find('a')['href'])
    return theme_urls


def get_theme_maxpage(theme_url):
    resp = urllib2.urlopen(theme_url)
    html = resp.read()
    soup = BeautifulSoup(html, "lxml")
    max_page = soup.find('div', {'class': 'pagenavi'}).find_all(
        'a')[-2].find('span').get_text()
    return int(max_page)


def get_img_url(page_url):
    resp = urllib2.urlopen(page_url)
    html = resp.read()
    soup = BeautifulSoup(html, "lxml")
    img_url = soup.find('div', {'class': 'main-image'}
                        ).find('p').find('a').find('img')['src']
    return img_url


def get_img_urls(theme_url):
    page_number = get_theme_maxpage(theme_url)+1
    img_urls = []
    for i in range(1, page_number):
        img_urls.append(get_img_url(theme_url+'/'+str(i)))
    return img_urls


def get_theme_title(theme_url):
    resp = urllib2.urlopen(theme_url)
    html = resp.read()
    soup = BeautifulSoup(html, "lxml")
    theme_title = soup.find('h2', {'class': 'main-title'}).get_text()
    RemoveSign = re.compile(r'[\/:*?"<>|"]')
    theme_title = re.sub(RemoveSign, '', theme_title)
    return theme_title


def download_imgs(theme_url):
    img_urls = get_img_urls(theme_url)
    path1 = './妹子图'.decode('utf-8').encode('gbk')
    if not os.path.exists(path1):
        os.mkdir(path1)
    title = get_theme_title(theme_url)
    path = './妹子图/'+title
    if not os.path.exists(path):
        try:
            os.mkdir(path)
        except:
            pass
    print('正在下载：'+'-------'+title+'-------')
    for img_url in img_urls:
        img_name = path+'/'+os.path.basename(img_url)
        socket.setdefaulttimeout(10)
        headers = {
            "Host": "i.meizitu.net",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0",
            "Accept": "*/*",
            "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
            "Accept-Encoding": "gzip, deflate",
            "Referer": "http://www.mzitu.com",
            "DNT": 1,
            "Connection": "keep-alive"
        }
        try:
            req = urllib2.Request(img_url, headers=headers)
            resp = urllib2.urlopen(req)
            data = resp.read()
            f = open(img_name, 'wb+')
            f.write(data)
            f.close()
        except:
            print('下载'+img_name+'失败')
    print('下载完成: '+'-------'+title+'-------')


def page_range(a=1, b=198):
    try:
        a = int(sys.argv[1])
        b = int(sys.argv[2])
    except:
        pass
    c = [a, b]
    return c


try:
    a=sys.argv[1]
    download_imgs(a)
except:
    page = page_range()
    for page in range(page[0], page[1]):
        theme_urls = get_theme_urls(page)
        for theme_url in theme_urls:
            download_imgs(theme_url)
print("-------------- 指定妹子图片下载完成 ---------------".decode('utf-8').encode('gbk'))
