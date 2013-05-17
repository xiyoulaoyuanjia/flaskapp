#!/usr/bin/python
#coding: utf-8

import requests
from HTMLParser import HTMLParser
from time import sleep
from threading import Thread

#from sqldb import *
import datetime

## 
globalName={}
HashKey={}

## 记录需要更新的项目
upGlobalName={}

## 记录需要更新的id(github上的) 每次都会发生变化
#oriId=""


URL="https://github.com/xiyoulaoyuanjia/blog"
BASEURL="https://github.com"




####
class MyBaseHTMLParser(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		self.recording = 0
		self.attrsLocal={}

	def	handle_starttag(self,tag,attrs):
## 对于 页面上每一个markdown文章 class属性都是确定的
### examle <a href="/xiyoulaoyuanjia/AboutWeb/blob/master/JSON%20.md" class="js-directory-link js-slide-to css-truncate-target" id="22cd99294dd3f24a40fa3008a24a7ead-27ce5e36995db72e2b8fbb46f063bda241014a43" title="JSON .md">JSON .md</a></td>
## 获得的属性 包括 href class id css title 
## 最后将list转化为(dict函数) 字典 
## 已字典的 id为key 整个字典为values 存入globalName中
		if tag=='a':
			for name,value in attrs:
				if name == "class" and value == 'js-directory-link js-slide-to css-truncate-target':
					### 这里先把内容存起来,等到时间判断后在决定是否添加到globalName 中去
					self.attrsLocal=dict(attrs)
					self.recording=dict(attrs)['id']

		if tag == 'time' and self.recording:
			for name,value in attrs:
					if name == "title":
							if self.attrsLocal['id'].split("-")[0] not in HashKey.keys() :    ### id 不再HashKey 内 则表明是新增的对象
								globalName[self.attrsLocal['id']]=self.attrsLocal
								globalName[self.recording]['datetime']=value

							### 获得的时间大于数据库中的时间即为有blog更新
							elif HashKey[self.attrsLocal['id'].split("-")[0]] < datetime.datetime.strptime(value,"%Y-%m-%d %H:%M:%S"):
								upGlobalName[self.attrsLocal['id']]=self.attrsLocal
								upGlobalName[self.recording]['datetime']=value
								print "有更新项目"
								pass
							else :   ### nothing to do
								pass
			self.recording =0
## 获取 <article> 与 </article> 中的所有内容 元素 与属性
## 注意这里 article 全局唯一
## 这里只测试了一些简单的情况 
class MyPageParser(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		self.recording = 0
		self.data = ""
		## 这里记录抓取内容的 des 描述信息
		self.des = ""
	def handle_starttag(self, tag, attrs):
		if self.recording:
			self.recording += 1
			if attrs:
				attrsStr = " ".join(['''%s="%s"''' % (k, v) for k, v in attrs])
				self.data += "<" + tag + " " + attrsStr+">"
			else:
				self.data += "<" + tag + ">"
			return
		if tag != 'article':
			return
		self.recording = 1

	def handle_endtag(self, tag):
		if tag == 'article':
				self.recording = 0
#		if tag == 'article' and self.recording:
#			self.recording -= 1
#		elif self.recording:
#			self.data += "</" + tag + ">"
		elif	self.recording : 
				self.data += "</" + tag + ">"
				self.recording -=1
##      这里取前五位的属性内容作为描述信息
				if 	self.recording <= 1:
					self.des=self.data
	def handle_data(self, data):
		if self.recording:
			self.data +=data


class URLThread(Thread):
	def __init__(self, url, key,timeout=10,allow_redirects=True):
		super(URLThread, self).__init__()
		self.url = url
		self.timeout = timeout
		self.allow_redirects = allow_redirects
		self.key=key
		self.response = None
###  存储 html 解析结果
		self.pageParse = None 
		self.des= None
	def run(self):
		try:
			self.response = requests.get(self.url, timeout = self.timeout, allow_redirects = self.allow_redirects)
### 返回结果处理
			getPageParse=MyPageParser()
			getPageParse.feed(self.response.text)
			self.pageParse=getPageParse.data
			self.des=getPageParse.des
		except Exception , what:
			print what
			pass

def multi_get(uris, timeout=10, allow_redirects=True,sleepTime = 0.01):
    '''
    uris    uri列表
    timeout 访问url超时时间
    allow_redirects 是否url自动跳转
    '''
    if not bool(uris):
	    return urls 
    def alive_count(lst):
       	alive = map(lambda x : 1 if x.isAlive() else 0, lst)
        return reduce(lambda a,b : a + b, alive)
    threads = [ URLThread(uris[key], key,timeout,allow_redirects) for key in uris.keys() ]
    for thread in threads:
        thread.start()
    while alive_count(threads) > 0:
        sleep(sleepTime)
    for x in threads:
		uris[x.key]={}
		uris[x.key]['content']=x.pageParse
		uris[x.key]['des']=x.des
    return uris
#    return dic(zip([ x.pageParse for x in threads ],[x.des for x in threads]))




def getPage(allItem=globalName):
#	import time
#	start=time.time()
	urlList={}
##  从 hash 中提取 url list
	for key in allItem:
		urlList[key]=BASEURL+allItem[key]['href']
	if not bool(urlList):
	 	return  
## contentOut is hash 
	contentOut=multi_get(urlList,5,False)
	for key in allItem:
		allItem[key]['content']=contentOut[key]['content']
		allItem[key]['des']=contentOut[key]['des']

	if allItem == globalName:
		initInsertGlobal(allItem)
	else:
		upGlobal(allItem)

#	end=time.time()
#	print (end-start)



## 更新 
### 1. 更新添加新blog页面
### 2. 更新原有的blog页面 

def updatemain():
	db=get_db()
## how do it whith [for in] .....
### oriId is like b128b7694e4de962e0088bcb1bcb254f-c427d342a9567ae85f40f17de4cff40cc03d3e02
#### when we edite blog on the github the b128b7694e4de962e0088bcb1bcb254f is same
	for item in update_db(db):
		HashKey[item['oriId']]=item['datetime']
## 
	initMain(allItem=[upGlobalName,globalName])	


## 初始化 默认抓取所有的
def initMain(allItem=[globalName]):
	localRequests=requests.get(URL)
	parser = MyBaseHTMLParser()
	parser.feed(localRequests.text)
	parser.close()
	[getPage(item) for item in allItem]

#	html='<div><html><article class="markdown-body entry-content" itemprop="mainContentOfPage"><h1><a name="django" class="anchor" href="#django"><span class="mini-icon mini-icon-link"></span></a>Django</h1><p><strong>视图与url配置</strong></p><p>一个视图就是一个python的函数,并且必须满足两个条件</p></article></html><p></p><p>ffff</p></div>'


#	html=requests.get("https://github.com/xiyoulaoyuanjia/blog/blob/master/Django.md")	

#	getPageParse=MyPageParser()
#	getPageParse.feed(html.text)
#	print getPageParse.data

if __name__ == '__main__':
#	initMain()
	updatemain()	
