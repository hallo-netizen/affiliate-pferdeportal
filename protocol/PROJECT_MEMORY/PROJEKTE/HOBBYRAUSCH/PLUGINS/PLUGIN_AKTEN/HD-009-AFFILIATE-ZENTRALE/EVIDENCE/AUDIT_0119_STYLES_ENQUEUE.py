from pathlib import Path
import zipfile,re
root=Path("protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH/PLUGINS/ISOLIERTE_PLUGINS/HD-009-AFFILIATE-ZENTRALE/CURRENT.zip")
patterns=("hdar-amazon-start.css","hdar-ci-amazon-slot","wp_enqueue_style","wp_add_inline_style","wp_enqueue_scripts")
with zipfile.ZipFile(root) as z:
 for name in z.namelist():
  if not name.endswith(".php"):continue
  t=z.read(name).decode("utf8","replace").splitlines()
  hits=[i for i,line in enumerate(t) if any(p in line for p in patterns)]
  if not hits:continue
  print("\nFILE",name,"HITS",len(hits))
  for i in hits[:90]:
   print("  ",i+1,repr(t[i][:400]))
   if "hdar-amazon-start.css" in t[i] or "wp_enqueue_style" in t[i]:
    for j in range(max(0,i-4),min(len(t),i+7)):
     print(f"  + {j+1:5d} {t[j][:420]}")

with zipfile.ZipFile(root) as z:
    name="affiliate-portal-router/includes/class-hdar-amazon-start.php"
    lines=z.read(name).decode("utf8").splitlines()
    for i in list(range(0,105))+list(range(132,147)):
        print("AMAZON START",i+1,lines[i][:520])
