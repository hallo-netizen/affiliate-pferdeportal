# Hab & Bewahr – 21.11.2026 – 0.4.31.19 – kostenloser Recheck bleibt RUNNING (Original-Driver-Sperre)

**Verbindlich:** Nur Recherche, kostenlose Keyword-Bestandsprüfung und Status. K0 bleibt vollständig unberührt. Keine kostenpflichtige DataForSEO-Anfrage. Bestehender originaler Ablauf, keine zweite Entscheidung und keine neue Architektur.

## Echte Diagnose aus WordPress
`texterstellung-diagnose-20261121-171352.json`: Plugin `0.4.31.18`, freie Originalqueue `RUNNING`, keine aktuellen Items in der Queueanzeige, letzter `SAVED_KEYWORDS_RECHECK_STARTED` am **21.11.2026 16:47:16 UTC**, Diagnose **17:13:52 UTC**. **Kein Abschluss oder fortlaufender Fortschritt nachgewiesen**. Die geloggte `ACTION_COMPLETED` bedeutet nur: Schaltfläche hat den Startauftrag angenommen.

## Eindeutiger echter Programmfehler: zwei widersprüchliche Sperren
1. `PSTE_Research_Driver::executeOneStep()` im originalen `class-pste-research-driver.php` beantwortet jede aktive Existing-Only-Queue bisher sofort mit `EXISTING_ONLY_AUTOREPLAY_DISABLED`, **statt die bereits vorhandene originale `PSTE_Breadth_Research_Queue::advance()`-Funktion zu verwenden**.
2. `PSTE_Research_Driver::maybeKickExisting()` ignoriert ebenfalls jede laufende Existing-Only-Queue; der automatische Wiederanlauf scheitert.
3. Die Diagnose meldet nur `RUNNING`, nicht die echten Originalverarbeiter-Felder, und im Backend fehlt die automatische Aktualisierung. **Keine Grundlage, einen fehlenden Fortschritt für einen normalen laufenden Auftrag zu halten.**

## KISS-Reparatur in 0.4.31.19
- **Einziger vorhandener Originalworker, eine Originalqueue**: Running Existing-Only durch die bereits vorhandene ursprüngliche Queue-Verarbeitung schicken; sichere Wiederaufnahme eines verwaisten Auftrags auf WP-Request erlauben. Die alte UUID, Original-Options, Signaturen und Locks bleiben maßgeblich. PAUSED_ERROR, OUTCOME_UNKNOWN, BLOCKED und aktive Locks **nicht übergehen**.
- Ein vorhandener kostenfreier Auftrag bleibt auch bei einem WordPress-Aktivierungsaufruf nach ZIP-Ersetzung erhalten, sofern signierter Originalstatus und Datenquelle exakt existing-only ohne Provider-Fallback sind.
- Reiter Recherche: echte `N von Gesamt`-Fortschritt, zuletzt abgeschlossener Arbeitsschritt, sichtbare Warnung bei längerer fehlender Bewegung, **alle 15 s automatische Browser-Aktualisierung nur für laufende kostenlose Queue**.
- Diagnose wird nur lesend um originale Worker-/Queue-Fortschrittsdaten ergänzt; **kein zweiter Verarbeiter, keine neuen DB-Tabellen, keine zweite fachliche Regel**.
- SEO-Keywords/Portalgate, DataForSEO-Methoden, MINI, K0, Import, Kategorie-Vertrag unverändert.

## Alt/Neu-Simulation mit tatsächlichem Original-PHP
**Keine vorgegebene COMPLETE-Queue**: dieselben **2128 synthetischen Kategorien**, **163 synthetischen Bestandsdatensätze**, der **originale vorbereitete Kontext (61 Verarbeitungsschritte)**, Original-`PSTE_Breadth_Research_Queue` und Original-`PSTE_Research_Driver`, isolierter WP-Optionsspeicher.
- **0.4.31.18:** 15 Original-Driver-Ticks, Warteschlange `RUNNING`, 0/163 bearbeitet, Driver `IDLE`. Reproduziert die konkrete Stillstandsursache.
- **0.4.31.19:** originale Driver-Ticks: **0 → 40 → 80 → 120 → 160 → 163 → COMPLETE**. Keine Anbieter-POSTs; Original-Queue nach jedem Schritt gespeichert und aus WP-Mock erneut gelesen, UUID bleibt.
- **15/15** zusätzliche Original-Driver-/Wiederaufnahme-/Negativtests bestanden (u.a. aktiver Lock wird nicht gestohlen, BLOCKED, PAUSED_ERROR und OUTCOME_UNKNOWN werden nicht wieder freigegeben, COMPLETE nicht erneut gestartet).
- UI-JavaScript in Node tatsächlich ausgeführt: sichtbarer Tab aktualisiert nach 15 Sekunden, versteckter Tab nicht.
- **78/78 PHP-Syntaxprüfungen**, **87/87 ZIP-Einträge CRC**, **83/87 Dateien bitidentisch** zu 0.4.31.18, vier existierende Dateien verändert. Die vollständige Quelldifferenz und QA liegen im Büro.
- Final ZIP SHA256: `9ab0a57cb2cd65883c96f830e1e3dba25686b04634b52b056136d929d6288f4d`.

## Grenzen
Die Testdaten sind **synthetisch**, nicht die tatsächlichen 163 WordPress-Kandidaten. Keine WordPress-Live-Verbindung und kein neuer Anbieteraufruf. Ein erfolgreiches WordPress-Review, die Zahl echter fachlich freigegebener Begriffe oder eine produktive MINI-Ausgabe sind **nicht** bewiesen. Behauptung „gesamter Live-Workflow fertig“ ist ausgeschlossen. **K0 wurde nicht ausgeführt oder geändert.**

## Installation / Prüfung
1. WPvivid-Backup. Vorhandenes Plugin durch `Texterstellung_HAB_UND_BEWAHR_0.4.31.19_ORIGINAL_DRIVER_LIVE_STATUS_FIX.zip` **ersetzen**, nicht deinstallieren.
2. **Nicht erneut** `Gespeicherte Keywords kostenlos erneut prüfen` klicken, wenn schon RUNNING: **Texterstellung → Recherche** einfach öffnen. Original-Driver stellt einen verwaisten aktiven Gratisauftrag im bestehenden Weg wieder her und zeigt den Fortschritt automatisch alle 15 Sekunden. Falls ausdrücklich `BLOCKED`, **nicht** heimlich wieder freigeben, Diagnose prüfen.
3. Nach tatsächlichem `COMPLETE` Diagnose-JSON exportieren und echte Keyword-Bewertungen und MINI-Übergabe prüfen. **Keine neue kostenpflichtige Recherche.**

Archiv: `/hab-und-bewahr/TEXTERSTELLUNG/PLUGIN_FREIGABEKANDIDATEN/` und `/hab-und-bewahr/TEXTERSTELLUNG/PRUEFUNG_ORIGINAL_WORKER_043119_20261121/`.
