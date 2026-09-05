# TEXT – HOBBYRAUM

STAND: 2026-09-05
STATUS: AKTIV / NORMALER TEXT-ARBEITSCHAT – B01-REGRESSIONSPRÜFUNG

## 1-KLICK-ÜBERSICHT

**WAS IST DAS?**  
Der einzige aktuelle Arbeitsraum des Büros TEXT.

**HIER BIST DU RICHTIG, WENN …**  
du den aktuell gebundenen TEXT/SEO-Arbeitsbereich, Branch und nächsten Schritt sehen musst.

**DU DARFST …**  
den aktuellen Auftrag und alle autoritativen Quellen lesen und ausschließlich im gebundenen Hobbyraum-Branch prüfen/reparieren.

**DU DARFST NICHT …**  
main verändern, zu Paul wechseln, Paul-Dateien/-Branch benutzen, einen neuen Workflow/Runner/Gate/Executor bauen oder Fach-/SEO-/Textmaschinenregeln verändern.

**ALS NÄCHSTES …**  
Nur B01 weiter belegen: bestehende KISS-Korrektur und die beiden stale Regressionstests M15/M31 hart positiv/negativ prüfen. Danach erst bestehende M01–M33-Gesamtregression; ein echter 7/7-Lauf bleibt der Livebeweis.

## ARBEITSKONTROLLPUNKT – NUR DIE AKTUELLE ARBEIT

- **BÜROSTAND:** `CURRENT_STATE.md`
- **AKTUELLER AUFTRAG / NEXT ACTION:** ausschließlich diese `HOBBYRAUM.md`
- **CURRENT_BLOCKER:** nicht hier duplizieren → `protocol/PROJECT_MEMORY/FEHLERREGISTER.md` → autoritative Quelle
- **AKTIVER ZIELVERTRAG:** nicht hier duplizieren → `protocol/PROJECT_MEMORY/ZIELVERTRAEGE/REGISTER.md`
- **NICHT ANFASSEN / WARUM:** Ziel-/Originalquelle + `protocol/PROJECT_MEMORY/AENDERUNGSREGISTER.md`

## Aktuelle Arbeitsbindung

Aktiver Arbeiter:
**normaler TEXT-Arbeitschat**

**Paul ist für diesen Auftrag tabu und nicht gebunden.**

Gebundener Hobbyraum-Branch:
`hobbyroom/b01-semantic-category-seed`

Draft-PR:
`#140`

Aktueller Arbeits-Head:
`f2b47e9ecce643acfdffbd68ccff0805117613da`

main bleibt unverändert:
`c8a96e7a2f598de69134d90b143257c3559bc98a`

## Aktueller Prüfstand

- B01-KISS-Fix verändert nur den bestehenden `fachworkflow_proof_handoff.py`: keine vorgezogene WordPress-ID im echten Produktionsplan; interne Seed-ID nur für den isolierten lokalen PPM-Testzustand.
- M15-Test war stale: er verbot inzwischen ausdrücklich erforderliche Handoff-Request-Texte bzw. wertete `kein submit-request` falsch.
- M31-Test war stale: er erwartete überhaupt keinen `fachworkflow_handoff`, obwohl der aktuelle Sollweg einen gebundenen Handoff innerhalb derselben Current Action vorsieht und gerade keinen separaten Executor verlangt.
- Korrigierte M15/M31-Logik wurde auf dem Hobbyraum-Branch positiv/negativ geprüft.
- GitHub `hardlock` und `hardlock-base` auf Head `f2b47e9…`: PASS.
- Kein Live-7/7-PASS behauptet.

## Single Writer

- Dieser normale TEXT-Arbeitschat ist für den aktuellen B01-Hobbyraumauftrag der einzige aktive technische Schreiber.
- Paul wird nicht benutzt.
- main wird nicht verändert.
- Andere Büros/Arbeitsbereiche bleiben unangetastet.
- Erst nach belastbarer Prüfung werden offizieller Stand und nächste Aktion weitergeschrieben.
