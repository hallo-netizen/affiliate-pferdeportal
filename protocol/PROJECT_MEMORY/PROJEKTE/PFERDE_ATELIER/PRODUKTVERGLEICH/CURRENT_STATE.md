# PRODUKTVERGLEICH – CURRENT STATE

STAND: 2026-09-09
STATUS: AKTIV / 0.8.1 LOKAL HART PASS / WORDPRESS-LIVE-RETEST OFFEN

## AUTORITÄT

Diese Datei ist die einzige aktuelle Büro-Standzusammenfassung.

- aktuelle Arbeit: `HOBBYRAUM.md`
- Fehlerdetails: über `FEHLERREGISTER.md` → `FEHLERQUELLEN.md`
- Ziel: über `ZIELVERTRAEGE/REGISTER.md` → `ZIELVERTRAG_V1.md`
- Warum/Prüfbeleg: `AKTENSCHRANK/02_V081_HARD_LOCAL_RELEASE_RECEIPT.md`

## AKTUELLER KANDIDAT

`universal-product-comparison-0.8.1-prototype.zip`

SHA-256:
`3ae3fe30365f767ea1e225554c7e986d70c6225d79884eeb796beadf1f6cb902`

Aktuelle Stufe:
`Produktwissen -> Vergleichbarkeit -> bidirektionales SEO -> aktuelle Readiness/Kannibalisierung -> Dossier -> unabhängiger Abschluss-Audit`

Writer/Draft/Publish sind in dieser 0.8.1-Prüfstufe nicht aktiv.

## HARTER LOKALBELEG

Finale Fresh-ZIP:
- 19/19 Positiv-/Negativtests PASS;
- PHP-Lint 39/39 PASS;
- Source ↔ finale ZIP 50/50 byte-inhaltlich identisch;
- Report-Hashbindung 49/49 PASS;
- ZIP-Wurzel/Pfade/Dubletten PASS;
- echte Product-Knowledge-0.5.0-Abhängigkeit SHA PASS;
- echter PSTE-0.56.25-Installer SHA PASS;
- echte PSTE-Themenmap / False-Pair-Guard PASS;
- Kosten- und API-Vertrag gegen PSTE PASS;
- Mutationstests PASS.

Zusätzliche unabhängige Gegenbeweise:
- Reaktivierung des echten alten Draft-Hooks -> Test ROT;
- Entfernen des neuen Abschluss-Audit-Guards -> Test ROT.

## GEFUNDENER UND BEHOBENER FEHLER

0.8.0 konnte in einem künstlich erzwungenen Negativfall PASS melden, obwohl die Dossier-Materialisierung Erfolg behauptete, aber im unabhängigen Abschluss-Audit kein zugehöriger Dossier-Receipt vorhanden war.

0.8.1 blockiert jetzt fail-closed:
- Rückgabemenge != Dossierliste -> `UPC_DOSSIER_MATERIALIZATION_COUNT_MISMATCH`;
- gemeldetes Dossier fehlt im Abschluss-Audit -> `UPC_DOSSIER_FINAL_AUDIT_RECEIPT_MISSING`.

## GESAMTWORKFLOW-GRENZEN

Bestätigt:
- keine freie Produkterfindung;
- Same-Brand-/Profil-Drift fail-closed;
- nur A oder nur B mit Nachfrage reicht nicht;
- 0 Nachfrage reicht nicht;
- direkte A-vs-B-Nachfrage oder Nachfrage beider exakten Produkte ist gebunden zulässig;
- Provider PARTIAL bleibt PARTIAL;
- veraltete SEO-Signale werden nicht als aktuelle Wahrheit verwendet;
- Dossier muss im unabhängigen Abschluss-Audit real gebunden vorhanden sein;
- Dossier-Export bleibt read-only;
- Affiliate bleibt Exact-Match-Leseschicht;
- aktiver 0.8.1-Workflow besitzt keinen WordPress-Post-/Publish-Schreibweg;
- kein Auto-Publish.

## LIVE-STATUS

Noch kein WordPress-LIVE-PASS für 0.8.1.

NEXT ACTION ausschließlich `HOBBYRAUM.md`.
