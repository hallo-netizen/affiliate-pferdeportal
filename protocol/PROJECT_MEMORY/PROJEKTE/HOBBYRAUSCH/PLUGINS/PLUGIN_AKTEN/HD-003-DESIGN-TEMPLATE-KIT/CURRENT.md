# HD-003 – HOBBY DEPOT DESIGN / TEMPLATE KIT – CURRENT

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-14
STATUS: **LIVE KRITISCHER FEHLER / NORMALE REPLACE-BUILDS GESPERRT / RECOVERY 1.50.658 LOKAL E2E PASS / KEIN LIVE-PASS**

## Letzter dokumentierter Vor-Reparatur-Build
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.652_HOBBY_DEPOT_HUB2_HERO_COMPACT_EXACT_SCENES_NOUPSCALE_LOCALPASS.zip`

SHA-256 laut Akte:
`c5c19f94b57c9dd95d88738f752e6e1ea5d880ea6d85ebc7bb31cfdd6b17234b`

Das exakte ZIP ist in den aktuell verfügbaren Projekt-/Library-/Conversation-Dateien nicht vorhanden. Es wird deshalb nicht rekonstruiert oder erfunden.

## Aktueller Reparaturstatus
1.50.653–1.50.657 nicht erneut verwenden.

Aktueller Recovery-Kandidat:
`HOBBY_DEPOT_RECOVERY_1.50.658.zip`

SHA-256:
`b5cda174d9162841ad983e7f69ace02111c25f81ae338ff0cdf237694e6296e1`

Der Recovery-Kandidat:
- prüft den echten Frontendzustand per WordPress-Loopback;
- sichert den aktuellen Pluginbaum vollständig;
- nutzt ein reales vorhandenes WordPress-Backup von 1.50.652 bevorzugt, falls vorhanden;
- sonst exakt den originalen 1.50.650-Baum;
- übernimmt einen Kandidaten nur nach realem Frontend-PASS;
- testet Fallbacks automatisch;
- rollt bei vollständigem Fehlschlag exakt auf den vorherigen Zustand zurück;
- deaktiviert doppelte Template-Kit-Instanzen vor Kandidatenaktivierung.

## Lokale Abnahme
- **11/11 E2E-Szenarien PASS**;
- Embedded 1.50.650: **981/981 Dateien SHA-identisch** zum Original;
- Payload PHP: **55/55 Syntax PASS**;
- `Druck & Fotografie` Render: PASS;
- Recovery-PHP: Syntax PASS;
- ZIP: PASS;
- Negativ-/Rollbackpfade: PASS.

Evidence:
`HOBBY_DEPOT_RECOVERY_1.50.658_LOCAL_TEST_EVIDENCE.json`

## NEXT ACTION
**Keine normale Template-Kit-Version installieren. Nur Recovery 1.50.658 als separates Plugin aktivieren; die echte Serverprüfung entscheidet automatisch über Behalten, Fallback oder Rollback.**
