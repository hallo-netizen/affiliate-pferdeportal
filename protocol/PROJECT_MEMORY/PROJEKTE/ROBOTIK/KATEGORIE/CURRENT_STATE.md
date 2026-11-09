# ROBOTIK / KATEGORIE – EINZIGER AKTUELLER STATUS
Stand: 09.11.2026

## Verbindlicher Fachstand
- **Eine Forschungsquelle**: `RECHERCHE/PRODUKTE_V2_20261108.json` (68 noch ungeprüfte Produktkandidaten, Revision 3). Die alte 27er-Liste nur Archiv; 17 identische Namen und 10 offene Begriffskonflikte sind nachverfolgt.
- **Ein WordPress-Zielplan**: `PLAN/robotik-empty.json`; noch 0 freigegebene Knoten.
- CORE: WP-Seite → weitere Seiten → letzte Seite = konkreter Robotertyp → dessen flache WP-Kategorien → Beiträge. Daneben getrennte Säulen Magazin und HivePress. Keine doppelten Such-Owner.
- Vorgehen gemäß `ARBEITSABLAUF.md`: automatische Bestandsaufnahme statt tausender Dateien, ein Gesamtbericht, fachliche Forschung/Keywords, kontrollierter späterer Dry-run, Freigabe und echter Frontend-Readback.

## Einzige aktuelle Plugin-Datei
- **Kategorieplugin 0.3.0**: `PLUGIN/CURRENT.zip` (identisch zu `PLUGIN/VERSIONEN/0.3.0.zip`). Unveränderte WordPress-Pluginidentität `robotik-kategorie-workflow`.
- **Installationsstatus:** Nutzer hat am 09.11.2026 ausdrücklich **„installiert“** zurückgemeldet. Damit ist die Installation berichtet, aber **nicht unabhängig im WordPress-Backend ausgelesen oder live abgenommen**.
- Lokaler Dateinachweis vom 09.11.: ZIP-CRC PASS; PHP-Lint für beide PHP-Dateien PASS; exakt 5 ZIP-Einträge (zwei Verzeichnisse, zwei PHP-Dateien, README), 7.926 Byte; SHA256 `3c31aaaf86379a054034a80c8aeb3eaebdf616baa953ac079793f6495f1ecd30`.
- GitHub-ZIP ist **byteidentisch** zum geprüften bereitgestellten 0.3.0-Installer (Git-Blob `3f7240d09c07a650083ed6d603c290aa06171e4d`).
- 0.3.0 **kann**: JSON-Entwurf formal prüfen, einen WordPress-Bestandscheck auf Admin-Klick auslösen (Seiten, Beiträge, WP-Kategorien; HivePress nur wenn installiert) und **einen** Gesamtbericht exportieren. Keine eigentliche Import-/Änderungsroutine für Seiten, Beiträge und Kategorien.
- **Nicht angebunden:** GitHub-Fachmaster-Revision, DataForSEO, semantische Vollprüfung/Contentqualität, echte Werbe-/Affiliate-Slots und bestätigte Magazin-Zuordnung. Fehlende Schnittstelle darf nicht als geprüfter PASS erscheinen.
- **Abnahmegrad:** ZIP und PHP **LOKAL PASS**; WordPress-Version **INSTALLIERT LAUT NUTZER**; tatsächlicher Backend-Bestandsscan und Export sowie Frontend-/HivePress-Wirkung **LIVE OFFEN**.

## Nächste konkrete Handlung (ohne Einzeldateien)
1. **WordPress → Robotik Kategorie → Bestand prüfen.** Dort Bericht und ggf. Anzeige `NICHT ANGEBUNDEN` prüfen.
2. Wenn der Bericht erscheint: **EINEN Gesamtbericht (JSON) herunterladen**; bei Bedarf genau diese EINE Datei für den fachlichen Abgleich bereitstellen.
3. Vor der nächsten Plugin-Version den echten WordPress-Befund dokumentieren; anschließend GitHub-Master-Revisionsabgleich als read-only Funktion in **dieselbe Pluginidentität** einbauen. Keine fremden Profile, keine automatische Paid-API, keine WordPress-Schreibvorgänge.
4. Für jeden weiteren Plugin-Release zuerst Version/Prüfung in `PLUGIN/RELEASE_PROTOKOLL.md` dokumentieren und ZIP in `PLUGIN/VERSIONEN/` archivieren; `PLUGIN/CURRENT.zip` **nur bewusst** auf die neueste als installiert gemeldete oder explizit freigegebene Version ändern. Keine zweite Current-/Protokollwahrheit.

**Andere Portalgebäude und bestehende Kategorien/Beiträge werden bei dieser Archivierung nicht geändert.**

## 09.11.2026 – echter WordPress-Bestandsscan mit 0.3.0
Nutzer hat den tatsächlichen **Gesamtbericht der installierten 0.3.0** hochgeladen (09.11.2026, 15:29 UTC). Verifiziert gegen den JSON-Bericht:
- WordPress-Seiten: 2 (Beispielseite veröffentlicht; Datenschutzerklärung Entwurf).
- Beiträge: 1 („Hallo Welt!“); WordPress-Kategorien: 1 („Allgemein“).
- HivePress-Listingkategorien und Inserate: **NOT_CONFIGURED** – kein Fehler, aber auch kein fachlicher PASS.
- Magazin-Taxonomie: **NOT_MAPPED**. Affiliate/Anzeigen: **NOT_CONNECTED**. Forschungs-Master: **NOT_CONNECTED**. Keywordrecherche: **NOT_CONNECTED**. Frontend-Navigation: **NOT_CHECKED**.
- Bericht meldet 0 formale Issues; nur WordPress-Inventar gelesen, **keine semantische/inhaltsbezogene Prüfung**.

**ENTSCHEIDUNG:** Nutzer nicht erneut um denselben Bericht bitten. Die Bestandsaufnahme auf einer praktisch leeren WordPress-Site war für die Kategorienermittlung kein sinnvoller Hauptschritt; sie hat nur die Funktion der 0.3.0-Inventarisierung nachgewiesen. Es sind noch **0 echte Robotik-Kategorien und -Produktseiten** vorhanden. Nächster Arbeitsschritt ohne Benutzeraufwand: den einen GitHub-Produktmaster (68 Kandidaten, Revision 3) in derselben Robotik-Pluginidentität **read-only und revisionsgeprüft** anbinden, danach Fach-/Keyword- und Drei-Säulen-Prüfung. Kein neuer Ist-Bericht nötig, bevor WordPress tatsächliche Robotik-Inhalte hat.

## 09.11.2026 – Erweiterte Kategorieforschung, 3 Säulen, Glossar/Finder/Register
- Einziger Fachmaster `RECHERCHE/PRODUKTE_V2_20261108.json` auf **Revision 4** erweitert (die Datei heißt aus Kontinuität weiterhin V2_20261108, maßgeblich ist das Revisionsfeld). **68/68** Ausgangskandidaten je einem vorläufigen CORE-Parent-/Welt-Pfad zugeordnet, **37** fachliche Abgrenzungsfragen dokumentiert, **20** neue Randkandidaten in **derselben Masterdatei**. Alles **UNAPPROVED**, keine deutsche SEO-Volumenmessung, keine WordPress-Schreibung.
- `RECHERCHE/KATEGORIEKONZEPT_V1_20261109.md`: zehn vorläufige Hauptwelten, produktfunktionale Seitenrollen, kritische Doppel-/Mehrzweckfälle.
- `RECHERCHE/INHALTSPOTENZIAL_V1_20261109.md`: **15** ausgesuchte Robotertypen über die ganze Themenlandschaft, **45** mögliche produktbezogene Inhaltsrubriken, **135** unterschiedliche grobe spätere Inhaltsabsichten; nicht als fertige Artikel oder geprüfte Suchvolumina ausgeben. **53** Produkttypen noch nicht produktweise vertieft.
- `RECHERCHE/DREI_SAEULEN_OWNER_V1_20261109.md`: elf Magazinrubriken, zwölf mögliche HivePress-Anbieter-/Leistungsrubriken, Beispiel-Suchintents eindeutig zu CORE/Magazin/Directory zugeordnet. HivePress aktuell NICHT eingerichtet; Werbe-/Affiliate-Plugin nicht angebunden.
- `RECHERCHE/GLOSSAR_FINDER_MODELLREGISTER_V1_20261109.md` aus **tatsächlich nachgelesenen** Pferdeatelier-, Hobbydepot- und Hab-&-Bewahr-Konzepten plus IFR/ISO-Fachrecherche: **Glossar JA**, **Roboterfinder JA als reine Filter-/Verweisansicht des EINEN Masters**, **Modellregister nach 10–15 herstellerbelegten Pilotmodellen prüfen**. Ein zusätzliches ausformuliertes Robotertypenregister mit denselben SEO-Produktseiten **NEIN**. Nicht als vierte Säule einrichten; keine weiteren Plugins oder individuellen WP-Seiten produziert.
- **Nächste fachliche Aufgabe ohne Nutzerinteraktion:** 37 identitäts-/SEO-riskante Kandidaten gegeneinander abgrenzen, 53 noch nicht vertiefte Produkttypen individuell prüfen, Glossar-Begriffe/Finder-Merkmale nur an bestehende Master-IDs binden; Quellen und offene Daten im `RECHERCHE/PRUEFSTAND_V1_20261109.md`. Bei Keyword-/DataForSEO-Kosten vorher explizite Freigabe.
- **Plugin 0.3.0 bleibt CURRENT und laut Nutzer installiert; keine neue ZIP oder WordPress-Änderung.** Bereits hochgeladener WordPress-Ist-Bericht vom 09.11.2026 nicht erneut anfordern.
