# SICHERHEITSGLOSSAR – VERBINDLICHER DATEN- UND TEXTVERTRAG
Fachmodell gespiegelt aus `protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/WISSENSDATENBANK/AKTENSCHRAENKE/GLOSSAR/GLOSSAR_STRUKTUR.md`, aber eigenständige Sicherheitswelten.

## Datensatz
`external_id` (stabil: `term-...`), `begriff`, `slug`, `synonyme[]`, `kurzdefinition`, `facherklaerung`, `abgrenzung`, `verwandte_begriffe[]`, `verwandte_slugs[]`, `themenwelt`, `quellen[]` mit URL/Beleg/Organisation/Trust, `recherche_status`, `last_verified_at`, `review_interval_months`, `seo_title`, `seo_description`, optional `primary_target` ({type:`page`|`category`, wp_id: tatsächliche Integer-ID}). Für Weiterverarbeitung `contract_version: HB_GLOSSARY_BATCH_V1`.

## Sechs primäre Schutzwelten
`einbruch` – Einbruch & Diebstahl;
`vandalismus` – Vandalismus & Zerstörung;
`wasser` – Wasser & Feuchtigkeit;
`feuer` – Feuer & Gase;
`wetter` – Wetter & Natur;
`technik` – Technik & Ausfälle.
Querschnittsbegriffe genau einer primären Welt zuordnen, mehrere im Text/relationen.

## Glossar oder Artikel?
Glossar = Begriff selbst verständlich machen. Portalhub = breites Themengebiet. Ratgeber = konkrete Handlung, Anleitung oder Vergleich. Keine 1:1-Kopie der Kategorien/Artikel im Glossar.

## WordPress und SEO
- `GEPRUEFT` erst nach 150–200 eigenen, belegten Wörtern, Abgrenzung, mindestens einem Related, Quellen, SEO-Feldern.
- **0 Bodylinks** innerhalb der Fachtextabsätze; UI-Querverweise separat.
- Quelle+Prüfdatum im Forschungsdatensatz, nicht blind unverständliche Normzusicherungen veröffentlichen.
- `primary_target` nur starke existierende Seite, vorzugsweise obere Affiliate-/Schutzwelt-Kategorie vor Magazin; wenn kein ehrliches Ziel: leer.
- WordPress schreibt höchstens Draft, maximal 25 Neue je Batch; validator vor und Readback nach jedem Batch; Mismatch → komplette Batch-Rücknahme.
- Synonyme: nur eine kanonische Term-ID/URL; keine 100 dünnen Seiten aus den Short-Defs 0.1.7.
- Zyklus `last_verified_at + review_interval_months` mit 6/12/24; fällig = Prüfbedarf, nie Autopublish.
