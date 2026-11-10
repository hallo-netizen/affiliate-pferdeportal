# Pferdeatelier Affiliate/eBay – Gesamtflow, KISS-Rückbau QA6

**10.11.2026 | isolierte QA6-Arbeitskopie von QA5 | NICHT INSTALLIEREN.** Kein Eingriff in WordPress, K0, Live-CURRENT, andere Portale oder Zugangsdaten. QA5 vollständig erhalten.

## Ein einziges Arbeitsprinzip – gegen echten QA5-Code kontrolliert

Ein gültiger Start aktiviert den **einen kanonischen** eBay-Lauf. In begrenzten Arbeitspaketen laufen: vorhandene und neue eBay-Quellen → fachliche und Herkunftsprüfung → zentrale BUSINESS-Auswahl mit Mehrfachzuordnung → Materialisierung → begrenzte Nachsuche nur für offene Produktfamilien → abschließende öffentliche Quellen- und Seitenprüfung → sicherer Veröffentlichungs-Checkpoint. Der interne signierte Fortsetzungspfad ruft immer denselben Worker auf; der äußere GitHub-Heartbeat ist nur Taktgeber/Reserve, **kein zweiter eBay-Produktentscheider**. Vorhandene Stop/Fortsetzen- und Fehlerisolation bleiben erhalten.

## Was schon erledigt war und NICHT erneut repariert wird

- 311/312: richtiger gespeicherter Zustand auch bei eBay-Timeout/Wiederholung; echter Retry ist kein Stillstand; Simulation mit 311 Paketen.
- 314: dieselbe Startbereitschaft in Oberfläche und Worker; `queued` ist kein nachgewiesener Gesamtabschluss.
- 315: Teilzählung 0/298 einer Nachsuche von veröffentlichter Gesamtabdeckung getrennt.
- QA2: ein einzelnes fehlerhaftes Produkt stoppt keine anderen Produktfamilien; Mehrfachzuordnung und letzter guter öffentlicher Stand geschützt.
- QA3: gespeicherte BUSINESS-Angebote direkt nach den **ausgewählten** IDs statt Vollscan lesen.
- QA4: öffentlichen Quellnachweis in Gruppen statt pro Produkt zweimal einzeln lesen.
- QA5: Nachsuch-Bereinigung nur für betroffene Familien; vorher 41, danach 1 Abfrage im dokumentierten Testbeispiel. Zweiter 319-Controller bereits entfernt; Backend Übersicht + fünf Bereiche.

## QA6 – ausschließlich gesichert unnütze Wege zurückgebaut

**Neun private Methoden entfernt:** `ebay_private_query_variants`, `ebay_admin_preview_url`, `ebay_private_bucket_definitions`, `ebay_recover_private_target_term_id`, `ebay_persist_recovered_private_target`, `ebay_private_review_targets`, `ebay_private_parent_refill_posts`, `ebay_business_local_recovery_state_save`, `ebay_business_local_recovery_state_current`. Die harte Suche über **sämtliche Plugin-PHP-, JS-, JSON-, CSS- und Textdateien** ergab für jeden Namen **genau eine einzige Nennung: seine eigene Definition**. Keine Referenz, Registrierung, Weiterleitung oder Verwendung im aktiven Ablauf. Die historischen Optionen und Daten werden **nicht** gelöscht.

Außerdem eine **nachweisbar logisch doppelte Bedingung** bei `ebay_run_phase_state_load` entfernt: „Lauf ist offen ODER Schema ist 1.0“. Der „Lauf ist offen“-Fall setzt bereits zwingend Schema 1.0 voraus; die zweite Hälfte deckt alle zulässigen Fälle allein ab. Der gespeicherte Zustand und die Rückgabe bleiben unverändert. **Wichtige Sicherungen** (Lease, Speicher-Rücklesen, Source/Checkpoint-Prüfung, Fachklassifikation und öffentliche Freigabe) wurden **ausdrücklich nicht entfernt** – sie sind keine Doppelarbeit.

**Dateivergleich:** 66/66 Dateien erhalten. Nur `includes/trait-ppar-ebay.php` und `includes/trait-ppar-ebay-run.php` geändert. Alle 64 übrigen Dateien bytegleich. Alle anderen öffentlichen, geschützten und verbliebenen privaten Methodennamen/Zugriffsrechte identisch. Unberührt: andere Provider, Kataloge, Bilder, Recoveries, Zugangsdatenpfade, Backend, WP-Optionen, Datenbanktabellen, WP-Cron und Live-Taktgeber.

**Tests auf der fertigen QA6-ZIP:** CRC aller 66 ZIP-Einträge PASS; 23/23 PHP-Syntax PASS; exakt neun entfernte unaufgerufene Methoden; sieben echte PHP-Zustandsvarianten (altes gegen neues `ebay_run_phase_state_load` für fehlendes/Legacy/aktives/pausiertes/fehlgeschlagenes/abgeschlossenes/fehlerhaftes Schema) mit identischem Ergebnis. Kein neuer Controller, keine weiteren Regelwerke oder Tabellenerweiterungen. Die früheren QA5-Fachtests wurden **nicht als neu ausgeführt ausgegeben**; ihr Stand bleibt als historische QA5-Evidenz erhalten.

QA5-Original-SHA256: `561e5a4ef7148b351579aec8f67073bbf0805c5d1e1bc79d2d7b8c9444c26dc3`.
QA6-ZIP-SHA256: `a383d9cf7b8428ace8f94577b28d839a9e8d51f3efe5589520e888f077cc35ea`.
QA6-Patch-SHA256: `d9d59b0a7481eaea625bad41289cf219975356bf0cb8f69864ff7ce6e09a8165`.

## Verbindliche Grenze / nächster echter Gesamtbeweis

Ohne isoliertes WordPress mit MariaDB und gesicherten realen Laufdaten bleibt die **End-to-End-Abnahme offen**: alter Zustand laden → Auswahl/Bestandswiederverwendung → begrenzte Nachsuche → fehlerhafte Produktfamilie ohne Gesamtstillstand → Stopp/Fortsetzung → öffentliche Abdeckung & genau richtige Produktseite. **Bis dahin keine Installation, kein CURRENT-Wechsel, kein weiteres symptomatisches Kleinteile-Patchen.**

Der GitHub-Heartbeat ist fachlich separat; aus `retryable_error` ohne vollständigen gespeicherten Laufstand lässt sich kein neuer Ursachenbeweis ableiten. Die kurzzeitig ergänzte Zusatzdiagnose wurde zuvor vollständig zurückgebaut. Keine neue Prüfungsschleife.

## Nachprüfung QA6 an vollständig entpackter ZIP (10.11.2026, nach dem Rückbau)

**Keine neue Pluginänderung, keine weitere Prüfschicht.** Die schon vorhandenen früheren echten PHP-Testskripte wurden mit unveränderten Fachtests auf die vollständig entpackte QA6-ZIP aus der Library gerichtet. Es wurden nur die lokalen Test-Dateipfade angepasst, nicht die Testaussagen oder Pluginmethoden.

- **61/61 frühere Fachprüfungen tatsächlich neu auf QA6 ausgeführt und bestanden:** kanonische Bestandsauswahl 16/16; einzelne Produktfamilienfehler 13/13; nur ausgewählte Angebote lesen 11/11; ein zusammenhängender Ablauf bis Abschluss 10/10; dauerhaftes Speichern, Fehlversuche und Zustandserhalt 11/11.
- **13/13 zusätzliche direkte QA5-vs-QA6-Ausgabevergleiche identisch:** vier öffentliche Quellen-/Creative-Abdeckungen (normal, eingeschränkte Kampagnen, kaputte Quelle, kaputtes Creative) und neun Auswahl-/Gapfill-Bereinigungsszenarien (inklusive Wiederaufnahme, leerer Liste, Checkpoint und Datenbankfehler). Das alte QA4-Testszenario erwartet ausdrücklich den eBay-*Run*-Trait; bei der ersten Ausführung wurde versehentlich der eBay-*Auswahl*-Trait angegeben. Nach Korrektur **nur des Testaufrufs** alle vier Fälle auf beiden Varianten bestanden. Kein Fehler am Plugin.
- **23/23 echte PHP-Dateien der QA6-ZIP:** Syntaxprüfung erneut bestanden. **66/66 ZIP-Dateien** mit Originaldateien aus QA5 gegengeprüft: gleiche Pfade, nur die bereits dokumentierten **zwei** eBay-Trait-Dateien geändert, alle anderen 64 bytegleich. ZIP-CRC und SHA256 der vorhandenen QA6-Datei erneut bestätigt.

**Gesamter Workflow-Funktionsstand nach diesem Rückbau:** Die bestehenden Wiederverwendungs-, Auswahl-, Fehlerisolierungs-, Speicher-, Nachsuch- und öffentlichen Abdeckungspfade haben in diesen vorhandenen Tests keinen Unterschied oder Defekt gezeigt. Es wurden keine neuen Funktionen, Tabellen, Regeln, doppelten Tests im Plugin oder weitere Arbeitsprozesse eingebaut.

**Grenze bleibt unverändert:** Es steht hier kein vollständiger WordPress-Kern mit MariaDB/MySQL und echten anonymisierten Laufständen zur Verfügung. Daher ist die eine durchgehende WordPress-Praxis-Endabnahme (gesicherter Altstand → zentraler Lauf → Veröffentlichung auf richtiger Produktseite) nicht als bestanden belegt. QA6 bleibt **NUR TEST / NICHT LIVE INSTALLIEREN**, die bereits gesicherte QA6-ZIP und CURRENT bleiben unverändert.
