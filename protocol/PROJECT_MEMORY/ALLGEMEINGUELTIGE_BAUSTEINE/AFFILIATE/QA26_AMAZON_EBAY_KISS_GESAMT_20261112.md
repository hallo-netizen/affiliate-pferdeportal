# QA26 Pferdeatelier Affiliate 6.72.331 – geprüfte vollständige ZIP, keine Live-Aktivierung

Datum: 2026-11-12. Grundlage ist exakt der laut Nutzer live installierte Stand 6.72.329 mit SHA256 97df9edc9b883194ff9666ad285b3f090db6e1889090fd25f1e22440a701b2db. Der frühere QA25-Test 6.72.330 wurde NICHT als Patchbasis verwendet.

Reale WordPress-Diagnose vom 12.11.: idealo `automatic`, Amazon aktiviert, letzter idealo-Import 09.11. 22:16:26 UTC; sieben getestete Produktkarten mit verifizierter einzelner ASIN liefern im originalen PHP **nur idealo**. Kausal nachgestellt: sobald das alte idealo-Frische-Gate `idealo_campaign_publicly_allowed` auf false geht, überspringt die gemeinsame Produktausgabe auch den eigenständig verifizierten Amazon-ASIN-Link. **Vorher 7/7 FAIL, nachher 7/7 PASS** mit den sieben echten ASIN-Fällen als Regressionsfixture.

Direkte KISS-Korrektur ausschließlich in `includes/trait-ppar-idealo.php`:
- Vorhandene Amazon-ASIN-/Bild-/Trackingentscheidung ohne idealo-Modus- oder idealo-Frische-Veto für die vorhandene Produktkarte verwenden.
- Bei neuem idealo-Feed ohne ASIN die zuvor eindeutig vorhandene ASIN im bestehenden Produktdatensatz nur bei **vollständig identischem GTIN-Produkt** erhalten. Bei geänderter GTIN, neuem widersprüchlichem ASIN, mehrdeutiger oder unzulässiger alter ASIN **keine** Übernahme. Keine neue DB-Tabelle, keine Cron-, API-, Feed- oder eBay-Architektur.
- 2 Versionsangaben zusätzlich auf 6.72.331; insgesamt 63/66 Plugin-Dateien byteidentisch zum Vorgänger, alle vier eBay-Dateien byteidentisch.

**Prüfstand:** Amazon 41/41 lokale original-PHP-/WordPress-Mock-Kontrollen PASS, eBay Worker-/Heartbeat 7/7 PASS, 10 eBay Original-Klassifikator-Proben ausgeführt, PHP Lint 23/23 PASS, 66 ZIP-CRC-Einträge PASS, Versionsstand 3/3 konsistent. Kein realer WP/DB/eBay-API-End-to-End-Test. GitHub PR #756 eBay-Heartbeat ist gemerged, beide Schutzchecks des main-Rulesets aktiv; letzter beobachteter echter Heartbeat idle, aktiver Live-eBay-Produktlauf **nicht** belegt.

**Eine vollständige ZIP**, persistent in persönlichem Pluginbüro: `/pferdeatelier/PLUGINS/QA/Pferdeatelier_Affiliate_6.72.331_AMAZON_EBAY_KISS_GESAMT.zip`. SHA256 `f11f19f996cd5b22a3b910f61279020ca866493bbef8a46ee406361111f5cbb4`.

Grenze: Amazon-Lösung für **vorhandene Karten**. Eine später durch komplette Quell-Entfernung nicht mehr vorhandene Karte kann damit nicht als unabhängig anzeigbar bewiesen werden. Keine Veränderung der Live-Website in diesem Vorgang.
