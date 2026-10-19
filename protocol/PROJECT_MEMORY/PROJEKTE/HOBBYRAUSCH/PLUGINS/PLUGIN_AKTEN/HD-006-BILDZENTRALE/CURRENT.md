# HD-006 – HOBBY DEPOT BILDZENTRALE – CURRENT

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-19
STATUS: **1.0.0 LOCAL PASS / INSTALLATIONSKANDIDAT / LIVE OFFEN**

Plugin-ID:
`HD-006-BILDZENTRALE`

Aktueller Hobby-Depot-Kandidat:
`HOBBY_DEPOT_BILDZENTRALE_1.0.0_INSTALLIEREN.zip`

SHA-256:
`bb74d795dffaa6d3ff51d6251d298c04c53ee9a3d75d39c00609afde867c7503`

Persistente Arbeitskopie:
`/Hobby Depot/Bildzentrale/HOBBY_DEPOT_BILDZENTRALE_1.0.0_INSTALLIEREN.zip`

Fach-Current:
`../../../BILD/CURRENT_STATE.md`

## Herkunft

Referenz:
Allgemeine Bildzentrale 2.7.6.

Die exakten 2.7.6-Bytes waren nicht als kopierbarer Quellkörper erreichbar. Deshalb ist 1.0.0 bewusst eine neu versionierte, bereinigte Hobby-Depot-Fassung auf Basis des belegten allgemeinen Funktionsvertrags und der aktuell real gelesenen Hobby-Depot-Designschnittstellen.

## Entfernt

- pa_breed;
- Rassenbatch;
- Pferde-Hero-Sonderlogik;
- Pferde-Prompts/-Framing;
- Pferde-IDs/-URLs/-Taxonomien;
- Bildertrommel;
- automatische Massenläufe;
- automatische Überschreibung.

## QA

- PHP PASS;
- ZIP PASS;
- No-Overwrite;
- Readback/Rollback;
- Kategorie-thumbnail_id;
- HivePress-Konfigurationsbindung;
- Pixabay/Pexels/Magnific;
- kein Scheduler/Cron.

## EXAKT EINE NEXT ACTION

**1.0.0 installieren und zunächst nur sichere Einzelzuweisungen testen; keine Massenbebilderung.**
