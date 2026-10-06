# Affiliate Router 6.72.191 — Tarifcheck Direct-Code KISS

Datum: 06.10.2026

## Ziel

Tarifcheck wird nicht als neuer Provider und nicht über eine neue API integriert.

Verbindliche Kette:

`manueller Code -> Trackinglink -> echte Ziel-URL -> Tarifart -> feste erlaubte Portalziele -> speichern -> Runtime liest nur gespeicherte Zielkarte`

## Reale Kategoriebaum-Prüfung

Autoritative Struktur:

`release/affiliate-zentrale/current/affiliate-portal-router/assets/ebay-portal-catalog-v2.json`

Belegt:
- 1.149 Artikelkategorien insgesamt;
- 67 konfigurierte Kosten-Einträge;
- 67 unterschiedliche Kosten-Slugs;
- 66 unterschiedliche Kosten-Pfade, weil ein Weidezaungeräte-Pfad im Katalog doppelt mit zwei Slugs vorkommt;
- Kosten-Blätter liegen verteilt unter Ausrüstung, Fütterung, Stall, Transport, Weide und Wissen;
- 14 konfigurierte Versicherungs-Blattkategorien unter `Wissen > Versicherungen & Recht`.

## Implementierter Vertrag

Tarifcheck-Kredit:
- Tarifart ausschließlich aus der echten Ziel-URL;
- alle real vorhandenen Kosten-Blätter sind feste Ziele;
- Kosten-Blatt muss sichtbar `Kosten …` heißen und einen `…-kosten`-Slug besitzen;
- keine Versicherungsziele;
- eine Kampagne mit allen gespeicherten Kosten-Zielschlüsseln, keine Bannerkopien pro Kategorie.

Tarifcheck-Versicherung:
- Tarifart ausschließlich aus der echten Ziel-URL;
- ausschließlich echte Blattkategorien im Ast `Wissen > Versicherungen & Recht`;
- keine Kosten-Ziele;
- eine Kampagne mit allen gespeicherten Versicherungs-Zielschlüsseln.

Unbekannte oder gemischte Tarifcheck-Ziel-URLs:
- keine Zielkarte;
- keine automatische Ausspielung.

Banner-/Alt-/Titeltext darf die aus der Ziel-URL erkannte Tarifart nicht überstimmen.

## KISS / Performance

- vorhandener Direkt-/Manuellpartner-Weg;
- keine Tarifcheck-API;
- kein neuer Provideradapter;
- keine neue Tabelle;
- keine neue Spalte;
- keine URL-Historie;
- keine URL-Neuklassifikation im Frontend;
- kein Frontend-HTTP für die Zuordnung;
- keine zusätzliche Frontend-DB-Abfrage;
- manueller Import lädt die betroffenen Banner nach dem Import in genau einer gebündelten DB-Abfrage;
- Runtime liest ausschließlich die gespeicherte Zielkarte.

## WordPress/MariaDB Source-Beweis

Run `37450657203`: SUCCESS.

Belegt:
- PHP-Lint 21/21 PASS;
- Kategoriebaum-Modell 67 Kosten-Einträge / 66 eindeutige Kostenpfade / sechs Hauptbereiche PASS;
- Kredit 66/66 eindeutige Kostenpfade PASS;
- Versicherungen 14/14 Versicherungsblätter PASS;
- Kredit-URL schlägt irreführenden Versicherungstitel PASS;
- Versicherungs-URL schlägt irreführenden Kredittitel PASS;
- Kosten/Versicherung gegenseitig ausgeschlossen PASS;
- unbekannte Tarifcheck-URL fail-closed PASS;
- gemischte Kredit/Versicherung-URL fail-closed PASS;
- Runtime-Zielmenge Kosten 66 PASS;
- Runtime-Zielmenge Versicherung 14 PASS;
- keine neue Tabelle durch Import/Zielkartenaufbau PASS.

## Exakter finaler ZIP-Beweis

Run `37450856670`: SUCCESS.

Belegt:
- Source-Manifest 27 Dateien;
- Fresh-Unpack 27/27 Byteidentität PASS;
- PHP-Lint 21/21 PASS;
- exaktes ZIP frisch in WordPress 7.1.2 + MariaDB 10.11 installiert und aktiviert;
- kompletter Tarifcheck Positiv-/Negativtest auf exakt diesem ZIP PASS;
- keine neue Tabelle durch Tarifcheck-Import/Zielkartenaufbau PASS.

Finaler Installer:

`release/affiliate-zentrale/artifacts/final/AFFILIATE_ZENTRALE_6.72.191.zip`

SHA-256:

`0987dec5826be39b99fc05a993a64149acf017445ecde0577dc3f975a13f9f5e`

Größe:

`800276 Byte`

Source-Manifest SHA-256:

`b49e27e2301bb5cc8cfa92c42b2cbd41af72bc68e8136e655e24d2061b3e66bc`

Binding-Commit:

`be83c55670c4f6c394629501262d6980afa0048f`

## Noch offen

Nur der gebundene Live-Schritt:
- exakt 6.72.191 manuell in der bestehenden WordPress-Installation installieren;
- danach Live-Readback/Closeout gegen die gespeicherten Zielkarten.

6.72.190 ist superseded und darf nicht mehr installiert werden.
