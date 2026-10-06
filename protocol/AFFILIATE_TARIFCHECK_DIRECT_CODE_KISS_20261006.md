# Tarifcheck Direktcode – KISS-Vertrag

Datum: 06.10.2026

## Verbindliches Ziel

Tarifcheck wird **nicht** als neuer technischer Provider und **nicht** über eine neue API integriert.

Es gilt der bestehende interne Weg:

`manuell eingefuegter Code -> Ziel-URL einmalig bestimmen -> feste Portalzielkarte speichern -> Runtime liest nur gespeicherte Zielkarte`

Tarifcheck wird dabei als bestehender Direkt-/Manuellpartner geführt.

## Harte Fachregel

- **Kredit / Darlehen / Finanzierung:** ausschließlich WordPress-Kategoriepfade unter **Kosten**.
- **Versicherung / Haftpflicht:** ausschließlich WordPress-Kategoriepfade unter **Versicherung**.
- Keine Kreuzzuordnung.
- Unbekannte oder mehrdeutige Tarifcheck-Ziel-URL: keine Zielkarte, keine automatische Ausspielung.
- Für Tarifcheck entstehen keine automatischen Seiten-/Beitragsziele; nur Kategorieziele sind zulässig.

## KISS-Technik

- keine neue Tabelle;
- keine neue Spalte;
- kein neuer Provideradapter;
- keine Tarifcheck-API;
- keine URL-Neuklassifikation im Frontend;
- kein allgemeiner Banner-Fallback;
- manuelle Bannerimporte laden nach dem Import alle betroffenen Banner in genau einer gebündelten DB-Abfrage;
- Ziel-URL-Auflösung ist ausschließlich Import-/Adminlogik.

## Version

6.72.190 bleibt bewiesene Hard-KISS-Bannerbasis, wird aber vor Live-Installation durch 6.72.191 ersetzt.

6.72.191 ergänzt:
1. den manuellen Direktcode-Import um denselben Zielkarten-Nachlauf;
2. die harte Tarifcheck-Familientrennung Kosten vs. Versicherung;
3. fail-closed für unbekannte/mehrdeutige Tarifcheck-Ziele.

## Abnahme

Vor Installation Pflicht:
- WordPress + MariaDB;
- Kredit positiv unter Kosten;
- Kredit negativ unter Versicherung;
- Versicherung positiv unter Versicherung;
- Versicherung negativ unter Kosten;
- unbekanntes Tarifcheck-Ziel negativ;
- gemischtes Kredit/Versicherung-Ziel negativ;
- Runtime liest gespeicherte Karte;
- Source-Manifest 27/27;
- PHP-Lint;
- Fresh-Unpack/Byteidentität des finalen ZIP.
