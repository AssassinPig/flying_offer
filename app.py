#!/usr/bin/python
# coding: utf-8
import os, sys
reload(sys)
sys.setdefaultencoding('utf-8')

from flask import Flask
app = Flask(__name__)

from flask import render_template
from flask import g, request, flash

from query_man import QueryMan

@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        keyword=request.form['q']
        query_man = QueryMan()
        job_list = query_man.query(keyword)
        return render_template('list.html', job_list = job_list)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
