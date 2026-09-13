# UNIVERSAL GLOSSAR ENGINE – HOBBYRAUM

STAND: 2026-09-13
STATUS: 0.2.8 LIVE FAIL / 0.2.9 TECHNISCH PASS / PFERDE-LIVE-READBACK OFFEN

## 1-KLICK-ÜBERSICHT

**WAS IST DAS?**  
Der isolierte Arbeitsraum für den allgemeinen Glossar-Core.

**DU DARFST …**  
den neutralen Core und seine gebundenen Positiv-/Negativtests pflegen sowie exakt 0.2.9 für den Pferde-Live-Readback verwenden.

**DU DARFST NICHT …**  
Pferde-Fachlogik in den neutralen Core schreiben, `main` verändern, 0.2.6/0.2.7/0.2.8 erneut ausgeben, unterschiedliche Paketbytes unter derselben Version erzeugen oder die verworfene Kategorie-Acceptance wiederverwenden.

**ALS NÄCHSTES …**  
exakt 0.2.9 auf Pferde Atelier installieren und real zurücklesen.

## GEBUNDENER TECHNISCHER KANDIDAT

Version: `0.2.9`
Rewrite-Schema: `7`
Branch: `hobbyroom/glossar-livefail-red-green-20260913`
Head: `f2fa6f0c248acfa6978b5faec5daf42a40d0ba3b`
Run: `34757795593`

PASS:
- Build `103725094481`
- Fresh/Regression/Null-Rewrite `103725094537`
- 0.2.8 → 0.2.9/erneuter Null-Rewrite `103725094620`
- Real Design 1.50.469/Browser/Null-Rewrite `103725094378`
- gated package `103725295224`

ZIP SHA-256:
`864befa0d159577e418906e4de3052ad0127b7dbcdad80775ba7e8f734ed1173`

Actions-Artefakt-ID:
`10317444708`

## WARUM 0.2.9 NÖTIG WAR

Realer 0.2.8-Readback:
- Hero nicht responsive;
- Kategorien nicht wie Glossar-Startseite gestaltet;
- Einzelartikel-Links laufen ins Leere.

Zusätzlich war die 0.2.8-Kategorie-Acceptance selbst falsch: sie verlangte das Fehlen von Hero/Tools statt des vollständigen Glossar-Rahmens.

## NEUE HARTE SCHRANKEN

- echtes Bild selbst muss bei 1200/900/720/500 proportional skalieren;
- Kategorie muss Hero + Suche/A–Z + Icon-Navigation + eigenen Kategorieinhalt besitzen;
- Browser muss einen real gerenderten Begriff-Link tatsächlich anklicken;
- Kategorie-/Begriff-Routing muss selbst nach Löschung **aller** gespeicherten Glossar-Rewrite-Regeln bei bereits aktuellem Schema weiter funktionieren;
- WordPress-Draft-Preview muss weiterhin funktionieren;
- unbekannter Begriff und öffentlicher Draft bleiben 404;
- alte Regressionen bleiben grün.

## EXAKTE ÜBERGABE

Nur:
`universal-glossary-engine-0.2.9.zip`

SHA-256:
`864befa0d159577e418906e4de3052ad0127b7dbcdad80775ba7e8f734ed1173`

Materielle Änderung danach → mindestens Version 0.2.10.

## HARTE GRENZE

0.2.9 ist technisch PASS, aber **noch kein Pferde-LIVE-PASS**. Nur der reale Nutzer-Readback kann die aktuellen Live-Fehler schließen.
