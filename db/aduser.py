from .tools import make_pw,power_to_str
from .tools import get_power as get_power_set
from .cms import User,ses
from .level import get_sub_lvls,get_lvl_name,lid_to_lvl

def add_user(name,password):
    pw = make_pw(name,password)
    u = User(name=name,password=pw)
    ses.add(u)
    ses.commit()
    return u

def add_admin_user(name,password):
    admin_users = ses.query(User).filter(User.user_type==100).all()
    if not admin_users:
        u = add_user(name,password)
        u.user_type = 100
        ses.add(u)
        ses.commit()

def edit_user(uid,name,password):
    u = ses.query(User).filter(User.id == uid).first()
    if u:
        if name:
            u.name = name
        if password:
            u.password = make_pw(name,password)
        ses.commit()

def ch_pw(uid,opw,npw,name):
    opw = make_pw(name,opw)
    u = ses.query(User).filter(User.id == uid).filter_by(password=opw).first()
    if not u:
        return False
    npw = make_pw(u.name,npw)
    u.password = npw
    ses.commit()
    return u

def login(name,pw):
    pw = make_pw(name,pw)
    u = ses.query(User).filter_by(name=name).filter_by(password=pw).first()
    if not u:
        return False
    return u

def get_users():
    users = ses.query(User).filter(User.user_type != 100).all()
    return users if users else []

def del_user(uid):
    u = ses.query(User).filter(User.id == uid).first()
    if u:
        ses.delete(u)
        ses.commit()

def get_power(uid):
    u = ses.query(User).filter(User.id == uid).first()
    if u:
        if u.user_type == 100:
            return get_sub_lvls(0)
        else:
            res = get_power_set(u.power) if u.power else []
            return [lid_to_lvl(i) for i in res]
    return []

def add_power(uids,powerids):
    if not uids:
        return
    uids = set(map(int,uids))
    powerids = ','.join(powerids)
    users = ses.query(User).filter(User.id.in_(uids)).all()
    for u in users:
        u.power = powerids
    ses.commit()
    return True

def get_user_power(users):
    if not users:
        return []
    user_powers = []
    for u in users:
        powers = get_power_set(u.power)
        if powers:
            user_powers.append(','.join([get_lvl_name(i) for i in powers]))
        else:
            user_powers.append('')
    return user_powers