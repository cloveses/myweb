# -*- coding:utf-8 -*-

import os
import re
from .botapp import app
from bottle import route,request,response,template,redirect
from db import aduser,level,news,tools
from setting import secret
from .ad_user import login_verify

@app.route('/imgmgr',method=['GET','POST'])
def imgmgr():
    info = request.get_cookie('info',secret=secret)
    response.set_cookie('info','',secret=secret)
    uid = request.get_cookie('adid',secret=secret)
    login_verify()
    if request.method == 'GET':
        name = request.get_cookie('adname',secret=secret)
        user_type = request.get_cookie('user_type',secret=secret)
        return template('tpls/ad_tpls/imgmgr.tpl',
            name=name,
            id=uid,
            user_type=user_type,
            info=info,
            )
    elif request.method == "POST":
        info = "上传成功！"
        upload = request.files.get('upload')
        fname = request.forms.get('titlename')
        if not isinstance(fname, str):
            fname = fname.decode('utf8', 'ignore')
        fname = fname[:10]
        fname = re.sub(r'\s+','',fname)
        if '.' not in upload.filename:
            fext = '.' + upload.filename
        else:
            fext = os.path.splitext(upload.filename)[1]
        # fname,fext = os.path.splitext(upload.filename)
#      纯动态部署可以用以下注释的部分
#         if fext in ['.jpg','.jpeg','.png','.gif']:
#             rootpath = './activeimg'
#             if not os.path.exists(rootpath):
#                 os.makedirs(rootpath)
#             while os.path.exists('/'.join((rootpath,fname+fext))):
#                 fname += 'c'
#             # upload.save('/'.join((rootpath,fname+fext)))
#             from PIL import Image
#             myimg = Image.open(upload.file)
#             myimg.thumbnail((240,160))
#             myimg.save('/'.join((rootpath,fname+fext)))
        if fext in ['.jpg','.jpeg','.png','.gif']:
        # 修改为两个目录同时保存，使得动态测试和静态服务正常
            rootpaths = ('./activeimg','./active')
            from PIL import Image
            myimg = Image.open(upload.file)
            myimg.thumbnail((240,160))
            for rootpath in rootpaths:
                # rootpath = './activeimg'
                if not os.path.exists(rootpath):
                    os.makedirs(rootpath)
                while os.path.exists('/'.join((rootpath,fname+fext))):
                    fname += 'c'
                # upload.save('/'.join((rootpath,fname+fext)))
                myimg.save('/'.join((rootpath,fname+fext)))
        else:
            info = '上传失败，你上传的不是图片文件。'
        response.set_cookie('info',info,secret=secret)
        redirect('/imgmgr')
