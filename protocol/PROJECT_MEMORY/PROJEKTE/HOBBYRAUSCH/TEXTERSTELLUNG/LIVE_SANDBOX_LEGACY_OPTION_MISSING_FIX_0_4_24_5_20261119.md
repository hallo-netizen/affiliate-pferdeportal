# 19.11.2026 – Hobbydepot Texterstellung 0.4.24.5, live gemeldeter Sandbox-Fehler

## Tatsächlicher Betreiberbefund
Screenshot auf Hobbydepot-Recherche-Seite: `PSTE_CONTEXT_BLOCKED_PSTE_SANDBOX_RECORD_STORE_LEGACY_OPTION_MISSING`; vorhandener Kontextjob ist BLOCKED. **Nichts aus der vorhandenen WordPress-Datenbank direkt ausgelesen**, aus Beleg und Originalcode ergibt sich jedoch: Der verpflichtende alte Sandbox-Optionsdatensatz wird im Kontextjob nicht gefunden. Bisheriger Teststand 0.4.24.4 hatte diesen frischen Datenbankzustand nie durchgespielt.

## Eindeutige zwei Code-Ursachen
1. Original `PSTE_Sandbox_Record_Store::stageSourceIfNeeded()` verlangt eine bereits vorhandene alte Sandbox-Option. Das Original `PSTE_Semantic_Review_Sandbox::stored()` kennt zwar einen kanonischen leeren Erstzustand, persistiert ihn aber nicht. Die ursprüngliche Streammigration blockiert mangels Quelle bei einem jungfräulichen Portal.
2. TXE-WordPress-Controller `ajaxSafeMigration()` verweigert schon **vor** dem Aufruf von `PSTE_Context_Refresh::processBatch()` pauschal jeden bestehenden `BLOCKED`-Kontext. Selbst eine im Original-Migrationsjob ausdrücklich erlaubte Fortsetzung konnte den Browser nicht erreichen.

## Korrektur ohne Neu-/Umbau
**Neue geprüfte Installer-ZIP:** `Texterstellung_Hobbydepot_0.4.24.5_SANDBOX_LEERBESTAND_FIX.zip`, SHA256 `42f648b59a99fda0b1684c0e174a9430f4d9d131eaa8d98548157c5d8e09e2ba` / 506541 Bytes; Wurzelordner `texterstellung-hobbydepot/`; Versionsheader `0.4.24.5` (höher als vorher installierte 0.4.24.4).
- 83 von 87 Dateien byteidentisch zu 0.4.24.4, vier bestehende Dateien geändert:
  - `original/pste/includes/class-pste-semantic-review-sandbox.php`: Kanonisch leere, signierte Originalquelle einmalig NUR bei Abwesenheit atomar per `add_option()` erzeugen, Echtdaten niemals überschreiben.
  - `original/pste/includes/class-pste-sandbox-record-store.php`: die bisher obligatorische Originalstreammigration darf ausschließlich ohne alte Quelle und ohne vorhandenes Manifest/Laufzeitindex diesen kanonischen Leerzustand initialisieren.
  - `original/pste/includes/class-pste-context-refresh.php`: gespeicherten BLOCKED-Kontext nur bei exakt passendem Fehler, Phase, Status, unverändertem Fortschritt, allen geprüften Vorstufen und nachgewiesener fehlender Quelle mit Original-UUID wieder aufnehmen.
  - `texterstellung.php`: Versionsheader und bestehender AJAX-Handler gestatten exakt diese durch die Originalprüfung erlaubte Wiederaufnahme. Andere BLOCKED-Zustände bleiben gesperrt.
- Keine neuen PHP-Dateien, keine K0-, DataForSEO-, MINI-, Kategorie-/Inhalts-/Entwurfs-/Publikationsänderung, keine neue Architektur/zweite Entscheidung.

## Originalcode-Praxistests in PHP-Mocks (NICHT Live-WP)
- Vollständige Original-Sandbox-Streammigration mit leerem, korrekt signiertem frischem Datensatz: 5 originale Statusschritte bis COMPLETE, 0 Datensätze.
- **Gespeicherter Original-PSTE-Kontextauftrag von BLOCKED bis COMPLETE mit derselben Auftragskennung:** echte `PSTE_Context_Refresh::processBatch()`-Methode 12-mal ausgeführt; der ORIGINAL-Sandbox-Store darin echt durchlaufen, spätere Index-/WordPress-Quellen simuliert.
- Tatsächlich von PHP gerenderter Button einschließlich originalem Browser-JS und echtem TXE-PHP-AJAX-Controller simuliert: 2 Requests (start/step) → COMPLETE und Reload. Ungültige Auftragskennung → HTTP 409.
- Ausgangszustand/Sperren 9 Tests; vorhandener 1-Datensatz-Speicher tatsächlich unverändert gestreamt; korrupte vorhandene Quelle **BLOCKED** und nicht überschrieben; vorhandenes Manifest verhindert künstliche Neubefüllung; alte Rohdaten-Migrationsprüfung 12/12 PASS.
- ZIP **87/87 CRC**, PHP **78/78 Syntax**, JSON **8/8** PASS.
- **Kein authentifizierter WP-/MySQL-Produktiv-Endlauf**. Bei weiteren echten Datenmängeln darf nicht blind weitergeklickt oder pauschal eine Prüfung entfernt werden.

## Büro und nächster Schritt
**Bytegleich gesichert und re-materialisiert geprüft:** `/Hobby Depot/Plugin-Büro/Texterstellung_Hobbydepot_0.4.24.5_SANDBOX_LEERBESTAND_FIX.zip`. Zweite Fachablage `/hobbydepot/TEXTERSTELLUNG/INSTALLATIONSKANDIDATEN/`. Eigene `/Hobby Depot/Plugin-Büro/Texterstellung-CURRENT.md` aktualisiert; vorherige 0.4.24.4 bleibt archiviert. Bericht `/Hobby Depot/Plugin-Büro/Texterstellung_0.4.24.5_PRUEFBERICHT.md`.

Nutzerhandlung: WordPress-Sicherung sicherstellen, Plugin 0.4.24.5 über vorhandenes Plugin ersetzen (nicht löschen), `Texterstellung → Recherche → Einrichtung fortsetzen` **einmal**; keine kostenpflichtige Recherche/K0-Produktion und keine erneute Abfrage von Credentials oder alter Diagnose.
