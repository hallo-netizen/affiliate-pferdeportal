# QA25 Amazon/idealo – belegte Kopplung, lokal geprüft, keine Live-Änderung

**12. November 2026 | Ist-Quelle: installierte Version 6.72.329 laut Nutzer.**

## Tatsächlicher Fehler
Originalfunktion `includes/trait-ppar-idealo.php::multiprovider_matching_offers_for_banner()` kehrt bei allen idealo-Ausgabemodi außer `combined` und `automatic` unmittelbar nur mit dem Hauptanbieter zurück. Der Amazon-eigene, bereits vorhandene `amazon_product_from_campaign()`-Gültigkeitscheck wird dabei gar nicht aufgerufen. Die Amazon-Schaltfläche hängt somit wider die geforderte Unabhängigkeit von einer **idealo-Ausgabeeinstellung** ab. Mit den **originalen PHP-Methoden**, nachgestellter WordPress-Datenquelle, reproduziert: 5/15 Negativfälle für bestehende 6.72.329. Insbesondere valider Amazon-ASIN verschwindet bei `separate`, `idealo_only`, `ebay_only`; auch gültige ASIN einer eBay-Kampagne oder gespeicherte Vertrauens-ASIN betroffen.

## Genau eine minimale KISS-Änderung, keine zweite Architektur
In **derselben vorhandenen Methode** nimmt die nicht-kombinierte Produktausgabe künftig den unabhängig geprüften Amazon-Kauflink auf, sofern **sämtliche bisherigen Amazon-Identitäts-/Bild-/PartnerNet-Gates** erfüllt sind. Fehlende, widersprüchliche oder unbestätigte ASIN erzeugen **keinen** Amazon-Link. Kein Eingriff in eBay-Lauf, Produktbestand, idealo-Feed, URL-Tracking, WordPress-Datenbank, Provider-Einstellungen oder Cron.

## Messungen an der Original-ZIP
- Vorher: 10/15 PASS, 5/15 FAIL; nachher: **15/15 PASS** für unabhängige Amazon-Zulassung und Negativkontrollen.
- eBay unabhängiger Heartbeat: **7/7 PASS**; alle 23 Plugin-PHP-Dateien: Lint PASS; ZIP-Test Python 66/66 CRC PASS.
- **63 von 66 Plugin-Dateien byteidentisch** gegenüber 6.72.329; verändert: ausschließlich `includes/trait-ppar-idealo.php` und die beiden Versionsorte (Pluginheader/Konstante, Readme). Keine weitere PHP-Funktion verändert.
- Vorbereitetes Update **6.72.330**, ZIP SHA256 `b5f5426d2e6a1b6cb6a2cb18184b497053e90be122c5b644cd3265cde93f16ac`; persistent im persönlichen Pluginbüro `/pferdeatelier/PLUGINS/QA/` samt Patch, reproduzierbarem Original-PHP-Test und Prüfprotokoll. **Nicht auf der Live-Website installiert.**

## Unbekannte Ursache des nächtlichen Vorfalls
**Nicht belegt**, dass live ein anderer idealo-Ausgabemodus als gestern eingestellt ist. Ebenfalls **nicht belegt**, ob auf den konkret sichtbaren Schabracken heute noch eindeutige Amazon-ASINs gespeichert sind. Der idealo-Feedimport schreibt `product_asins` aus dem jeweils aktuellen Feed neu; das ist ein weiterer möglicher Datenverlustpfad im Code, **nicht** nachgewiesener Live-Vorfall. Die Veränderung des GitHub-eBay-Heartbeat am 11.11. betrifft nur die GitHub-Workflowdatei und kein Amazon-PHP. Kein fiktiver E2E-Test und keine zusätzliche Vermutungsreparatur.

**Entscheidung:** Die QA25-ZIP ist lokal geprüft, darf aber nicht als bewiesene Wiederherstellung der gestrigen Amazon-Anzeige ausgegeben werden. Live-Ursache erfordert echten Vergleich des gespeicherten `output_mode` sowie `product_asins`/`_ppar_dfs_amazon_asin` für die betroffenen Produktkarten. Danach ein einziger kontrollierter Praxistest. Keine neue separate Plugin-Struktur.
