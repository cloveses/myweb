from .tools import make_pw
from .cms import OrdUser,ses

def login(name,password):
    password = make_pw(name,password)
    u = ses.query(OrdUser).filter_by(name=name).filter_by(password=password)
    u = u.first()
    return u if u else False

def reg_user(name,password):
    password = make_pw(name,password)
    ou = OrdUser(name=name,password=password)
    ses.add(ou)
    ses.commit()
    return ou

def ch_pw(oid,name,opw,npw):
    opw = make_pw(name,opw)
    ou = OrdUser.objects(id=ObjectId(oid)).filter(password=opw)
    ou = ses.query(OrdUser).filter_by(name=name).filter_by(password=password)
    ou = ou.first()
    if ou:
        ou.password = make_pw(name,npw)
        ses.commit()
        return True
    return False