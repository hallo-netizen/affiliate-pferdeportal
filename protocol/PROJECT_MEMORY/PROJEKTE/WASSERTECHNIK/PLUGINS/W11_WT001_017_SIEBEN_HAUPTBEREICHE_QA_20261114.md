# Wassertechnik W11 – Sieben echte Hauptbereiche: geprüfte technische Vorbereitung
**Datum:** 14.11.2026. **Status:** Offline getestete WT001 0.1.7 als ZIP **im Chat zum Download**, **noch NICHT** auf WordPress installiert, **noch KEINE** WordPress-Umordnung durchgeführt. ZIP ist **nicht** in diesem GitHub-PR abgelegt; Dateibeleg: `WASSERTECHNIK_KATEGORIE_WORKFLOW_0.1.7_SIEBEN_HAUPTBEREICHE_NUR_TEST.zip` im zugehörigen Chat, SHA256 `0d27ea4caa9296ae750874957ddc7b51a3243c3af04a6e0e419e13297a91d246`, 50.544 Byte, 12 ZIP-Einträge.

## Tatsächlicher Ausgangspunkt
- W7-/WT001-0.1.6-Navigation hatte **neun sichtbare Hauptpunkte**, entgegen der 6–8-Vorgabe. W10 schlägt sieben vor. 
- W6-Produktbaum: **113 echte WordPress-Seiten** mit Besitzer-ID, **105 produktbezogene Beitragskategorien**, **79 Produktseiten**. Alle Quellen und Daten unverändert.
- Bereits publizierte Seiten auf der Testseite laut Nutzer erreichbar; **kein unabhängiger aktueller WP-Bestandsnachweis in diesem Durchgang**.
- Robotik hatte Konzept-/SEO-/Navigationregeln, aber keinen belegten fertig implementierten Live-Mega-Menü-Übernahmepfad. Daher kein Fremdplugin, nur bestehendes WT001 angepasst.

## W11: eine zusammenhängende Erweiterung in WT001 0.1.7
- **Sieben** Menüpunkte (19/8/9/12/15/8/8 Produkte), 79 konkrete Produktlinks genau einmal, max. drei Spalten, keine leeren Industrie-Untergruppen, keine zusätzlichen Seiten für hübsche Optik. Vier vorhandene Teilbereiche unter sachlich zwei Fusionen:
  * Brunnen + Bewässerung = 9 Produktseiten, 3 gleichmäßig belegte Spalten.
  * Regenwasser + Wassertanks = 15 Produktseiten, 6/5/4 Links je Spalte.
  * Wasseranalyse wird als vorhandene Labortests / Schnelltests und Probenahme / Messgeräte angezeigt, ohne zusätzliche WP-Seite.
  * Abwassertechnik vorhandene Entwässerung in zwei rein visuelle Untergruppen geteilt; 0 neue SEO-Owner.
- **Vor ausdrücklicher Freigabe:** Das Menü zeigt sieben Bereiche, verlinkt die **alten funktionierenden** WP-Seitenadressen; es verspricht **nicht**, dass WordPress bereits umstrukturiert ist.
- **Mit separater ausdrücklicher WordPress-Freigabe** über dasselbe Plugin und ein neues Backend-Untermenü „7 Hauptbereiche“: *nur* zwei bereits existierende WordPress-Hauptseiten werden umgehängt: `bewaesserung` unter `brunnen`, `wassertanks` unter `regenwasser`. Nur die zwei oberen Überschriften `brunnen` und `regenwasser` werden in `Brunnen & Bewässerung` und `Regenwasser & Wassertanks` umbenannt; **Slugs der beiden oberen Seiten bleiben gleich**. Das ergibt **7 echte Wassertechnik-Hauptseiten**, erhält alle 113 Seiten-IDs und 105 Inhaltskategorien.
- Insgesamt ändern sich **17 Seitenadressen**, davon 9 im Bewässerungs- und 8 im Wassertankzweig (die 12 Produktseiten liegen darin). Nur diese beiden URL-Familien werden nach erfolgreicher einmaliger Umstellung dauerhaft per **301** auf `/brunnen/bewaesserung/...` und `/regenwasser/wassertanks/...` weitergeleitet. Die übrigen Seitenadressen bleiben unverändert.
- Ein gemeinsamer Bestandsabgleich anhand aller **113 + 105 W6-Owner** und ihrer Eltern, aktueller veröffentlichter Status, Zielpfadkonflikte und ein Bestandsfingerabdruck vor dem einzigen Schreibvorgang. Falsche Website, fehlende Inhalte, konkurrierender Lauf und veränderte Daten sperren. **Keine** weiteren technischen Entscheidungs-/Rechercheebenen. Die vier konkreten WP-Update-Operationen erfolgen in einem freigegebenen Vorgang; Gesamt-Readback, sonst Wiederherstellung der geänderten Eltern/Titel. Vorherige SEO-/Inventurfunktionen byteunverändert. Der alte W6-Anleger wird nach abgeschlossener W10-Umordnung gesperrt, damit er nicht die ursprünglichen URLs neu anlegt.
- Keine neue WordPress-Tabelle, kein WP-Core-Eingriff, keine fremden Portale, keine neue DataForSEO-Abfrage, keine neuen Produkt-/Artikelobjekte. Das einfache Voransicht-Design bleibt sonst gleich.

## Lokale Tests tatsächlich ausgeführt
1. Echte ZIP 0.1.6 entpackt und Original-W6-Mapping unverändert übernommen; WT001 0.1.7 ZIP mit **12 Mitgliedern**, Python-ZIP-CRC und **PHP-Lint aller PHP-Dateien: PASS**.
2. Alle **79** Produktlinks genau einmal in 7 W10-Menübereichen; 113 Seiten und 105 Kategorien unverändert: **PASS**.
3. Lokaler WordPress-Simulator mit kompletten 113 echten W6-Owner-Seiten und 105 Kategorien: Vorabprüfung 9 echte Wassertechnik-Hauptseiten, nach vier Updates 7 Hauptseiten, 113 Seiten-/105 Kategorien-Identitäten erhalten: **PASS**.
4. Fehler bei zweitem WP-Update: ursprüngliche Seitenhierarchie und Titel wiederhergestellt: **PASS**.
5. Veralteter Vorschau-Fingerabdruck, fremde Zielpfadkollision und falsche Zielwebsite: jeweils **blockiert, keine Änderung**: **PASS**.
6. Weiterleitung einer alten verschobenen Produktseiten-URL als 301 an dieselbe neue Produktseiten-URL unter Regenwasser/Wassertanks: **PASS**.
7. Desktop-Vorschau mit 7 Bereichen, Brunnen & Bewässerung 9 sichtbare Produktlinks und Mobil-Vorschau mit 7 Bereichen und öffnendem Regenwasser-&-Wassertanks-Menü mit 15 Links (Chromium/Playwright): **PASS**.

## Nicht als erledigt behaupten
- **Noch kein echter WordPress-Live-Test der Version 0.1.7**, keine Installation und **kein** WP-Migrationslauf. Die 301-Wege sind lokal simuliert, nicht live auf dem Server bestätigt.
- Die ZIP ist **im Chat**, nicht schon im Wassertechnik-GitHub-Pluginordner; **nicht** als dort archiviert ausgeben. Der SHA und dieser Status sind verbindlich.
- Zwei Fusionen verändern tatsächliche URLs nur **nach** ausdrücklicher Admin-Bestätigung; WordPress auf der Testseite bleibt bis dahin unverändert. SEO-/Google-Indexzustand der neuen Live-Seiten nicht belegt.
- Die optionale **gezielte neue Produktrecherche** der W10-Lücken erfolgt getrennt nach einer stabilen Baumumstellung; **keine** pauschale neue kostenpflichtige SEO-Recherche.

**Nächster echter Schritt:** 0.1.7 als **Update des einzigen bestehenden Wassertechnik-Plugins** auf `wasser.oliver-beil.de` installieren, im Frontend sieben Menü-Reiter ansehen. Danach unter **Wassertechnik Kategorie → 7 Hauptbereiche** den **einmaligen Gesamtbestand** prüfen. Der eigentliche WordPress-Umbau erfolgt **nur** mit dem dortigen ausdrücklichen Admin-Häkchen und Button; nach erfolgreichem Lauf einmal Frontend-/Redirect-Resultat rücklesen.
