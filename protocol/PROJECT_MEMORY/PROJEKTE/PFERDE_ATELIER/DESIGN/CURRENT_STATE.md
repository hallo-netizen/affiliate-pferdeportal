# DESIGN – CURRENT STATE

STAND: 2026-09-13

## AUTORITÄT DIESER DATEI

Diese Datei ist die **einzige aktuelle Campus-Standzusammenfassung dieses Büros**.

- aktuelle Arbeit / NEXT ACTION → `HOBBYRAUM.md`
- Fehler → `protocol/PROJECT_MEMORY/FEHLERREGISTER.md` → autoritative Fehlerquelle
- Zielvertrag → `protocol/PROJECT_MEMORY/ZIELVERTRAEGE/REGISTER.md` → Hauptquelle
- Änderungsgrund → `protocol/PROJECT_MEMORY/AENDERUNGSREGISTER.md`
- Historie → `protocol/PROJECT_MEMORY/ARCHIV/REGISTER.md`

Technische/Fachwahrheit bleibt an den in dieser Datei verlinkten Originalquellen. Andere Campus-Dateien dürfen diesen dynamischen Bürostand nicht als zweite Wahrheit fortschreiben.

## Aktueller LIVE-Stand

**Pferde Atelier Design 1.50.472 / Contract V104 + DESIGN-ORDER-SWAP-002**

Basis-Live:
GitHub Branch:
`fix/category-intro-targeted-79-v150472-20260831`

Commit:
`f1e074b2e6dae9bec76ee8ab3f177080f69d2d41`

Basis-Live-Beleg:
`design-baseline/2026-08-31/v150472-category-intro-79/LIVE_PASS.md`

Zusätzlicher aktuell bestätigter Live-Patch:
**Affiliate-Produkte / Produktvorschläge stehen über der Beitragsvorschau.**
Affiliate-Banner sowie Artikel-/Verweisstruktur bleiben unverändert.

Live-Patch-Beleg:
`LIVE_PASS_DESIGN_ORDER_SWAP_002.md`

Exakter aktuell gebundener LIVE-Artefakt-SHA-256:
`11b664a10d4ef0ec82f0011436eb92715d9efd14474893fecddcb64e91e6fe0b`

`main` bleibt für diesen LIVE-Stand nicht führend und wird nicht automatisch verändert.

## Aktueller technischer Kandidat – Journal V1.50.477

Status:
**TECHNISCHER KANDIDAT PASS / PFERDE-LIVE-READBACK OFFEN**

Arbeitsbranch:
`hobbyroom/design-journal-wissen-v150477-20260913`

Ausgangsbasis sind exakt die oben gebundenen LIVE-Bytes mit SHA `11b664…`.

Ziel der Änderung:
- normale redaktionelle Journal-Themen bleiben oben;
- `Pferderassen` wird aus diesem Themenraster herausgenommen;
- neuer eigener Bereich `Wissen & Nachschlagen` mit zwei breiten Kacheln `Glossar` und `Pferderassen`;
- danach `Neu im Journal`;
- Glossar- und Pferderassen-Beiträge werden aus `Neu im Journal` und `Besonders lesenswert` hart ausgeschlossen.

Neue WordPress-Kategorie `Glossar`:
- exakter Slug `glossar`;
- ersatzweise exakter Name `Glossar`;
- keine unscharfe Erkennung;
- fehlt die Kategorie, wird keine Ersatzkategorie erfunden.

Technische Prüfung:
- 8 redaktionelle + 2 Nachschlagebereiche PASS;
- Abschnittsreihenfolge PASS;
- Query-Ausschluss positiv/negativ PASS;
- Glossar-Auflösung positiv und fail-closed negativ PASS;
- PHP-Lint PASS;
- genau eine Plugin-Datei geändert PASS;
- Paketpfade 498/498 identisch PASS;
- Source ↔ entpacktes ZIP identisch PASS;
- ZIP-Integrität PASS.

Übergabepaket:
`PFERDE_ATELIER_DESIGN_V1.50.477_CONTRACT_V104_JOURNAL_WISSEN_NACHSCHLAGEN_INSTALLIEREN.zip`

SHA-256:
`5fe869e076bf3c30f34889cd6a887c23eb46a81b5502f49a859abffb380db458`

**Wichtig:** 1.50.477 ist noch kein LIVE-Stand. Bis zur realen Nutzerprüfung bleibt ausschließlich `1.50.472 / Contract V104 + DESIGN-ORDER-SWAP-002` die LIVE-Wahrheit.

## Übergebene Masterbasis

Vom Nutzer übergeben und vollständig archiviert:
- Plugin 1.50.469 / Contract V104;
- vollständiger Master 1.50.469 / Contract V104.

Diese beiden Dateien sind vollständige historische Basis für die spätere GitHub-Kette 1.50.470→1.50.472.

## Spätere GitHub-Kette

1.50.470: gezielte 45 Kategorietextkorrekturen.

1.50.471: gezielte Erweiterung auf 70.

1.50.472: final 79/79 Audit-Scope.

MASTER_STATUS V1.50.472 sagt:
- vollständiger Master basiert ausdrücklich auf dem vollständigen 1.50.469/V104-Master;
- CURRENT_PLUGIN_SOURCE auf 1.50.472 aktualisiert;
- Installer 1.50.470/.471/.472 ergänzt;
- 388 Seitentexte + 1052 Leaftexte = 1440;
- allgemeiner und Pferde-V104-Vertrag byte-identisch zu 1.50.469;
- keine CSS/JS/Journal/Tabellen/Affiliate/Such/Breadcrumb/Bild/Karten/Publish-Änderung.

## QA V1.50.472

- Source ↔ finaler Installer: 498/498 PASS;
- 309/309 alte Seitentexte wertidentisch;
- 1052/1052 Leaftexte wertidentisch;
- 79/79 neue auditgebundene Seitentexte PASS;
- Search-Plugin-Quelle byte-identisch PASS;
- allgemeiner V104-Vertrag byte-identisch PASS;
- Pferde-V104-Vertrag byte-identisch PASS;
- Manifest-Readback/ZIP-Integrität PASS;
- LIVE PASS nach Nutzerbestätigung dokumentiert.

## Aktuelle Designregel

V104 bleibt unverändert.

Zusätzlich LIVE bestätigt: Auf der zentralen Kategorieebene stehen Affiliate-Produkte / Produktvorschläge vor der Beitragsvorschau; der Affiliate-Banner bleibt unverändert an seiner bisherigen Position.

## NEXT ACTION

Exaktes 1.50.477-Paket real installieren und ausschließlich die Journal-Startseite Desktop/Mobil sowie den Ausschluss von Glossar-/Rassenbeiträgen prüfen. Erst danach LIVE-Wahrheit ändern.
