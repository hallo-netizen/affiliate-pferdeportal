# W35 – Einmaliger W27-konformer WordPress-Gesamtimport: erstellt und zehnfach vollständig offline geprüft
**Stand: 16.11.2026 | GitHub-Actions-Build PASS | kein WordPress-Live-Schreiben, keine Installationsfreigabe.**

## W35 löst den alten Neuner-/neuen Siebener-Widerspruch als EINEN Importgegenstand
- **Einziger aktueller Fachmaster:** W27. Alte W6-218-Owner bleiben exakt erhalten; kein neuer alter SEO-Owner, keine doppelte Fach- oder SEO-Entscheidung.
- **Importplan:** 219 Ziele = **114 WordPress-Seiten** (113 alte W6 plus **eine neue, unveröffentlichte Pool-&-Teich-Hub-Seite**) und **105 alte Beitragskategorien**. Die 81 marktgeprüften neuen W28-Kandidaten werden weder als Seiten noch als Kategorien automatisch importiert; SEO-/WP-Freigaben bleiben `false`.
- **WordPress-Struktur:** sieben Hauptseiten für Verbraucher (`wasseraufbereitung`, `wasseranalyse`, `brunnen`, `pumpen-druck`, `regenwasser`, `abwassertechnik`, `pool-teichtechnik`), **eine zusätzliche vorhandene eigenständige Industrie-Informationswurzel** (`industrie-grossanlagen`), ausdrücklich **nicht** als achter kaufnaher Menüpunkt. Das ist eine fachliche Menütrennung, keine verschwiegene achte Hauptkategorie.
- Genau zwei vorhandene Unterwurzel-Objekte bekommen eine neue Elternseite, sofern sie überhaupt schon existieren: `bewaesserung` unter `brunnen` und `wassertanks` unter `regenwasser`. Es sind **17 betroffene bisherige URLs** (9 Bewässerung, 8 Wassertanks); nach erfolgreicher Migration gibt es genau 17 **owner-geprüfte 301-Weiterleitungen**. Keine sonstigen alten Slugs/Produkt-Owner gehen verloren. Sechs bestehende Dachseiten erhalten die fachlich aktuellen W27-Titel, ihre Slugs bleiben erhalten.
- **Alte 79 W4-Produktseiten:** identische Owner, darunter 71 kaufnahe Menüpunkte und acht Industrie-Fachseiten. Der Renderer findet dieselben IDs vor **und nach** der 17er-Adressumstellung. Es werden keine weiteren Produktseiten über das SEO-genehmigte Material hinaus angelegt.

## Eine ausführende Stelle statt paralleler alter Schreibmodule
- Quelle der einzigen WP-Schreibfunktion: `../PLUGINS/QUELLCODE/W35_class-wassertechnik-import.php`, Klasse/Pluginidentität `Wassertechnik_Kategorie_Importer`/WT001.
- **Der alte W9-Importer ist im W33-Gesamtbuild tatsächlich ersetzt**, nicht zusätzlich eingehängt. Die ältere W6-218er-Importliste kann als historischer Datenbeleg im Paket bleiben, aber ihr alter Neuner-Importer ist **nicht aktiv**.
- Die vorangegangene W34-WP-Bestandslesefunktion bleibt als technischer Quellstand erhalten, wird in diesem Gesamtbau aber **nicht** als zweites WordPress-Admin-/Prüfmodul gestartet. W35 übernimmt genau **ein** aktuelles Gesamt-Preflight.
- W35-Preflight: Zielwebsite, Administrator, 219 eindeutige Owner, 114 gültige Zielpfade, 105 eindeutige Rubrik-Slugs, 17 exakt zugeordnete historische Umzüge, acht physische Wurzeln (sieben kaufnah + Industrieinfo), aktuelle WP-Seiten inkl. Entwürfe und Besitzerkennung, Kategorien, Fremdpfade, doppelte Owner und unveränderten WP-Bestandsfingerabdruck.
- Nur nach **einer ausdrücklichen Admin-Bestätigung** und unverändertem Gesamtbestand: einmal fehlende Seiten als Entwürfe anlegen; vorhandene zwei Unterseiten umhängen bzw. sechs Titel korrigieren; fehlende Kategorien nur ergänzen; **ein** Gesamt-Readback. Bei Fehlern nur die in diesem Lauf angelegten/umgehängten Objekte zurücknehmen. Keine Artikel und keine SEO-Abfrage.
- Bestehende veröffentlichte Produktseiten bleiben veröffentlicht. 301-Antworten greifen nur auf wirkliche 404-Anfragen, wenn das reale Ziel veröffentlicht ist und dieselbe Owner-ID trägt. Kein automatisches Redirect auf fremde Seiten.

## Tatsächlich ausgeführte GitHub-Actions-Gesamtprüfung
- GitHub W33-W35-Workflow `43868692835`: **erfolgreich**, Original WT001 0.1.4 SHA geprüft, originale 218er SEO-/DataForSEO-/Inventurklassen bytegleich, alte 218 SEO-Owner und Fingerabdruck `9570a11250f6d3684f52af69239a9af2090a292ba1646dafde76380c471b3462` identisch; W28 echte 81/90, W32/W35 echte 79/71/8, PHP-Lint, ZIP-CRC **PASS**.
- **10/10 eigenständige WP-Integrationsszenarien erfolgreich (echte PHP-Klasse mit WordPress-Mocks, keine behauptete WP-Live-Testumgebung):**
  1. `blank` – Beispielseite/Datenschutz/Allgemein erhalten, 114 neue Entwurfsseiten + 105 Kategorien importiert, 219 von 219 Besitzer zugeordnet.
  2. `old9` – bereits existierende 113 W6-Seiten + 105 WP-Kategorien, IDs/Veröffentlichungsstatus erhalten, nur Pool-Hub als Entwurf ergänzt, 17 neue Pfade, 71 gültige Produktmenülinks.
  3. `idempotent` – bereits vollständig importierter Bestand: **0** fehlende/zusätzliche Ziele, kein erneuter Importbutton, **0** Schreibaufrufe.
  4. `collision` – fremder vorhandener WordPress-Zielpfad sperrt vor jeder Änderung.
  5. `rollback` – absichtlicher Fehler bei der ersten Kategorie: alle 114 zuvor angelegten Seiten gelöscht und alter Bestand wiederhergestellt.
  6. `update-rollback` – Fehler bei der **zweiten** begonnenen Seitenänderung: sämtliche ursprünglichen Seiten-IDs, Pfade, Eltern und Titel wiederhergestellt; Pool-Hub zurückgenommen.
  7. `stale` – zwischen Vorschau und Freigabe geänderter WP-Fingerabdruck stoppt den Vorgang **ohne** Schreiben.
  8. `wrongsite` – fremde Website blockiert.
  9. `nonadmin` – fehlende Adminrechte blockieren.
  10. `redirect` – echte alte Bewässerungsproduktadresse erhält bei korrektem 404/Owner exakt den neuen **301**-Zielpfad.
- Zusätzlich zum Import bestehen sämtliche W33-Regressionen: 218 Alt-SEO-Owner, 81 neue Fachkandidaten/90 Rubriken, sieben Hauptbereiche, unveränderte originalen SEO-Klassen, alte 79 Produkte, **0 bezahlte DataForSEO-Aufrufe**.

## Festgehaltene Grenze
- Die W35-Einmalübernahme wurde **ausschließlich in GitHub-Actions-Mocks** ausgeführt; es gab **0 echte WordPress-Schreibvorgänge** und **0 neue SEO-Kosten**. Der letzte aktuelle WordPress-Live-Admin-Bestand ist noch nicht auslesbar, öffentliche WP-REST-Abfrage antwortet HTML statt JSON.
- Der zuvor in einem anderen Chat nur als ZIP erschienene WT001 **0.1.7**-Quellstand ist weiterhin nicht vollständig im Büro archiviert. Die funktionale Rekonstruktion aus dem echten 0.1.4-Original kann seine vollständige Menü-/Import-/Frontend-Parität nicht beweisen. Daher trägt die reproduzierbare Datei WT001 **0.1.8** weiterhin ausdrücklich **`NICHT INSTALLIEREN`**, selbst bei bestandenem Offline-Test.
- Die W35-Daten sind **abgeleiteter Importplan**, **kein zweiter Fachmaster**; W27 bleibt alleiniger Fach-Entscheider.

**Nächster sinnvoller Schritt:** Die vollständig getestete aktuelle Importplanung nicht erneut zerlegen; vor realer Installation nur einmal den tatsächlich vorhandenen WordPress-Plugin-/Adminstand und das Live-Frontend gegen den Gesamtbuild prüfen. Nach gesonderter Installationsfreigabe ist genau ein 219-Ziel-Import mit einem Admin-Preflight/Einmalfreigabe/Readback vorbereitet. Nutzer muss keine alten ZIP-Dateien auftreiben.
