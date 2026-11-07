# Hab & Bewahr – Amazon-Automatik: HARTE RC3-Quellprüfung (07.11.2026)

## Nutzerentscheidung
- Keine manuelle Anlage einzelner Amazon-Links.
- Gewünschter bestehender Pferdeatelier-Weg: automatische Such-/Produktverknüpfung über idealo-Produktdaten und/oder DataForSEO, keine zweite Engine; isoliert für Hab & Bewahr anpassen.
- Amazon PartnerNet: `https://hab-und-bewahr.de` auf bestätigter Website-Liste neben Pferdeatelier/Hobbydepot. Eigene Tracking-ID laut SiteStripe-Screenshot **`habundbewahr-21`**, aktuell auswählbar. Credentials nicht in Plugin/Repository schreiben. Branding-Banner zweitrangig, keine manuelle Übergangslösung.
- idealo beantragt, noch nicht freigeschaltet. Damit ist gegenwärtig kein nutzbarer idealo-Produktfeed für Hab & Bewahr belegt. Die eBay-Developer-Keyset-Anträge sind separat offen.

## Exakter Beweis: Offizielles Hab-Plugin
- Originales, **tatsächlich lokal vorliegendes**, unmodifiziertes `HAB-004-Affiliate-0.1.0-rc3.zip` geprüft: 605.196 Byte, SHA-256 `2e5f6790ab3a64b446e34d132037684ad8fa637f76f43974e2816a1f75bc11eb`. Stimmt mit dem GitHub-CURRENT-Manifest überein. 27 Plugin-Dateien, WordPress-Pluginwurzel `affiliate-portal-router/`.
- Alle PHP-/JS-/Textdateien nach `DataForSEO`, `dfs_amazon`, `amazon_search`, `ppar_network_amazon` durchsucht: **je 0 Treffer**.
- `includes/class-ppar-product-source-plan.php`: Amazon ist nur `state=prepared`, mit ausdrücklichem Kommentar `the real adapter remains absent until real access exists`.
- `includes/trait-ppar-provider-registry.php`: Amazon `state=prepared`, mit `capabilities=('creatives','outputs','veto')`, **keine** Amazon-Schnittstelle, kein Feedimport, keine automatische ASIN-Recherche.
- `includes/trait-ppar-idealo.php`: tatsächlicher existierender idealo-Feed-Import und Verarbeitung der gegebenenfalls dort enthaltenen `asins_product`/`product_asins` sowie `gtin`; `amazon` sonst nur als Netzwerklabel/Anbieteroption. Ein automatisch erzeugter Amazon-/DataForSEO-Direktproduktlink ist in RC3 damit **nicht belegt**.
- Der Hab-Baucode unter `AFFILIATE/HAB_BAU/build.py` basiert explizit auf dem neutralen älteren 26-Dateien-Stamm; er enthält ebenfalls **0** Treffer für `DataForSEO`, `dfs` oder `amazon`. Seine feste Aussage „alle Funktionen des neutralen Stamms erhalten“ ist **kein Beweis** für später in Pferdeatelier hinzugefügte Amazon-Funktionen.
- Deshalb ist die Aussage „Amazon/DataForSEO muss nur noch per Schalter für Hab aktiviert werden“ für diese exakte ZIP **widerlegt**. Ebenso falsch wäre „keine Affiliate-Infrastruktur vorhanden“: idealo, Werbemittel, Ausgabe/Kategorieziel-Regeln sind bereits vorhanden.

## Pferdeatelier-Referenz (nur lesend, nicht als Installationsbasis)
- In den übergebenen Prüfdateien der neueren Pferdeatelier-ZIPs 6.72.284–6.72.287 sind `includes/trait-ppar-dfs-amazon.php`, `ppar_amazon_search_v1` und eine automatisierte ASIN-Suche tatsächlich dokumentiert.
- DataForSEO kann für bereits vorhandene, eindeutig identifizierte idealo-/eBay-Produkte passende ASIN suchen. Es liefert **keine** erlaubten aktuellen Amazon-Preise/Bilder/Verfügbarkeiten. Maximal 5 kostenpflichtige Suchaufträge/UTC-Tag im dokumentierten Original.
- Historisch zusätzlich automatisierte Amazon-Suchlinks für Kategorien/Artikel ohne API. Das ist keine vollautomatische eigenständige Amazon-Produktversorgung.
- Die Pferdeatelier-Voll-ZIP 6.72.304 ist in der Nutzerdateiliste **verzeichnet**, die angeforderte Übernahme der Originalbytes in die lokale Laufzeit scheiterte aber ausdrücklich; Quellstand ist hier nicht byteweise zur Hab-ZIP diffbar. Reproduktion der ursprünglichen vollständigen Amazon-Engine aus Beschreibungen wäre ungeprüfte Neuerfindung, verboten.
- Sonstige Projekte, vorhandene Pferdeatelier-/Hobbydepot-Bereiche, eBay-Notification-Endpoints und Pluginversionen bleiben unverändert.

## Ergebnis / Nächster Schritt
**Status: BESTAND BEWIESEN / AMAZON-ANPASSUNG IN RC3 FEHLT / KEIN UNGEPRÜFTES PLUGINUPDATE AUSGEBEN.**

Der sicherste KISS-Weg ist, aus der zugänglichen vollständigen neueren **originalen Pferdeatelier-Affiliate-ZIP** ausschließlich die tatsächlich enthaltene Amazon/DataForSEO-Automatik nach unabhängigem Codevergleich in die **eigene Hab-RC3-Quelle** zu übernehmen, ihre Zielkategorien und Hab-Tracking-ID getrennt zu binden, bestehende idealo-/eBay-/Affiliate-Ausgabe zu regressionsprüfen, standardmäßig deaktiviert testen und erst nach bestandenem Original-Gesamttest ein einziges vollwertiges Hab-004-Update mit GitHub-CURRENT-Archivierung herauszugeben. Kein manuelles Einzel-Link-Anlegen; kein zweiter Schalter-/Datenbank-/Worker-Weg. Wo Idealo/ASIN-Kandidaten fehlen, darf keine konkrete Amazon-Produktkarte behauptet werden; Searchlink-Fallback nur nach eindeutiger bewusster Freigabe und echten Zieltests.

**Harte Arbeitsgrenze heute:** kein Code verändert, nichts in WordPress installiert, kein Test einer behaupteten neuen Amazon-Ausgabe auf `hab-und-bewahr.de`. Der erwiesene RC3-Zustand bleibt die einzige Plugin-Current.
