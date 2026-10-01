# HOBBYRAUSCH – TEXT_REDAKTION – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-01
STATUS: HD-001 PRODUKTIV LIVE PASS / HDTE LIVE WEITER BLOCKED PLAN_HASH_MISSING / V0.1.3 NICHT ABGENOMMEN / V0.1.4 COMPLETE ADMIN→REQUEST WORKFLOW POS+NEG HARD PASS

## HD-001

Produktiver Buchbinden-Pilot:
- deployed;
- Schreiben und Readback erfolgreich;
- Bestand bleibt live;
- 7 Owner / 11 ARTICLE_ONLY / 11 gebunden.

## HDTE Live

Owner-Handoff:
PASS.

Gesamtbestand:
erfasst.

Portalabgleich:
weiterhin
`BLOCKED · HDTE_CONTEXT_STAGE_PLAN_HASH_MISSING`.

0.1.3 ist deshalb nicht live abgenommen.

## Warum 0.1.3 nicht genügte

Der PHP-Worker war request-getrennt getestet.
Nicht vollständig bewiesen war der reale erste Backend-Einstieg:
BLOCKED-Job → Browser-JavaScript → erster AJAX-Request.

Live blieb der Job auf BLOCKED.

## HDTE 0.1.4

Installer:
`HOBBY_DEPOT_SEO_THEMENENGINE_V0.1.4_SERVER_SIDE_RESUME_FULL_WORKFLOW_HARD_PASS.zip`

SHA:
`02d52e326cce990833fb6661885d3ba5e30ab6461af76e8b0a2ebdcc3b78c12d`

0.1.4 macht die erste Wiederaufnahme serverseitig beim Öffnen der Übersicht.
Der Browser ist nicht mehr Voraussetzung dafür, den bekannten Blocked-State zurück auf RUNNING zu setzen.

## Vollständige lokale Abnahme

Exakter 0-Themen-Livezustand:
- alter Fehler reproduziert;
- Admin-Aufruf → RUNNING;
- jeder Folgeschritt separater Request;
- bis COMPLETE.

Zusätzlich:
- fehlendes altes Job-Planfeld → COMPLETE;
- kompletter Neuablauf → COMPLETE;
- 4-Themen-Stresslauf → COMPLETE;
- vorhandener Redaktionsplan → COMPLETE.

Negativ:
malformed NOT_AVAILABLE / vorhandener Plan / Structure-Mismatch / falscher Fehler / falsche Phase / fehlender echter Hash / manipulierte Stage / finale Strukturdrift / upstream nicht deployed
→ jeweils fail-closed.

Fresh Installer:
80/80 PHP PASS; 135/135 Dateiparität; kompletter Pos/Neg-Ablauf erneut PASS.

## NEXT ACTION

0.1.4 installieren → nur `Hobby Depot Themenengine → Übersicht` öffnen.

Keine neue Bestandserfassung.
Kein Handoff-Import.
Kein Research-Neustart.

Live-Abnahme erst bei:
`Portalabgleich COMPLETE`.
