# HD-007 – EVIDENCE 1.2.5 DATENPFAD-ROBUST

STAND: 2026-10-23
STATUS: LOCAL HARD PASS / LIVE OFFEN

Artefakt:
`HOBBY_DEPOT_HOBBYREGISTER_CORE_HD007_V1.2.5_FULL_DATENPFAD_ROBUST.zip`

SHA-256:
`6b601d37027ddf208994e5cc32bd2bd3f1b1b94106f818f0b0db87dce9de765a`

Zusätzlich:
`HOBBY_DEPOT_HD007_V1.2.5_INHALT_FUER_AKTIVEN_ORDNER.zip`
SHA-256:
`a0cc7436e07e589b210883fbd68415792f776a4563e2d0e19e01f9279e7a4506`

## Diagnose

1.2.4 frisch entpackt:
- Core ready PASS;
- 862 Datensätze;
- 862/862 Profile gefunden;
- 862/862 Profile mit Artikel gerendert;
- Registerindex PASS.

Damit liegt der Live-Ausfall nicht im ausgelieferten 1.2.4-Datensatz oder in der Profilauflösung, sondern im geladenen Live-Ordner/Datenpfad.

## 1.2.5

Der Core ermittelt einen vollständigen Datenordner robust:
1. Datenordner des aktuell geladenen Pluginordners;
2. kanonischer Geschwisterordner `hd-hobbyregister-core/data`;
3. weitere Geschwisterordner `hd-hobbyregister-core*/data`.

Ein Ordner gilt nur dann als vollständig, wenn:
- hobby-register.json: 862 Records und 57 Traits;
- hobby-articles-v1.json: 862 Artikel;
- hobby-image-map-v1.json: 862 Einträge;
- traits-schema.json lesbar.

Damit wird insbesondere ein versehentlicher aktiver Ordner `hd-hobbyregister-core 2` ohne eigene Daten gegen den vollständigen kanonischen Datenordner abgefangen.

## Simulation

Normalinstallation:
- VERSION 1.2.5;
- ready PASS;
- count 862;
- 862/862 Profile;
- Index PASS.

Doppelordnersimulation:
- aktiver Code unter `hd-hobbyregister-core 2`;
- dort absichtlich kompletter data-Ordner entfernt;
- kanonischer `hd-hobbyregister-core/data` vorhanden;
- ready PASS;
- count 862;
- aktiver Datenpfad korrekt auf kanonischen Ordner;
- 862/862 Profile;
- Index PASS.

PHP-Lint / Fresh-Unpack PASS.

Kein Live-PASS behaupten.
