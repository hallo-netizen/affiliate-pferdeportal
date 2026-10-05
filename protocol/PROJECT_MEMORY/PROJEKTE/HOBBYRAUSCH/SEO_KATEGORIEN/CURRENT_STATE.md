# HOBBYRAUSCH – SEO_KATEGORIEN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-05
STATUS: BLOCKED – WORDPRESS-HIERARCHIEÜBERSETZUNG NICHT ZIELKONFORM / V1.9.7 VERWORFEN

## Harte Abnahmeregel

Keine Abnahme ohne lokale Positiv- UND Negativsimulation bis zum echten WordPress-/Frontend-Endzustand.

Ein technischer Objekt-Readback oder ein optischer Linkblock ersetzt keine korrekte WordPress-Taxonomie-/Seitenhierarchie.

## Verbindlicher Zielvertrag

`ZIELVERTRAG_HD001_AUTOMATISCHE_SEO_HIERARCHIE_20261003.md`

Fachliches Ziel:
`SEITE → SEITE → SEITE → KATEGORIE → BEITRÄGE`
plus getrennte Magazin- und HivePress-Stränge.

## Reale Live-Wahrheit

- `Buchbinden` ist im Frontend sichtbar.
- Die vorgesehenen Unterkategorien sind dort nicht als echte untergeordnete Struktur sichtbar.
- Livebestand nicht verändern, bis die WordPress-Übersetzung hart geklärt ist.

## Harte technische Befunde

### 1. Der reale Buchbinden-Pilot bildet die Solltiefe nicht ab

Aktuelles Pilotpaket:
- `Buchbinden` = Level 1 = `wordpress_page`;
- `Einstieg`, `Ausrüstung`, `Material`, `Techniken & Praxis` = Level 2 = WordPress-`category`.

Die konzeptionellen oberen Seiten
`Fertigen → Buch & Papier`
fehlen im technisch erzeugten Baum.

### 2. WordPress-native Elternschaft bricht am Übergang Seite → Taxonomie

Der bestehende Writer kann nativ:
- Seite → Seite über `post_parent`;
- Term → Term nur innerhalb derselben Taxonomie über `parent`.

Bei Seite → Kategorie setzt der Writer den nativen Term-Parent auf 0 und speichert lediglich
`_apkw_parent_concept_id`.

Damit ist eine Kategorie technisch **kein nativer WordPress-Child der Seite**.

### 3. Der Writer kann Tiefe, der Builder nicht

Validator:
- Level 1..20 zulässig;
- Parent-Level wird hart geprüft.

Writer:
- Page→Page und Category→Category können hierarchisch geschrieben werden.

Concept Builder:
- erzeugt derzeit pro Seed nur eine Root-Seite auf Level 1;
- erzeugt maximal 4 direkte `category`-Kinder auf Level 2;
- `MAX_CONTENT_CHILDREN_PER_TOPIC=4`;
- erzeugt keine `Fertigen → Buch & Papier → Buchbinden`-Kette.

### 4. Wiederkehrende Leaf-Namen skalieren derzeit nicht

Harter lokaler Test mit zwei verschiedenen Hobbyseiten und jeweils Leaf `Einstieg`:
BLOCKED durch:
- `VISIBLE_NAME_DUPLICATE_GLOBAL`;
- `SLUG_DUPLICATE_WITHIN_BLOCK`;
- `PACKAGE_TARGET_SLUG_COLLISION`.

WordPress selbst erlaubt bei hierarchischen Taxonomien gleiche Child-Namen unter verschiedenen Eltern; der aktuelle APKW-Validator ist hier strenger als WordPress.

Da die aktuellen Hobby-Leafs wegen Seite→Kategorie aber native Root-Terme sind, fehlt ihnen genau der WordPress-Taxonomie-Parent, der diese Wiederholung sauber trennen könnte.

### 5. Content und Magazin teilen aktuell dieselbe WordPress-Taxonomie

Content-Leafs und Magazin-Knoten verwenden beide die Core-Taxonomie `category`.
Die Trennung existiert nur im APKW-`block`, nicht als getrennte WordPress-Taxonomie.

### 6. HivePress

HivePress definiert `listing_category` ausdrücklich hierarchisch; die reale Taxonomie ist `hp_listing_category`.
Native HivePress Term→Term-Tiefe ist damit technisch vorgesehen.

Vor einem produktiven Tiefenbaum muss auf Hobby Depot selbst zusätzlich `get_taxonomy('hp_listing_category')->hierarchical === true` real zurückgelesen werden.

### 7. Sonderzeichen / Darstellung

Der frühere Fehler bei `Techniken & Praxis` ist geklärt:
WordPress speichert den Namen intern escaped als `Techniken &amp; Praxis`.
V1.9.4 normalisiert dies beim Readback; im Browser wird korrekt `Techniken & Praxis` dargestellt.
Das ist **nicht** der aktuelle Strukturfehler.

## V1.9.7

V1.9.7 ist **NICHT FREIGEGEBEN / NICHT INSTALLIEREN**.

Der dortige Managed-Linkblock hätte die fehlende native WordPress-Hierarchie nur optisch überdeckt und löst weder:
- die Solltiefe,
- die Seite→Taxonomie-Grenze,
- wiederkehrende Leaf-Namen,
- noch die Content/Magazin-Taxonomie-Trennung.

## ERSTER BLOCKER

`HD001_WORDPRESS_HIERARCHY_TRANSLATION_MISMATCH`

## NEXT ACTION

Keine neue Pluginversion und kein Live-Write.

Als nächstes wird genau ein technischer WordPress-Übersetzungsvertrag für den fertigen Fachbaum festgelegt und lokal hart bewiesen:

1. wie `SEITE → SEITE → SEITE → KATEGORIE` technisch in WordPress abgebildet wird;
2. wie wiederkehrende Leaf-Namen wie `Einstieg` je Hobby konfliktfrei funktionieren;
3. wie Content-Kategorien und Magazin technisch sauber getrennt bleiben;
4. wie HivePress separat hierarchisch bleibt;
5. wie diese Struktur im Frontend ohne Theme-Trick sichtbar wird;
6. wie spätere Deltas ohne Gesamtumbau ergänzt werden.

Erst nach Positiv-/Negativ-E2E dieser Übersetzung darf ein neuer Kandidat gebaut werden.
