# HD-005 – HOBBY DEPOT GLOSSAR CORE – CURRENT

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-24
STATUS: **1.0.23 / GLOSSAR-STARTLINK HOVER HARD PASS / 308 BEGRIFFE / LIVE OFFEN**

Plugin-ID:
`HD-005-GLOSSAR-CORE`

Aktueller Hobby-Depot-Kandidat:
`HOBBY_DEPOT_GLOSSAR_CYBERDUCK_1.0.23_HOVER_HARDPASS.zip`

SHA-256:
`ba95a5a2919ae4fce30a209c99dac0c3acda19128bd9fd5caf2ab46024931991`

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
- Artefakt: `HOBBY_DEPOT_GLOSSAR_CYBERDUCK_1.0.23_HOVER_HARDPASS.zip`
- SHA-256: `ba95a5a2919ae4fce30a209c99dac0c3acda19128bd9fd5caf2ab46024931991`


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
- Artefakt: `HOBBY_DEPOT_GLOSSAR_CYBERDUCK_1.0.23_HOVER_HARDPASS.zip`
- SHA-256: `ba95a5a2919ae4fce30a209c99dac0c3acda19128bd9fd5caf2ab46024931991`


## 1.0.19
300 Begriffe; A–Z vollständig; alle acht Hobbywelten mindestens 31 Begriffe; 12/12 Batches PASS; Cyberduck-Ordner bleibt `hobby-depot-glossar`.


## 24.10.2026 – 1.0.20 finaler Lückenschluss
- Endbestand: 308 Glossarbegriffe.
- Mindestabdeckung A–Z: mindestens 5 Begriffe je Buchstabe.
- Mindestabdeckung Hobbywelten: mindestens 30 Begriffe je Welt; kleinste Welt Tiere = 31.
- Ergänzt ausschließlich 8 Lückenbegriffe: Jute, Quadrant, Xenolith, Xylem, Yagi-Antenne, Yaw, Yarn Over, Yarn Weight.
- echte HDG_Manager::validate_batch()-Routine: 13/13 Batches PASS, 308/308 eindeutige IDs und Slugs.
- Fachtexte 151–178 Wörter.
- AJAX-Sperre bleibt aktiv; Update-Simulation 300→308 in einem normalen Admin-Aufruf PASS.
- PHP-Lint komplett PASS; ZIP-Integrität PASS; exakt ein Root `hobby-depot-glossar/`.
- Artefakt: `HOBBY_DEPOT_GLOSSAR_CYBERDUCK_1.0.23_HOVER_HARDPASS.zip`
- SHA-256: `ba95a5a2919ae4fce30a209c99dac0c3acda19128bd9fd5caf2ab46024931991`


## 24.10.2026 – 1.0.21 Glossar-Übersicht Design/Navigation
- Kachel-Kurzdefinition von 10.5 px auf 11.5 px erhöht.
- Link „Zum Begriff“ von 9.5 px auf 10.5 px erhöht.
- Begriffsanzahl auf der öffentlichen Glossarübersicht vollständig entfernt.
- Überschrift abhängig vom aktiven Zustand:
  - Start: „Alle Glossarbegriffe“
  - Hobbywelt: „Begriffe: <Hobbywelt>“
  - Buchstabe: „Begriffe mit <Buchstabe>“
  - Suche: „Suchergebnisse“
- Link „Zur Glossar-Startseite“ rechts in der Kopfzeile über den Kacheln.
- zweiter Link „Zur Glossar-Startseite“ im unteren Navigationsbereich neben/unter der Pagination.
- 308 Begriffe und Produktionsdaten unverändert; keine Inhaltsänderung.
- PHP-Lint 8/8 PASS; ZIP-Integrität PASS.
- Artefakt: `HOBBY_DEPOT_GLOSSAR_CYBERDUCK_1.0.23_HOVER_HARDPASS.zip`
- SHA-256: `ba95a5a2919ae4fce30a209c99dac0c3acda19128bd9fd5caf2ab46024931991`


## 24.10.2026 – 1.0.22 Design-Render-Hardpass
- 1.0.21 war nur auf Quellcode-Ebene geprüft; 1.0.22 wird zusätzlich als tatsächlich gerenderte Ausgabe geprüft.
- Vorschautext Kachel: 12.5 px, mit stärkerem Selektor/important gegen Theme-Überschreibung.
- Link „Zum Begriff“: 11.5 px, ebenfalls gehärtet.
- Start: „Alle Glossarbegriffe“.
- Themenfilter: „Begriffe zum Thema <Hobbywelt>“.
- Buchstabenfilter: „Begriffe mit <Buchstabe>“.
- Suche: „Suchergebnisse“.
- öffentliche Begriffsanzahl entfernt.
- „Zur Glossar-Startseite“ oben und unten.
- Glossarroute setzt DONOTCACHEPAGE + nocache_headers und trägt HDG_VERSION im HTML zur eindeutigen Deploy-Prüfung.
- Cyberduck-Paket: alle Dateien frisch datiert.
- Finales ZIP erneut entpackt und daraus gerendert: Start, Fertigen, J, Suche PASS.
- Datenbestand unverändert: 13 Batches, 308 Begriffe, 308 eindeutige IDs/Slugs.
- PHP-Lint 8/8 PASS; ZIP-Integrität PASS; Source/ZIP-Tree bytegleich.
- Artefakt: `HOBBY_DEPOT_GLOSSAR_CYBERDUCK_1.0.23_HOVER_HARDPASS.zip`
- SHA-256: `ba95a5a2919ae4fce30a209c99dac0c3acda19128bd9fd5caf2ab46024931991`


## 24.10.2026 – 1.0.23 Hover Glossar-Startseite
- Alle Links „Zur Glossar-Startseite“ erhalten einen sichtbaren Hover-/Focus-Effekt.
- Effekt: Petrol-Farbwechsel, Unterstreichung nimmt Akzentfarbe an, leichte 2px-Bewegung nach rechts.
- Keine sonstige Layout- oder Inhaltsänderung.
- Gerenderte Ausgabe geprüft: oberer und unterer Startseiten-Link vorhanden; Hover-/Focus-Regeln greifen.
- PHP-Lint PASS; finales ZIP erneut entpackt und bytegleich gegen Quelldatei geprüft.
- Artefakt: `HOBBY_DEPOT_GLOSSAR_CYBERDUCK_1.0.23_HOVER_HARDPASS.zip`
- SHA-256: `ba95a5a2919ae4fce30a209c99dac0c3acda19128bd9fd5caf2ab46024931991`
