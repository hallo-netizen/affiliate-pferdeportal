# Robotik Kategorie-Workflow 0.4.13 – Sichtbarkeitsblockade im Gesamtablauf korrigiert

**15.11.2026. Aktuelle installierbare Version:** `PLUGIN/CURRENT.zip` = `PLUGIN/VERSIONEN/0.4.13.zip`.

## Nachgewiesener Programmfehler in 0.4.12
- Der alte WordPress-Plan umfasst **104 bereits angelegte Seiten**, deren bisherige Veröffentlichung von `Robotik_Publish` geprüft und ausgeführt wird.
- Die neue Veröffentlichung `Robotik_V65_Publication::preview()` verweigert die Fortsetzung ausdrücklich, wenn nicht **104/104 alte Seiten veröffentlicht** sind.
- Der mit 0.4.12 gebaute einheitliche Gesamtworkflow sprang direkt vom 227er Import zur Veröffentlichung von 68 weiteren Seiten und übersprang die vorhandene **104er-Veröffentlichung vollständig**. Bei noch unveröffentlichten alten Seiten konnte er deshalb nicht erfolgreich abschließen. Bei nicht publizierten Seiten zeigt das öffentliche Strukturdesign folgerichtig keine Links.
- Das ist ein **im Code belegter, konkret behobener Ablaufwiderspruch**, aber noch **kein unabhängig nachgewiesener WordPress-Livezustand**. Auf `robotik.oliver-beil.de` war aus dem verfügbaren Webzugriff kein Readback möglich.

## KISS-Korrektur ohne neues Plugin oder neuen Writer
- Vorhandene Pluginidentität `robotik-kategorie-workflow` von **0.4.12 → 0.4.13** aktualisiert; nur der vorhandene Gesamtcontroller und dessen Versionsmarker/README sind verändert.
- **Einmalige Gesamtfreigabe**, dann vier intern zusammenhängende Phasen: `227 ursprüngliche Importaufgaben → 104 vorhandene Seiten veröffentlichen → 68 neu angelegte Seiten veröffentlichen → 16 weitere Robotertypseiten + 48 Inhaltsrubriken`.
- Die Originalfunktion `Robotik_Publish::advance()` führt die 104er-Veröffentlichung selbst aus; **kein zweiter Veröffentlichungs-Writer**, keine veränderten Original-WP-IDs. Bereits veröffentlichte Seiten werden übersprungen.
- Bei einem gespeicherten alten 104er Status `BLOCKED` ist Wiederaufnahme ausschließlich bei eindeutig identischen 104 WordPress-IDs möglich, sonst sicherer Stopp; bei 0.4.12-Übergang mit Gesamtphase `veroeffentlichen` wird die fehlende 104er Phase zuerst nachgeholt.
- Vorherige Daten und 16/227-Zwischenstand werden nicht zurückgesetzt. Die 16 ursprünglich blockierten Fachseiten sind bereits redaktionell ohne Google-Zieladressen entschieden. Industrie/Gewerbe, Magazin, Glossar, Finder, HivePress, Theme, Designplugin und fremde WordPress-Objekte bleiben unangetastet.

## Nachweis
GitHub Actions **SUCCESS**, Lauf: https://github.com/hallo-netizen/affiliate-pferdeportal/actions/runs/43704446763
- Installations-ZIP `unzip -t` ohne Fehler, `CURRENT.zip` byteidentisch zu `VERSIONEN/0.4.13.zip`.
- **10/10 PHP-Dateien** ohne Syntaxfehler.
- Bytegleiches Paket mit den geänderten Quelltexten.
- Simulation mit gespeichertem Stand **16/227**, inklusive neuer 104er Veröffentlichung, 68er Veröffentlichung und 64er Fachnachtrag, kompletter Abschluss; Doppelaufruf schreibt nicht erneut.
- Negativprüfung: fehlender Kategorienbesitzer blockiert, geändertes Originalmanifest blockiert, unterbrochener 16/227-Lauf bleibt fortsetzbar. 0.4.12-Zwischenphase `veroeffentlichen` korrigiert sich automatisch um die fehlende 104er Phase.
- **Wichtig:** Die CI simuliert WordPress-Zustände. Sie ist keine echte Live-Abnahme des Benutzerportals.

## Verbleibende echte Grenze
Die **öffentliche Darstellung** wird weiterhin vom **vorhandenen Designplugin** `robotik-strukturdesign` gesteuert. Sein letzter dokumentierter Stand ist **0.2.5**, das nur veröffentlichte Seiten für Besucher als Navigation ausgibt und für Administratoren zusätzlich Entwurfsvorschauen erlaubt. Ohne aktive/korrekte Designplugin-Ausgabe, oder solange der neue Gesamtworkflow nicht abgeschlossen ist, kann die öffentliche Startseite trotzdem leer bleiben. **Der aktuelle tatsächliche Aktivierungsstand ist nicht verifiziert.** Keine neue Designversion und keine Frontend-Umbauten auf Verdacht.

## Einziger Nutzerweg
**Nur das bestehende Kategorieplugin auf 0.4.13 aktualisieren.** Danach **Robotik Kategorie → Gesamtabschluss (einmalig)** öffnen und denselben vorhandenen Lauf mit der bereits gespeicherten Freigabe fortsetzen beziehungsweise bei noch nicht erfolgter Freigabe einmal zustimmen. Danach **einen** Gesamtbericht. Keine zusätzlichen SEO-Abfragen.
