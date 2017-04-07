import requests # 网络请求
from bs4 import BeautifulSoup # 截取http网页内容
import os
import time
import hashlib
from selenium import webdriver  #导入Selenium的webdriver


from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

#phantomjs 其实就是一个没有界面的浏览器，最主要的功能是能够读取js加载的页面。
#Selenium 实质上是一个自动化测试工具，能够模拟用户的一些行为操作，比如下拉网页。


class GetPicture():
    def __init__(self): #类的初始化操作
        # 给请求指定一个请求头来模拟chrome浏览器
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'}
        self.webUrl = 'https://unsplash.com'
        self.folderPath = '/Volumes/影片/Pictures'

    def mkdir(self, path):
        path = path.strip()
        isExists = os.path.exists(path)
        if not isExists:
            print('创建名字叫做', path, '的文件夹')
            os.makedirs(path)
            print('创建成功！')
        else:
            print(path, '文件夹已经存在了，不再创建')

    def saveImg(self, url, name):
        fileNames = os.listdir(self.folderPath)   # 只会获取当前目录下的文件,不会递归进行访问
        if name in fileNames:
            print('图片已存在, 跳过')
            return 0
        else:
            img = requests.get(url)
            f = open(name, 'ab')
            f.write(img.content)
            f.close()
            return 1

    # 使用 requests 通过PhantomJS来进行网络请求获取图片
    def getPic(self):
        r = requests.get(self.webUrl, headers=self.headers)
        all_a = BeautifulSoup(r.text, 'lxml').find_all('a', class_='cV68d')  #获取网页中的class为cV68d的所有a标签

        self.mkdir(self.folderPath)
        os.chdir(self.folderPath)  # 切换路径至上面创建的文件夹

        for a in all_a:
            img_str = a['style'] # background-image:url("https://images.unsplash.com/reserve/unsplash_528b27288f41f_1.JPG?dpr=1&auto=compress,format&fit=crop&w=767&h=511&q=80&cs=tinysrgb&crop=&bg=");width:0;height:0
            # print(img_str)

            str1 = img_str[img_str.find('"')+1 :] # https://images.unsplash.com/reserve/unsplash_528b27288f41f_1.JPG?dpr=1&auto=compress,format&fit=crop&w=767&h=511&q=80&cs=tinysrgb&crop=&bg=");width:0;height:0
            # print(str1)

            imgUrl = str1[:str1.find('"')]
            # print(imgUrl)

            array = imgUrl.split("-")
            if len(array) > 1:
                self.saveImg(imgUrl, array[1])

    def scrollDown(self, driver, times):
        for i in range(times):
            print("开始执行第", str(i + 1), "次下拉操作")

            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") #执行JavaScript实现网页下拉倒底部

            time.sleep(30)
            # TODO: 等待时间优化

    def getMD5String(self, stringValue):
        encodeString = stringValue.encode('utf8')
        md5Object = hashlib.md5(encodeString)
        return md5Object.hexdigest()

    # 获取文件夹内所有文件名

    # 使用 selenium 通过 PhantomJS 来进行网络请求获取图片
    def getPicWithSelenium(self):

        print('正在获取网页内容...')

        driver = webdriver.PhantomJS()
        driver.get(self.webUrl)

        # locator = (By.LINK_TEXT, 'cV68d')
        # WebDriverWait(driver, 60, 1).until(EC.text_to_be_present_in_element())
        # TODO:等待与超时处理

        self.scrollDown(driver=driver, times=1)

        all_a = BeautifulSoup(driver.page_source, 'lxml').find_all('a', class_='cV68d')  # 获取网页中的class为cV68d的所有a标签
        # print(all_a)

        self.mkdir(self.folderPath)
        os.chdir(self.folderPath)

        imgCount = 0
        for a in all_a:
            img_str = a['style'] # background-image:url("https://images.unsplash.com/reserve/unsplash_528b27288f41f_1.JPG?dpr=1&auto=compress,format&fit=crop&w=767&h=511&q=80&cs=tinysrgb&crop=&bg=");width:0;height:0
            # print(img_str)

            imgUrl = img_str[img_str.find('(')+1:] # https://images.unsplash.com/reserve/unsplash_528b27288f41f_1.JPG?dpr=1&auto=compress,format&fit=crop&w=767&h=511&q=80&cs=tinysrgb&crop=&bg=");width:0;height:0
            # print(str1)

            imgUrl = imgUrl[:imgUrl.find(')')]
            print(imgUrl)

            # 根据摘要生成文件名
            imgName = self.getMD5String(imgUrl) + '.JPG'
            print('生成文件名', imgName)

            print('正在保存图片:', imgName, '...')
            if self.saveImg(url = imgUrl, name = imgName):
                imgCount+=1
                print(imgName, '保存成功！')

        print('操作完成,一共保存了', imgCount, '张图片')

getPictureObj = GetPicture()
# getPicture.getPic()
getPictureObj.getPicWithSelenium()
