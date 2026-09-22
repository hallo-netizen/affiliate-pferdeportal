import json,sys
b=json.load(open(sys.argv[1])); c=json.load(open(sys.argv[2])); a=json.load(open(sys.argv[3]))
print("BASELINE",b)
print("CANDIDATE",c)
print("ADMIN",a)
assert b["direct_hashes"]==c["direct_hashes"],(b,c)
for k in ["desktop_hash","mobile_hash","astra_header_hash","astra_mobile_hash"]:
    assert b[k]==c[k],(k,b[k],c[k])
assert c["meta_hooks"] < b["meta_hooks"]*0.35,(b["meta_hooks"],c["meta_hooks"])
assert c["cache_hits"] >= 1520*8,c
assert a["cache_hits"]==0,a
assert a["meta_hooks"]>0,a
print("PASS DESIGN V2: identical direct/menu HTML hashes; request-wide core menu setup cache reduces metadata hooks >65%; admin remains uncached")
