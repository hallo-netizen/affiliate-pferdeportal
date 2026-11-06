# Nachtrag 06.11.2026: Beitragsdatum entfernen, einheitlicher Affiliate-Entwurf

## Ausführung auf Basis von Design 0.1.185
- Version 0.1.186: **HAB_UND_BEWAHR_DESIGN_0.1.186_OHNE_BEITRAGSDATUM.zip**
- SHA-256: `eed7d4cbda9758b4c287f4097e790bbcc36bdbaec60921a4c07d88f1689d6b37`
- 428 -> 429 ZIP-Dateien; 426/428 Originaldateien byteidentisch; zwei geändert, ein Yoast-Datumsmodul ergänzt.
- PHP-Syntax 35/35 bestanden, ZIP-CRC bestanden, isolierte Yoast-Filtertests bestanden.
- Sichtbare Datumszeile auf normalen Einzelbeiträgen entfernt, Kategorie ohne Datum belassen.
- Yoast Article/WebPage-schema datePublished/dateModified/dateCreated auf Einzelbeiträgen entfernt; Yoast Open-Graph-Zeitpresenter entfernt, canonical/andere SEO-Elemente behalten.
- Keine Kategorie-, Artikel-, Themen-, Partner-, WordPress- oder K0-Daten verändert. Kein neues Plugin.
- **Noch kein WordPress-Live-PASS**; Originaldatei 0.1.185 bleibt als Basis erhalten, 0.1.186 als Nutzer-Updatekandidat.
- Google kann ein Datum aus anderen Hinweisen weiterhin selbst erkennen; ein Google-Verbot ist unmöglich (Google Search Central).
- Beispiel-URL enthält noch `-muster-20261106/`; Slug/Weiterleitung bewusst NICHT ohne gesonderten Freigabe- und Redirectplan ändern.

## Beitragsdesign – Entwurf, keine Live-Behauptung
Eine universelle Vorlage: redaktionelles Titelbild, gemeinsame H1/H2/Tabellen/Listen/Merksatzgestaltung, auf Desktop seitlich passende Produktkarten, mobil als zusammenhängender Block; nach dem Vergleichsteil optional eine passende Produktgruppe, am Ende max. ein thematisch relevanter Banner. Produkt und Banner sind klar mit »Anzeige« markiert, die fachliche Bewertung ist unabhängig. Fehlende Produktdaten ergeben **keine sichtbaren Leerplätze**. Die Provideranbindung ist noch offen.

## Vorprüfung
Nicht wiederholen: falschen Renderer/CSS allein reparieren; das alte Plugin begrenzte den Beitragsrenderer auf `_hbdp_demo=1`. Dies wurde ab 0.1.185 auf reguläre Posts ausgedehnt. 0.1.186 korrigiert nur die Datumsdarstellung/Yoast-Datumsquelle. Plugin-Identität bleibt `hab-bewahr-design-vorschau`.

Das offiziell veröffentlichte Pluginbüro auf dem Campus darf nur nach positivem WordPress-Livetest auf die neue Version umgestellt werden; dieser isolierte Entwicklungsbranch ist **nicht** automatisch Live-Current.
