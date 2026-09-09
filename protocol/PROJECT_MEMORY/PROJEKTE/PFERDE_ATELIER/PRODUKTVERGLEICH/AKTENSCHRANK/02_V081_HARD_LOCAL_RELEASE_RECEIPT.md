# PRODUKTVERGLEICH 0.8.1 – HARD LOCAL RELEASE RECEIPT

Stand: 2026-09-09
Status: LOCAL + FINAL-FRESH-ZIP HARD PASS / WORDPRESS-LIVE-RETEST OFFEN

Artefakt:
`universal-product-comparison-0.8.1-prototype.zip`

SHA-256:
`3ae3fe30365f767ea1e225554c7e986d70c6225d79884eeb796beadf1f6cb902`

## Anlass

0.8.0 wurde nicht abgenommen.

In der zusätzlichen Gesamtworkflow-Negativprüfung wurde PV-ERR-004 gefunden:
Materialisierung konnte Erfolg melden, obwohl im unabhängigen Abschluss-Audit kein zugehöriger Dossier-Receipt vorhanden war. 0.8.0 konnte dadurch falsch PASS melden.

## KISS-Fix

Nur `src/class-upc-workflow.php` fachlich geändert:
- gemeldete Dossieranzahl muss zur Liste passen;
- jede gemeldete comparison_id muss im unabhängigen finalen Audit vorkommen;
- sonst fail-closed.

Zusätzlich nur Testhärtung:
- echter dormant Draft-Hook wird explizit negativ geprüft;
- fehlender finaler Dossier-Receipt ist feste Regression.

## Harte lokale Prüfung

Exakte Abhängigkeiten:
- Universal Product Knowledge 0.5.0:
  `80218ec721631353d62a7e3058e76d9c4a4829802c4d5c6bd6f1f2014b6879e3`
- PSTE 0.56.25:
  `8122e3fa2273fe4d8e53476f557ed0ddd99a197e8b1c40302f35db245ebb0f95`

Ergebnis:
- Arbeitskandidat komplette Suite: 19/19 PASS;
- Arbeitskandidat PHP-Lint: 39/39 PASS;
- erste Fresh-ZIP komplette Suite: 19/19 PASS;
- erste Fresh-ZIP PHP-Lint: 39/39 PASS;
- finale Fresh-ZIP komplette Suite: 19/19 PASS;
- finale Fresh-ZIP PHP-Lint: 39/39 PASS;
- Source ↔ finale ZIP: 50/50 identisch;
- Report-Hashbindung: 49/49 PASS;
- ZIP-Wurzel exakt `universal-product-comparison/`;
- keine Dubletten;
- keine gefährlichen Pfade;
- reale PSTE-Themenmap False-Pair-Guard PASS;
- 0.7.1 Kostencheck gegen autoritative PSTE-Rate PASS;
- 0.8 Gesamtplan-Kostencheck PASS;
- statischer Gesamtworkflow-Gate mit echten UPK-/PSTE-Abhängigkeiten PASS;
- bestehende Mutation Guards PASS.

Unabhängige Gegenbeweise:
- alten echten Draft-Hook wieder aktivieren -> Test ROT;
- neuen Dossier-Abschluss-Audit-Guard entfernen -> Test ROT.

## Gesamtworkflow-Prüfung

PASS:
`Produktwissen -> Vergleichbarkeit -> bidirektionale SEO-Nachfrage -> aktuelle Readiness/Kannibalisierung -> Dossier -> unabhängiger Abschluss-Audit`

Fail-closed geprüft:
- Same Brand;
- 0g/50g-/Profil-Drift;
- unbekannte Produktidentität;
- generische Anfrage erfindet kein Produkt;
- nur ein Produkt mit Nachfrage;
- null Nachfrage;
- Provider PARTIAL;
- veralteter Providervertrag/SEO-Signal;
- Dossier-/Audit-Drift;
- falscher Success-Status.

Grenzen:
- Dossier-Export read-only;
- Affiliate nur Exact-Match-Leseschicht;
- Writer/Draft-Adminweg dormant;
- aktiver Workflow ohne WordPress-Post-/Publish-Schreibweg;
- kein Auto-Publish.

## Grenze

Dies ist die lokale Freigabe für den nächsten WordPress-Live-Retest.
Noch kein WordPress-LIVE-PASS.
