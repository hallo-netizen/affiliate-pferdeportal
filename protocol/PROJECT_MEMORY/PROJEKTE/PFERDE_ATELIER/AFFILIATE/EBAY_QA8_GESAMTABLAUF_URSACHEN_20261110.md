# Pferdeatelier eBay – QA8: belegte Ursachen im GESAMTEN Ablauf (10.11.2026)

**Status:** Quellenprüfung und isolierter KISS-Patch, **nicht installiert, kein Frontend-Release, kein WordPress-Testpass**. Grundlage ist die vom Nutzer bereits installierte bzw. zur Installation erhaltene QA7-Datei `Pferdeatelier_Affiliate_6.72.320_QA7_TEST.zip`. Originaldatei bleibt unangetastet. Keine neuen Tabellen, Controller oder Provider, keine Löschung, kein Wortwechsel bei K0 oder CURRENT.

## 1. Fehlkonstruktion: PAUSE wird als Fehler und neue Arbeit behandelt (nachgewiesen)

Direkt im bestehenden PHP-Code (Run-Trait):

- Der zentrale Worker meldet bei explizitem manuellen Stopp korrekt `tick_result=paused` und `reason=operator_paused`, **ohne** den Fortschritt zu verändern.
- Der äußere REST-Taktgeber erlaubt `paused` nicht und wandelt es pauschal in `retryable_error` um. Zugleich zählt die gemeinsame Abfrage `ebay_run_is_active` ein `paused` zu den offenen Läufen; aus dem falschen `retryable_error` folgt ein neuer `self_drive`-Aufruf. GitHub macht daraus erneut eine „erfolgreiche“ Herzschlagrunde.
- Damit waren die vielen `retryable_error`-Meldungen während des belegten manuellen Stopps **nicht** nachweislich gescheiterte Produktsuchen, sondern ein reproduzierbarer falsch übersetzter Laufzustand.

**Minimaler Ursachenfix in isolierter Arbeitskopie:** Bei wirklichem `status=paused` und `resume_reason=operator_stop` gibt der bestehende REST-Taktgeber `status=idle`, `run_status=paused`, `reason=operator_paused` zurück. Keine Selbstfortsetzung, **kein neuer Worker**. Der gespeicherte Cursor bleibt unverändert; normale `advanced`, `retryable_error`, `busy`, `local_checked` behalten exakt ihr altes Verhalten. Der Fix ist **nicht auf WordPress installiert**, ändert nicht die eBay-Produktanzeige.

**Beleg:** `EBAY_QA8_PAUSE_LOOP_CAUSE_FIX_20261110.patch`, `EBAY_QA8_PAUSE_LOOP_REGRESSION_20261110.json` und `qa8_external_paused_contract_test.php`. Tatsächliche `handle_ebay_external_tick`-Methode im QA7-Code mit gleichbleibenden Eingaben vorher und nachher ausgeführt: vorher falsch `retryable_error` + ein neuer Dispatch; nachher `idle` + 0 Dispatches. Vier weitere Taktgeber-Ausgänge unverändert. **66/66** bestehende ZIP-Dateipfade, ausschließlich `includes/trait-ppar-ebay-run.php` als isolierte Entwurfsänderung; **23/23** PHP-Syntaxprüfungen, **61/61** bestehende echte PHP-Fachprüfungen bestanden. Kein neues ZIP veröffentlicht.

## 2. Warum die alten eBay-Kacheln verschwinden können (Quellcode-Ursache bestätigt; Produktionsverteilung NICHT nachgewiesen)

Dieselben, vorher bereits vorhandenen Sicherheitsfunktionen erklären den **anderen Teil** des Problems:

1. Frische eBay-Quellbestätigung wird im vorhandenen eBay-Quellimport nur **sechs Stunden** gültig gespeichert (`fresh_until = now + 6 * HOUR_IN_SECONDS`).
2. Der öffentliche Produktfilter `ebay_business_campaign_source_allows_delivery_base` sperrt die komplette eBay-Produktkampagne sofort, wenn `fresh_until <= time()` – **auch bei vorhandenem Produkt, alter Freigabe und erhaltenem Checkpoint**. Fehlt die Kampagne aus dem ausdrücklich sicheren öffentlichen Checkpoint, sperrt zusätzlich `ebay_public_checkpoint_allows_business_campaign`.
3. Die bestehende automatische eBay-Quellenaktualisierung für die **neue** öffentliche Auswahl erfolgt erst spät in `ebay_run_tick_public_verify`. Frühere WP-Cron-Synchronisierungs-/Refresh-Hooks werden bewusst abgeschaltet (`retire_ebay_legacy_cron_transport`). Ein **manuell gestoppter** Gesamtworker führt keine neuen Produktspeicherungen aus. Somit kann die bisherige freigegebene Ausgabe während einer langen Recherche/Stoppphase vollständig veralten und aus dem Frontend fallen.
4. Der Screenshot vom 10.11. zeigt ca. **22 Stunden** seit dem letzten echten Fortschritt, `status=pausiert`, Phase `gapfill_select/business_prune`, **114/298** zuvor nachgewiesene Familien und **keine eBay-Kacheln**. Das ist konsistent mit diesem Konflikt. Ohne verbundenen produktiven Datenbanklesezugriff ist NICHT belegbar, ob jede der betroffenen Kampagnen wegen Frische, Checkpoint, Platzierung oder weiteren bestehenden Sicherheitsbedingungen ausgeblendet wird.

**Direkter reproduzierbarer Codebeleg:** `ebay_visibility_gate_repro.php` verwendet die echte gespeicherte QA7-Quell-Filtermethode; vier Fälle nachgewiesen: frische und freigegebene Kampagne sichtbar; gleiche Kampagne abgelaufen unsichtbar; gleiche frische Kampagne ohne Checkpoint-Freigabe unsichtbar; nach erneuter gültiger Freigabe sichtbar.

## 3. KISS-Gesamtentscheidung statt erneuter 211er-Diagnose

**Nicht erneut machen:** 211 Produktfamilien einzeln prüfen; den bereits vorhandenen Suchgrundbericht neu erstellen; einen zweiten Recovery-/Auswahl-Controller eröffnen; 298/298 als Pflicht definieren; den 6-Stunden-Sicherheitsnachweis blind aufheben; einen `paused`-Status als neuen Produktfehler behandeln; kosmetische Fortschrittszahlen als erfolgreiche Veröffentlichung ausgeben.

**Einzige zusammenhängende noch offene Funktionsänderung:** Der **bestehende** kanonische Arbeitsweg muss die bereits veröffentlichten eBay-BUSINESS-Quellen **rechtzeitig wieder gültig bestätigen**, ohne auf das Ende der gesamten Suche zu warten. Dies ist mit dem bestehenden eBay-Refresh/getItem und vorhandenen eBay-Quell-/Checkpoint-Tabellen zu lösen, **nicht mit einem zweiten Such-/Veröffentlichungsweg**. Harte Sperren für wirklich beendete, gesperrte oder nicht nachweisbare Artikel bleiben bestehen; ein ausdrücklich manuell angehaltener Recherche-Cursor wird nicht zurückgesetzt. Erst nachdem genau dieser Übergang in WordPress/MariaDB und auf der Produktseite nachgewiesen ist, soll ein gebündelter installierbarer Nachfolger von 6.72.320 freigegeben werden. Bis dahin weder neue Plugin-Version noch Live-Datenänderung.
