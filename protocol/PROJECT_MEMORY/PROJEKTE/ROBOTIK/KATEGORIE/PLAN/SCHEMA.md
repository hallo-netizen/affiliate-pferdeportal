# PROFILFORMAT – LEERSTART

Die aktuelle **WP-ZIELVORLAGE** ist `robotik-empty.json` und bleibt bis zur Freigabe bei `nodes:[]`. Dies ist **KEINE zweite Produktliste**. Die einzige aktive Produktrecherchequelle ist `../RECHERCHE/PRODUKTE_V2_20261108.json`. Produktseiten werden später nur als freigegebener, zurückverfolgbarer Auszug daraus erzeugt.

Erst nach der Fachentscheidung erhält jeder Knoten:
- `id`: eindeutige, bleibende Robotik-ID (klein, z. B. `rk_...`);
- `pillar`: `core`, `editorial` oder `directory`;
- `kind`: `page`, `content_category`, `magazine_category` oder `listing_category`;
- `title`: sichtbarer, fachlich richtiger Name;
- `slug`: URL-Teil;
- `parent`: Eltern-ID oder `null` bei Hauptknoten.

`core/page`: WordPress-Seite.
`core/content_category`: unterste, flache Inhaltskategorie, braucht eine Elternseite.
`editorial/magazine_category`: Magazinrubrik.
`directory/listing_category`: HivePress-Anzeigenkategorie.

Die Plugin-Vorschau prüft die Rollen, Eltern, Zyklen, Dubletten im gleichen Zweig und Grundformat. Sie legt noch keine WordPress-Objekte an.

## Erweiterungen für die geprüfte Produkt-Hierarchie (Testkandidat 0.2.0)
- `phase`: `draft` oder `final` (Standard: `draft`).
- CORE-Seite `role=group` für übergeordnete WordPress-Seite oder `role=product` für letzte konkrete Produktseite.
- `content_category` direkt unter `role=product`; keine Kategorie unter `role=group`, keine neue Seite unter `role=product`.
- Für finale `content_category`: `topic_directions` mit mindestens drei unterschiedlichen GROBEN Stoffrichtungen; nicht die späteren Artikeltitel.
- Slugs für WordPress-Inhaltskategorien werden global eindeutig gebildet, zum Beispiel `servierroboter-kosten`, statt überall nur `kosten`.
- `role` gilt nur für CORE-Seiten, nicht Magazin-/Anzeigen-Kategorien oder Beitragskategorien.
- Die beiden übrigen Säulen bleiben getrennt; es gibt keine WordPress-Importfunktion.

**Wichtig:** `robotik-empty.json` mit `nodes:[]` bleibt der autoritative, unberührte Startplan; die Forschungsdaten in `RECHERCHE` werden NICHT automatisch eingefügt.

## Mindestpotenzial neuer Inhaltskategorien (09.11.2026)
- Kategorie gehört **fachlich direkt zu genau einer letzten Produkt-WP-Seite**, ist eine **flache WordPress-Inhaltskategorie**; WordPress-`category` ist technisch keine Seite und wird nicht als WP-Unterseite mit `post_parent` angelegt.
- Für `phase=final` sind **mindestens drei voneinander sachlich verschiedene realistische spätere Beitragsabsichten** erforderlich; das Plugin prüft in 0.3.0 nur die **formale Anzahl/Verschiedenheit**, nicht automatisch den fachlichen Gehalt.
- **3–5** sind eine sinnvolle Mindest-/Orientierungsgröße, **keine Obergrenze**. Bei nur **ein bis zwei** eigenständigen Beitragsthemen keine neue Kategorie, sondern die Information auf der Produktseite oder unter einer thematisch passenden schon vorhandenen Kategorie **desselben Robotertyps** behandeln.
- Namen wie Fragen, Kosten, Vergleich, Betrieb, Fehler sind **individuell zu prüfen**, nicht als identische Standardpalette überall anzulegen.
