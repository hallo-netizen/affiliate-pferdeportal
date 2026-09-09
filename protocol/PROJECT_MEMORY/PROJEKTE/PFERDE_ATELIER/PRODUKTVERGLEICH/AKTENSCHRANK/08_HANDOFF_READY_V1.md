# PRODUKTVERGLEICH – ÜBERGABEBEREIT V1

Stand: 2026-09-09
Status: FACHLICH BEREIT / TECHNISCHE ANBINDUNG WARTET AUF SEO-TEXT-ACM-FREIGABE

## Produktvergleich-Stand

Kandidat:
`universal-product-comparison-0.8.3-prototype.zip`

SHA-256:
`4c08ca1df348ab49849ddde8f85980db450694c58010cd0c431575bc6a3cd11e`

Fachblock:
PASS.

WordPress-Live-Wiederholung:
PASS für unveränderten realen Bestand:
- 0 Provider;
- $0.0000;
- 8 BLOCKED;
- 0 Dossiers;
- `NO_ELIGIBLE_COMPARISONS`.

Kein offener Produktvergleichs-Reparaturfehler.

## Für das Nachbarbüro verbindlich zu lesen

1. `ZIELVERTRAG_V2.md`
2. `AKTENSCHRANK/01_UEBERGABEKONZEPT_PRODUKTVERGLEICH_TEXT_ACM_V1.md`
3. `AKTENSCHRANK/05_FACH_DOSSIER_ARTIKELTYP_VERTRAG_V1.md`
4. `AKTENSCHRANK/06_V083_HARD_LOCAL_RELEASE_RECEIPT.md`
5. `AKTENSCHRANK/07_V083_WORDPRESS_LIVE_REPEAT_RECEIPT.md`
6. `CURRENT_STATE.md`

## Gebundener Fachinput

Aktiver Artikeltyp-Scope:
`PRODUCT_COMPARISON V1`

Bedeutung:
- exakt 2 Produkte;
- A gegen B;
- mindestens zwei Hersteller;
- gleiche Produktgruppe/Nutzungsebene.

Dossier:
`UPC_BOUND_COMPARISON_DOSSIER_V2`

Es liefert strukturiert:
- Produktidentitäten;
- Fakten/Quellenstatus;
- SEO-Evidenz;
- Zielkeyword;
- Readiness/Kannibalisierung;
- Decision-Policy-Hash;
- erlaubte Aussagearten;
- Verbote;
- feste Need-Codes;
- Abschluss-Audit.

Es liefert **keine Prosa**.

## Harte Schnittstellengrenze

Spätere Produktions-Eingangswahrheit bleibt ausschließlich:
`FACHWORKFLOW_HANDOFF_REQUEST.json`

Verboten:
- neues Handoff;
- 17. Top-Level-Feld;
- neues Jobmanifest;
- neuer Controller;
- neue Textmaschine;
- Produktvergleich-Writer als zweite Produktionsstraße.

Die exakte Abbildung des Dossier V2 in vorhandene `fact_pack` / `production_plan_item`-Kontexte ist erst im SEO/TEXT-Büro gegen das reale Schema zu bestimmen und positiv/negativ zu testen.

## Aktueller Nachbarstatus

Read-only geprüft auf:
`alternative/seo-text-central-machine-20260908`

Autoritative ACM-Statusakte:
`control/seo-text-buero/alternative-central-machine/AKTENSCHRANK/58_ACM_ROUTE_STATUS_20260909.md`

Dort:
- ACM-KERN PASS;
- PRODUKTIONSADOPTION BLOCKED;
- erster offener Punkt: direkte Prüferherkunft für `research_fact_pack`;
- keine technische Änderung erlaubt, solange kein vorhandener autoritativer Prüferpfad belegt ist.

Neuester Branch-Head:
`fd1ae90a60e91f75759ab88da0386835eb377901`

Dieser beweist zusätzlich den signierten WordPress-Seam batch-generic, ersetzt aber die autoritative BLOCKED-Statusakte nicht.

## Übergaberegel

Solange ACM/SEO-TEXT BLOCKED:
**keine technische Produktvergleichs-Anbindung beginnen.**

Sobald dort die Produktionsadoption hart freigegeben ist:

Nachbarchat bekommt nur diesen Auftrag:

`Campus -> Pferde Atelier -> SEO/TEXT/ACM. Lies read-only den Produktvergleich-Übergabestand auf branch hobbyroom/productvergleich-workflow-v070-20260908, insbesondere AKTENSCHRANK/08_HANDOFF_READY_V1.md, 01_UEBERGABEKONZEPT..., 05_FACH_DOSSIER... und ZIELVERTRAG_V2.md. Produktvergleich-Branch nicht verändern. Prüfe gegen deinen aktuellen autoritativen SEO/TEXT-/ACM-Stand, wie UPC_BOUND_COMPARISON_DOSSIER_V2 ohne neues Handoff und ohne neue Top-Level-Felder in die bestehenden gebundenen Produktionskontexte passt. Ergebnis ACCEPTED oder BLOCKED in deinem eigenen Aktenschrank dokumentieren.`

## Bedingungsabhängiger Rest

Positiver WordPress-Dossier-V2-Livefall:
wird beim ersten realen SEO-PASS-A-vs-B-Paar nachgeholt.

Kein künstliches SEO-PASS erzeugen.
Kein Providerkauf nur für einen Test.
