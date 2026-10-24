# HD-005 – HOBBY DEPOT GLOSSAR CORE – CURRENT

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-23
STATUS: **1.0.16 / IMPORT- UND DATEN-HARDPASS / 100 BEGRIFFE / LIVE OFFEN**

Plugin-ID:
`HD-005-GLOSSAR-CORE`

Aktueller Hobby-Depot-Kandidat:
`HOBBY_DEPOT_GLOSSAR_CORE_1.0.16_IMPORT_DATEN_HARDPASS_100_BEGRIFFE.zip`

SHA-256:
`7f1697e62ac3a20da7d34e3d8fe9c75ee102eadbc764b2591e544114ccebebd5`

Fach-Current:
`../../../GLOSSAR/CURRENT_STATE.md`

## Produktionsstand

- technische Basis: 1.0.13 Layout/Typo Hard Pass;
- 100 geprüfte Glossarbegriffe;
- 4 Batches à maximal 25;
- alle Begriffe Draft-only, kein Auto-Publish;
- 150–173 Wörter je Fachtext;
- 0 Bodylinks;
- echte Hauptziele für „Mehr zum Thema“;
- Quellen und Synonyme bleiben interne Metadaten;
- Übergangsregel Kurzdefinition → Fließtext im Validator;
- einmalige idempotente Übernahme der 100 Entwürfe nach Update;
- bestehende sechs Pilotbegriffe werden über stabile external_id aktualisiert, nicht verdoppelt.

## Unverändert gegenüber 1.0.13

- Route;
- Core;
- Frontend;
- SEO-Renderer;
- Templates;
- Hero;
- Layout/Breadcrumbs/Typografie.

## QA

- PHP-Lint 8/8 PASS;
- 100/100 Inhaltsvalidator PASS;
- keine doppelten term-IDs/Slugs;
- Übergangsregel 100/100 PASS;
- ZIP-Integrität PASS;
- exakt ein Root `hobby-depot-glossar/`.

## EXAKT EINE NEXT ACTION

**1.0.15 über den bestehenden Ordner `hobby-depot-glossar` hochladen/überschreiben und WordPress-Admin einmal neu laden.**


## 24.10.2026 – 1.0.16 Import-/Daten-Hardpass
- Ursache der 1.0.15-Liveblockade: lokale Vorprüfung hatte nicht exakt dieselbe Wortzählung wie HDG_Manager::validate_batch().
- 8 Fachtexte mit 148/149 Wörtern korrigiert: Serife, Schrötling, Trittfrequenz, Debouncing, Hot-Swap, Rektaszension, Münzzeichen, Fehlprägung.
- Direkter Aufruf der echten Plugin-Prüfroutine gegen alle vier eingebauten 25er-Batches: 4/4 PASS, 100/100 PASS.
- Finaler Wortbereich: 150–172 Wörter.
- Übergangsregel Kurzdefinition → erster Fließtextsatz: PASS; maximale Überschneidung 0,3333 unter Blockiergrenze 0,35.
- PHP-Lint komplett PASS; ZIP-Integrität PASS; exakt ein Root hobby-depot-glossar/.
