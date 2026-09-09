# PRODUKTVERGLEICH – AUTORITATIVE FEHLERQUELLE

STAND: 2026-09-09
ROLLE: einzige detaillierte Fehlerquelle für den aktuellen PRODUKTVERGLEICH-V1-Arbeitsweg.

## PV-ERR-001 – falsche WordPress-Kategoriehierarchie

STATUS: CLOSED

Befund:
Der frühe Prototyp erwartete für `Vergleich Regendecken` eine echte Taxonomie-Unterkategorie. Die reale Pferde-Atelier-Kategorie ist technisch flach.

Fix:
Ab 0.2.1 werden ID/Name/Slug/Parent exakt geprüft.

## PV-ERR-002 – Erst-Draft sprang an Materialisierungsstufe vorbei

STATUS: CLOSED

Befund:
Der frühe Erst-Draft-Test rief die Link-Finalisierung vor der WordPress-DRAFT-Materialisierung auf.

Fix:
`Import -> WordPress-DRAFT -> Link-Finalisierung -> Grafik-Finalisierung -> Endhash`.

## PV-ERR-003 – Hauptmenü-Test war falscher Positivtest

STATUS: TECHNISCHER FIX BESTÄTIGT / AKTUELLER 0.8.1-LIVE-RETEST NOCH OFFEN

Befund:
Der alte Test rief Menüregistrierung künstlich direkt auf statt den echten WordPress-Admin-Lifecycle zu prüfen.

Technischer Fix wurde lokal im echten WP-Admin-Lifecycle bewiesen. Der aktuelle 0.8.1-Kandidat erhält trotzdem erst nach dem neuen Nutzer-Live-Retest einen LIVE-PASS.

## PV-LIVE-001 – falsches PASS bei null geeigneten Vergleichen

STATUS: CLOSED / REGRESSION AKTIV

Realer 0.7.0-Befund:
8 Kandidaten -> 16 Provider-Aufrufe -> 0 SEO-PASS -> 8 blockiert -> 0 Dossiers, aber die Oberfläche meldete grün PASS.

Fix ab 0.7.1:
0 gültige Dossiers + 0 SEO-PASS -> `NO_ELIGIBLE_COMPARISONS`, niemals Success-Notice.

0.8.1:
entsprechende Regression weiterhin PASS.

## PV-ERR-004 – PASS möglich ohne realen Dossier-Receipt im Abschluss-Audit

STATUS: CLOSED IM 0.8.1-KANDIDAT / WORDPRESS-LIVE-RETEST OFFEN

Harter lokaler Negativbefund gegen 0.8.0:
Die Materialisierungsstufe konnte Erfolg + Dossier melden, während der unabhängige finale Registry-Audit tatsächlich null passende Dossier-Receipts enthielt. 0.8.0 konnte trotzdem `PASS` zurückgeben.

Das verletzt fail-closed.

KISS-Fix 0.8.1:
- `dossier_count` muss exakt zur gemeldeten Dossierliste passen;
- jede gemeldete `comparison_id` muss im unabhängigen finalen Audit vorhanden sein;
- sonst BLOCK.

Exakte Blocks:
- `UPC_DOSSIER_MATERIALIZATION_COUNT_MISMATCH`;
- `UPC_DOSSIER_FINAL_AUDIT_RECEIPT_MISSING`.

Beleg:
- kompletter Kandidat 19/19 PASS;
- finale Fresh-ZIP erneut 19/19 PASS;
- PHP-Lint 39/39;
- unabhängige Gegenprobe: Guard entfernt -> Regression ROT.

## Regel

Neue Produktvergleichsfehler werden ausschließlich hier ergänzt.
Das zentrale `FEHLERREGISTER.md` bleibt reiner Wegweiser.
