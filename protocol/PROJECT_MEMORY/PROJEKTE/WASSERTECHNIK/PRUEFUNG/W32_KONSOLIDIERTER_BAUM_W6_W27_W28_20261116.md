# Wassertechnik – W32: Altbestand, endgültiger Fachbaum und neue Kandidaten in EINEM Navigationsentwurf
**16.11.2026 · fachlicher/technischer Read-only-Stand · kein WP-Import, keine neue Installations-ZIP**

## Bestandsvergleich ohne Vermutungen
- **Original W6:** 218 SEO-Owner = 113 bestehende fachliche Seitenentwürfe + 105 Rubriken. Darunter genau 79 W4-Produkt-Owner mit konkretem altem Seitenpfad.
- **Aktueller W27-Fachbaum:** sieben neue Hauptbereiche, darunter `Pool & Teichtechnik`. W11-0.1.7 enthielt ebenfalls sieben, aber fachlich **andere** Menübereiche, einschließlich eines Industriezugangs. Daher darf eine W11-URL-Umstellung um 17 Adressen nicht ungeprüft als W27-Migration übernommen werden.
- **79 W4-Produkte vollständig abgeglichen:** 71 kaufnahe Seiten über die sieben Fachbereiche, 8 ausschließlich im Fachtechnik-Zugang. Keine neuen WP-Owner, keine Seite gelöscht oder umgehängt.
- **Neue 81 W28-Marktkandidaten** besitzen weder SEO- noch WordPress-Freigabe. Davon sind 12 Pool/Teich; noch **0 bestehende WP-Produktseiten** in diesem Bereich. Eine Navigation darf dort keinen vorgetäuschten Produktlink zeigen.

## Einmalige Zuordnung
| Hauptbereich | Bestehende kaufnahe W4-Owner | Neue SEO-ungeprüfte W28-Kandidaten |
|---|---:|---:|
| Pumpen & Drucktechnik | 12 | 0 |
| Brunnen & Bewässerung | 9 | 21 |
| Regenwasser & Wasserspeicher | 15 | 8 |
| Trinkwasser & Hausinstallation | 19 | 23 |
| Wasseranalyse & Steuerung | 8 | 6 |
| Abwasser & Entwässerung | 8 | 11 |
| Pool & Teichtechnik | 0 | 12 |
| **Summe kaufnah** | **71** | **81** |

**Zusätzlich 8 W4-Industrie-Owner** im Fachtechnik-Einstieg, mit alten W6-Ownern und alten URLs unverändert erhalten. Damit sind alle **79** vorhandenen Produktowner einmalig abgedeckt.

## Technisch erledigt
1. **Ein automatisch aus echten W6/W27/W28-GitHub-Daten abgeleitetes, schreibfreies Anzeigeasset:** `../PLUGINS/ASSETS/W32_wassertechnik-navigation.json`. Es führt pro altem Produkt die tatsächliche Owner-ID und den unveränderten W6-WP-Seitenpfad; neue Produktkandidaten erscheinen ausschließlich als Zählung, nicht als neue WP-Seite.
2. **Ein reiner WordPress-Renderer** `../PLUGINS/QUELLCODE/W32_class-wassertechnik-navigation.php`: prüft, ob die frühere Seite tatsächlich existiert, veröffentlicht ist und dieselbe Owner-ID trägt; andernfalls kein Link. Zeigt keine leere Pool-Navigation. Kein SEO-Kosten-, Seiten-, Umzugs-, Kategorie- oder Redirect-Schreiber.
3. **Ein gebündeltes reproduzierbares Testskript** `W32_READONLY_NAVIGATION_QA.php` mit echten W32-Ownerreferenzen und WordPress-Mocks: die 79/71/8-Quoten, Vermeidung leerer Pool-Links, Sperre von Entwürfen/falschen Ownern/fehlender Datei, Admin-Zugriff, keine WordPress- oder API-Schreibaufrufe.
4. **Lokal synthetisch** dieselben 10 Verhaltensfälle der Renderer-Logik mit PHP 8.4 erfolgreich ausgeführt; die neue echte W32-Asset-Zuordnung direkt aus W6/W27/W28 beim Speichern mit vollständiger 79/71/8/7/81-Bilanz geprüft. Die separat im Büro gespeicherte W32-Dateiprüfung kann mit `php PRUEFUNG/W32_READONLY_NAVIGATION_QA.php` aus dem Wassertechnik-Root erneut gestartet werden. Dies ist **keine Behauptung eines WordPress-Livetests**.

## Was nicht erlaubt wird
- 0 neue SEO-Owner, 0 neue WP-Seiten, 0 URL-Änderungen und keine bezahlte DataForSEO-Abfrage.
- Das frühere 0.1.7-Original-ZIP ist nicht mehr als Originaldatei vorhanden; seine bewiesenen Menü- und Migrationsfunktionen werden deshalb nicht blind durch einen 0.1.4-Nachbau überschrieben.
- **Noch nicht installationsreif**: Der gesamte Build muss aus dem erhaltenen Original-0.1.4-SEO-System, dem W9-Importer, W30-81er-Einleser, W31-Preview und der neuen W32-Navigation **einmal** konsolidiert werden. Ein einziger vollständiger Test muss die 218 Alt-SEO-Owner, 81 neuen Produkte, sicheren Import einschließlich Rücknahme, Navigation, Fremdportal-Isolation und Freigabesperren umfassen.

**Abschluss dieses Arbeitspakets:** Zielnavigation ohne doppelte Seitenentscheidungen festgelegt; der originalfehlerhafte 0.1.7/W27-Begriffskonflikt ist als Migrationsrisiko beseitigt. Keine Nutzerdatei vorausgesetzt.
