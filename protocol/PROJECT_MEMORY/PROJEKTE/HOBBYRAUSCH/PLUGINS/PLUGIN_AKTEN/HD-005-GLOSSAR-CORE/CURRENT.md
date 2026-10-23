# HD-005 – HOBBY DEPOT GLOSSAR CORE – CURRENT

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-23
STATUS: **1.0.14 / 100 BEGRIFFE PRODUKTION HARD PASS / LIVE OFFEN**

Plugin-ID:
`HD-005-GLOSSAR-CORE`

Aktueller Hobby-Depot-Kandidat:
`HOBBY_DEPOT_GLOSSAR_CORE_1.0.14_100_BEGRIFFE_PRODUKTION_HARDPASS.zip`

SHA-256:
`4b998db76541e4654c0ec227b9efb9a28acfb231c8fe769cf4518f94a48eba39`

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

**1.0.14 über den bestehenden Ordner `hobby-depot-glossar` hochladen/überschreiben und WordPress-Admin einmal öffnen, damit die 100 Entwürfe angelegt bzw. aktualisiert werden.**
