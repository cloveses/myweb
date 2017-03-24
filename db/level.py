from sqlalchemy.sql import func
from .cms import Level,ses

def lid_to_lvl(lid):
    if lid:
        return ses.query(Level).filter_by(id=lid).first()

def get_pos(parent_r):
    lvln = ses.query(Level).filter_by(r=parent_r).first()
    if not lvln:
        return None
    lvls = ses.query(Level).filter(Level.r>parent_r).order_by(Level.r)
    if lvls:
        for lvl in lvls:
            if lvl.c <= lvln.c:
                return lvl.r,lvln.c + 1
            else:
                return lvl.r + 1,lvln.c + 1
    return lvln.r + 1,lvln.c + 1

def move_after(r):
    lvls = ses.query(Level).filter(Level.r >= r).order_by(Level.r)[::-1]
    if lvls:
        for lvl in lvls:
            lvl.r += 1
            ses.commit()

def insert_lvl(name,parent_r):
    r_c = get_pos(parent_r)
    if r_c:
        r,c = r_c
        move_after(r)
        ses.add(Level(name=name,r=r,c=c))
        ses.commit()
    else:
        r = ses.query(func.max(Level.r))
        r += 1
        ses.add(Level(name=name,r=r,c=0))
        ses.commit()


def move_before(r):
    lvls = ses.query(Level).filter(Level.r >= r).order_by(Level.r)
    if lvls:
        for lvl in lvls:
            lvl.r += 1
            ses.commit()

def insert_before_lvl(name,after_lid):
    after_lvl = lid_to_lvl(after_lid)
    if after_lvl:
        r = after_lvl.r
        c = after_lvl.c
        move_after(r)
        ses.add(Level(name=name,r=r,c=c))
        ses.commit()

def add_level(name,parent_lid=0):
    if parent_lid == 0:
        r = ses.query(func.max(Level.r)).first()
        r = r[0]
        r= 1 if (r is None) else r + 1
        ses.add(Level(name=name,r=r,c=0))
        ses.commit()
    else:
        plvl = ses.query(Level).filter_by(id=parent_lid).first()
        insert_lvl(name,plvl.r)

def edit_level(name,lid):
    lvl = ses.query(Level).filter_by(id=lid).first()
    if lvl:
        lvl.name = name
        ses.commit()

def get_lvls():
    res = ses.query(Level).all()
    return res if res else []

def get_sub_lvls(lid):
    if lid == 0:
        res = ses.query(Level).filter_by(c=0).order_by(Level.r).all()
        return res if res else []
    v = ses.query(Level).filter_by(id=lid).first()
    if v:
        lvls = ses.query(Level).filter(Level.r>v.r).order_by(Level.r)
        sub_lvls = []
        for sub_lvl in lvls:
            if sub_lvl.c > v.c:
                sub_lvls.append(sub_lvl)
            else:
                break
        return sub_lvls if sub_lvls else []
    return []

def get_lvl(lid):
    return ses.query(Level).filter_by(id=lid).first()

def del_level(lid):
    lvl = ses.query(Level).filter_by(id=lid).first()
    if lvl:
        r = lvl.r
        ses.delete(lvl)
        ses.commit()
        move_before(r)

def del_levels(lid):
    if lid:
        sub_lvls = get_sub_lvls(lid)
        for l in sub_lvls:
            del_level(l.id)
        del_level(lid)

def get_parent_lvl(lid):
    v = ses.query(Level).filter_by(id=lid).first()
    if v:
        res = ses.query(Level).filter(Level.r<v.r).order_by(Level.r).all()
        if res:
            for lvl in res[::-1]:
                if lvl.c == v.c - 1:
                    return lvl

def get_bread_nav(lid):
    if lid:
        lvl = ses.query(Level).filter_by(id=lid).first()
        if lvl:
            ids = [(lid,lvl.name),]
            if lvl.c == 0:
                return ids
            res = ses.query(Level).filter(Level.id<lvl.r).order_by(Level.r).all()[::-1]
            cc = lvl.c
            for v in res:
                if v.c == cc - 1:
                    ids.append((v.id,v.name))
                    cc -= 1
                if cc <= 0:
                    break
            ids.reverse()
            return ids
    return []


def get_brother_lvls(lid):
    lvl = lid_to_lvl(lid)
    if lvl.c == 0:
        res = ses.query(Level).filter_by(c=0).order_by(Level.r).all()
        return res if res else []
    pv = get_parent_lvl(lid)
    if pv:
        sub = get_sub_lvls(pv.id)
        if sub:
            r = [v for v in sub if v.c == pv.c + 1]
            return r if r else []
    return []

def get_next_lvls(parent_lid):
    if parent_lid:
        plvl = ses.query(Level).filter_by(id=parent_lid).first()
        if plvl:
            sub_lvls = get_sub_lvls(parent_lid)
            # for l in sub_lvls:
            #     print(l.id,l.name,l.r,l.c)
            if sub_lvls:
                r = [v for v in sub_lvls if v.c -1 == plvl.c]
                return r if r else []
    else:
        res = ses.query(Level).filter_by(c=0).order_by(Level.r).all()
        return res if res else []
    return []

def get_lvl_name(lid):
    lvl = ses.query(Level).filter_by(id=lid).first()
    if lvl:
        return lvl.name