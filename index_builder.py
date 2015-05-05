#!/usr/bin/python
# -*- coding: utf-8 -*-
#encoding=utf-8
import jieba
import sys, os
reload(sys)
sys.setdefaultencoding('utf8')

import redis
connection = redis.StrictRedis(host='localhost', port=6379, db=0)

import hashlib

#word word_id [docid: time, [pos1, pos2, ...]]
class IndexBuilder(object):
    def __init__(self, raw_content):
        self.raw_content = raw_content

    def build(self, doc_id):
        #print self.raw_content
        seg_list = jieba.cut_for_search(self.raw_content)  # 搜索引擎模式
        #print("".join(seg_list))

        temp_string = ",".join(seg_list)
        temp_list = temp_string.split(",")
        #print temp_list

        excluded_list = ['', ' ', ' ', '\t', '\n', '\r\n', '；', ';', ':', '：', '.', '。', ',', '，', '!', '（', '）', '(', ')','！','、', '-', '・']

        for i,w in enumerate(temp_list):
            if w in excluded_list: 
                continue

            #print "[%d] = (%s)" %(i,w)
            
            md5 = hashlib.md5()
            md5.update(w)
            w = md5.hexdigest() 

            if connection.hget(w, 'word') is None:
                connection.hset(w, 'word', w)

            df = connection.hget(w, 'df')
            if connection.hget(w, 'df') is None:
                connection.hset(w, 'df', 1)
            else:
                connection.hincrby(w, 'df', 1)

            doc_hash_key = connection.hget(w, 'doc_hash_key')
            if doc_hash_key is None:
               connection.hset(w, 'doc_hash_key', w+'_doc_hash_key') 
            
            did = connection.hget(w+'_doc_hash_key', doc_id)
            set_key = "%s_%s_pos_set" % (w, doc_id)
            if did is None: 
                connection.hset(w+'_doc_hash_key', doc_id, set_key)

            #print doc_id
            connection.sadd(set_key, i)


if  __name__ == '__main__':
    #with open('./cleaned_data/f86bfb798496058c61343542858490f2', 'r') as f:
    #    content = f.read()
    #    indexBuilder = IndexBuilder(content)
    #    indexBuilder.build('f86bfb798496058c61343542858490f2')

    dirlist = os.listdir('./cleaned_data/')
    for i in dirlist:
        with open('./cleaned_data/'+i, 'r') as f:
            content = f.read()
            indexBuilder = IndexBuilder(content)
            indexBuilder.build(i)
