# Affiliate Router 6.72.193 — Tarifrechner-Platzhalter KISS

Datum: 06.10.2026

## Ziel

Tarifrechner/Widgets werden getrennt von Bannern zentral verwaltet.

Verbindliche Kette:

`Rechner im Backend anlegen -> stabilen Platzhalter automatisch erzeugen -> Schreiber setzt nur Platzhalter -> Runtime setzt aktuellen zentralen Code automatisch ein`

## Implementierung

Eigener Backend-Bereich:

`Affiliate-Zentrale -> Tarifrechner`

Pro Rechner:
- Rechnername / Typ;
- vertrauenswürdiger HTML-/Widget-Code;
- aktiv/inaktiv;
- stabile automatisch erzeugte ID;
- sichtbarer Platzhalter wie `[affiliate_rechner id="kredit"]`.

Artikel enthalten niemals den Widget-Code.

## Writer-Vertrag

Die aktive Writer-Liste enthält ausschließlich:
- Name;
- ID;
- Platzhalter.

Der HTML-Code wird nicht an den Writer ausgegeben.

Backend zeigt die aktive Platzhalterliste sichtbar und kopierbar an.

## Runtime

- Shortcode wird beim normalen WordPress-Rendern automatisch ersetzt.
- Kein Nachlauf.
- Keine Artikelmutation.
- Zentraler Codewechsel wirkt beim nächsten Seitenaufruf auf alle Artikel mit demselben Platzhalter.
- Umbenennen verändert die einmal erzeugte ID nicht.
- deaktiviert / gelöscht / unbekannt -> leere Ausgabe, kein Fallback.

## Datenbank / Performance

- keine neue Tabelle;
- keine neue Spalte;
- eine kleine Option `ppar_tariff_tools_v1`;
- Option nicht autoload;
- normale Inhalte ohne Rechner: 0 Zugriffe auf diese Option;
- mehrere Rechner im selben Request: genau 1 Registry-Ladevorgang, danach Request-Cache;
- keine Änderung an Banner-, Produkt-, Ranking-, Output-Object- oder URL-Zuordnungshotpaths.

## Isolationsbeweis gegen 6.72.192

Basiscommit des exakt getesteten 6.72.192-Plugins:

`aa3bdbbae8520d6f5e9bd517be0d9325169177f8`

Im Plugin-Sourcebaum änderten sich ausschließlich:
- neue Datei `includes/trait-ppar-tariff-tools.php`;
- fünf kleine Verdrahtungspunkte plus Versionsnummer in `pferdeportal-affiliate-router.php`;
- `readme.txt`.

Nach Entfernen genau dieser Verdrahtung und Rücksetzen der Versionsnummer ist die Hauptdatei bytegleich zur getesteten 6.72.192-Hauptdatei.

## Source WordPress/MariaDB

Run `37471777928`: SUCCESS.

PASS:
- 6.72.192 Runtime außerhalb der Tarifrechner-Verdrahtung unverändert;
- PHP-Lint 22/22;
- Backend-Seite vorhanden;
- Platzhalter sichtbar;
- Writer-Registry nur aktive Rechner, ohne HTML-Code;
- normale Inhalte: 0 Tarifrechner-Optionszugriffe;
- mehrere Platzhalter: 1 Registry-Ladevorgang;
- Script-/Iframe-Code bleibt unverändert;
- zentrale Codeänderung wirkt sofort;
- Platzhalter bleibt bei Umbenennung stabil;
- inaktiv/unbekannt -> leer;
- keine neue Tabelle;
- Option nicht autoload.

## Exaktes finales ZIP

Run `37472204233`: SUCCESS.

PASS:
- Source-Manifest 28 Dateien;
- Fresh-Unpack 28/28 Byteidentität;
- PHP-Lint 22/22;
- exaktes ZIP frisch in WordPress 7.1.2 + MariaDB 10.11 installiert;
- kompletter Tarifrechner-KISS-Test auf exakt diesem ZIP PASS;
- kompletter 6.72.192 Tarifcheck-HTML-Bannervertrag erneut PASS.

Finaler Installer:

`release/affiliate-zentrale/artifacts/final/AFFILIATE_ZENTRALE_6.72.193.zip`

SHA-256:

`1390374ce27c5acfe0cacf1f6ef593d75142c65090b3742c73504e9e0d1d7d27`

Größe:

`805229 Byte`

Source-Manifest SHA-256:

`877886e4eba8c3d0336f2d93ad829f122cd3d9122d14aa94e6b17ca1462e680f`

Binding-Commit:

`16fee0f1584646a13a860fdc1a2dbda2604abe83`

## Live-NEXT

6.72.192 nicht separat installieren.

Direkt 6.72.193 installieren. Danach:
1. reale Tarifcheck-HTML-Banner über den bewiesenen Bannerweg importieren;
2. Tarifrechner unter `Affiliate-Zentrale -> Tarifrechner` händisch definieren;
3. automatisch erzeugte Platzhalter aus dem Backend verwenden.
