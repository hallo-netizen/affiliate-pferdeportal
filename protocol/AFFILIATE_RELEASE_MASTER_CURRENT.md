# AFFILIATE-ZENTRALE — CURRENT MASTER

Stand: 2026-09-18
Workstream: `AFFILIATE_ZENTRALE`
Status: `ACTIVE / CANONICAL DELTA PRECHECK REQUIRED`

## Eine aktuelle Wahrheit

- Repository: `hallo-netizen/affiliate-pferdeportal`
- Arbeitsbranch: `affiliate-release-current`
- Kanonische Source: `release/affiliate-zentrale/current/affiliate-portal-router/`
- Kanonisches Manifest: `release/affiliate-zentrale/CURRENT_SOURCE_SHA256.txt`
- Release-Governance: `control/release-governance/CURRENT_RELEASE.json`
- Kanonischer Pluginstand bleibt **6.72.19**; `release_allowed=false`.
- Pluginbüro `/Campus-Plugins/PFERDE_ATELIER/PPA-001/CURRENT.zip` bleibt **6.72.19** / SHA-256 `72f437e5235aaec53631db052e2184b588366c7f8aa7eb72ae1c9e043cdf157f`.
- Lokale 6.72.60–6.72.65-Pakete sind Test-/Diagnoseoracle und ausdrücklich **keine zweite Release-/Current-Wahrheit**.

## Aktueller Nutzer-Scope / Zielvertrag

Gebunden:
`protocol/AFFILIATE_RELEASE_AUTOMATIC_CREATIVE_LIFECYCLE_SCOPE_20260918.md`

Fachquellen:
- `/Pferde-Atelier/Aktenschraenke/Affiliate/WERBEPLATZ_REGISTER.md`
- `/Pferde-Atelier/Aktenschraenke/Affiliate/KONZEPT_AUTOMATIK_LIFECYCLE_20260918.md`

Kernziel:
- Normalbetrieb vollautomatisch;
- neue valide Partner/Creatives ohne Pflichtklick aufnehmen;
- jederzeit manuell sperren/Veto/fixieren/bevorzugen und zur Automatik zurück;
- identische Creatives nur eindeutig/fail-safe deduplizieren; pro identischer Variante + Formatfamilie größte Originalversion produktiv;
- gleiches Bild mit anderem Text/CTA/Rabatt/Angebot bleibt getrennte Variante;
- zentrale Hintergrundprüfung: Bestands-/Partner-/Creative-Sync alle 2 Wochen, tiefer Integritätslauf alle 3 Wochen, plus `Jetzt prüfen`;
- verschwundene/deaktivierte/abgelaufene Creatives automatisch aus aktiver Eignung nehmen und betroffene Ziele neu bewerten;
- Providerstatus/echte Laufzeitdaten sind Autorität; keine OCR-/Bildtext-Erfindung von Ablaufdaten;
- Partner-/Einnahmen-Seite trennt lokale Klicks, Provider-Klicks und echte Reportdaten; fehlende Daten sind nicht `0 €`, Währungen werden nicht falsch als EUR addiert;
- KISS: kein Zwischenplugin. Ein neues Test-ZIP erst, wenn ein vollständig gebundener Technikblock konkret im WordPress getestet werden muss.

## Letzter sicher belegter Live-/Teststand

- Glossar-Linie **6.72.60**: Nutzer bestätigte Design/Position/Zentrierung LIVE PASS.
- Danach lokale Rassen-/Disclosure-/Kachelbreiten-Linie 6.72.61–6.72.63.
- Letzter Nutzer-Screenshot vor 6.72.63: **Produktkachelbreite FAIL**, Rassenseite **fast PASS**; gewünschte Abstände/Disclosure wurden danach lokal nachgezogen.
- 6.72.63: lokale Strukturchecks 10/10 PASS + Fresh-Unpack 26/26 byteidentisch; LIVE-Retest offen.
- 6.72.64: lokaler Hintergrund-Lifecycle-/Status-Prototyp; kein kanonischer Gesamtgate/LIVE-PASS.
- 6.72.65: lokaler Partner-Analytics-Wahrheitsfix; kein kanonischer Gesamtgate/LIVE-PASS.
- Nichtkanonische Testartefakte liegen getrennt unter `/Campus-Plugins/PFERDE_ATELIER/PPA-001/TESTARTEFAKTE_20260918/` und ersetzen CURRENT.zip nicht.

## Erster offener Punkt

Der 2026-09-18-Zielvertrag ist fachlich gebunden, aber sein exakter minimaler Delta zur **kanonischen 6.72.19-Source** ist noch nicht read-only bestimmt.

Daher darf jetzt weder aus 6.72.65 weitergebaut noch ein Installer erzeugt werden.

## NEXT ACTION — exakt eine

`AFFILIATE_HOBBYRAUM/TASK.current.json` ausführen:

`automatic-creative-lifecycle-canonical-precheck-20260918`

Zweck:
- kanonische 6.72.19-Source read-only gegen den gebundenen 2026-09-18-Vertrag prüfen;
- nur den exakten fehlenden Source-Delta ausgeben;
- **kein Build, kein Installer, keine Versionswahl**.

Erst danach:
1. genau ein minimaler kanonischer Rootfix-Kandidat;
2. vollständige harte lokale POSITIV-/NEGATIV-/Gesamtworkflow-/Regression-/Fresh-Unpack-/Source-Identitäts-/Mutationtests;
3. nur wenn danach ein konkreter WordPress-Livetest erforderlich ist: genau ein Testplugin;
4. LIVE-PASS ausschließlich nach echtem WordPress-Readback.

## Verbindlicher Einstieg für jeden Nachfolgechat

1. `AFFILIATE_HOBBYRAUM/START_HERE.txt`
2. diese `protocol/AFFILIATE_RELEASE_MASTER_CURRENT.md`
3. Frischecheck:
   - Branch `affiliate-release-current`
   - `control/release-governance/CURRENT_RELEASE.json`
   - `release/affiliate-zentrale/CURRENT_SOURCE_SHA256.txt`
   - `protocol/AFFILIATE_RELEASE_ERROR_REGISTER.md`
   - gebundener Scope `protocol/AFFILIATE_RELEASE_AUTOMATIC_CREATIVE_LIFECYCLE_SCOPE_20260918.md`
4. exakt die NEXT ACTION oben
5. `AFFILIATE_HOBBYRAUM/TASK.current.json`

`START_HERE.txt` bleibt nur Wegweiser und enthält keine eigene dynamische Standwahrheit.

## Nicht anfassen

- keine weitere lokale Versionskaskade;
- keine Übernahme von 6.72.60–6.72.65 als kanonische Source;
- `PPA-001/CURRENT.zip` nicht ersetzen;
- keine eBay-PRIVATE-/Checkpoint-Massenmutation;
- keine OTTO-Cleanup-Neuarchitektur;
- kein Designplugin für Affiliate-Fachlogik;
- keine zweite Werbeplatz-/Pixel-/Provider-/Lifecycle-Wahrheit;
- keine Backendpfade raten.

## Fehler-/Prozessbindung

Mindestens bindend:
- `AFF-ERR-001`: kein PASS ohne echte Evidence;
- `AFF-ERR-006`: keine Mini-Fix-/Versionskaskade;
- `AFF-ERR-009`: Provider/Format nicht hart verdrahten;
- `AFF-ERR-010`: Re-evaluation + zentraler periodischer Recheck;
- `AFF-ERR-011` / `AFF-ERR-026`: Partner-/Einnahmen-Wahrheit;
- `AFF-ERR-027`: lokale 6.72.60–6.72.65 niemals als zweite Current-Wahrheit;
- `AF-021`: Hobbyraum-Task schemaexakt;
- `AF-027`: reale installierte WordPress-Version vor späterer Versionswahl;
- `AF-069`: nichtkanonische Folgepakete nicht kanonisieren.

Historie bleibt in Protokollen/Git-History. Dieses Dokument enthält nur aktuellen Stand, ersten offenen Punkt und eine NEXT ACTION.
