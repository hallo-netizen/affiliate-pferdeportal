# HD-003 – HOBBY DEPOT DESIGN / TEMPLATE KIT – CURRENT

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-24
STATUS: **1.50.730 BODY 1200 / HEADER + FOOTER UNVERÄNDERT / LOCAL HARD PASS / LIVE OFFEN**

Plugin-ID:
`HD-003-DESIGN-TEMPLATE-KIT`

Artefakt:
`HOBBY_DEPOT_HD003_CYBERDUCK_1.50.730_BODY_1200_HEADER_FOOTER_UNBERUEHRT_HARDPASS.zip`

SHA-256:
`b31c2528ad049d9974104cd8de35b39cf69bf701efe429104c8c4218bd798279`

HD-003 liegt darin vollständig unter:
`affiliate-portal-template-kit/`

## Wesentliche Korrektur

- kein Delta mehr;
- Footer-Logo mit eigenem physisch zugeschnittenem Asset ohne Unterzeile;
- keine CSS-Abschneidung des Hauptlogos;
- Runtime-Marker `HD-003 RUNTIME 1.50.729`;
- Magazin-/Footer-Navigation aus dem vorherigen Stand bleibt erhalten.

QA:
- Full-Unpack PASS;
- Footer-Render PASS;
- PHP-Lint PASS.

Evidence:
`../../EVIDENCE_FULL_REPLACEMENT_20261023.md`

## EXAKT EINE NEXT ACTION

**Die beiden bestehenden Pluginordner serverseitig vollständig durch die Ordner aus dem Vollersatz ersetzen und danach Live-Readback durchführen.**


## 1.50.730 – zentrale Body-Achse
- Root-`--hd-content` bleibt 1440 px als unveränderte Header-/Footer-Basis.
- Auf `body.pftk-design-profile-hobby-depot` wird `--hd-content:1200px` gesetzt.
- `.hd-header-v150616` und `.hd-footer-v150616` setzen lokal wieder `--hd-content:1440px`.
- Native ListingHive-`.site-content`-Bereiche werden zentral auf max. 1200 px begrenzt und zentriert.
- Glossar-Single-Altbreite 1240 px wird zentral auf max. 1200 px gekappt.
- Keine Änderung an Header-/Footer-Layout, Typografie, Navigation oder sichtbaren Inhalten.
- Finales ZIP: 935 Dateien, ein Root `affiliate-portal-template-kit/`, PHP 10/10 PASS, ZIP PASS, Source/ZIP bytegleich.
- Browser-Hardpass 1600/1366/1024/760/390: Header/Footer jeweils 0 px Geometriedifferenz zum 1.50.729-Stand; Body bei breiten Viewports 1200 px.
