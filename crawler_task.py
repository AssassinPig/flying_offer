#!/usr/bin/python
# coding: utf-8
from bs4 import BeautifulSoup
import requests
import os, sys
import json
from task import Task
import hashlib
from models import Job, Company 

#import lxml.html as LH
from lxml import etree
from StringIO import StringIO
from utils import *

from datetime import *

class Task(object):

    def __init__(self, keyword):
        self.User_Agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.152 Safari/537.36"

        self.headers = {}
        self.post_info = {}
        self.session = requests.Session()

    def search(self):
        pass

    def parse(self):
        pass

    def fetch(self):
        pass

class Go51JobTask(Task):

    def __init__(self, keyword):
        super(Go51JobTask, self).__init__(keyword)
        self.headers = {
            #"User-Agent" : User_Agent,
            "Accept":" text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding":" gzip, deflate",
            "Accept-Language":" zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4,ja;q=0.2",
            "Cache-Control":" no-cache",
            "Content-Length":" 179",
            "Content-Type":" application/x-www-form-urlencoded",
            "Host":" search.51job.com",
            "Origin":" http://search.51job.com",
            "Pragma":" no-cache",
            "Proxy-Connection":" keep-alive"
        }

        self.post_info = {
            "lang":"c",
            "stype":"1",
            "postchannel":"0000",
            "fromType":"1",
            "line":"",
            "confirmdate":"9",
            "from":"",
            "keywordtype":"2",
            "keyword":"java",
            "image.x":"33",
            "image.y":"12",
            "funtype":"0000",
            "industrytype":"00"
        }

        self.keyword = keyword


    def make_search_url(self):
        self.post_info['keyword'] = self.keyword 
        search_url = 'http://search.51job.com/jobsearch/search_result.php'
        search_url+='?'

        content_param = ''
        for key,value in self.post_info.items():
            content_param += key+'='+value + '&'
        search_url += content_param + 'fromJs=1'

        self.headers['Content-Length'] = len(content_param)-1

        return search_url

    def search(self):
        session = self.session

        search_url = self.make_search_url()
        #print search_url
        resp = session.post(search_url,data=json.dumps(self.post_info),headers=self.headers,verify=False)
        html_doc = resp.content
        soup = BeautifulSoup(html_doc)
        
        del self.headers['Content-Length']

        has_visited = []
        to_visited = []
        while True:
            job_list = soup.select('#resultList .td1 a')
            for j in job_list:
                job = j.get('href')
                self.fetch_job(job)

            next_page = soup.select('.searchPageNav td a')

            #if len(job_list) == 0:
            #    break

            for l in next_page:
                url = l.get('href')
                if url not in has_visited:
                    to_visited.append(url)
                    #print "add %s" % url

            if len(to_visited) <= 0:
                print 'the end1'
                break

            url = ''
            while True:
                if len(to_visited) <= 0:
                    break

                url = to_visited.pop() 
                if url in has_visited:
                    continue
                else:
                    has_visited.append(url)
                    break
            
            if len(to_visited) <= 0:
                print 'the end2'
                break

            #print 'will fetch %s' % url

            resp = session.post(url, headers=self.headers,verify=False)
            html_doc = resp.content
            soup = BeautifulSoup(html_doc)
    
    def fetch_job(self, url):
        #print 'fetch job %s' % url
        session = self.session
        resp = session.post(url, headers=self.headers, verify=False)
        html_doc = resp.content
        soup = BeautifulSoup(html_doc)

        m = hashlib.md5()
        m.update(url)
        file_name = m.hexdigest()
        file_name = os.path.join(os.getcwd(), 'data', file_name)

        with open(file_name, 'a+') as f:
            #f.write(html_doc)
            info = "version:%s\nurl:%s\n" % ('0.1', url)
            f.write(info)

            dt = datetime.today()
            nowtime = "date:%d-%d-%d %d-%d-%d\n" % ( dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second )
            f.write(nowtime)
            
            #f.write(item.getHeader())
            #f.write('\n')
            f.write(html_doc)

        print "fetch %s" % url
        #self.save_job(html_doc)

    def save_job(self, html_doc):
        job = Job()

        parser = etree.HTMLParser()
        tree   = etree.parse(StringIO(html_doc), parser)

        #title
        title = tree.xpath('//td[@class=\'sr_bt\']/text()')
        for i in title:
            job.title = title[0] 
            break

        #job_detail
        job_detail = tree.xpath('//td[contains(@class, \'txt_4 wordBreakNormal job_detail\')]/div/text()')
        for i in job_detail:
            job.detail = job_detail[0]
            break
    
        welfare = tree.xpath('//span[contains(@class, \'Welfare_label\')]/text()')
        for w in welfare:
            job.welfare.add(w)

        #date location saraly
        txt1 = tree.xpath('//table[contains(@class, \'jobs_1\')]/tr/td[contains(@class, \'txt_1\')]')
        txt2 = tree.xpath('//table[contains(@class, \'jobs_1\')]/tr/td[contains(@class, \'txt_2\')]')
        
        txt1_tag = ['发布日期：', '工作地点：', '薪水范围：' ]
        for i, e in enumerate(txt1):
            if len(e.text.lstrip()) == 0:
                break
            if txt1[i].text == '发布日期：':
                #hdls[txt1[i].text] = txt2[i].text
                job.date = txt2[i].text 
            if txt1[i].text == '工作地点：':
                job.location = txt2[i].text 
            if txt1[i].text == '薪水范围：':
                job.salary = txt2[i].text 

        job.save()
        #need for speed
        self.save_company(tree)


    def save_company(self, tree):
        company = Company()
        
        #company introduction
        l = tree.xpath('//div[contains(@class, \'jobs_txt\')]/p')
        #print "company introduction:"
        for i in l:
            if not i.text is None:
                #print i.text
                company.introduction = i.text


        #company name
        l = tree.xpath('//td[@class=\'sr_bt\']')
        for i in l:
            tr = l[0].getparent()
            print "company name:"
            iters = tr.itersiblings(); 
            for it in iters: 
                a_list = it.xpath('//td/table/tr/td/a')
                for i in a_list:
                    if not i.text is None:
                        #print i.text
                        company.name = i.text
                break
            break

        #company info
        l = tree.xpath('//td/strong')
        txt1_tag = ['公司行业：', '公司性质：', '公司规模：' ]

        remove_from_list(l, txt1_tag)
        for i in l:
            td = i.getparent()
            iters = td.itertext()
            index = 0
            for it in iters:
                it = it.lstrip()
                if it in txt1_tag:
                    continue
                if index == 0:
                    company.industry = it
                elif index == 1:
                    company.nature = it
                elif index == 2:
                    company.scale = it
                index += 1
                #print "[%s]" % it.lstrip()
            break

        company.save()

if __name__ == '__main__':
    task = Go51JobTask('java+济南')
    task.search()
