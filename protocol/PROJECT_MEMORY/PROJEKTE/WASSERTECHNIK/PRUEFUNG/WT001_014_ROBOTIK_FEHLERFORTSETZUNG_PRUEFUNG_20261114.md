# Wassertechnik WT001 0.1.4 – Gesamtprüfung der Fehlerfamilie vom 14.11.2026

## Beleg
- Nutzer-Screenshot WordPress `wasser.oliver-beil.de`: DataForSEO 0.1.3 `PARTIAL_STOPPED_NO_AUTO_RETRY`, **1/3** Anfragen abgeschlossen, **0,09000 USD** bereits gemeldet, **218** W4-Keywordzeilen. Zweiter Auftrag: `dataforseo_labs/google/bulk_keyword_difficulty/live`. Generische Fehlermeldung; **kein gespeicherter tatsächlicher HTTP-/Taskstatuscode**, Ursache beim Anbieter unbekannt.
- Robotik: `/robotik/Konzeptbüro/V60_RELEASE_PRUEFUNG_20261114.md` plus vorhandener `V60_SOURCE_class-robotik-dataforseo.php`, Update **0.4.7**. Dort gelöster Gesamtablauf: gleiche Run-ID und alte Ergebnisse behalten, bei belegter Anbieterstörung nicht wiederholen, als `NICHT_GEPRUEFT` dokumentieren und nur neue Aufgaben unter altem Budget ausführen. **Keine Robotik-Datei geändert**.
- Zusätzlicher **nachgewiesener** Wassertechnik-Programmfehler: Search Intent Live akzeptiert `keywords`, optional `tag` – **kein `language_code`**. 0.1.3 sendete `language_code=de`; 0.1.4 tut das nicht. Original-Doku https://docs.dataforseo.com/v3/dataforseo_labs-google-search_intent-live/ ; DataForSEO-Codeliste: https://docs.dataforseo.com/v3/appendix/errors/

## Umgesetzt, kein Neubau
- W4 218er Keyword-/Owner-Fachplan, Inventurmodul, ZIP-Eintragspfade **byteidentisch zur v0.1.3**, keine neuen WordPress-Import-/Publikationsfunktionen. Gleicher Plugin-Slug `wassertechnik-kategorie-workflow`.
- Alte Optionen `wassertechnik_dfs_013_result`, `wassertechnik_dfs_013_once_lock` und altes Passwort bleiben bestehen. Ein zusätzliches Einmal-Lock verhindert die doppelte Fortsetzung.
- **Spezifische Legacy-Wiederaufnahme** nur bei exaktem 0.1.3-Abbruch, passender Lauf-ID, 218/218 gespeicherten Ownern und identischem W4-Fingerprint. Bewahrt bisherige Suchvolumen-Messwerte. Schwierigkeitsabfrage **niemals wiederholt** und bleibt `NICHT_GEPRUEFT`, da historischer Provider-Code nicht überliefert ist.
- **Nur eine** neue, explizit kostenfreigegebene kostenpflichtige Anfrage für Search Intent. Anbieterlistenschätzung ca. **0,03816 USD**; früher bestätigte **0,09 USD** plus möglicher unbekannter Preis des fehlgeschlagenen Difficulty-Aufrufs werden im 0,25-USD-Budget berücksichtigt.
- Für neue Läufe: API-Fehlerstatus explizit protokollieren, bekannte Anbieterfehler 40101/50000/503xx/50401/HTTP500 als Datenlücke erfassen, keine automatische Doppelanfrage. Tatsächlich ungültige Parameter 40506 blockieren und erscheinen im Export, kein falscher Anbieterfehler. Nach Unterbrechung keine stillen Wiederholungen.

## Einmalige durchgängige Tests
- PHP-Syntax **4/4 PASS**, ZIP CRC / Mitglieder **6/6 PASS**, Quell-W4-Manifest und WP-Inventur bytegleich, kein WP-Content-Writer, kein Cron.
- **11 PHP WordPress-Mock-Szenarien:** (1) exakter alter 0.1.3-Abbruch (Volume + Fehlversuch), (2) Fortsetzungsbutton sichtbar, (3) nur Intent-Payload mit **ausschließlich keywords** ausgeführt, 218 alte Volume-Werte behalten, 218 Intent-Werte übernommen, Difficulty 0 und als Lücke, Kosten im Mock 0,12816 USD; (4) Doppelklick 0 neue POSTs, Bericht unverändert; (5) manipulierte Owner blockieren; (6) Anbieterfehler beim Intent übersprungen; (7) 40506 beim Intent blockiert; (8) neuer Lauf mit 40101 setzt nach übersprungener Schwierigkeit fort; (9) neuer Lauf mit 40506 stoppt vor Intent; (10) HTTP500 ohne JSON bewahrt Volume und setzt beim nächsten zulässigen Auftrag fort, ungemeldete Fehlerkosten reserviert; (11) keine explizite Einwilligung ⇒ 0 POSTs.
- Nur lokal simuliert. **Kein WordPress-Update, keine echte DataForSEO-Zahlung, keine reale Anbieterreaktion durch den Assistenten.**
- ZIP `WASSERTECHNIK_KATEGORIE_WORKFLOW_0.1.4_FORTSETZUNG_OHNE_NEUSTART_NUR_TEST.zip`; SHA256 `73b50022aecde2e3d7fd805acfeb94c7c588489abe85383da0905a5fd5736fd4`; Git-Blob `4a96504b421fd407b718355937b230bf0776bbfc`.

## Ergebnis / nächster einzelner Schritt
**OFFLINE PASS, WORDPRESS-LIVE NOCH OFFEN.** Auf der bestehenden Wassertechnik-Testsite als Plugin-Update installieren, in DataForSEO **„GESPERRTEN LAUF SICHER FORTSETZEN – KEINE WIEDERHOLUNG“** nach Kostenfreigabe ausführen, **einen** SEO-Bericht JSON exportieren. Der Endzustand wird bei offener Difficulty `COMPLETE_WITH_GAPS`, nicht `COMPLETED`, und nie automatisch für WordPress-Import freigegeben.
