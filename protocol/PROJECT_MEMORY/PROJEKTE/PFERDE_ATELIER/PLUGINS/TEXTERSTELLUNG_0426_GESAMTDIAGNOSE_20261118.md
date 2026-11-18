# Pferdeatelier – Texterstellung 0.4.26 Gesamtdiagnose
Stand 18.11.2026. **Nur Testinstallation, keine Live-Freigabe.**
- Basis: 0.4.25 (bereits aus vom Benutzer hochgeladenem Pferdeatelier-Original 0.4.24 gebaut).
- Ursache bisher gesichert: WordPress meldet bei zwei echten K0-Artikeln `empty_content`. Der konkrete Filter/Owner auf oliver-beil.de ist noch **nicht** bestimmt.
- Neue Diagnose: erfasst die tatsächlichen Originalargumente zum WP-Schreibaufruf (nur Bytes/Hash), WP-Leerfilter vor und nach Fremd-Callbacks, Hook-Inventar mit Herkunft, Post-Datenfilter, SQL-Schreibversuch ohne SQL-Text, WP_Error, Rücklese-/Auftragsstatus.
- 14 Prozessbereiche im Bericht: Umgebung, Recherche/Provider, Kategorien, Redaktion, K0-Ausgabe, Datei-Upload, Normalisierung, WP-Argumente, Leerfilter, Datenfilter, Datenbank, Ergebnis, Rücklesen/Auftrag und Fehler/Abschluss.
- Nur tatsächliche Belege; nicht beobachtet ist KEIN PASS. Externe K0-Texterstellung nicht aus WordPress heraus inspiziert, nur Datei-Ein-/Ausgang.
- Physisches vollständiges ZIP im Pferdeatelier-Plugin-Büro: `/pferdeatelier/PLUGINS/ARBEITSRAUM_PSTE_KISS/Texterstellung-0.4.26-GESAMTDIAGNOSE-PFERDEATELIER-TEST.zip`.
- SHA-256 `3a76597e990b888ddc4d58fabd6b25149ced6b9ef28fdc0302121b706f603bfb`. 88 Dateien, 84 von 0.4.25 bytegleich. 78/78 PHP-Syntax, 35/35 gezielte Funktionstests mit den originalen zwei K0-Artikeldateien (WordPress nachgebildet), ZIP CRC OK.
- Das Nachstellen eines Fremdfilters bewies den richtigen Diagnosebeleg: Core-Leerwert springt `false → true` trotz mehr als 9000 Bytes Inhalt; nach Entfernen dieses simulierten Filters werden dieselben Artikel korrekt importiert. **Das ist kein Beweis, dass der echte Testserver denselben Filter hat.**
- Kein Live-Test durchgeführt. Einziger nächster WordPress-Test: auf oliver-beil.de 0.4.26 über bestehendes Plugin installieren (nicht löschen), unveränderte 2-Artikel-JSON einmal zurückimportieren, Texterstellung → Diagnose → JSON herunterladen.
- Unverändert: K0, Artikeltext, Redaktion, WordPress-Liveportal, Originaldateien 0.4.24 und 0.4.25. Keine zusätzlichen Entscheidungen.
- Hobbydepot/Hab & Bewahr: 0.4.26 ist **nur Pferdeatelier**; keine ungeprüfte Übernahme und keine Kopie über dortige Plugin-Versionen.
- Prüfbericht und JSON-Prüfwerte sind im selben Plugin-Büro gespeichert.
