# Affiliate-Zentrale 6.72.199 — interner Candidate-Gate 07.10.2026

**Rolle:** Evidence/Nachweis. Keine Current-/NEXT-ACTION-Autorität.

## Bindung

- Branch: `affiliate-release-current`
- Testlauf: `37606358698`
- Test-Head: `f6e6d62b5d23d6768f09dd2236d4872d84b2a020`
- Source-Manifest: `release/affiliate-zentrale/CURRENT_SOURCE_SHA256.txt`
- Source-Manifest-SHA-256: `85554ba74ccbac2a81abe15b63243c5128d6d06c7634161e32ad52504fb72800`
- Source-Dateien: 28
- Nach dem erfolgreichen Lauf wurden keine Plugin-Source-Dateien mehr geändert. Danach wurden nur der temporäre Workflow entfernt und Current nachgezogen.

## Tatsächlich ausgeführter PASS

Run `37606358698` / Job `112742685919`:

- Governance / Source / Tree / Start: PASS.
- PHP-Lint des aktuellen Plugins: PASS.
- Frische WordPress-7.1.2-/MariaDB-Installation: PASS.
- installierter Pluginbaum gegen Manifest: PASS 28/28 byteidentisch.
- statischer ADCELL-Basisvertrag: PASS.
- ADCELL mocked WordPress/MariaDB E2E: PASS.
- 6.72.198 -> 6.72.199 Upgrade-E2E: PASS.
- Tarifcheck / CHECK24 / manueller Bannerimport E2E: PASS.
- Verify-before-Assign: PASS.
- fehlgeschlagenes Bild bleibt fail-closed; späterer echter Reimport öffnet nur die technische Prüfung erneut: PASS.
- bestehende Bannerregression: PASS.
- Installer-Fresh-Unpack / Byteidentität: PASS 28/28.
- ZIP-Integrität: PASS.

## Candidate-Installer

- Datei: `AFFILIATE_ZENTRALE_6.72.199.zip`
- Innerer Installer SHA-256: `dba7441a02821385ed723c031000f390f05c5c17e33a9a5f9e2e388281c3393b`
- Größe: `816205` Bytes
- GitHub-Actions-Artifact-ID: `11475087240`
- Actions-Container-Digest: `sha256:67ac0d8ea12593b529c9a2eaf75c7843a6ba147891e3d51118a4624754660967`

## Nicht ausgeführt

Der echte ADCELL-Provider-Gate wurde **nicht** ausgeführt, weil im Repository-Lauf keine Werte für
`PPAR_ADCELL_USERNAME`, `PPAR_ADCELL_PASSWORD` und `PPAR_ADCELL_PROGRAM_IDS` vorhanden waren.

Daher ausdrücklich **kein Real-ADCELL-PASS** und noch keine Releasefreigabe.

## KISS / PASS-Reuse

Die oben genannten internen PASS-Nachweise sind bei unverändertem Source-Manifest gültig und werden **nicht noch einmal wiederholt**.

Keine neuen oder zusätzlichen Tests erfinden. Keine Einzeltests aus Vorsicht wiederholen. Nur der in Current gebundene erste offene Gate darf als nächstes ausgeführt werden. Erst wenn dieser einen konkreten Fehler zeigt, wird genau dieser Fehler behoben und nur die dadurch stale gewordene Evidence erneut geprüft.
