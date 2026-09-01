# STARTMASTER0107 – dauerhafter CODEX_CLOUD Host-Bridge-Rootfix

Stand: 2026-09-01

## Nachgewiesene Ursache

Die produktive H1/H2-Single-Door-Schicht modellierte `execute_bound_action` als erzwungene Function-Tool-Capability eines OpenAI-Responses-Aufrufs. `single_door_boundary.py` definiert den Namen und die Request-Struktur, implementiert aber keine gleichnamige Codex-Cloud-Host-Capability. Ein Codex-Cloud-Task besitzt diese synthetische Function nicht automatisch.

Damit war die Route mechanisch beweisbar, aber im produktiven CODEX_CLOUD-Host an R_001 nicht ausführbar. Der Fehler lag in der Host-Adapter-Schicht, nicht in Artikelinhalt, Qualität, Recherche oder Signaturprüfung.

## Dauerhafte Lösung

Für den fest gebundenen Hard-Worker `CODEX_CLOUD` gilt im produktiven Raum R_001 nun ausschließlich:

- Die bereits durch den offiziellen Runtime-Entry materialisierte `.pferde-capsule` ist selbst die eine gebundene produktive Aktion.
- `project_single_door_entry_v2.py` prüft die Capsule mechanisch gegen Ticket, State-Hash, Bundle-Hash, Manifest und die exakt materialisierte Instruction.
- Bei PASS liefert der Project-Entry `worker_request=null`, `custom_function_capability_required=false` und `CODEX_CLOUD_BOUND_CAPSULE_PASS`.
- Codex darf `execute_bound_action` im produktiven 107007-Lauf weder suchen noch als Host-Capability voraussetzen.
- State-/Workflow-Navigation bleibt ausschließlich beim bestehenden Entrance Gate; der Worker darf keinen nächsten Schritt wählen.

Der alte Function-Tool-Mechanismus bleibt ausschließlich als technische Abstraktion für andere/ältere Single-Door-Transporte erhalten. Er ist nicht mehr die produktive CODEX_CLOUD-Hostanforderung in R_001.

## Unverändert

Keine Änderung an:

- Recherche- oder Fact-Pack-Regeln
- Text-/Inhaltsregeln
- Qualitätsregeln
- LanguageTool
- PPM / PSERC / PSTE
- Titel / Keywords / SEO
- Design
- Dubletten-/Kannibalisierungslogik
- Parallelisierung
- Signatur-/H8-Herkunftsprüfung
- Quarantäne / Release-Receipt-only
- Publish-Regeln

Die technische Bridge besitzt `content_semantics_authority=NONE`, `quality_authority=NONE`, `workflow_navigation_authority=NONE` und `publish_authority=NONE`.
