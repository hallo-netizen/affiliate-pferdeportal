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
