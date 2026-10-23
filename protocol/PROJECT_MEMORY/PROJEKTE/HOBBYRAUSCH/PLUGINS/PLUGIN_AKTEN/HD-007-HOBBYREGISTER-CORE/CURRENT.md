# HD-007 – HOBBYREGISTER CORE – CURRENT

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-23
STATUS: **1.2.7 STABILE REPARATUR LOCAL HARD PASS / LIVE OFFEN**

Plugin-ID:
`HD-007-HOBBYREGISTER-CORE`

Artefakt:
`HOBBY_DEPOT_HOBBYREGISTER_CORE_HD007_V1.2.7_FULL_STABIL_REPARIERT.zip`

SHA-256:
`1019a7b0df6f268caba9acdeaa296a2a12817e1264db43024adaec369517dc7c`

## Reparatur

1.2.6 wird vollständig verworfen.
Rückkehr zum stabilen JSON-Laufzeitsystem.

Zusätzlich behoben:
Mehrfach geladene Hobbyregister-Kopien dürfen keine Klassen-/Funktions-Neudeklaration und damit keinen PHP-Fatal mehr verursachen.

## Inhalt

- 862/862 Hobbys;
- 57/57 Traits;
- 862 statische Artikel mit je 8 Abschnitten;
- 862 Bildzuordnungen;
- `Selbe Hobbygruppe`;
- kein Detailbanner unten;
- Portalbreite `min(calc(100% - 72px),1440px)`.

## QA

- Fresh-Unpack PASS;
- PHP-Lint 4/4 PASS;
- 862/862 Slug-/Artikelprüfung PASS;
- 8 heterogene Detail-Vollrenders PASS;
- Registerindex PASS;
- Doppelplugin alt -> neu PASS;
- Doppelplugin neu -> alt PASS;
- kein PHP-Fatal in beiden Lade-Reihenfolgen.

Evidence:
`EVIDENCE_1.2.7.md`

## EXAKT EINE NEXT ACTION

**1.2.7 über den bestehenden aktiven Ordner `hd-hobbyregister-core` kopieren/überschreiben und zuerst prüfen, dass die Website wieder normal lädt; anschließend Registerstart und ein Detailprofil öffnen.**
