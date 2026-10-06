# Affiliate Router 6.72.192 — Tarifcheck HTML Verify-Before-Assign

Datum: 06.10.2026

## Verbindliche KISS-Kette

`HTML-Code -> Trackinglink/Bildquelle lesen -> echte Ziel-URL ermitteln/pruefen -> Banner technisch pruefen -> Tarifart aus Ziel-URL -> feste erlaubte Portalziele speichern -> Runtime liest nur gespeicherte Zielkarte`

Tarifcheck bleibt bestehender Direkt-/Manuellpartner. Keine Tarifcheck-API und kein neuer Provideradapter.

## Sicherheitsregel

Vor erfolgreicher technischer Bildpruefung existiert fuer einen neu importierten Direkt-/Tarifcheck-Banner keine Zielkarte.

Technische Pruefung:
- vollstaendiger <a><img>-Code;
- gueltiger Trackinglink;
- gueltige Bild-URL;
- echte Ziel-URL muss importseitig explizit, lokal dekodiert oder ueber begrenzte Redirect-Pruefung bestimmt sein;
- reales Bannerbild wird geladen;
- echte Bildmasse und Inhalts-Hash werden bestimmt.

Scheitert die Bildpruefung, bleibt `topic_targets=[]` und der Banner ist `format_blocked`.

## Fachzuordnung

Tarifcheck Kredit:
- ausschliesslich aus der echten Ziel-URL erkannt;
- 67 konfigurierte Kosten-Eintraege, 66 eindeutige reale Kostenpfade;
- eine Kampagne mit allen realen Kosten-Zielschluesseln;
- keine Versicherungsziele.

Tarifcheck Versicherung:
- ausschliesslich aus der echten Ziel-URL erkannt;
- 14 reale Blattkategorien unter `Wissen > Versicherungen & Recht`;
- keine Kostenziele.

Unbekannte oder gemischte Ziel-URL:
- keine Zielkarte;
- keine automatische Ausspielung.

Titel/Alt-Text duerfen die URL-Klassifikation nicht ueberstimmen.

## Datenbank-/Performance-KISS

- keine neue Tabelle;
- keine neue Spalte;
- keine URL-Historie;
- keine neue Frontend-DB-Abfrage;
- kein Frontend-HTTP;
- nach manuellem HTML-Import genau eine gebuendelte DB-Abfrage der betroffenen Banner;
- ungepruefte neue Direkt-/Tarifcheck-Banner werden nicht zugeordnet;
- technische Bildpruefung laeuft im vorhandenen kleinen Pruefbatch;
- der Pruefer bekommt die gespeicherte Zielmenge direkt aus dem Mapping-Ergebnis zurueck; dafuer ist kein zusaetzlicher DB-Read pro Banner erforderlich.

## Source-/WordPress-/MariaDB-Beweis

Run `37454893550`: SUCCESS.

PASS:
- PHP-Lint 21/21;
- vor technischer Pruefung Kredit: 0 Ziele;
- nach technischer Pruefung Kredit: 66/66 eindeutige Kostenpfade;
- vor technischer Pruefung Versicherung: 0 Ziele;
- nach technischer Pruefung Versicherung: 14/14 Versicherungsblaetter;
- Kredit-URL gewinnt gegen irrefuehrenden Versicherungstitel;
- unbekannte Tarifcheck-URL bleibt nach erfolgreicher Bildpruefung ohne Ziel;
- gemischte Kredit/Versicherung-URL bleibt ohne Ziel;
- kaputtes Bild bleibt ohne Ziel und wird format_blocked;
- Runtime liest gespeicherte Kredit-Zielkarte mit 66 Zielschluesseln;
- keine neue Tabelle.

## Exakter finaler ZIP-Beweis

Run `37455039161`: SUCCESS.

PASS:
- Source-Manifest 27 Dateien;
- Fresh-Unpack 27/27 Byteidentitaet;
- PHP-Lint 21/21;
- exaktes ZIP frisch in WordPress 7.1.2 + MariaDB 10.11 installiert und aktiviert;
- kompletter Verify-Before-Assign-Test auf exakt diesem ZIP PASS;
- keine neue Tabelle.

Finaler Installer:

`release/affiliate-zentrale/artifacts/final/AFFILIATE_ZENTRALE_6.72.192.zip`

SHA-256:

`49add47f6876e78737704b3ca067bf5d931ee68a5f7448f99d8227ee57fc60d9`

Groesse:

`801146 Byte`

Source-Manifest SHA-256:

`6b38a862bdcff56006c32382a258bf74550ccba25537001d5398494b957aba77`

Binding-Commit:

`aa3bdbbae8520d6f5e9bd517be0d9325169177f8`

## Tarifrechner

Tarifrechner/Widgets sind ausdruecklich NICHT Bestandteil dieses Releases. Sie werden spaeter als eigener Werbemitteltyp konzipiert. 6.72.192 schliesst nur die korrekte HTML-Banneraufnahme und Bannerzuordnung ab.
