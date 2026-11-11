# Pferdeatelier Affiliate – gemeinsamer Fehler-/Ursachenstand, 07.11.2026

**Empfänger:** Hobby Depot. **Rolle:** unveränderte UPSTREAM-REFERENZ, **kein** Hobby Depot-Plugin, kein Current, keine Installationsfreigabe.

## Ausgangsstand und vollständiger Arbeitsnachweis
- Pferdeatelier-Testbasis: `AFFILIATE_ZENTRALE_6.72.308_URSACHENFIX_GESAMTTEST_NUR_TEST.zip`
- Exakter SHA-256 der Basis: `b4d8547fd2aa134f7f82f568db3a81df54bb7d2131fd0752e76e3f0ca2251fe0`.
- Sammelpatch vom 06.11.: `PFERDEATELIER_AFFILIATE_6.72.308_KISS_GESAMTURSACHEN_PATCH_NICHT_INSTALLIEREN.patch`.
- Exakter SHA-256 des Patchs: `e3311d0720a06d1f443e22bb1375688145e3fc0979de1e7ff05394ec635e23fe`. 23.179 Bytes, 316 Zeilen.
- Patch-Anwendung auf vollständige Original-ZIP lokal erfolgreich (4 PHP-Dateien betroffen; 62 der 66 Plugin-Dateien unverändert).
- **GitHub-Referenz inzwischen vollständig gesichert:** `protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH/AFFILIATE/REFERENZEN/PFERDEATELIER_6.72.308_URSACHENPATCH_NICHT_INSTALLIEREN.patch` (Originalpatch 23.179 Bytes, SHA-256 `e3311d0720a06d1f443e22bb1375688145e3fc0979de1e7ff05394ec635e23fe`). Nur der vollständige Patch liegt hier, **nicht die gesamte Pferdeatelier-Installations-ZIP**; separate persönliche Bibliotheksablage weiterhin wegen Speicherlimit blockiert.

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

## Nachtrag vom 10.11.2026 – vollständige Änderungen seit der Kopie bis QA9

Das **zentrale [Affiliate-Änderungsregister seit dem Kopierstand](https://github.com/hallo-netizen/affiliate-pferdeportal/blob/audit/affiliate-crossportal-changelog-20261110/protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/AFFILIATE/AENDERUNGSREGISTER_NACH_KOPIE_HOBBYDEPOT_HABBEWAHR_20261026.md)** ergänzt diese Referenz chronologisch um die belegten Pferdeatelier-Stände **311–315, 319/QA1–QA7, QA8 und QA9 6.72.321**. Es nennt Zweck, Ursache, KISS-Rückbau, Prüfungen, Live-Grenze und mögliche Relevanz für Hobbydepot und Hab & Bewahr.

**Kernänderung QA9:** Recherche, bereits sichere Veröffentlichung und zweistündliche Verfügbarkeitskontrolle werden getrennt; gespeicherte Angebote und Zuordnungen bleiben erhalten, nicht mehr pauschal bis zum Gesamtabschluss blockieren. **Warnung:** Nach QA9 meldete der Nutzer ein erheblich langsames Backend. Der neue Zeitplan startet nach 60 Sekunden und kann weitere Fünferpakete im 90-Sekunden-Abstand ausführen; die genaue Lastursache ist noch nicht mit realen WordPress-Messungen belegt. Deshalb **keine Übernahme dieses Codes oder Zeitplans ohne vollständigen Portaltest**.

Quellen und Tests sind im separaten [Pferdeatelier-QA-PR #748](https://github.com/hallo-netizen/affiliate-pferdeportal/pull/748) unter `protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/AFFILIATE/` und `.../PLUGINS/EVIDENCE/` gespeichert. Die installierbare ZIP liegt ausschließlich in der persönlichen Plugin-Library. **Keine Änderung der Hobbydepot-Plugin-Version, Daten, Kampagnen, Providerzugänge oder Current durch diesen Nachtrag.**

### QA11-Folgeänderung vom 11.11.2026 – nur Hobbydepot-Referenz

Pferdeatelier QA11 **6.72.322** behebt den per PHP nachgewiesenen **Gesamtabbruch durch einen Einzelartikel bei der finalen eBay-Verfügbarkeitsprüfung**. Andere Angebote werden im bestehenden getItem-Pfad weiter geprüft; ungültige Quellen bleiben gesperrt und der letzte sichere Produktstand geschützt. Zusätzlich ist für exakt diesen Fehler die Schlussprüfung **ohne erneute Recherche** fortsetzbar. Das Backend fragt Status ohne Worker-Start ab und lädt die ausführliche CSV-Auswertung nur bei Bedarf. Enthält die separat dokumentierte QA10-KISS-Änderung.

**Hobbydepot nicht automatisch aktualisieren:** Nur als gemeinsames Entwicklungs- und Fehlerregister. Eigene Provider-, Kampagnen- und Datenwege gegen diesen konkreten [Pferdeatelier-QA11-Patch](https://github.com/hallo-netizen/affiliate-pferdeportal/blob/qa/pferdeatelier-ebay-319-qa5-evidence-20261110/protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/PLUGINS/EVIDENCE/EBAY_QA11_GESAMT_KISS_FIX_GEGEN_QA9.patch) vergleichen. Keine Portierung, kein ZIP in Hobbydepot, keine Änderungen an dessen Current oder gespeicherten Produkten. Vollprotokoll im [zentralen Änderungsregister](https://github.com/hallo-netizen/affiliate-pferdeportal/blob/audit/affiliate-crossportal-changelog-20261110/protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/AFFILIATE/AENDERUNGSREGISTER_NACH_KOPIE_HOBBYDEPOT_HABBEWAHR_20261026.md). Echte WordPress-Abnahme von QA11 fehlt noch.
