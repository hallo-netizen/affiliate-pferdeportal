# HOBBYRAUSCH – WISSENSDATENBANK – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-23
STATUS: **HOBBYREGISTER 862/862 / SCHEMA 1.2 MIT 57 TRAITS / 862 STATISCHE TEXTE VOLLSTÄNDIG**

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

## Zentraler Hobbybestand

- **862** kanonische Hobbyidentitäten;
- **57** Eigenschaften in 8 Gruppen;
- **862/862** Hobbys mit **57/57** klassifizierten Traits;
- **862/862** Hobbys mit statischen Registerartikeln;
- exakt **8 Abschnitte je Hobby**;
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

## Texte

- 862/862 statisch eingefroren;
- exakt 8 Abschnitte je Hobby;
- 57/57 Trait-IDs im Produktionsgenerator berücksichtigt;
- Wortumfang 656–761 Wörter;
- keine Kurzprofil-Fallbacks.

## Bilder – Fachgrenze

Der technische Bildproduktions-/Auditstatus wird **nicht** hier als zweite Current-Wahrheit geführt.

Aktuelle technische Autorität:
`../PLUGINS/PLUGIN_AKTEN/HD-007-HOBBYREGISTER-CORE/CURRENT.md`

Fachlich verbindlich bleibt:
- ein kanonisches Hobby je Register-ID;
- genau ein finales Masterbild pro Hobby;
- dasselbe Masterbild für Hero + Beitrag;
- kein Hochskalieren ungeeigneter Quellen;
- Dubletten/Fehlversuche zählen nicht als final.

## SEO

Die SEO-Owner-Regel bleibt:
- dedizierte gleichartige CORE-Seite gewinnt;
- ohne entsprechende CORE-Seite darf das Registerprofil SEO-Owner werden;
- Owner-Matrix 862/862 bleibt offen;
- bis dahin Prototypschutz noindex,follow.

## EXAKT EINE NEXT ACTION

**Wenn die fachliche Registerarbeit wieder aufgenommen wird: die 862er CORE-vs-REGISTER-Owner-Matrix erstellen. Technische Plugin-/Bildaktionen ausschließlich über die HD-007-Current führen.**
