# PLAN A / PLAN B – SWITCHBOARD

ROLLE: neutraler Wegweiser für zwei vollständig getrennte technische Linien.
Keine Fach-/Inhalts-/Qualitätswahrheit. Keine zweite Fehlerquelle.

## HARTE REGEL

Plan A und Plan B werden:
- unabhängig gebaut;
- unabhängig geprüft;
- unabhängig dokumentiert;
- unabhängig gelagert;
- niemals innerhalb eines Teststands vermischt.

Kein Cherry-Pick, kein Teil-Merge, kein gemeinsamer Arbeitsbranch, kein "nur diese eine Datei" zwischen den Linien während der Vergleichsphase.

## PLAN A – BESTEHENDES SYSTEM

Zweck:
aktuellen bestehenden Produktionsweg mit kleinstmöglichem B01-Fix real prüfen.

Kandidat:
- Draft-PR #141
- Branch: `hobbyroom/b01-only-kiss-20260906`
- Head: `94917596adce04765380c60dd7ade0fb23793393`
- Base: `c8a96e7a2f598de69134d90b143257c3559bc98a`

Dokumentation:
- TEXT/HOBBYRAUM.md
- TEXT/PRE_CODEX_READINESS_20260906.md
- TEXT/FIRST_CODEX_RUN_B01_20260906.md
- autoritative Fehlerquelle via FEHLERREGISTER

Plan A bleibt vollständig erhalten, solange die Entscheidung A/B offen ist.

## PLAN B – SLIMLINE SHADOW

Zweck:
technisch vereinfachte Alternative ohne Qualitäts-, Inhalts-, Design- oder Sicherheitsverlust entwickeln und separat prüfen.

Kandidat:
- Draft-PR #143
- Branch: `plan-b/text-slimline-shadow-v1-20260907`
- Basis-Snapshot: `c8a96e7a2f598de69134d90b143257c3559bc98a`

Lagerort innerhalb Plan-B-Branch:
`experiments/plan_b_text_slimline/`

Plan B darf während der Vergleichsphase:
- keinen produktiven Workflow referenzieren;
- keinen Plan-A-Controller importieren;
- keine Plan-A-Datei verändern;
- nicht nach main gemergt werden.

## GEMEINSAME VERGLEICHSBASIS

Nur die Testdaten dürfen identisch sein:
- derselbe Generation-1-7er-Batch;
- dieselben Fach-/Qualitäts-/Designregeln;
- dieselben PPM-/PSERC-/PSTE-Vorgaben;
- dieselben Sicherheitsgrenzen;
- dieselbe Publish-Sperre.

Die technische Implementierung und alle Testergebnisse bleiben getrennt.

## TESTERGEBNISSE

Plan A:
eigene Protokolle / eigene Runs / eigene Fehlerkette.

Plan B:
eigene Protokolle / eigene Runs / eigene Fehlerkette.

Ein Fehler oder Fix aus A wird niemals automatisch auf B übertragen.
Ein Fehler oder Fix aus B wird niemals automatisch auf A übertragen.

Erst nach unabhängiger Reproduktion darf geprüft werden, ob derselbe Befund beide Linien betrifft.

## UMSCHALTEN

"Auf Plan A umschalten" bedeutet:
- ausschließlich Plan-A-Branch/-PR/-Runbook verwenden;
- Plan-B-Dateien ignorieren.

"Auf Plan B umschalten" bedeutet:
- ausschließlich Plan-B-Branch/-PR/-Runbook verwenden;
- Plan-A-Änderungen seit dem gemeinsamen Basis-Snapshot nicht übernehmen, außer nach eigener separater Prüfung.

Umschalten ist eine Auswahl des Teststands, kein technisches Mischen.

## ENTSCHEIDUNGSKRITERIEN

Plan B kann Plan A nur ersetzen, wenn mindestens nachgewiesen ist:
1. Qualität identisch;
2. Inhalt/Fachlogik identisch;
3. Design identisch;
4. Sicherheitsgrad identisch;
5. Chat-Zwangsjacke mindestens gleich streng;
6. genau eine Tür;
7. Wächter bleibt fachblind/dumm;
8. vollständige Automatisierung mindestens gleich hoch;
9. gleicher 7er-Batch erreicht mindestens denselben Endzustand;
10. technische Komplexität/Fehlerfläche ist messbar kleiner.

Bis dahin:
**BEIDE PLÄNE BLEIBEN VOLLSTÄNDIG ERHALTEN.**
