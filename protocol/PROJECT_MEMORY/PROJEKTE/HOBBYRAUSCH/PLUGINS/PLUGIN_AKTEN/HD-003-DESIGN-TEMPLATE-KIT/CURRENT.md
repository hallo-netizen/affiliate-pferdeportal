# HD-003 – HOBBY DEPOT DESIGN / TEMPLATE KIT – CURRENT

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-15
STATUS: **LIVE-SEITE WIEDER ERREICHBAR / TEMPLATE-KIT 1.50.650 BLEIBT AKTIV UND UNANGETASTET / 1.50.661 NUR 30 HERO-DATEIEN LOKAL E2E PASS / LIVE-VISUALPRÜFUNG OFFEN**

## Aktiver Grundstand
Affiliate Portal Template Kit **1.50.650**.

## Nicht verwenden
- 1.50.651;
- Repair Installer 1.50.657;
- Recovery 1.50.658;
- Hero Images ONLY 1.50.659;
- Hero Replace ONLY 1.50.660 als Endstand für die 30 live verworfenen Heroes.

## Aktueller Bildpatch
`HOBBY_DEPOT_HERO_REPLACE_30_ONLY_1.50.661.zip`

SHA-256:
`befb9a73f67e3827b7ad5c7c03d940976a5362a2a732f779654499685f0f0b3e`

Der Patch:
- enthält exakt 30 neue 600×220-Hero-Dateien;
- ersetzt nur die 30 Nutzer-Hard-Reject-Kategorien;
- nutzt ausschließlich die bereits aktiven Zielpfade des vorhandenen Mappings;
- schreibt/ändert das Mapping nicht;
- ändert keine Template-Kit-PHP-Datei;
- ändert keine Templates, kein Routing, kein CSS, keine Karten und keine Architektur;
- lässt die anderen 35 aktuell gemappten Hero-Dateien unverändert.

## Lokale E2E-Prüfung
PASS auf:
1. pristine 1.50.650;
2. simuliertem Nach-1.50.659+1.50.660-Zustand.

Jeweils:
- exakt 30 erwartete Bilddatei-Diffs;
- Mapping unverändert;
- 35 nicht betroffene Hero-Zieldateien unverändert;
- 0 PHP-Diffs;
- 30/30 Zielbilder = Payload;
- keine temporären/Backup-Reste.

## NEXT ACTION
**Nur 1.50.661 installieren/aktivieren und die 30 betroffenen Heroes live visuell prüfen.**
