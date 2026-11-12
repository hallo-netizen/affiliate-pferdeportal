# Pferdeatelier eBay QA13 – Abschlussfehler der Produktausspielung, KISS

**Stand 11.11.2026, Version 6.72.324, nur getrennte WordPress-Testinstallation. Keine Produktions-/CURRENT-Freigabe.**

## Exakt verifizierte Ursache im vorherigen QA12 6.72.323

Die laufende Recherche materialisiert bereits geeignete BUSINESS-Artikel und besitzt einen vorgezogenen gesicherten Einzelprodukt-Freigabeweg. Trotzdem hielt `ebay_run_tick_public_verify` nach der letzten `getItem`-Runde den **gesamten** neuen öffentlichen Checkpoint zurück, sobald **mindestens ein einzelnes Angebot** nicht bestätigt werden konnte: `public_source_refresh_warning` → `checkpoint_deferred=1` → `ebay_run_complete` ohne neuen Gesamt-Commit. Der alte sichere öffentliche Bestand blieb zwar erhalten; **andere fertig bestätigte Produkte aus der letzten Prüfung wurden in diesem Zweig nicht mehr ergänzt**. Das widerspricht dem bereits vereinbarten Prinzip "ein einzelner Anbieterfehler blockiert nicht die übrigen Produkte" und ist von den alten Fehlerisolationstests nicht erfasst worden.

## Minimaler Fix – bestehende Veröffentlichung wiederverwenden

- Erfolgreich geprüfte Quellen werden beim vorhandenen Abschlussweg der **bestehenden** Methode `ebay_public_checkpoint_add_verified_business_ids()` übergeben. Diese prüft publizierte Kampagne, tatsächliche Quelle, eBay-Herkunft/Regeln, aktiven und frischen Bestand nochmals. **Kein neuer Publisher, kein zweiter Worker, keine neue Suche und keine neue Tabelle.**
- Fehlerhafte Produkte werden **vollständig nach Kampagnen-ID** ausgeschlossen. Bisher gab es nur bis zu zwölf Fehlerbeispiele für die Diagnose; diese verkürzte Liste darf nie als Freigabegrundlage verwendet werden. Alle betroffenen Kampagnen-IDs werden im **vorhandenen laufbezogenen Prüfzustand** erfasst; es werden weiterhin höchstens zwölf Fehlerbeispiele für die UI gesammelt.
- Ist beim Update aus QA12 ein laufender Schlussprüfstand vorhanden, der zwar Fehler zählt, aber deren einzelne IDs noch nicht vollständig erfasst hat, erfolgt **keine** pauschale Teilfreigabe. Der bestehende sichere Checkpoint bleibt maßgeblich.
- Der alte Checkpoint wird **nur ergänzt**, nicht gelöscht oder durch einen unvollständig geprüften Gesamtstand ersetzt. Dauerhafter eBay-Deutschland-Filter, Frischegrenze sechs Stunden, Provider-Zugänge, Kategoriezuordnung, bestehende Produktdaten und Run-Cursor bleiben unverändert.
- Globale Token-/HTTP-401/403-Fehler bleiben harte Sperren. Die QA12-Audit-Downloads, Stop/Fortsetzen, KISS-Backend und unabhängige Verfügbarkeitskontrolle bleiben erhalten.

## Tatsächlich gelaufene Tests – präzise Grenze

- `QA13_PUBLIC_APPEND_REAL_TRAIT_TEST.php`: **42 direkte PHP-Funktionsprüfungen** am echten QA13-Run-Trait mit nachgestellten WordPress-Datenspeicherungen/eBay-Antworten. Getestet: 16 Einzelfehler + 1 gültige Quelle, sogar wenn die fehlerhaften Quellen noch 60 Sekunden scheinbar frisch wären; **nur die gültige 17 wird ergänzt**, alter Safe-Bestand 501 bleibt; 12 UI-Fehlerbeispiele dürfen die vollständige Fehler-ID-Liste nicht verkürzen. Ein QA12-Altlauf mit unbekannten früheren Fehler-IDs erzeugt keine falsche Freigabe. Nebenbei alte Retry-, 401- und sichere Wiederaufnahmefälle erneut PASS.
- **61/61 bestehende Fachregressionen**: 16 Kanonisch, 13 Einzel-Fehler, 11 Effizienz, 10 Ablaufmock, 11 Speicherung PASS. Neun QA5-Vergleichsvarianten + ein QA4-Public-Gate-Vergleich gegenüber QA12 identisch. Der historische 187-Familien-Replay kann mit dem jüngeren 138-Familien-Export nicht als Original-187er-Datenlauf wiederholt werden; daraus wird kein neuer Erfolg behauptet.
- **23/23 PHP-Lints bestanden**, **66/66 ZIP-Einträge/CRC**, **63/66 Dateien bytegleich zu QA12**. Nur `includes/trait-ppar-ebay-run.php`, Plugin-Hauptdatei (Version 6.72.324) und `readme.txt` geändert.
- ZIP SHA-256: `69c5a2b9e837a5968b376761cc96b763e22f8d5dd2e95f635b4fa86ea3bb3425` (5.379.206 Bytes). Separat im privaten Pluginbüro gespeichert; keine binäre ZIP auf GitHub behaupten.

## Was NICHT bewiesen ist

**Kein realer WordPress/MariaDB/eBay-End-to-End-Test** und kein nachgewiesener Abschluss der gesamten Kategorieabdeckung. Die bereitgestellten Screenshots mit 489 gespeicherten Freigaben allein beweisen nicht deren tatsächliche öffentliche Sichtbarkeit, Frische und Platzierung. Ein PHP-Test mit nachgestellten Daten ist **kein Live-Test**.

**Bei realer Staging-Prüfung nur:** bestehender Run-/Bestandsschutz, erfolgreiche safe-append-Zahl nach Quellen-Einzelfehler, eine tatsächlich sichtbare passende eBay-Kachel (Kategorie und Beitrag) und Protokollauszug. **Kein Neustart nur für den Test, keine Löschen/Zurücksetzen.**

## Prioritätsvertrag bleibt

Erst echte Ausspielung und aktuelle Produktverfügbarkeit, dann verbliebene belegte Kategorie-Lücken; **Serverlast zuletzt**. QA13 behauptet keine Reparatur des gesamten Rankings oder Frontends. Hobbydepot und Hab & Bewahr: nur Referenz in getrennten Büros, **keine Plugin-Übernahme**.