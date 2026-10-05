# HOBBYRAUSCH – SEO_KATEGORIEN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-05
STATUS: V1.9.8 WORDPRESS-HIERARCHIEÜBERSETZUNG LOKAL HARD PASS / KEIN INSTALLER / BUILDER NOCH BLOCKER

## Harte Abnahmeregel

Keine Live-Abnahme ohne vollständige lokale Positiv-/Negativ-E2E-Simulation bis zum sichtbaren Frontend-Endzustand und danach realen WordPress-/Frontend-Readback.

## Zielvertrag

`ZIELVERTRAG_HD001_AUTOMATISCHE_SEO_HIERARCHIE_20261003.md`

## Livebestand

Live unverändert lassen.
Aktuell real beobachtet:
- `Buchbinden` sichtbar;
- bisherige vier Content-Unterkategorien auf der Seite nicht sichtbar.

V1.9.7 bleibt verworfen und darf nicht installiert werden.

## V1.9.8 lokaler Hierarchie-Prototyp

Basis:
exakte V1.9.6-Arbeitsbasis, keine neue Pluginlinie.

### Bewiesene WordPress-Übersetzung

Fachbaum:
`SEITE → SEITE → SEITE → KATEGORIE → BEITRÄGE`

Technisch:
- Page→Page bleibt native WordPress-`post_parent`-Hierarchie;
- Page→Taxonomy erhält pro Page/Taxonomie-Grenze einen internen technischen Bridge-Term;
- sichtbare Leaf-Terme hängen nativ unter diesem Bridge-Term;
- die logische `parent_concept_id`-Bindung an die Seite bleibt zusätzlich erhalten;
- der technische Bridge wird im Frontend niemals als sichtbarer Navigationspunkt ausgegeben;
- Frontend rendert direkte veröffentlichte Page-Kinder und direkte native Leaf-Kinder des Bridge-Terms;
- dieser sichtbare Endzustand ist Bestandteil des Deployment-Readbacks.

### Wiederholbare Leaf-Namen

Kurze sichtbare Leafs wie `Einstieg` dürfen unter verschiedenen Hobby-Seiten erneut vorkommen, wenn:
- die Page-Kontexte verschieden sind;
- die technischen Slugs verschieden sind;
- Primärkeyword/Intent-Owner verschieden bleiben.

Gleicher sichtbarer Leaf unter demselben Page-Parent bleibt BLOCKED.
Technische Slug-Kollision bleibt BLOCKED.

### Magazin

`journal_cat` wird in derselben Pluginlinie bei Bedarf als eigene öffentliche, hierarchische Taxonomie registriert.
Kein stilles Remap auf Content-`category`.

### HivePress

`hp_listing_category` bleibt eigener nativer hierarchischer Strang.
Content-Frontend darf weder Magazin- noch HivePress-Knoten anzeigen.

## Harte lokale Evidenz

Gesamtsuite aktuell:
- 270/270 PASS;
- bestehende Regression bleibt grün.

Exakter Zielprojektions-Test:
- `Fertigen → Buch & Papier → Buchbinden` als native 3-Seiten-Kette PASS;
- `Buchbinden → Einstieg/Ausrüstung/Material/Techniken & Praxis` über nativen Taxonomie-Bridge PASS;
- zweiter Strang `Fertigen → Textil → Nähen → Einstieg` PASS;
- kein Cross-Hobby-Leak;
- technische Bridges unsichtbar;
- Magazin/HivePress getrennt;
- Bridge-Tamper BLOCKED.

Realer Buchbinden-Migrationstest auf Basis der echten Datei
`HOBBY_DEPOT_BUCHBINDEN_READ_ONLY_PREVIEW_V1.json`:
- alter Zustand exakt reproduziert: Buchbinden-Seite sichtbar, Leafs nicht sichtbar;
- exakt 1 Content-Bridge erforderlich;
- bestehende 4 Content-Term-IDs bleiben erhalten;
- alle 4 werden ohne Neu-ID unter den Bridge verschoben;
- Frontend danach PASS mit:
  - Einstieg
  - Ausrüstung
  - Material
  - Techniken & Praxis
- `Buchbinden Set` leakt nicht;
- `Buchbinden Online` leakt nicht;
- technischer Bridge leakt nicht;
- `&` wird korrekt HTML-escaped und browserseitig als `&` dargestellt.

## ERSTER OFFENER BLOCKER

`HD001_CONCEPT_BUILDER_FULL_HIERARCHY_NOT_YET_RESOLVED`

Der alte Concept Builder enthält weiterhin:
- `MAX_CONTENT_CHILDREN_PER_TOPIC=4`;
- pro Seed nur eine Root-Seite;
- danach direkte Kategorie-Kinder;
- keine variable Page→Page→Page-Kette.

Die Writer-/WordPress-Übersetzung ist damit lokal geklärt; der Builder erzeugt den vollständigen Zielbaum aber noch nicht automatisch.

## NEXT ACTION

Kein Installer und kein Live-Write.

Als nächstes den bestehenden Concept Builder minimal auf den bereits bewiesenen WordPress-Zielvertrag umstellen:
- variable 1–3 Page-Ebenen;
- keine feste Root+4-Grenze;
- DataForSEO-Evidenz/Intent-Ownership bleibt autoritativ;
- Content + Magazin + HivePress gemeinsam;
- danach kompletter lokaler DataForSEO→Builder→Research→Deploy→Frontend-Readback Positiv-/Negativlauf.

Erst danach neuer installierbarer Kandidat.
