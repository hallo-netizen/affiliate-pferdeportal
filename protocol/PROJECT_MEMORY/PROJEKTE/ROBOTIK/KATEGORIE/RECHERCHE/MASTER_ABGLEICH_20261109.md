# Robotik – geprüftes bewährtes Kategorie-Verfahren
Stand: 09.11.2026 · Gilt nur für ROBOTIK/KATEGORIE

## Originalunterlagen nachgelesen
1. `PROJEKTE/HOBBYRAUSCH/SEO_KATEGORIEN/ZIELVERTRAG_HD001_AUTOMATISCHE_SEO_HIERARCHIE_20261003.md` (V2.8): Zentraler Hobbybestand → HOBBY_MASTER V2 → fachliche Bewertung → integrierter Drei-Säulen-Zielbaum → DataForSEO als Beleg → globale Suchintent-/Owner-Prüfung → WP/HivePress-Abgleich → tatsächlicher Frontend-Readback.
2. `PROJEKTE/HOBBYRAUSCH/SEO_KATEGORIEN/KATEGORIE_WORKFLOW_AUDIT_20260926.md`: 14-stufige Kategorie-Recherche, Keyword Ideas/Suggestions/Overview; damals konnte der Writer WordPress-Taxonomien, aber **keine WordPress-Seiten** anlegen.
3. `ALLGEMEINGUELTIGE_BAUSTEINE/KATEGORIENMODELL/CURRENT_STATE.md`: allgemeine V1.9.1 derselben Pluginlinie, Recherche nur lesend; Writer getrennt und nur nach Freigabe.
4. `PROJEKTE/EIGENTUMSSCHUTZ/KONZEPT/KATEGORIEN_NAVIGATION_PORTALSTANDARD_FEHLERLEHREN_20261017.md`: Bestandsverlust/Dubletten verhindern, Produkt-`page` nie mit `category` verwechseln, nur ein aktiver Writer, positive/negative Tests und echte WordPress-Abnahme.

## Verbindlicher KISS-Ablauf für Robotik
**Quelle:** ausschließlich `RECHERCHE/PRODUKTE_V2_20261108.json` mit stabilen `rb...`-IDs. 68 Hypothesen, sämtlich UNAPPROVED; keine ist schon eine fertige Produktseite.
**Geschichte:** alte `RECHERCHE/PRODUKTKANDIDATEN_20261108.json` mit 27 Namen ist ARCHIV. Alle 27 auf den neuen Master zurückverfolgt; 17 identische Namen, 10 Namensabweichungen bewusst als `REQUIRES_HUMAN_REVIEW` markiert, nicht blind synonymisiert.
**Entscheidung:** Chat/Fachprüfung kann Masterkandidaten mit Quellen beurteilen und freigeben; DataForSEO/Plugin liefert Suchintent-, Keyword-, Lücken- und Überlappungs-Evidenz, darf NICHT selbst Kategorien erfinden.
**Abgeleiteter WP-Zielbaum:** allein `PLAN/robotik-empty.json` beziehungsweise seine später genehmigte Revision; aktuell weiterhin **LEER**. Später pro letzte Produktseite einen erkennbaren Bezug zur freigegebenen `rb...`-ID bewahren. Flache Content-Kategorien erst bei mindestens drei unterschiedlichen sinnvollen späteren Beitragsrichtungen.
**Drei Säulen:** CORE/Produkt-Hierarchie, Magazin und HivePress mit fachlichem Haupt-Owner; keine kopierten Produktseiten über Säulen.
**Live:** zuerst Dry-run/Delta und explizite Freigabe; danach genau ein Writer, WordPress-Readback und echter Desktop-/Mobil-Frontendcheck. Designplugin und Kategorieplugin dürfen nicht konkurrierend schreiben.

## Wichtige nicht gelöste Technikgrenze
Die aktuell installierte Robotik-Version **0.2.0** validiert JSON lokal und speichert WordPress-Entwürfe, aber **liest nicht** `PRODUKTE_V2_20261108.json` von GitHub. Eine selbständige in WordPress gespeicherte Kopie kann veralten. Die behauptete automatische Abstimmung ist daher derzeit **NICHT TECHNISCH GEWÄHRLEISTET**.

Für echte Abstimmung zuerst die vorhandene allgemeine Kategorie-Pluginlinie auf eine **manuell auslösbare, nur lesende Übernahme der aktuellen Robotik-Masterrevision** anpassen (kein zweites Plugin, kein Frontendabruf, keine API-Kosten) und die Revision vor jeder späteren WP-Freigabe erneut vergleichen. Das ist ein noch offener Umsetzungsschritt, nicht schon erledigt.
