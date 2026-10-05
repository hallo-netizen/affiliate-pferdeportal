# Affiliate Router 6.72.186 – Strict Best Banner Tier – Red/Green Full E2E

Datum: 2026-10-05
Branch: affiliate-672186-strict-tier
Version: 6.72.186
Release: NICHT freigegeben; realer WordPress-Readback offen.

## Vertrag

Für jeden Bannerplatz gilt genau eine fachliche Hierarchie:

1. exakter Treffer,
2. erweiterter Themenkreis,
3. allgemeiner Pferde-/Shop-Fallback,
4. technisch gültiger letzter Fallback.

Zuerst wird die höchste vorhandene Stufe bestimmt. Erst danach darf verteilt werden.
Schwächere Stufen sind nicht ausgabefähig, solange mindestens ein Kandidat der besseren Stufe vorhanden ist.

- Ein einziger bester Banner bleibt fix.
- Mehrere Banner derselben besten Stufe dürfen nur untereinander rotieren.
- Eine eindeutige gespeicherte Zielkante gilt auf allen Ebenen und Beitragsarten, einschließlich Pferderassen.
- Manuelle FIXED-Zuweisungen bleiben separat.
- Keine neue Frontend-DB-Abfrage, kein HTTP, keine URL-Neuklassifikation.

## Negativbeweis 6.72.185

Exakter Ausgangsinstaller:
`AFFILIATE_ZENTRALE_6.72.185.zip`
SHA-256:
`13fff3d67507d152e5368da9d7fc99028f8d26ad6d19338bb0cad1f44463fa28`

Fokussierter WordPress/MariaDB-Run:
`37293474957`

Fall: ein exakter Reithelm-Banner plus mehrere allgemeine Banner.

Ergebnis auf 6.72.185:
- Position 1 = exact: PASS.
- Position 2 = general: FAIL.
- Allgemeiner Banner dringt trotz vorhandenem exact in die Auslieferung ein: FAIL.
- Mehrere exact-Banner rotieren dagegen bereits korrekt innerhalb exact.
- Frontend HTTP: 0.

All-Context-Negativrun:
`37293850326`

Der gleiche lower-tier escape wurde auf den aktiven Inhaltsfamilien reproduziert:
Startseite, Hub, Kategorie/Produktseite, Kategoriearchiv, klassischer Beitrag, Journal, Anzeigenmarkt/HivePress, Glossar und Rassen-Übersicht.
Bei Rassen-Einzelartikeln konnte die historische neutrale Rassenregel sogar einen vorhandenen exact-Treffer vor Position 1 neutralisieren.

## Root Cause

Die bestehende Bannerverteilung ordnete die stärkste Relevanzstufe zwar zuerst, ließ aber schwächere Kandidaten in derselben Ergebnisliste.
`select_campaign_for_slot_position()` versuchte für eine zweite Position zwingend einen anderen Banner zu finden.
Bei nur einem exact-Banner nahm es deshalb den nächsten schwächeren Banner aus general/technical.

Zusätzlich lag die historische themenneutrale Rassenregel in `campaign_match_rank()` vor der Auswertung einer bereits gespeicherten exakten Zielkante.

## KISS-Fix 6.72.186

1. Neue zentrale In-Memory-Funktion `banner_strict_best_relevance_tier_v672186()`.
   Sie erhält die bereits gerankte Kandidatenliste und behält ausschließlich die beste vorhandene Relevanzstufe.

2. `ranked_campaigns_for_slot()` liefert für Banner nur noch diese beste Stufe weiter.

3. `select_campaign_for_slot_position()`:
   Gibt es nur einen Kandidaten in der besten Stufe, bleibt dieser auch an einer weiteren Bannerposition derselbe, statt in eine schwächere Stufe zu fallen.
   Bei mehreren Kandidaten bleibt die bestehende Rotation innerhalb der besten Stufe aktiv.

4. Pferderassen:
   Gespeicherte exact-Zielkante wird vor der neutralen Rassenfallbackregel geprüft.
   Nur ohne exact greift die bestehende neutrale Rassenverteilung.

Nicht geändert:
- `banner_distribution_reorder_candidates`,
- `banner_distribution_stable_index`,
- `render_banner`,
- geschützte Performance-Hotpaths,
- Providerlogik,
- eBay/Idealo-Produktpfade,
- Creative-Library-Ziel-URL-Klassifikation,
- Datenbank-/Migrationsarchitektur.

## Source-Positivbeweis

Run:
`37295037827`

WordPress 7.1.2 + MariaDB.

Universaltest:
- 16 reale Inhalts-/Slotfamilien,
- pro Familie ein exact + general: exact bleibt Position 1 UND Position 2,
- pro Familie zwei exact + general: Rotation nur zwischen den zwei exact,
- Hierarchie exact > broad > general > technical auf allen aktiven Produktions-Bannerslots.

Ergebnis:
`139/139 PASS`
`0 Frontend-HTTP`

Bestehende Regressionen auf frischer Datenbank:
- Banner-Gesamttest: 21/21 PASS.
- Ziel-URL-Library: 26/26 PASS.
- Performance-Hardlock: PASS.

## Exakter ZIP-Red/Green-Beweis

Run:
`37295977106`

Ablauf:
1. Exakten bisherigen 6.72.185-Installer mit SHA `13fff3d...` installieren.
2. Fokussierten Rotfall auf dieser echten Version reproduzieren:
   Position 1 exact, Position 2 general.
3. Dieselbe WordPress-Installation auf die im Lauf gebaute 6.72.186-ZIP aktualisieren.
4. Universaltest erneut ausführen.

Ergebnis nach Upgrade:
- strict best tier: 139/139 PASS.
- Frontend HTTP: 0.
- Fresh-ZIP Banner-Gesamttest: 21/21 PASS.
- Fresh-ZIP Ziel-URL-Library: 26/26 PASS.
- ZIP/Source Manifestidentität: 27/27 PASS.
- PHP lint: 21/21 PASS.
- Performance-Hardlock: PASS.

## Getesteter Installer

Pfad:
`release/affiliate-zentrale/artifacts/final/AFFILIATE_ZENTRALE_6.72.186.zip`

SHA-256:
`1ca526ce92f339c678f2dc6e8775eae31355414668b8e06ed4afd561d5c15cae`

Bytes:
`793558`

Git blob:
`d6b019c7cc6680136b54aca8ed728f8ebffa200c`

Source-Manifest SHA-256:
`5042a415b825bebd3a5059d0994c89a61002448cfa0ff80ee4b1f6f645286cea`

Source-Dateien:
27.

## Performance

Geschützte Funktionen bleiben gegenüber Baseline
`a381aff4eb3f41754186f4bad86ce1a7e0823a29`
körperidentisch.

Der neue Strict-Tier-Pfad arbeitet ausschließlich auf der bereits im Speicher vorhandenen Kandidatenliste:
- keine neue DB-Abfrage,
- kein `get_post_meta`,
- kein `get_posts`,
- kein `get_option`,
- kein `wp_remote_*`,
- kein `output_plan_creative`,
- keine Frontend-Ziel-URL-Neuklassifikation.

## Status

Source und exakte installierbare ZIP sind Red -> Green vollständig bewiesen.

`release_allowed=false`

Offen ist ausschließlich der reale Produktionsnachweis:
6.72.186 über die vorhandene 6.72.185 installieren und danach mindestens Reithelme und Schabracken frisch prüfen.
Bei Reithelme darf bei vorhandenem exakten Reithelm-Banner kein allgemeiner SanoVet-/Guardian-/sonstiger Fallback gewinnen.
Wenn nur ein exact existiert, muss er stabil bleiben; bei mehreren exact darf nur innerhalb dieser exact-Gruppe gewechselt werden.
