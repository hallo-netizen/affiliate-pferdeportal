#!/usr/bin/env python3
from pathlib import Path
import struct, sys, zlib

if len(sys.argv) != 2:
    raise SystemExit('usage: verify_visual_png.py <screenshot.png>')
raw = Path(sys.argv[1]).read_bytes()
if raw[:8] != b'\x89PNG\r\n\x1a\n':
    raise SystemExit('not png')
pos=8; width=height=ctype=bit=None; idat=b''
while pos < len(raw):
    n=struct.unpack('>I',raw[pos:pos+4])[0]; typ=raw[pos+4:pos+8]; data=raw[pos+8:pos+8+n]; pos += 12+n
    if typ==b'IHDR':
        width,height,bit,ctype,comp,flt,interlace=struct.unpack('>IIBBBBB',data)
        if bit!=8 or interlace!=0 or ctype not in (2,6):
            raise SystemExit(f'unsupported png bit={bit} ctype={ctype} interlace={interlace}')
    elif typ==b'IDAT': idat += data
    elif typ==b'IEND': break
bpp = 3 if ctype==2 else 4
scan=zlib.decompress(idat); stride=width*bpp
rows=[]; prev=bytearray(stride); off=0
def paeth(a,b,c):
    p=a+b-c; pa=abs(p-a); pb=abs(p-b); pc=abs(p-c)
    return a if pa<=pb and pa<=pc else (b if pb<=pc else c)
for y in range(height):
    ft=scan[off]; off+=1; src=bytearray(scan[off:off+stride]); off+=stride
    dst=bytearray(stride)
    for i,x in enumerate(src):
        a=dst[i-bpp] if i>=bpp else 0
        b=prev[i]
        c=prev[i-bpp] if i>=bpp else 0
        if ft==0: v=x
        elif ft==1: v=(x+a)&255
        elif ft==2: v=(x+b)&255
        elif ft==3: v=(x+((a+b)//2))&255
        elif ft==4: v=(x+paeth(a,b,c))&255
        else: raise SystemExit('unsupported filter '+str(ft))
        dst[i]=v
    rows.append(dst); prev=dst

def px(x,y):
    if not (0<=x<width and 0<=y<height): raise AssertionError((x,y,width,height))
    row=rows[y]; i=x*bpp; return tuple(row[i:i+3])
def near(p,q,t=70): return all(abs(a-b)<=t for a,b in zip(p,q))
def must(xy,color,name):
    p=px(*xy)
    if not near(p,color): raise AssertionError(f'{name} at {xy}: got {p}, expected near {color}')
    print('PASS',name,xy,p)

WHITE=(255,255,255); RED=(255,0,0); GREEN=(0,170,0); MAG=(255,0,255)
# Landscape source is 3:2. contain => full 150x100 image centered vertically with white letterbox.
must((75,10),WHITE,'landscape_top_letterbox')
for xy,n in [((3,75),'landscape_left_border'),((146,75),'landscape_right_border'),((75,28),'landscape_top_border'),((75,121),'landscape_bottom_border')]: must(xy,RED,n)
# Portrait source is 2:3. contain => full 100x150 image centered horizontally with white letterbox.
must((180,75),WHITE,'portrait_left_letterbox')
for xy,n in [((198,75),'portrait_left_border'),((291,75),'portrait_right_border'),((245,3),'portrait_top_border'),((245,146),'portrait_bottom_border')]: must(xy,GREEN,n)
# Square source fills the full third 150x150 frame without crop.
for xy,n in [((343,75),'square_left_border'),((486,75),'square_right_border'),((415,3),'square_top_border'),((415,146),'square_bottom_border')]: must(xy,MAG,n)
print(f'PNG_SIZE={width}x{height}')
print('VISIBLE_SOURCE_EDGES_ALL_PRESENT=PASS')
print('NO_CROP_VISUAL_COUNTERPROOF=PASS')
