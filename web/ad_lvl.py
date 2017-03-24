# -*- coding:utf-8 -*-

import os
from bottle import route,request,response,template,redirect
from db import aduser,level,news,tools
from setting import secret
from .ad_user import admin_verify

@route('/lvlmgr',method=["GET","POST"])
@route('/lvlmgr/<parent_lid:int>',method=["GET","POST"])
def lvlmgr(parent_lid=0):
    admin_verify()
    if request.method == 'GET':
        bread_nav = level.get_bread_nav(parent_lid)
        name = request.get_cookie('adname',secret=secret)
        current_lvls = level.get_next_lvls(parent_lid)
        user_type = request.get_cookie('user_type',secret=secret)
        id = request.get_cookie('adid',secret=secret)
        return template('tpls/ad_tpls/lvlmgr.tpl',
            name=name,
            id=id,
            current_lvls=current_lvls,
            parent_lid=parent_lid,
            bread_nav=bread_nav,
            user_type=user_type)
    if request.method == 'POST':
        action = request.forms.getunicode('action')
        if action == 'add':
            name = request.forms.getunicode('name')
            parent_lid = request.forms.getunicode('parent_lid')
            level.add_level(name,parent_lid)
        elif action == 'edit':
            name = request.forms.getunicode('name').strip()
            lid = request.forms.getunicode('lid')
            level.edit_level(name,lid)
        elif action == 'insert':
            name = request.forms.getunicode('name').strip()
            lid = request.forms.getunicode('lid')
            level.insert_before_lvl(name,lid)
        url = '/lvlmgr/' + parent_lid if parent_lid else '/lvlmgr'
        redirect(url)

@route('/lvldel/<lid:int>')
@route('/lvldel/<lid:int>/<parent_lid:int>')
def lvldel(lid=0,parent_lid=0):
    admin_verify()
    if lid:
        level.del_levels(lid)
    url = ''.join(('/lvlmgr/',parent_lid)) if parent_lid else '/lvlmgr'
    redirect(url)