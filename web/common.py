# -*- coding:utf-8 -*-

from bottle import route,error,static_file,response
from tools.verify_gen import get_verify
from setting import secret

@error(404)
def err(err):
    return '404'

@route('/static/<filename:re:.*.[js|css|jpg|jpeg|png]$>')
def get_tatic(filename):
    rootdir = './img'
    if filename.endswith('js'):
        rootdir = './js'
    if filename.endswith('css'):
        rootdir = './css'
    return static_file(filename,root=rootdir)

@route('/ckeditor/<filename:re:.*.[js|css|jpg|jpeg|png]$>')
def get_ckeditor(filename):
    rootdir = './js/ckeditor'
    return static_file(filename,root=rootdir)

@route('/img/<filename:re:.*.[js|css|jpg|jpeg|png]$>')
def get_img(filename):
    rootdir = './uploads'
    return static_file(filename,root=rootdir)

@route('/active/<filename:re:.*.[gif|jpg|jpeg|png]$>')
def get_active(filename):
    rootdir = './activeimg'
    return static_file(filename,root=rootdir)

@route('/verify')
def verify():
    img,text = get_verify()
    response.set_cookie('verify_text',text,secret=secret)
    return img