# -*- coding:utf-8 -*-

import os
from bottle import route,request,response,template,redirect
from db import aduser,level,news,tools
from setting import secret

def admin_verify(go_url='/admin'):
    user_type = request.get_cookie('user_type',secret=secret)
    if user_type != 100:
        response.set_cookie('info',
            "你未登录或无权限此项使用管理功能！",
            secret=secret)
        redirect(go_url)

def login_verify(go_url='/admin'):
    name = request.get_cookie('adname',secret=secret)
    id = request.get_cookie('adid',secret=secret)
    if name and id:
        return int(id)
    response.set_cookie('info',
            "请登录后使用管理功能！",
            secret=secret)
    redirect(go_url)

@route('/usermgr',method=["GET","POST"])
def usermgr():
    admin_verify()
    if request.method == "GET":
        users = aduser.get_users()
        powers = aduser.get_user_power(users)
        lvls = level.get_lvls()
        user_type = request.get_cookie('user_type',secret=secret)
        name = request.get_cookie('adname',secret=secret)
        id = request.get_cookie('adid',secret=secret)
        return template('tpls/ad_tpls/usermgr.tpl',
            users=users,
            powers=powers,
            lvls=lvls,
            name=name,
            id=id,
            user_type=user_type)
    if request.method == "POST":
        action = request.forms.getunicode('action')
        if action == "add":
            name = request.forms.getunicode('name')
            password = request.forms.getunicode('password')
            aduser.add_user(name=name,password=password)
        elif action == "power":
            param_keys = [i for i in request.forms.keys()]
            # print(param_keys)
            uid_suffix = '-chkbox'
            lvl_suffix = '-vchkbox'
            user_ids = [i[:-len(uid_suffix)] for i in param_keys 
                if i.endswith(uid_suffix)]
            lvl_ids = [i[:-len(lvl_suffix)] for i in param_keys 
                if i.endswith(lvl_suffix)]
            aduser.add_power(user_ids,lvl_ids)
        elif action == 'edit':
            name = request.forms.getunicode('name').strip()
            password = request.forms.getunicode('password').strip()
            uid = request.forms.getunicode('uid')
            aduser.edit_user(uid,name,password)
        redirect('/usermgr')

@route('/userdel/<id:int>')
def userdel(id=0):
    admin_verify()
    if id:
        aduser.del_user(id)
    redirect('/usermgr')

@route('/chgpw/<uid:int>',method=["GET","POST"])
def chgpw(uid=0):
    id = login_verify()
    if uid != id:
        redirect('/admin')
    if request.method == "GET":
        name = request.get_cookie('adname',secret=secret)
        user_type = request.get_cookie('user_type',secret=secret)
        id = request.get_cookie('adid',secret=secret)
        return template('tpls/ad_tpls/chgpw.tpl',
            name=name,
            id=id,
            user_type=user_type)
    elif request.method == "POST":
        opassword = request.forms.getunicode('opassword').strip()
        npassword = request.forms.getunicode('npassword').strip()
        kpassword = request.forms.getunicode('kpassword').strip()
        name = request.get_cookie('adname',secret=secret)
        if opassword and npassword and\
            npassword == kpassword and opassword != npassword:
            aduser.ch_pw(uid,opassword,npassword,name)
            response.set_cookie('info','你密码更改，请重新登录！',secret=secret)
        redirect('/adlogout')


@route('/adlogout')
def logout():
    response.delete_cookie('adid')
    response.delete_cookie('user_type')
    response.delete_cookie('adname')
    redirect('/admin')