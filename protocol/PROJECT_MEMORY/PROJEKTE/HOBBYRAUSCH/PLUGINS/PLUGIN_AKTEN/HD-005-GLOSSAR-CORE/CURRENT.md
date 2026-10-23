# HD-005 – HOBBY DEPOT GLOSSAR CORE – CURRENT

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-23
STATUS: **1.0.15 / IMPORTFIX / 100 BEGRIFFE HARD PASS / LIVE OFFEN**

Plugin-ID:
`HD-005-GLOSSAR-CORE`

Aktueller Hobby-Depot-Kandidat:
`HOBBY_DEPOT_GLOSSAR_CORE_1.0.15_IMPORTFIX_100_BEGRIFFE_HARDPASS.zip`

SHA-256:
`48f20672cff3d01cb5866469475d773e91602ad3ae2656ef4be1155efc0dd8da`

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
