# AFFILIATE – CURRENT STATE

STAND: 2026-09-07
STATUS: OTTO PRIORISIERT / DIGISTORE24 ZURÜCKGESTELLT / TECHNISCHE AKTIVIERUNG NOCH OFFEN


## AUTORITÄT DIESER DATEI

Diese Datei ist die **einzige aktuelle Campus-Standzusammenfassung dieses Büros**.

- aktuelle Arbeit / NEXT ACTION → `HOBBYRAUM.md`
- Fehler → `protocol/PROJECT_MEMORY/FEHLERREGISTER.md` → autoritative Fehlerquelle
- Zielvertrag → `protocol/PROJECT_MEMORY/ZIELVERTRAEGE/REGISTER.md` → Hauptquelle
- Änderungsgrund → `protocol/PROJECT_MEMORY/AENDERUNGSREGISTER.md`
- Historie → `protocol/PROJECT_MEMORY/ARCHIV/REGISTER.md`

Technische/Fachwahrheit bleibt an den in dieser Datei verlinkten Originalquellen.
Andere Campus-Dateien dürfen diesen dynamischen Bürostand nicht als zweite Wahrheit fortschreiben.

## Prioritätsentscheidung 07.09.2026

Der Nutzer meldet die **Zusage für das OTTO-Partnerprogramm**.

Verbindliche Arbeitspriorität:
- **OTTO muss in die Affiliate-Zentrale integriert werden.**
- **Digistore24 wird vorerst zurückgestellt.**
- Der offene Digistore24-Stand bleibt dokumentiert, wird aber aktuell nicht weiterbearbeitet.
- Keine Digistore24-Regressionen, Discovery-Schleifen oder Support-URL-Arbeit starten, solange der OTTO-Auftrag gebunden ist.

## Konzeptprüfung OTTO

Die vorhandene Architektur passt bereits zum neuen Auftrag:

- `class-ppar-product-source-plan.php` führt OTTO bereits als vorbereitete Produktquelle.
- Vorgesehener Weg: **Awin → fachlich OTTO**.
- Das bestehende Affiliate-Konzept priorisiert Awin als Kernnetzwerk und zentrale Produkt-/Feedverarbeitung.
- Deshalb wird **kein neuer OTTO-Gesamtworkflow und kein separates OTTO-Netzwerk erfunden**.
- OTTO wird als konkrete Produktquelle in den vorhandenen Awin-/Produktquellenweg integriert.

Harte Aktivierungsgrenze:
Die gemeldete Programmzusage ist die Prioritätsfreigabe. **Produktfeed, reale Awin-Zugänglichkeit, Tracking-/Linkdaten und erforderliche Produktfelder müssen vor öffentlicher Ausgabe real geprüft werden.**
Bis dahin bleibt der technische Providerstatus `prepared / integration pending`, nicht `active`.

## OTTO-spezifische Pflichtpunkte für die Integration

- bestehende zentrale Produktkarten-/Zuordnungslogik wiederverwenden;
- reale Produktdaten statt erfundener oder manuell nachgebauter Feeds;
- Produktdaten regelmäßig aktualisieren;
- Verkäufer-/Merchant-Angaben aus dem Feed korrekt berücksichtigen;
- bei Produktvergleichen die bestehende transparente Bewertungs-/Vergleichslogik einhalten;
- Tracking und Ausgabe weiterhin fail-closed behandeln.

## Aktueller GitHub-Releasebezug

Branch:
`affiliate-release-current`

HEAD:
`355a40ebbeceec0a4b90158db9f197b8f6e2ee7b`

GitHub-Governance:
`control/release-governance/CURRENT_RELEASE.json`

Dort gebundener aktiver Kandidat:
**6.72.1**

Source-Dateien:
26

Manifest SHA-256:
`bc6a47afc0ccac612667eef55b33ec0f7b4f4a6511f3e24546102c4345c141fa`

## WordPress-Livebeleg aus aktueller Übergabe

Live-Version:
**6.72.2**

Live-Installer:
`affiliate-zentrale_v6.72.2_LIVE_CANDIDATE_26FILE.zip`

SHA-256:
`789c7859cd9b5390bc561d6a564c2680125bcd453673cf9c6f18285c1103ba2d`

## Harte Statusdifferenz

GitHub kanonisch:
**6.72.1**

WordPress live:
**6.72.2**

Diese Differenz bleibt dokumentiert.
Sie darf bei späterer technischer OTTO-Arbeit nicht ignoriert werden.

## Aktuelle Übergabeakten

Pferde-Atelier-Status:
`AFFILIATE_ZENTRALE_MASTER_STATUS_ZIELVERTRAG_FEHLERPROTOKOLL_2026-09-05.md`

Allgemeiner Gesamtmaster:
`MASTERDATEI_AFFILIATEPORTAL_ALLGEMEIN_GESAMTPAKET_NEU_V5_31_20260905_KOMPLETT.zip`

Details:
`MASTERDATEIEN_INVENTAR.md`

## Persistentes Archiv

Pferde:
`/Campus-Archiv/PROJEKTE/PFERDE_ATELIER/AFFILIATE/2026-09-05/`

Allgemeiner Master:
`/Campus-Archiv/ALLGEMEINGUELTIGE_BAUSTEINE/AFFILIATE/2026-09-05/`

Archivstatus:
GELB.

## Harte Sortiergrenze

Diese Datei fasst nur belegte Quellenstände und die aktuelle Nutzerpriorität zusammen.

Originale, Governance, Pluginquellen und Fachregeln bleiben unangetastet.
