"""Branded 1200x900 GBP post image. Usage: make_branded_post.py config.json out.jpg"""
import sys, json
from PIL import Image, ImageDraw, ImageFont
cfg=json.load(open(sys.argv[1])); out=sys.argv[2]
W,H=1200,900
BLUE=(47,85,151); LBLUE=(68,114,196); GREEN=(84,160,52); LGREEN=(169,209,142); NAVY=(16,37,66); GREY=(90,100,115)
B="/usr/share/fonts/opentype/inter/Inter-Bold.otf"; R="/usr/share/fonts/opentype/inter/Inter-Regular.otf"; M="/usr/share/fonts/opentype/inter/Inter-Medium.otf"
def F(p,s):
    for f in (p,"/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"):
        try: return ImageFont.truetype(f,s)
        except Exception: pass
img=Image.new("RGB",(W,H),(255,255,255)); d=ImageDraw.Draw(img)
# soft background band
d.rectangle((0,0,W,H),fill=(246,249,253))
d.rectangle((0,0,W,12),fill=LBLUE); d.rectangle((0,12,W,18),fill=LGREEN)
# logo
logo=Image.open(cfg.get("logo",__import__("os").path.join(__import__("os").path.dirname(__import__("os").path.abspath(__file__)),"..","assets","logo.png"))).convert("RGBA")
lh=104; lw=int(logo.width*lh/logo.height); logo=logo.resize((lw,lh),Image.LANCZOS)
img.paste(logo,(56,36),logo)
# tagline top-right
t=cfg.get("tagline","Monitor Today for a Safer Tomorrow"); f=F(M,24)
d.text((W-56-d.textlength(t,font=f),84),t,font=f,fill=GREY)
# headline (two tone)
y=160
for i,line in enumerate(cfg["headline"]):
    d.text((56,y),line,font=F(B,66),fill=BLUE if i==0 else GREEN); y+=74
# product pill
pt=cfg["product"]; pf=F(B,30); pw=int(d.textlength(pt,font=pf))+56
d.rounded_rectangle((56,y+8,56+pw,y+66),radius=29,fill=NAVY); d.text((84,y+19),pt,font=pf,fill=(255,255,255))
# dashboard card (left)
cx0,cy0,cx1,cy1=56,y+88,560,y+88+292
d.rounded_rectangle((cx0,cy0,cx1,cy1),radius=22,fill=(255,255,255),outline=(205,215,232),width=3)
d.text((cx0+26,cy0+20),cfg.get("card_title","IoT Dashboard"),font=F(B,26),fill=NAVY)
d.rounded_rectangle((cx1-130,cy0+18,cx1-26,cy0+54),radius=18,fill=(222,242,214)); d.text((cx1-112,cy0+23),"Online",font=F(B,22),fill=GREEN)
for k,(lab,val) in enumerate(cfg.get("readings",[("Temperature","37.0 °C"),("Humidity","45 %RH")])):
    bx=cx0+26+k*232
    d.rounded_rectangle((bx,cy0+74,bx+216,cy0+160),radius=14,fill=(238,243,251))
    d.text((bx+16,cy0+82),lab,font=F(R,20),fill=GREY); d.text((bx+16,cy0+110),val,font=F(B,34),fill=BLUE)
# mini chart with alert
gx0,gy0,gx1,gy1=cx0+26,cy0+172,cx1-26,cy1-18
d.rounded_rectangle((gx0,gy0,gx1,gy1),radius=12,fill=(238,243,251))
import math
pts=[]
for i in range(60):
    x=gx0+14+(gx1-gx0-28)*i/59; yy=gy0+(gy1-gy0)*0.38+math.sin(i/3.2)*5
    if i>38: yy+=(i-38)**1.1*2.3
    pts.append((x,min(yy,gy1-12)))
d.line(pts,fill=LBLUE,width=5,joint="curve")
ax,ay=pts[44]; d.ellipse((ax-10,ay-10,ax+10,ay+10),fill=(235,87,87))
d.text((ax-150,gy0+8),"Alert sent",font=F(B,20),fill=(200,60,60))
# bullets (right)
bx=610; by=cy0+6
d.text((bx,by),"KEY FEATURES",font=F(B,26),fill=GREEN); by+=46
for b in cfg["bullets"]:
    d.ellipse((bx,by+4,bx+34,by+38),fill=LGREEN)
    d.line([(bx+9,by+21),(bx+15,by+28),(bx+26,by+13)],fill=(255,255,255),width=5)
    d.text((bx+50,by),b,font=F(M,28),fill=NAVY); by+=56
# ideal for strip
sy=H-170
d.rounded_rectangle((56,sy,W-56,sy+86),radius=20,fill=BLUE)
d.text((84,sy+14),"IDEAL FOR",font=F(B,22),fill=LGREEN)
d.text((84,sy+42),cfg["ideal_for"],font=F(B,30),fill=(255,255,255))
d.text((56,H-60),cfg.get("cta","Call now to enquire or request a demo"),font=F(B,28),fill=NAVY)
site="techmedsmartsense.com"; sf=F(M,26); d.text((W-56-d.textlength(site,font=sf),H-58),site,font=sf,fill=GREY)
img.save(out,quality=93)
