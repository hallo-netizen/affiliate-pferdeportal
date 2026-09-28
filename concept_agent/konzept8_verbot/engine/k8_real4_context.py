#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json
from copy import deepcopy

RETRIEVED_AT="2026-09-26T13:24:47Z"

DATA={
0:{
"source_snapshot_id":"3ac8a725f3e7ebb8a6e332b07e88b989e508e05fe9aa29260aaca6f9bedfc761",
"claims":[
("fact-rp-0-a","Reitplatzplaner werden zur Pflege verschiedener Reitböden eingesetzt.","Der Reitplatzplaner dient der Pflege von Sand-, Sand/Vlies- und weiteren Reitböden."),
("fact-rp-0-b","Striegelzinken lockern die Tretschicht des Reitbodens.","Striegelzinken lockern die Tretschicht"),
("fact-rp-0-c","Ein Planierschild ebnet die Tretschicht; die Arbeitstiefe muss zum jeweiligen Boden passen.","ein Planierschild ebnet sie; die Arbeitstiefe ist einstellbar und muss zum jeweiligen Boden passen.")
],
"runtime":{"order_id":"concept-agent-0b401802eeed8574","article_type":"Beratung","title":"Das Wichtigste über Reitplatzplaner für Pferde","slug":"das-wichtigste-ueber-reitplatzplaner-fuer-pferde","subject_scope":"Das Wichtigste über Reitplatzplaner für Pferde","subject_label":"Reitplatzplaner für Pferde","lead":"Reitplatzplaner für Pferde sollen die Tretschicht passend zum jeweiligen Reitboden lockern und anschließend wieder gleichmäßig einebnen.","conclusion":"Entscheidend ist, dass Arbeitsweise und Arbeitstiefe zum vorhandenen Reitboden passen und sich das Gerät sauber einstellen lässt.","question":"Das Wichtigste über Reitplatzplaner für Pferde","answer":"Die Auswahl richtet sich vor allem nach Bodenaufbau, gewünschter Lockerung, Einebnung und einstellbarer Arbeitstiefe.","summary":"Ein passender Reitplatzplaner lockert und ebnet die Tretschicht, ohne den individuellen Bodenaufbau zu ignorieren.","search_intent":"DECISION_SUPPORT","decision_goal":"Einen Reitplatzplaner auswählen, dessen Arbeitsweise und Einstellmöglichkeiten zum vorhandenen Reitboden passen.","decision_criteria":["Bodenart und Tretschicht","passende Lockerung","gleichmäßige Einebnung","einstellbare Arbeitstiefe"],"allowed_fact_ids":["fact-rp-0-a","fact-rp-0-b","fact-rp-0-c"]}
},
1:{
"source_snapshot_id":"63b926fb25bc073674e5451899a1013e0e618c8285fa40f4fba064d4898bdccb",
"claims":[
("fact-23330868f4b0-1","Ein gesundes Pferd kann sich mit Winterfell und Körperfett gut gegen Kälte isolieren.","Ein gesundes Pferd kann sich mit Winterfell und Körperfett gut gegen Kälte isolieren."),
("fact-23330868f4b0-2","Nässe und Regen verringern die Isolationswirkung des Fells deutlich.","Nässe und Regen verringern die Isolationswirkung des Fells deutlich"),
("fact-23330868f4b0-3","Ob eine Regendecke sinnvoll ist, hängt unter anderem von Nässe, Wind und Schutz ab.","ob eine Regendecke sinnvoll ist, hängt deshalb unter anderem von Nässe, Wind, Schutz"),
("fact-23330868f4b0-4","Auch Schur, Alter, Gesundheit und Körperzustand gehören zu den Faktoren für die Beurteilung einer Regendecke.","Schur, Alter, Gesundheit und Körperzustand ab.")
],
"runtime":{"order_id":"concept-agent-23330868f4b0c797","article_type":"FAQ","title":"Frieren Pferde unter Regendecken?","slug":"frieren-pferde-unter-regendecken","subject_scope":"Frieren Pferde unter Regendecken?","subject_label":"Frieren Pferde unter Regendecken","lead":"Nicht automatisch. Ob ein Pferd unter einer Regendecke friert, hängt nicht allein von der Decke ab, sondern von Nässe, Wind, Schutz, Schur, Alter, Gesundheit und Körperzustand.","conclusion":"Entscheidend sind die gebundenen Einflussfaktoren rund um Kälte, Nässe, Wind, Schutz, Schur, Alter, Gesundheit und Körperzustand.","question":"Frieren Pferde unter Regendecken?","answer":"Nicht automatisch. Ob ein Pferd unter einer Regendecke friert, hängt nicht allein von der Decke ab, sondern von Nässe, Wind, Schutz, Schur, Alter, Gesundheit und Körperzustand.","faq_question":"Frieren Pferde unter Regendecken?","faq_answer":"Nicht automatisch. Ob ein Pferd unter einer Regendecke friert, hängt nicht allein von der Decke ab, sondern von Nässe, Wind, Schutz, Schur, Alter, Gesundheit und Körperzustand.","primary_question":"Frieren Pferde unter Regendecken?","summary":"Nicht automatisch. Ob ein Pferd unter einer Regendecke friert, hängt nicht allein von der Decke ab, sondern von Nässe, Wind, Schutz, Schur, Alter, Gesundheit und Körperzustand.","search_intent":"INFORMATIONAL_DIRECT_QUESTION","allowed_fact_ids":["fact-23330868f4b0-1","fact-23330868f4b0-2","fact-23330868f4b0-3","fact-23330868f4b0-4"]}
},
2:{
"source_snapshot_id":"8acdb8128cb720b2b413dd4edd4cac992b6339530f92c1e6807af4914745ff17",
"claims":[
("fact-916a0af7de79-1","Eine Reitplatzbewässerung von unten ist technisch möglich.","Eine Reitplatzbewässerung von unten ist technisch möglich."),
("fact-916a0af7de79-2","Beim Ebbe-Flut-System wird Wasser unterhalb der Tretschicht geregelt und über Kapillarwirkung in die Tretschicht transportiert.","Beim Ebbe-Flut-System wird Wasser unterhalb der Tretschicht geregelt und über Kapillarwirkung in die Tretschicht transportiert"),
("fact-916a0af7de79-3","Beim Ebbe-Flut-System wird der Wasserpegel gesteuert.","der Wasserpegel wird gesteuert.")
],
"runtime":{"order_id":"concept-agent-916a0af7de798127","article_type":"FAQ","title":"Ist eine Reitplatzbewässerung von unten möglich?","slug":"ist-eine-reitplatzbewaesserung-von-unten-moeglich","subject_scope":"Ist eine Reitplatzbewässerung von unten möglich?","subject_label":"Ist eine Reitplatzbewässerung von unten möglich","lead":"Ja. Eine Bewässerung eines Reitplatzes von unten ist technisch möglich: Beim Ebbe-Flut-System wird Wasser unterhalb der Tretschicht geregelt, über Kapillarwirkung in die Tretschicht transportiert und der Wasserpegel gesteuert.","conclusion":"Ja. Eine Bewässerung eines Reitplatzes von unten ist technisch möglich: Beim Ebbe-Flut-System wird Wasser unterhalb der Tretschicht geregelt, über Kapillarwirkung in die Tretschicht transportiert und der Wasserpegel gesteuert.","question":"Ist eine Reitplatzbewässerung von unten möglich?","answer":"Ja. Eine Bewässerung eines Reitplatzes von unten ist technisch möglich: Beim Ebbe-Flut-System wird Wasser unterhalb der Tretschicht geregelt, über Kapillarwirkung in die Tretschicht transportiert und der Wasserpegel gesteuert.","faq_question":"Ist eine Reitplatzbewässerung von unten möglich?","faq_answer":"Ja. Eine Bewässerung eines Reitplatzes von unten ist technisch möglich: Beim Ebbe-Flut-System wird Wasser unterhalb der Tretschicht geregelt, über Kapillarwirkung in die Tretschicht transportiert und der Wasserpegel gesteuert.","primary_question":"Ist eine Reitplatzbewässerung von unten möglich?","summary":"Ja. Eine Bewässerung eines Reitplatzes von unten ist technisch möglich: Beim Ebbe-Flut-System wird Wasser unterhalb der Tretschicht geregelt, über Kapillarwirkung in die Tretschicht transportiert und der Wasserpegel gesteuert.","search_intent":"INFORMATIONAL_DIRECT_QUESTION","allowed_fact_ids":["fact-916a0af7de79-1","fact-916a0af7de79-2","fact-916a0af7de79-3"]}
},
3:{
"source_snapshot_id":"2a3df396299f6153a2fcbe6d995f0b2872884bf4be72bd3ec1f2c5b2a7291c16",
"claims":[
("fact-160c801f6e1b-1","Ein gut sitzender Kappzaum kann für Spaziergänge genutzt werden.","Ein gut sitzender Kappzaum kann für Spaziergänge"),
("fact-160c801f6e1b-2","Ein gut sitzender Kappzaum kann für Handarbeit und Bodenarbeit genutzt werden.","Handarbeit und Bodenarbeit genutzt werden."),
("fact-160c801f6e1b-3","Ein Kappzaum wirkt über den Nasenbereich statt über das Pferdemaul.","Er wirkt über den Nasenbereich statt über das Pferdemaul"),
("fact-160c801f6e1b-4","Entscheidend sind korrekter Sitz und eine dem Pferd angemessene Einwirkung.","entscheidend sind korrekter Sitz und eine dem Pferd angemessene Einwirkung.")
],
"runtime":{"order_id":"concept-agent-160c801f6e1b6c99","article_type":"FAQ","title":"Kann man mit Kappzaum spazieren gehen?","slug":"kann-man-mit-kappzaum-spazieren-gehen","subject_scope":"Kann man mit Kappzaum spazieren gehen?","subject_label":"Kann man mit Kappzaum spazieren gehen","lead":"Ja. Mit einem gut sitzenden Kappzaum kann man spazieren gehen. Er kann außerdem für Handarbeit und Bodenarbeit genutzt werden; wichtig sind korrekter Sitz und eine dem Pferd angemessene Einwirkung.","conclusion":"Ja. Mit einem gut sitzenden Kappzaum kann man spazieren gehen. Er kann außerdem für Handarbeit und Bodenarbeit genutzt werden; wichtig sind korrekter Sitz und eine dem Pferd angemessene Einwirkung.","question":"Kann man mit Kappzaum spazieren gehen?","answer":"Ja. Mit einem gut sitzenden Kappzaum kann man spazieren gehen. Er kann außerdem für Handarbeit und Bodenarbeit genutzt werden; wichtig sind korrekter Sitz und eine dem Pferd angemessene Einwirkung.","faq_question":"Kann man mit Kappzaum spazieren gehen?","faq_answer":"Ja. Mit einem gut sitzenden Kappzaum kann man spazieren gehen. Er kann außerdem für Handarbeit und Bodenarbeit genutzt werden; wichtig sind korrekter Sitz und eine dem Pferd angemessene Einwirkung.","primary_question":"Kann man mit Kappzaum spazieren gehen?","summary":"Ja. Mit einem gut sitzenden Kappzaum kann man spazieren gehen. Er kann außerdem für Handarbeit und Bodenarbeit genutzt werden; wichtig sind korrekter Sitz und eine dem Pferd angemessene Einwirkung.","search_intent":"INFORMATIONAL_DIRECT_QUESTION","allowed_fact_ids":["fact-160c801f6e1b-1","fact-160c801f6e1b-2","fact-160c801f6e1b-3","fact-160c801f6e1b-4"]}
}
}

def _sha(s:str)->str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

def build_context(item:dict)->dict:
    i=item["item_index"]
    if i not in DATA: raise RuntimeError("K8_REAL4_INDEX_UNSUPPORTED")
    spec=DATA[i]
    research=item["research_bound"]
    sources=research["sources"]
    if len(sources)!=1: raise RuntimeError("K8_REAL4_SOURCE_COUNT")
    source=sources[0]
    claims=[]
    for fid,statement,evidence_text in spec["claims"]:
        if evidence_text not in source["evidence"]: raise RuntimeError("K8_REAL4_FACT_NOT_IN_BOUND_RESEARCH:"+fid)
        claims.append({
          "article_types":[item["identity"]["article_type"]],
          "claim_status":"FULLY_SUPPORTED",
          "evidence_text":evidence_text,
          "evidence_text_sha256":_sha(evidence_text),
          "fact_id":fid,
          "source_id":source["source_id"],
          "source_url":source["source_url"],
          "statement":statement
        })
    pack={
      "contract":"canonical_fact_pack_v1",
      "status":"SOURCE_VERIFIED_PRODUCTION_READY",
      "fact_pack_id":spec["source_snapshot_id"],
      "source_snapshot_id":spec["source_snapshot_id"],
      "sources":[{
        "source_id":source["source_id"],"source_title":source["source_title"],
        "source_url":source["source_url"],"retrieved_at":RETRIEVED_AT,
        "snapshot_sha256":source["snapshot_sha256"],"evidence":source["evidence"]
      }],
      "claims":claims
    }
    plan=deepcopy(item["production_plan_item"])
    plan["source_snapshot_id"]=spec["source_snapshot_id"]
    runtime=deepcopy(spec["runtime"])
    runtime["links"]=deepcopy(plan["quality_binding"]["link_bindings"])
    plan["runtime_order"]=runtime
    if item["identity"]["article_type"]=="FAQ":
        plan["quality_binding"]["faq_direct_answer"]=runtime["faq_answer"]
    # Re-seal quality after the FAQ direct-answer addition.
    plan["quality_binding_hash"]=hashlib.sha256(json.dumps(plan["quality_binding"],ensure_ascii=False,sort_keys=True,separators=(",",":")).encode()).hexdigest()
    return {"fact_pack":pack,"production_plan_item":plan}

def build_all(binding:dict)->dict:
    items=[]
    for item in binding["items"][:4]:
        ctx=build_context(item)
        items.append({"item_index":item["item_index"],"identity":item["identity"],**ctx})
    return {"contract":"K8_REAL4_CONTEXT_V1","item_count":4,"items":items,"publish_allowed":False}
