# HAB-004 RC8 – tatsächlich ausgeführte Ablauf-Simulation (07.11.2026)

**RC8 ist lokal gebaut und vollständig gegen den realen HAB-004-Code geprüft, aber die Binär-ZIP ist noch NICHT in GitHub-CURRENT.zip übernommen. Das GitHub-CURRENT bleibt derzeit RC7. Nicht als abgeschlossen markiert.**

Artefakt aus demselben Hab-&-Bewahr-Chat: `HAB_UND_BEWAHR_AFFILIATE_0.1.5_RC8_WORKFLOW_GEPRUEFT.zip`, 620242 Bytes, ZIP-SHA256 `f2d09e649fbb6a69a54e64b01df239013975999e46921f08b722adff139ccd30`, 28 Dateien. Verändert wurden nur `affiliate-portal-router.php`, `includes/trait-ppar-hb-amazon.php`, `readme.txt`. 25/28 Dateien bytegleich zur offiziellen RC7. Kein anderes Portal bearbeitet.

Screenshot 07.11.2026 13:06 zeigte nach einem manuellen Klick: tatsächlicher Lauf um 12:06, **0/5 API-POST, 0 Kategorien, 0 Beiträge, 0 Links**, Meldung „Keine neuen passenden Produkte, Beiträge oder Hab-Produktkategorien“.

**Reproduzierte Ursachen im echten Code:** Der Quellkatalog `PPAR_Portal_Source::catalog()` kann WP_Error liefern (fehlender, widersprüchlicher oder nicht zuordenbarer aktiver Kategoriebaum). RC7 verschluckt den Fehler und meldet irreführend keine Kandidaten. Die RC7-Tests verwendeten falsche Kombination Kategoriearchiv mit `product_after_category_tiles`; echte WordPress-Kategorien benutzen `category_recommendation`, die Design-Produktseiten `category_product_1..3`. Bei fehlenden Artikeln konnte die Werbung deshalb unsichtbar bleiben.

**Lokal nachweislich korrigiert:** Statuskasten direkt oben in der vorhandenen WordPress Amazon-Automatik mit Datum, Zahl freigegebener Kategorien, Kostenlimit, offenem Auftrag, echter Kategoriebaum-/API-Fehlerursache; keine bezahlte Suche bei unzulässigem Zielkatalog; Fehlercode/Ende bei abgelehntem DataForSEO Auftrag; vorhandene Design- und Kategorieausgabe für echte autorisierte Produktseiten auch ohne Beiträge; bestehende Werbung und Affiliate-Hauptschalter respektiert. Ein POST pro Kandidat, GET kostenlos zur Bearbeitung desselben Auftrags; Tageslimit 5.

**Prüfung:** 234 positive Prüfaussagen, 25/25 PHP Syntax, ZIP CRC 28/28. Offline-Tests mit echten Original-Plugin-Dateien, eigenem originalen Hab-Kategorieadapter, originalem Main-Router und originalem Design-Hook; simulierte WordPress-Seitendaten/Providerantworten. Kein echter Zugriff auf die produktiven Hab-WordPress-Optionen, keine echte kostenpflichtige DataForSEO-Abfrage, keine Liveabnahme behauptet.

**Nächster Schritt:** Nur nach offizieller Übernahme des geprüften 620242-Byte-ZIP als `HAB-004-AFFILIATE/CURRENT.zip` gilt RC8 als Pluginbüro-Current. Danach in WordPress RC8 installieren und *einmal* auf „Jetzt einen Suchlauf starten“ klicken; obere Statusbox zeigt den verbleibenden konkreten Liveblocker (falls aktiver Hab-Kategoriebaum immer noch nicht verwendbar ist). Wiederholte blinde Klicks vermeiden.
