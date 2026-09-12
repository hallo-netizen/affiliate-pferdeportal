# PB ONE – PLUGINS – UPDATEPROTOKOLL

STAND: 2026-09-12
ROLLE: ZENTRALES HISTORISCHES PLUGIN-ÄNDERUNGSPROTOKOLL

## Grenze

Genau ein Vorgang je tatsächlicher Pluginentwicklung/-aktualisierung.
Keine zweite Fach-, Release- oder LIVE-Wahrheit. Keine Secrets.

## PU-20260912-001 – Affiliate-Zentrale (Portal-kompatibel)

- **Plugin-ID / Name:** `PBO-PLUGIN-001` / `Affiliate-Zentrale (Portal-kompatibel)`
- **ART:** ENTWICKLUNG
- **Herkunft:** EIGENENTWICKLUNG
- **zuständiges Fachbüro:** `PROJEKTE/PFERDE_ATELIER/AFFILIATE/`
- **VON_VERSION:** `6.72.17` – letzter vor Integration frisch geprüfter Pluginbüro-Stand
- **AUF_VERSION:** `6.72.19`
- **Quelle / Branch:** `affiliate-release-current`
- **kanonische Source:** `release/affiliate-zentrale/current/affiliate-portal-router/`
- **WARUM:** ADCELL vollautomatisch über belegte API v2: accepted + active, explizite programId-Allowlist, CSV/Banner/Deeplink; kein Awin-Fallthrough und keine manuelle CSV-URL als Normalbetrieb. Der getestete ADCELL-Fix wurde auf den jüngsten vollständig geprüften Pluginbüro-Stand 6.72.17 integriert, statt eine ältere 6.72.8/6.72.9-Linie fortzuführen.
- **Abhängigkeiten / Schnittstellen:** WordPress; MariaDB über WordPress; ADCELL API v2; bestehende zentrale Creative-/Relevanz-/Asset-/Output-/Pause-/Veto-Logik. Awin/OTTO wurden regressionsgesichert, nicht in diesem Vorgang fachlich weiterentwickelt.
- **relevante Fehlerquelle:** ausschließlich `AFFILIATE_HOBBYRAUM/FEHLERMATRIX.md` auf `affiliate-release-current`, insbesondere AF-058 bis AF-068; keine Fehlerdetails hier duplizieren.
- **Backup-/Rollback-Referenz:** letzter frisch geprüfter Pluginbüro-Stand 6.72.17; kanonische 6.72.19-Source über Git-Historie + Manifest nachvollziehbar. Kein LIVE-Rollback ausgeführt.
- **Positivprüfung tatsächlich ausgeführt:** ADCELL accepted+active+allowlisted; API-v2 Static/Runtime; kanonischer Full-Gate-Lauf `34690118524` PASS.
- **Negativprüfung tatsächlich ausgeführt:** non-allowlisted / inactive / not accepted / falscher Host / mehrdeutige CSV-Lage fail-closed; kein Awin-Fallthrough; Lauf `34690118524` PASS.
- **Fach-/Regressionstest:** Awin/OTTO 18/18 PASS; Banner Positiv/Negativ PASS; PHP 21/21 PASS; Release-Guard Governance/Source/Tree/Start PASS; Fresh-Unpack/Source-Identity 26/26 PASS.
- **Artefakt-Nachweis:** kanonischer Neubau nach AF-067: Run `34692865477`, Job `103551115066` PASS; Test-ZIP SHA-256 `72f437e5235aaec53631db052e2184b588366c7f8aa7eb72ae1c9e043cdf157f`.
- **Closeout-Governance:** Run `34693281391`, Job `103552273581` PASS; AF-068 geschlossen.
- **ERGEBNIS:** `BLOCKED` nur für LIVE-Abnahme. Technische 6.72.19-Source-/Artefakt-Gates PASS; offen ist AF-066: read-only ADCELL-Live-API-Preflight im echten WordPress mit bereits gespeicherten API-Zugangsdaten, danach realer WordPress/MariaDB-E2E.
- **Fach-/Release-/LIVE-Autorität:** Affiliate-Fachbüro + `affiliate-release-current`; dieses Protokoll ist nur zentrales Kontrollpult.
