# PROFILFORMAT – LEERSTART

Die aktive Vorlage ist `robotik-empty.json`. Solange das Konzept offen ist, bleibt `nodes` leer.

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
