# HOBBYRAUSCH – PLUGINS – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-01
STATUS: HD-001 V1.9.4 ROOT-CAUSE FIX POS+NEG HARD PASS / LETZTER TESTLAUF VOLLSTÄNDIG ZURÜCKGEROLLT / LIVE-RETEST OFFEN · HD-002 V0.1.1 LIVE-MIGRATION PASS

## HD-001 – Kategorie-Workflow

Aktuell:
`Affiliate-Portal Kategorie-Workflow V1.9.4`

Live-Root-Cause:
- V1.9.3 Diagnose identifizierte `hdc-21557545f2e7cc51`;
- einziges abweichendes Feld: `name`;
- Knoten: `Techniken & Praxis`;
- WordPress Core speichert den Taxonomie-Namen als `Techniken &amp; Praxis`;
- alter Readback verglich roh statt semantisch normalisiert.

Altcode lokal wortgleich reproduziert:
`DEPLOY_READBACK_MISMATCH ... Felder: name ... Rollback: PASS`

V1.9.4:
- normalisiert nur WordPress-Core-Termname-Escaping beim Lesen;
- echte Namensabweichung bleibt BLOCKED.

Beweise:
- echter 7-CREATE-Buchbinden-Pfad PASS;
- relevante Negativfälle BLOCKED + Rollback PASS;
- Source 251/251 PASS;
- Fresh Installer 251/251 PASS;
- Source PHP 25/25;
- Installer PHP 17/17;
- Runtime-Parität 22/22.

Installer SHA:
`85990b87f0ef35530b616df7716547cb20974d1c77ca21aa7b3e0edec723f249`

## Live-Zustand

Der V1.9.3-Diagnose-Testlauf wurde vollständig zurückgerollt.
Es gibt daher aktuell keinen aktiven Dry-Run.

## HD-002 – Themenengine

V0.1.1 Live-Migration COMPLETE.

Weiterhin kein `Gesamtbestand erfassen`, solange HD-001 nicht live erfolgreich deployt und readback-verifiziert ist.

## NEXT ACTION

HD-001 V1.9.4 installieren → denselben Buchbinden READ_ONLY_PREVIEW erneut übernehmen → Finalfreigabe → neue WordPress-Vorschau → Apply.

Kein neuer Research-Lauf.
