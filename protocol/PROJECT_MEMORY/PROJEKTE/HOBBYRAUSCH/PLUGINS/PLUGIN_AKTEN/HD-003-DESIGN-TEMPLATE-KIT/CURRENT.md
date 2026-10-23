# HD-003 – HOBBY DEPOT DESIGN / TEMPLATE KIT – CURRENT

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-23
STATUS: **LIVE 1.50.711 / 1.50.714 DELTA LOKAL PASS / CYBERDUCK-INSTALLATION OFFEN**

Plugin-ID:
`HD-003-DESIGN-TEMPLATE-KIT`

Fach-Current:
`../../../DESIGN/CURRENT_STATE.md`

## Live

Aktiv und nach Nutzer-Readback funktionsfähig:
**1.50.711**.

1.50.710 ist verworfen.

## Lokaler Kandidat 1.50.714 – Delta

Basis:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.712_FULL_SLIM30.zip`

Artefakt:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.714_DELTA_PBONE_NEUES_FENSTER.zip`

SHA-256:
`4d7e0c0a7087d6c365783bc9929244a7795389161945d1da99dd28c53b1a90d3`

Größe:
570,882 Bytes.

Delta gegenüber 1.50.713:
- `pferde-template-kit.php`: Version 1.50.714;
- `includes/class-hobby-depot-profile-v150709.php`: PB-one-Link mit `target="_blank" rel="noopener noreferrer"`.

Footer:
- Logo entfernt;
- vier Spalten: Rechtliches / Wissen / Service / Anzeigenmarkt;
- Wissen = Hobbymagazin / FAQ / Glossar / Hobbyregister;
- Service = Werben im Hobby Depot / Preise / Kontakt;
- Links 14px, Überschriften 16.5px;
- Copyright mittig unter dem Footer;
- kleiner Hinweis `* mithilfe von KI erstellt`;
- `© [Jahr] Hobby Depot | PB one.`;
- PB one. → `https://p-b.one/`.

Lokale QA:
- kompletter PHP-Lint 10/10 PASS;
- nur zwei bestehende Runtime-Dateien gegenüber 1.50.712 geändert;
- keine Seitentemplates geändert;
- Footer Positiv-/Negativrender PASS;
- ZIP/Fresh-Unpack PASS.

Evidence:
`EVIDENCE_1.50.713.md`

## Installation

Der WordPress-ZIP-Uploadweg bleibt wegen HTTP 413 unbrauchbar.
Der Nutzer arbeitet deshalb über Cyberduck.

1.50.714 ist **nicht live**.

## EXAKT EINE NEXT ACTION

**1.50.714-Delta lokal entpacken und nur die enthaltenen zwei Dateien in den vorhandenen Plugin-Ordner kopieren/überschreiben. Danach PB-one-Link + Plugin-Version live prüfen.**
