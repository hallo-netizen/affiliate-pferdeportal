#!/usr/bin/env python3
import argparse, hashlib, json, sys
from pathlib import Path
from PIL import Image

HERO_SIZE=(600,320)
PREVIEW_SIZE=(200,107)
WEBP_QUALITY=90

def sha256_file(path: Path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024), b''):
            h.update(chunk)
    return h.hexdigest()

def dhash(path: Path, hash_size=16):
    with Image.open(path) as im:
        im=im.convert('L').resize((hash_size+1,hash_size), Image.Resampling.LANCZOS)
        px=list(im.getdata())
    bits=[]
    for y in range(hash_size):
        row=px[y*(hash_size+1):(y+1)*(hash_size+1)]
        bits.extend(1 if row[x]>row[x+1] else 0 for x in range(hash_size))
    v=0
    for b in bits:
        v=(v<<1)|b
    return v

def ham(a,b):
    return (a^b).bit_count()

def cover_crop(im: Image.Image, target):
    tw,th=target
    w,h=im.size
    if w<tw or h<th:
        raise ValueError(f'upscale forbidden: source {w}x{h} smaller than {tw}x{th}')
    target_ratio=tw/th
    src_ratio=w/h
    if src_ratio>target_ratio:
        cw=round(h*target_ratio)
        ch=h
        left=(w-cw)//2
        top=0
    else:
        cw=w
        ch=round(w/target_ratio)
        left=0
        top=(h-ch)//2
    box=(left,top,left+cw,top+ch)
    out=im.crop(box).resize(target, Image.Resampling.LANCZOS)
    return out,box

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--queue',required=True)
    ap.add_argument('--source-dir',required=True)
    ap.add_argument('--out-dir',required=True)
    ap.add_argument('--report',required=True)
    args=ap.parse_args()

    q=json.load(open(args.queue,'r',encoding='utf-8'))
    items=q.get('items',[])
    srcdir=Path(args.source_dir)
    outdir=Path(args.out_dir)
    hero_dir=outdir/'heroes'
    preview_dir=outdir/'previews'
    hero_dir.mkdir(parents=True,exist_ok=True)
    preview_dir.mkdir(parents=True,exist_ok=True)

    report={
        'queue':Path(args.queue).name,
        'count':len(items),
        'hero_size':HERO_SIZE,
        'preview_size':PREVIEW_SIZE,
        'items':[],
        'errors':[],
        'duplicate_checks':{}
    }
    hero_hashes={}
    preview_hashes={}
    hero_dh={}
    preview_dh={}

    for item in items:
        cat=item['category']
        fname=item['expected_source_filename']
        src=srcdir/fname
        rec={'category':cat,'source':str(src),'expected_source_filename':fname}
        try:
            if not src.exists():
                raise FileNotFoundError(str(src))
            rec['source_sha256']=sha256_file(src)
            with Image.open(src) as im0:
                im=im0.convert('RGB')
                rec['source_size']=list(im.size)
                hero,hero_box=cover_crop(im,HERO_SIZE)
                prev,prev_box=cover_crop(im,PREVIEW_SIZE)
            slug=Path(fname).stem.replace('-source','')
            hp=hero_dir/f'{slug}.webp'
            pp=preview_dir/f'{slug}.webp'
            hero.save(hp,'WEBP',quality=WEBP_QUALITY,method=6)
            prev.save(pp,'WEBP',quality=WEBP_QUALITY,method=6)
            rec.update({
                'hero_file':str(hp),
                'preview_file':str(pp),
                'hero_crop_box':list(hero_box),
                'preview_crop_box':list(prev_box),
                'hero_sha256':sha256_file(hp),
                'preview_sha256':sha256_file(pp),
                'hero_size':list(Image.open(hp).size),
                'preview_size':list(Image.open(pp).size),
                'no_upscale':True,
                'status':'PASS_TECHNICAL_PENDING_VISUAL'
            })
            hero_hashes[cat]=rec['hero_sha256']
            preview_hashes[cat]=rec['preview_sha256']
            hero_dh[cat]=dhash(hp)
            preview_dh[cat]=dhash(pp)
        except Exception as e:
            rec['status']='FAIL'
            rec['error']=str(e)
            report['errors'].append({'category':cat,'error':str(e)})
        report['items'].append(rec)

    cats=list(hero_dh)
    exact_hero=len(hero_hashes)!=len(set(hero_hashes.values()))
    exact_prev=len(preview_hashes)!=len(set(preview_hashes.values()))
    hd=[]
    pd=[]
    for i in range(len(cats)):
        for j in range(i+1,len(cats)):
            a,b=cats[i],cats[j]
            hd.append((ham(hero_dh[a],hero_dh[b]),a,b))
            pd.append((ham(preview_dh[a],preview_dh[b]),a,b))

    report['duplicate_checks']={
        'hero_exact_duplicate':exact_hero,
        'preview_exact_duplicate':exact_prev,
        'hero_min_dhash':min(hd)[0] if hd else None,
        'hero_min_pair':list(min(hd)[1:]) if hd else None,
        'preview_min_dhash':min(pd)[0] if pd else None,
        'preview_min_pair':list(min(pd)[1:]) if pd else None
    }
    report['pass_technical']=(
        not report['errors']
        and not exact_hero
        and not exact_prev
        and all(
            x.get('hero_size')==list(HERO_SIZE)
            and x.get('preview_size')==list(PREVIEW_SIZE)
            for x in report['items']
        )
    )

    Path(args.report).parent.mkdir(parents=True,exist_ok=True)
    json.dump(report,open(args.report,'w',encoding='utf-8'),ensure_ascii=False,indent=2)
    print(json.dumps({
        'pass_technical':report['pass_technical'],
        'count':len(items),
        'errors':len(report['errors']),
        'duplicate_checks':report['duplicate_checks']
    },ensure_ascii=False))
    return 0 if report['pass_technical'] else 2

if __name__=='__main__':
    sys.exit(main())
