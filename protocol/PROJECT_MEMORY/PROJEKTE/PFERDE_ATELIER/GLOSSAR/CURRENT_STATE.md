# BÜRO GLOSSAR – CURRENT_STATE

STAND: 2026-09-14
STATUS: EINZELARTIKELANZEIGE LIVE PASS / EINZELANSICHT + FLIESSTEXTLINKS LIVE FAIL / TECHNISCHE NACHBESSERUNG 1.2.2 + 1.50.490 LOKAL PASS, NICHT LIVE

## Belastbarer aktueller Stand

- Büro `GLOSSAR` steuert das öffentliche Pferde-Atelier-Glossar.
- Fachwahrheit bleibt ausschließlich in `../WISSENSDATENBANK/AKTENSCHRAENKE/GLOSSAR/`.
- Öffentlicher Begriffstyp: `uge_term`; Glossar-Oberbereiche: `uge_group`.
- Arbeitsbranch: `hobbyroom/glossar-livefail-red-green-20260913`.
- Der funktionierende Single-Routingweg bleibt unangetastet.

## LIVE bestätigt

Der Nutzer bestätigte `artikelanzeige pass`. `GLOSSAR-ROUTE-004` ist damit real geschlossen: Einzelbegriffe öffnen.

## Aktueller LIVE FAIL – Nutzerreadback 2026-09-14

Am realen Glossar-Single ist weiterhin fehlerhaft:

1. Breadcrumbs stimmen nicht; im Screenshot erscheint die Oberbereichskette falsch/doppelt.
2. Im Fließtext sind weiterhin Links sichtbar.
3. Der ockerfarbene obere Strich der rechten Blöcke ist zu dick.
4. Auch bereits vorhandene Glossarbeiträge müssen nach der neuen Regel gezielt überschrieben/aktualisiert werden.

Verbindliche neue Regel: **Im Glossar-Fließtext exakt 0 Links.** Verwandte Begriffe werden ausschließlich rechts in `Verwandte Begriffe`, das Portalziel ausschließlich rechts in `Mehr zum Thema` verlinkt.

## Lokale technische Nachbesserung – noch kein LIVE-PASS

### Glossar Core 1.2.2

Paket:
`UNIVERSAL_GLOSSARY_ENGINE_1.2.2_ZERO_BODY_LINKS_BESTAND_UPDATE_INSTALLIEREN.zip`

SHA-256:
`3d6ffc2cdfcc4872e49e97f4adc54de31d4ef2714b0af07e399a681f15d1f447`

Geändert:
- 14 gebundene Glossartexte werden mit 0 Fließtextlinks erzeugt;
- bestehende `uge_term`-Datensätze werden zusätzlich linkfrei zurückgeschrieben, ID bleibt erhalten;
- normale WordPress-Posts sind hart ausgeschlossen;
- State auf `1.2.2:14`, damit ein vorhandener 1.2.1-Bestand erneut durch den Updateweg läuft.

Lokal ausgeführt:
- PHP-Lint Core-Dateien → PASS;
- 14 Begriffe, jeweils 150–200 Wörter → PASS;
- 0 `<a>`-Links in allen 14 Fließtexten → PASS;
- Related-Relationen bleiben vorhanden → PASS;
- bestehende ID `77` im positiven Update-Test erhalten → PASS;
- absichtlich mitgelieferter normaler Post im Negativtest nicht verändert → PASS;
- ZIP-Lesetest → PASS;
- Version 1.2.2 aus ZIP → PASS.

Marker:
- `CORE_122_ZERO_BODY_LINKS_POS_NEG_PASS`
- `CORE_122_EXISTING_ID_PRESERVE_AND_NORMAL_POST_NEG_PASS`

### Pferde Atelier Design 1.50.490

Paket:
`PFERDE_ATELIER_DESIGN_V1.50.490_GLOSSAR_BREADCRUMB_STRIPE_FIX_INSTALLIEREN.zip`

SHA-256:
`251e90a7c7115cd4ce166ddefb5f0918904f28b89d85f2a173c190201b454657`

Geändert:
- globaler Universal-Breadcrumb wird auf `uge_term` bereits serverseitig gar nicht mehr erzeugt;
- eigene Single-Kette bleibt `Startseite > Glossar > Oberbereich > Begriff`;
- zusätzliche CSS-Sperre blendet jeden globalen Breadcrumb-Rest auf `uge_term` aus;
- Render-Endschranke entfernt jeden eventuell verbliebenen Link aus dem Fließtext;
- obere Ockerlinie der rechten Boxen von 4 px auf 2 px reduziert;
- Scope ausschließlich `uge_term`, normale Posts bleiben außen vor.

Lokal ausgeführt:
- PHP-Lint → PASS;
- Breadcrumb-/Scope-/0-Link-/2px-Vertrag positiv/negativ → PASS;
- ZIP-Lesetest → PASS;
- Version 1.50.490 aus ZIP → PASS.

Marker:
`DESIGN_150490_BREADCRUMB_ZERO_LINKS_THIN_STRIPE_POS_NEG_PASS`

## Harte Grenze

**Noch kein LIVE PASS.** Die neuen Paketbytes sind lokal gebaut und geprüft, aber noch nicht im realen Pferde-Atelier installiert/readback-bestätigt. Die bisherige Plugin-Artefaktquelle im PLUGINS-Büro darf deshalb nicht als LIVE-Nachweis interpretiert werden.

## Nächster belastbarer Schritt

1. Core `1.2.2` und Design `1.50.490` über die vorhandenen Pluginstände installieren.
2. Bestehenden Begriff `Bandmaß` neu laden und real prüfen:
   - Breadcrumb exakt `Startseite > Glossar > Pferd & Biologie > Bandmaß`;
   - Fließtext 0 Links;
   - `Stockmaß` rechts in `Verwandte Begriffe` als Link;
   - Portalziel rechts in `Mehr zum Thema`;
   - obere Ockerlinie der rechten Boxen sichtbar dünner;
   - Bestands-ID/URL unverändert.
3. normalen WordPress-Beitrag gegenprüfen.
4. Erst nach realem Readback LIVE PASS setzen und danach Plugin-Artefaktpflicht final synchronisieren.

Neue Glossarbegriffe weiterhin nur aus frisch nachgewiesenen `GEPRUEFT`-WDB-Quellen.
