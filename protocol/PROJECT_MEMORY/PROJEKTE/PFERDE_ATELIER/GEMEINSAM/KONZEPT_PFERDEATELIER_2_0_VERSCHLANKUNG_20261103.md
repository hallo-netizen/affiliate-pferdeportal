# Pferdeatelier 2.0 – Verbindliches Gesamtkonzept und Arbeitsfahrplan

**Stand: 04.11.2026 | Status: Arbeitsauftrag / Fahrplan, keine Installationsfreigabe.**

**Ein Satz:** Wir behalten die heutige Website in **jedem sichtbaren und fachlichen Detail**, ersetzen nur die überladene Technik und entfernen jede nachweislich unnötige Funktion. Die Arbeiten laufen ausschließlich auf der getrennten Testinstallation. **K0 und LIVE bleiben unverändert.**

## 1. Zielvertrag – unverhandelbar

- **Frontend unverändert:** Logo, Header, Footer, Schriften, Farben, Abstände, Bilder, Navigation, Hover, Buttons, Kacheln, Tabellen, Suche, Desktop und Mobil. Kein neues Design, keine neue inhaltliche Schablone.
- **Alle Daten und Adressen bleiben erhalten:** veröffentlichte Seiten, Kategorien, Beiträge, Magazininhalte, FAQ, Glossar, Pferderassen, Anzeigen, Affiliate-Produkte/Banner/Textlinks, Bilder, Menüs, Formulare, URLs, SEO und vorhandene Verknüpfungen. Alte Papierkorbinhalte nicht unbeabsichtigt veröffentlichen.
- **Alle Funktionen bleiben erhalten:** HivePress, Suchwege, Nutzerkonten, Affiliate-Aktualisierung, Redaktion, Produktionsübergaben, Tabellen, E-Mails, Datenschutz und Wartung. Auf der Testseite dürfen keine echten externen Schreib-, Import-, Zahlungs-, Mail- oder Produktionsaktionen ausgelöst werden.
- **Astra und Kubio sollen in der endgültigen Installation wegfallen**, aber erst nachdem alle ihre heutigen sichtbaren Aufgaben nachweislich 1:1 durch die zentrale schlanke Designbasis übernommen sind.
- **K0 bleibt exklusiv für das Pferdeatelier aktiv, unverändert und physisch/logisch getrennt.** K1–K9 sind Archiv, keine Ausweichroute. An K0, LIVE und ihren Daten wird für dieses Projekt nichts verändert.
- **Extreme Verschlankung mit KISS:** je Funktion ein eindeutiger Verantwortlicher, keine doppelten Such-/Backup-/Bild-/Designwege, keine dauerhaften Test-/Importer-/Diagnose-Plugins, keine unnötige Zusatzsoftware oder neuer Monolith.
- **Keine Behauptung ohne Beleg:** Quellprüfung ≠ WordPress-Test ≠ 1:1-Frontendtest ≠ Produktionsfreigabe. Ein fehlender Test bedeutet STOP, nicht Erfolg.

## 2. Verifizierter Ausgangsstand und offene Punkte

| Bereich | Belegt | Offen für die Zielinstallation |
|---|---|---|
| LIVE-Plugins | WordPress-Bericht vom 03.11.: **46 aktiv, 3 inaktiv = 49**. Hochgeladene `plugins.zip`: **58 Pluginordner** inkl. älterer Kopien und neuerer Teststände. | Verbindliche Auswahl pro Funktion aus Quellcode und echtem Funktionsnachweis. |
| Design | LIVE: **Astra 4.14.2, Kubio 2.9.5, Template Kit 1.50.613**. Theme-Kandidat `pferdeatelier-core 0.1.0-test` ist **gesperrt**. | Exakte Identität auf Mobil/Desktop, Originalmenüs, Footer, Logo und Kubio-Seiten. |
| Seiten | Originalexport: **424 veröffentlicht**, 1 Entwurf, 1 Papierkorb. Testseite zuletzt vom Betreiber: **423 Seiten**. | Fehlende Seite anhand von Quell- und Zielbestand bestimmen; keine Seite manuell raten. |
| Artikel | Original: **163 veröffentlicht**, 19 im Papierkorb. Testseite: **163** gemeldet. | Inhalte, interne Links, Anhänge und Beitragsmetadaten stichprobenartig und systematisch abgleichen. |
| Kategorien | Original: **1.176**. Testseite: **1.177** gemeldet. | Zusatzkategorie anhand Name/Slug/ID nachvollziehen, nicht blind löschen. |
| Seitentexte | **398** veröffentlichte Seiten haben den Einleitungstext in `_pftk_category_intro_text`; **410** haben keinen normalen Seiteninhalt. | Der neue Renderer muss diese gespeicherten Texte exakt wie bisher ausgeben. |
| Kubio | **9 veröffentlichte Seiten** haben Kubio-Blöcke (u. a. Startseite, Impressum, AGB, Datenschutz, Preise, Werbeseiten, Deckengurte). | Alle Blöcke ohne Kubio optisch und funktional gleichwertig darstellen. |
| Fachinhalte | Im Originalexport: **2.857 Affiliate-Kampagnen, 196 Pferderassen, 184 Glossareinträge, 55 Anzeigen**. | Diese **3.292 Datensätze** waren im ersten Testimport ausgeschlossen. Erhalten samt Feldern, Beziehungen und Bildern. |
| Navigation | Original: **1.616 Menüeinträge**, darunter 1.582 im großen Hauptmenü; 413 auf den bisher betrachteten oberen 3 Ebenen. | Kein Abschneiden der übrigen Menüdaten; Originalzuordnungen übernehmen und visuell prüfen. |
| Medien | Original-WXR: **459 Medieneinträge**, 450 WebP und 9 JPG. Betreiber hat den Ordner `uploads/2026` auf TEST kopiert; **ein Testbild ist erreichbar**. | Vollständiger Medien-/Bildreferenz- und Bildzuordnungsabgleich; Vorhandensein einer Datei ist kein vollständiger Mediathek-PASS. |
| Einstellungen | WXR enthält **nicht** alle Theme-/Plugin-/Formular-/Benutzer-/Widget-/Cron-Konfigurationen. | Nur tatsächlich notwendige Konfigurationen kontrolliert übernehmen, statt die alte Installation vollständig zu klonen. |
| Performance | Vorliegende Speicheranalyse, Website-Bericht und frühere Diagnose. | Vergleichbare echte Vorher-/Nachhermessungen für LIVE-Referenz und TEST auf mehreren Seitentypen. |

**Wichtig:** Die WordPress-Zahlen sind die letzte belegte Momentaufnahme; sie sind keine Behauptung über zwischenzeitliche Änderungen. Die Plugin-ZIP enthält auch **nicht freigegebene** Teststände (beispielsweise Themenengine 0.57.144.8 vs. LIVE 0.57.120; Compiler 0.28.53 vs. LIVE 0.28.43; Affiliate 6.72.300 vs. LIVE 6.72.298). Diese dürfen nicht still zur Produktionsgrundlage werden.

### Bereits konkret bewiesene Fehler am ersten Theme-Kandidaten

1. Menüfilter zeigt bei fehlender Hauptseite **nur 1 statt 413** Einträge; bei fehlender Unterseite 412 statt 413 ohne Fehlermeldung.
2. Das Theme schreibt beim Aktivieren selbst zusätzliche Menü-/Optionsdaten.
3. Footer und Logo werden teils nachgebaut; der Betreiber sah eine **Logoabweichung**.
4. CSS-Größen und Abstände wurden neu gesetzt, **nicht** aus dem Original nachgewiesen.
5. Das originale Designplugin wurde praktisch **nicht verschlankt**; ein kleines Theme allein beweist keine Performanceverbesserung.
6. Fehlende 3.292 Fachobjekte, 9 Kubio-Seiten und keine gemessene Gesamtfunktion.

**Folge:** Die bestehende `pferdeatelier_core_nur_test_20261103.zip` bleibt **gesperrt**. Nicht als neue Freigabebasis oder Baustein für ein blindes weiteres Paket verwenden.

## 3. Technisches Zielbild – klein und eindeutig

**WordPress bleibt unverändert.** Eine schlanke zentrale Designbasis übernimmt den **bereits bestehenden** sichtbaren Aufbau. Fachfunktionen bleiben nur dort eigenständig, wo sie notwendig sind: Affiliate, HivePress-Anzeigenmarkt, SEO/Redaktion, K0-Schnittstellen, Bilder, Glossar, Pferderassen und Produktwissen. Einheitliche Seitenausgabe statt vieler paralleler Eingriffe. Im Backend bleiben nur die tatsächlich benötigten Bedienpunkte.

Das ist **kein** neues Gestaltungssystem und **kein** Komplettimport der alten 49 Plugins. Der Inhalt und das Verhalten bleiben gleich; Code, Datenbankarbeit, Ladeverhalten und Pluginanzahl werden an der Ursache vereinfacht.

## 4. Verbindlicher Fahrplan – streng nacheinander

| Schritt | Wer / Arbeit | Muss am Ende nachweislich stimmen | Sonst |
|---|---|---|---|
| **0. Ausgangszustand einfrieren** | **Ich:** Belege, ZIPs, XML, Versionsgrenzen und Sperrbericht bündeln; bestehendes TEST-Theme als Fehlkandidat markieren. **Du:** nichts installieren. | Eine widerspruchsfreie LIVE-Referenz, getrennte TEST-/LIVE-Versionen, keine Eingriffe in LIVE/K0. | STOP. |
| **1. Daten und Einstellungen vollständig herstellen** | **Ich:** Original-WXR und Originalcode für Datenfelder, Fachtypen, URLs, Links, Menüs, Bildreferenzen und Formulare auswerten; geprüften Übertragungsweg vorbereiten. **Auf TEST:** fehlende Inhalte kontrolliert übernehmen. | Exakt 424 veröffentlichte Seiten, 163 veröffentlichte Artikel, 1.176 Quellkategorien bzw. jede Abweichung ausdrücklich geklärt, alle 3.292 Fachobjekte, echte Navigation, Medien-/Feldzuordnungen, keine doppelten Datensätze. | Kein Design- oder Plugin-Freigabepaket. |
| **2. Unveränderliche Frontend-Referenz festhalten** | **Ich:** Originalseiten nach Seitentyp vergleichen: Start, Hub, Kategorien, Magazin, Beiträge, 9 Kubio-Seiten, Glossar, Rassen, Anzeigenmarkt, Formulare, Suche, Menüs, Footer; Desktop und Mobil. | Eine genaue Soll-Liste der bestehenden Darstellung, Interaktionen und URLs. Kein gestalterischer Spielraum. | Fehlende Vorlage erst belegen; niemals schätzen. |
| **3. Astra/Kubio gezielt technisch ablösen** | **Ich:** Altes Design-Plugin anhand der realen Codepfade entflechten, vorhandene Layout- und CSS-Ausgaben 1:1 zentralisieren; ursprüngliche Einstellungen, Logo/Footer/Menüs übernehmen; Kubio-Blöcke funktionsgleich ersetzen. | Auf vollständig befülltem TEST sieht und arbeitet jeder Seitentyp wie LIVE. Keine Funktion benötigt mehr Astra/Kubio. Menü-Negativfälle werden sicher abgefangen. | Bestehendes Theme als TEST-Rückweg behalten; STOP. |
| **4. Plugin für Plugin radikal reduzieren** | **Ich:** Alle **49 LIVE-Einträge** und **58 ZIP-Quellordner** einzeln in Behalten / Zusammenlegen / Entfallen / nur während Import / offen einordnen, tatsächliche Funktionsaufrufe und Daten nachweisen. Auf TEST jeweils nur eine unnötige Zuständigkeit entfernen. | Keine Funktion doppelt, keine nötige Funktion weg; weniger dauerhafte Plugins, Hooks, Backend-Menüs und Hintergrundaufgaben. | Letzte funktionierende TEST-Konfiguration wiederherstellen. |
| **5. Performance an der Ursache verbessern** | **Ich:** überflüssige CSS/JS-Ausgaben, doppelte Abfragen, langsame Menü-/Produktlisten, Bildvarianten, Caches, Hintergrundjobs und Datenbank-/Backup-Reste prüfen. | Messbar weniger unnötige Last; identisches Frontend; keine Verschlechterung der Bildqualität oder Fachfunktion. | Maßnahme rückgängig und Ursache erneut bestimmen. |
| **6. Vollständige Endabnahme** | **Ich:** Ein gemeinsamer Positiv-, Negativ-, Browser-, Mobil-, SEO-, Funktions-, Daten- und Lasttest auf TEST, mit originalen Daten und realem WordPress. | **Alle** verbindlichen Prüfpunkte PASS; keine unbekannten Unterschiede. Vorher/Nachhermessung vorhanden, Wiederherstellung getestet. | Keine Freigabe, keine neue LIVE-Datei. |
| **7. Kontrollierte Umstellung** | **Erst nach Freigabe:** frische LIVE-Daten seit dem letzten Export sicher ergänzen, Vollbackup und Rückspieltest, geplanter Domainwechsel; Schreibjobs/Importe nicht doppelt starten. | LIVE sieht aus wie zuvor, alle URLs/SEO/Produkte/Inserate/Formulare laufen, Monitoring und Rückweg funktionieren. | Sofortiger Rückweg, keine Improvisation am Produktivsystem. |
| **8. Nachkontrolle und endgültig aufräumen** | **Ich:** Messergebnisse, Indexierung, Fehlprotokolle, geplante Jobs, Bilder, SEO und Pluginbestand erneut vergleichen. | Ein schriftlich nachvollziehbarer Abschlussstand inkl. verbleibender notwendiger Plugins. | Fehler ursächlich beheben, nicht nur Symptome verdecken. |

### Die Reihenfolge wird nicht verändert

**Keine Verschlankung vor Datensicherheit. Kein Designwechsel vor Originalvergleich. Keine Plugin-Löschung vor Funktions-/Abhängigkeitsbeweis. Kein neues Installationspaket vor bestandenem lokalem Test. Kein LIVE-Wechsel vor echtem WordPress-Gesamttest.**

## 5. Gemeinsame Prüfliste für jedes spätere Installationspaket

Jede neue Datei muss **vor ihrer Ausgabe** vier Hürden erfüllen:

1. **Vollständigkeit:** Originalquelle und freigegebene Versionsbasis eindeutig. Alle betroffenen Dateien/Seiten/Plugins erfasst. Keine fremden Teststände oder fehlenden Abhängigkeiten.
2. **Lokale Positiv- und Negativtests:** Paketintegrität, Quellvergleich, Syntax, echte Funktionsfälle und Fehlerfälle (fehlende Seiten, leere Menüs, defekte Referenzen, Dubletten, deaktivierte Komponenten). Der frühere 413→1-Menüfehler ist Pflicht-Gegentest.
3. **Gesamtkonzept-Abgleich:** Ändert die Datei Erscheinungsbild, Texte, SEO, Daten, K0, fremde Plugins, Hintergrundaktionen? Nutzt sie dieselbe Funktion ein zweites Mal? Hat sie einen echten Rückweg? Ein NEIN/UNBEKANNT an einer Pflichtstelle sperrt die Datei.
4. **Echte TEST-Abnahme:** Installation in isoliertem WordPress mit vollständigen Inhalten, Funktionen, Browser-/Mobilvergleich und Performancekontrolle. Erst das kann eine spätere Produktionsfreigabe begründen. Ist das Testsystem von hier nicht zugänglich, wird ausdrücklich **kein echter WordPress-PASS behauptet**.

**Eine ZIP, die lediglich entpackt oder deren PHP korrekt geschrieben ist, besteht diese Freigabe ausdrücklich nicht.** Vorbereitete Kandidaten sind von freigegebenen Paketen sichtbar getrennt.

### Pflicht-Funktionsmatrix für die Gesamtabnahme

- **Darstellung:** Startseite; Kopf-/Fußbereich; 3 sichtbare Navigationsebenen und Erreichbarkeit tieferer Ziele; Breadcrumbs; 9 Kubio-Seiten; alle Hub-/Kategorie-/Magazin- und Beitragstypen; Glossar; Pferderassen; Anzeigenmarkt; Desktop/Mobil.
- **Inhalte:** 424 Seiten, 163 Beiträge, 1.176 Quellkategorien, 3.292 Fachobjekte; Einleitungstexte in Metafeldern; Taxonomie- und Bildzuordnungen; Beziehungen; keine Doppelungen/fehlenden Einträge.
- **Affiliate:** Produkte und Banner auf den richtigen Kategorien, keine fachfremden Ausgaben; Textlinks; Klickziele; Kampagnenpflege; Importfortschritt; eBay; Ein- und Ausblendung. Externe Schreibimporte auf TEST bleiben gesperrt.
- **Anzeigenmarkt:** Anzeigen, Kategorien, Suche, Sortierung, Benutzerkonten und tatsächlich genutzte Erweiterungen; keine echten Zahlungen oder Nutzerbenachrichtigungen auf TEST.
- **Suche/SEO:** Suche in Titeln und Texten, passende Ergebniskategorien; URL-Pfade/Permalinks, interne Links, Canonicals, Metadaten, Sitemaps, robots/noindex, strukturierte Daten; TEST bleibt nicht indexierbar.
- **Produktionssystem:** Redaktion, Titel-/Kategoriezuordnung, K0/PPM/SEO-Übergabe nur in isolierten Prüfwegen; keine Veränderung am K0-Original, keine doppelten Cron-Jobs oder automatische Veröffentlichung durch TEST.
- **Formulare/Recht/Betrieb:** WPForms-Inhalte und Shortcodes, Absender/Bestätigung, Impressum/Datenschutz, Cookie-Einwilligung, Login, Backups und Wiederherstellung.
- **Performance:** gleiche Seiten und Bedingungen, Mobil/Desktop, mehrfach wiederholt; reale Ladezeiten, Anzahl/Größe übertragener Dateien, Browser-/Server- und Datenbanklast, Bildgrößen und Hintergrundprozesse. Keine unbelegte Beschleunigungsbehauptung.

## 6. Plugin-Entscheidungen – vollständige LIVE-Liste

**Diese 49 Zeilen stammen aus dem belegten LIVE-Systembericht vom 03.11.2026.** Die rechte Spalte benennt den **noch erforderlichen Test** – sie ist bewusst keine vorschnelle LIVE-Löschfreigabe. Für den vollständigen ZIP-Quellordner-Abgleich gelten zusätzlich die 58 Positionen des vorhandenen Quellprüfberichts. Alte Parallelkopien `hivepress-messages-x`, `hivepress-paid-listings-x`, `hivepress-reviews-x` werden **nicht** in die neue Installation übernommen.

| Nr. | Plugin (LIVE) | Version / Status | Zielentscheidung vor Funktionstest | Entscheidender Nachweis |
|---:|---|---|---|---|
| 1 | Affiliate-Zentrale (Portal-kompatibel) | 6.72.298 / Aktiv | Erhalten | Importe, Produkt-/Banner-/Textlinkausgabe, Klickziele, Zeitpläne, eBay-Status, sichere TEST-Sperren |
| 2 | Affiliate Portal Template Kit (Pferde-kompatibel) | 1.50.613 / Aktiv | Technisch ersetzen | Alle sichtbaren Ausgaben 1:1; Astra-/Kubio-Abhängigkeiten und doppelte Ausgaben entfernen |
| 3 | Akismet Anti-spam: Spam Protection | 5.7.2 / Aktiv | Nutzung klären | Prüfen, ob Kommentare oder Formulare diesen Schutz tatsächlich nutzen |
| 4 | All-in-One WP Migration and Backup | 7.113 / Aktiv | Backup zusammenlegen | Nur eine geprüfte aktive Sicherungsstrategie und funktionierende Wiederherstellung |
| 5 | Allgemeine Bildzentrale | 2.7.6 / Aktiv | Erhalten | WebP-Quelle, Größen, Uploadregeln, Hero-Bilder und Start-/Kategorie-/Artikelbilder |
| 6 | Canonical Table Contract V1 | 1.1.0 / Aktiv | Erhalten bis Abgleich | Tatsächliche K0-/Tabellen-/Design-Abhängigkeit prüfen, nicht still verändern |
| 7 | CookieYes / GDPR Cookie Consent | 3.5.8 / Aktiv | Erhalten | Einwilligung, Cookie-Blockade, Einstellungen und Banner 1:1 |
| 8 | DBStorage Insights | 1.2.0 / Aktiv | Später weglassen | Reines Diagnosewerkzeug; nach Abschluss der Messung weglassen |
| 9 | HivePress | 1.8.1 / Aktiv | Erhalten | Anzeigen, Kategorien, Benutzerrollen, Suche und Frontend |
| 10 | HivePress Authentication | 1.1.5 / Aktiv | Nutzung klären | Benutzeranmeldung und Kontofunktionen testen |
| 11 | HivePress Claim Listings | 1.1.5 / Aktiv | Nutzung klären | Übernahme/Beanspruchung von Anzeigen nachweisen |
| 12 | HivePress Favorites | 1.2.2 / Aktiv | Nutzung klären | Favoriten samt vorhandenen gespeicherten Daten prüfen |
| 13 | HivePress Paid Listings | 1.1.10 / Aktiv | Nutzung klären | Zahlungs-/Paketwege und Angebotszuordnung ohne echten TEST-Kauf prüfen |
| 14 | HivePress Reviews | 1.4.1 / Aktiv | Nutzung klären | Bewertungen/Anzeigenbezug und aktive Frontendausgabe prüfen |
| 15 | Kubio | 2.9.5 / Aktiv | Nach Ersatz entfallen | Neun Kubio-Seiten und sämtliche Formatierungen 1:1 ersetzen, dann keine aktiven Bausteine mehr |
| 16 | Performance Diagnose Safe | 3.0.0 / Aktiv | Später weglassen | Nach nachvollziehbaren Vorher-/Nachhermessungen entfernen |
| 17 | Pferde Atelier Editorial Guard | 0.1.1-quarantine / Aktiv | Erhalten bis Abgleich | Bestehende Veröffentlichungssperren/K0-Schutz unverändert nachweisen |
| 18 | Pferde Atelier Glossar Core | 1.4.0 / Aktiv | Erhalten | 184 Glossareinträge, Verknüpfungen, Suche und Vorlagen |
| 19 | Pferde Atelier HivePress Anzeigensuche | 2.1.5-ajax-category-label / Aktiv | Suche zusammenlegen | Mit 1.0.1 und HivePress-Suche vergleichen, genau einen sichtbaren Anzeigenmarktweg |
| 20 | Pferde Atelier Mail-Absender | 1.0.0 / Aktiv | Erhalten bis Abgleich | Absenderadresse und E-Mail-Ausgaben, keine Testmails an LIVE-Adressen |
| 21 | Pferde Atelier – Anzeigenmarkt & Journal Breadcrumbs | 1.1.1 / Aktiv | Design zusammenlegen | Breadcrumb-Verhalten unverändert zentral im Design bereitstellen |
| 22 | Pferdeatelier – eBay Ursachencheck (nur lesen) | 1.0.0 / Aktiv | Später weglassen | Nach Ursachenanalyse und Bedarfsklärung nicht dauerhaft betreiben |
| 23 | Pferde Atelier – HivePress Anzeigensuche | 1.0.1 / Aktiv | Suche zusammenlegen | Mit 2.1.5 überlappende Kategorienseiten-/AJAX-Darstellung vergleichen |
| 24 | Pferde Atelier – Komplettsicherung | 2.1.1 / Aktiv | Backup zusammenlegen | Wöchentlichen eigenen Sicherungslauf nachweislich ersetzen und Rückweg belegen |
| 25 | Pferde Atelier – Pferderassen Manager | 0.2.6 / Aktiv | Erhalten | 196 Rassen, Beziehungen, Bilder, Navigation und Ausgabe |
| 26 | Portal Production Center | 1.1.1 / Aktiv | Erhalten | Produktionskoordination nur nach K0-Isolationsprüfung |
| 27 | Portal Production Link Policy Gate | 1.0.1 / Aktiv | Erhalten | Linkregeln und Negativsperren nicht verändern |
| 28 | Portal Production Machine | 6.7.9 / Aktiv | Erhalten | K0-Anbindung, Artikelübergabe, Produktions-Sperren; kein TEST-Job auf LIVE |
| 29 | Portal SEO Redaktionsplan Compiler | 0.28.43 / Aktiv | Erhalten | Freigegebene LIVE-Quelle vs. neue Testversion streng trennen |
| 30 | Portal SEO Themenengine | 0.57.120 / Aktiv | Erhalten | Kategorien, Magazine, Titelzuordnung, Redaktionsplanung unverändert |
| 31 | Relevanssi | 4.28.8 / Aktiv | Suche prüfen | Inhaltssuche inkl. Titel und Taxonomien; Ergebnisqualität und Ladezeit |
| 32 | Relevanssi Live Ajax Search | 2.6 / Aktiv | Suche prüfen | Suchtipp-AJAX vs. Relevanssi-Index: getrennte Funktion oder Dublette? |
| 33 | Reveal IDs | 1.6.3 / Aktiv | Später weglassen | Nur Backend-Anzeigehilfe; keine notwendige Produktionsfunktion |
| 34 | SEO-Quellpaket Exporter | 1.0.0 / Aktiv | Später weglassen | Nur notwendige finale Exportnachweise, dann nicht dauerhaft |
| 35 | Shortcodes Ultimate | 7.9.2 / Aktiv | Nutzung klären | Verwendete Shortcodes in echten Seiten/Artikeln vollständig suchen |
| 36 | Single Sign-On | 2.3.2 / Aktiv | Nutzung klären | IONOS-Login und Admin-Zugangsweg ohne Aussperren abgleichen |
| 37 | Site Kit by Google | 1.191.0 / Aktiv | Nutzung klären | Analytics/Search Console/Tag-Ausgabe gegen Datenschutz und Doppeltracking prüfen |
| 38 | Universal Product Comparison | 0.8.5-prototype / Aktiv | Erhalten bis Abgleich | Bestehende Vergleiche und Product-Knowledge-Abhängigkeit nachweisen |
| 39 | Universal Product Knowledge | 0.5.1-prototype / Aktiv | Erhalten bis Abgleich | Produktdatenbasis, Relation und Comparison-Anbindung |
| 40 | Universal Research & Fill | 1.9.9 / Aktiv | Erhalten bis Abgleich | Echter Verbrauch durch Fachabläufe; keine blinde Löschung |
| 41 | WordPress Importer | 0.9.7 / Aktiv | Nach Migration weglassen | Erst nach vollständiger Datenübernahme und Abnahme |
| 42 | WordPress Speicheranalyse | 1.1.0 / Aktiv | Nach Diagnose weglassen | Nach protokollierter Speicherprüfung entfernen |
| 43 | WP-Optimize - Clean, Compress, Cache | 4.7.0 / Aktiv | Optimierung prüfen | Tatsächliche Datenbank-/Cache-/Bildfunktionen, Überschneidungen und Hostwirkung |
| 44 | WPForms Lite | 2.0.3.1 / Aktiv | Erhalten bis Abgleich | Alle Formulare, IDs, Shortcodes, E-Mail-/Bestätigungstests |
| 45 | WPvivid Backup Plugin | 0.9.139 / Aktiv | Backup prüfen | Mindestens eine nachweislich funktionierende Sicherung und Rückspielung behalten |
| 46 | Yoast SEO | 28.8 / Aktiv | Erhalten | Metadaten, Canonicals, Sitemaps, Indexierung, strukturierte Daten |
| 47 | HivePress Geolocation | 1.3.11 / Inaktiv | Inaktiv; Wegfall prüfen | Daten/Ortsfilter/Abhängigkeit vor Nichtübernahme prüfen |
| 48 | HivePress Messages | 1.4.1 / Inaktiv | Inaktiv; Wegfall prüfen | Nachrichtenverläufe oder Login-Abhängigkeiten vor Nichtübernahme prüfen |
| 49 | Pferdeatelier – Affiliate Einzelbeitrag Diagnose (nur lesen) | 1.0.0 / Inaktiv | Inaktiv; weglassen prüfen | Nach Fertigstellung der Prüfung nur als getrenntes Werkzeug behalten |

## 7. Keine Zusatzforderungen / exakter nächster Arbeitsauftrag

**Jetzt macht der Betreiber nichts.** Weder Plugin noch Theme installieren, nichts löschen, keine weiteren pauschalen Komplett-Exporte. Das vorhandene TEST-Theme bleibt ein gesperrter Kandidat; die bereits laufende LIVE-Installation ist die Referenz.

**Meine nächste Arbeit ist Schritt 1:** Die **vorhandenen** Originaldaten (WXR, komplette Plugin-ZIP, Speicher-/Website-Bericht und Campus-Fachquellen) gegen die bereits importierten Datentypen und die Designabhängigkeiten abgleichen; daraus die **eine geprüfte Reihenfolge der notwendigen Daten-/Einstellungsübernahme** ableiten. Erst wenn dafür ein tatsächlicher fehlender Nachweis aus dem geschützten Test-WordPress notwendig wird, benenne ich **genau diesen** statt weiterer Vermutungen. Eine Datenbank- oder Adminzugriffsprüfung kann ich aus ZIP und XML allein nicht ersetzen.

**Jeder Schritt wird abgeschlossen, geprüft und protokolliert, erst dann folgt der nächste.** Das Programm ist ein Ziel- und Arbeitsplan, **keine Erklärung, dass alle offenen Tests bereits bestanden seien.**

## 8. Quellen und Zuständigkeit

- Originaldateien des Betreibers: `pferdeatelier.WordPress.2026-11-03.xml`, `plugins.zip`, `wordpress-speicheranalyse-20261103-114349.json`, LIVE-WordPress-Systembericht `Eingefügter Text.txt`.
- Lokale Prüfungen: `pferdeatelier_plugin_pruefung_20261103.md`, `pferdeatelier_plugin_liste_20261103.csv`, `pferdeatelier_theme_sperrbericht_20261103.md`.
- Im Campus: `PLUGINS/REGISTER.md` mit LIVE-Snapshot vom 03.11.; `PLUGINS/CURRENT_STATE.md` und `PLUGINS/EVIDENCE/PFERDEATELIER_CORE_THEME_010_TESTBLOCKER_20261103.md` im geprüften Stand `qa/pferdeatelier-abschluss-audit-20261103`. Fachliche Freigaben stammen nur aus den jeweiligen zuständigen CURRENT-/Releasequellen, niemals aus einem älteren PPA-Registereintrag.
- Zielvertrag/Regeln: `protocol/PROJECT_MEMORY/ZIELVERTRAEGE/REGISTER.md`; K0 `konzept0-portal-neutral-20261002:K0_GOAL_CONTRACT.json`; keine neue K0-Fassung.
- **Dieses Dokument ist der eine operative, fachübergreifende Fahrplan.** Es ersetzt die früheren schrittweisen Einzel-Anweisungen zum Neubau; die bisherigen Protokolle bleiben über die Git-Historie nachvollziehbar. Es **überschreibt nicht** die einzelnen Fach-CURRENT- und Release-Autoritäten.
## Fortschritt zu Schritt 1 – Quell- und Zuordnungsprüfung 08.11.2026

**Read-only; keine Veränderung an LIVE, K0 oder TEST.** Durch Parser-/Quellcodeprüfung des WordPress-Originalexports, der bereits erstellten Importpakete und des in `plugins.zip` mitgelieferten WordPress-Importers nachgewiesen:

- WXR: **424 veröffentlichte Seiten, 163 veröffentlichte Beiträge, 1.176 normale WordPress-Kategorien, 459 Medieneinträge**.
- Im vorhandenen Importpaket 01 **nicht enthalten:** 2.857 Affiliate-Kampagnen, 196 Pferderassen, 184 Glossareinträge, 55 Anzeigen, außerdem ein HivePress-Anbieter und eine HivePress-Anzeigenfeld-Definition; **3.294 Fachobjekte insgesamt**. Damit sind die bisherigen **3.292 Fachinhalte plus zwei technische Datensätze** präzisiert.
- **1.616 Menüpunkte in sieben Menüs:** 424 verweisen auf Seiten, 1.179 auf normale WordPress-Kategorien, 13 sind individuelle Links. Alle 1.603 Zielverweise und alle 1.574 verwendeten übergeordneten Menüverweise sind in der Original-XML auflösbar. Das frühere Abschneiden auf 413 Punkte ist **nicht zulässig**.
- Die Original-XML enthält **140 zusätzliche Taxonomie-/Menüeinträge**, die in den bisherigen Importpaketen nicht enthalten sind: 92 HivePress-Anzeigenkategorien, 35 Glossargruppen, sechs Rassengruppen, sieben Menüs. Eine Glossargruppe `pferd-biologie` steht unter zwei unterschiedlichen Original-IDs (1534, 1535), also **139 unterschiedliche Taxonomie-/Slug-Paare**. Keine Dublette ohne Prüfung entfernen oder neu erzeugen.
- Sämtliche **196 Rassen- und 163 Beitrags-Vorschaubilder**, drei Seiten-Vorschaubilder und 20 HivePress-Kategoriebilder referenzieren valide in der Original-WXR vorhandene Anhänge. Alle 55 Anzeigen verweisen auf den einen Original-HivePress-Anbieter.
- **Technischer Befund aus dem wirklich mitgelieferten WordPress-Importer:** Er hält die Alt-/Neu-ID-Zuordnungen für Bilder, Elternseiten und Menüs **nur während des jeweiligen Einzeldurchgangs** vor. Getrennte unkontrollierte Nachimporte sind deshalb keine beweisbare sichere Zuordnungsreparatur. Er braucht außerdem die registrierten Spezial-Inhaltstypen. Vorher keinen weiteren Import starten.
- **Externe Zustandsgrenze:** WXR und PHP-Quellen liefern **keinen** aktuellen Überblick über die tatsächlichen Einträge und IDs in der TEST-Datenbank und enthalten keine vollständigen LIVE-Formular-, Widget-, Benutzer- und Plugin-Einstellungen.
- **Kontrolltests ausgeführt:** Quell-WXR gegen sich selbst ergibt null Abweichungen. Negativtest Quell-WXR gegen Basisimport 01 erkennt exakt die sechs oben genannten fehlenden Fachtypen ohne erfundene fehlende Standardkategorien/Seiten/Artikel/Bilder. Diese Tests beweisen Dateiinhalte, nicht den realen Testseitenzustand.

**Nächster notwendiger, genau einmaliger Betreiber-Schritt für die exakte Differenzprüfung:** **nur auf der separaten TEST-Seite** unter **Werkzeuge → Daten exportieren → Alle Inhalte** die aktuelle XML herunterladen und hier bereitstellen. Damit kann die Assistenz **die eine fehlende Seite, die eine zusätzliche Kategorie, die tatsächlich vorhandenen Fachdatensätze und eventuelle Bild-ID-Abweichungen** durch direkten Alt-/Neu-Exportvergleich identifizieren und anschließend den minimal sicheren Import-/Reparaturweg erstellen. Vorher keine weitere XML oder Plugins installieren und nichts auf LIVE verändern. Der vom Betreiber bereits übertragene Ordner `uploads/2026` bleibt bestehen.

**Prüfprotokoll:** `pferdeatelier_schritt1_quellpruefung_20261108.md` (Gesprächsdatei). Es ist ein Nachweis für **Schritt 1**, kein zweites Konzept und keine Installationsfreigabe.

## Schritt 1 – vollständiger Alt-/Neu-WXR-Abgleich 09.11.2026

**Quellen wirklich vollständig verglichen:** LIVE-WXR `pferdeatelier.WordPress.2026-11-03.xml` (37.572.355 Bytes) und vom Betreiber aus der isolierten TEST-Website exportiertes WXR `pferdebackup.WordPress.2026-11-09.xml` (9.507.997 Bytes). Read-only XML-Gegenprobe, kein WordPress-/LIVE-/K0-Eingriff.

**BELEGT:**
- 424 veröffentlichte Seiten Original, 423 TEST. Fehlend ist **Original-ID 283**, Slug `weide-zauntechnik-weidezaungeraete`, Titel **Weidezaungeräte**, Parent 123 **Zauntechnik**; alle 423 vorhandenen Seiten haben denselben Inhalt/Slug/Status/Eltern-ID wie das Original.
- Exakte Root Cause: Originalseiten 282 und 283 haben **identischen Titel, `post_date=2026-06-20 11:05:42` und Typ `page`**, aber zwei unterschiedliche Slugs und Intro-Metafelder. Die TEST-Seite 282 enthält beide Original-Einleitungen als **doppelt gespeicherte** `_pftk_category_intro_text`- und `_pftk_category_intro_source`-Metafelder; ID 283 fehlt. Der tatsächlich hochgeladene Importer-Code `plugins/wordpress-importer/class-wp-import.php` nutzt `post_exists($post['post_title'], '', $post['post_date'], $post['post_type'])`. Daher wäre unveränderter Wiederimport falsch.
- 163/163 veröffentlichte Beiträge vollständig, sämtliche 163 `post_content` exakt gleich; bei zwei Beiträgen ist die ursprüngliche Bildreferenz `_thumbnail_id` im TEST nicht vorhanden.
- 1.176/1.176 Original-Beitragskategorien, alle Namen/Slugs/Eltern/Metafelder exakt, 1.177 im TEST wegen zusätzlicher **regulärer WordPress-Standardkategorie „Allgemein“**. Nicht als fehlerhafte Dublette löschen.
- Medien-Datenbankeinträge: **459 → 270**, genau **189 fehlen** (140 aus 2026/09, 47 aus 2026/10, je 1 aus 2026/07 und 2026/08). Die 270 vorhandenen Einträge sind nach Datei**pfad und ID** mit dem Original identisch. Physische Bilddateien sind durch XML allein nicht nachgewiesen.
- Fachobjekte **3.294 fehlen:** 2.857 `ap_campaign`, 196 `pa_breed`, 184 `uge_term`, 55 `hp_listing`, je ein `hp_vendor` und `hp_listing_attribute`. **140** spezielle Taxonomie-/Menüdefinitionen fehlen (92 `hp_listing_category`, 35 `uge_group`, sechs `pa_breed_group`, sieben `nav_menu`). Original **1.616** klassische `nav_menu_item`, TEST **0**. Testseitiger Block-Navigationseintrag ersetzt diese nicht.

**Vorbereitete gezielte 1-Seiten-XML** `pferdeatelier_Seite_283_REPARATUR_NUR_TEST_20261109.xml` (2.760 Bytes, SHA-256 `82c59ad0688abe1b822f40a139fcfbad173a73398c11d119124c3357c60279f1`): enthält nur Original-ID 283, **alle Metafelder, Parent-ID 123, Status `publish`, Original-Slug und Originaldaten unverändert**, ausschließlich vorübergehender eindeutiger Titel `Weidezaungeräte [Import 283 – danach umbenennen]` gegen den bestätigten Importer-Kollisionsmechanismus. Nach TEST-Import den sichtbaren Titel auf Original zurücksetzen. **Statische XML-Struktur-/Quelltest-PASS; echter WordPress-Import noch NICHT ausgeführt**, daher keine Freigabe für LIVE, keine automatische Behauptung eines vollständigen Reparatur-PASS. Doppelte Intro-Metadaten auf Seite 282 separat nach Sicherung gezielt bereinigen.

**Weiterer verbindlicher Weg:** Kein ungefilterter Voll-Reimport und keine ungeprüfte Übernahme der Testplugin-Versionen. Nach exakter Verfügbarkeit/Registrierung aller benötigten benutzerdefinierten Inhaltstypen im TEST die verbleibenden Fachobjekte, Spezialtaxonomien, Medien-ID-Verweise und 1.616 Menüpunkte in abgestimmten Paketen importieren; Bilddateien und Settings verifizieren; vollständigen WXR-Gegenvergleich und realen WordPress-Frontend-Test bestehen lassen. Danach erst Theme-/Plugin-Verschlankung fortsetzen. LIVE/K0 unangetastet.

**Quellen-Prüfprotokoll im Gespräch:** `pferdeatelier_Datenabgleich_20261109.md`; die kleine WXR-Datei ist nur ein TEST-Kandidat. Der aktuelle Arbeitsschritt 1 ist **noch NICHT abgeschlossen**.
