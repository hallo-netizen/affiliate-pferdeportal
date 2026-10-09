# HOBBYRAUSCH – SEO_KATEGORIEN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-09
STATUS: RULE 2.7 / 2357 ZIELOBJEKTE / LIVE-PASS / ABGESCHLOSSEN

## Autoritative Bindung

Zielvertrag:
`ZIELVERTRAG_HD001_AUTOMATISCHE_SEO_HIERARCHIE_20261003.md` – Fassung 2.7.

Technische Plugin-Wahrheit:
`../PLUGINS/PLUGIN_AKTEN/HD-001-KATEGORIE-WORKFLOW/CURRENT.md`.

Finale Live-Evidence:
`HD001_FINAL_LIVE_ACCEPTANCE_20261009.md`.

Wiederverwendbarer Workflow für neue Themen:
`../PROJEKTLEITUNG/HOBBYRAUSCH_UEBERGABE_OPTIMIERTER_WORKFLOW_NEUES_THEMA_20261009.md`.

## Produktiver Endstand

WordPress / Hobby Depot:
- Plugin-Codebasis 1.14.8;
- Runner COMPLETE;
- reason `TARGET_TREE_SYNC_AND_READBACK_PASS`;
- Live-Profilrevision `HD-TARGET-3P-RULE27-CATEGORY-GAPFIX-HOBBYFINDER-20261009+0f4dbf59238a7d83`;
- 2371 logische Knoten;
- 2357 physische Zielobjekte;
- 2357/2357 Readback;
- 256 created;
- 2100 updated;
- 1 unchanged;
- 1 archived;
- 0 adopted;
- 0 editorial demotions;
- error leer.

Frontend:
- PASS;
- 8 Welten;
- 330/330 terminale CORE-Seiten im Kategorie-Gate;
- Verteilung 129×5 / 139×6 / 55×7 / 7×8;
- 0 Kategorie-Gate-Fehler;
- 0 ungebundene CORE-Seiten.

Magazin:
- Hobbyfinder ist direkte Hauptkategorie;
- darunter Hobbywelten / Alleine / Zu zweit / Gruppe;
- altes `Hobby finden` archiviert.

## Regel-2.7-Endstand

Lokaler Kategorienbeweis vor Live:
- 1920 aktive CORE-Content-Kategorien;
- 1665 vorhandene Bestands-Leafs vollständig erhalten;
- 255 neue Leafs mit jeweils >=3 unterschiedlichen Supporting Intents;
- keine generisch erzwungenen `Ausrüstung & Kosten`-Leafs;
- keine Kategorie unter Kategorie;
- keine doppelten Slugs;
- keine fehlenden Parents;
- keine Zyklen;
- 8 Welten ROOT;
- Hobbywelten nur View;
- sichtbare Direktkinder: Gestalten 7 / Fertigen 10 / Technik 9 / Forschen 5 / Pflanzen 9 / Tiere 7 / Bewegen 8 / Sammeln 8.

## Lokale technische Abnahme

Finales geprüftes Release:
`HD001_V1.14.8_RULE27_FINAL_VERIFIED_E2E_20261009.zip`

SHA-256:
`709134631895a901bcb4fc5f5d71889d317954d9928c0ed20700883990a5a52c`

Beweis:
- statischer Kategorienbaum 43/43 PASS;
- positive + negative E2E 14/14 PASS;
- Full Sync / Resume / Readback PASS;
- Idempotenz 0 Delta;
- Drift-Erkennung PASS;
- injizierter Write-Fehler -> exakter Rollback PASS;
- AJAX/Nonce positiv + negativ PASS;
- PHP 33/33 PASS;
- ZIP-Integrität PASS.

## ERSTER OFFENER BLOCKER

KEINER für den abgeschlossenen HD-001-Kategorienlauf.

## EXAKT EINE NEXT ACTION

Für den bestehenden Kategorienbaum:
**keine weitere Aktion. Nicht erneut synchronisieren.**

Für ein neues Thema:
den wiederverwendbaren Workflow
`../PROJEKTLEITUNG/HOBBYRAUSCH_UEBERGABE_OPTIMIERTER_WORKFLOW_NEUES_THEMA_20261009.md`
lesen und ausschließlich als Delta gegen diese 2357er Live-Baseline arbeiten.

## NICHT ANFASSEN

- keine Vollrekonstruktion des bestehenden Portals;
- keine Wiederbelebung 1.14.9/1.14.10;
- keine neue Architektur ohne bewiesenen Enginefehler;
- keine Rücknahme von Performanceoptimierungen;
- keine generischen Pflicht-Leafs ohne >=3 echte Intents;
- keine Zwischen-ZIPs;
- kein Sync ohne kompletten lokalen POS+NEG-E2E-Hard-Pass und anschließenden Live-Dry-Run.
