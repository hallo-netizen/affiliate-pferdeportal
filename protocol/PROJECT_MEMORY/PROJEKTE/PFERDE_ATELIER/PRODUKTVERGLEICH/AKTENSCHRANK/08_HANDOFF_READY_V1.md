# PRODUKTVERGLEICH – ÜBERGABEBEREIT V1

Stand: 2026-09-11
Status: HOLD / DURCH PV-SCALE-084-001 NOCH NICHT ÜBERGABEBEREIT

## Korrektur

Die frühere Freigabe war zu eng, weil 0.8.3 nur die Proofgruppe Regendecken vollständig belegte.

Autoritative Portalabdeckung:
- 329 Produktseiten;
- 1124 Artikelkategorien;
- 175 eindeutige Produktgruppen mit eigener `Vergleich`-Kategorie.

Regendecken ist 1/175.

Damit bleibt diese Übergabeakte auf HOLD, bis die generische Multi-Group-Abdeckung fachlich geschlossen ist.

## Was 0.8.3 weiterhin gültig beweist

- Dossier V2;
- gebundene Decision-Policy;
- A-vs-B = exakt 2 Produkte;
- Kostenwiederverwendung;
- fail-closed bei Null-Eignung;
- kein Auto-Publish.

Diese Beweise bleiben Regression-Basis für alle weiteren Gruppen.

## Vor erneuter Übergabefreigabe zwingend

- 175/175 Gruppen in portalgebundener Registry;
- jede Gruppe mit explizitem Readiness-/Coverage-Status;
- keine stille Auslassung;
- vollständige fachlich zulässige A-vs-B-Paarabdeckung je READY-Gruppe;
- Produktrecherche/Profil/Policy sichtbar vollständig oder explizit offen/blockiert;
- Kosten-/Resume-/Idempotenzschutz;
- globale Coverage-Prüfung;
- harte positive/negative/Fresh-ZIP-Prüfung.

## Spätere Schnittstellengrenze bleibt unverändert

Produktvergleich -> Dossier V2 -> bestehender SEO/TEXT-Fachworkflow -> bestehender `FACHWORKFLOW_HANDOFF_REQUEST.json` -> ACM.

Kein neues Handoff.
Kein zweiter Writer.
Kein Publish.
