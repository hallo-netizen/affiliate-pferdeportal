# HD-007 – HOBBYREGISTER CORE – CURRENT

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-23
STATUS: **1.2.13 CORE-BILDPRÜFUNG ABGESCHLOSSEN / LOCAL HARD PASS / LIVE OFFEN**

Plugin-ID:
`HD-007-HOBBYREGISTER-CORE`

Artefakt:
`HOBBY_DEPOT_HOBBYREGISTER_CORE_HD007_V1.2.13_FULL_CORE_BILDPRUEFUNG.zip`

SHA-256:
`67a052dd1f648fd8e1550c326f8efe2ad5c55b4aa75e51397ad0c7ceefcd4d0d`

## Bildstand

- Gesamt: 862 Hobbys.
- Final DONE: 14 erzeugte/verifizierte Masterbilder.
- 382 vorhandene CORE-Kandidaten vollständig geprüft.
- Davon inhaltlich passend: 81.
- Davon inhaltlich unpassend: 301.
- Technisch als gemeinsames 1500×1000-Master für Hero + Beitrag geeignet: 0/382.
- Grund: kein vorhandener CORE-Kandidat erreicht 1000 px Höhe; Hochskalieren ist laut Bildvertrag verboten.
- 81 passende CORE-Motive: High-Res-Quelle suchen oder neu erzeugen.
- 301 unpassende CORE-Motive: neu erzeugen.
- Noch offene NO_CORE-Fälle: 466.

Zentrale Dateien im Plugin:
- `data/hobby-image-production-status-v1.json`
- `data/core-image-audit-v1.json`

## Weiterhin unverändert

- 862/862 Hobbys.
- 57/57 Traits.
- 862 statische Artikel.
- Hobby-Depot-Breiten-/Containerstand aus bestandenem 1.2.10-Stamm.
- 14 vorhandene finale Masterbilder.

## QA

- 382/382 CORE-Zuordnungen geprüft.
- 212/212 unterschiedliche CORE-Dateien visuell geprüft.
- 862/862 Detailseiten PASS.
- Registerübersicht PASS.
- PHP-Lint PASS.
- Fresh-Unpack PASS.

Evidence:
`EVIDENCE_1.2.13_CORE_IMAGE_AUDIT.md`

## EXAKT EINE NEXT ACTION

**Live nur Plugin 1.2.13 über den bestehenden Ordner kopieren/überschreiben; danach keine weitere Bildproduktion, bis die nächste Arbeitsstufe bewusst gestartet wird.**
