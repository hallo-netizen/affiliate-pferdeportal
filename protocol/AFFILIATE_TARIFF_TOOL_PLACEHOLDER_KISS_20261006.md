# Tarifrechner-Platzhalter – KISS-Vertrag 6.72.193

Datum: 06.10.2026

## Ziel

Tarifrechner/Widgets werden zentral in der Affiliate-Zentrale verwaltet und niemals fest in Artikeltexte kopiert.

Verbindliche Kette:

`Rechner einmal im Backend anlegen -> Plugin erzeugt stabilen Platzhalter -> Schreiber setzt nur den Platzhalter -> Runtime setzt den aktuell zentral gespeicherten Rechnercode ein`

## Backend

Eigener Bereich:

`Affiliate-Zentrale -> Tarifrechner`

Pro Rechner werden nur gespeichert:
- Rechnername / fachlicher Typ, manuell vom Administrator definiert;
- vertrauenswürdiger HTML-/Widget-Code;
- aktiv/inaktiv;
- automatisch erzeugte, danach stabile ID.

Der daraus erzeugte Platzhalter ist sichtbar und kopierbar:

`[affiliate_rechner id="kredit"]`

`[affiliate_rechner id="pferdehaftpflicht"]`

Der Anbietername ist bewusst kein Bestandteil des Platzhalters. Ein späterer Anbieterwechsel verändert keinen Artikel.

## Writer-Vertrag

Der Schreiber kennt ausschließlich:
- Rechnername;
- stabile ID;
- Platzhalter.

Der HTML-/Widget-Code wird dem Schreiber nicht übergeben.

Aktive Rechner können intern als kleine Writer-Registry ausgelesen werden. Im WordPress-Backend wird dieselbe Liste sichtbar als kopierbare Platzhalterliste ausgegeben.

## Runtime

- Artikel enthält nur den Shortcode-Platzhalter.
- Der aktuelle zentrale Rechnercode wird beim normalen Rendern automatisch eingesetzt.
- Kein Nachlauf, kein erneutes Befüllen und keine Artikeländerung notwendig.
- Wird der zentrale Code geändert, verwenden alle Artikel beim nächsten Aufruf sofort den neuen Code.
- Wird ein Rechner deaktiviert oder gelöscht, erzeugt sein Platzhalter keine Ausgabe.
- Unbekannte IDs bleiben leer/fail-closed.
- Kein allgemeiner Ersatzrechner/Fallback.

## Datenbank- und Performance-KISS

- keine neue Tabelle;
- keine neue Spalte;
- genau eine kleine gemeinsame WordPress-Option `ppar_tariff_tools_v1`;
- Option ist bewusst **nicht autoload**;
- Seite ohne `[affiliate_rechner]`: **kein Zugriff** auf diese Option;
- Seite mit einem oder mehreren Rechnern: Registry wird **höchstens einmal pro Request** geladen und danach im Request-Speicher wiederverwendet;
- keine Änderung an Banner-, Produkt-, Ranking-, Output-Object- oder URL-Zuordnungshotpaths;
- 6.72.192 Bannerlogik bleibt fachlich und technisch unverändert.

## Trennung Banner / Tarifrechner

Banner bleiben im bestehenden Bereich `Banner & Werbemittel` mit der 6.72.192-Prüf-/Zielkartenlogik.

Tarifrechner erhalten einen getrennten Bereich `Tarifrechner`.

Tarifrechner werden nicht in Bannerrotation, Bannermapping oder Banner-Creative-Library gezwungen.

## Abnahme

Pflichtbeweise vor Installation:
- WordPress + MariaDB;
- Backend-Seite vorhanden;
- individuelle Platzhalter automatisch erzeugt und sichtbar;
- Writer-Registry enthält nur aktive Rechner und niemals HTML-Code;
- normales Content-Rendering ohne Rechner verursacht 0 Tarifrechner-Optionszugriffe;
- mehrere Rechner im selben Request verursachen höchstens 1 Registry-Ladevorgang;
- zentraler Codewechsel wirkt sofort mit unverändertem Platzhalter;
- Umbenennen ändert die bestehende Platzhalter-ID nicht;
- deaktiviert/gelöscht/unbekannt -> leere Ausgabe;
- vertrauenswürdiger Script-/Iframe-Code wird nicht zerstört;
- keine neue Tabelle;
- Option nicht autoload;
- bestehende 6.72.192 Runtimequellen außerhalb der ausdrücklich kleinen Integrationspunkte bytegleich;
- finaler ZIP Fresh-Unpack und WordPress/MariaDB-Test.


## Abnahmeergebnis

Source WordPress/MariaDB:

- Run `37471777928` = SUCCESS.
- 6.72.192 Runtime außerhalb der exakten Tarifrechner-Verdrahtung unverändert.
- normale Inhalte: 0 Tarifrechner-Optionszugriffe.
- mehrere Rechner in einem Request: 1 Registry-Ladevorgang.
- zentrale Codeänderung ohne Artikeländerung wirksam.
- Option nicht autoload.
- keine neue Tabelle.

Exaktes Final-ZIP:

- Run `37472204233` = SUCCESS.
- Fresh-Unpack 28/28 Byteidentität.
- PHP-Lint 22/22.
- kompletter Tarifrechner-Test PASS.
- kompletter 6.72.192 Tarifcheck-Bannervertrag erneut PASS.

Finaler Installer:

`release/affiliate-zentrale/artifacts/final/AFFILIATE_ZENTRALE_6.72.193.zip`

SHA-256:

`1390374ce27c5acfe0cacf1f6ef593d75142c65090b3742c73504e9e0d1d7d27`

Größe: `805229 Byte`.
