import os
import threading
import re
from bs4 import BeautifulSoup
from urllib.request import urlopen
from selenium import webdriver

browserPath = 'D:/phantomjs-1.9.2-windows/phantomjs.exe'
homePage = 'https://mm.taobao.com/search_tstar_model.htm?'
outputDir = 'photo/'
parser = 'html5lib'


def main():

    driver = webdriver.PhantomJS(executable_path=browserPath, service_args=['--ignore-ssl-errors=true', '--ssl-protocol=any'])
    driver.get(homePage)
    # driver.get("javascript:document.getElementById('overridelink').click();");
    bsObj = BeautifulSoup(driver.page_source, parser)
    print("[*]OK GET Page")
    girlsList =driver.find_element_by_id('J_GirlsList').text.split('\n')
    girlsUrl = bsObj.find_all('a',{'href':re.compile('\/\/.*\.htm\?(userId=)\d*')})
    imagesUrl = re.findall('\/\/gtd\.alicdn\.com\/sns_logo.*\.jpg',driver.page_source)
    girlsNL = girlsList[::3]
    girlsHW = girlsList[1::3]
    girlsHURL = [('http:'+i['href'])for i in girlsUrl]
    girlsPhotoURL = [('https:' + i) for i in imagesUrl]
    girlsInfo = zip(girlsNL,girlsHW,girlsHURL,girlsPhotoURL)
    for girlNL,girlHW,girlHURL,girlCover in girlsInfo:
        print('[*]Girl:',girlNL,girlHW)
        mkdir(outputDir+girlNL)
        print('[*]saving...')
        data =urlopen(girlCover).read()
        with open(outputDir+girlNL+'/COVER.jpg','wb') as f:
            f.write(data)
        print('[+]Loading Cover...')
        getImgs(girlHURL,outputDir+girlNL)
        driver.close()
    # print(driver.page_source)
    print(girlsUrl)


def mkdir(path):
    isExists = os.path.exists(path)
    if not isExists:
        print('[*]新建了文件夹', path)
        os.makedirs(path)
    else:
        print('[+]文件夹',path,'已经创建')


def getImgs(url, path):
    driver = webdriver.PhantomJS(executable_path=browserPath, service_args=['--ignore-ssl-errors=true', '--ssl-protocol=any'])
    driver.get(url)
    print("    [*]Opening...")
    bsObj = BeautifulSoup(driver.page_source, parser)
    #获得模特个人页面上的艺术照地址
    imgs = bsObj.find_all("img", {"src": re.compile(".*\.jpg")})
    for i, img in enumerate(imgs[1:]):  #不包含与封面图片一样的头像
        try:
            html = urlopen('https:' + img['src'])
            data = html.read()
            fileName = "{}/{}.jpg".format(path, i + 1)
            print("    [+]Loading...", fileName)
            with open(fileName, 'wb') as f:
                f.write(data)
        except Exception:
            print("    [!]Address Error!")
    driver.close()

if __name__ == '__main__':
    if not os.path.exists(outputDir):
        os.makedirs(outputDir)
    main()