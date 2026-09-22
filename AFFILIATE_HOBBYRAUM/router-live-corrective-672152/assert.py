import json,sys
p=json.load(open(sys.argv[1])); a=json.load(open(sys.argv[2]))
print("PUBLIC",p); print("ADMIN",a)
assert p["old_hash"]==p["new_hash"], p
assert p["new_rank"] < p["old_rank"], p
assert p["new_single"]==p["old_single"], p
assert p["new_total"] < p["old_total"], p
assert a["sanitize"] > 0 and a["reg"] >= 100 and a["terms"] >= 100, a
print("PASS 6.72.152: one-pass ranking reduces sanitizer work, single-field path never expands, frontend lookup caches work, admin uncached")
