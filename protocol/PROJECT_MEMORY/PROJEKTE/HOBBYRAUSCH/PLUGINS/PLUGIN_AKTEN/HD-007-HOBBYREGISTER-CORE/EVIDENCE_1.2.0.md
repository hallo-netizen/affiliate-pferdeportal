# HD-007 – EVIDENCE 1.2.0 / 57 TRAITS + 862 TEXTE

STAND: 2026-10-23
STATUS: LOCAL HARD PASS / LIVE OFFEN

Artefakt:
`HOBBY_DEPOT_HOBBYREGISTER_CORE_HD007_V1.2.0_FULL_57TRAITS_862TEXTE.zip`

SHA-256:
`f73e9ae3d09f2339659b3cbfabab98f99758f9513c124e01017481dd401801a1`

Größe:
1,722,774 Bytes.

## Daten

- 862/862 kanonische Hobbys.
- 57/57 Traits je Hobby.
- 2.586 neue Schema-1.2-Zuweisungen gebunden.
- 46.548 alte 54er Traitwerte gegenüber 1.1.7 unverändert.
- Runtime-Register-SHA: `d0d424485e6dbcf65a8332da732d2e342b279f0a1311919149ba8dfcdb93604a`.

## Texte

- 862/862 statische Schema-F-Texte.
- je exakt 8 Abschnitte.
- 57/57 Trait-IDs im Produktionsgenerator berücksichtigt.
- Wortumfang: min. 656 / Median 708 / max. 761 Wörter.
- Buchbinden und Slacklining bleiben die manuell ausformulierten Referenztexte.
- alle anderen Texte wurden aus der geprüften zentralen Klassifikation deterministisch erzeugt und anschließend statisch eingefroren.

## Layout

- Register-/Profilbreite max. 1180px.
- wiederholender Kurzprofil-Untertext im Profil-Hero entfernt.
- kurzer Claim je primärer Hobbygruppe.
- Claim grüne Schreibschrift.
- vorhandener gelber Hobby-Depot-Brush als Unterstrich.

## Bilder

Aktuelle sichtbare Bildabdeckung: 862/862.
- 328 exakt kuratierte vorhandene Hobby-/CORE-Fotos.
- 534 fachlich zugeordnete vorhandene Themen-Masterbilder.
- alle referenzierten Dateien physisch im aktuellen HD-003-Assetbestand vorhanden.

WICHTIG:
Diese 534 Themen-Masterbilder sind keine neu erzeugten individuellen Portraitmaster.
Der autoritative Bildplan `HOBBY_PORTRAIT_BILDPLAN_V1` bleibt für dedizierte Masterbilder bestehen und wird nicht als erledigt umetikettiert.

## QA

- HD_Hobbyregister_Core::ready(): PASS.
- 862 Records / 57 Traits: PASS.
- 862 Artikel / je 8 Abschnitte: PASS.
- 862 Bildzuordnungen: PASS.
- 7 heterogene Profile vollständig gerendert: PASS.
- Bodybreite 1180: PASS.
- Brush-Claim: PASS.
- wiederholender Hero-Einstieg entfernt: PASS.
- PHP-Lint: 4/4 PASS.
- Fresh-Unpack PASS.

Kein Live-PASS behaupten.
