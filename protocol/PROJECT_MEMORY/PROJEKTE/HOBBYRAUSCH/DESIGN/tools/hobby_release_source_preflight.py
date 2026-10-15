#!/usr/bin/env python3
import argparse, json, sys
from pathlib import Path
from PIL import Image

MIN_HERO=(600,320)
MIN_PREVIEW=(200,107)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--manifest',required=True)
    ap.add_argument('--source-dir',required=True)
    ap.add_argument('--report',required=True)
    args=ap.parse_args()

    m=json.load(open(args.manifest,'r',encoding='utf-8'))
    root=Path(args.source_dir)
    items=[]
    missing=[]
    invalid_status=[]
    too_small=[]

    for x in m['categories']:
        slug=x['stage_slug']
        src=root/f'{slug}-source.png'
        rec={'category':x['category'],'status':x['status'],'source':str(src)}
        if x['status']!='ready_source':
            invalid_status.append(x['category'])
            rec['gate']='BLOCKED_STATUS'
        elif not src.exists():
            missing.append(x['category'])
            rec['gate']='MISSING_SOURCE'
        else:
            with Image.open(src) as im:
                rec['size']=list(im.size)
                if im.width<MIN_HERO[0] or im.height<MIN_HERO[1]:
                    too_small.append(x['category'])
                    rec['gate']='SOURCE_TOO_SMALL'
                else:
                    rec['gate']='PASS'
        items.append(rec)

    report={
        'total':len(items),
        'ready_status':sum(1 for x in m['categories'] if x['status']=='ready_source'),
        'blocked_status_count':len(invalid_status),
        'missing_ready_sources':missing,
        'too_small_ready_sources':too_small,
        'items':items
    }
    report['release_source_gate_pass']=(
        len(items)==30
        and not invalid_status
        and not missing
        and not too_small
    )

    Path(args.report).parent.mkdir(parents=True,exist_ok=True)
    json.dump(report,open(args.report,'w',encoding='utf-8'),ensure_ascii=False,indent=2)
    print(json.dumps({
        'release_source_gate_pass':report['release_source_gate_pass'],
        'total':report['total'],
        'ready_status':report['ready_status'],
        'blocked_status_count':report['blocked_status_count'],
        'missing_ready_sources':len(missing),
        'too_small_ready_sources':len(too_small)
    },ensure_ascii=False))
    return 0 if report['release_source_gate_pass'] else 2

if __name__=='__main__':
    sys.exit(main())
