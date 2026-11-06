#!/usr/bin/env python3
from zipfile import ZipFile
from pathlib import Path
import json
root=Path("protocol/PROJECT_MEMORY/PROJEKTE/EIGENTUMSSCHUTZ")
design=root/"PLUGINS/ISOLIERTE_PLUGINS/HAB-001-DESIGN/CURRENT.zip"
with ZipFile(design) as z:
    names=[x for x in z.namelist() if x.endswith("/nodes.json")]
    assert len(names)==1,names
    data=json.loads(z.read(names[0]))
nodes=[]; mapping={}
for node in data["nodes"]:
    if not isinstance(node,dict) or not node.get("id"): continue
    nid=node["id"]
    nodes.append(dict(node_id=nid,pillar=node.get("pillar",""),
      display_name=node.get("name",""),slug=node.get("slug",""),
      parent_id=node.get("parent",""),object_type=node.get("type","")))
    mapping[nid]=dict(object_type=node.get("type",""),
      object_id=int(node.get("wp_id") or 0))
snapshot=dict(revision="real-hab-category-test",nodes=nodes,mapping=mapping)
target=root/"AFFILIATE/HAB_BAU/_build/hb-real-design-nodes-snapshot.json"
target.write_text(json.dumps(snapshot,ensure_ascii=False))
print("HB_OFFICIAL_DESIGN_NODES_LOADED",len(nodes))
