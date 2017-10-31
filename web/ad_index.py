# -*- coding:utf-8 -*-

import os
from .botapp import app
from bottle import route,request,response,template,redirect
from db import aduser,level,news,tools
from setting import secret

@app.route('/admin',method=['GET','POST'])
def index():
    info = request.get_cookie('info',secret=secret)
    info = response.set_cookie('info','',secret=secret)
    response.set_cookie('info','',secret=secret)
    if request.method == 'GET':
        name = request.get_cookie('adname',secret=secret)
        id = request.get_cookie('adid',secret=secret)
        user_type = request.get_cookie('user_type',secret=secret)
        return template('tpls/ad_tpls/index.tpl',
            name=name,
            id=id,
            user_type=user_type,
            info=info
            )
    elif request.method == 'POST':
        verify_text = request.get_cookie('verify_text',secret=secret)
        response.set_cookie('verify_text','',secret=secret)
        if verify_text and verify_text.lower() == \
            request.forms.getunicode('verify_text').lower().strip():
            name = request.forms.getunicode('name')
            password = request.forms.getunicode('password')
            u = aduser.login(name,password)
            if u:
                response.set_cookie('adname',u.name,secret=secret)
                response.set_cookie('adid',str(u.id),secret=secret)
                response.set_cookie('user_type',u.user_type,secret=secret)
                return template('tpls/ad_tpls/index.tpl',
                    name=name,
                    id=str(u.id),
                    user_type=u.user_type,
                    info=info)
            else:
                response.set_cookie('info',
                    "登录失败，请检查用户名或密码！",
                    secret=secret)
        else:
            response.set_cookie('info',"验证码错误，请重新登录！",
                secret=secret)
        redirect('/admin')
