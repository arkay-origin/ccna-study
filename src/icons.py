from PIL import Image, ImageDraw, ImageFont
F='/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf'
BG=(12,11,16);TAN=(217,215,176);RED=(217,86,31);GOLD=(191,161,82)
def icon(size,scale,name):
    S=512;im=Image.new('RGB',(S,S),BG);d=ImageDraw.Draw(im);f=ImageFont.truetype(F,int(180*scale))
    w=lambda t:(lambda b:b[2]-b[0])(d.textbbox((0,0),t,font=f))
    gap=int(120*scale);x=(S-(w('C')+gap+w('N')))/2;y=S/2-int(20*scale)
    b=d.textbbox((0,0),'C',font=f);h=b[3]-b[1]
    d.text((x,y-h/2-b[1]),'C',font=f,fill=TAN);d.text((x+w('C')+gap,y-h/2-b[1]),'N',font=f,fill=TAN)
    cx=x+w('C')+gap/2;sh=int(105*scale);th=int(15*scale);k=0.3
    d.polygon([(cx+sh*k-th,y-sh),(cx+sh*k+th,y-sh),(cx-sh*k+th,y+sh),(cx-sh*k-th,y+sh)],fill=RED)
    lw=int(300*scale);d.rectangle([(S-lw)/2,y+sh+int(18*scale),(S+lw)/2,y+sh+int(30*scale)],fill=GOLD)
    im.resize((size,size),Image.LANCZOS).save('out/'+name)
icon(512,1,'icon-512.png');icon(192,1,'icon-192.png');icon(180,1,'apple-touch-icon.png');icon(512,0.72,'icon-maskable-512.png')
