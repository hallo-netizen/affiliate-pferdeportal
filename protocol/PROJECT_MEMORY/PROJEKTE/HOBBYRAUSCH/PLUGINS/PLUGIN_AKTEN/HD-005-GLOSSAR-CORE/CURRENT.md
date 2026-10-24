# HD-005 – HOBBY DEPOT GLOSSAR CORE – CURRENT

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-24
STATUS: **1.0.19 / 300 BEGRIFFE / A–Z + THEMENCOVERAGE HARD PASS / LIVE OFFEN**

Plugin-ID:
`HD-005-GLOSSAR-CORE`

Aktueller Hobby-Depot-Kandidat:
`HOBBY_DEPOT_GLOSSAR_CYBERDUCK_1.0.19_300_BEGRIFFE_AZ_THEMEN_HARDPASS.zip`

SHA-256:
`d959e0b3a40069121dc803d23c0bf1fa33f6ac8d4df842018421df7875ea4a74`

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


## 24.10.2026 – 1.0.17 Produktionsbestand 150 Begriffe
- 50 neue Glossarbegriffe (101–150) in zwei weiteren 25er-Batches.
- Themen: Fotografie, Keramik, Holz, Pflanzen, Imkerei, Numismatik, Mikroskopie, Astronomie, Typografie, Elektronik.
- echte HDG_Manager::validate_batch()-Routine: 6/6 Batches PASS, 150/150 Begriffe PASS.
- globale Dublettenprüfung: 150 eindeutige external_id, 150 eindeutige Slugs.
- Fachtexte 150–172 Wörter; 0 Bodylinks; Quellen und Hauptziele vollständig.
- Update-Simulation mit bereits vorhandenen 100 Begriffen: 100 übernommen/aktualisiert + 50 ergänzt = 150/150 PASS.
- Layout, Route, Hero und Frontenddarstellung gegenüber 1.0.16 nicht umgebaut.
- Artefakt: `HOBBY_DEPOT_GLOSSAR_CYBERDUCK_1.0.19_300_BEGRIFFE_AZ_THEMEN_HARDPASS.zip`
- SHA-256: `d959e0b3a40069121dc803d23c0bf1fa33f6ac8d4df842018421df7875ea4a74`


## 24.10.2026 – 1.0.18 AJAX-Fix + 200 Begriffe
- Produktionsbestand auf 200 Begriffe erweitert, 8 Batches à 25.
- Ursache des WordPress-Fehlerwegs abgesichert: admin_init läuft auch bei admin-ajax.php; der gebündelte Import kehrt bei AJAX/Heartbeat und REST jetzt sofort zurück.
- Pro normalem Admin-Aufruf wird maximal ein 25er-Batch importiert.
- Simulation mit vorhandenem 150er-Stand: AJAX 150→150 PASS; normale Admin-Aufrufe 150→175→200 PASS.
- echte HDG_Manager::validate_batch()-Routine: 8/8 Batches PASS, 200/200 PASS.
- globale Dublettenprüfung: 200 eindeutige external_id, 200 eindeutige Slugs.
- Wortbereich 151–178 Wörter.
- PHP-Lint 8/8 PASS; ZIP-Integrität PASS; exakt ein Root `hobby-depot-glossar/`.
- Cyberduck-Vertrag: Ordner `hobby-depot-glossar` direkt über den bestehenden Pluginordner kopieren/ersetzen.
- Artefakt: `HOBBY_DEPOT_GLOSSAR_CYBERDUCK_1.0.19_300_BEGRIFFE_AZ_THEMEN_HARDPASS.zip`
- SHA-256: `d959e0b3a40069121dc803d23c0bf1fa33f6ac8d4df842018421df7875ea4a74`


## 1.0.19
300 Begriffe; A–Z vollständig; alle acht Hobbywelten mindestens 31 Begriffe; 12/12 Batches PASS; Cyberduck-Ordner bleibt `hobby-depot-glossar`.
