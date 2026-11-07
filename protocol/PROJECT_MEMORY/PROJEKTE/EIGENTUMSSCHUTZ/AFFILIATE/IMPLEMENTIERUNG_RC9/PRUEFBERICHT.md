# HAB & BEWAHR – HAB-004 RC9: Kategorieabgleich und vollständige lokale Simulation
Datum: 7. November 2026. Plugin: Hab & Bewahr – Affiliate-Zentrale 0.1.6-rc9.

## 1. Tatsächliche Ursache
Das bestehende HAB-004 RC8 verlangte **exakt 6 Hauptwelten**. Das aktuelle Hab-Kategorienbüro dokumentiert neben den sechs bestehenden Schutzwelten die **siebte Hauptwelt „Versicherungen“** (`core:world:insurance`). Diesen Widerspruch bestätigt der Originalcode. In einem unveränderten RC8-Test mit 7 Welten ergibt sich wortwörtlich: `RC8_ORIGINAL_BLOCKER hb_worlds_unexpected Der aktive Hab-&-Bewahr-Bestand muss sechs Schutzwelten enthalten.`

Der Nutzer-Screenshot vom 7.11.2026 zeigt außerdem 2.720 Knoten und 2.714 Zuordnungen im aktiven Katalog. Die aktive WordPress-Datenbank wurde hier nicht ausgelesen; diese Zahlen stammen aus dem sichtbaren Backendstatus. Es liegt daher kein Beweis vor, dass die Produktionsseite tatsächlich alle sieben Weltobjekte enthält, aber der Widerspruch zwischen kategorienseitiger Planung und starrer Affiliate-Prüfung ist belegt.

## 2. Strukturabgleich
Verbindliche Kategoriehierarchie: **Hauptwelt (WordPress-Seite R1) → Schutzbereich (R2) → konkretes Thema (R3) → flache WordPress-Artikelkategorie**. Beispiele aus den vorhandenen Kategorieunterlagen: „Leckwarnung & Absperrung“ → „Wassermelder“, „Brandschutz & Löschmittel“ → „Rauchmelder / Vernetzung“, „Wertsachen & Schadenfall“ → „Tresor & Versicherungsschutz“. Die siebte Welt „Versicherungen“ ist keine Voraussetzung für die Produktrecherche der anderen Welten; sie muss daher ohne geeignete Amazon-Produkte bestehen dürfen.

Der bestehende Katalogadapter wird jetzt **nicht mehr auf exakt sechs Hauptwelten** begrenzt. Er liest die tatsächlich gültig zugeordneten Welten aus dem aktiven Kategorie-Snapshot, ermittelt deren Anzahl dynamisch und bearbeitet nur gültig zugeordnete Kategorien. Eine fehlende einzelne Welt- oder Kategoriezuordnung blockiert den Rest nicht. Das notwendige Sicherheitsverhalten bleibt: Bei fehlendem oder widersprüchlichem **gesamten** aktiven Kategorie-Snapshot werden keine kostenpflichtigen DataForSEO-Abfragen gestartet.

## 3. Umfang der Änderung (KISS)
- Die vorhandene Datei `includes/class-ppar-hab-bewahr-bridge.php` wurde an **einer Stelle** korrigiert: starre 6-Welten-Sperre → Prüfung, dass überhaupt eine gültige Welt vorliegt. Die angezeigten Welt-/Bereichszahlen werden aus der realen Anzahl berechnet.
- Versionsnummer in `affiliate-portal-router.php` und `readme.txt` erhöht.
- **25 von 28 Originaldateien byteidentisch** gegenüber RC8. Keine Datenbank, kein zweites Plugin, kein neues Backend, kein zusätzlicher Cron, keine Änderungen am Kategorieplugin, Designplugin oder an anderen Portalen.
- Der bereits vorhandene Hauptschalter **„Affiliate-Automatik aktiv“** bleibt absichtlich erhalten und wird **nicht** heimlich aktiviert. Ein ausgeschalteter Hauptschalter verhindert weiterhin die sichtbare Werbung; er ist eine **separate Einstellung**, kein Kategoriefehler.

## 4. Ausgeführte Simulationen
**116 bestandene Prüfungen**: vollständiges Original-HAB-004 mit 6, 7 und 8 gültigen Hauptwelten sowie mit einer nicht zugeordneten Versicherungswelt; 2.720 simulierte Knoten, 2.714 Zuordnungen, reale WP-Seitenhierarchie R1→R2→R3→category. Start der bestehenden DataForSEO-Suche, Abruf eines Ergebnisses, ASIN-Prüfung, Speicherung, Amazon-Link mit `habundbewahr-21`, Anzeige über die **vorhandenen** R3-Themenseiten-/Kategorie-Werbeplätze; bestehende Werbung hat Vorrang. Auch Entwürfe, globale Deaktivierung, fehlender Gesamt-Snapshot, falsche Revision und Kategorie ohne Produktthema wurden geprüft.

**104 bestandene Prüfungen**: siebte Hauptwelt bei DataForSEO-POST und GET, offenem Auftrag, HTTP-403, abgelehntem Auftrag, fehlgeschlagenem GET, geeignetem Beitrag und ungültigem Katalog. Keine doppelte kostenpflichtige Suche beim Nachfragen eines offenen Auftrags.

**96 bestandene Prüfungen**: bisherige Amazon-/RC5-/RC6-/RC7-Regressionstests vollständig erneut ausgeführt.

**Zusammen: 316 bestandene funktionale Einzelprüfungen, 0 fehlgeschlagen, 0 PHP-Warnungen**. Zusätzlich 25/25 PHP-Syntaxprüfungen und ZIP-Integrität 28/28. Original-RC8-Fehler separat reproduziert und dokumentiert.

## 5. Grenzen des Beweises
Dies ist eine **vollständige lokale Ausführung der tatsächlichen Affiliate-Plugin-Dateien** mit einem aus dokumentierten Kategorien gebauten **simulierten** WordPress-Katalog auf der im Screenshot gezeigten Größenordnung. Es ist **kein** Live-Datenbankabzug von hab-und-bewahr.de und **kein** echter kostenpflichtiger DataForSEO-Auftrag. Reales Provider-Verhalten, WordPress-Installation und öffentliches Design sind damit nicht abschließend bewiesen.

Die bereits im Screenshot gemeldete zweite Sperre **„Affiliate-Zentrale insgesamt ausgeschaltet“** ist unabhängig davon. Sie muss in WordPress ausdrücklich über **Affiliate-Zentrale → Übersicht → Hauptschalter → Affiliate-Automatik aktiv → Einstellung speichern** eingeschaltet werden; die Codeänderung übergeht diese Nutzerentscheidung nicht.

## 6. Lieferung
Vollständige Plugin-ZIP: `HAB_UND_BEWAHR_AFFILIATE_0.1.6_RC9_KATEGORIEN_GEPRUEFT.zip`
Dateien: 28. ZIP-SHA256: `04de5f4492887686c5a224640ffa5e4d64175927186dc3fe7f19d546e0ea4120`.
Der Source-Diff, die vier ursprünglichen Regressionstests und die beiden neuen integrierten Simulationen liegen in den separaten Testbelegen.