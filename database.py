#!/usr/bin/python
# coding: utf-8

import hashlib
import redis

class Database(object):
    def __init__(self):
        self.connection = redis.StrictRedis(host='localhost', port=6379, db=0)

    def get_connection(self):
        return self.connection

database = Database()
