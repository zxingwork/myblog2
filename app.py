#!/usr/bin/env python
# encoding: utf-8
# @author   : changhsing
# @time     : 2020/8/3 19:39
# @site     : 
# @file     : app.py
# @software : PyCharm
from flask import *
import os
import requests
import pymysql


app = Flask(__name__)
key = os.urandom(24)
app.secret_key = key


@app.route('/')
def index():
    error = None
    username = None
    show_num = 10
    if 'username' in session:
        error = '1'
        username = session['username']
    zhihuhotlist = zhihu_hot()[:10]
    return render_template('index.html', zhihuhotlist=zhihuhotlist, error=error, username=username)


@app.route('/login/',methods=['POST', 'GET'])
def login():
    app.logger.debug(session)
    if request.method.upper() == 'POST':
        if 'username' not in session:
            username, password = request.form['username'], request.form['password']
            if username == 'root' and password == 'ZXSSJDY111899':
                session['username'] = username
                session['password'] = password
                return redirect(url_for('index'))
            error = 'Error username or password...'
            return render_template('login.html', error=error)
        return redirect(url_for('index'))
    if 'username' in session:
        return redirect(url_for('index'))
    return render_template('login.html')


@app.route('/logout/')
def logout():
    if 'username' in session:
        session.pop('username')
        session.pop('password')
    return redirect(url_for('index'))


@app.route('/blog/<name>')
def show_blog(name):
    name = name + '.md'
    blog_path = './blog'
    file_path = os.path.join(blog_path, name)
    app.logger.debug(file_path)
    if os.path.exists(file_path):
        Typecode = 'gbk'
        try:
            with open('./blog/{}'.format(name), 'r', encoding='utf-8', errors='ignore') as f:
                app.logger.debug('open file {}'.format(name))
                text = f.read()
                app.logger.debug(text)
            return render_template('showblog.html', text=text)
        except Exception as e:
            app.logger.error(e)
            return render_template('errorpage.html', error="Open Filed!")

    return render_template('errorpage.html', error="The Blog not exists!")


def zhihu_hot() -> list:
    header = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN',
        'User-Agent': 'ApiPOST Runtime +https://www.apipost.cn'
    }
    re = requests.get(url='https://www.zhihu.com/api/v4/search/top_search', headers=header)
    j = re.json()['top_search']['words']
    r = []
    for i in j:
        r.append(i['display_query'])
    return r


def bloglist():
    dir_path = './blog'
    return os.listdir(dir_path)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)