#!/usr/bin/python
# coding: utf-8
import os, sys
reload(sys)
sys.setdefaultencoding('utf-8')

from lxml import etree
import lxml.html as LH
from StringIO import StringIO
from utils import remove_from_list 

class Parser(object):
    def __init__(self, content):
        self.content = content
        self.extract_content = ''

    def run(self):
        parser = etree.HTMLParser()
        tree   = etree.parse(StringIO(self.content), parser)

        #job title
        title = tree.xpath('//td[@class=\'sr_bt\']/text()')
        for t in title:
            print "job title: %s" % t 
            self.extract_content += "%s\n" % t

        #job detail
        detail = tree.xpath('//td[contains(@class, \'txt_4 wordBreakNormal job_detail\')]/div/text()')
        print "job detail: " 
        job_detail = ""
        for d in detail:
            print d
            job_detail += "%s\t" % d
        self.extract_content += "%s\n" % job_detail 

        #welfare
        welfare = tree.xpath('//span[contains(@class, \'Welfare_label\')]/text()')
        #print "job welfare %s " % welfare 
        print "job welfare :" 
        welfare_info = ""
        for w in welfare:
            print w
            welfare_info += "%s\t" % w
        self.extract_content += "%s\n" % welfare_info 

        #l = tree.xpath('//table[contains(@class, \'jobs_1\')]')
        txt1 = tree.xpath('//table[contains(@class, \'jobs_1\')]/tr/td[contains(@class, \'txt_1\')]')
        txt2 = tree.xpath('//table[contains(@class, \'jobs_1\')]/tr/td[contains(@class, \'txt_2\')]')

        #txt1_tag = ['发布日期：', '工作地点：', '招聘人数：', '工作年限：', '薪水范围：' ]
        txt1_tag = ['发布日期：', '工作地点：', '薪水范围：' ]

        print "job info:"
        job_info = ''
        for i, e in enumerate(txt1):
            if len(e.text.lstrip()) == 0:
                break
            if txt1[i].text == '发布日期：':
                job_info += "%s\t" % txt2[i].text
            if txt1[i].text == '工作地点：':
                job_info += "%s\t" % txt2[i].text
            if txt1[i].text == '薪水范围：':
                job_info += "%s\t" % txt2[i].text
        print job_info
        
        self.extract_content += "%s\n" % job_info 

        #company introduction
        l = tree.xpath('//div[contains(@class, \'jobs_txt\')]/p')
        print "company introduction:"
        company_intro = ""
        for i in l:
            if not i.text is None:
                print i.text
                company_intro += "%s\t" % i.text

        self.extract_content += "%s\n" % company_intro 

        #company name
        print 'company name'
        company_name = ""
        l = tree.xpath('//td[@class=\'sr_bt\']')
        for i in l:
            tr = l[0].getparent()
            iters = tr.itersiblings(); 
            for it in iters: 
                a_list = it.xpath('//td/table/tr/td/a')
                for i in a_list:
                    if not i.text is None:
                        print i.text
                        company_name = i.text
                break
            break

        self.extract_content += "%s\n" % company_name 

        #company info
        company_info = ""
        l = tree.xpath('//td/strong')
        txt1_tag = ['公司行业：', '公司性质：', '公司规模：' ]
        remove_from_list(l, txt1_tag)
        #print l
        for i in l:
            td = i.getparent()
            iters = td.itertext()
            index = 0 
            for it in iters:
                it = it.lstrip()
                #if it in txt1_tag:
                print "[%s]" % it
                company_info += "%s\t" % it
                index += 1

            break
        self.extract_content += "%s\n" % company_info


if __name__ == "__main__":

    dirlist = os.listdir('./data/');
    for i in dirlist:
        with open(os.path.join(os.getcwd(), 'data', i), 'r') as f:
            print "handle %s" % i
            content = f.read()
            
            content_list = content.split('\n')
            content_list = content_list[3:]

            content = ''.join(content_list)
            parser = Parser(content)
            extract_content = parser.run()
            with open(os.path.join('cleaned_data', i), 'a') as out:
                out.write(parser.extract_content)

