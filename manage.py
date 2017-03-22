import os
from bottle import route,run,error,static_file,request,response,template,redirect
from tools.verify_gen import get_verify
# import cmstools,mtools
from db import aduser,user,level,news,tools

secret = 'df%$%^&*()_++((*&^%$:""><<<Q#TG'
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

@route('/ckupload',method=["POST",])
def ckupload():
    admin_verify()
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

@route('/verify')
def verify():
    img,text = get_verify()
    response.set_cookie('verify_text',text,secret=secret)
    return img

@route('/admin',method=['GET','POST'])
def index():
    info = request.get_cookie('info',secret=secret)
    info = response.set_cookie('info','',secret=secret)
    response.set_cookie('info','',secret=secret)
    if request.method == 'GET':
        name = request.get_cookie('name',secret=secret)
        id = request.get_cookie('id',secret=secret)
        user_type = request.get_cookie('user_type',secret=secret)
        # print('.....',name,id,user_type)
        return template('tpls/index.tpl',
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
                response.set_cookie('name',u.name,secret=secret)
                response.set_cookie('id',str(u.id),secret=secret)
                response.set_cookie('user_type',u.user_type,secret=secret)
                return template('tpls/index.tpl',
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

def admin_verify(go_url='/admin'):
    user_type = request.get_cookie('user_type',secret=secret)
    if user_type != 100:
        response.set_cookie('info',
            "你未登录或无权限此项使用管理功能！",
            secret=secret)
        redirect(go_url)

def login_verify(go_url='/admin'):
    name = request.get_cookie('name',secret=secret)
    id = request.get_cookie('id',secret=secret)
    if name and id:
        return id
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
        name = request.get_cookie('name',secret=secret)
        id = request.get_cookie('id',secret=secret)
        return template('tpls/usermgr.tpl',
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

@route('/userdel/<id>')
def userdel(id=None):
    admin_verify()
    if id:
        aduser.del_user(id)
    redirect('/usermgr')

@route('/lvlmgr',method=["GET","POST"])
@route('/lvlmgr/<parent_lid>',method=["GET","POST"])
def lvlmgr(parent_lid=''):
    admin_verify()
    if request.method == 'GET':
        bread_nav = level.get_bread_nav(parent_lid)
        name = request.get_cookie('name',secret=secret)
        current_lvls = level.get_next_lvls(parent_lid)
        user_type = request.get_cookie('user_type',secret=secret)
        id = request.get_cookie('id',secret=secret)
        return template('tpls/lvlmgr.tpl',
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

@route('/lvldel/<lid>')
@route('/lvldel/<lid>/<parent_lid>')
def lvldel(lid='',parent_lid=''):
    admin_verify()
    if lid:
        level.del_levels(lid)
    url = ''.join(('/lvlmgr/',parent_lid)) if parent_lid else '/lvlmgr'
    redirect(url)

@route('/chgpw/<uid>',method=["GET","POST"])
def chgpw(uid):
    id = login_verify()
    if uid != id:
        redirect('/admin')
    if request.method == "GET":
        name = request.get_cookie('name',secret=secret)
        user_type = request.get_cookie('user_type',secret=secret)
        id = request.get_cookie('id',secret=secret)
        return template('tpls/chgpw.tpl',
            name=name,
            id=id,
            user_type=user_type)
    elif request.method == "POST":
        opassword = request.forms.getunicode('opassword').strip()
        npassword = request.forms.getunicode('npassword').strip()
        kpassword = request.forms.getunicode('kpassword').strip()
        name = request.get_cookie('name',secret=secret)
        if opassword and npassword and\
            npassword == kpassword and opassword != npassword:
            user.ch_pw(uid,opassword,npassword,name)
            response.set_cookie('info','你密码更改，请重新登录！',secret=secret)
        redirect('/logout')


@route('/ctxmgr',method=['GET','POST'])
@route('/ctxmgr/<lid>',method=['GET','POST'])
@route('/ctxmgr/<lid>/<page>',method=['GET','POST'])
def ctxmgr(lid='',page=0):
    uid = request.get_cookie('id',secret=secret)
    login_verify()
    if request.method == 'GET':
        name = request.get_cookie('name',secret=secret)
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
        newses = news.get_news(lid)
        return template('tpls/ctxmgr.tpl',
            name=name,
            id=uid,
            lid=lid,
            lname=level.get_lvl_name(lid) if lid else '',
            user_type=user_type,
            power=power,
            bread_nav=bread_nav_dec,
            next_lvls=next_lvls,
            news=newses)
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
    uid = request.get_cookie('id',secret=secret)
    for key in param_keys:
        nid = request.forms.getunicode(key)
        news.check_news(nid,uid,user_type)
    redirect('/ctxmgr/' + lid)

@route('/delctx/<nid>')
def delctx(nid):
    uid = request.get_cookie('id',secret=secret)
    if nid and uid:
        news.del_news(nid,uid)
    redirect('/ctxmgr/' + uid)

@route('/editctx/<lid>/<nid>',method=["GET","POST"])
def editctx(lid,nid):
    login_verify()
    name = request.get_cookie('name',secret=secret)
    user_type = request.get_cookie('user_type',secret=secret)
    uid = request.get_cookie('id',secret=secret)
    power = aduser.get_power(uid)
    if request.method == "GET":
        if nid:
            anews = news.get_one_news(nid,uid,user_type)
            if anews:
                return template('tpls/editctx.tpl',
                    id=uid,
                    lid=lid,
                    name=name,
                    power=power,
                    user_type=user_type,
                    news=anews)
        redirect('/ctxmgr/' + lid)
    elif request.method == "POST":
        title = request.forms.getunicode('title')
        txt = request.forms.getunicode('txt')
        uid = request.get_cookie('id',secret=secret)
        if nid:
            news.edit_news(nid,uid,title,txt,user_type)
        redirect('/ctxmgr/' + lid)

@route('/imgmgr',method=['GET','POST'])
def imgmgr():
    info = request.get_cookie('info',secret=secret)
    response.set_cookie('info','',secret=secret)
    uid = request.get_cookie('id',secret=secret)
    login_verify()
    if request.method == 'GET':
        name = request.get_cookie('name',secret=secret)
        user_type = request.get_cookie('user_type',secret=secret)
        return template('tpls/imgmgr.tpl',
            name=name,
            id=uid,
            user_type=user_type,
            info=info,
            )
    elif request.method == "POST":
        info = "上传成功！"
        upload = request.files.get('upload')
        fname,fext = os.path.splitext(upload.filename)
        if fext in ['.jpg','.jpeg','.png','.gif']:
            rootpath = './activeimg'
            if not os.path.exists(rootpath):
                os.makedirs(rootpath)
            while os.path.exists('/'.join((rootpath,fname+fext))):
                fname += 'c'
            # upload.save('/'.join((rootpath,fname+fext)))
            from PIL import Image
            myimg = Image.open(upload.file)
            myimg.thumbnail((240,160))
            myimg.save('/'.join((rootpath,fname+fext)))
        else:
            info = '上传失败，你上传的不是图片文件。'
        response.set_cookie('info',info,secret=secret)
        redirect('/imgmgr')

@route('/logout')
def logout():
    response.delete_cookie('id')
    response.delete_cookie('user_type')
    response.delete_cookie('name')
    redirect('/')

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
@route('/<plid:int>/<page>',method=["GET",])
def pindex(plid='0',page=1):
    info = request.get_cookie('info',secret=secret)
    info = response.set_cookie('info','',secret=secret)
    response.set_cookie('info','',secret=secret)
    navs = level.get_next_lvls(plid)
    mnewslist,pages = news.get_lvl_page_news(int(plid),limit=20,page=int(page)-1)
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

@route('/news/<nid>')
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

@route('/me/<uid>',method=['GET','POST'])
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




ADD_AMDIN = True
DEFAULT_ADMIN = {'name':'adm','password':'123'}

if __name__ == '__main__':
    from db.cms import db_init
    db_init()
    if ADD_AMDIN:
        aduser.add_admin_user(**DEFAULT_ADMIN)
    run(port=9099,debug=True,reloader=True)
    # run(server='waitress',port=9099,debug=True,reloader=True)