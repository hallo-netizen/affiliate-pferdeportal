#!/usr/bin/env python3
import argparse, hashlib, json, shutil, tempfile, zipfile, sys
from pathlib import Path
from PIL import Image

HERO_SIZE=(600,320)
PREVIEW_SIZE=(200,107)
MAP_REL='assets/hobby-depot-v150650/hub2-image-map.json'

def sha256(path: Path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''):
            h.update(chunk)
    return h.hexdigest()

def file_hashes(root: Path):
    out={}
    for p in sorted(root.rglob('*')):
        if p.is_file():
            out[p.relative_to(root).as_posix()]=sha256(p)
    return out

def slugify(s):
    import unicodedata,re
    s=unicodedata.normalize('NFD',s.lower())
    s=''.join(ch for ch in s if unicodedata.category(ch)!='Mn')
    s=s.replace('&','und')
    s=re.sub(r'[^a-z0-9]+','-',s).strip('-')
    return s

def check_image(path,size):
    with Image.open(path) as im:
        actual=im.size
    if actual!=size:
        raise ValueError(f'{path}: expected {size[0]}x{size[1]}, got {actual[0]}x{actual[1]}')

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--base-zip',required=True)
    ap.add_argument('--manifest',required=True)
    ap.add_argument('--stage-dir',required=True)
    ap.add_argument('--out-zip',required=True)
    ap.add_argument('--report',required=True)
    ap.add_argument('--allow-partial',action='store_true')
    args=ap.parse_args()

    manifest=json.load(open(args.manifest,'r',encoding='utf-8'))
    cats=manifest['categories']
    stage=Path(args.stage_dir)
    report={'base_zip':args.base_zip,'manifest':args.manifest,'allow_partial':args.allow_partial,'replaced':[],'missing':[],'errors':[]}

    with tempfile.TemporaryDirectory() as td:
        td=Path(td)
        base=td/'base'
        work=td/'work'
        with zipfile.ZipFile(args.base_zip,'r') as z:
            z.extractall(base)
        roots=[p for p in base.iterdir() if p.is_dir()]
        if len(roots)!=1:
            raise RuntimeError(f'expected one plugin root, got {len(roots)}')
        root=roots[0]
        shutil.copytree(root,work)
        before=file_hashes(work)
        root_name=root.name

        for x in cats:
            slug=x.get('stage_slug') or slugify(x['category'])
            hp=stage/'heroes'/f'{slug}.webp'
            pp=stage/'previews'/f'{slug}.webp'
            if not hp.exists() or not pp.exists():
                report['missing'].append(x['category'])
                continue
            check_image(hp,HERO_SIZE)
            check_image(pp,PREVIEW_SIZE)
            ht=work/x['hero_target']
            pt=work/x['preview_target']
            if not ht.exists() or not pt.exists():
                raise FileNotFoundError(f'target missing for {x["category"]}: {ht} / {pt}')
            shutil.copy2(hp,ht)
            shutil.copy2(pp,pt)
            report['replaced'].append({
                'category':x['category'],
                'hero_target':x['hero_target'],
                'preview_target':x['preview_target'],
                'hero_sha256':sha256(ht),
                'preview_sha256':sha256(pt)
            })

        if report['missing'] and not args.allow_partial:
            raise RuntimeError(f'incomplete stage: missing {len(report["missing"])} categories')

        after=file_hashes(work)
        added=sorted(set(after)-set(before))
        removed=sorted(set(before)-set(after))
        changed=sorted(k for k in before.keys()&after.keys() if before[k]!=after[k])
        expected=set()
        for r in report['replaced']:
            expected.update({r['hero_target'],r['preview_target']})
        unexpected=sorted(set(changed)-expected)
        missing_expected=sorted(expected-set(changed))
        map_before=before.get(MAP_REL)
        map_after=after.get(MAP_REL)
        report['tree_check']={
            'before_files':len(before),
            'after_files':len(after),
            'added':added,
            'removed':removed,
            'changed_count':len(changed),
            'changed':changed,
            'unexpected_changes':unexpected,
            'expected_not_changed':missing_expected,
            'mapping_sha256_before':map_before,
            'mapping_sha256_after':map_after,
            'mapping_identical':map_before==map_after
        }
        report['pass_technical']=(
            not added
            and not removed
            and not unexpected
            and not missing_expected
            and map_before==map_after
            and len(changed)==2*len(report['replaced'])
        )
        if not report['pass_technical']:
            raise RuntimeError('overlay tree validation failed')

        out=Path(args.out_zip)
        out.parent.mkdir(parents=True,exist_ok=True)
        with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
            for p in sorted(work.rglob('*')):
                arc=Path(root_name)/p.relative_to(work)
                if p.is_dir():
                    z.writestr(arc.as_posix().rstrip('/')+'/',b'')
                else:
                    z.write(p,arc.as_posix())
        report['out_zip_sha256']=sha256(out)
        report['out_zip_size']=out.stat().st_size

        rt=td/'roundtrip'
        with zipfile.ZipFile(out,'r') as z:
            z.extractall(rt)
        rtroot=rt/root_name
        roundtrip=file_hashes(rtroot)
        report['roundtrip_identical']=(roundtrip==after)
        report['pass_technical']=report['pass_technical'] and report['roundtrip_identical']

    Path(args.report).parent.mkdir(parents=True,exist_ok=True)
    json.dump(report,open(args.report,'w',encoding='utf-8'),ensure_ascii=False,indent=2)
    print(json.dumps({
        'pass_technical':report['pass_technical'],
        'replaced_categories':len(report['replaced']),
        'missing_categories':len(report['missing']),
        'changed_files':report['tree_check']['changed_count'],
        'roundtrip_identical':report['roundtrip_identical']
    },ensure_ascii=False))
    return 0 if report['pass_technical'] else 2

if __name__=='__main__':
    sys.exit(main())
