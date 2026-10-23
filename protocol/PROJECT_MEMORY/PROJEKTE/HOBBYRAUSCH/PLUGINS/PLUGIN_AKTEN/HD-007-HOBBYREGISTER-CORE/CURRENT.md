# HD-007 – HOBBYREGISTER CORE – CURRENT

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-23
STATUS: **1.1.2 BREADCRUMB + BANNER LOCAL HARD PASS / CYBERDUCK-INSTALLATION OFFEN**

Plugin-ID:
HD-007-HOBBYREGISTER-CORE

Artefakt:
`HOBBY_DEPOT_HOBBYREGISTER_CORE_HD007_V1.1.2_UPDATE_BREADCRUMB_BANNER.zip`

SHA-256:
`d83cb6de965f495e07bdc2746013657f864bda93861bfcd188db63a1287ec96e`

Größe:
22.620 Bytes.

Hauptordner:
`hd-hobbyregister-core/`

## Basis

1.1.2 ist ein kleines UPDATE auf 1.1.1.
Die 862er Datenprojektion, acht Fließtextabschnitte, Iconnavigation, Sidebar und Relationslogik bleiben unverändert.

## Breadcrumb

Jetzt auf eigener 900-px-Achse nach dem bewährten Pferdeatelier-/Universal-Breadcrumb-Prinzip, nicht mehr im 1180-px-Registercontainer.

Detailhierarchie:
**Startseite › Hobbyregister › Hobby**

Magazin wird nicht zwischengeschaltet, weil Hobbyregister und Magazin eigenständige Säulen sind.

## Register-Startseite

- ungefiltert kein „862 Treffer“ mehr;
- bei Suche/A–Z/Gruppe bleibt die Trefferzahl erhalten.

## Banner

Bestehender Slot:
`pp_affiliate_slot / hub_after_cards / portal_context`

Platzierung:
- einmal nach der Registerliste;
- einmal nach dem Haupttext eines Detailprofils.

Kein leerer öffentlicher Wrapper bei unbelegtem Slot; eingeloggte Prüffläche bleibt sichtbar.

## QA

- PHP-Lint PASS;
- Fresh-Unpack PASS;
- ZIP exakt 2 Dateien;
- Core 862/862 unverändert;
- Breadcrumb-Achse PASS;
- Startseite ohne 862-Treffer PASS;
- Filterzählung PASS;
- Banner Index + Detail PASS;
- Detail-Fließtext unverändert 8 Abschnitte.

Evidence:
`EVIDENCE_1.1.2.md`

## EXAKT EINE NEXT ACTION

**1.1.2 per Cyberduck über den bestehenden Ordner `wp-content/plugins/hd-hobbyregister-core/` zusammenführen und Register-Startseite plus ein Detailprofil live prüfen.**
