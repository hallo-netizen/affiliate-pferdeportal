from pathlib import Path
import zipfile,re
base=Path("protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH/PLUGINS/ISOLIERTE_PLUGINS")
target=[
("HD-007-HOBBYREGISTER-CORE","hd-hobbyregister-core/includes/class-hd-hobbyregister-frontend.php",[(350,550),(560,705),(700,795)]),
("HD-009-AFFILIATE-ZENTRALE","affiliate-portal-router/hobby-depot-affiliate-router.php",[(2600,2675)]),
]
for office,file,ranges in target:
 with zipfile.ZipFile(base/office/"CURRENT.zip") as z: lines=z.read(file).decode("utf8").splitlines()
 print("\n","##",office,file,"LINES",len(lines))
 for start,end in ranges:
  print("\nRANGE",start,end)
  for i in range(start-1,min(end,len(lines))): print(f"{i+1:5d}: {lines[i][:500]}")
