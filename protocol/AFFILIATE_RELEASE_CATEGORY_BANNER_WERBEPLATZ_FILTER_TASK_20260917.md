# AFFILIATE-ZENTRALE — Kategorie-Querbanner + Werbeplatzfilter

Stand: 2026-09-17
Workstream: `AFFILIATE_ZENTRALE`
Status: `BOUND_TASK / NO_RELEASE_PASS`

## Ziel

Ausgehend ausschließlich von der kanonischen Source `release/affiliate-zentrale/current/affiliate-portal-router/` den bereits fachlich festgelegten Kategorie-Querbanner-Workflow und den Backendfilter nach Werbeplatz in **einen** kanonisch gebundenen Kandidaten überführen. Keine Versionskaskade, keine Nebenarchitektur.

## Verbindliche Fachregeln

1. Kategorieebenen nutzen nur die bereits vorhandenen Kategorie-Bannerplätze; großer Querbanner, proportional, kein Crop, keine Verzerrung.
2. Downscaling hat Vorrang; Upscaling maximal +10 %; größere Abweichung fail-closed.
3. Backend `Import & Auswahl`: zusätzlicher Filter nach **Werbeplatz**; Filterregeln müssen direkt aus derselben zentralen Slotmatrix/demselben Matcher wie die produktive Ausspielung kommen. Keine zweite Pixel-/Providerlogik.
4. Providerneutral: ADCELL, Awin, Digistore24, Direktpartner und registrierte Adapter werden nach ihren providerlokalen Sicherheitsgates im gemeinsamen Bestand/Matcher gleich behandelt. Keine hart codierte Providerbevorzugung.
5. Neue Partner/Werbemittel werden per bestehendem Upsert übernommen; nach Bestandsänderung muss die betroffene Zuordnung neu bewertet werden. Neue Provider dürfen über Registry/Adapter ohne Umbau des Matching-Kerns teilnehmen.
6. Gibt es kein gültiges Werbemittel, wird nichts gerendert; kein Platzhalter.

Fachregister außerhalb des Repositories: `/Pferde-Atelier/Aktenschraenke/Affiliate/WERBEPLATZ_REGISTER.md`.

## Bereits vorhandene lokale Diagnose-/Testbelege — NICHT kanonisch

Diese Belege dürfen als Testoracle/Delta-Hinweis dienen, **nicht** als Source- oder Release-Autorität:

- 6.72.36 Fullchain: SHA-256 `1cf141d4aae60d7b817bf503dd0e6328280b2527d1f2e219e4195a7a0fda07c0`; lokaler POS/NEG/Full-Workflow PASS, LIVE offen.
- 6.72.37 Kategorie/Provider: SHA-256 `08f07a772a3ca29520ef86270ed7c32d624789160fd2b056dcaaf79589da74c6`; 29 PASS / 0 FAIL + lokaler Browser-Runtime, LIVE offen.
- 6.72.38 Werbeplatzfilter: SHA-256 `3791eebbdfdcaafa6af265eb1ad6c47cefc715217f149dcdc94d5bc474556f9b`; Fresh-Unpack 39 PASS / 0 FAIL, 1120/1120 Planer-Regression, 1200-Zeilen-Filterkombination und Mutationstests PASS; echter WordPress-Live-Readback offen.

HARD RULE: Diese nichtkanonische Linie wird **nicht** direkt zum Release erklärt und nicht als Pluginbüro-CURRENT übernommen. `AF-069` / `AFF-ERR-006` bleiben bindend.

## Pflichtprüfung vor irgendeinem Installer

1. ERROR-REGISTER PRECHECK gegen `protocol/AFFILIATE_RELEASE_ERROR_REGISTER.md` und `AFFILIATE_HOBBYRAUM/FEHLERMATRIX.md`.
2. Exakte alte Fehlerlage reproduzieren (NEGATIV).
3. Exakten Fixfall ausführen (POSITIV).
4. Vollständigen betroffenen Gesamtworkflow lokal ausführen: Provider-Sync/Bestand → technische Eignung → thematische Zuordnung → Auswahl/Rotation → Veröffentlichungspfad → Frontend-Regel → Neu-Sync/Neubewertung → Backendfilter.
5. Providerregression: mindestens ADCELL + zweite Providerquelle oder Direktpartner; registrierter Adapterweg bleibt dynamisch.
6. Relevante historische eBay/idealo/Awin/ADCELL-/Automationsregressionen; unveränderte Teile byte-/hashgebunden wiederverwenden, nicht neu erfinden.
7. PHP-Lint, JS/JSON, Fresh-Unpack, Source↔ZIP-Identität, Mutation/Sabotage.
8. ERROR-REGISTER POSTCHECK.

**Keine Abnahme, kein Installer und kein PASS vor vollständig ausgeführter harter lokaler POSITIV-/NEGATIV-/Gesamtworkflowprüfung.** Live-PASS bleibt danach separat offen bis echter WordPress-Readback.

## Versionsregel

Vor Wahl einer neuen kanonischen Versionsnummer zuerst die tatsächlich live installierte WordPress-Version belegen (`AF-027`). Nicht raten. Bis dahin keine neue Versionsnummer und kein neuer Installer.

## Nicht anfassen

- keine eBay-PRIVATE-/Checkpoint-Massenmutation;
- keine OTTO-Cleanup-Neuarchitektur;
- keine Designplugin-Änderung;
- keine neue Werbeplatz-/Pixel-Zweitlogik;
- keine neue Pluginversion nur zur Diagnose.

## Abschlussbedingung

Erst wenn der eine kanonische Kandidat aus der committed Source sämtliche gebundenen lokalen Gates bestanden hat, darf exakt dieser Kandidat als Live-Testinstaller ausgegeben werden. Pluginbüro-CURRENT erst nach regelkonformer Source-/Manifest-/Evidence-Bindung; Live-Abnahme erst nach WordPress-Readback.