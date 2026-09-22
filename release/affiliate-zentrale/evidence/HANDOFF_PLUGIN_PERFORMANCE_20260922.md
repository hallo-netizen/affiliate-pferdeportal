# Übergabe – Plugin-Performancebereinigung 2026-09-22

**Rolle:** kurzer Wegweiser. Diese Datei ist KEINE CURRENT-/Status-/NEXT-ACTION-Quelle.

## Einstiegspunkt / Bürotür
`release/affiliate-zentrale/AGENTS.md`

## Zuständige eine Current-Autorität
`control/release-governance/CURRENT_RELEASE.json`

## Frischecheck
- Branch: `affiliate-release-current`
- Current Generation: 91
- Current wurde gegen den Performance-Nachweis vom 22.09.2026 nachgezogen.
- Governance-Guardlogik: PASS.
- Canonical Source Manifest SHA-256: `ab1f4f54a7b0743e00ccbde5e1c11aa278a790ca47e5f72348bd125be9eabf29`
- Source-Dateiliste 26/26 gebunden; Hashprüfung PASS, einschließlich separat byteidentisch verifiziertem großen Portal-Structure-JSON.

## Aktueller belastbarer Stand
PPA-001 Affiliate-Zentrale:
- 6.72.145 live: SQL-N+1 beseitigt.
- 6.72.147: CPU-/Rankingbereinigung HARDTEST PASS.
- Runs: 35693134066, 35693058767, 35693264536 SUCCESS.
- ZIP SHA-256: `905f6db0941c04d0275aad3e63db8bdca80fb95f6659de2d2bb118359a9d72a5`.
- noch kein 6.72.147 LIVE-PASS.

PPA-013 Pferde Atelier Design:
- globaler Brand-Menü-Setup-Patch HARDTEST PASS.
- Real WordPress Run 35693870974 SUCCESS.
- zweiter Menü-Render Metadata-Hooks 2520 -> 360 (-85,7 %).
- Desktop-/Mobile-HTML unverändert.
- noch kein installierbares Paket, weil aktueller Live-Vollstand des Plugins nicht gebunden ist.

## Letzter sicherer Stand
Router-Rollback: 6.72.142 GOLDMASTER, unverändert und separat persistent gesichert.

## Erster offener Blocker
Exakter aktueller Live-Vollstand von PPA-013 ist nicht gebunden. Kein historisches Designpaket als Ersatz verwenden.

## Formale Current-NEXT-ACTION
`RUN_BOUND_RELEASE_GATES`

## Exakt gebundener nächster Arbeitsschritt
Aktuellen Live-Vollstand von PPA-013 exakt beziehen/binden, Version/Struktur/SHA prüfen, ausschließlich den bereits bewiesenen Brand-Menü-Setup-Cache-Patch anwenden, Source-/PHP-/Real-WordPress-Regressionsprüfung ausführen und genau einen separaten Design-Testkandidaten bauen.

## Verbindlicher Arbeitsweg
Bürotür -> Current -> Frischecheck -> ausschließlich gebundener PPA-013-Schritt.

## Nicht anfassen
- PPA-001 6.72.147 nicht neu bauen, solange kein neuer Testfehler vorliegt.
- 6.72.142 GOLDMASTER nicht überschreiben.
- Kubio nicht verändern.
- Astra/Theme nicht verändern.
- Banner-6.72.143-Arbeit bleibt pausiert.
- keine historischen Design-ZIPs als aktuellen Vollstand verwenden.

## Plugin-Refs
- Zielvertrag: `protocol/AFFILIATE_RELEASE_PERFORMANCE_CLEANUP_TARGET_20260922.md`
- Problem-/Arbeitsprotokoll: `protocol/AFFILIATE_RELEASE_PERFORMANCE_CLEANUP_PROTOCOL_20260922.md`
- Testevidence: `release/affiliate-zentrale/evidence/performance_cleanup_router_design_20260922.md`
- Zentrales Plugin-Protokoll: `/Pferde-Atelier/Aktenschraenke/PLUGINS/PLUGIN_UPDATEPROTOKOLL_20260916.md`, Vorgang PU-20260922-001.
