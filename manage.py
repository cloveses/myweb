# -*- coding:utf-8 -*-

from bottle import run
from setting import DEFAULT_ADMIN,ADD_AMDIN
from web.common import *
from web.ad_index import *
from web.ad_user import *
from web.ad_lvl import *
from web.ad_ctx import *
from web.ad_actimg import *
from web.myweb import *

if __name__ == '__main__':
##    from db.cms import db_init
##    db_init()
##    if ADD_AMDIN:
##        aduser.add_admin_user(**DEFAULT_ADMIN)
    run(app=app,server='waitress',host='60.175.231.170',port=9099,reloader=True)
