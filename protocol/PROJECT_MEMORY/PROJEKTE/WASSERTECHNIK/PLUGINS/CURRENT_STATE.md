# WASSERTECHNIK / PLUGINS – einzige aktuelle Büroautorität

**Stand:** 14.11.2026 · **Status:** WT001 **0.1.4 – gesicherte Fortsetzung des echten 0.1.3-Abbruchs** lokal vollständig geprüft; echter WordPress-Update-/Anbieter-Test noch OFFEN.

**Aktueller Kandidat:** `WASSERTECHNIK_KATEGORIE_WORKFLOW_0.1.4_FORTSETZUNG_OHNE_NEUSTART_NUR_TEST.zip`, SHA256 `73b50022aecde2e3d7fd805acfeb94c7c588489abe85383da0905a5fd5736fd4`, Git-Blob `4a96504b421fd407b718355937b230bf0776bbfc`. Gleiches WordPress-Plugin `wassertechnik-kategorie-workflow`; kein zweites Plugin. Keine Neuinstallation, kein Reset, kein Import.

## Belegte Ursache und konsequente Reparatur
- WordPress-Screenshot vom 14.11.2026: Version 0.1.3 `PARTIAL_STOPPED_NO_AUTO_RETRY`, 1/3 bezahlt erledigt, **0,09000 USD** vom Anbieter ausgewiesen, 218 gespeicherte Keyword-Zeilen. Zweiter Auftrag `dataforseo_labs/google/bulk_keyword_difficulty/live` meldet Fehler, der vollständige Aufrufstop blockiert den dritten Auftrag.
- **Ursache des zweiten Anbieterfehlers nicht belegbar:** Das alte Plugin verwirft bei diesem Fehler den tatsächlichen Anbieterstatuscode und zeigt nur generischen Text. Kein unbelegter Schluss auf 40101/50000 oder ungültige Felder.
- **Belegter weiterer Pluginfehler:** 0.1.3 übergibt `language_code=de` an DataForSEO `dataforseo_labs/google/search_intent/live`, das laut Anbieter nur `keywords` und optional `tag` annimmt. Dieser unzulässige Parameter ist in 0.1.4 entfernt. Quelle: https://docs.dataforseo.com/v3/dataforseo_labs-google-search_intent-live/
- **Robotik-Fix übernommen, ohne Robotik umzubauen:** 0.4.7 im Robotik-Konzeptbüro behandelt nachweisbare Anbieterstörungen separat, erhält alte Messwerte, wiederholt Fehleraufträge nicht und erlaubt eine manuell bestätigte Fortsetzung; fachliche Lücken bleiben als `NICHT_GEPRUEFT` ausgewiesen.

## Einziger konkreter WordPress-Nutzerweg
1. **Als Update** 0.1.4 über die installierte 0.1.3 legen. Bereits vorhandene WordPress-Optionen, 218 W4-Owner, gespeicherte Suchvolumen-Zeilen, ursprüngliche Lauf-ID, Zugangsdaten und Budget bleiben unverändert.
2. `Wassertechnik Kategorie → DataForSEO`: neue Aktion `GESPERRTEN LAUF SICHER FORTSETZEN – KEINE WIEDERHOLUNG`, einmalige Kostenfreigabe für **nur die noch offene Suchabsicht** (Anbieterlistenschätzung 0,03816 USD). Bereits gezahlte 0,09 USD und fehlgeschlagene Schwierigkeit werden **NICHT** erneut abgefragt.
3. Danach `Gesamten SEO-Bericht als JSON herunterladen`. Endstatus `COMPLETE_WITH_GAPS` – organische Schwierigkeit bleibt `NICHT_GEPRUEFT`, niemals als SEO-PASS ausgegeben. Unbekannte mögliche Altgebühr der Fehlanfrage wird vorsichtig im bestehenden 0,25-USD-Budget reserviert.

**Harte Schutzprüfung:** Exakter alter Zustand, 218/218 Owner-/Keyword-Übereinstimmung, W4-Prüfsumme, gespeicherte ursprüngliche Lauf-ID/Lock, 1/3 Resultate und ursprünglicher 0.1.3-Fehlertext müssen übereinstimmen. Zweites dauerhaftes Fortsetzungs-Lock sperrt Doppelklick und kostenpflichtige Wiederholung. Ungültige API-Parameter `40506` stoppen sichtbar mit Status, belegte Anbieterfehler wie `40101`, `50000` und HTTP-500 werden ohne Doppel-POST als Lücken ausgewiesen und die übrigen Schritte nur innerhalb Restbudget fortgesetzt.

**Nachweis:** 4/4 PHP-Lint, 6/6 ZIP-CRC, Original-W4-SEO-Manifest und WP-Inventurmodul bytegleich, 11 lokale PHP-/WordPress-Mock-Szenarien PASS (einschließlich exakt reproduziertem 0.1.3-Abbruch, einmaliger Fortsetzung, Providerfehlern, HTTP-500, 40506, Manipulation, Doppelklick und fehlender Zustimmung). Details `../PRUEFUNG/WT001_014_ROBOTIK_FEHLERFORTSETZUNG_PRUEFUNG_20261114.md`.

**NEXT ACTION:** Einmal Update auf 0.1.4 in der bestehenden Wassertechnik-WordPress-Testsite, ausdrücklich bestätigte **Fortsetzung ohne Wiederholung** anklicken, **einen** SEO-Gesamtbericht exportieren. Keine neue Dreifachrecherche, kein Import und kein neuer Keywordsatz. Alle echten SEO-Ergebnisse erst aus dem Export auswerten.
