# Pferdeatelier eBay – gebündelte Ausspielungsfassung QA14 6.72.325

**Stand 11.11.2026 | Einzige weitere zusammengefasste Staging-Installation, KEIN bestätigtes Live-/CURRENT-Release.** Grundlage ist das vollständige, physisch geprüfte QA13 ZIP **6.72.324**. Keine Migration, kein Löschen oder Rücksetzen der bestehenden WordPress-Daten, Produktquellen, Checkpoints, Recherchen, Laufcursor oder K0-Inhalte. Hobbydepot und Hab & Bewahr unberührt.

## Zielvertrag / unverändert

- **Recherche, Ausspielung und 2h-Verfügbarkeitsprüfung** bleiben voneinander unabhängig. Prüfergebnisse und Freigaben von QA9–QA13 werden beibehalten; kein neuer Such-, Anbieter- oder Veröffentlichungsworker.
- **eBay Deutschland**, gewerbliche Verkäufer, sechs Stunden Datenfrische, nachweislich beendete Angebote nicht öffentlich ausspielen. Versicherungen und andere ausgeschlossene Nicht-Waren nicht erneut suchen. Nach begrenzter Suche offene Warenfamilien mit bekannten Gründen stehen lassen; keine künstliche 298/298-Pflicht.
- **Serverlast und weitere Backend-Verschlankung auf ausdrücklichen Wunsch erst danach.** QA12-Protokollierung und Download enthalten, nicht entfernt.
- **Keine neue Installation je Kleinstfix:** zwei nachweisliche weitere Fehlerursachen plus bisheriger QA13-Publisher in einer einzigen ZIP. Kein erneutes Installieren von 6.72.324 nötig.

## 1. Bestehende Beitragsprodukt-Pläne wurden bei jeder neuen eBay-Freigabe neu gestartet

**Quellnachweis QA13:** `ebay_public_checkpoint_add_verified_business_ids` ruft bei jedem neu bestätigten Produkt `article_plan_rebuild_request('ebay_verified_business_incremental', ..., 'products_only')` auf. `article_plan_rebuild_request` speichert bislang auf jedem Aufruf `cursor=0` und `scanned=0`, auch wenn gerade Artikel 26–60 in Arbeit sind. Wiederholte Einzelprodukte verschieben damit die spätere Artikelaktualisierung immer wieder an den Anfang. Dieser Fehler ist im QA13-Original-Source-Test reproduziert, **nicht** nur als Vermutung aus einer Anzeige abgeleitet.

**QA14-KISS-Korrektur:** Die vorhandene, einzige Produktplan-Aktualisierung läuft am alten Cursor zu Ende; weitere einzelne Checkpoint-/Ausverkauf-Ereignisse markieren nur `pending_ebay_product_pass=1` im **bereits existierenden** Plan-Status. Nach regulärem Abschluss läuft höchstens **ein** weiterer Produktdurchgang; kein zweiter Cron-Hook, keine zusätzliche Tabelle/Option. Verloren gegangener einzelner WP-Cron-Auftrag wird über denselben Hook neu terminiert, ohne Cursor-Reset. Übliche Gesamtplan-Rebuilds bei tatsächlichem Versionswechsel behalten ihre frühere Funktion.

**Test an echter geänderter Trait-Funktion mit simuliertem WordPress-Datenspeicher:** 60 Beiträge, sieben Einzelproduktfreigaben, gewöhnlicher Voll-Rebuild und verlorenes Cron-Ereignis. Alle Beiträge erreicht, höchstens ein Nachlauf, alte Gesamtplanfunktionen unverändert; QA13-Baseline schlug beim wiederholten Cursor-Reset nachweislich fehl.

## 2. Ein beendetes Produkt meldete einen nicht sichtbaren Nachrücker als „erfolgreich“

**Quellnachweis QA13:** `ebay_business_promote_ended_replacement` interpretierte **jedes** Nicht-`WP_Error` von `ebay_route_business` als erfolgreiche Veröffentlichung. `ebay_route_business` darf aber eine strukturierte, nicht fehlerhafte Antwort `last_good_preserved` ohne neue aktive Produktkampagne liefern. Außerdem wurde selbst nach wirklich aktivem Materialisieren **keine Aufnahme des Ersatzprodukts in den öffentlichen Checkpoint** nachgewiesen; das Produkt konnte intern als „promoted“ gelten und außen unsichtbar bleiben.

**QA14-KISS-Korrektur:** Nachrücker zählt nur, wenn `plan.active >= 1`, der Rückgabestatus **nicht** `last_good_preserved` ist, die bereits bestehende veröffentlichte eBay-Output-Zuordnung nachgewiesen wird und `ebay_public_checkpoint_add_verified_business_ids` den Ersatz nach seiner **unveränderten** öffentlichen Qualitäts-/Frischeprüfung tatsächlich aufnimmt. Ein ausstehender Checkpoint bleibt als `public_checkpoint_pending` sichtbar und wird **nicht** fälschlich als Erfolg gezählt. Ein wirklich beendeter alter öffentlicher Artikel wird weiterhin ausgeblendet; die **bereits vorhandene** Beitragsproduktplanung wird für passende verbleibende Karten/Fallback einmal gesammelt aktualisiert. Keine ungültige Quelle wird als verfügbar erklärt.

**Direkte Tests am geänderten Original-Ebay-Trait mit nachgestellten WP/DB-Objekten:** gültiger Ersatz, soft-review-Ergebnis, fehlendes veröffentlichtes Kampagnenobjekt, nicht gespeicherter öffentlicher Checkpoint, Datenbank-Lesefehler, unveröffentlichter Kandidat, zwei Reserven (erste verworfen, zweite nachweislich veröffentlicht), korrekt ausgeblendeter Altartikel. Die QA13-Baseline meldete in denselben Bedingungen zu Unrecht Erfolg.

## 3. Bereits bestehende Funktionen **nicht erneut entwickelt**

Sichere QA13-Teilfreigabe bei einzelnem Schlussprüfungsfehler, unabhängiger Availability-Worker und Nachweis von `source_state`, bestehende Quell-Reuse-/Search-Grenzen, eBay-DE-Filter, ausgeschlossene Nicht-Waren, QA11-Fortsetzung bei exaktem Fehler, QA12-CSV/JSON-Laufprotokoll und reduzierte eBay-Backendseite bleiben **bytegleich**, soweit nicht die zwei oben genannten bestehenden Ausspielungstraits berührt sind.

## 4. Technische Prüfergebnisse, Grenze

**Plugin:** `Pferdeatelier_Affiliate_6.72.325_QA14_GEBUENDELTE_AUSSPIELUNG_NUR_TEST.zip`  
**SHA256:** `54cb268274849b830131a89dc73e1f93059479b343df88855b5fe0ff13ae77f0`  
**Größe:** 5.380.468 Bytes; **66/66** ZIP-Dateien CRC/Bytevergleich PASS; **23/23** PHP-Syntaxprüfungen PASS.

Gegen QA13 **4 von 66 Dateien verändert**: `includes/trait-ppar-article-plans.php`, `includes/trait-ppar-ebay.php`, Plugin-Hauptdatei für Version, `readme.txt`. **62 Dateien vollständig unverändert**; kein neues Plugin, keine neue Datenbank, kein zusätzlicher Worker.

Bestehende **61** KISS-Fachregressionen gegen den QA14-Quellstand PASS. QA12-Audit-Speicher-Test PASS. QA13-Safe-Teilfreigabe-Test PASS. Neue Originaltrait-Tests: **12** Artikelplan-Fälle, **12** Nachrück-/Ende-Fälle PASS (QA13-Original versagt in beiden neuen Baseline-Szenarien).

**Nicht behaupten:** dass die zuvor im echten WordPress gemeldete Langsamkeit schon behoben ist (auf später verschoben); dass nun alle 489 gespeicherten Freigaben öffentlich sichtbar sind; dass 298/298 abgedeckt ist; oder dass eine echte WordPress/MariaDB/eBay-End-to-End-Abnahme bestanden wurde. Alle genannten PHP-Tests verwenden nachgestellte WordPress-/Datenbankzustände. Live-Dateien und gespeicherte Produktdaten wurden nicht verändert.

## 5. Einziger nächster WordPress-Praxistest ohne neuen Recherche-Lauf

Auf der bereits getrennten **WordPress-Testinstallation mit gesichertem Bestand**, **nur diese eine gebündelte QA14-ZIP installieren**. Prüfen: (1) alte Quellen, öffentliche Freigaben und Run-ID/Cursor bleiben erhalten; (2) zwei bekannte passende eBay-Produktseiten, davon eine **Kategorie und ein Beitrag**, zeigen echte aktuelle Kacheln; (3) ein bereits geprüftes/fachlich beendetes Angebot bleibt aus, ein nachgerücktes Produkt erscheint nur bei nachweislich gültigem öffentlichem Angebot; (4) Protokoll CSV zeigt die tatsächliche Phase ohne Neustart. Kein absichtliches Starten neuer Gesamtrecherche. Erst nach diesem echten Abnahmelauf über weitere Fehlerkorrektur oder produktive Freigabe entscheiden.

**GitHub:** Text-Patch, vollständige PHP-Testdateien und Bericht im existierenden isolierten eBay-QA-PR #748; ergänzendes reines Übertragungsregister PR #751. Test-ZIP im persönlichen `/pferdeatelier/PLUGINS/QA/` – GitHub nicht als binäre Pluginablage ausgeben.