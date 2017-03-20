from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import io
import random
import os

def get_text():
    mystr = "ABCDEFGHJKMNPQRSTUVWXYZ"
    text = []
    for i in range(4):
        text.append(random.choice(mystr))
    random.shuffle(text)
    return ''.join(text)

def get_color():
    r = random.randint(0,255)
    g = random.randint(0,255)
    b = random.randint(0,255)
    return "rgb(%d,%d,%d)" % (r,g,b)

def make_noises(drw,lines=3):
    for i in range(3):
        drw.line((random.randint(5,10),random.randint(5,45),
            random.randint(60,75),random.randint(5,45)), fill='green', width=2)
    pnt = []
    for i in range(300):
        pnt.append((random.randint(5,75),random.randint(5,45)))
    drw.point(pnt,fill=get_color())

def get_verify():
    path = os.path.split(os.path.realpath(__file__))[0]
    a = Image.new('RGB',(80,50),'white')
    drw = ImageDraw.Draw(a)
    myfont = ImageFont.truetype(os.path.join(path,'swiss.ttf'),size=20)
    atext = get_text()
    drw.text((10,10),atext,font=myfont,fill='green')
    make_noises(drw)
    f = io.BytesIO()
    a.save(f,'JPEG')
    f.seek(0)
    return f.read(),atext