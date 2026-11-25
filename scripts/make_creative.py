"""Techmed Smart Sense GBP creative, 900x500. Usage: make_creative.py config.json out.jpg"""
import sys, json, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
cfg=json.load(open(sys.argv[1])); out=sys.argv[2]
S=2; W,H=900*S,500*S
BLUE=(38,84,170); LBLUE=(70,118,200); GREEN=(62,150,48); LGREEN=(170,210,140); NAVY=(14,40,90); GREY=(95,105,120); WHITE=(255,255,255)
HERE=os.path.dirname(os.path.abspath(__file__))
FD="/usr/share/fonts/opentype/inter/"
def F(w,sz):
    try: return ImageFont.truetype(FD+"Inter-%s.otf"%w,int(sz*S))
    except Exception: return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",int(sz*S))
s=lambda *a:[int(v*S) for v in a]
img=Image.new("RGB",(W,H),WHITE); d=ImageDraw.Draw(img)
# background: light lab/shelf feel
for y in range(H):
    t=y/H; d.line([(0,y),(W,y)],fill=(int(236+14*t),int(243+8*t),int(250+4*t)))
for i in range(5):  # soft shelf bokeh
    x=60+i*190; d.rounded_rectangle(s(x,120,x+120,330),radius=14*S,fill=(228,238,248))
img=img.filter(ImageFilter.GaussianBlur(10*S)); d=ImageDraw.Draw(img)
# logo
logo=Image.open(os.path.join(HERE,"..","assets","logo.png")).convert("RGBA")
lh=64*S; lw=int(logo.width*lh/logo.height); logo=logo.resize((lw,lh),Image.LANCZOS)
img.paste(logo,s(22,14),logo)
d.text(s(24,82),cfg.get("tagline","Smart Monitoring. Safer Tomorrow."),font=F("SemiBold",13),fill=BLUE)
# headline
y=112
d.text(s(24,y),cfg["headline"][0],font=F("ExtraBold",32),fill=BLUE)
d.text(s(24,y+38),cfg["headline"][1],font=F("ExtraBold",32),fill=GREEN)
d.text(s(24,y+82),cfg["subtitle"],font=F("SemiBold",17),fill=NAVY)
# feature row (2x2)
icons={}
def circle_icon(cx,cy,r,kind,fg=BLUE,bg=WHITE,ring=LBLUE):
    d.ellipse(s(cx-r,cy-r,cx+r,cy+r),fill=bg,outline=ring,width=2*S)
    g=lambda *a:s(*[cx+v for v in a[:1]])  # unused
    def P(dx,dy): return (int((cx+dx)*S),int((cy+dy)*S))
    w=3*S
    if kind=="check": d.line([P(-8,0),P(-2,7),P(9,-7)],fill=fg,width=w)
    elif kind=="bell":
        d.pieslice([P(-9,-11),P(9,7)],180,360,fill=fg); d.rectangle([P(-9,-2),P(9,6)],fill=fg); d.ellipse([P(-3,7),P(3,12)],fill=fg)
    elif kind=="cloud":
        d.ellipse([P(-11,-3),P(-1,8)],fill=fg); d.ellipse([P(-6,-10),P(6,4)],fill=fg); d.ellipse([P(2,-4),P(12,8)],fill=fg); d.rectangle([P(-6,2),P(7,8)],fill=fg)
    elif kind=="chart":
        for i,hh in enumerate((8,15,11)): d.rectangle([P(-10+i*8,10-hh),P(-5+i*8,10)],fill=fg)
    elif kind=="shield": d.polygon([P(0,-11),P(10,-7),P(8,5),P(0,12),P(-8,5),P(-10,-7)],fill=fg)
    elif kind=="clock":
        d.ellipse([P(-11,-11),P(11,11)],outline=fg,width=w); d.line([P(0,0),P(0,-7)],fill=fg,width=w); d.line([P(0,0),P(6,3)],fill=fg,width=w)
    elif kind=="snow":
        d.line([P(0,-11),P(0,11)],fill=fg,width=w); d.line([P(-10,-5),P(10,5)],fill=fg,width=w); d.line([P(-10,5),P(10,-5)],fill=fg,width=w)
    elif kind=="pill":
        d.rounded_rectangle([P(-12,-5),P(12,5)],radius=5*S,fill=fg); d.rectangle([P(0,-5),P(3,5)],fill=bg)
    elif kind=="hospital":
        d.rectangle([P(-10,-10),P(10,10)],outline=fg,width=w); d.line([P(0,-5),P(0,5)],fill=fg,width=w); d.line([P(-5,0),P(5,0)],fill=fg,width=w)
    elif kind=="flask":
        d.rectangle([P(-3,-11),P(3,-3)],fill=fg); d.polygon([P(-3,-3),P(3,-3),P(11,10),P(-11,10)],fill=fg)
    elif kind=="truck":
        d.rectangle([P(-12,-8),P(3,5)],fill=fg); d.rectangle([P(4,-3),P(12,5)],fill=fg); d.ellipse([P(-9,3),P(-3,10)],fill=fg,outline=bg); d.ellipse([P(4,3),P(10,10)],fill=fg,outline=bg)
    elif kind=="building":
        d.rectangle([P(-9,-11),P(9,11)],fill=fg)
        for yy in (-6,0,6):
            for xx in (-5,2): d.rectangle([P(xx,yy),P(xx+3,yy+3)],fill=bg)
    elif kind=="food": d.ellipse([P(-9,-6),P(9,11)],fill=fg); d.line([P(0,-6),P(0,-11)],fill=fg,width=w)
    else: d.ellipse([P(-4,-4),P(4,4)],fill=fg)
feats=cfg["features"]
fx,fy=24,222
for i,(ic,t1,t2) in enumerate(feats):
    cx=fx+(i%2)*258; cy=fy+(i//2)*64
    circle_icon(cx+24,cy+24,24,ic)
    d.text(s(cx+58,cy+4),t1,font=F("Bold",16),fill=NAVY)
    d.text(s(cx+58,cy+25),t2,font=F("Regular",12),fill=GREY)
# device illustration (right)
dx,dy=640,126
d.ellipse(s(dx-20,dy+190,dx+250,dy+232),fill=(214,226,240))
d.ellipse(s(dx-10,dy+178,dx+240,dy+216),fill=(236,242,250))
sh=Image.new("RGBA",(W,H),(0,0,0,0)); sd=ImageDraw.Draw(sh)
sd.rounded_rectangle(s(dx+16,dy+30,dx+226,dy+196),radius=18*S,fill=(0,0,0,70)); sh=sh.filter(ImageFilter.GaussianBlur(8*S))
img.paste(sh,(0,0),sh); d=ImageDraw.Draw(img)
d.rounded_rectangle(s(dx+10,dy+20,dx+220,dy+182),radius=18*S,fill=(250,251,253),outline=(205,214,226),width=2*S)
d.rounded_rectangle(s(dx+10,dy+20,dx+220,dy+36),radius=8*S,fill=(255,150,40))
d.rounded_rectangle(s(dx+34,dy+52,dx+196,dy+112),radius=8*S,fill=(18,24,34))
d.text(s(dx+46,dy+60),cfg.get("device_time","13:59"),font=F("Medium",13),fill=(150,220,230))
d.text(s(dx+46,dy+78),cfg.get("device_reading","23.4 °C"),font=F("Bold",26),fill=(235,250,255))
d.text(s(dx+34,dy+126),cfg.get("device_label","TSS Data Logger"),font=F("Bold",13),fill=NAVY)
d.ellipse(s(dx+34,dy+152,dx+44,dy+162),fill=(60,180,90)); d.ellipse(s(dx+52,dy+152,dx+62,dy+162),fill=(255,150,40))
d.rounded_rectangle(s(dx+164,dy+146,dx+204,dy+170),radius=6*S,fill=(40,44,52))
# ideal-for strip
sy=372
d.rounded_rectangle(s(14,sy,886,sy+114),radius=16*S,fill=BLUE)
d.text(s(32,sy+10),"IDEAL FOR",font=F("ExtraBold",14),fill=LGREEN)
items=cfg["ideal_for"]; n=len(items); x0=36; span=530
for i,(ic,lab) in enumerate(items):
    cx=x0+i*(span/n)+ (span/n)/2-4
    circle_icon(cx,sy+52,20,ic,fg=BLUE,bg=WHITE,ring=WHITE)
    f=F("SemiBold",10.5)
    tw=d.textlength(lab,font=f)/S; d.text(s(cx-tw/2,sy+80),lab,font=f,fill=WHITE)
# contact block
cx0=600
d.line(s(cx0-12,sy+14,cx0-12,sy+100),fill=LBLUE,width=2*S)
for j,(ic,txt) in enumerate(cfg["contact"]):
    yy=sy+16+j*28
    d.ellipse(s(cx0,yy,cx0+22,yy+22),fill=WHITE)
    d.text(s(cx0+7,yy+3),ic,font=F("Bold",12),fill=BLUE)
    d.text(s(cx0+32,yy+2),txt,font=F("SemiBold",14),fill=WHITE)
img=img.resize((900,500),Image.LANCZOS)
img.save(out,quality=94)
