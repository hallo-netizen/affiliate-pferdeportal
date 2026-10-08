# Affiliate Zentrale 6.72.206 – Glossar/Rassen Real-Injection-Rootfix

Datum: 2026-10-08

## Live-Ausgangslage
Nutzer-Livereadback 6.72.204:
- Tarifrechner: PASS – zweiter automatischer Banner mitten im Text ist weg.
- Glossar-Einzelbeiträge: FAIL – kein Banner sichtbar.
- Pferderassen-Einzelbeiträge: FAIL – kein Banner sichtbar.

## Exakte Root Cause
Der echte WordPress/MariaDB-Negativlauf für 6.72.205 zeigte:
- Desktop-Creative 310x310 war für `glossary_single_desktop_banner` und `breed_single_desktop_banner` technisch formatgültig.
- Seine Placements enthielten korrekt `hub_grid_card`, `glossary_single_desktop_banner`, `breed_single_desktop_banner`.
- Der allgemeine Fallback-Planer wählte jedoch `hub_grid_card` zuerst als Aktivierungsanker.
- `hub_grid_card` ist bewusst kein Auto-Publish-Slot.
- Folge: Ausgabeobjekt `draft`, Kampagne `active=false`; die gültigen Glossar-/Rassen-Desktop-Placements konnten daher nicht rendern.
- Mobil wählte direkt `glossary_single_mobile_banner`, wurde `published` / `active=true` und funktionierte im gleichen Negativlauf.

## KISS-Rootfix 6.72.206
Nur für den bestehenden allgemeinen Banner-Fallback werden technisch kompatible redaktionelle Single-Slots vor `hub_grid_card` als Aktivierungsanker priorisiert:
1. glossary_single_desktop_banner
2. breed_single_desktop_banner
3. glossary_single_mobile_banner
4. breed_single_mobile_banner
5. danach unverändert alle übrigen kompatiblen Slots.

Kein neues Ranking, keine neue Tabelle, keine neue Frontend-DB-Abfrage, kein Frontend-HTTP. Die bestehende Formatprüfung und alle Placements bleiben erhalten.

Der 6.72.205-DOM-Fallback bleibt enthalten:
- historischer Glossar-/Rassen-Anker vorhanden -> bisherige Position bleibt;
- Anker fehlt -> derselbe bereits formatgeprüfte Banner wird am Ende des Einzelinhalts ausgegeben.

## Echter WordPress + MariaDB Positiv-/Negativnachweis
Workflow Run: 37765412152
Job: 113271746824
Ergebnis: SUCCESS

Planung:
- Desktop: created=2, drafts=1, active=1, blocked=0, review=1
- Mobil: created=2, drafts=1, active=1, blocked=0, review=1

Fokussierte Assertions: 24 PASS / 0 FAIL
Unter anderem:
- desktop_banner_materialized PASS
- mobile_banner_materialized PASS
- Glossar Desktop Format positiv/negativ PASS
- Glossar Mobil Format positiv/negativ PASS
- Rassen Desktop/Mobil Format PASS
- Glossar ohne alten Designanker Desktop sichtbar PASS
- Glossar ohne alten Designanker Mobil sichtbar PASS
- Rasse ohne alten Designanker Desktop sichtbar PASS
- Rasse ohne alten Designanker Mobil sichtbar PASS
- alter Glossar-Anker Position erhalten PASS
- alter Rassen-Anker Position erhalten PASS
- Duplicate-Guard Glossar PASS
- Duplicate-Guard Rassen PASS
- live-bestätigter Rechner-Suppression-Pfad unverändert PASS
- unterer Rechner-Banner nicht unterdrückt PASS

## Exakter getesteter Installer
- Datei: AFFILIATE_ZENTRALE_6.72.206.zip
- SHA256: 7bcfab7f15913d4d80c3c0ba9959f3f63ca19f6db593e1924035f3dc3a6db4e1
- Bytes: 821045
- Source/ZIP Byteidentität: 28/28 PASS
- Workflow Artifact ID: 11543543898

Ergebnis: **GLOSSARY_BREED_6_72_206_REAL_WORDPRESS_INJECTION_GATES_PASS**

Live-Status bleibt bis zur Installation offen.
