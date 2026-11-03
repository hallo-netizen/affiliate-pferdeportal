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
| B – Testbasis | Vom Betreiber freigegebene, **separat isolierte** WordPress-Testinstallation herstellen; produktive Daten nur als geschützte Kopie übernehmen; ausgehende E-Mails, Tracking, Cron/Automatik und externe Aktionen auf der Kopie kontrollieren, damit es keine Wirkung auf LIVE gibt. | Gemeinsam bei Einrichtung, Assistenz bei Planung und Tests | Nachgewiesene Trennung und sichere Rückkehrmöglichkeit |
| C – Design | Aktuelles Frontend als Vergleichsbasis dokumentieren; identische Vorlagen in einer zentral gesteuerten schlanken Designbasis umsetzen. | Assistenz | Desktop-/Mobilansichten und Interaktionen stimmen überein |
| D – Funktionen | Bestehende Fachfunktionen auf der Testkopie anbinden; Astra/Kubio nur dann ablösen, wenn die betreffenden Funktionen nachweisbar weiter funktionieren. | Assistenz | Jede bestehende Funktion besteht ihren Test; K0 unverändert |
| E – Verschlanken | Nachgewiesene Doppelungen, unnötige Frontend-Dateien, dauerhaft aktive Diagnose-/Importwerkzeuge und verwaiste temporäre Daten gezielt reduzieren. | Assistenz, nur Testsystem | Kein Funktionsverlust, geringere technische Last; nichts ohne Rückweg löschen |
| F – Gesamtabnahme | Vorher/nachher auf gleichen Seiten und unter vergleichbaren Bedingungen testen: Optik, Mobilansicht, URLs, SEO, Suche, Formulare, Anzeigenmarkt, Affiliate, redaktionelle Abläufe, Geschwindigkeit. | Assistenz; Betreiber gibt Ergebnis frei | Dokumentierter Gesamt-PASS, offene Abweichungen = keine Freigabe |
| G – Umstellung | Gesicherter, geplanter Wechsel unter Berücksichtigung neu hinzugekommener LIVE-Daten; sofortige Rückkehrmöglichkeit. | Gemeinsam | LIVE entspricht in Aussehen/Inhalt/Funktion dem Ausgangsstand; Performance gemessen |

## 5. Was jetzt konkret zu tun ist

- **Betreiber:** Die bereits angekündigte aktuelle Speicheranalyse hochladen. Sonst vorerst **nichts** installieren, deaktivieren, löschen oder exportieren.
- **Assistenz:** Aus aktuellen Informationen und vorhandenen Original-Pluginunterlagen zunächst die **eine** konsolidierte Entscheidungsübersicht mit Abhängigkeiten erstellen. Kein Versionsraten.
- **Später, erst für Phase B:** Gemeinsam eine tatsächlich isolierte Testinstallation bereitstellen. Eine bloße Test-URL ist für die jetzige Konzeptphase nicht erforderlich.
- **Erst nach harter technischer Prüfung:** Neue Designbasis bauen, Funktionen nachweisen, technische Altlasten entfernen und ggf. LIVE umstellen.

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
