# HOBBYRAUSCH – WISSENSDATENBANK – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-23
STATUS: **HOBBYREGISTER 862/862 / SCHEMA 1.2 MIT 57 TRAITS VOLLSTÄNDIG GEBUNDEN / 862 SCHEMA-F-TEXTE LOCAL HARD PASS**

## Rolle

Einzige aktuelle Zustandsautorität des Scopes `HOBBYRAUSCH_WISSENSDATENBANK`.

Fester Registervertrag:
`HOBBYREGISTER.md`

Eigenschaftsvertrag:
`HOBBY_EIGENSCHAFTEN_SCHEMA_1_2_DELTA.md`

Register-Seitenvertrag:
`HOBBYREGISTER_SCHEMA_F_V1.md`

Textvertrag:
`HOBBYREGISTER_TEXTREGELN_V1.md`

Design-/Referenztransfer:
`HOBBYREGISTER_REFERENZTRANSFER_V1.md`

## Zentraler Hobbybestand

- **862** kanonische Hobbyidentitäten;
- **57** Eigenschaften in 8 Gruppen;
- **862/862** Hobbys mit **57/57** klassifizierten Traits;
- **862/862** Hobbys mit **4/4** Kurzprofilfeldern;
- Aliasnamen erzeugen keine zweite Hobbyidentität.

## Schema 1.2

Neu:
- `equipment_maintenance`;
- `strength_need`;
- `coordination_balance_need`.

Audit:
- 2.586/2.586 neue Einzelwerte;
- 46.548 alte Traitwerte unverändert;
- 0 ungültige neue Werte;
- 0 UNKNOWN bei neuen Traits.

Basis-54-SHA:
`4deb4be2b235db450d58f02485ec40e780fc2671f9dfc6edf8cbbba0f738af78`

HD-007-1.2.0-Runtime-SHA:
`d0d424485e6dbcf65a8332da732d2e342b279f0a1311919149ba8dfcdb93604a`

## Schema-F-Produktion 2026-10-23

HD-007 1.2.0 bindet nun die vollständige 57er Laufzeitprojektion.

Texte:
- 862/862 statisch eingefroren;
- exakt 8 Abschnitte je Hobby;
- 57/57 Trait-IDs im Produktionsgenerator berücksichtigt;
- Wortumfang 656–761 Wörter;
- keine Kurzprofil-Fallbacks.

## Bilder

Zentraler Bildplan:
`/Hobby Depot/Hobby-Klassifikation/HOBBY_PORTRAIT_BILDPLAN_V1.json`

Aktuelle Runtime-Darstellung:
- 862/862 Profile haben eine Bildzuordnung;
- 328 exakt kuratierte vorhandene Hobby-/CORE-Fotos;
- 534 fachlich passende vorhandene Themen-Masterbilder.

Die Themen-Masterbilder ersetzen nicht die im Bildplan vorgesehenen dedizierten neuen Portraitmaster.

## SEO

Die SEO-Owner-Regel bleibt:
- dedizierte gleichartige CORE-Seite gewinnt;
- ohne entsprechende CORE-Seite darf das Registerprofil SEO-Owner werden;
- Owner-Matrix 862/862 bleibt noch offen;
- bis dahin Prototypschutz noindex,follow.

## EXAKT EINE NEXT ACTION

**HD-007 1.2.0 live abnehmen. Danach die 862er CORE-vs-REGISTER-Owner-Matrix erstellen und separat entscheiden, welche der im Bildplan vorgesehenen dedizierten Portraitmaster noch neu erzeugt werden.**
