#!/usr/bin/env python3
import argparse, hashlib, json, shutil, sys, tempfile, zipfile
from pathlib import Path
from PIL import Image

HERO=(600,320)
PREVIEW=(200,107)
MAP_REL='assets/hobby-depot-v150650/hub2-image-map.json'
WEBP_QUALITY=90
DHASH_SIZE=16
MIN_DHASH_DISTANCE=24

def sha256(path: Path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024), b''):
            h.update(chunk)
    return h.hexdigest()

def tree_hashes(root: Path):
    return {p.relative_to(root).as_posix():sha256(p) for p in sorted(root.rglob('*')) if p.is_file()}

def dhash(path: Path, size=DHASH_SIZE):
    with Image.open(path) as im:
        im=im.convert('L').resize((size+1,size),Image.Resampling.LANCZOS)
        px=list(im.getdata())
    v=0
    for y in range(size):
        row=px[y*(size+1):(y+1)*(size+1)]
        for x in range(size):
            v=(v<<1)|(1 if row[x]>row[x+1] else 0)
    return v

def hamming(a,b): return (a^b).bit_count()

def cover(im: Image.Image, target):
    tw,th=target; w,h=im.size
    if w<tw or h<th:
        raise ValueError(f'upscale forbidden: {w}x{h} < {tw}x{th}')
    tr=tw/th; sr=w/h
    if sr>tr:
        cw=round(h*tr); ch=h; l=(w-cw)//2; t=0
    else:
        cw=w; ch=round(w/tr); l=0; t=(h-ch)//2
    return im.crop((l,t,l+cw,t+ch)).resize(target,Image.Resampling.LANCZOS), [l,t,l+cw,t+ch]

def source_path(root: Path, slug: str):
    for ext in ('.png','.jpg','.jpeg','.webp'):
        p=root/f'{slug}-source{ext}'
        if p.exists(): return p
    return None

def fail(msg, report_path=None, report=None):
    if report is not None and report_path:
        report['pass']=False; report['fatal_error']=msg
        Path(report_path).parent.mkdir(parents=True,exist_ok=True)
        json.dump(report,open(report_path,'w',encoding='utf-8'),ensure_ascii=False,indent=2)
    print(json.dumps({'pass':False,'fatal_error':msg},ensure_ascii=False))
    return 2

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--base-zip',required=True)
    ap.add_argument('--manifest',required=True)
    ap.add_argument('--source-dir',required=True)
    ap.add_argument('--out-zip',required=True)
    ap.add_argument('--report',required=True)
    ap.add_argument('--test-mode',action='store_true')
    args=ap.parse_args()

    report={'base_zip':args.base_zip,'manifest':args.manifest,'source_dir':args.source_dir,'test_mode':args.test_mode,'categories':[]}
    try:
        m=json.load(open(args.manifest,'r',encoding='utf-8'))
        cats=m.get('categories',[])
        if len(cats)!=30:
            return fail(f'manifest must contain exactly 30 categories, got {len(cats)}',args.report,report)
        if not args.test_mode and m.get('release_allowed') is not True:
            return fail('release_allowed is not true',args.report,report)
        if not args.test_mode:
            not_ready=[x['category'] for x in cats if x.get('status')!='ready_source']
            if not_ready:
                return fail(f'{len(not_ready)} categories are not ready_source',args.report,report)

        srcroot=Path(args.source_dir)
        with tempfile.TemporaryDirectory() as td:
            td=Path(td); stage=td/'stage'; heroes=stage/'heroes'; previews=stage/'previews'
            heroes.mkdir(parents=True); previews.mkdir(parents=True)
            hero_sha={}; prev_sha={}; hero_dh={}; prev_dh={}

            for x in cats:
                cat=x['category']; slug=x['stage_slug']
                sp=source_path(srcroot,slug)
                if sp is None:
                    return fail(f'missing source for {cat}: {slug}-source.[png|jpg|jpeg|webp]',args.report,report)
                with Image.open(sp) as im0:
                    im=im0.convert('RGB')
                    hero,hbox=cover(im,HERO); prev,pbox=cover(im,PREVIEW)
                hp=heroes/f'{slug}.webp'; pp=previews/f'{slug}.webp'
                hero.save(hp,'WEBP',quality=WEBP_QUALITY,method=6)
                prev.save(pp,'WEBP',quality=WEBP_QUALITY,method=6)
                hero_sha[cat]=sha256(hp); prev_sha[cat]=sha256(pp)
                hero_dh[cat]=dhash(hp); prev_dh[cat]=dhash(pp)
                report['categories'].append({
                    'category':cat,'source':str(sp),'source_sha256':sha256(sp),
                    'hero_crop_box':hbox,'preview_crop_box':pbox,
                    'hero_sha256':hero_sha[cat],'preview_sha256':prev_sha[cat],
                    'hero_target':x['hero_target'],'preview_target':x['preview_target']
                })

            if len(set(hero_sha.values()))!=30 or len(set(prev_sha.values()))!=30:
                return fail('exact duplicate derived image detected',args.report,report)
            catsn=list(hero_dh)
            near=[]
            for i in range(30):
                for j in range(i+1,30):
                    a,b=catsn[i],catsn[j]
                    hd=hamming(hero_dh[a],hero_dh[b]); pd=hamming(prev_dh[a],prev_dh[b])
                    if hd<MIN_DHASH_DISTANCE or pd<MIN_DHASH_DISTANCE:
                        near.append({'a':a,'b':b,'hero_dhash':hd,'preview_dhash':pd})
            if near:
                report['near_duplicates']=near
                return fail(f'near duplicate gate failed for {len(near)} pairs',args.report,report)

            base=td/'base'
            with zipfile.ZipFile(args.base_zip,'r') as z: z.extractall(base)
            roots=[p for p in base.iterdir() if p.is_dir()]
            if len(roots)!=1: return fail(f'expected one plugin root, got {len(roots)}',args.report,report)
            root=roots[0]; work=td/'work'; shutil.copytree(root,work)
            before=tree_hashes(work)
            expected=set()
            for x in cats:
                slug=x['stage_slug']; hp=heroes/f'{slug}.webp'; pp=previews/f'{slug}.webp'
                ht=work/x['hero_target']; pt=work/x['preview_target']
                if not ht.exists(): return fail(f'hero target missing in base: {x["hero_target"]}',args.report,report)
                if not pt.exists(): return fail(f'preview target missing in base: {x["preview_target"]}',args.report,report)
                shutil.copy2(hp,ht); shutil.copy2(pp,pt)
                expected.update([x['hero_target'],x['preview_target']])
            after=tree_hashes(work)
            added=sorted(set(after)-set(before)); removed=sorted(set(before)-set(after))
            changed=sorted(k for k in before.keys()&after.keys() if before[k]!=after[k])
            unexpected=sorted(set(changed)-expected); missing_expected=sorted(expected-set(changed))
            map_identical=before.get(MAP_REL)==after.get(MAP_REL)
            report['tree']={'before_files':len(before),'after_files':len(after),'changed_count':len(changed),'added':added,'removed':removed,'unexpected_changes':unexpected,'expected_not_changed':missing_expected,'mapping_identical':map_identical}
            if added or removed or unexpected or missing_expected or len(changed)!=60 or not map_identical:
                return fail('60-file image-only tree gate failed',args.report,report)

            out=Path(args.out_zip); out.parent.mkdir(parents=True,exist_ok=True)
            with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
                for p in sorted(work.rglob('*')):
                    if p.is_file(): z.write(p,(Path(root.name)/p.relative_to(work)).as_posix())
            rt=td/'roundtrip'
            with zipfile.ZipFile(out,'r') as z: z.extractall(rt)
            rt_identical=tree_hashes(rt/root.name)==after
            if not rt_identical: return fail('zip roundtrip mismatch',args.report,report)
            report['out_zip']=str(out); report['out_zip_sha256']=sha256(out); report['roundtrip_identical']=True; report['pass']=True
            Path(args.report).parent.mkdir(parents=True,exist_ok=True)
            json.dump(report,open(args.report,'w',encoding='utf-8'),ensure_ascii=False,indent=2)
            print(json.dumps({'pass':True,'categories':30,'changed_files':60,'mapping_identical':True,'roundtrip_identical':True,'out_zip_sha256':report['out_zip_sha256']},ensure_ascii=False))
            return 0
    except Exception as e:
        return fail(str(e),args.report,report)

if __name__=='__main__': sys.exit(main())
