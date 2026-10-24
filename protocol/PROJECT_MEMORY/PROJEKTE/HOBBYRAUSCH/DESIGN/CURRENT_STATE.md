# HOBBYRAUSCH – DESIGN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-24
STATUS: **HD-003 1.50.730 / ZENTRALE BODY-ACHSE 1200 PX / HEADER + FOOTER UNVERÄNDERT / LOCAL HARD PASS / LIVE OFFEN**

Zielvertrag:
**ZV-HOBBYRAUSCH-DESIGN-001 Fassung 5.5 / 2026-10-19**

## HD-003

Footer-/Magazinstand bleibt 1.50.729.

## Hobbyregister / HD-007

Die früheren Zwischenstände mit eigenen Breitenwerten 1050/1180/1200 px sind verworfen.

Seit HD-007 1.2.10 verwendet das Hobbyregister die echten Hobby-Depot-Containerklassen aus HD-003:
- `hd-content-v150616`;
- `hd-portal-section`;
- `hd-breadcrumb-wrap`.

Lokaler Chromium-Vergleich gegen Hobby-Depot-Kategorie:
1600 / 1440 / 1366 / 1180 / 1024 / 761 / 760 / 390 px → linke Kante, rechte Kante und Gesamtbreite jeweils **0 px Differenz**.

Der Nutzer bestätigte diesen sichtbaren Breitenstand anschließend live mit **„pass“**.

HD-007 1.2.13 verändert diesen Layout-/Containerstand nicht.

## Profil-Hero / Inhalt

- Hobbytitel als H1;
- kurzer gruppenspezifischer Claim;
- grüne Schreibschrift + gelber Brush;
- 862/862 Detailprofile;
- 57/57 Traits;
- 862 statische Artikel mit je 8 Abschnitten;
- Sidebar-Überschrift `Selbe Hobbygruppe`;
- unterer Detail-Banner entfernt.

## Bilder

Der laufende Hobbyregister-Bildstatus ist technische HD-007-Arbeit und wird nicht hier dupliziert.

Aktuelle technische Autorität:
`../PLUGINS/PLUGIN_AKTEN/HD-007-HOBBYREGISTER-CORE/CURRENT.md`

## EXAKT EINE NEXT ACTION

**Hobbyregister-Layout nicht weiter verändern. Nur bei einer neuen sichtbaren Designbeanstandung erneut im DESIGN-Scope arbeiten; Bild-/Pluginarbeit über HD-007 führen.**


## 24.10.2026 – zentrale Body-Breite 1200 px
- HD-003 auf 1.50.730.
- Hobby-Depot-Inhaltsachse zentral auf maximal 1200 px gesetzt.
- Header und Footer behalten ihre bisherige 1440-px-Variable und ihre Geometrie.
- Native ListingHive-/WordPress-Inhaltsseiten werden ebenfalls auf dieselbe 1200-px-Außenachse zentriert.
- Glossar-Übersicht, Glossar-Einzelseite und Hobbyregister wurden gegen die zentrale Achse geprüft; die historische feste 1240-px-Glossar-Einzelseite wird zentral auf 1200 px gekappt.
- Browservergleich 1.50.729 → 1.50.730 bei 1600 / 1366 / 1024 / 760 / 390 px: Headerbreite Delta 0 px, Footerbreite Delta 0 px.
- Finales ZIP erneut entpackt und daraus geprüft: PASS.
- Artefakt: `HOBBY_DEPOT_HD003_CYBERDUCK_1.50.730_BODY_1200_HEADER_FOOTER_UNBERUEHRT_HARDPASS.zip`
- SHA-256: `b31c2528ad049d9974104cd8de35b39cf69bf701efe429104c8c4218bd798279`
