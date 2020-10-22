# -*- coding:utf-8 -*-
import requests
import os
import time
from bs4 import BeautifulSoup
import base64


# 发出请求获得HTML源码
def get_html(url):
    # 指定一个浏览器头,referer 破解盗链
    headers = {"Referer": "www.mzitu.com",'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
    # 代理，免费的代理只能维持一会可能就没用了，自行更换
    proxies = {'http': '111.23.10.27:8080'}
    try:
        # Requests库的get请求
        resp = requests.get(url, headers=headers)
    except:
        # 如果请求被阻，就使用代理
        resp = requests.get(url, headers=headers, proxies=proxies)

    return resp

# 创建文件夹的函数，保存到D盘
def mkdir(path):
    # os.path.exists(name)判断是否存在路径
    # os.path.join(path, name)连接目录与文件名
    isExists = os.path.exists(os.path.join("/Users/jerry/mztu/", path))
    # 如果不存在
    if not isExists:
        print('makedir', path)
        # 创建文件夹
        os.makedirs(os.path.join("/Users/jerry/mztu/", path))
        # 切换到创建的文件夹
        os.chdir(os.path.join("/Users/jerry/mztu/", path))
        return True
    # 如果存在了就返回False
    else:
        print(path, 'already exists')
        os.chdir(os.path.join("/Users/jerry/mztu/", path))
        return False

# 获得图片地址调用download函数进行下载
def get_imgs(dir):
    # 调用函数获得所有页面
    i=1
    for url in all_page(dir):
        # path = url.split('-')[-1]
        # # 创建文件夹的函数
        # mkdir(path)
        # # 调用请求函数获得HTML源码
        html = get_html(url).text
        # print(html)
        # 使用lxml解析器，也可以使用html.parser
        soup = BeautifulSoup(html, 'lxml')
        # print(soup)
        # css选择器
        allimgs = soup.select('div.main-image > p > a > img.blur')
        # print(allimgs)
        # 调用download函数下载保存
        download(allimgs)
        print('page %d finished!'%i)
        i=i+1
    # 执行完毕打出ok
    print('ok')

# 获得所有页面
def all_page(dir):
    base_url = 'https://www.mzitu.com/' + dir + '/'
    # base_url = 'https://www.mzitu.com/216203/'
    # # BeautifulSoup解析页面得到最高页码数
    soup = BeautifulSoup(get_html(base_url).text, 'lxml')
    # 获得最高页码数
    pagediv=soup.find('div',class_="pagenavi")
    allpage=pagediv.find_all('span')[-2].get_text()
    # print(soup.find('span', class_="current-comment-page"))
    urllist = []
    # for循环迭代出所有页面，得到url
    for page in range(1, int(allpage)+1):
    # for page in range(1, 2):
        allurl = base_url + str(page)  # 拼出分页地址
        urllist.append(allurl)
    return urllist

# 保存图片函数，传入的参数是一页所有图片url集合
def download(list):
    for img in list:
        urls = img['src']
        # 判断url是否完整
        if urls[0:6] == 'https:':
            img_url = urls
        else:
            img_url = 'https:' + urls
        filename = img_url.split('/')[-1]
        # 保存图片
        with open(filename, 'wb') as f:
            # 直接过滤掉保存失败的图片，不终止程序
            try:
                f.write(get_html(img_url).content)
                print('Sucessful image:',filename)
            except:
                print('Failed:',filename)

if __name__ == '__main__':
    # 计时
    t1 = time.time()

    #meitun专题，所有图片使用https://www.mzitu.com/page/
    start_url = 'https://www.mzitu.com/tag/meitun/page/'
    soup = BeautifulSoup(get_html(start_url + '3').text, 'lxml')
    # 获得最高页码数
    pagediv = soup.find('div', class_="pagination")
    pages = pagediv.find_all('a')[-2].get_text()
    for page in range (3,int(pages)+1):
        #抓取当页面所有套图
        print('catching ' + (start_url + str(page)))
        picdiv = soup.find('div', class_="postlist")
        i=1 #步长是2
        for k in picdiv.find_all('a'):
            if i%2 == 1:
                print(k['href'])  # 查a标签的href值
                mkdir(k['href'].split('/')[-1])
                get_imgs(k['href'].split('/')[-1])
                i=2
            else:
                i=1
        soup = BeautifulSoup(get_html(start_url + str(page+1)).text, 'lxml')

    print(time.time() - t1)