# Robotik V59 – Plugin 0.4.6: Weiterarbeiten trotz DataForSEO-HTTP-500 ohne Wiederholungsgebühren

**14.11.2026 · Status: lokal funktionsgeprüftes Test-Update; kein WordPress-Live-Lauf und keine echte DataForSEO-Abfrage aus dieser Entwicklung.**

## Beleg und tatsächliche Ursache
- Der laufende WordPress-SEO-Gesamtauftrag (0.4.5) erreichte **3 von 38 abgeschlossenen Aufträgen** und **0,1135 USD vom Anbieter bestätigte Kosten** (Screenshot 14.11.2026 13:46).
- Der folgende **4. Auftrag** ist **Keyword Ideas für Freizeit**, mit **14** Seed-Keywords, `limit=300`, `location_name=Germany`, `language_code=de`. Diese Felder liegen innerhalb der DataForSEO-Grenzen (maximal 200 Seed-Keywords, Limit maximal 1000). Daher **kein belegter Eingabe- oder Zugangsdatenfehler**. Datenlieferung des gescheiterten Auftrags nicht vorhanden. Der WordPress-Status ist `BLOCKED_UNCERTAIN` wegen DataForSEO-HTTP-500.
- Das alte Plugin 0.4.5 konnte lediglich den **ersten** fehlgeschlagenen Auftrag (Index 0) einmalig wiederholen. Nach drei erfolgreichen Ergebnissen gab es keinen Wiederaufnahmeweg. **Dies ist der konkret nachgewiesene Plugin-Funktionsmangel.**

## Funktionsänderung – KEINE Neuarchitektur
- Bestehende Pluginidentität `robotik-kategorie-workflow`, Versionsschritt **0.4.5 → 0.4.6**.
- Bei exakt passendem gespeicherten Fehlerstand (gleiche Run-ID, letzte Aufgabe/Typ/Welt, 3 bereits gespeicherte Anbieterantworten, aktuelle V52-Planprüfsumme, keine laufende Abfrage) im WordPress-Menü **einmalige Fortsetzung mit ausdrücklicher Freigabe**.
- Der **fehlgeschlagene Freizeit-Auftrag wird NICHT erneut gesendet**; nur als `NICHT_GEPRUEFT` im Gesamtbericht markiert. Alle bereits bezahlten Ergebnisse und 0,1135 USD als gespeicherter Anbieter-Kostenwert bleiben erhalten.
- Danach die **noch offenen Teilaufträge** unter **derselben** ursprünglichen Run-ID und Budgetobergrenze abarbeiten. Weitere **tatsächliche Anbieter-HTTP-500er** bei Keyword Ideas oder SERP werden nur einmal **als Lücke** erfasst, nicht nochmals angefragt; andere Fehler/unsichere Abbrüche stoppen weiterhin.
- Unsichere mögliche Anbieter-Abbuchungen werden vorsichtshalber gegen das frühere Budget **mit dem jeweiligen Reservewert** gerechnet, darunter der erste fehlgeschlagene Overview-Aufruf. Ein Budget darf nicht durch fehlende Fehlerantworten unbegrenzt belastet werden. Dies ersetzt keine spätere Überprüfung der Anbieterabrechnung.
- Falls ein oder mehrere Teilaufträge fehlen, Abschlussstatus **`COMPLETE_WITH_GAPS`** mit vollständiger Lückenliste; **nie** als vollständige Google-/SEO-Prüfung ausgeben. Die 16 HOLD-Vergleiche ohne SERP-Daten bleiben `NICHT_PRUEFBAR`, nicht freigegeben.
- **Kein** Frontendwechsel, kein WP-Inhaltsimport, keine Änderung an freigegebenen 437 Suchbegriffen, alten URLs, Seiten, Kategorien oder Benutzerzugängen. Kein neues Plugin, keine neue Datenbanktabelle.

## Testnachweise
- Alle **437** vorhandenen Keywords und der ursprüngliche **38er-Plan** unverändert; 4. Teilauftrag nachgerechnet: `ideas / Freizeit / 14 Seeds`.
- **5 von 5 PHP-Lint bestanden**, ZIP-CRC/ZIP-Einträge **PASS**, genau 8 Dateien.
- Alle bisherigen **3 unveränderten PHP-Module**, beide JSON-Plan-Assets und der historische Import-/Veröffentlichungspfad aus 0.4.5 **bytegleich** erhalten. Geändert nur das bestehende DataForSEO-Include, die Versionsangaben im Haupteintrag und das README.
- Simulierter WordPress-Lauf mit bereits **3 erledigten echten-Struktur-Aufträgen**, 0,1135 USD gespeichert, gescheitertem Freizeit-Auftrag (Index 3), erstmals zulässiger Weiterführung: **Index springt auf 4** ohne Provider-Aufruf für Index 3.
- Negativtests: keine Wiederaufnahme bei unpassendem vorherigen Auftrag, bei HTTP 200 mit unlesbarer Antwort, ohne gespeicherte drei Ergebnisse, bei nochmaligem Benutzerklick. Bei weiteren simulierten HTTP-500ern an Index 5 und 7 jeweils **nur ein** Provider-Aufruf, kein zweiter; Abschluss **38/38 mit 3 offen ausgewiesenen Lücken**, 35 erfolgreiche/gespeicherte Teilaufträge.
- Budget-Negativtest: auch ohne genau bestätigte Kosten für bereits fehlgeschlagene Aufträge **kein weiterer API-Aufruf**, sobald der vorsichtig reservierte Kostenrahmen die ursprüngliche Grenze erreicht.

**Installer:** `PLUGIN/CURRENT.zip` = `PLUGIN/VERSIONEN/0.4.6.zip`, **57.028 Bytes**, SHA256 `1c6517a1bab3efea1214fdb3336de975c1a357049a2969dd72c21081595cbb2b`. Library Backup: `/robotik/Konzeptbüro/ROBOTIK_KATEGORIE_WORKFLOW_0.4.6_FEHLERSICHERE_FORTSETZUNG_TEST.zip`.

**Nutzerweg:** Altes Plugin **mit derselben Identität** auf Version 0.4.6 aktualisieren. Menü `Robotik Kategorie → DataForSEO` öffnen. Nur **`Mit gespeicherten Ergebnissen fortfahren – Fehler nicht wiederholen`** plus ausdrückliche Bestätigung verwenden. Browser geöffnet lassen. Danach **EINEN SEO-Gesamtbericht als JSON** bereitstellen. Dabei können neue Datenkosten im verbleibenden, ursprünglichen Budget anfallen. Keine Wiederholung des Freizeit-Auftrags. Keine Freigabe für WP-Import.