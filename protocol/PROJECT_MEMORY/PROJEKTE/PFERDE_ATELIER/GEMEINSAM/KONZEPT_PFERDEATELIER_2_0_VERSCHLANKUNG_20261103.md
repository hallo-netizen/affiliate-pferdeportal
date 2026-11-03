# Pferdeatelier 2.0 – Konzept zur radikalen technischen Vereinfachung

**Datum:** 03.11.2026  
**Status:** Abgelegter, beauftragter Konzept-/Fahrplan; **keine technische Umsetzung oder Installationsfreigabe**.  
**Ablage:** Pferdeatelier → GEMEINSAM. Fachbüros bleiben für ihre jeweiligen Funktionen zuständig; dies ist kein zweiter technischer CURRENT-Stand.

## 1. Ziel und Grenzen

Pferdeatelier auf WordPress-Basis technisch neu und möglichst schlank aufsetzen. Weniger unnötige Plugins und technische Schichten, übersichtliches Backend, zentral gesteuertes Design, bessere messbare Performance und langfristig wartbare Struktur.

**Unverhandelbar:**
- Frontend sieht nach der Umstellung **genauso aus wie bisher**, auch mobil.
- **Keinerlei Änderung** an Texten, Bildern, Kategorien, Navigation, URLs, SEO-Inhalten, Affiliate-Daten oder bestehenden Beiträgen.
- **Keine Funktion geht verloren**: insbesondere Anzeigenmarkt/HivePress, Affiliate, Suche, Formulare, Glossar, Pferderassen, Bilder, Redaktion/Produktion und automatisierte Abläufe.
- **K0 bleibt vollständig unverändert und technisch getrennt**; kein Rückgriff auf K1–K9.
- Keine Experimente, Löschungen, Theme- oder Plugin-Wechsel am LIVE-System.
- Kein Neubau einer unnötigen zweiten Verwaltungssoftware; WordPress-Kern unverändert.
- Keine Lösung durch bloßes Aufsetzen weiterer Plugins oder durch einen neuen riesigen Monolithen.

## 2. Verifizierter Ausgangspunkt (Stichtag 03.11.2026)

WordPress-Website-Zustandsbericht des Betreibers:
- 46 aktive, 3 inaktive Plugins.
- Astra 4.14.2, Kubio 2.9.5 und Affiliate Portal Template Kit 1.50.613 aktiv.
- Plugin-Verzeichnis 10,63 GB; Datenbank 1,11 GB.
- Aktuelle LIVE-Versionen laut diesem Bericht: Affiliate-Zentrale 6.72.298; Portal SEO Themenengine 0.57.120; SEO-Compiler 0.28.43.
- Separate frühere Speicheranalyse (15.10.2026): sehr große Export-/Zwischendateien im Speicherbereich von All-in-One WP Migration; dies erklärt nicht ohne aktuelle Prüfung die heutigen 10,63 GB.
- Leistungsdiagnose vom Oktober zeigt Designlast durch Astra/Kubio und zahlreiche Datenbankabfragen; **kein Nachweis einer bereits erreichten Verbesserung**.
- Ein konkreter Konflikt zwischen Template Kit und Affiliate-Produktkarten wurde in einer früheren lokalen Browserprüfung nachgestellt. Aus diesem Befund folgt **keine pauschale Löschfreigabe**.

Ältere GitHub-/Bürostände sind ausdrücklich **nicht** automatisch identisch mit dem aktuellen WordPress-LIVE-Bestand.

## 3. Technisches Zielbild

1. **WordPress als schlanke Basis**, normale Updates bleiben möglich.
2. **Eine zentrale Design-Zuständigkeit** für Farben, Schriften, Abstände, Header/Footer, Seitenvorlagen, Mobilansichten und globale Layoutregeln. Möglichst kleines, eigenständiges Theme; Astra und Kubio sollen nach vollständigem Nachweis entfallen können.
3. **Eine fachliche Zuständigkeit je Funktion**. Doppelte Eingriffe in Darstellung und Ausgabe vermeiden. Funktionale Plugins nur behalten, wo erforderlich.
4. **Übersichtliches Backend**: unnötige Bedienoberflächen und reine Diagnose-/Import-Werkzeuge nach Bedarfsprüfung entfernen oder nur zeitweise nutzen; nicht bloß optisch verstecken, wenn sie weiterhin Ressourcen benötigen.
5. **Performance mit Messbelegen** verbessern: Ladezeiten, Datenbankabfragen, Speicher, Frontend-Dateien und Hintergrundlast.
6. **Bestehende Fachsysteme nicht umbauen**, wenn das keinen nachgewiesenen Nutzen hat.

## 4. Verbindliche Umsetzungsreihenfolge

| Phase | Konkrete Arbeit | Zuständigkeit | Erfolgskriterium |
|---|---|---|---|
| A – Bestandsplan | Aktuellen WP-Bericht und vorhandene Pluginquellen gegenüberstellen; Funktion → zuständige Komponente; Design-Abhängigkeiten, mögliche Doppelungen und reine Werkzeuge erfassen. Speicheranalyse ergänzen. | Assistenz; Betreiber liefert nur die bereits angekündigte Analyse | Liste **Behalten / Prüfen / Zusammenlegen / Ersetzen / Entfallen** mit konkreten Belegen und ohne voreilige Löschfreigabe |
| B – Testbasis und geplanter Import | Separate WordPress-Testinstallation nutzen; **keine Seiten von Hand neu anlegen**. Originalseiten, Beiträge, Kategorien, Medien, Navigation, erforderliche Einstellungen sowie Anzeigenmarkt-Daten über einen vorher festgelegten kontrollierten Import übernehmen. Plugins/Funktionen nur gezielt und mit Abhängigkeitsprüfung installieren; kein blindes Komplettklonen. E-Mails, Tracking, Cron und externe Aktionen auf der Kopie isolieren. | Gemeinsam bei Übernahme, Assistenz bei Importplanung und Tests | Nachgewiesene Trennung, Vollständigkeit der Inhalte und sichere Rückkehrmöglichkeit |
| C – Design | Aktuelles Frontend als Vergleichsbasis dokumentieren; identische Vorlagen in einer zentral gesteuerten schlanken Designbasis umsetzen. | Assistenz | Desktop-/Mobilansichten und Interaktionen stimmen überein |
| D – Funktionen | Bestehende Fachfunktionen auf der Testkopie anbinden; Astra/Kubio nur dann ablösen, wenn die betreffenden Funktionen nachweisbar weiter funktionieren. | Assistenz | Jede bestehende Funktion besteht ihren Test; K0 unverändert |
| E – Verschlanken | Nachgewiesene Doppelungen, unnötige Frontend-Dateien, dauerhaft aktive Diagnose-/Importwerkzeuge und verwaiste temporäre Daten gezielt reduzieren. | Assistenz, nur Testsystem | Kein Funktionsverlust, geringere technische Last; nichts ohne Rückweg löschen |
| F – Gesamtabnahme | Vorher/nachher auf gleichen Seiten und unter vergleichbaren Bedingungen testen: Optik, Mobilansicht, URLs, SEO, Suche, Formulare, Anzeigenmarkt, Affiliate, redaktionelle Abläufe, Geschwindigkeit. | Assistenz; Betreiber gibt Ergebnis frei | Dokumentierter Gesamt-PASS, offene Abweichungen = keine Freigabe |
| G – Umstellung | Gesicherter, geplanter Wechsel unter Berücksichtigung neu hinzugekommener LIVE-Daten; sofortige Rückkehrmöglichkeit. | Gemeinsam | LIVE entspricht in Aussehen/Inhalt/Funktion dem Ausgangsstand; Performance gemessen |

## 5. Was jetzt konkret zu tun ist

- **Stand:** Speicheranalyse und Pluginbestand eingegangen; leere neue Testinstallation ist laut Betreiber eingerichtet und aufgeräumt; HivePress und passendes Theme bereits installiert. **Nicht erneut anfordern.**
- **Nächste Betreiberhandlung:** Auf der **alten LIVE-Seite** unter **Werkzeuge → Daten exportieren → Alle Inhalte → Export-Datei herunterladen** eine XML-Datei erzeugen und zur **Inhaltsprüfung** übergeben. Dabei wird auf LIVE nichts gelöscht oder umgestellt. **Noch nicht importieren.**
- **Nächste Assistenzhandlung:** XML auf tatsächlichen Seiten-/Beitrags-/Kategoriebestand, zusätzliche Seitentypen und dynamische Plugin-Seiten prüfen; vorhandene Pluginakten abgleichen. Daraus einen nachweislich vollständigen, schlanken Importplan ableiten.
- **Danach:** Originaldaten kontrolliert übernehmen, schlanke Designbasis auf realen Inhalten anfertigen, Fachfunktionen isoliert ergänzen, testen. Keine vollständige Altinstallation kopieren.

## 5a. Verbindliche Präzisierung nach Prüfung am 03.11.2026

Der Betreiber hat die **leere, isolierte WordPress-Testinstallation** bereits eingerichtet, Grundeinstellungen erledigt, Beispielinhalte/überflüssige Plugins entfernt, HivePress aktiviert und ein HivePress-Theme installiert.

**Korrektur eines falschen Chat-Arbeitsschritts:** Das manuelle Anlegen leerer Seiten namens „Startseite“ und „Anzeigenmarkt“ war **nicht nötig und nicht durch dieses Konzept gedeckt**. Es ist zu unterlassen. Falls die beiden leeren Seiten schon angelegt wurden, vor dem Import prüfen, dass keine doppelten URL-Namen oder Seiten entstehen.

**Import-Regel:** Die bisherigen tatsächlichen Seiten, Beiträge, Kategorien, Bilder und Navigation werden aus der bisherigen WordPress-Seite **übernommen**, mit bestehenden URLs und Inhalt. Die Daten des Anzeigenmarkts und individuelle Design-/Plugin-Einstellungen müssen explizit berücksichtigt werden. Ein einfaches WordPress-XML-Importverfahren ist nicht automatisch ein vollständiger Umzug sämtlicher pluginbezogener Einstellungen/Daten. **Keine pauschale vollständige Datenbank-/Plugin-Kopie**, da das alte System so wiederhergestellt und die Verschlankung unterlaufen würde.

**Korrigierte Reihenfolge ab jetzt:**
1. Assistenz bestimmt den **konkreten Importumfang und die Quelle jeder Datenart** auf Basis vorhandener LIVE-Plugin- und Projektunterlagen.
2. Erforderliche Ziel-Funktionen/Seitentypen vorbereiten, ohne das alte Designsystem unkontrolliert zu übernehmen.
3. **Kontrollierter Import der Originaldaten** auf die isolierte Testinstallation – nicht neu tippen.
4. Neue schlanke Designbasis auf den importierten Originalseiten entwickeln und mit LIVE vergleichen.
5. Vollständige Funktions- und Abnahmeprüfung vor irgendeiner Umstellung.

**Nächste Aufgabe des Betreibers:** Keine zusätzlichen Seiten anlegen und zunächst nichts importieren; erst der geprüfte Importfahrplan nennt notwendige konkrete Klicks.

## 6. Stopp-Regeln

- Ein nicht belegter oder fehlgeschlagener Test bedeutet **STOP**, nicht „wird schon gehen“.
- Keine Entfernung von Astra, Kubio, Plugin oder gespeicherten Daten ohne dokumentierte Nutzung-/Abhängigkeits- und Rückwegprüfung.
- Kein Vergleichstest darf als bestanden ausgegeben werden, wenn nur einzelne Teilfunktionen simuliert wurden.
- Dieses Konzept selbst verändert keine Programme, Inhalte, Datenbank, LIVE-Konfiguration, Fach-Current-Dateien oder K0.

**Leitgedanke:** Nicht weiter auf bestehende Schichten draufbauen. Saubere, kleinere technische Basis schaffen und alle vorhandenen Leistungen unverändert erhalten.


## 7. Phase A: Tatsächlicher Auswertungsstand vom 03.11.2026

Quellen: WordPress-Website-Zustandsbericht vom 03.11.2026 und **bereits eingegangene** Speicheranalyse `wordpress-speicheranalyse-20261103-114349.json`. Keine erneute Anforderung dieser Dateien.

### Harte Messwerte und Abgrenzung

- Speicheranalyse vollständig abgeschlossen, 33.094 Dateien, **2,53 GB erfasst** (nur untersuchter Dateibestand).
- Davon **1,83 GB WPvivid-Sicherungen**, 335 MB Uploads, 37,4 MB Kubio, 22,8 MB Astra.
- WordPress-Website-Zustandsbericht meldet hingegen **10,63 GB für Plugins**. Die Differenz ist **ungeklärt**; sie darf nicht als reale aktuelle Pluginlast oder sicher vorhandener Altbestand ausgegeben werden. Möglich ist ein unterschiedlicher Erfassungszeitpunkt/-umfang; keine unbewiesene Ursachenzuschreibung.
- Datenbank laut Speicheranalyse ca. **1,19 GB**; vor allem PSTE-Arbeits-/Statusdaten, Optionsspeicher und Affiliate-Produktdaten. Diese sind potentiell funktions-/produktionskritisch und **nicht zur pauschalen Bereinigung freigegeben**.
- Vorhandenes Performance-Profil dokumentiert Frontend-Dateien und lange Datenbank-/Laufzeitpfade; daraus folgt kein automatischer Verursachernachweis für einzelne Plugins.

### Konsolidierte Entscheidungsgruppen – noch keine Löschfreigabe

| Gruppe | Bestand | Konkrete Maßnahme auf der isolierten Kopie |
|---|---|---|
| Zentrale Designsteuerung | Astra, Kubio, Affiliate Portal Template Kit; zusätzlich Breadcrumb-/Formular-/Produktdarstellung | Funktionen und Layoutvorlagen erfassen, identische Ausgabe schrittweise in kleine zentrale Designbasis überführen; bestehende Fachausgaben nicht doppelt umformen |
| Kritische Fachfunktionen | K0/PPM, PSTE, PSERC, Affiliate-Zentrale, Bildzentrale, Glossar, Pferderassen, Produktwissen | **Unverändert übernehmen**; nur Anbindungen und sichtbare Ausgaben abgleichen; kein Fachlogikumbau |
| Anzeigenmarkt und Suche | HivePress plus Erweiterungen; zwei Pferde-HivePress-Suchplugins; Relevanssi plus Live-Suche, mögliche Astra-Suche | Zuständigkeiten und tatsächliche Nutzung vergleichen; erst nach positivem Volltest eine nachweisliche Dublette ersetzen/entfernen |
| Betrieb und Werkzeuge | Performance Diagnose Safe, DBStorage Insights, WordPress Speicheranalyse, eBay Ursachencheck, Reveal IDs, Importer, Exporter | Werkzeugbedarf dokumentieren; nur entbehrliche Dauerausführung entfernen, Diagnose bei Bedarf getrennt verfügbar halten |
| Backup und Optimierung | WPvivid, All-in-One WP Migration, Pferde Atelier – Komplettsicherung, WP-Optimize | **Keine Löschung von Sicherungen.** Eine verifizierbare Recovery-Methode festlegen; überlappende Automatik erst danach vereinfachen |
| Allgemein notwendig | WordPress-Core, Yoast, CookieYes, WPForms, Akismet, Google Site Kit und ggf. weitere belegte Schnittstellen | Beibehalten, solange erforderlich; Ladeverhalten auf Testkopie prüfen |

### Konkreter nächster Arbeitsauftrag

1. **Assistenz, jetzt:** Aus vorhandenem WP-Pluginstand, Performance- und Speicherbericht eine Funktion-zu-Plugin-Liste und die Design-Umstellungsschritte ausarbeiten; **keine weiteren Datenuploads vom Betreiber erforderlich**.
2. **Betreiber, jetzt:** **Nichts** installieren, löschen oder deaktivieren. Die angekündigte Speicheranalyse ist **bereits vorhanden**.
3. **Erst bei Beginn der Umsetzung:** Eine technisch getrennte Testkopie mit vollständiger Isolierung gegenüber LIVE herstellen (separate Daten, keine produktive Automatik/ausgehenden Effekte). Notwendige einzelne Klicks dann genau benennen.
4. **Danach:** Design nachbauen, Funktionen/Pflegewege vollständig vergleichen, realistische Vorher-/Nachhermessung. Erst nach Abnahme Umstellung.

**Ungeprüftes bleibt ungeprüft.** Diese Phase-A-Auswertung ist eine Dokumentation, keine technische Installation, kein vollständiger Test und keine Freigabe zum Entfernen eines Plugins.

## 8. Nächster verifizierter praktischer Schritt: eigene WordPress-Arbeitsinstallation

**Stand:** 03.11.2026. Die Daten-/Plugininventur und Speicheranalyse liegen bereits vor. Die nächsten technischen Arbeiten dürfen keine Verknüpfung zu K0-LIVE schaffen.

**Entscheidung:** Keine WPvivid-Standard-Staging-Kopie direkt im produktiven WordPress-Pfad: Die freie Staging-Funktion kann nach Herstellerdokumentation WordPress-Dateien unter dem LIVE-Webspace und getrennte Tabellen in derselben LIVE-Datenbank anlegen. Das erfüllt die geforderte strikte Trennung nicht automatisch. Stattdessen eine **neue IONOS-WordPress-Installation mit eigener Installation und eigener Datenbank** aufsetzen; keine Übernahme von LIVE-Daten beim Anlegen.

**Verifizierter IONOS-Click-&-Build-Pfad (Webhosting):**
1. Im IONOS-Konto anmelden → **Menü → Web-Projekte**.
2. **Neue Website oder Shop anlegen** wählen.
3. **WordPress & Mehr** → **Open-Source-Lösungen für Ihre Website mit Click & Build**.
4. Bereits vorhandenen Webhosting-Vertrag auswählen (keinen kostenpflichtigen Neuvertrag bestellen).
5. Bei **WordPress → Installieren → WordPress selbst verwalten**.
6. Projektname **Pferdeatelier-Technik-Test**, neuen eigenen Administrator (Zugangsdaten nicht im Chat teilen).
7. **Temporäre System-Domain verwenden**; auf keinen Fall `pferde-atelier.de` zuordnen.
8. Erst wenn keine zusätzliche Bestellung und keine Zuordnung zur LIVE-Domain verlangt wird: **WordPress installieren**. IONOS dokumentiert, dass die nötige Datenbank dabei automatisch erstellt wird.
9. Unter **Website verwalten → Technische Daten** danach den **separaten Installationsordner und die separate Datenbank** gegenüber LIVE kontrollieren. Bei Übereinstimmung: **STOP**, nichts importieren.
10. Keine Plugins/K0/Automatik oder produktiven Daten auf der neuen Installation aktivieren, bis der Isolationscheck bestanden ist.

**Betreiber-Aktion jetzt:** Genau diese separate leere Installation anlegen. Keine ZIPs/Datenbanken in ChatGPT hochladen; kein FTP-/Serverzugang teilen. Wenn IONOS nur eine kostenpflichtige Zusatzbestellung anbietet, dort stoppen und keine Bestellung bestätigen.

**Danach führt Assistenz fort:** Testinstallations-Isolation prüfen, schlanke Designbasis vorbereiten, nur benötigte Funktionen kontrolliert übernehmen, Optik und Bedienung gegen LIVE vergleichen.

**Quellen (aktuell geprüft):**
- https://www.ionos.de/hilfe/hosting/click-build-anwendungen/wordpress-installieren/
- https://www.ionos.de/hilfe/mein-konto/hosting/click-build-daten-exportieren/
- https://docs.wpvivid.com/overview-staging-free.html

## 9. Prüfung der Reihenfolge – festgelegt am 03.11.2026

**Begründung:** Der offizielle WordPress-Standardexport „Alle Inhalte“ überträgt WordPress-Seiten, Beiträge, Kategorien/Taxonomien, Menüs und exportierbare eigene Inhaltstypen in eine XML-Datei. Er installiert **keine** Plugins und überträgt **keine** Theme-/Plugin-Konfiguration. Exportierbarkeit eigener Inhaltstypen ist konfigurierbar. Medien werden nicht einfach als Binärdateien in diese XML eingebettet; nicht zugeordnete Medien können fehlen. Quelle: https://wordpress.org/documentation/article/tools-export-screen/ und https://learn.wordpress.org/tutorial/tools-import-and-export/ und https://developer.wordpress.org/reference/functions/export_wp/

Pferdeatelier besitzt außerdem dynamische Design-/Kategorieausgaben und HivePress-Erweiterungen: **Eine XML-Datei beweist nicht, dass alle sichtbaren Seiten und Anzeigenmarktfunktionen enthalten sind.** Das ist explizit anhand der XML und Originalpluginquellen zu kontrollieren, bevor sie auf der Testseite importiert wird. Auf LIVE darf K0 nicht verändert werden. Die WordPress-Exportdatei ist eine **Erhebungsquelle, kein blindes vollständiges Migrationspaket**.

**Verbindliche Reihenfolge:** (1) Bestehende Inhalte read-only exportieren und ihren tatsächlichen Umfang prüfen; (2) fehlende Inhalte/Einstellungen der Fachplugins getrennt erfassen; (3) zielgerichtet importieren, ohne bisherige Programme/Designballast zu übernehmen; (4) Design auf importierten Originalinhalten nachbauen; (5) weitere Funktionen übernehmen und durchtesten. **Keine Seiten manuell neu erzeugen, keine Kategorie-Alleinmigration und keine vorzeitige Design-Entwicklung.**

**Jetzt:** Betreiber exportiert **Alle Inhalte** aus der alten LIVE-Installation, lädt die XML-Datei zur Prüfung hoch; **keine Importaktion** auf der neuen Installation. Assistenz prüft dann die tatsächlich enthaltenen Elemente, bevor der nächste Klick angewiesen wird.

## 10. Eingang des WordPress-Exports und tatsächliche Importentscheidung (03.11.2026)

**Original:** `pferdeatelier.WordPress.2026-11-03.xml` (36 MB, WordPress-WXR 1.2, geprüft).

**Originalbestand:** 6.045 WordPress-Objekte; darin 1.176 WordPress-Kategorien, 426 Seiten (424 veröffentlicht, 1 Entwurf, 1 Papierkorb), 182 Beiträge (163 veröffentlicht, 19 Papierkorb), 459 Bilder/Anhänge, 1.616 Menüeinträge (davon **1.582** im alten Produktnavigation-V4-Menü), 2.857 Affiliate-Kampagnen, 55 Anzeigen, 196 Pferderassen, 184 Glossareinträge; darüber hinaus Designvorlagen und Fach-Taxonomien.

**Wesentliche Architekturbeobachtung:** 411 der 426 Seiten haben keinen eigentlichen Seiteninhalt. Bei 399 Seiten ist der Einleitungstext im Feld `_pftk_category_intro_text` gespeichert und wurde bisher vom Design-Plugin gerendert. Ein unverändertes Design und vollständig sichtbare Seiten setzen deshalb eine neue gezielte Darstellung dieses Feldes voraus. **XML-Import allein ist kein sichtbarer vollständiger Seitenumzug.**

**Import-Paket 01 – erstellt und XML-geprüft:** `pferdeatelier_import_01_basis_20261103.xml` (9.778.884 Bytes). Enthält **genau** 1.176 WordPress-Kategorien, 424 veröffentlichte Seiten, 163 veröffentlichte Beiträge und 459 Medien-Anhänge, jeweils inklusive der zugehörigen Exportmetadaten. Keine Altdesign-Templates, keine riesigen Produkt-Menüs, keine Affiliate-Kampagnen, keine zusätzlichen Fach-Datensätze, keine Papierkorbobjekte. XML auf WXR-Version, vollständig vorhandene Kategorien und Inhaltszahlen validiert. Dies ist ein **Testimport**, kein fertiger Komplettumzug.

**Begründung:** Ein Import aller 6.045 Objekte auf die bloße HivePress-/WordPress-Basis würde alte Designdaten und nicht registrierte Fach-Inhaltstypen ungeprüft vermischen. Die Alt-Produktnavigation muss später aus tatsächlichen Seiten/Kategorien abgeleitet bzw. aus Originalmenüinformationen kontrolliert wiederhergestellt werden, nicht pauschal als 1.582 manuelle Menüelemente mitgenommen werden.

**Unmittelbar nächster Betreiber-Schritt:** Vor Import sicherstellen, dass nur die **separate Testinstallation** erreichbar ist bzw. dass sie ausreichend zugriffsgeschützt ist; WordPress-Importeur unter **Werkzeuge → Daten importieren → WordPress** installieren, dann Paket 01 nur in der Testinstallation importieren. Autor einem bestehenden Testbenutzer zuweisen; bei Bildern **„Dateianhänge herunterladen und importieren“** auswählen. Die importierten, durch das neue Design noch nicht gerenderten leeren Kategorieseiten sind erwartbar. Bei einem Importfehler stoppen und Fehlerwortlaut prüfen, nicht mehrfach blind importieren.

**Spätere Arbeit:** Fach-Inhaltstypen (Pferderassen, Glossar, Anzeigen, Affiliate-Produkte) mit genau registrierten Typen und ID-/Bild-/Relationen-Abgleich getrennt übernehmen; K0/produktionsaktive Automatik bleibt unberührt. Original-XML bis zum vollständigen Gesamtvergleich erhalten. Keine Änderungen an LIVE.

## 11. Korrektur nach erstem Basisimport – 03.11.2026

**Gemeldetes tatsächliches Ergebnis:** Betreiber sieht nach Import von `pferdeatelier_import_01_basis_20261103.xml` in der Zielinstallation **Kategorien, aber keine Seiten und Beiträge**. Das ist **kein erfolgreicher Import**. Die Ursache ist mangels Importer-Fehlerprotokoll noch nicht bewiesen, darf nicht als sicherer PHP-/Timeoutfehler ausgegeben werden.

**Verifizierte Datei-Reihenfolge:** Das erste Paket ist formal wohlgeformt und enthält 1.176 Kategorien (im Dateikopf), dann **459 Medien-Anhänge**, anschließend **424 Seiten** und erst zuletzt **163 Beiträge**. Ein Importabbruch bei/unter Medienverarbeitung würde exakt zur beobachteten Teilmenge passen; das ist eine **Hypothese**, kein Ursachennachweis.

**Korrekturmaßnahme ohne zusätzliche WordPress-Plugins:** Zwei separate, erneut parser-geprüfte XML-Dateien erstellt, Original-Elemente bytegenau beibehalten, Medien und Kategorie-Stammdaten für diesen Folgeschritt weggelassen:
- `pferdeatelier_import_02_seiten_20261103.xml`: 424 veröffentlichte Seiten, 868.671 Bytes.
- `pferdeatelier_import_03_beitraege_20261103.xml`: 163 veröffentlichte Beiträge, 5.195.433 Bytes.

Diese Dateien werden **nur auf der getrennten Testseite** über **Werkzeuge → Daten importieren → WordPress** importiert. Beim Autor den vorhandenen Test-Admin auswählen, **„Dateianhänge herunterladen und importieren“ nicht aktivieren**, zunächst **Seiten, danach Beiträge**. Erfolgsprüfung in **Seiten → Alle Seiten** bzw. **Beiträge → Alle Beiträge**, nicht am öffentlichen Design. Fehlen Inhalte oder erscheint eine Fehlermeldung, **keine Mehrfachimporte**; stattdessen exakten Importer-Ausgabetext prüfen. Bilder und Fach-/Design-Datentypen bleiben für spätere kontrollierte Schritte offen. Die bereits vorhandenen Kategorien werden anhand der Inhaltszuordnungen benutzt.

## 11. VERBINDLICHE KORREKTUR – Bildimport unvollständig, 03.11.2026

**Geprüft gegen vorliegenden Originalexport und vollständige Speicheranalyse:** In der originalen WordPress-XML gibt es **459 Datensätze des Typs `attachment`**, jeder mit einer URL. Die zeitgleiche Speicheranalyse der produktiven WordPress-Installation zählt im Verzeichnis **`wp-content/uploads` 3.743 physische Dateien, insgesamt 334.903.572 Bytes**. Darunter liegen Originalbilder, generierte Bildgrößen und ggf. andere Upload-Dateien; **3.743 sind ausdrücklich nicht 3.743 unterschiedliche Originalbilder**. Die XML enthält darüber hinaus mindestens 247 in Inhalt/Metadaten referenzierte Upload-Dateipfade, die nicht als wortgleiche `attachment_url` vorkommen (überwiegend Größenvarianten). Der Nutzer meldet auf der Testinstallation nach fünf gestückelten XML-Medienimporten zahlreiche fehlende Bilder.

**Fehler der bisherigen Empfehlung:** 459 Medieneinträge wurden mit dem vollständigen physischen Bildbestand verwechselt und ein erneuter XML-Import empfohlen, obwohl die XML keine vollständigen Datei-Bytes enthält. Auch ein gelungener WordPress-WXR-Import ist kein Nachweis, dass sämtliche alten Upload-Dateien und Größenvarianten tatsächlich auf der Zielinstallation liegen. **Die frühere Aussage 'Bildimport vollständig' wird widerrufen.**

**Erneute Korrektur auf Basis genauer WXR-Pfadprüfung:** Der pauschale Transfer **aller** 3.743 Upload-Dateien war zu weitgehend. Der WXR enthält **459 registrierte Medien, sämtlich unter `wp-content/uploads/2026/`**, 450 WebP und 9 JPG; Mittelwert registrierter Originaldateigrößen 138.603 Byte, Maximum 357.960 Byte. Zusätzlich explizit in Inhalten verlinkt (nicht als Attachment exportiert): `2020/07/Klaudia-Skodnik-Profilbild-2.jpg`, `2023/03/hero-new1.jpg`, `2023/03/hero-new2.jpg`, `2024/02/Proceedings-69th-Annual-Convention-2023.pdf`, `2024/02/Proceedings-64th-Annual-Convention-2018.pdf`, `fonts/Porcelain.ttf`. Vorhandensein dieser sechs zusätzlichen Dateien auf LIVE noch nicht einzeln nachgewiesen; Dateiübernahme nur, wenn vorhanden und tatsächlich für die Darstellung benötigt.

**Korrigierter Dateitransfer:** Nur die datierten Unterordner `2026/`, `2020/`, `2023/`, `2024/` und bei Bedarf `fonts/` unter unveränderter Struktur von **LIVE `wp-content/uploads`** nach **TEST `wp-content/uploads`** **kopieren (niemals verschieben)**. Es ist nicht erforderlich, den gesamten Upload-Hauptordner zu übertragen. Vor dem Kopieren Quell-/Ziel-WordPress-Installation anhand separater Hostingpfade festlegen. Die technischen Funktionen und Datenbanken bleiben getrennt; kein K0-Kopie- oder Jobstart.

**Explizit NICHT kopieren:** `wp-content/uploads/result_NANO_BANANA_PRO_FLASH_*.png` im Stammordner (große Generator-Originale; keine regulären Attachment-URLs im WXR), `pferdeportal_workflow_*.tmp.zip`, `pferde-atelier-pftk-backups`, `pferde-atelier-template-kit-category-1149-backups`, Produktionscenter-/Workflow-/K0-Arbeitsordner, `wpo`/Caches, `wpforms/cache`, Wartungs- und Plugin-ZIP-Dateien. `wp-content/wpvividbackups` liegt außerhalb `uploads` und wird ebenfalls nicht kopiert. Keine Altdateien auf LIVE löschen; kein Optimierungsplugin zusätzlich installieren.

**Nachweisgrenze:** Ein Kopieren der Dateien allein registriert fehlende Medienobjekte nicht in der neuen WordPress-Datenbank und schreibt eingebettete absolute LIVE-Adressen nicht automatisch um. Der gezielte WXR-Import der 459 Medien ist bereits versucht. Nach Kopie erst Auslieferung auf der Testseite kontrollieren, dann bildbezogene IDs/URLs und sichtbare Kategorie-/Hero-/Glossarbilder prüfen. Ein reiner Ordnervergleich ist keine funktionale Abnahme.

**Dem Betreiber jetzt zu sagen:** Aus altem `wp-content/uploads` ausschließlich `2026` (alle registrierten Bilder), ergänzend `2020`, `2023`, `2024`, `fonts` wenn vorhanden/benötigt, in gleichnamige Ordner der neuen Installation **kopieren**. Workflow-ZIPs, Backups, Production Center und Nano-Banana-Original-PNGs im Upload-Hauptverzeichnis **nicht kopieren**. Erst dann Stichprobenprüfung und ggf. Bild-URL-/ID-Reparatur. **Frühere Anweisung, alles aus `uploads` zu kopieren, ist ausdrücklich widerrufen.**
