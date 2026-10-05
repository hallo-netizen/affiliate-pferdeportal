# HD-001 – KATEGORIE-WORKFLOW – CURRENT

STAND: 2026-10-05
STATUS: LIVE-FEHLER REPRODUZIERT / V1.9.7 FRONTEND-ENDSTATE LOKAL HARD PASS / LIVE-UPDATE OFFEN

## Reale Live-Wahrheit

Aktuell beobachtet:
- `Buchbinden` ist im Frontend sichtbar;
- direkte Unterkategorien sind dort nicht sichtbar.

Damit ist der bisherige Workflow trotz technischem Write-/Readback **nicht end-to-end abgenommen**.

## Root Cause

`Buchbinden` = WordPress-Seite.
Direkte Kinder = WordPress-Taxonomie-Terme.

Cross-Adapter-Parenting wurde bisher nur logisch über `_apkw_parent_concept_id` gespeichert.
Es existierte kein persistenter Frontend-Renderer für diese Beziehung.

Der bisherige Readback prüfte die WordPress-Objekte und Metadaten, nicht den tatsächlichen sichtbaren Seiteninhalt.

## V1.9.7

Gleiche Pluginlinie, kein Zusatzplugin.

Gezielter Fix:
- persistenter verwalteter Kinderblock im `post_content` der Elternseite;
- direkte Content-Kinder werden dort mit echten WordPress-Links ausgegeben;
- HivePress-/Marketplace- und Magazin-Knoten werden ausgeschlossen;
- redaktioneller Inhalt außerhalb des Blocks bleibt erhalten;
- Sparse-Erweiterung ergänzt/ändert nur den Block;
- keine automatische Löschung;
- kein Laufzeit-Frontendfilter;
- Block gehört zum strukturellen Readback;
- Frontend-Mismatch → Rollback.

## Harte Positiv-/Negativ-E2E

Vor Fix:
- Write PASS;
- technischer Readback PASS;
- Publish-Status PASS;
- Frontend FAIL wegen leerem Seiteninhalt.

Nach Fix mit echter Buchbinden-Topologie:
- Einstieg sichtbar/verlinkt PASS;
- Ausrüstung sichtbar/verlinkt PASS;
- Material sichtbar/verlinkt PASS;
- Techniken & Praxis sichtbar/verlinkt PASS;
- Buchbinden Set nicht im Contentblock PASS;
- Buchbinden Online nicht im Contentblock PASS;
- Idempotenz PASS;
- spätere zusätzliche Kategorie ohne Gesamtumbau PASS;
- bestehender Seiteninhalt erhalten PASS;
- Managed-Block-Tamper BLOCKED;
- kaputte Marker BLOCKED;
- Frontend-Endzustand manipuliert → Readback FAIL + Rollback PASS;
- Rename/Delta ohne Parent-Neuaufbau PASS.

Gesamtsuite:
- 275/275 PASS;
- Fresh Source 275/275 PASS;
- Runtime-Parität 23/23 PASS;
- Source PHP 17/17 PASS;
- Installer PHP 17/17 PASS.

Installer:
`AFFILIATE_PORTAL_KATEGORIE_WORKFLOW_V1.9.7_FRONTEND_ENDSTATE_HARD_PASS.zip`

Installer SHA-256:
`89790e0b12b4c72c96c8c5a9387dabc160c21707d6147e65898303eef70a0f40`

Source:
`QUELLCODE_KATEGORIE_WORKFLOW_V1.9.7_FRONTEND_ENDSTATE_HARD_PASS.zip`

Source SHA-256:
`7d324512d2d0e89faac82be50b54bd580facb4e2eef782eba32ab0ce8378af1a`

## Beleggrenze

Noch kein Live-PASS für V1.9.7.
Keine weitere Version bauen, bevor der reale Frontend-Readback dieses exakt simulierte Ergebnis bestätigt oder widerlegt.

## NEXT ACTION

V1.9.7 installieren → bestehenden Buchbinden-Stand einmal veröffentlichen/republishen → Frontend prüfen.

PASS nur wenn Buchbinden im sichtbaren Seiteninhalt exakt die vier direkten Content-Kinder zeigt.
