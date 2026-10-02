# K0 START

## Zentraler Befehl

`K0:start`

## Normalbetrieb

Bei angehängter gültiger `PSERC_TEXTMACHINE_METADATA_BATCH_V2`-Datei sofort arbeiten.

Der Nutzerablauf ist ausschließlich:

`Datei hochladen -> K0:start -> Portal automatisch erkennen -> vollständig produzieren -> verifizierte WordPress-Datei`

Keine Portalangabe im Befehl. Keine manuelle Portalauswahl.

## Auftrag

Die fünf Felder

`title + target_keyword + category + article_type + plan_slot`

sind die alleinige Job-Identität.

Die Portalzuordnung kommt ausschließlich aus `K0_PORTAL_REGISTRY.json` und muss eindeutig sein. Unbekannte oder mehrdeutige Zuordnung blockiert fail-closed.

## Qualität

Intern vollständig:

`Portalzuordnung -> Recherche -> Schreiben -> K0-Regelwerk -> LT 6.8 -> PPM-6.7.9-Parität -> PSERC/Exportprüfung -> ENDSTEMPEL -> WordPress-Datei -> STOP`

Keine Qualitätsregel lockern. Keine Performanceverbesserung zurücknehmen. `publish_allowed=false`.

## Autorität

Repository: `hallo-netizen/affiliate-pferdeportal`

Branch: `konzept0-portal-neutral-20261002`

Current: `K0_CURRENT_STATE.json`

K0 ist ein eigenständiger Fork der K10-Regelarchitektur. Kein Runtime-Import aus K10, kein Schreiben nach K10 oder K9.
