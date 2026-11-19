#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont
import os

W=H=1024
BG="#f4efe3"; INK="#17202a"; RED="#d64032"; BLUE="#176b87"; GOLD="#e3aa35"; GREEN="#43836c"; PALE="#ded6c5"
img=Image.new("RGB",(W,H),BG); d=ImageDraw.Draw(img)
FP="/usr/share/fonts/truetype/dejavu/"
def font(n,b=False): return ImageFont.truetype(FP+("DejaVuSans-Bold.ttf" if b else "DejaVuSans.ttf"),n)
def text(x,y,s,f,fill=INK,anchor=None): d.text((x,y),s,font=f,fill=fill,anchor=anchor)
def fit(s,box,start,b=True,minsize=6,spacing=1,fill=INK):
    x,y,w,h=box
    for n in range(start,minsize-1,-1):
        f=font(n,b); words=s.split(); lines=[]; line=""
        for q in words:
            z=(line+" "+q).strip()
            if d.textbbox((0,0),z,font=f)[2]<=w: line=z
            else:
                if line: lines.append(line)
                line=q
        if line: lines.append(line)
        lh=n+spacing
        if len(lines)*lh<=h and all(d.textbbox((0,0),q,font=f)[2]<=w for q in lines):
            assert len(lines)*lh<=h
            for i,q in enumerate(lines): text(x,y+i*lh,q,f,fill)
            return
    raise AssertionError("text overflow: "+s)
def rect(box,fill,outline=None,width=1): d.rectangle(box,fill=fill,outline=outline,width=width)
def vignette(x,y,w,h,k):
    colors=[RED,BLUE,GOLD,GREEN]; c=colors[k%4]
    rect((x,y,x+w,y+h),"#ebe4d5")
    # deterministic flat miniatures: horizon, sun, subject glyph
    d.ellipse((x+w-20,y+5,x+w-7,y+18),fill=GOLD)
    d.line((x,y+h-9,x+w,y+h-9),fill=INK,width=2)
    t=k%7
    if t==0: # city / alert
        for i,hh in enumerate((17,27,21)): rect((x+6+i*13,y+h-9-hh,x+16+i*13,y+h-9),c)
        d.polygon([(x+51,y+8),(x+60,y+26),(x+42,y+26)],fill=RED)
    elif t==1: # ballot
        rect((x+13,y+18,x+45,y+h-10),c); d.polygon([(x+20,y+6),(x+48,y+13),(x+43,y+22),(x+17,y+15)],fill="#fff")
    elif t==2: # ship
        d.polygon([(x+7,y+29),(x+52,y+29),(x+44,y+40),(x+15,y+40)],fill=c); rect((x+24,y+15,x+39,y+29),INK)
    elif t==3: # factory
        rect((x+7,y+24,x+50,y+h-9),c); d.polygon([(x+7,y+24),(x+20,y+14),(x+20,y+24),(x+34,y+14),(x+34,y+24)],fill=c); rect((x+45,y+7,x+51,y+25),INK)
    elif t==4: # people
        for i in range(3):
            d.ellipse((x+8+i*17,y+10,x+18+i*17,y+20),fill=c); rect((x+9+i*17,y+21,x+17+i*17,y+38),c)
    elif t==5: # globe
        d.ellipse((x+10,y+5,x+49,y+44),fill=c,outline=INK,width=2); d.arc((x+21,y+5,x+38,y+44),90,270,fill=BG,width=2); d.line((x+11,y+24,x+48,y+24),fill=BG,width=2)
    else: # satellite
        d.polygon([(x+25,y+12),(x+42,y+22),(x+32,y+36),(x+16,y+25)],fill=c); rect((x+4,y+17,x+18,y+26),BLUE); rect((x+40,y+27,x+55,y+36),BLUE)

# masthead
rect((0,0,1024,8),RED); text(24,20,"THE DAY IN WORLD NEWS",font(47,True),INK)
text(25,76,"WEDNESDAY 18 NOVEMBER 2026",font(31,True),RED)
text(998,31,"GLOBAL EDITION  •  1024",font(10,True),INK,"ra")
d.line((24,116,1000,116),fill=INK,width=3)

stats=[("141","DRONES FIRED AT UKRAINE"),("126","DOWNED"),("25.9bn km","VOYAGER 1 DISTANCE"),("55","FACTORIES SHUT"),("251–11","JEFFRIES VOTE"),("11,300+","EBOLA CASES")]
sw=976//6
for i,(a,b) in enumerate(stats):
    x=24+i*sw; text(x,125,a,font(22,True),[RED,BLUE][i%2]); fit(b,(x,151,sw-8,18),8,True)
d.line((24,174,1000,174),fill=INK,width=2)

stories=[
("EUROPE","NIGHT SKY FILLS WITH DRONES","Ukraine says 126 of 141 were downed as cities sheltered."),
("AMERICAS","JEFFRIES WINS HOUSE TEST","Democrats back their leader 251–11 in a unity vote."),
("ASIA","FIFTY-FIVE FACTORIES PAUSE","Power curbs shut 55 plants as officials ration supply."),
("AFRICA","EBOLA RESPONSE WIDENS","Regional tally passes 11,300 as mobile clinics deploy."),
("MIDEAST","GAZA TRUCE TALKS REOPEN","Mediators return with a phased aid-and-hostage plan."),
("PACIFIC","ISLANDS PRESS CLIMATE CASE","Leaders seek binding protection for displaced citizens."),
("SPACE","VOYAGER 1 CALLS HOME","The probe reports clean data from 25.9bn km away."),
("EUROPE","DANUBE FLOOD WALLS RISE","Crews reinforce levees after three days of hard rain."),
("AMERICAS","AMAZON PACT GAINS GROUND","Seven states agree a shared forest-fire command."),
("ASIA","RAIL LINK CROSSES NEW PASS","A high-altitude freight route begins trial operations."),
("AFRICA","SOLAR MICROGRIDS SWITCH ON","Rural clinics gain round-the-clock vaccine cooling."),
("MIDEAST","RED SEA PORT CLEARS QUEUE","Inspections speed up and grain vessels begin docking."),
("PACIFIC","CORAL NURSERIES SHOW GAINS","Heat-tolerant fragments survive a second warm season.")]

# lead grid: 4,4,5 cards
top=183; cardh=102
for row,count in enumerate((4,4,5)):
    gap=8; cw=(976-gap*(count-1))//count
    for col in range(count):
        k=sum((4,4,5)[:row])+col; x=24+col*(cw+gap); y=top+row*(cardh+7)
        rect((x,y,x+cw,y+cardh),"#faf7ef",PALE)
        vignette(x+6,y+6,60,45,k)
        text(x+73,y+6,stories[k][0],font(7,True),RED)
        fit(stories[k][1],(x+73,y+17,cw-79,35),11,True,7)
        fit(stories[k][2],(x+6,y+57,cw-12,38),9,False,7)

# lower field
ly=516; text(24,ly,"THE WORLD, MAPPED",font(15,True),INK); text(405,ly,"31 MORE HEADLINES",font(15,True),INK)
mapbox=(24,541,384,950); rect(mapbox,"#dce8df",INK)
# abstract world map silhouettes
d.polygon([(48,603),(83,573),(139,582),(157,611),(126,637),(107,690),(77,671)],fill=GREEN)
d.polygon([(135,700),(166,718),(158,785),(136,844),(119,791)],fill=GREEN)
d.polygon([(200,580),(240,565),(280,584),(331,579),(365,608),(337,632),(294,625),(270,661),(230,646),(206,615)],fill=GREEN)
d.polygon([(266,668),(310,674),(333,717),(306,793),(270,749)],fill=GREEN)
d.polygon([(332,769),(367,779),(378,807),(349,820),(322,801)],fill=GREEN)
markers=[(117,615,"AMERICAS"),(232,595,"EUROPE"),(285,695,"AFRICA"),(309,616,"ASIA"),(345,787,"PACIFIC"),(264,643,"MIDEAST"),(196,875,"SPACE  •  VOYAGER")]
for x,y,s in markers:
    d.ellipse((x-4,y-4,x+4,y+4),fill=RED); text(x+7,y-5,s,font(7,True),INK)
fit("SEVEN REGIONS  •  13 LEAD REPORTS  •  ONE PLANET",(39,913,330,20),9,True)

briefs=[
"Poland opens an eastern civil-defence hub","Canada tables an Arctic shipping code","Mexico launches drought insurance for farms","Brazil court protects a river reserve","Chile expands quake-sensor coverage","Caribbean states pool hurricane aircraft","France caps winter rail fares","Germany trims industrial grid fees","Spain restores wetlands after wildfire","Italy opens a migrant processing review","Nordic ministers align cyber rules","Balkans sign a cross-border power pact","India adds night trains for festival crowds","China reports a softer property decline","Japan tests autonomous harbour tugs","Korea unveils a battery recycling standard","Thailand raises coastal flood barriers","Indonesia maps peat-fire risk daily","Pakistan vaccinates in remote districts","Bangladesh upgrades cyclone shelters","Kenya launches an electric bus corridor","Nigeria targets methane leaks at wells","Congo river ferry rules are tightened","Sahel schools trial radio classrooms","South Africa posts a cooler inflation print","Egypt restores a historic Alexandria quay","Jordan expands desalination tenders","Lebanon schools reopen on staggered hours","Australia funds Indigenous ranger teams","New Zealand widens marine protection","UN members seek a plastics treaty compromise"]
assert len(briefs)==31
cols=2; bx=405; bw=290; bh=25
for i,s in enumerate(briefs):
    col=i//16; row=i%16; x=bx+col*(bw+8); y=541+row*bh
    text(x,y+1,f"{i+1:02d}",font(8,True),RED)
    fit(s,(x+20,y,bw-22,22),9,True,7)
    d.line((x,y+23,x+bw-4,y+23),fill=PALE,width=1)

rect((0,964,1024,1024),INK)
text(24,976,"DATE CHECK",font(9,True),GOLD)
fit("All items are written for the Wednesday 18 November 2026 edition; figures in the numbers band match the lead reports above.",(100,974,720,34),9,False,7,1,BG)
text(998,983,"THE DAY / WORLD DESK",font(9,True),BG,"ra")

img.save("entry.png",optimize=True)
assert img.size==(1024,1024)
assert os.path.getsize("entry.png")<1048576
print(f"entry.png: {os.path.getsize('entry.png')} bytes; 44 stories; 13 illustrations")
