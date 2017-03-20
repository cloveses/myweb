from .cms import Level,News,User,ses
from .level import get_bread_nav,get_sub_lvls
from .tools import get_power,power_to_str

def get_anews(nid):
    news = ses.query(News).filter_by(id=nid).first()
    return news

def add_news(title,txt,lid,uid):
    u = ses.query(User).filter_by(id=uid).first()
    if lid in get_power(u.power) or u.user_type == 100:
        news = News(title=title,txt=txt,author=u.name,category=lid)
        ses.add(news)
        ses.commit()

def has_power(lid,powers):
    powers = get_power(powers)
    parents = get_bread_nav(lid)
    parents = {i[0] for i in parents}
    parents.add(lid)
    if powers.intersection(parents):
        return True

def get_one_news(nid,uid,user_type):
    news = ses.query(News).filter_by(id=nid).first()
    u = ses.query(User).filter_by(id=uid).first()
    if news.author == u.name or has_power(lid,u.power) or user_type==100:
        return news

def edit_news(nid,uid,title,txt,user_type):
    news = get_one_news(nid,uid,user_type)
    if news:
        news.title = title
        news.txt = txt
        ses.commit()

def del_news(nid,uid):
    news = ses.query(News).filter_by(id=nid).first()
    u = ses.query(User).filter_by(id=uid).first()
    if has_power(news.category,u.power):
        ses.delete(news)
        ses.commit()

def check_news(nid,uid,user_type):
    news = ses.query(News).filter_by(id=nid).first()
    u = ses.query(User).filter_by(id=uid).first()
    if news and u and has_power(news.category,u.power) or user_type==100:
        news.is_released = True
        ses.commit()

def get_news(lid='',limit=10,page=0):
    if not lid:
        return []
    sub_ids = []
    if lid:
        sub_lvls = get_sub_lvls(lid)
        sub_ids.append(lid)
        sub_ids.extend([i.id for i in sub_lvls])
    else:
        sub_lvls = ses.query(Level).filter_by(c=0).all()
        sub_ids = [i.id for i in sub_lvls]
    if sub_ids:
        start = page * limit
        res = ses.query(News).filter(News.category.in_(sub_ids)).\
                        order_by(News.release_date).all()[::-1]
        if res:
            return res[start:limit + 1]
    return []

def get_lvl_news(lid):
    if lid:
        res = ses.query(News).filter(News.category==lid).\
                        order_by(News.release_date).all()[::-1]
        return res if res else []
    return []

def get_lvl_page_news(lid,limit=10,page=0):
    if lid:
        res = ses.query(News).filter(News.category==lid).\
                        order_by(News.release_date).all()[::-1]
        pages = list(range(0,len(res),limit))
        pages = [i // limit + 1 for i in pages]
        return [res,pages] if res else [[],[]]
    return [[],[]]

def get_last_news(sub_ids,limit=3):
    r = News.objects(id__in=sub_ids).order_by('-release_date')[0:limit]
    res = ses.query(News).filter(News.category.in_(sub_ids)).\
                        order_by(News.release_date).all()[::-1]
    return r if r else []