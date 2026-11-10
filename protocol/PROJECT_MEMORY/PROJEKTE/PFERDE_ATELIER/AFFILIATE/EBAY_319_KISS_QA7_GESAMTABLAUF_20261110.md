# Pferdeatelier eBay – QA7: KISS-Rückbau ohne Funktionsverlust

**10.11.2026 – isolierte Arbeitskopie, nicht live installiert, nicht als Produktionsrelease freigegeben.** Grundlage ist die bereits geprüfte QA6-Kopie; keine neue Plugin-Architektur, kein zusätzlicher Worker, keine neue Datenbanktabelle oder WordPress-Option.

## Gesamtablauf bleibt unverändert

Start → ein zentraler gespeicherter Lauf → vorhandene und neue eBay-Angebote prüfen → BUSINESS-Auswahl mit Mehrfachzuordnung → ausgewählte Angebote verarbeiten → gezielte Nachsuche fehlender Familien → öffentliche Nachweise und sicherer Veröffentlichungsstand. Einzelne Produktfehler stoppen andere Produktfamilien nicht. Pause/Fortsetzen, Zugriffssperre und Schutz des letzten gültigen öffentlichen Bestands bleiben erhalten. Die frühere zusätzliche 319-Steuerung war bereits in QA5 entfernt; sie wurde nicht neu eingebaut.

## Zwei nachweislich überflüssige Bestandteile entfernt

1. **Zweite Datenlesung nach erfolgreichem Speichern:** `ebay_run_save` vergleicht den **gesamten** geschriebenen Zustand mit dem aus WordPress zurückgelesenen Zustand und meldet einen echten Speicherfehler. `ebay_run_phase_state_save` las danach denselben gespeicherten Zustand nochmals ausschließlich für den Vergleich eines Teilabschnitts. Jetzt wird derselbe Teilabschnitt aus dem *bereits erfolgreich vollständig verifizierten* Zustand verglichen – **kein erneuter Datenbank-/Optionslesevorgang**, gleiche Rückgabe. Die entscheidende Kontrolle gegen fehlgeschlagene Schreibvorgänge wurde **nicht** entfernt.
2. **Nicht erreichter privater Wrapper:** `ebay_private_public_post_allowed` war im gesamten Plugin nur einmal vorhanden: als eigene `private`-Definition. Die tatsächlich verwendete private Prüfregel `ebay_private_public_post_allowed_base` bleibt unverändert, inklusive aller bestehenden öffentlichen Sicherheitsfilter. Keine Schnittstelle und keine öffentliche Funktion entfernt.

## Physische Kontrollen und reproduzierbare Tests

- QA6 → QA7: **66/66 ZIP-Dateien** vorhanden und CRC-PASS; nur zwei bekannte eBay-Trait-Dateien geändert, **64/66 Dateien bytegleich**. PHP-Syntax **23/23 PASS**. Kein Anbieterwechsel, keine Änderung an Katalogen, Bildern, historischen Sicherungen, Zugangsdatenpfaden oder WordPress-Core.
- Die **fünf bereits bestehenden Fachtestprogramme** an der aus der **fertigen QA7-ZIP** entpackten Originalquelle ausgeführt: **61/61 PASS** (16 zentrale Auswahl, 13 Fehlerisolation, 11 direkte Materialisierung, 10 zusammenhängender Testablauf, 11 dauerhaftes Speichern).
- **13/13 direkte QA6/QA7-Vergleiche identisch:** vier öffentliche Nachweisfälle sowie neun Nachsuch- und Auswahlfälle; Status, gespeicherte Ergebnisse und Aktionen identisch.
- **8/8 zusätzliche Speicher-Rückgabevergleiche identisch**, einschließlich fehlgeschlagener Speicherung, altem Schema, ungültigem Schlüssel und ungewöhnlichen Eingabewerten. Bei fünf erfolgreichen Speichervorgängen wurde genau **eine zusätzliche Optionslesung entfernt**; bei Fehlerwegen gab es keine Änderung.
- Alle Tests in der isolierten PHP-Umgebung mit nachgestellten WordPress-Funktionen; **kein realer WordPress-/MariaDB-/eBay-End-to-End-PASS** daraus abgeleitet.

## Dateien / Ablage

- QA7-ZIP in der persönlichen Library: `/pferdeatelier/PLUGINS/QA/EBAY_319_KISS_QA7_KISS_DOPPELTE_LESUNG_WEG_NICHT_INSTALLIEREN_20261110.zip`.
- ZIP SHA256: `9d5a9a37ee9a268bfde914449c6736ef7313271e01973082ca265393a3e41f4c`.
- Änderungspatch SHA256: `9ee3b191e26507b78883c6bc24d523b175d0ddc5b9f013c40299f099c6ad5c7f`.
- Prüfbelege: `EBAY_319_KISS_QA7_RUECKBAU_NUR_BEWIESENES_20261110.patch`, `EBAY_319_KISS_QA7_REGRESSION_20261110.json`.

**Einziger offener Gesamtbeweis:** Die getrennte IONOS-WordPress-Testinstallation `Pferdeatelier-Technik-Test` muss einen realen gespeicherten Altstand mit WordPress/MariaDB bis zur richtigen Produktkachel durchlaufen. Die temporäre System-Domain oder ein verbundener WP-Testzugang liegt in diesem Arbeitskontext nicht vor. Deshalb weder eine Live-Änderung noch eine Installationsfreigabe behaupten. Bis dahin QA7 Staging, ursprüngliche Version/Release-CURRENT und K0 unangetastet.
