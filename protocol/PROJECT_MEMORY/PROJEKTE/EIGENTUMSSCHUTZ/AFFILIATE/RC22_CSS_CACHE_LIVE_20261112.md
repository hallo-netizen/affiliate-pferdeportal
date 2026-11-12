# HAB & Bewahr – RC22 Rootfix: Browser zeigt nach Plugin-Update unverändert große, gestapelte Produktkacheln

**Datum:** 12.11.2026 · **Portal:** ausschließlich Hab & Bewahr · **HAB-004 Release:** RC22 (0.1.19-rc22) · **WordPress-Live-Installation RC22:** noch offen.

## Nachgewiesene Ursache (nicht geschätzt)

1. Betreiber meldet: Installation des vollständigen **RC21** brachte subjektiv **keine sichtbare Änderung** auf der Kategorie `Haustürschlösser` (`/einbruch-und-diebstahl/einbruch-und-diebstahl-haus-und-wohnung/c22-haustuerschloesser-dd9773fd40/`). Die drei Amazon-Karten blieben groß und untereinander.
2. **Öffentliche echte Seite** vom 12.11.2026 mit HTTP 200 und 188.006 HTML-Bytes abgefragt: Der **neue RC21-Kategoriemarkup** `ppar-hb-category-products-grid` ist **tatsächlich vorhanden**, mit drei bestehenden Affiliate-Slots. Der Plugin-Update-Code ist somit serverseitig aktiv.
3. Die Seite bindet jedoch **`assets/frontend.css?ver=6.72.211-hb-rc16-20261108`** ein. Diese Versionskennung wurde nach RC16 trotz RC21-CSS-Änderungen **nicht** aktualisiert. Die betroffenen Browser können eine alte CSS-Fassung für dieselbe URL behalten. **Der Fehler liegt in der Versionierung der CSS-Ressource, nicht in einer fehlenden gespeicherten Kategorie oder Datenbank.**
4. **Wichtig:** Der Server liefert das richtige neue CSS bei einer frischen HTTP-Abfrage (100.383 Bytes, SHA256 `de6af0e8fb11d0580d9238f1d2ccd459f902b96225c81d8c0c249e8af0dc2da7`). Dies ist **kein Beweis**, welcher Cache beim konkreten Betreiber lokal geladen war, aber die Ursache ist in einem echten Browser **exakt reproduzierbar**.
5. **Echter Chrome-Headless-Test mit unveränderter Live-Seite**, Run **43247959556**: Neue CSS-Fassung ergibt **3 Karten nebeneinander**, `x=123/521/919`, alle `y=1496`, Breite je 384 Pixel. In genau derselben Seite wurde **ausschließlich testweise** die alte RC20-`frontend.css` eingeblendet: Die Karten standen sofort wieder **untereinander**, `x=123/123/123`, `y=1529/1762/2020`, Breite je 1180 Pixel. Nach Rückschalten auf RC21-CSS: wieder 3 nebeneinander. **Dieser Vorher-/Nachher-Beweis bestätigt das tatsächliche sichtbare Symptom.**
6. Breitenprüfung frisches Chrome, Run **43247047847**: Desktop 1440px: 3 Spalten; Desktop 1050px: 3; Tablet 750px: 2; Mobil 390px: 1. **Keine Fotos im Produktblock, drei Amazon-Anbieterlinks**: Produktbilder und Idealo-Zusatzangebote sind **ein separates Daten-/Freigabeproblem**, nicht durch CSS behoben.

## Minimaler RC22-Fix (bestehendes HAB-004, kein zweites Plugin)

- Aus **RC21 `CURRENT.zip` exakt SHA256 `0f40eddb4526434c03acdd370d2763ac5a01eaea862a40cb9ae25bb8754363bf`** aufgebaut.
- In der bestehenden Haupt-Plugin-Datei die bislang fixierte CSS-Version `self::VERSION . '-hb-rc16-20261108'` ersetzt durch eine Versionskennung aus dem **echten Plugin-Header** mit der vorhandenen WordPress-Core-Funktion `get_file_data(..., 'plugin')`. Der nächste Pluginrelease invalidiert damit automatisch alte Browser-/Proxy-Caches. Keine neue HTTP-Abfrage, Datenbank, Plugin, Sonderfunktion oder Templateänderung.
- Neue Vollversion `0.1.19-rc22` im Hauptplugin und Readme. **Nur diese zwei Dateien im Inneren der ZIP geändert**. Das Layout-CSS, Kategoriebrücke, multiprovider/Idealo, ASIN-/GTIN-Zuordnung, Amazon, eBay und Versicherungsregeln sind gegenüber RC21 **byteidentisch**.
- Vollständiges offizielles `CURRENT.zip` + `HAB_AFFILIATE_RC22_0.1.19-rc22.zip` mit **36 Dateien, 2.337.621 Bytes**, SHA256 `c9d501396d5500e699eb6dd8d867318c41e8ea8efc43c8fe00ad9ee4ab4e32d1`.
- Runner **43247959556 PASSED**: 25/25 PHP Syntax, alle 11 RC21-HAB-Design/PHP-Bridgetests, 36/36 Affiliate-/432/432 Design-CRC, echte WordPress-ähnliche Headerauswertung ergibt jetzt `6.72.211-hb-plugin-0.1.19-rc22`; realer Chrome-Vorher-/Nachher-CSS-Gegentest besteht.
- Nach Installation sollte CSS im Seitencode mit **`?ver=6.72.211-hb-plugin-0.1.19-rc22`** erscheinen. **Erst diesen Live-Readback und die sichtbare Darstellung prüfen, bevor RC22 als live abgenommen gilt.** Kein aktives WordPress-Konto oder Schreibzugriff zum Installieren vorhanden.

## Noch nicht gelöst – nicht als abgeschlossen melden

- **Echte Produktfotos**: Hab-Amazon-ASIN/Titel ergeben keine lizenzierten Produktbilder. Frische Browserprüfung zeigt in den drei getesteten Kacheln aktuell **0 Bilder**. Keine fremden ASIN-Fotos oder generierte Platzhalter als konkretes Produkt ausgeben.
- **Mehrere Providerbuttons je Einzelprodukt**: aktuelle drei Kacheln haben nur Amazon; Idealo-Feed ist zwar mit freigegebener Adspace/Feed-ID verbunden, muss noch in der bestehenden Affiliate-Zentrale verfügbar gemacht werden, mit echten GTIN-Zuordnungen und freigegebener öffentlicher Idealo-Ausgabe; bestehende technische Mehrfachanbieterfunktion ist vorhanden, aber ohne Matching nicht sichtbar. **Nicht behaupten, dass Multibuttons bereits live sind.**
- **Artikel** weiterhin nicht geändert; **Versicherungszweig** bleibt aus Produktwerbung ausgespart. **Pferde Atelier, Hobby Depot und HAB-001-Design unverändert**.

## Installationsschritt

Bestehendes Hab-&-Bewahr-`Affiliate-Portal-Router` mit der vollständigen `HAB_AFFILIATE_RC22_0.1.19-rc22.zip` aktualisieren. Keine separate zweite Installation und keine manuellen Seitenbearbeitungen. Danach die identische `Haustürschlösser`-Kategorie neu öffnen und echte Desktop-Kacheln kontrollieren. Bei weiterer Abweichung CSS-Link und Browserzustand direkt prüfen, nicht mehrere Plugins blind ändern.
