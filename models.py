#!/usr/bin/python
# coding: utf-8

import hashlib
import redis

from database import database 

class Employer(object):
    pass

class Employee(object):
    # this object reserved in redis as hash
    # search_list is list
    def __init__(self, email):
       self.email = email 

       self.nick = '' 
       self.tel = '' 
       self.password = ''

       self.search_list = [] 


    def login_author(self):
        return True

    def is_exist(self):
        connection = database.get_connection() 
        key = self.make_unique_key()

        exist_email = connection.hexists(key, 'email')
        if exist_email == 0:
            return False
        
        return True

    def make_unique_key(self):
        md5 = hashlib.md5()
        md5.update(self.email)
        return md5.hexdigest() 

    def load(self):
        connection = database.get_connection() 
        object_key = self.email
        
        connection.hexists(object_key, 'email')

        connection.hget(object_key, 'email')
        connection.hget(object_key, 'nick')
        connection.hget(object_key, 'password')

        search_list_id = self.make_unique_search_list_id()
        search_list_len = connection.llen(search_list_id)
        search_list = connection.lrange(search_list_id, 0, -1)

        for l in search_list:
            self.search_list.append(l)


    def make_unique_search_list_id(self):
        md5 = hashlib.md5()
        md5.update(self.email+ '_search_list')
        return md5.hexdigest()
        

class Job(object):
    def __init__(self):
        self.title = ''
        self.location = ''
        self.company = '' 
        self.date = ''
        self.salary = ''
        self.detail = '' 
        self.welfare = set() 

    def is_exist(self):
        connection = database.get_connection() 
        job_key = self.make_unique_key()

        exist_name = connection.hexists(job_key, 'title')
        if exist_name == 0:
            return False
        
        return True

    def save(self):
        connection = database.get_connection() 
        job_key = self.make_unique_key()
        print "saving job %s" % job_key
        connection.hset(job_key, 'title', self.title) 
        connection.hset(job_key, 'location', self.location) 
        connection.hset(job_key, 'company', self.company) 
        connection.hset(job_key, 'date', self.date) 
        connection.hset(job_key, 'detail', self.detail) 
        connection.hset(job_key, 'salary', self.salary) 

        welfare_list_key = self.make_unique_welfare_key()
        for e in self.welfare:
            connection.sadd(welfare_list_key, e)

    def load(self):
        pass

    def make_unique_key(self):
        #title_company
        md5 = hashlib.md5()
        md5.update(self.title+"_"+self.company)
        return md5.hexdigest()

    def make_unique_welfare_key(self):
        md5 = hashlib.md5()
        md5.update(self.title+"_welfare_list")
        return md5.hexdigest()

class Company(object):
    def __init__(self):
        self.name = ''
        self.href = ''
        self.scale = ''
        self.industry = ''
        self.nature = ''
        self.introduction = ''

    def is_exist(self):
        connection = database.get_connection() 
        company_key = self.make_unique_key()

        exist_name = connection.hexists(company_key, 'name')
        if exist_name == 0:
            return False
        
        return True

    def save(self):
        connection = database.get_connection() 
        company_key = self.make_unique_key()
        print "saving company %s" % company_key 
        connection.hset(company_key, 'name', self.name)
        connection.hset(company_key, 'href', self.href)
        connection.hset(company_key, 'scale', self.scale)
        connection.hset(company_key, 'industry', self.industry)
        connection.hset(company_key, 'nature', self.nature)
        connection.hset(company_key, 'introduction', self.introduction)

    def make_unique_key(self):
        md5 = hashlib.md5()
        md5.update(self.name)
        return md5.hexdigest()

