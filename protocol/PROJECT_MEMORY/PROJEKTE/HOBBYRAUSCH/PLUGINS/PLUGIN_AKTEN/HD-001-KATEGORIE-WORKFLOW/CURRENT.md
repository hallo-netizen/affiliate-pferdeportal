# HD-001 – KATEGORIE-WORKFLOW – CURRENT

STAND: 2026-10-05
STATUS: BLOCKED – WORDPRESS-HIERARCHIEÜBERSETZUNG FALSCH / V1.9.7 VERWORFEN

## Livebestand

Livebestand unverändert lassen.

Beobachtet:
- `Buchbinden` sichtbar;
- vorgesehene Unterstruktur nicht als echte WordPress-Hierarchie sichtbar.

## Harte Ursache

Der Pilot übersetzt den Fachbaum derzeit so:

`Buchbinden [page] → Einstieg/Ausrüstung/Material/Techniken & Praxis [category]`

Der Sollbaum ist dagegen mindestens:

`Fertigen [page] → Buch & Papier [page] → Buchbinden [page] → Leaf-Kategorie → Beiträge`

Der Writer setzt einen nativen Parent nur bei gleichem technischen Ziel:
- page→page = nativ;
- category→category = nativ;
- hp_listing_category→hp_listing_category = nativ;
- page→category = **nicht nativ**, Term-Parent 0 + nur logische Meta-Bindung.

## Weitere harte Befunde

- Validator unterstützt Level 1..20.
- Concept Builder erzeugt trotzdem nur Root-Seite + maximal 4 direkte Kategorien.
- `MAX_CONTENT_CHILDREN_PER_TOPIC=4`.
- Zwei Hobbys mit jeweils sichtbarem Leaf `Einstieg` werden aktuell vom APKW-Validator global blockiert.
- Content und Magazin verwenden aktuell beide WordPress-`category`.
- HivePress Core konfiguriert Listing-Kategorien hierarchisch; produktiver Site-Readback der Taxonomie-Eigenschaft bleibt vor Nutzung tiefer Ebenen Pflicht.
- `Techniken & Praxis`: `&amp;` ist WordPress-Core-Speicherescaping, V1.9.4 Readback-Fix korrekt; kein aktueller Strukturblocker.

## V1.9.7

**NICHT INSTALLIEREN.**

Der Frontend-Linkblock wäre nur eine optische Reparatur auf einer nicht zielkonformen technischen Taxonomieübersetzung.

## ERSTER BLOCKER

`HD001_WORDPRESS_HIERARCHY_TRANSLATION_MISMATCH`

## NEXT ACTION

Kein weiterer Installer.

Zuerst den exakten WordPress-Übersetzungsvertrag für:
`SEITE → SEITE → SEITE → KATEGORIE → BEITRÄGE`
plus Magazin und HivePress lokal Positiv/Negativ bis Frontend beweisen.

Danach erst minimaler Codefix auf der bestehenden Pluginlinie.
