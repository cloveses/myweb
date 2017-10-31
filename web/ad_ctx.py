# -*- coding:utf-8 -*-

import os
from .botapp import app
from bottle import route,request,response,template,redirect
from db import aduser,level,news,tools
from setting import secret
from .ad_user import login_verify

@app.route('/ckupload',method=["POST",])
def ckupload():
    login_verify()
    upload = request.files.get('upload')
    fname,fext = os.path.splitext(upload.filename)
    rootpath = './uploads'
    if not os.path.exists(rootpath):
        os.makedirs(rootpath)
    while os.path.exists('/'.join((rootpath,fname+fext))):
        fname += 'c'
    callback = request.GET.getunicode('CKEditorFuncNum')
    upload.save('/'.join((rootpath,fname+fext)))
    restr = "<script type=\"text/javascript\">"
    restr += "window.parent.CKEDITOR.tools.callFunction("+ callback + ",'" +"/img/"+ fname + fext + "','')"
    restr += "</script>"
    return restr


@app.route('/ctxmgr',method=['GET','POST'])
@app.route('/ctxmgr/<lid:int>',method=['GET','POST'])
@app.route('/ctxmgr/<lid:int>/<page:int>',method=['GET','POST'])
def ctxmgr(lid=0,page=0):
    uid = request.get_cookie('adid',secret=secret)
    login_verify()
    if request.method == 'GET':
        name = request.get_cookie('adname',secret=secret)
        user_type = request.get_cookie('user_type',secret=secret)
        power = aduser.get_power(uid)
        powers = []
        next_lvls = []
        bread_nav_dec = []
        if power:
            for p in power:
                powers.append(level.get_sub_lvls(p.id))
        if powers and lid:
            lid = int(lid)
            bread_nav = level.get_bread_nav(lid)
            ids = set().union(*powers)
            ids = {i.id for i in ids}
            for bn in bread_nav:
                if bn[0] in ids:
                    bread_nav_dec.append(bn)
            next_lvls = level.get_next_lvls(lid)
        newses,sum_pages = news.get_news(lid,page=page)
        pages = tools.get_pages(sum_pages,page)
        return template('tpls/ad_tpls/ctxmgr.tpl',
            name=name,
            id=uid,
            lid=lid,
            lname=level.get_lvl_name(lid) if lid else '',
            user_type=user_type,
            power=power,
            bread_nav=bread_nav_dec,
            next_lvls=next_lvls,
            news=newses,
            page=page,
            pages=pages)
    elif request.method == "POST":
        action = request.forms.getunicode('action')
        if action == "add":
            add_ctx()
        elif action == "release":
            # print('.........',action)
            release()

def add_ctx():
    title = request.forms.getunicode('title')
    uid = request.forms.getunicode('uid')
    lid = request.forms.getunicode('lid')
    txt = request.forms.getunicode('txt')
    if title and uid and lid and txt:
        news.add_news(title,txt,lid,uid)
    redirect('/ctxmgr/' + lid if lid else '/ctxmgr')

def release():
    key_suffix = '-rels'
    param_keys = [i for i in request.forms.keys() if i.endswith(key_suffix)]
    user_type = request.get_cookie('user_type',secret=secret)
    lid = request.forms.getunicode('lid')
    uid = request.get_cookie('adid',secret=secret)
    for key in param_keys:
        nid = request.forms.getunicode(key)
        news.check_news(nid,uid,user_type)
    redirect('/ctxmgr/' + lid)

@app.route('/delctx/<nid:int>/<lid:int>')
@app.route('/delctx/<nid:int>/<lid:int>/<page:int>')
def delctx(nid,lid,page=0):
    login_verify()
    uid = request.get_cookie('adid',secret=secret)
    user_type = request.get_cookie('user_type',secret=secret)
    if nid and uid:
        news.del_news(nid,uid,user_type)
    url = '/'.join(('/ctxmgr',str(lid)))
    if page:
        url += '/' + str(page)
    redirect(url)

@app.route('/editctx/<lid:int>/<nid:int>',method=["GET","POST"])
@app.route('/editctx/<lid:int>/<nid:int>/<page:int>',method=["GET","POST"])
def editctx(lid,nid,page=0):
    login_verify()
    name = request.get_cookie('adname',secret=secret)
    user_type = request.get_cookie('user_type',secret=secret)
    uid = request.get_cookie('adid',secret=secret)
    power = aduser.get_power(uid)
    url = '/ctxmgr/' + str(lid)
    if page:
        url += '/' + str(page)
    if request.method == "GET":
        if nid:
            anews = news.get_one_news(nid,uid,user_type)
            if anews:
                return template('tpls/ad_tpls/editctx.tpl',
                    id=uid,
                    lid=lid,
                    name=name,
                    power=power,
                    user_type=user_type,
                    news=anews)
        redirect(url)
    elif request.method == "POST":
        title = request.forms.getunicode('title')
        txt = request.forms.getunicode('txt')
        uid = request.get_cookie('adid',secret=secret)
        if nid:
            news.edit_news(nid,uid,title,txt,user_type)
        redirect(url)
