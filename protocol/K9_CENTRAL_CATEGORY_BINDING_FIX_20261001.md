# K9 – Zentrale Kategorienanbindung – 2026-10-01

Status: IMPLEMENTED_FOR_TEST

## Ursache
K9 verwendete `contracts/K9_PORTAL_BINDINGS.json` als manuell gepflegte Teilmenge.
Dadurch wurde `heutaschen-beratung` im aktuellen 3er-Lauf geblockt, obwohl die Kategorie zentral existiert.

## Autorität
Einzige Kategorien-Inhaltsquelle:
`CATEGORY_INTEGRATION_HOBBYRAUM/PFERDEPORTAL_KATEGORIEN/KATEGORIEN.tsv`
auf `category-integration-template-source-readonly-20260923`.

Die Portalstruktur wird ausschließlich zur Ableitung der drei Navigationslinks genutzt:
`release/affiliate-zentrale/current/affiliate-portal-router/assets/portal-structure-v279.json`.

## Änderung
- K9 liest die zentrale Kategorienquelle read-only.
- Die manuelle K9-Kategorienliste wird entfernt.
- Vor dem ersten Research-Job werden alle noch offenen Research-Kategorien des Batches geprüft.
- Unbekannte zentrale Kategorie, fehlender Portalbezug, Namensdrift oder Artikeltyp-Drift blockieren vor Produktionsbeginn.
- Keine Kategorie wird geschrieben, umbenannt, verschoben oder ergänzt.
- LT 6.8, PPM 6.7.9, PSERC, ENDSTEMPEL und WordPress-Verify bleiben unverändert.
- publish_allowed bleibt false.

## Aktueller 3er-Batch
Erwartete zentrale Kategorien:
- heutaschen-beratung
- longierpeitschen-faq
- heunetze-faq

## Tests
Positiv:
- alle drei aktuellen Kategorien werden aus zentraler Quelle aufgelöst.
- kompletter Batch-Preflight läuft vor dem ersten Research-Job.

Negativ:
- unbekannte Kategorie blockiert.
- zentral bekannte Kategorie ohne Portalbezug blockiert.
- Artikeltyp-Drift blockiert.
