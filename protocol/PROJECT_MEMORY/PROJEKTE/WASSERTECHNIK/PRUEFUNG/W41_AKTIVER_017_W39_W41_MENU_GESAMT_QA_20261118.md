# W41 – Wiederaufnahme ab wirklich installiertem WT001 0.1.7 (18.11.2026)

## Verifizierter Ausgangsstand
- Nutzer hat die aktive Pluginzeile von `wasser.oliver-beil.de` gezeigt: `wassertechnik-kategorie-workflow` Version **0.1.7**. Das ist jetzt verbindlicher Installationsstand, nicht mehr als „unbekannte Version“ beschreiben.
- W11-Originalprüfprotokoll (PR #785): sieben damalige Navigationsbereiche, 79 Altprodukt-Owner, die ursprünglichen 218 SEO-Owner, zwei nach Freigabe umzuhängende Teilbäume und 17 Redirects. Der damalige 0.1.7-Quell-ZIP war ausschließlich ein Chat-Artefakt; in den geprüften Wassertechnik-Library-/GitHub-Archiven nicht wiedergefunden. Version und dokumentierte **Funktion** sind belegt, die damaligen **Originalbytes** nicht.
- Der Nutzer lehnt eine zusätzliche W40-Diagnoseplugin-Installation ausdrücklich ab. Keine neue Export-, Upload- oder Diagnoseanforderung. Keine automatische WordPress-Verbindung behaupten.

## Tatsächliche W41-Gesamtänderungen
- W39-Gesamtbau 0.1.10 unter derselben bestehenden Pluginidentität als **ein** W41-Gesamtbau 0.1.11 fortgeführt; kein zweites Plugin und keine neue fachliche Entscheidung.
- Konkrete aus W11/W39-Historie gefundene Menü-Lücke geschlossen: zuvor nur optionaler Shortcode, keine automatische sichtbare Frontend-Ausgabe, Pool-Hauptbereich wegen noch fehlender veröffentlichter Produkte ausgeblendet, die acht Spezialprodukte nicht in der Ausgabe. Jetzt **sieben kaufnahe W27-Hauptbereiche plus ein separater Fachtechnik-Zugang**. Weiterhin 79 echte Alt-Owner-Produktlinks: 71 kaufnahe und acht Fachtechnik. Keine fiktiven Pool-Links. Die Menüausgabe erfolgt einmalig in `wp_body_open`, wird bei schon verwendetem Shortcode nicht dupliziert; auf Mobilgeräten per native Details aufklappbar.
- Datensicherung: Nur bei `publish` und korrekter `_wt_owner_id` werden Links ausgegeben; alte und neue Besitzerpfade bleiben berücksichtigt. Inhalt und WP-Eigentümer werden durch Navigation **nie** geschrieben.
- Der tatsächliche Startbildschirm wurde korrigiert: Der **nur nach eigener ausdrücklicher Freigabe** mögliche W35-Strukturimport wird nicht mehr irreführend als dauerhaft „deaktiviert“ bezeichnet.
- W35 bleibt der einzige WordPress-Schreiber mit 219 Zielen (114 Seiten inkl. Pool-Hub-Entwurf + 105 Kategorien), 218 unveränderten alten Zuordnungen und 17 adressgeschützten Umstellungen. Alte Neuner-Importeraktion nicht aktiv; keine automatische Import-/Publikationsaktion.
- Die 218er-SEO-Quellen und Fingerprint bleiben gesperrt und unverändert. Die 81 neuen Kandidaten bleiben getrennt und ohne neue bezahlte Abfrage / automatische Inhaltsfreigabe.
- Kein Eingriff in WordPress; keine DataForSEO-Kosten.

## Technischer Gesamtnachweis
- GitHub-PR #820; Actions-Run **44280215525: success** (18.11.2026).
- Bestehende W33-Gesamtregression (Original 218/SEO, Fingerprint, 81-Kandidaten, Hauptstruktur), **10/10 W41-Navigationstests**, **10/10 W35-WP-Import-/Rollback-Szenarien**, **15/15 W38/W39-Provider-/SEO-UI-Szenarien**, Zielvertragsprüfung, PHP-Lint, ZIP-CRC: **PASS**.
- Technisches CI-Artefakt `WASSERTECHNIK_WT001_0.1.11_W41_GESAMTPRUEFUNG_NICHT_INSTALLIEREN.zip`: 16 Dateien, CRC gültig, SHA-256 `cc3e0fa5959d8469be13fb9d031c6279b9be1234395772e7d59c286f2870da07`. Es ist eine **geprüfte Offline-Rekonstruktion**, noch keine live getestete 0.1.7-Überschreibung.
- Prüfung der **damaligen Originalbytes von 0.1.7** bleibt mangels Datei unmöglich. Dieser bekannte Unterschied wird offen benannt; keine Behauptung einer tatsächlich erfolgten WP-Testinstallation. Der historische W11-Funktionsumfang wurde gezielt in die Tests integriert.

## Arbeitsregel für Fortsetzung
Keine W40-Diagnose-ZIP anfordern. W41-Entwicklung und Regression auf GitHub sind vorhanden, nicht nochmals von vorne beginnen. Eine echte WT001-Installation/WordPress-Freigabe nicht als ausgeführt behaupten; Nutzerdaten nicht mutieren. Kein weiterer Diagnoselauf, keine neue separate Pluginlinie, keine alten 218er-SEO-Kosten. Das Ziel bleibt **ein** konsolidiertes WT001-Gesamtupdate.
