# -*- coding:utf-8 -*-

import os
from bottle import route,run,error,static_file,request,response,template,redirect
from db import user,level,news,tools
from setting import secret

@route('/',method=["GET","POST"])
def mindex():
    info = request.get_cookie('info',secret=secret)
    info = response.set_cookie('info','',secret=secret)
    response.set_cookie('info','',secret=secret)
    navs = level.get_next_lvls('')
    newslist = [(nav,news.get_lvl_news(str(nav.id))[:7]) 
                for nav in navs]
    activeimgs = tools.get_imgs('./activeimg/')
    activeimgs = ['/active/'+i for i in activeimgs]
    if request.method == 'GET':
        name = request.get_cookie('name',secret=secret)
        id = request.get_cookie('id',secret=secret)
        return template('tpls/mindex.tpl',
            name=name,
            id=id,
            info=info,
            navs=navs,
            newslist=newslist,
            plid='',
            activeimgs=activeimgs,
            )
    elif request.method == 'POST':
        verify_text = request.get_cookie('verify_text',secret=secret)
        response.set_cookie('verify_text','',secret=secret)
        if verify_text and verify_text.lower() == \
            request.forms.getunicode('verify_text').lower().strip():
            name = request.forms.getunicode('name')
            password = request.forms.getunicode('password')
            u = user.login(name,password)
            if u:
                response.set_cookie('name',u.name,secret=secret)
                response.set_cookie('id',str(u.id),secret=secret)
                return template('tpls/mindex.tpl',
                    name=name,
                    id=str(u.id),
                    info=info,
                    navs=navs,
                    newslist=newslist,
                    plid='',
                    activeimgs=activeimgs,
                    )
            else:
                response.set_cookie('info',
                    "登录失败，请检查用户名或密码！",
                    secret=secret)
        else:
            response.set_cookie('info',"验证码错误，请重新登录！",
                secret=secret)
        redirect('/')

@route('/<plid:int>',method=["GET",])
@route('/<plid:int>/<page:int>',method=["GET",])
def pindex(plid='0',page=0):
    info = request.get_cookie('info',secret=secret)
    info = response.set_cookie('info','',secret=secret)
    response.set_cookie('info','',secret=secret)
    navs = level.get_next_lvls(plid)
    mnewslist,sum_pages = news.get_lvl_page_news(plid,limit=20,page=page)
    pages = tools.get_pages(sum_pages,page)
    all_navs = [level.get_lvl(plid),]
    all_navs.extend(navs)
    newslist = [(nav,news.get_lvl_news(str(nav.id))[:7]) 
                for nav in navs]
    name = request.get_cookie('name',secret=secret)
    id = request.get_cookie('id',secret=secret)
    return template('tpls/more.tpl',
        name=name,
        id=id,
        info=info,
        navs=all_navs,
        mnewslist=mnewslist,
        pages=pages,
        newslist=newslist,
        plid=str(plid)
        )

@route('/news/<nid:int>')
def detail(nid,plid=''):
    navs = level.get_next_lvls('')
    anews = news.get_anews(nid)
    more_news = news.get_lvl_news(anews.category)[:15]
    name = request.get_cookie('name',secret=secret)
    id = request.get_cookie('id',secret=secret)
    return template('tpls/detail.tpl',
        name=name,
        id=id,
        navs=navs,
        news=anews,
        more_news=more_news,
        plid=plid
        )


@route('/signup',method=["GET","POST"])
def signup():
    if request.method == "GET":
        info = request.get_cookie('info',secret=secret)
        return template('tpls/signup.tpl',info=info)
    elif request.method == "POST":
        name = request.forms.getunicode('name')
        password = request.forms.getunicode('password')
        vpassword = request.forms.getunicode('vpassword')
        verify_text = request.forms.getunicode('verify_text')
        response.set_cookie('verify_text','',secret=secret)
        v_t = request.get_cookie('verify_text',secret=secret)
        info = ''
        if verify_text.strip().lower() == v_t.lower():
            if name and password == vpassword:
                ou = user.reg_user(name,password)
                if ou:
                    response.set_cookie('name',name,secret=secret)
                    response.set_cookie('id',str(ou.id),secret=secret)
                    redirect('/')
                else:
                    info = '注册发生错误，请与管理员联系。'
            else:
                info = '密码不匹配！' if name else '姓名不能为空！' 
        else:
            info = '验证码错误！'
        response.set_cookie('info',info,secret=secret)
        redirect('/signup')

@route('/me/<uid:int>',method=['GET','POST'])
def meo(uid):
    if request.method == 'GET':
        info = request.get_cookie('info',secret=secret)
        response.set_cookie('info','',secret=secret)
        name = request.get_cookie('name',secret=secret)
        id = request.get_cookie('id',secret=secret)
        if name and id and uid:
            return template('tpls/me.tpl',name=name,id=id,info=info)
        else:
            response.set_cookie('info','请先登录！',secret=secret)
            redirect('/')
    else:
        chn_pw(uid)

def chn_pw(uid):
    opassword = request.forms.getunicode('opassword')
    npassword = request.forms.getunicode('npassword')
    kpassword = request.forms.getunicode('kpassword')
    name = request.get_cookie('name',secret=secret)
    if npassword and npassword == kpassword:
        user.ch_pw(uid,name,opassword,npassword)
        redirect('/logout')
    else:
        response.set_cookie('info','可能是密码不匹配或为空！',secret=secret)
        redirect('/me/%s' % uid)

@route('/logout')
def logout():
    response.delete_cookie('id')
    response.delete_cookie('name')
    redirect('/')