# ALLGEMEINES DESIGN – MASTERDATEIEN-INVENTAR

STAND: 2026-09-15

## DES-UNI-001 – Universal Plugin

Datei:
`UNIVERSAL_PORTAL_DESIGN_SUITE_V2.2.41_GLOBAL_BREADCRUMB_GAP_15_10_INSTALLIEREN.zip`

SHA-256:
`2bc9e9327601f8e1f1cf2cb1d299f9ec120994e325abb5d676fd347005e55512`

STATUS:
AKTUELLER ALLGEMEINER PLUGIN-BELEG – LOKAL HART PASS / LIVE OFFEN.

Änderung gegenüber 2.2.40 ausschließlich:
- Breadcrumb-Unterkante → erster sichtbarer Inhalt zentral 15 px Desktop / 10 px mobil;
- individuelle `breadcrumb_gap`-Einstellung entfernt;
- seitentyp-/Leading-Image-spezifische Breadcrumb-Abstandautoritäten entfernt.

## DES-UNI-002 – Universal Master

Datei:
`MASTER_ALLGEMEINGUELTIG_DESIGN_V2_2_41_CONTRACT_V104_20260915.zip`

SHA-256:
`a6486b41e786ad53a90d5203720244f4055b52dd359779cd31b5a5444e380da3`

Mastermanifest:
**301/301 OK**

STATUS:
AKTUELLE ALLGEMEINE HAUPTAKTE – LOKAL HART PASS / LIVE OFFEN.

Enthält:
- CURRENT_PLUGIN_SOURCE 2.2.41;
- Installer 2.2.41 plus Historie;
- V104-Vertrag mit zentraler Breadcrumb-Abstandsregel;
- vollständige Designhistorie;
- QA/Evidenz;
- Sucharchitektur;
- separaten Universal-HivePress-Suchplugin-Quellbaum + Installer.

## Plugin-/Master-Abgleich

- externer V2.2.41-Plugin-ZIP = eingebetteter V2.2.41-Installer byte-identisch;
- CURRENT_PLUGIN_SOURCE = Installer inhaltlich identisch;
- Overwrite 2.2.40 → 2.2.41 ergibt bytegleichen Zielbaum.

## Persistentes Archiv

Aktueller Stand:
`/Campus-Archiv/ALLGEMEINGUELTIGE_BAUSTEINE/DESIGN/2026-09-15/`

Enthält:
- Plugin-ZIP 2.2.41;
- Master-ZIP 2.2.41/V104;
- Testreport 2.2.41.

Historischer Stand 2.2.40/V104 bleibt unverändert unter:
`/Campus-Archiv/ALLGEMEINGUELTIGE_BAUSTEINE/DESIGN/2026-09-05/`

## Nebenkomponente – nicht verlieren

Im Master enthalten:
`UNIVERSAL_HIVEPRESS_ANZEIGENSUCHE_v2.1.5_AJAX_ANZEIGENKATEGORIEN_INSTALLIEREN.zip`

sowie Source/Evidenz/QA.

Zuordnung:
separater Baustein-Kandidat MOD-004, vorläufig UNGEKLÄRT bis eigener Modul-Audit.
