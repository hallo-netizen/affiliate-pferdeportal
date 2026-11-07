#!/usr/bin/env python3
import urllib.request, zipfile, io, hashlib
urls=[
"https://m.media-amazon.com/images/G/01/AdProductsWebsite/images/ad-specs/available_at_amazon___de_3f5c5e60.zip",
"https://m.media-amazon.com/images/G/01/AdProductsWebsite/images/AUX/brand-usage/Available_at_Amazon_DE_Ex.zip",
]
for url in urls:
    print("URL",url)
    try:
        req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0"})
        with urllib.request.urlopen(req,timeout=25) as r:data=r.read()
        print("HTTP OK ZIP",len(data),hashlib.sha256(data).hexdigest())
        with zipfile.ZipFile(io.BytesIO(data)) as z:
            for info in z.infolist():
                if not info.is_dir():
                    print("FILE",info.filename,"size",info.file_size,"sha",hashlib.sha256(z.read(info.filename)).hexdigest())
    except Exception as e: print("ERROR",type(e).__name__,str(e))
