
# HD009 0.1.35 – Korrektur Produktrelevanz Airbrush

Datum: 13.11.2026. Original HD009 0.1.34 (inklusive 2901-Vergleich) erhalten,
nur zwei bestehende Plugin-Dateien verändert. Keine Änderung an Design, eBay,
Amazon/DataForSEO, den Feed-Daten, Materialisierung oder vorhandenen Produktkarten.

Livebeweis: Airbrush-Seite enthielt als echte Idealo-Produkte zwei Kleidungsstücke
mit Modelnamen Malene sowie Cotton Batik. Die alte Wortverkürzung machte
aus Malene das Wort Malen. Außerdem durften konkrete Idealo-Artikel über
Eltern-Hobbyseiten auf unpassende Unterseiten vererbt werden.
Quelle: https://github.com/hallo-netizen/affiliate-pferdeportal/actions/runs/43399503056

Ursachenlösung: Idealo-Produktkarten in den drei Kategorie-Slots einer
WordPress-Hobbyseite erfordern nun den exakten Zielschlüssel der aktuellen
Hobbyseite. Nur Eltern-Hobby-Ziele reichen nicht mehr. Die Morphologie vermeidet
außerdem falsches Malene->Malen, lässt Teleskope->Teleskop unverändert.
Amazon, eBay, Artikel, Banner, bestehende Idealo-Feedprüfungen bleiben unangetastet.

Harte QA: 41/41 ZIP-CRC, 24/24 PHP-Syntax, 12 PHP-Lauftests für echte
Klassenauszüge einschließlich Negativbeispiele.
https://github.com/hallo-netizen/affiliate-pferdeportal/actions/runs/43400956434

Nicht live installiert oder im geänderten Frontend abgenommen.
Vorhandene unpassende Kampagnen bleiben in WordPress gespeichert,
erscheinen aber nicht mehr auf unpassenden Hobby-Unterseiten.
Bei fehlenden exakten Treffern bleibt der Slot leer.

Vollinstaller:
https://github.com/hallo-netizen/affiliate-pferdeportal/releases/download/hobby-hd009-0.1.35-airbrush-relevance-20261113/HOBBY_DEPOT_HD009_0.1.35_THEMATIC_PRODUCT_CARDS.zip

SHA-256: c30b3381928454671a8784f99c6bd59aaec79c800b9d38925462fc9dd29fe246
