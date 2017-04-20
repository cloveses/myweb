import hashlib
import os

SALT = '&**&^#@@hjkjk^GGIO))(&^&^^}{HYJjg>?<MM?!@@'

def make_pw(name,password):
    pw = hashlib.sha512(SALT.join((name,password)).encode())
    pw = pw.hexdigest()
    return pw

def get_power(powerstr):
    if not powerstr:
        return set()
    power = set(powerstr.split(','))
    power = {int(i) for i in power}
    return power

def power_to_str(powerset):
    power = {str(i) for i in powerset}
    return ','.join(power)

def get_imgs(path,nums=10):
    if os.path.exists(path):
        files = list(os.walk(path))[0][2]
        if not files:
            return []
        return sorted(files,key=lambda fn:os.path.getctime(path+fn))[:-10:-1]
    return []

def get_pages(sum_pages,page,p=3):
    min_page = page - p if page - p >= 0 else 0
    max_page = min_page + p * 2 + 1
    if max_page > sum_pages:
        max_page = sum_pages
    return [i for i in range(min_page,max_page)]
