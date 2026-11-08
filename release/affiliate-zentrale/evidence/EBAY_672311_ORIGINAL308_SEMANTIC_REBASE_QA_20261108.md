# Pferdeatelier Affiliate / eBay 6.72.311 – echte Originalbasis 6.72.308, lokales KISS-Gesamt-Quellgate (08.11.2026)

**Status: QUELLCODE-TEST PASS, LIVE-RELEASE NICHT FREIGEGEBEN.**
Dieses QA-Dokument ist aktuellster Nachtrag zum historischen `EBAY_672311_GESAMTFLOW_QUELLGATE_AUDIT_20261108.md`. Die damalige Aussage „Original-ZIP für vollständigen Test nicht lesbar“ gilt **seit der erfolgreichen persistierten Library-Ablage nicht mehr**. Das GitHub-Current 6.72.211 und `CURRENT_RELEASE.json` bleiben UNVERÄNDERT.

## Physische Ablage, ausgelesen und zurückgeprüft

- Original **6.72.308**: `/pferdeatelier/PLUGINS/AFFILIATE_ZENTRALE_6.72.308_URSACHENFIX_GESAMTTEST_NUR_TEST.zip`
- Original SHA-256: `b4d8547fd2aa134f7f82f568db3a81df54bb7d2131fd0752e76e3f0ca2251fe0`
- Neue **6.72.311 QA nur Test**: `/pferdeatelier/PLUGINS/QA/AFFILIATE_ZENTRALE_6.72.311_ORIGINAL308_BUSINESS_ONLY_KISS_QA_NICHT_INSTALLIEREN.zip`
- QA SHA-256: `c2e43b13f7a74a5d9cb4824b15a0fb17ae711961aa56e3253566983807e8aa94`
- QA-Prüfnachweise inkl. ausführbarer PHP-Referenztests/Rebase-Skripte und Original-/Patchanker: `/pferdeatelier/PLUGINS/QA/EBAY_311_ORIGINAL308_QA_NACHWEISE.zip`
- Arbeitsstand: `/pferdeatelier/PLUGINS/QA/EBAY_311_ORIGINAL308_QA_STAND_20261108.md`
- Persistente QA-ZIP **nach dem Upload erneut materialisiert** und bytegleich / SHA-256 identisch bestätigt.

## Durchgeführt / Ursachen

Der kumulative 311-GitHub-Patch enthält 58 Hunks / 75 Änderungsgruppen, aber seine Zeilennummern entsprechen nicht dem tatsächlich physisch geprüften 308-Plugin. Blindes Patchen führte zum PHP-Syntaxfehler (Testverwurf). Danach **64 Änderungsgruppen mit eindeutigen Original-Funktions-/Textankern rebasiert**, 11 bereits in 308 enthaltene bzw. gegenstandslos gewordene PRIVATE-Alt-Patches nicht erneut angewandt. Fünf Dateien tatsächlich geändert, **61/66 Dateien bytegleich**. Alle **23/23 PHP-Dateien Syntax PASS**, Originalkatalog und Portalstruktur SHA-korrekt.

**Zusätzlicher echter Ursachenfix:** Der letzte öffentliche Quellrefresh hatte einen Retry-/Cursor-Standsverlust, wenn er noch das alte Run-Snapshot erhielt. Der vorhandene kanonische gespeicherte Lauf wird bei identischer Lauf-ID erneut gelesen; begrenzte Retry-/Cursor-Daten bleiben ohne zweite Worker-Strecke erhalten. Ein simuliertes 3-maliges Provider-Timeout demonstrierte zunächst diesen Fehler, nach Fix **49/49 ausführbare PHP-Prüfungen PASS**.

Geprüft wurden BUSINESS-only-Routing und alte ALL/PRIVATE-Snapshots, bestehende HivePress-Inserate, sichere Entfernung eigener Legacy-eBay-Anzeigen in 25er-Paketen, Quell-/Policy-/Frische-/Endfreigabe, 6-Stunden-Quellverfall, sichere Vorversion, HTTP 429/503/cURL28 und 401, dauerhafte Wiederholung und fehlerfreie Abbruch-/Warnzustände. **Kein neuer Worker, keine neue Tabelle und kein Frontend-HTTP**. Kein Eingriff in K0, WordPress oder andere Provider.

## Unveränderte Grenzen / tatsächlicher nächster Schritt

**Kein WordPress/MariaDB-Live-E2E und keine echten eBay-Browse/getItem-Abfragen** durchgeführt. Kein Beleg, dass das Live-System diese QA-ZIP installiert hat oder die tatsächlichen 311 Laufpakete bis Ende durchlaufen sind. Ungeprüft bleiben tatsächliche WP-Sitemap, direkte HivePress-Einzelseiten, echter Business-Produktkarten-Render und Benutzer-/Account-Konfiguration. `release_allowed=false` bleibt bestehen.

**Nächster Schritt: ein kontrollierter vollständiger Testlauf in isolierter WordPress-Umgebung** (echte Datenbank + eBay-Endpunkte) anhand der originalbasierten QA-ZIP, einschließlich negativer Suche, Altanzeigen und sämtlicher Frontend-Kontexte; erst bei echten belegten PASS-Ergebnissen Installations-/Release-Freigabe. **Original 308 nicht neu anfordern**; Library ist Quelle. Nicht mit GitHub 6.72.211 gleichsetzen oder aktuelle ZIP fälschlich als GitHub-Binärinhalt darstellen.
