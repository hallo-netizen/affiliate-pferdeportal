# AFFILIATE-ZENTRALE — CURRENT MASTER

Stand: 2026-09-17
Workstream: `AFFILIATE_ZENTRALE`
Status: `BLOCKED / CURRENT-SCOPE RECONCILIATION REQUIRED`

## Eine Release-Wahrheit

- Repository: `hallo-netizen/affiliate-pferdeportal`
- Arbeitsbranch: `affiliate-release-current`
- Kanonische Source: `release/affiliate-zentrale/current/affiliate-portal-router/`
- Kanonisches Manifest: `release/affiliate-zentrale/CURRENT_SOURCE_SHA256.txt`
- Release-Governance: `control/release-governance/CURRENT_RELEASE.json`
- Kanonischer aktiver Kandidat bleibt **6.72.19**; `release_allowed=false`.
- Pluginbuero `PPA-001/CURRENT.zip` bleibt **6.72.19**. Lokale hoehere Testlinien sind keine zweite Release-Wahrheit.

## Aktueller Fachstand

Verbindliches Fachregister fuer Werbeplaetze:
`/Pferde-Atelier/Aktenschraenke/Affiliate/WERBEPLATZ_REGISTER.md`

Aktuell gebunden:
- Kategorie-Querbanner zuerst vollstaendig fertigstellen.
- Downscaling bevorzugt; Upscaling hoechstens +10 %; proportional, kein Crop, keine Verzerrung.
- Providerneutraler Bestand/Matcher: Provideradapter duerfen nur beschaffen/importieren; technische Eignung, Themenmatch, Rotation und Ausspielung bleiben zentral.
- Neue Partner/Werbemittel muessen nach Sync/Upsert erneut in die Zuordnung eingehen; neue Adapterprovider ohne Umbau des Matching-Kerns.
- Backendfilter primaer nach **Werbeplatz** und aus derselben Slotmatrix/demselben Matcher wie die Ausspielung; keine zweite Pixel-/Providerlogik.
- Keine Abnahme ohne ausgefuehrte harte lokale POSITIV-/NEGATIV-/Gesamtworkflowpruefung inklusive Regression, Fresh-Unpack und Mutation/Sabotage. Live-PASS ist danach separat.

Gebundener Repo-Auftrag:
`protocol/AFFILIATE_RELEASE_CATEGORY_BANNER_WERBEPLATZ_FILTER_TASK_20260917.md`

## Lokale Testlinie — Diagnose/Testoracle, NICHT kanonisch

- 6.72.36: Fullchain lokal hart PASS; LIVE offen. SHA-256 `1cf141d4aae60d7b817bf503dd0e6328280b2527d1f2e219e4195a7a0fda07c0`.
- 6.72.37: Kategorie/Provider lokal 29 PASS / 0 FAIL + Browser-Runtime; LIVE offen. SHA-256 `08f07a772a3ca29520ef86270ed7c32d624789160fd2b056dcaaf79589da74c6`.
- 6.72.38: Werbeplatzfilter lokal Fresh-Unpack 39 PASS / 0 FAIL, Planer-Regression 1120/1120, kombinierter 1200-Zeilen-Filtertest und Mutationstests PASS; echter WordPress-Live-Readback offen. SHA-256 `3791eebbdfdcaafa6af265eb1ad6c47cefc715217f149dcdc94d5bc474556f9b`.

Diese Linie verletzt als nichtkanonische Fortsetzung die bereits gebundene Nicht-Wiederholungsregel `AF-069`/`AFF-ERR-006` und darf deshalb **nicht** als Release, Pluginbuero-CURRENT oder Quelle weitergefuehrt werden. Ihre Tests duerfen nur als Oracle fuer den einen kanonischen Rootfix dienen.

## Live-Stand

- Die **exakt aktuell installierte WordPress-Pluginversion ist nicht autoritativ read-back-belegt**. Nicht raten.
- Der letzte reale Backend-Screenshot `Import & Auswahl` zeigt **keinen Werbeplatzfilter**. Damit ist 6.72.38 im Live-System nicht nachgewiesen und fuer diese Funktion kein LIVE-PASS zulaessig.
- Kein weiterer Installer und keine neue Versionsnummer, bevor die kanonische Sourcearbeit und die gebundenen lokalen Gates abgeschlossen sind. Vor Versionswahl muss die reale installierte WordPress-Version belegt werden (`AF-027`).

## Frischecheck-Befund / erster offener Blocker

`control/release-governance/CURRENT_RELEASE.json` ist fuer die **Release-Source** korrekt auf 6.72.19 gebunden, fuehrt aber im dynamischen `user_scope_lock.current_focus` und `execution_state.bound_user_scope_action` noch den vorherigen **ADCELL**-Fokus. Der aktuelle ausdrueckliche Nutzer-Scope ist inzwischen Kategorie-Querbanner + Werbeplatzfilter.

Damit liegt aktuell eine **CURRENT-SCOPE-Drift** vor. Diese wird nicht durch Raten ueberschrieben. Solange Governance-Scope und CURRENT MASTER nicht atomar auf denselben Fachscope zeigen, bleibt der technische Einstieg BLOCKED.

## NEXT ACTION — exakt eine

**Governance-Scope atomar auf den bereits gebundenen 2026-09-17-Auftrag `protocol/AFFILIATE_RELEASE_CATEGORY_BANNER_WERBEPLATZ_FILTER_TASK_20260917.md` nachziehen, ohne die kanonische 6.72.19-Source, Manifestbindung oder `release_allowed=false` vorzeitig zu veraendern.**

Dabei muessen die bestehenden immutable Guard-Vertragswerte und der erlaubte `authorized_next_action`-Enum unveraendert respektiert werden. Kein Pluginbuild, kein Installer, keine Versionswahl.

**Erst nach diesem Governance-Frischecheck:** `AFFILIATE_HOBBYRAUM/TASK.current.json` ausfuehren. Das ist ein read-only kanonischer Delta-Precheck und darf ebenfalls keinen Build/Installer erzeugen.

Danach darf aus der kanonischen Source genau **ein** Rootfix-Kandidat entstehen. Vor irgendeinem Installer muss derselbe Kandidat die im gebundenen Task verlangte harte lokale POSITIV-/NEGATIV-/Gesamtworkflowpruefung bestehen.

## Verbindlicher Arbeitsweg

1. `AFFILIATE_HOBBYRAUM/START_HERE.txt`
2. diese `protocol/AFFILIATE_RELEASE_MASTER_CURRENT.md`
3. Frischecheck: Branch + Governance + kanonisches Manifest + Fehlerregister
4. zuerst den oben belegten Governance-Scope-Drift beheben
5. dann `AFFILIATE_HOBBYRAUM/TASK.current.json`
6. nach bestandenem Precheck: ein kanonischer Rootfix, keine Versionskaskade
7. vollstaendige harte lokale Gates
8. erst dann Live-Testinstaller; Live-PASS nur mit realem WordPress-Readback

## Nicht anfassen

- keine weiteren lokalen Versionsspruenge/Diagnose-ZIPs;
- keine eBay-PRIVATE-/Checkpoint-Massenmutation;
- keine OTTO-Cleanup-Neuarchitektur;
- kein Designplugin fuer diese Facharbeit;
- keine zweite Werbeplatz-/Pixel-/Provider-Wahrheit;
- keine Backendpfade raten.

## Fehler-/Prozessbindung

Bindend mindestens:
- `AFF-ERR-001`: kein Gesamt-/Release-PASS ohne echte Evidence;
- `AFF-ERR-006`: keine Mini-Fix-/Versionskaskade;
- `AFF-ERR-007`: Backendpfade nur real belegt;
- `AFF-ERR-009`: Slot/Format nicht im Providercode hart verdrahten;
- `AFF-ERR-010`: Re-evaluation bei wachsendem Portal/Bestand;
- `AFF-ERR-025` / `AF-057`: CURRENT-/Task-Drift nach Scopewechsel verhindern;
- `AF-021`: `TASK.current.json` schemaexakt;
- `AF-027`: reale installierte Version vor Versionswahl;
- `AF-069`: nichtkanonische Folgepakete nicht als kanonisch behandeln.

Historie bleibt in Git-History/Protokollen. Dieses Dokument enthaelt nur den aktuellen belastbaren Stand, den ersten offenen Blocker und die eine NEXT ACTION.
