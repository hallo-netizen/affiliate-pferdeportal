# GLOSSAR – HOBBYRAUM

STAND: 2026-09-13
STATUS: AKTIV / 0.2.10-rc11-native-single KUBIO-INTEGRATION + PAKET PASS / LIVE-READBACK OFFEN

## 1-KLICK-ÜBERSICHT

**WAS IST DAS?**  
Der einzige aktuelle Arbeitsraum des Büros GLOSSAR.

**DU DARFST …**  
nur den exakt aus Run `34766187415` paketierten und hashgebundenen `0.2.10-rc11-native-single`-Kandidaten für den realen Pferde-Readback verwenden.

**DU DARFST NICHT …**  
`main` oder das Pferde-Designplugin verändern, rc8/rc10 aus dem Chat verwenden, aus CI einen Pferde-LIVE-PASS ableiten, weitere Fehler gleichzeitig reparieren oder Altbestand löschen.

**ALS NÄCHSTES …**  
das exakte rc11-Paket installieren und **nur einen realen Glossar-Einzelartikel** aufrufen. Erst anhand dieses Live-Ergebnisses weiterarbeiten.

## ARBEITSORT

Branch:
`hobbyroom/glossar-livefail-red-green-20260913`

Aktueller getesteter Workflow-Head:
`b0b6fb786bcafe37819700df019ec31a92a2dc30`

Autoritative Fehlerquelle:
`FEHLERQUELLEN.md`

Autoritativer Stand:
`CURRENT_STATE.md`

## VERBRAUCHTE / ABGELÖSTE VERSIONEN

- 0.2.6 / 0.2.7 / 0.2.8: historisch bzw. LIVE FAIL; nicht verwenden.
- 0.2.9: früherer technischer Kandidat; nicht CURRENT.
- 0.2.10-rc1 bis rc6: Entwicklungs-/Diagnosestufen.
- 0.2.10-rc7: technisch grün, aber durch echten Nutzer-Readback beim Single-Rendering widerlegt.
- rc8 / rc10: Chat-Zwischenstände ohne ausreichenden echten Integrationsbeweis; nicht verwenden.

## AKTUELL: 0.2.10-rc11-native-single

Realer Befund, der repariert wird:
zweite `<!DOCTYPE html>/<html>/<head>`-Hülle innerhalb der bereits laufenden Kubio-Dokumenthülle.

Fixgrenze:
- UGE wählt für `uge_term` keine eigene klassische Full-Document-Single-PHP mehr;
- WordPress/Kubio rendert den Einzelbegriff nativ;
- Kategorie-/Taxonomie-Rendering bleibt unverändert.

Hardtest Run `34766187415` → SUCCESS.

Jobs:
- `103747455702` Kubio/WordPress Positiv + Negativ + Regression → PASS
- `103747644208` exaktes Paket → PASS

Harte Marker:
- `UGE0210RC11_KUBIO_PUBLISHED_SINGLE_VISIBLE_PASS`
- `UGE0210RC11_KUBIO_SINGLE_DOCUMENT_SHELL_EXACTLY_ONCE_PASS`
- `UGE0210RC11_DRAFT_AND_MISSING_NEGATIVE_PASS`
- `UGE0210RC11_UNRELATED_POST_REGRESSION_PASS`
- `UGE0210RC11_TAXONOMY_UNCHANGED_PASS`

## EXAKTES PAKET

`universal-glossary-engine-0.2.10-rc11-native-single.zip`

SHA-256:
`45c8f4d2a01883b6bb548c8db2db8bf9b19f5ddc80cb346b647d992fca7f748f`

Actions-Artefakt-ID:
`10320871739`

Outer artifact SHA-256:
`8ced9d219a6a38d81ab9be50fe146dc8a5acfa6a8e58a0154f5e84410d450434`

## NÄCHSTE HARTE REIHENFOLGE

1. exakt rc11 installieren;
2. einen realen Glossar-Einzelartikel anklicken;
3. wenn Inhalt sichtbar und keine leere Seite: Livebefund dokumentieren;
4. wenn weiter FAIL: exakt diesen Live-HTML-Befund aufnehmen und nur Single weiter reparieren;
5. keine Arbeit an Abständen/Hero/Kategorien, bis der Single-Fehler erledigt ist.

## NICHT ANFASSEN

- `main`;
- Pferde-Designplugin;
- bestehende Live-Inhalte;
- andere Glossar-Fehler während dieser Single-Reparatur.
