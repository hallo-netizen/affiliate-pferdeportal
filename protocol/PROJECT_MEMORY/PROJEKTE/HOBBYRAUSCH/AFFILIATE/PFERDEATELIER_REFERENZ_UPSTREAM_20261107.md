# Pferdeatelier Affiliate – gemeinsamer Fehler-/Ursachenstand, 07.11.2026

**Empfänger:** Hobby Depot. **Rolle:** unveränderte UPSTREAM-REFERENZ, **kein** Hobby Depot-Plugin, kein Current, keine Installationsfreigabe.

## Ausgangsstand und vollständiger Arbeitsnachweis
- Pferdeatelier-Testbasis: `AFFILIATE_ZENTRALE_6.72.308_URSACHENFIX_GESAMTTEST_NUR_TEST.zip`
- Exakter SHA-256 der Basis: `b4d8547fd2aa134f7f82f568db3a81df54bb7d2131fd0752e76e3f0ca2251fe0`.
- Sammelpatch vom 06.11.: `PFERDEATELIER_AFFILIATE_6.72.308_KISS_GESAMTURSACHEN_PATCH_NICHT_INSTALLIEREN.patch`.
- Exakter SHA-256 des Patchs: `e3311d0720a06d1f443e22bb1375688145e3fc0979de1e7ff05394ec635e23fe`. 23.179 Bytes, 316 Zeilen.
- Patch-Anwendung auf vollständige Original-ZIP lokal erfolgreich (4 PHP-Dateien betroffen; 62 der 66 Plugin-Dateien unverändert).
- **WICHTIG:** Die Patch-Originalbytes befinden sich weiterhin nur im betreffenden Chat-Arbeitsartefakt und sind **nicht** physisch in diesem GitHub-Büro hochgeladen. Eine Bibliotheksablage in beiden Affiliate-Büros scheiterte am Speicherlimit; daher kein vorgetäuschter Vollbackup-PASS.

## Änderungen (für jedes spätere Fremdprojekt einzeln gegen dessen eigene Quelle prüfen)
1. `includes/trait-ppar-ebay.php`: Produktgruppensuche mit maximal einer bedingten zweiten Ergebnisseite; eBay-Marktplatz-Gate EBAY_DE unverändert. Zusätzlich redundant wiederholte Qualitätsprüfung aus Preis-Neubewertung entfernt; nur Preisanteil neu berechnet.
2. `includes/trait-ppar-ebay-run.php`: Abdeckungsprüfung liest Produkt- und Kreativdaten gebündelt; verhindert 2 Datenbankabfragen je Eintrag. Festhängende Statusabfrage stößt keinen synchronen schweren Arbeitslauf an; erneuter Versuch höchstens alle 5 Minuten.
3. `includes/trait-ppar-ebay-account-deletion.php`: Löschmeldung durchsucht Rohdaten in 100er-Schritten und hält vor irreversibler Löschung an, wenn eine DB-Lesung scheitert. Ein überfälliger Crontermin kann ohne Doppeltermin einmalig neu angestoßen werden.
4. `pferdeportal-affiliate-router.php`: ehrliche Anzeige überfälliger Cron-Termine und fehlender Fertigstellungsnachweise.

## Prüfungen und bekannte Grenzen
- Alter lokaler Sammelprüfbericht: 68 Simulationen PASS, PHP-Dateien Syntax PASS; **keine echte WordPress-Liveabnahme**.
- Aktueller Source-Check 07.11.: In der Anfrage ist `X-EBAY-C-MARKETPLACE-ID: EBAY_DE` bereits gesetzt, zugleich filtert `deliveryCountry:DE` nach Lieferung und nicht nach dem Herkunftsmarktplatz. Deshalb Fremdmarktplatz-Sperre keinesfalls einfach abschalten.
- Die im Quellstand fest erzwungenen **6 Stunden Frische** sind eine absichtliche Schutzregel; ohne Provider-Nachweis nicht verlängern.
- Kein Beweis steigender Live-Produktabdeckung. Auch die 201+ wartenden eBay-Löschmeldungen sind nicht live als erledigt bestätigt.
- GitHub-Releasesteuerung des Pferdeateliers: 6.72.211 / AFF-ERR-065 weiterhin formal BLOCKED. Lokale 6.72.308-Arbeitskopie ist nicht die autorisierte GitHub-Current.
- Hobby Depot besitzt einen eigenen Pluginstand. **Nichts automatisch übernehmen, kein Current und keine Zugangsdaten überschreiben.**

**KISS-Übernahmeregel ab 07.11.2026:** Jede neue bestätigte Pferdeatelier-Änderung mit Basisversion, Ursprungshash, fachlichem Grund, betroffenen Dateien, Regressionstest und Live-Grenze **in diesem Affiliate-Büro** dokumentieren. Gemeinsame Logik nur nach Diff gegen die eigenständige Pluginquelle übernehmen. Bei gleicher Logik nicht erneut portieren; keine zweite Engine.
