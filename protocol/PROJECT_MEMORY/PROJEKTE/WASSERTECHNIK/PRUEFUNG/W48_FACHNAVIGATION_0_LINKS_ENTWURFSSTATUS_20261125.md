# W48 – Fachnavigation vorhanden; unter acht Bereichen keine veröffentlichten Produktlinks

**25.11.2026 · echter zweiter WP-Admin-Screenshot geprüft · kein Pluginwechsel / keine DataForSEO-Kosten**

## Gesehener Iststand
- Vom Nutzer übermittelter Screenshot der echten WP-Adminseite **Wassertechnik Kategorie → Fachnavigation – Vorschau**, URL `/wp-admin/admin.php?page=wassertechnik-w32-navigation`.
- Originalbild unverändert in persönlicher Library archiviert unter `/Wassertechnik/Plugin-Büro/W48_FACHNAVIGATION_7_PLUS_FACHTECHNIK_0_LINKS_2026-11-25.png`.
- Die sieben Käufer-Hauptbereiche sind sichtbar, dazu **Fachtechnik** als getrennter Zugang. Oben stehen konzeptionell **79 bestehende Produktowner (71 Kaufprodukte, 8 Fachtechnik)**. Die Zahl ist eine reine Zählung des statischen W32-Plans, **keine** Zählung tatsächlich publizierter WordPress-Produktseiten.
- Unter **allen acht Menüpunkten** steht „Noch keine veröffentlichten Produktseiten“ beziehungsweise „Noch keine veröffentlichten Fachproduktseiten“. In dieser Vorschau sind **0 echte veröffentlichte Produktlinks**.
- Die bereits gesicherte W47 WordPress-Bestandsmeldung **390 von 390, fehlende Seiten/Kategorien/Anpassungen/Konflikte jeweils 0** ist nicht widersprüchlich: sie zählt sowohl veröffentlichte Seiten als auch **Entwürfe**.

## Ursachenprüfung mit vorhandenem Originalcode
Bestehenden, auf GitHub archivierten WT001-Importer `PLUGINS/QUELLCODE/W35_class-wassertechnik-import.php`, W44-Finalbau `PLUGINS/BUILD/W44_install_build.py` und Navigation `PLUGINS/QUELLCODE/W42_class-wassertechnik-navigation.php` überprüft:
1. Der W35-Bestandsabgleich verwendet `get_posts(post_status=any)` und akzeptiert deshalb sowohl publizierte als auch nicht publizierte Seiten. Ein vollständiger 390er Owner-Bestand belegt **nicht** die Veröffentlichung.
2. Der einzige W35-Importer legt **jede wirklich fehlende Produkt- und Struktur-Seite** mit `post_status=draft` an. Vorhandene Bestandsseiten werden bei Umordnung nicht automatisch veröffentlicht.
3. Die W42/W44-Navigation lädt dagegen ausschließlich `get_posts(post_status=publish)` und zeigt nur den zugehörigen `_wt_owner_id` mit passendem Pfad. Damit ist eine **leere Navigation erwartbar, wenn die 79 bisherigen Produktseiten Entwürfe sind**; sie schützt vor dem öffentlichen Verlinken leerer Placeholder-Seiten.
4. Ein alternativer Grund wäre, dass veröffentlichte Produktseiten nicht den erwarteten Besitzer-/Pfadbezug haben. W47 hat genau diesen Besitzer-/Pfadbezug für den Gesamtbestand erfolgreich geprüft, nicht aber den `post_status`. **Ohne direkten WordPress-Beleg für die Zahl tatsächlich veröffentlichter Seiten lässt sich die Entwurfsursache nicht als bewiesen melden.**
5. Der Hinweis in der W32-Vorschau, die 81 neu aufgenommenen Produkte seien noch „nicht WordPress-freigegeben“, stammt aus einer statischen Beschreibung. Er ist hinsichtlich bereits angelegter Entwürfe sprachlich veraltet; er bedeutet nicht, dass die 390er Zuordnungen fehlen. Kein Einzel-Plugin allein zur Textkorrektur ausgeben.

## Abnahmeentscheidung und nächster, gezielter Schritt
- **Kategorien- und Produkt-Struktur vollständig in WordPress vorhanden: W47 PASS, 390/390.** Sieben Hauptbereiche und separater Fachtechnik-Reiter werden gerendert: W48 PASS.
- **Sichtbare Produktlinks noch 0**: Frontend-/Publikationsreife **nicht** abgenommen. Nicht blind die 79 + 81 leeren Seiten veröffentlichen; keine unbefugte Massenpublikation.
- **Eine gezielte Bestandsfrage ohne Diagnoseplugin:** WP **Seiten → Alle Seiten** öffnen und die oben angezeigten Gesamtzahlen für **„Veröffentlicht“** und **„Entwurf“** prüfen. Liegen die 79 Bestandsproduktseiten als Entwürfe vor, ist das Schutzverhalten im Menü korrekt und die Veröffentlichung gehört in die spätere Inhalts-/Qualitätsfreigabe. Falls es veröffentlichte Besitzer-Produktseiten gibt und weiterhin 0 Menülinks, müsste anschließend **gezielt** die Pfad-/Owner-Zuordnung des konkreten veröffentlichten Produkts untersucht werden, statt pauschal neu zu importieren.
- Die ursprünglichen 17 Weiterleitungen dürfen nur für veröffentlichte Zielseiten aktiv sein; sie sind durch den Screenshot weiterhin **nicht** als HTTP-301-geprüft. Der öffentliche Webzugriff auf `wasser.oliver-beil.de` war aus dieser Umgebung nicht erreichbar, keine erfundenen Live-Zugriffe.
- **Keine erneute DataForSEO-Recherche**, 81/81 ist abgeschlossen (Kosten 0,13344 USD). **Kein W35-Neuimport**, 390/390 erreicht. **Keine neue Pluginversion**: aktuell installiert nutzerbestätigt WT001 **0.1.14 W44**, letzte geprüfte ZIP vollständig in `/Wassertechnik/Plugin-Büro/` erhalten; Vorgänger 0.1.13 bleibt archiviert.

**Fazit:** Kategoriekonzept als Struktur im WordPress-Bestand fertig. Publikations-/Navigationsfreigabe ist ein separater späterer Schritt, der nicht durch das Vorhandensein der Entwürfe ersetzt werden darf.
