from pathlib import Path
import json, subprocess, tempfile, sys
ROOT=Path(__file__).parent
SNAP=Path(sys.argv[1]) if len(sys.argv)>1 else ROOT/'live_fixture'/'wordpress_snapshot.json'
RESEARCH='''Live test research. Hindernisstangen werden in Bodenarbeit, Cavaletti- und Springtraining verwendet. Für die Auswahl sind Einsatzzweck, Material, Gewicht, Sichtbarkeit, Lagerung und sichere Handhabung relevant. Diese Recherche ist nur Testinhalt für den isolierten Workflow.'''
FACTS='''Live test facts. Titel, Zielkeyword, Kategorie, Beitragsart und Plan-Slot stammen ausschließlich aus dem WordPress-Snapshot. Externe Daten dürfen weder Route noch Publish-Status verändern. Die Ausgabe muss WordPress-Status draft behalten.'''
BAD='# Falscher Titel\n\nKurzer Testtext.'
GOOD='''# Das Wichtigste über Hindernisstangen für Pferde

Hindernisstangen für Pferde gehören zu den vielseitigsten Trainingshilfen im Alltag. Sie können bei Bodenarbeit, Cavalettiarbeit und beim Springtraining eingesetzt werden. Entscheidend ist nicht eine pauschal beste Ausführung, sondern ob Material, Gewicht, Sichtbarkeit und Handhabung zum geplanten Einsatz passen. Wer vor dem Kauf den eigenen Trainingsalltag betrachtet, kann unnötige Kompromisse vermeiden und die Auswahl nachvollziehbar eingrenzen.

## Einsatz zuerst festlegen

Für Schritt- und Trabstangen sind andere Eigenschaften wichtig als für regelmäßig aufgebaute Gymnastikreihen. Leichtere Stangen lassen sich schnell versetzen und erleichtern häufige Umbauten. Mehr Eigengewicht kann dagegen sinnvoll sein, wenn die Stangen ruhiger liegen sollen. Auch der Untergrund spielt eine Rolle. Auf tiefem oder unebenem Boden verhält sich eine Stange anders als auf einem festen Reitplatz. Deshalb sollte die Auswahl immer mit dem tatsächlichen Trainingsort beginnen.

## Material und Alltag berücksichtigen

Holz und Kunststoff unterscheiden sich vor allem bei Gewicht, Pflege und Witterungsbeständigkeit. Holz kann robust sein, benötigt je nach Ausführung aber regelmäßige Kontrolle und Pflege. Kunststoff ist oft leichter und unempfindlicher gegen Feuchtigkeit, kann sich jedoch beim Handling anders anfühlen. Wichtig ist außerdem eine gut sichtbare Gestaltung. Klare Kontraste helfen Pferd und Reiter, Abstände und Positionen im Training früh zu erkennen.

Bei der Lagerung sollte berücksichtigt werden, wie oft die Stangen bewegt werden und ob sie dauerhaft im Freien liegen. Eine ordentliche Ablage reduziert Beschädigungen und erleichtert die Kontrolle. Risse, scharfe Kanten oder beschädigte Oberflächen sollten vor dem Einsatz erkannt werden. Auch das Gewicht sollte zu den Personen passen, die den Platz regelmäßig auf- und abbauen.

## Sicherheit vor Bequemlichkeit

Eine Hindernisstange sollte sich praktisch handhaben lassen, ohne dass dafür sichere Eigenschaften geopfert werden. Sehr leichte Lösungen können komfortabel sein, müssen aber zum vorgesehenen Training passen. Umgekehrt ist eine besonders schwere Stange nicht automatisch besser. Entscheidend ist, dass sie für Pferd, Reiter und Helfer berechenbar bleibt und keine unnötigen Verletzungsrisiken entstehen.

Vor jeder Nutzung lohnt ein kurzer Blick auf Zustand, Lage und Abstand. Gerade bei häufig genutzten Trainingsmitteln verhindert diese einfache Routine, dass kleine Schäden übersehen werden. So bleibt die Auswahl nicht nur eine Kaufentscheidung, sondern Teil eines sicheren Trainingsablaufs.

## Auswahl systematisch treffen

Sinnvoll ist eine kurze Reihenfolge: zuerst Trainingszweck, danach Untergrund, Material, Gewicht, Sichtbarkeit und Lagerung prüfen. Erst wenn diese Punkte feststehen, lohnt sich der Vergleich konkreter Angebote. Auf diese Weise wird aus einer großen Produktauswahl eine überschaubare Entscheidung, die zum eigenen Stallalltag passt.
'''

def run(cmd, expect=(0,)):
 p=subprocess.run(cmd,text=True,capture_output=True); print(p.stdout.strip())
 if p.returncode not in expect: raise SystemExit('UNEXPECTED_RC:'+str(p.returncode)+' '+p.stderr)
 return p
with tempfile.TemporaryDirectory() as td:
 td=Path(td); w=td/'room'; out=td/'out'; r=td/'research.txt'; f=td/'facts.txt'; b=td/'bad.md'; g=td/'good.md'
 r.write_text(RESEARCH); f.write_text(FACTS); b.write_text(BAD); g.write_text(GOOD)
 run([sys.executable,str(ROOT/'codex_entry.py'),'start',str(SNAP),str(w)])
 run([sys.executable,str(ROOT/'controller.py'),'research',str(w),str(r)])
 run([sys.executable,str(ROOT/'controller.py'),'facts',str(w),str(f)])
 run([sys.executable,str(ROOT/'controller.py'),'draft',str(w),str(b)])
 run([sys.executable,str(ROOT/'controller.py'),'check',str(w)],expect=(3,))
 s=json.loads((w/'state.json').read_text()); assert s['phase']=='REPAIR_REQUIRED' and s['last_error']=='TITLE_BINDING_FAIL'
 run([sys.executable,str(ROOT/'codex_entry.py'),'next',str(w)])
 run([sys.executable,str(ROOT/'controller.py'),'draft',str(w),str(g)])
 run([sys.executable,str(ROOT/'controller.py'),'check',str(w)])
 run([sys.executable,str(ROOT/'controller.py'),'release',str(w),str(out)])
 s=json.loads((w/'state.json').read_text()); assert s['phase']=='RELEASED' and s['released'] is True and s['revision']==2
 rel=json.loads((out/'release.json').read_text()); assert rel['publish_allowed'] is False and rel['wordpress_status']=='draft'
 xml=(out/'wordpress_draft.xml').read_text(); assert '<wp:status>draft</wp:status>' in xml and s['article']['title'] in xml
 s['article']['title']='MANIPULIERT'; (w/'state.json').write_text(json.dumps(s,ensure_ascii=False,indent=2,sort_keys=True))
 run([sys.executable,str(ROOT/'codex_entry.py'),'next',str(w)],expect=(0,))
 p=subprocess.run([sys.executable,str(ROOT/'controller.py'),'release',str(w),str(out/'tampered')],text=True,capture_output=True)
 print(p.stdout.strip()); assert p.returncode==2 and 'IMMUTABLE_CORE_TAMPERED' in p.stdout
 print('SYSTEM4_FIRST_CODEX_BOUNDARY_LIVE_TEST_PASS')
