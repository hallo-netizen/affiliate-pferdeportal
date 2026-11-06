# Pferdeatelier MINI – geprüfte Original-ZIP / 87er Ursachenbefund

**Stand: 06.11.2026 · nur Nachweis und Arbeitsauftrag, KEIN Plugin-Installer, KEIN Fix.**

## Originalquelle
Vom Nutzer im Chat am 06.11.2026 hochgeladen und lokal erfolgreich geöffnet:
`PFERDEATELIER_PSTE_0.57.144.12_MINI_ZUM_REDAKTIONSPLAN_NUR_TEST.zip`.
Größe 627.824 Bytes, SHA256 `fac094d994276608453ed4a731b49212528fe71184823f3885127e4ee6f16bd9`.
Die ZIP ist *nicht* diesem GitHub-Branch beigefügt; Binary-Upload mit den verfügbaren GitHub-Werkzeugen nicht möglich. Library-Upload scheiterte an vollem Speicher. Diese Notiz **nicht als erfolgreiche ZIP-Ablage** ausgeben. Bei späterem Dateizugriff Originalprüfung über die genannte SHA durchführen.

## Originalcode tatsächlich untersucht
`Portal SEO Topic Engine/includes/class-pste-mini-workflow.php`, `class-pste-repository.php`, `class-pste-admin.php`, `class-pste-normal-metadata-path.php`, `class-pste-title-pipeline.php`.

Die MINI-Schnittstelle speichert bei JA genau den ersten Titel pro Keyword und lässt zehn weitere Ideen im Zwischenspeicher. NEIN / VIELLEICHT gehen **nicht** in die Planung. Über `forwardToPlan` wird nur ein Titel mit Quellbeleg an `saveManualTitleOverride` geschrieben und die normale bestehende `scheduleTitleDeskReentry` gestartet. **Das externe JA wird nicht als gebundener Relevanzbeleg übergeben.** Der alte Themenweg verlangt deshalb erneut eigenen Relevanzbeleg. Er prüft außerdem Titelbindung, Kategorie und bestehende Planstellen.

## Gesicherter tatsächlicher TEST-Bestand (06.11.)
100 Keywords: 87 JA, 9 VIELLEICHT, 4 NEIN. 97 Titelideen, davon 87 erster Titel weitergegeben. 87/87 Reentry verarbeitet, 0 pending, 7 PASS, 78 HELD, 2 BLOCKED, kein Transportfehler.
Diagnose in Campus PLUGINS:
`EVIDENCE/pste-gesamtdiagnose-2026-11-06.json`
und `EVIDENCE/PSTE_MINI_REIMPORT_URSACHENBEFUND_20261106.json`.
50 Kategorien offen; 7 Relevanzbeleg erneut nötig; 6 Sprachtitel erneut verlangt; 3 Titelbeleg-Konflikte; 12 Planungssperren; 1 Produktwahl; 1 Familienlücke; 7 PASS. Diese Gruppen sind disjunkt.

## Ursache und nächster Schritt
Gemeinsame Schnittstellenursache: Titel/Quellbeleg wird gespeichert, die extern getroffene Relevanzentscheidung **nicht fachlich gebunden** durchgereicht. Der bestehende Themen-Owner berechnet erneut und kann alte Titelbelege bzw. unentschiedene Kategorien/Planungsfragen vorfinden. Ein gespeicherter Titel ist noch kein Artikelauftrag. **Nicht** behaupten, 50 WordPress-Kategorien fehlten, dass alle 12 Planungsblockaden falsch seien oder dass 80 Titel verloren seien.

Nächster Schritt: Exakte Quell-ZIP dauerhaft an GitHub binden; vorhandene Reentry-Schnittstelle ursächlich und minimal korrigieren (quellengebundene JA- und Titelbelege, alte überholte Zustände nur kontrolliert ersetzen, keine Doppel-Sprachprüfung). Mit den gleichen 87 Eingaben und echten WordPress-Terms an einem vollständigen TEST-Ablauf verifizieren; reale Dubletten weiterhin blockieren. K0, PSERC und LIVE unverändert halten. Keine erneute Keyword-Recherche, keine erneute Titelerstellung, kein blindes Plugin-Update.

**GitHub-Schutz:** Dokumentation auf separatem Branch, kein Main-/CURRENT-Update ohne Review.
