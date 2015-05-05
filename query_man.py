# -*- coding: utf-8 -*-
# encoding=utf-8
import jieba
import sys, os
reload(sys)
sys.setdefaultencoding('utf8')

import redis
connection = redis.StrictRedis(host='localhost', port=6379, db=0)

import math
import hashlib

class QueryMan(object):
    def __init__(self):
        pass

    def query(self, keyword):
        job_list = []
        doc_file_list = []
        pos_set = [] 

        word_list = keyword.split(' ')
        #print word_list
        
        for w in word_list:
            doc_list, pos_set_list = self.single_word(w)

            #print doc_list
            doc_file_list.append(doc_list)
            pos_set.append(pos_set_list)
        
        #print doc_file_list

        score_dict = {}
        if len(word_list) == 1:
            for i, d in enumerate(doc_file_list[0]):
                score_dict[d] = len(pos_set[0][i])

        for d in doc_file_list[0]:
            i = 1
            while i<len(doc_file_list):
                #print "i = %d" % i
                if d in doc_file_list[i]:
                    #print "len doc_file_list[%d] = %d" % (i, len(doc_file_list[i]))
                    if score_dict.get(d) is None:
                        score_dict[d] = math.pow(10, (len(doc_file_list)-i))
                        #print 'here'
                        #print 'score_dict[%s] = %d' % ( d, score_dict[d])
                    else:
                        score_dict[d] = score_dict[d] + math.pow(10, (len(doc_file_list)-i))
                        #print 'there'
                        #print 'score_dict[%s] = %d' % ( d, score_dict[d])
                i += 1
       

        sorted_list = []
        while len(score_dict) != 0:
            flag_k = score_dict.keys()[0]
            flag_v = score_dict[flag_k]

            for k,v in score_dict.items():
                if flag_v < v:
                    flag_v = v
                    flag_k = k

            sorted_list.append(flag_k)
            score_dict.pop(flag_k)

        #print sorted_list
        for d in sorted_list:
            file_path = os.path.join('cleaned_data', d)
            with open(file_path, 'r') as in_file:
                job_list.append(in_file.read())
            
        return job_list
    
    def single_word(self, w):
        
        md5 = hashlib.md5()
        md5.update(w)
        w = md5.hexdigest()
        
        doc_hash_key = connection.hget(w, 'doc_hash_key')
        pos_dic = connection.hgetall(doc_hash_key)

        doc_list = [] 
        pos_set_list = []

        for doc_id,pos_set_key in pos_dic.items():

            pos_set = connection.smembers(pos_set_key)

            if len(pos_set_list) == 0:
                pos_set_list.append(pos_set)
                doc_list.append(doc_id)

            for i, e in enumerate(pos_set_list):
                if len(pos_set) < len(e):
                    pos_set_list.insert(i+1, pos_set)
                    doc_list.insert(i+1, doc_id)

        return doc_list, pos_set_list
                    

if __name__ == "__main__":
    query_man = QueryMan()
    query_man.query(u'java c++ 电力')
    #query_man.query('java c++ 电力')
    #query_man.query('java')
