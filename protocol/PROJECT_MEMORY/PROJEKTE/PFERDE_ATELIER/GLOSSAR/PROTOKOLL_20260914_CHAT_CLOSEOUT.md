# GLOSSAR – PROTOKOLL CHAT-CLOSEOUT 2026-09-14

ROLLE: HISTORISCHES AUSFÜHRUNGSPROTOKOLL; keine zweite CURRENT-/Fehler-/Zielwahrheit.

## Tatsächlich bestätigte LIVE-Befunde

- Nutzer bestätigte: `artikelanzeige pass` → Einzelbegriffe öffnen real → LIVE PASS.
- Danach real gemeldet: verwandte Begriffe noch im Fließtext, `Stockmaß` doppelt verlinkt, rechte Verwandt-Box/Icons fehlen bzw. stimmen nicht, Breadcrumbs falsch.

Aktueller Fehlerstatus ausschließlich in `FEHLERQUELLEN.md`.

## Dauerhafte Regeln nachgeholt

`TEXT_UND_LINKREGELN.md` wurde in den aktiven Hobbyraum übernommen. Verbindlich insbesondere:
- 150–200 Wörter;
- keine Zwischenüberschriften;
- individuelle Texte ohne wiederkehrende Floskeln;
- nur geprüfte WDB-Fakten;
- Kurzdefinition Pflicht;
- kein Linkziel doppelt;
- bevorzugt übergeordnete Portal-Kategorie, Journal nur ersatzweise;
- verwandte Glossarbegriffe ausschließlich in der rechten Linkbox, nicht zusätzlich im Fließtext.

## Tatsächlich ausgeführte lokale Prüfungen am finalen lokalen Stand

### Glossar Core / Engine 1.2.1
Paket: `UNIVERSAL_GLOSSARY_ENGINE_1.2.1_GLOSSAR_ARTIKEL_UPDATE_INSTALLIEREN.zip`
SHA-256: `f6788524f50413541ea40e33bc7005a4e936e2915e4465cf2e7a08e221c900e0`

Ausgeführt:
- `FINAL_test_core_121_contract.php` → `CORE_121_POS_NEG_PASS`;
- `FINAL_test_core_121_update.php` → `CORE_121_EXISTING_IDS_OVERWRITE_POS_NEG_PASS`;
- `FINAL_test_core_121_foreign.php` → `CORE_121_FOREIGN_FAILCLOSED_AND_NORMAL_POST_NEG_PASS`;
- ZIP-Lesetest → PASS;
- Version 1.2.1 → PASS.

Konkrete Vertragswerte: 14 Begriffe, jeweils 150–200 Wörter, genau 1 Fließtext-Link, Related separat gebunden.

### Pferde Atelier Design 1.50.489
Paket: `PFERDE_ATELIER_DESIGN_V1.50.489_GLOSSAR_EINZELANSICHT_FIX_INSTALLIEREN.zip`
SHA-256: `fc6bc67a827f314e37c597e4fbb764f616c86d97bfc6d621c238c813a64ab600`

Ausgeführt:
- PHP-Lint → PASS;
- ZIP-Lesetest → PASS;
- Version 1.50.489 → PASS;
- `FINAL_test_design_150489_browser.py` bei 1200/900/720/500 px → `DESIGN_150489_POS_NEG_PASS`.

Browserbelegt:
- Breadcrumb `Startseite > Glossar > Pferd & Biologie > Bandmaß`;
- falscher globaler Breadcrumb auf Glossar-Single verborgen;
- Kurzdefinition + rechte Box desktop bündig;
- 2 Sideboxen;
- mindestens 3 Icons;
- kein Overflow.

## Nicht ausgeführt / nicht behaupten

- kein realer LIVE-Readback der exakten lokalen Paketbytes 1.2.1 / 1.50.489;
- kein autoritativ gebundener GitHub-Quellcommit dieser finalen Paketbytes;
- kein neues `CURRENT.zip`/`MANIFEST.md` für diese finalen Kandidaten;
- keine Freigabe neuer Glossarbegriffe ohne frisch gelesene `GEPRUEFT`-WDB-Quelle.

## Nachholungen in Campus/Fachbüro

Aktualisiert:
- `CURRENT_STATE.md`;
- `HOBBYRAUM.md`;
- `FEHLERQUELLEN.md`;
- `START_HERE.md`;
- `TEXT_UND_LINKREGELN.md`;
- `../PLUGINS/REGISTER.md`;
- `../PLUGINS/UPDATEPROTOKOLL.md`.

Plugin-Artefaktsynchronisierung bewusst **nicht** durchgeführt, weil Quell-/Releasebindung für die finalen lokalen Kandidaten fehlt. Alte `CURRENT.zip` nicht ersetzt.
