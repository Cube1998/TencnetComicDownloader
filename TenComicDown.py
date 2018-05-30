#coding=utf8

#腾讯的漫画ID：
#狐妖小红娘 ：518333
#海贼王 ： 505430
#小绿和小蓝 ； 536332
import requests
import json
import selenium.webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import os
import random
import re


os.environ["LANG"] = "en_US.UTF-8"


def scroll(n,i):

    return "window.scrollTo(0,(document.body.scrollHeight/{0})*{1}*100);".format(n,i)

def comic(url):
    comics={}
    comic_url=[]
    #driver = selenium.webdriver.Chrome()
    driver = selenium.webdriver.PhantomJS()
    #driver.implicitly_wait(30)
    driver.set_page_load_timeout(30)

    #url='http://ac.qq.com/ComicView/index/id/543606/cid/1'
    #url='https://manhua.163.com/reader/4639712296520118385/4643138479170091194#scale=7@imgIndex=8'
    driver.get(url)
    time.sleep(1)
    n = 50
    for i in range(0,n+1):
        s = scroll(n,i)
        print(s)
        driver.execute_script(s)
        random_time = random.random()
        print (random_time)

        time.sleep(random_time)
    



    content=driver.page_source

    #print (content)
    soup = BeautifulSoup(content,"html.parser")
    

    comic_list=soup.find_all('li')
    comic_title=soup.find('title').text.strip()
    comic_title=comic_title.replace('/',' ')
    for i in comic_list:
        
        try:
            
            image_url=i.find('img')['src']
            #print(image_url
            comic_url.append(image_url)
            print ("No Bug Here")
        except Exception as e:
            
            print ("Here Is Debuging")

    comics['title']=comic_title
    comics['url']=comic_url
            

    return comics
    #print (content)
    #soup = BeautifulSoup(content,"lxml")


def download(comics):
    #print (comics)

    title=comics['title']
    #print (title)
    pattern = re.compile(r"(.*?)-在线漫画",re.S)
    pattern2 = re.compile(r"《(.*?)》",re.S)
    title = re.findall(pattern,title)
    title = title[0]
    a = re.findall(pattern2,title)
    urls=comics['url']
    directory =  os.getcwd()
    if os.path.exists(directory + '/'+a[0]):
        print ("dir exists")
    else :
        os.mkdir(directory + '/'+a[0])
    directory=directory + '/'+a[0]+ '/'+title

    if os.path.exists(directory):
        for download_link in urls:
            time.sleep(random.randint(1, 10))
            fname=directory+'/'+str(urls.index(download_link)+1)+'.png'
            if os.path.exists(fname):
                #pass
                print ('File '+fname+' is already exists,SKIP......')
            else:
           #     print ('Folder is already exists,Downloding '+directory+'.....Please Waiting')
                r=requests.get(download_link)
                with open (fname,"wb") as code:
                    code.write(r.content)
                print(fname+' Downloading Completed')
    else:
        os.mkdir(directory)
        print (len(urls))
        indexPic = 0
        #     print ('Downloding '+directory+'.....Please Waiting')
        for download_link in urls:
            random_time = random.random()
            print (random_time)

            time.sleep(random_time)
            fname=directory+'/'+str(indexPic+1)+'.png'
            if os.path.exists(fname):
                #pass
                print ('File '+fname+' is already exists,SKIP......')
            elif 'gif' in download_link:
                print ("Wrong Link")
            elif 'qpic' in download_link:
                print ("Not Interested Pic")
            elif 'data:image' in download_link:
                print ("Wrong Link")
            else :
                r=requests.get(download_link)
                with open (fname,"wb") as code:
                    code.write(r.content)
                print(fname+' Downloading Completed')
                indexPic = indexPic+1

if __name__=="__main__":

    url='http://ac.tc.qq.com/store_file_download?buid=15017&uin=1422363399&dir_path=/&name=27_20_56_3faad5b60275c2829819a8c41cb0a919_953.ori'

    for i in range(150,180):
        url='http://ac.qq.com/ComicView/index/id/505430/cid/'+str(i)

        print ('Now Analyzing  Chapter '+ str(i)+',waiting for 60 seconds')
        #time.sleep(random.randint(50, 60))
        result=comic(url)
        download(result)



    #print (result)