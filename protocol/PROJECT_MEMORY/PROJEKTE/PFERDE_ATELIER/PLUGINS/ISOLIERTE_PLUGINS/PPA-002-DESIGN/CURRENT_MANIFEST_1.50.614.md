# PPA-002 – Pferdeatelier Design – Version 1.50.614
Stand: 2026-11-09
Projekt: ausschliesslich Pferdeatelier; Hobbydepot und Hab & Bewahr unberuehrt.

## Original und Update (physische Dateiablage)
Original-Archiv: `/pferdeatelier/PLUGINS/PPA-002-DESIGN/ORIGINAL_1.50.613_20261103.zip`
Original SHA-256: `18697a6f3db41b37a82fe59ca32d3978d42053adb2d3361020ca0518c2dc4659`
Update-Archiv: `/pferdeatelier/PLUGINS/PPA-002-DESIGN/PFERDE_ATELIER_DESIGN_1.50.614_MOBIL_ANMELDUNG_URSACHENFIX.zip`
Update SHA-256: `e15cc9676d172fdbc70372cad21cf164ff42e70f6e60d6451d0b80918eaa7b77`
Die ZIP-Dateien liegen physisch in der persoenlichen Projekt-Dateibibliothek, nicht als Binaerdateien in diesem GitHub-Branch. Keine falsche Behauptung zur GitHub-Archivierung.

## Änderung zum Original 1.50.613
In `affiliate-portal-template-kit/pferde-template-kit.php` wurden nur die Versionsnummern angehoben und die bisher irrtuemlich entfernten HivePress-Basis-Assets fuer Authentifizierungsdialoge vom Pruning ausgenommen. Die restliche Ladeoptimierung bleibt aktiv.
Zusaetzliche mobile CSS-Absicherung: Nur geschlossene Dialoge `#user_login_modal`, `#user_register_modal`, `#user_password_request_modal` sind bei <=767px verborgen. Wenn Fancybox den Dialog mit `.fancybox-content` oeffnet, bleibt er sichtbar.
Alle anderen 503 Dateien sind bytegenau unveraendert.

## Prüfung
Original-ZIP: 504 Eintraege, CRC PASS
Update-ZIP: 504 Eintraege, CRC PASS
PHP-Syntax: PASS
PHP-Quellverhaltensvergleich: notwendige HivePress-Modal-CSS/JS verbleiben, optionales Reviews-Pruning bleibt: PASS
Chromium-Mobiltest 360/390/767px: Ausblenden geschlossen, Anmeldung/Registrieren/Passwort-Fenster aufklappbar: PASS
Desktop-Breiten 768/1200px: mobile Fallback-Regel greift nicht: PASS
Produktiv-Live-Abnahme: PASS laut ausdruecklicher Nutzerbestaetigung am 2026-11-09 ("ok pass"). Einzelne Testschritte wurden vom Nutzer nicht gesondert dokumentiert.

## Abschluss / NEXT ACTION
Stand 2026-11-09: Nutzer hat Version 1.50.614 als PASS abgenommen. Mobiler Footer-/Anmeldemaskenfehler gilt damit fuer diesen Stand als geschlossen.
Keine weitere Reparatur im aktuellen Auftrag offen. Bei einem neuen Fehler erst 1.50.614 und die Originaldatei 1.50.613 aus der Projekt-Dateibibliothek vergleichen; den vorhandenen Code nicht durch eine historische Pluginversion ueberschreiben.
Die ZIP-Dateien bleiben in der Bibliothek, GitHub enthaelt Manifest und Patch; keine Behauptung eines binaeren ZIP-Uploads nach GitHub.
