# HD-006 – HOBBY DEPOT BILDZENTRALE – CURRENT

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-20
STATUS: **2.7.7 AUS BYTEGENAU VERIFIZIERTEM PFERDEATELIER-ORIGINAL 2.7.6 / LOCAL PASS / LIVE OFFEN**

Plugin-ID:
`HD-006-BILDZENTRALE`

## Verifizierte Quelle

WPvivid-Pluginbackup:
`pferde-atelier.de_wpvivid-6e9ec6d805997_2026-09-24-11-08_backup_plugin.part001.zip`

Originaldatei:
`plugins/pferde-atelier-bildzentrale/pferde-atelier-bildzentrale.php`

Beweis:
- Version 2.7.6;
- 383603 Bytes;
- SHA-256 `984a8d4da6594ffa93e6d4024b57cc6c22c7d1fbfec398177a19b0490c20d89b`;
- exakte Übereinstimmung mit dokumentiertem Pferdeatelier-Source-Scan.

## Aktueller Kandidat

`HOBBY_DEPOT_BILDZENTRALE_2.7.7_AUS_ORIGINAL_2.7.6_BEREINIGT_INSTALLIEREN.zip`

ZIP SHA-256:
`c27eff9a48007a5317832cf3d6f539d49856a1e6edaf92eebd1bfdb89e030ab7`

Hauptdatei:
- 317483 Bytes;
- SHA-256 `5126d57a1a04d75e561bf7eab35227e176a04352eb70f587a4f392e463331b38`.

## Korrektur

Der frühere Kandidat 1.0.0 war **nicht** aus dem echten Pluginquellstand abgeleitet und ist verworfen. Seine Library-Kopien im Bildbüro und Plugin-Büro wurden entfernt.

## Delta

Entfernt:
- pa_breed;
- kompletter Rassen-Batch;
- Rassen-Hero-Sonderprompt;
- Pferde-Motivcluster und Pferde-Such-/Alttext-/Fallbackregeln;
- feste ID 9120;
- Pferdeatelier-Admin-/REST-Slugs.

Angepasst:
- Hobby-Depot-Name/Slug;
- HDBZ-Namespace;
- neutraler Hobby-Prompt;
- acht Hobbywelten;
- Hobby-Depot-WordPress-/HivePress-Bildbindung.

Beibehalten:
- allgemeiner Originalkern; nach Namespace-Normalisierung 134 Funktionen unverändert.

## QA

- PHP PASS;
- ZIP PASS;
- WordPress-Paketstruktur PASS;
- 0 fehlende Callbacks;
- 0 fehlende self-calls;
- 0 Pferde-/Rassen-/Horse-/Breed-/pa_breed-Literale;
- allgemeine Kernwege gegen Original unverändert PASS.

## Bildertrommel

Im verifizierten Original ist kein eindeutiger Code-/UI-Block dieses Namens belegbar. Daher wurde kein allgemeiner Weg auf Verdacht gelöscht.

## EXAKT EINE NEXT ACTION

**2.7.7 installieren und ausschließlich sichere Einzeltests durchführen; kein Massenlauf vor Live-Readback.**
