# P33 – M01–M33 KISS-CROSSWALK

Datum: 2026-09-08
Status: GO – KEINE NEUE ARCHITEKTUR AUS HISTORISCHEN FEHLERN ABLEITEN

## Harte Auditbasis

Vorhandener autoritativer Runner wiederverwendet:
`control/startmaster0107/HOBBYRAUM_M01_M33_REGRESSION.py`

Kein zweiter Regression-Runner gebaut.

Geprüfter aktueller main:
`2325f6e18bcd8cbb491a604780ee5b65d4bbf8ea`

Aktueller main-Status:
- 28/33 PASS
- 5/33 FAIL: M15, M16, M17, M22, M26

Diese fünf Fehler werden in der Alternativroute NICHT repariert.
Sie stammen aus dem parallel weiterentwickelten bestehenden STARTMASTER-Weg.

## KISS-Regel für den Crosswalk

Historische Fehler liefern Sicherheitsanforderungen.

Sie erzwingen NICHT automatisch:
- dieselbe alte Raumarchitektur
- dieselben alten Zwischenartefakte
- dieselben alten Formulierungen
- neue Ersatz-Gates

Wenn eine einfachere Architektur dieselbe Sicherheitsanforderung bereits hart erfüllt:
alte Implementierung nicht kopieren.

## Crosswalk

| M | Sicherheitsziel | KISS-Zielarchitektur | Status |
|---|---|---|---|
| M01 | State/Hash-Bindung | ein kanonischer Job + signiertes Jobmanifest; vorhandener Entry bleibt außen | ABGEDECKT |
| M02 | keine Artikelkollision | eindeutige Item-IDs/Release-Identitäten + vorhandene Artikel-Namensbindung | ABGEDECKT |
| M03 | Restart ohne PREPARED-Schleife | kein Zwischencheckpoint: unvollständiges Item startet am ersten Schritt neu | VEREINFACHT |
| M04 | Finalisierung real aufrufbar | vorhandene äußere Finalisierung wiederverwenden | REUSE |
| M05 | durable Release/Receipt | vorhandene durable Release-/Endstempel-Infrastruktur wiederverwenden | REUSE |
| M06 | kein Fake-Produktionsvertrag | exakte PPM/PSERC-Pakethashes + feste Schemas | ABGEDECKT |
| M07 | Recovery nicht automatisch final | nur extern signiertes/verifiziertes Release darf weiter | ABGEDECKT |
| M08 | exaktes PPM | P3 hashbindet Original PPM 6.7.9 | ABGEDECKT |
| M09 | exaktes PSERC | P3 hashbindet Original PSERC-FIX | ABGEDECKT |
| M10 | Preflight fail-closed | vorhandener Entry/Preflight + feste Paketidentität | REUSE |
| M11 | echter PPM-Aufruf | feste PSERC→PPM-Seam, real geprüft | ABGEDECKT |
| M12 | Fake-PPM blockieren | kein wählbarer Enginepfad; nur hashgebundenes Original | ABGEDECKT |
| M13 | finaler Content-Hash | prepare-Payload/Fingerprint + externe Signatur + Readback | ABGEDECKT |
| M14 | Current-Action-Handoff | bestehende Dateiübergabe unverändert wiederverwenden | REUSE |
| M15 | keine widersprüchliche/freie Handoff-Navigation | Zentralmaschine wählt Reihenfolge; Worker keine Next-Step-/Handoff-Wahl | ABGEDECKT; alter Wortlauttest auf main rot |
| M16 | Signer außerhalb Worker | P7/P8: externer Signer, privater Schlüssel nie beim Producer | ABGEDECKT; stärker als Altmarker |
| M17 | kein Final-PASS ohne externe Finalisierung | ohne externe Signatur/Verifikation kein Write; alte 107008-Mechanik nicht in Kern kopieren | ABGEDECKT / VEREINFACHT |
| M18 | Endstempel-/Importvertrag | vorhandenen äußeren Endstempel wiederverwenden | REUSE |
| M19 | GitHub-Endstempel-Trigger | vorhandene GitHub-Infrastruktur wiederverwenden | REUSE |
| M20 | Delivery vollständig hashgebunden | vorhandene Delivery + signiertes Release | REUSE |
| M21 | kein Auto-Publish | durchgehend publish_allowed=false; Draft-only | ABGEDECKT |
| M22 | Herkunft/Preproduction geschützt | keine interne Signierung neu einführen; feste Paketidentität + bestehender Entry + externe Endsicherung | SICHERHEITSZIEL BEHALTEN, ALTES H8-MECHANISMUS NICHT KOPIEREN |
| M23 | nur autorisierter Produktionsweg | feste hashgebundene Originalkomponenten + bestehender Entry | ABGEDECKT |
| M24 | kein Rollback auf alten unsicheren Stand | feste Versions-/Hashbindung; bestehender Hardlock bleibt außen | ABGEDECKT / REUSE |
| M25 | keine freie Neuplanung | Zentralmaschine + gebundene Worker; PSTE/PSERC ohne Content-/Workflowfreiheit | ABGEDECKT |
| M26 | echter aktueller Fact-Pack/Plan-Kontext | gebundener Codex-Worker erzeugt aktuellen Fact-Pack; PPM prüft Source-/Planbindung | ABGEDECKT; alter Wortlauttest auf main rot |
| M27 | aktuelle main-/Umgebungsidentität | bestehenden Chat→Codex-/Preflight-Weg wiederverwenden | REUSE |
| M28 | Handoff materiell ausführbar | bestehende exakte 16-Feld-Request wiederverwenden | ABGEDECKT |
| M29 | Release an Batch/Count gebunden | signiertes Jobmanifest + feste Release-Identität; vorhandene Metadata-Prüfung bleibt | ABGEDECKT / REUSE |
| M30 | kein Kontextwechsel zwischen Batchstufen | ein kanonischer Job; signierte Item-/Job-Identität; vorhandene Finalprüfung bleibt | ABGEDECKT |
| M31 | kein synthetischer Executor | aktueller Codex-Worker ist gebunden; kein zweiter Executor | ABGEDECKT |
| M32 | PPM-Pfad fest gebunden | repositorygebundener exakter Paketpfad/Hash; keine Runtime-Auswahl | ABGEDECKT |
| M33 | Endstempel ohne Codex-Git-Auth | vorhandener GitHub-Endstempel + externe Signertrennung | REUSE |

## Die fünf aktuellen main-FAILs

### M15
Alter Regressionstest erwartet wörtlich:
`Kein Vorab-Handoff durch den Worker`

Der aktuelle Workflow wurde inzwischen anders formuliert.

Für die Alternativarchitektur zählt die Sicherheitsanforderung:
Worker darf Handoff/Next Step nicht wählen.

P11/P27/P32: PASS.

Keine Reparatur hier.

### M16
Alter main-Test erwartet eine bestimmte Signer-Markierung in `runtime_entry_gate.py`.

Alternativroute:
P7/P8 beweisen real die stärkere Grenze:
privater Schlüssel außerhalb Producer/Importer.

Keine Zusatzarchitektur.

### M17
Alter main-Test erwartet `host_pserc_finalization_required`.

Alternativroute benötigt diesen alten Mechanismus nicht im Zentralmaschinenkern:
prepare -> externe Signatur -> Verifikation -> exakt gebundener Draft-Write.

Fehlende Signatur = BLOCKED.

### M22
Current-main-Test scheitert in der isolierten Auditkopie an
`CODEX_BOUND_CAPSULE_MISSING`.

Das ist ein Zustand der bestehenden Entry-/H8-Infrastruktur.

Für die Alternativarchitektur wird daraus KEIN neues H8-System gebaut.
Die bestehende Entry-Infrastruktur wird später nur wiederverwendet.
Interne Signierung wird ausdrücklich nicht neu eingeführt.

### M26
Alter Regressionstest erwartet den Wortlaut
`reale Nicht-PPM-Stage-Artefakte`.

P26/P27 haben die zugrunde liegende fachliche Anforderung bereits geprüft:
aktueller gebundener Worker erzeugt Recherche/fact_pack und aktuelle Produktionskontexte; PPM validiert deren Bindung.

Keine Wortlautreparatur im Parallelchat.

## Gesamturteil P33

Keiner der 33 historischen Fehler erzwingt eine neue zusätzliche Architektur im Alternativweg.

KISS-Ziel bleibt:

`bestehender Chat/Codex-Entry -> eine Zentralmaschine -> vorhandene Fachbausteine -> prepare -> externe Signatur -> verifizierter Draft-Write -> Readback/DOM -> kein Publish`

Historische Sicherheitsziele bleiben erhalten.
Alte technische Umwege werden nicht automatisch mitkopiert.
