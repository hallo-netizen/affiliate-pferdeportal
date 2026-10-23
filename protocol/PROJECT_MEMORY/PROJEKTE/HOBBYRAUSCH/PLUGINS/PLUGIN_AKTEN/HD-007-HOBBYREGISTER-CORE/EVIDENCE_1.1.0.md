# HD-007 – EVIDENCE 1.1.0 HOBBYREGISTER FRONTEND PROTOTYP

STAND: 2026-10-23
STATUS: LOCAL HARD PASS / LIVE OFFEN

Artefakt:
`HOBBY_DEPOT_HOBBYREGISTER_CORE_HD007_V1.1.0_FULL_PROTOTYP.zip`

SHA-256:
`85c267e999bbb34b56c31003473b0f33fd8589a87dfa4d4fede98d2bca3e1ff0`

Größe:
926,146 Bytes.

Hauptordner:
`hd-hobbyregister-core/`

## Basis

Die vorhandene HD-007-1.0.0-Laufzeitprojektion wurde erweitert, nicht durch ein Parallelplugin ersetzt.

Unverändert:
- zentrale 54er Basis-JSON;
- Register-SHA `4deb4be2b235db450d58f02485ec40e780fc2671f9dfc6edf8cbbba0f738af78`;
- 862 Records;
- bestehende Read-only API;
- keine DB-Writes / Tabellen / Cron / Netzwerk.

Die fachliche Schema-1.2-Autorität bleibt in der Wissensdatenbank.
Für die zwei vollständigen Textproben sind die drei zusätzlichen Schema-1.2-Werte exakt aus der geprüften Evidence gebunden:
- Buchbinden: Wartung gering / Kraft 1 / Koordination 2;
- Slacklining: Wartung mittel / Kraft 3 / Koordination 5.

## Frontend

Virtuelle read-only Routen:
- `/hobbyregister/`
- `/hobbyregister/<hobby-slug>/`

Übersicht:
- Hero;
- Suche;
- A–Z;
- 8 Gruppen;
- 4-spaltige Karten;
- 16 Karten je Seite;
- Pagination.

Gruppenprojektion aus bestehender Welt + bestehenden Activity-Modes:
- Gestalten 372;
- Fertigen 387;
- Technik 50;
- Forschen 479;
- Pflanzen 48;
- Tiere 31;
- Bewegen 131;
- Sammeln 175;
- unzugeordnet 0.
Mehrfachzuordnungen sind bewusst erlaubt.

Detail:
- Hero;
- „Auf einen Blick“;
- Hobbygruppe;
- gleiche Gruppe;
- ähnliche Hobbys;
- Schema-F-Fließtext;
- Register-/Magazin-Links.

Volltextproben:
- Buchbinden: 8 Abschnitte / 657 Wörter;
- Slacklining: 8 Abschnitte / 670 Wörter.

Alle anderen 860 Profile bleiben im Prototyp bewusst kompakt, bis die zwei Text-/Designproben abgenommen sind.

## QA

- Core-ready: 862/862 PASS;
- Base-SHA unverändert PASS;
- 54 alte Basis-Traits je Record unverändert PASS;
- 862 eindeutige Profilslugs PASS;
- Gruppenabdeckung 862/862 PASS;
- Übersichtsrender 16 Karten + Pagination PASS;
- Buchbinden E2E HTML PASS;
- Slacklining E2E HTML PASS;
- beide: Hero / Bild / Fakten / 8 Textabschnitte / gleiche Gruppe / ähnliche Hobbys PASS;
- PHP-Lint 4/4 PASS;
- Pferde-/Rassenbegriffe im ausgelieferten Plugin: 0;
- Post-/Option-/SQL-Writes: 0;
- Cron: 0;
- Netzwerkpfade: 0.

## SEO-Prototypschutz

Virtuelle Detailprofile werden im Prototyp `noindex,follow` ausgegeben, bis die verbindliche CORE-vs-REGISTER-Owner-Matrix je Hobby vorliegt.
Das ist kein finaler Voll-noindex-Vertrag.
