# Navigationsebenen 12.11.2026 – geprüfter Stand und Entscheidung

## Nutzerabnahme
Der Nutzer meldet Robotik-Testdesign **0.2.3** als visuell **okay**. Er fragt, warum Haushalt im Mega-Menü weniger Tiefen zeigt als Garten und ob die letzte Kategorieebene erscheinen soll. **Keine Designversion erzeugen, keine zusätzliche Pluginrunde.**

## Befund (Originalcode + importiertes Fachprofil)
- Genau **104 WordPress-Seiten** in 0.4.2 eingebettet: 7 Hauptseiten, 25 Zwischen-/Landingpages, 72 konkrete Produktseiten.
- Original-0.2.3-PHP rendert im lokalen WordPress-Mock **104 von 104 Seiten als Links** im siebenfachen Mega-Menü; keine fehlenden Seitenlinks.
- **Haushalt:** drei direkte Produktseiten, ohne künstliche Zwischenebene; 4 vertiefende WordPress-Beitragskategorien.
- **Garten:** vier direkte Unterseiten, davon drei mit weiteren Produktseiten und eine Produktseite; 7 Produktseiten insgesamt, 9 vertiefende WordPress-Beitragskategorien.
- **Industrie** unter Gewerbe umfasst vier Landingpages, ebenfalls von der Mega-Ausgabe verlinkt.
- Der Importplan enthält zusätzlich **89 flache WordPress-Beitragskategorien**, an 72 konkrete Produktseiten über `_robotik_product_page_id` gebunden. Im ursprünglichen 0.2.3-Frontend wird keine einzige dieser Taxonomien dargestellt. Dies ist eine **echte funktionale Lücke für die spätere Produktseitenansicht, aber kein fehlender Menüpunkt und kein Strukturimportfehler**.
- 63/89 Kategorien heißen kurz „Kaufberatung“; Keywords und spezifische Inhalte sind noch nicht aus echten DataForSEO-Abfragen validiert. Eine blinde Veröffentlichung leerer Kategoriearchive wäre keine fachlich fundierte SEO-Aufwertung.

## Verbindliche KISS-Entscheidung
1. **Sieben Hauptbereiche und unterschiedliche Tiefe im Header beibehalten.** Keine optische Gleichmacherei, keine 89 Kategorie-Links im Mega-Menü.
2. Letzte, flache WordPress-Beitragskategorien **jeweils auf ihrer zugehörigen Roboter-Produktseite** anbieten, sobald Produktseitenlayout/echte Inhalte dafür bereit sind, nicht global im Header/Footer.
3. Gruppenseiten benötigen später echte Verweise zu ihren Unterseiten, statt leerer WordPress-Standardinhalte; Design erst im selben bestehenden Plugin angehen, nicht sofort eine neue ZIP.
4. Als nächstes die **SEO-Sammelprüfung in vorhandener Kategorie-Pluginversion 0.4.2** (Backend `Robotik Kategorie → DataForSEO`): Zugang speichern und kostenlos testen, kostenloses Preflight über 161 Keywords. Kostenpflichtige SEO-Abfragen nur nach separater Freigabe, keine automatische Mutation des Masterbaums.
5. Live-WordPress-Einträge können von der lokalen Prüffassung abweichen. Der Nachweis **104/104** bezieht sich auf den Originalimportplan und Originalrenderer im lokalen WP-Mock, **nicht auf einen unabhängigen Live-Readback**.

## Nachweisdokumente
- Library: `/robotik/Designbüro/ROBOTIK_NAVIGATION_EBENENPRUEFUNG_2026-11-12.md`
- Library: `/robotik/Konzeptbüro/ROBOTIK_NAVIGATION_EBENENPRUEFUNG_2026-11-12.json` (maschinelle 104/104-Prüfung).
- Designplugin 0.2.3 und Kategorie/DataForSEO-Plugin 0.4.2 sind **unverändert**.
