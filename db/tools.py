import hashlib

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