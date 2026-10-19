# HOBBY DEPOT – GLOSSAR-PLUGIN – ÜBERNAHMEPRÜFUNG

STAND: 2026-10-19
STATUS: QUELLBINDUNG OFFEN / KEIN INSTALLER

## Referenz

Pferde-Installation:
- Slug: `universal-glossary-engine`
- Version: **1.4.0**
- Hauptdatei: `universal-glossary-engine.php`
- zusätzlicher belegter Manager: `includes/class-uge-manager.php`

Bekannter Releaseverweis:
`UNIVERSAL_GLOSSARY_ENGINE_1.4.0_SAFE_MANAGER_RELATIONS_REVIEW_INSTALLIEREN.zip`

Bekannter SHA-256:
`fb75ff8044eff4383ba44dd6389b1aa97ff16ab500445037ce2d5819f2335231`

## Übernehmbar

Konzeptionell übernehmen:
- eigener Glossar-Inhaltstyp;
- Glossar-Gruppen/Themenwelten;
- Hauptseitenbindung;
- eigene Begriff-URLs;
- A–Z/Suche/Filter;
- strukturierter Draft-Import;
- Validator;
- Readback/Rollback;
- verwandte Begriffe;
- optionale Hauptseite;
- Reviewbedarf;
- kein Auto-Publish.

## Nicht übernehmen

- Pferdebegriffe und Pferdetexte;
- Pferde-Themenwelten;
- Pferde-IDs und URLs;
- Pferde-SEO-Formulierungen;
- Pferde-Designwerte;
- Bestandsmigration von Pferdebegriffen;
- historische autonome Discovery-/Cron-/Loopback-Logik als aktiven Weg.

## Noch nicht belegbar

Die exakten 1.4.0-Bytes liegen im aktuell erreichbaren Arbeitsbestand nicht vor. Deshalb sind konkrete Codefundstellen und ein bytegenauer Diff noch offen.

Keine ältere 0.2.x-Quelle als angebliche 1.4.0 ersetzen.
