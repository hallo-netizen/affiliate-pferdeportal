# Affiliate Router 6.72.186 – REAL WORDPRESS LIVE FAIL – Guardian auf Reithelme und Schabracken

Datum: 2026-10-05
Workstream: AFFILIATE_ZENTRALE
Branch: affiliate-release-current
Version: 6.72.186
Status: LIVE FAIL / ROOT CAUSE OPEN / KEIN NEUER FIX VOR DIAGNOSE

## Reale Live-Evidence

Nach Installation des exakt getesteten Installers
`AFFILIATE_ZENTRALE_6.72.186.zip`
mit SHA-256
`1ca526ce92f339c678f2dc6e8775eae31355414668b8e06ed4afd561d5c15cae`
zeigt der reale WordPress-Frontendzustand weiterhin fachlich falsche Banner.

Benutzer-Screenshot 2026-10-05 13:32 lokal:
- reale Seite Schabracken;
- sichtbarer Banner: Guardian Horse;
- Produktkarten darunter sind Schabracken, die Seite selbst ist also eindeutig der Schabracken-Kontext.

Frischer öffentlicher Read-only-Readback nach der Installation:
- Commit: `6d54e1fa622771a9effa9e106eef97af6407e9cb`
- Run: `37304066825`
- Reithelme: Promo `185797`
- Schabracken: Promo `185797`
- jeweils mehrfach normal und mit Cache-Bust identisch.

Damit ist 6.72.186 real widerlegt. Der lokale/CI-Red-Green-Beweis ist kein Live-PASS.

## Was 6.72.186 bewiesen hat – und was nicht

6.72.186 hat den Auswahlvertrag gegen kontrollierte WordPress/MariaDB-Fixtures bewiesen:
- nur höchste vorhandene Relevanzstufe bleibt ausgabefähig;
- ein einziger Best-Tier-Banner bleibt fix;
- mehrere Banner derselben Best-Tier-Stufe rotieren nur innerhalb dieser Stufe;
- 139/139 Universalassertions PASS;
- 0 Frontend-HTTP;
- Performance-Hardlock PASS.

Nicht bewiesen wurde damit, dass der reale Live-Datenbestand für Reithelme und Schabracken die fachlich richtigen Banner mit der richtigen gespeicherten Zielkante überhaupt als beste Kandidaten in den Rankingpfad einspeist.

Der reale Fehler liegt daher vor dem Abschluss der Best-Tier-Auswahl oder in deren realer Datenbasis. Welche konkrete Ursache gilt, ist noch NICHT bewiesen.

## Nicht raten – offene Root-Cause-Frage

Für Seite 186 Reithelme und Seite 193 Schabracken muss der reale Kandidatenbestand read-only erfasst werden.

Für jeden real lieferbaren Banner müssen mindestens feststehen:
- Kampagnen-/Creative-ID bzw. Promo-ID;
- `active`;
- `source`;
- `assignment_mode`;
- gespeicherte `automation_target_keys`;
- `destination_url` und Ziel-URL-Provenienz;
- `placements`;
- technische Slot-Eignung;
- berechnete `specificity`;
- berechneter Ranking-`reason`;
- Position / tatsächlich ausgewählter Kandidat.

Zusätzlich ausdrücklich prüfen:
- Reithelm-Creative `322674`: existiert es real noch aktiv/materialisiert, ist es technisch slotfähig und besitzt es die erwartete exakte Reithelm-Zielkante?
- welche Schabracken-spezifischen Creatives existieren real überhaupt, mit welcher gespeicherten Zielkante und welchem Status?
- warum Promo `185797` auf beiden Seiten die beste ausgabefähige Stufe erreicht bzw. warum ein fachlich genauerer Kandidat davor fehlt oder ausscheidet.

## Performance-Hardlock

Während dieser Diagnose keine Änderung an Frontend-Hotpaths.

Verboten:
- neue Frontend-DB-Abfragen;
- Frontend-HTTP;
- erneute Ziel-URL-Klassifikation beim Seitenaufruf;
- Vollscan des Creative-/Produktbestands im Frontend;
- Änderung der geschützten Ranking-/Render-/Distribution-Hotpaths nur zur Diagnose.

Die Diagnose muss read-only bzw. außerhalb des öffentlichen Hotpaths erfolgen.

## Historische Einordnung

Die bisherigen Reparaturen lösten jeweils reale Teilfehler:
- 6.72.182: vollständiger Kandidaten -> Technik -> Relevanz -> Auswahl -> Renderer-Pfad;
- 6.72.183: Creative-Library als zentrale gespeicherte Ziel-URL-/Zielkanten-Wahrheit;
- 6.72.184: Legacy-Automatik aus automatischem Pool + Banner-only-Migration;
- korrigierte 6.72.184: stale gespeicherte Zielkante vor Re-Evaluation entfernen;
- 6.72.185: eigene Versions-/Migrationsgeneration;
- 6.72.186: Rotation darf die beste Relevanzstufe nicht verlassen.

Der neue Live-Fail beweist, dass diese Teilkorrekturen nicht ausreichen, solange die reale Kandidaten-/Zielkantenbasis für die konkrete Seite nicht exakt diagnostiziert ist.

## NEXT ACTION

`DIAGNOSE_REAL_LIVE_CANDIDATE_POOL_AND_SPECIFICITY_FOR_REITHELME_186_AND_SCHABRACKEN_193_BEFORE_ANY_FIX`

Kein neuer Installer und keine neue Version vor diesem Root-Cause-Beweis.
