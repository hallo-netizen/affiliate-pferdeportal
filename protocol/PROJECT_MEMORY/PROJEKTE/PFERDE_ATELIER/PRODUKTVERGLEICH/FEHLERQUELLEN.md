# PRODUKTVERGLEICH – AUTORITATIVE FEHLERQUELLE

STAND: 2026-09-09
ROLLE: einzige detaillierte Fehlerquelle für den aktuellen PRODUKTVERGLEICH-V1-Arbeitsweg.

## PV-ERR-001 – falsche WordPress-Kategoriehierarchie
STATUS: CLOSED

## PV-ERR-002 – Erst-Draft sprang an Materialisierungsstufe vorbei
STATUS: CLOSED

## PV-ERR-003 – Hauptmenü-Test war falscher Positivtest
STATUS: TECHNISCH CLOSED / LIVE-GESAMTWEG WEITER IN PRÜFUNG

## PV-LIVE-001 – falsches PASS bei null geeigneten Vergleichen
STATUS: CLOSED / LIVE 0.8.1 UND 0.8.2 BESTÄTIGT / REGRESSION AKTIV

Realer Befund:
0.7.0 meldete bei 0 SEO-PASS / 0 Dossiers fälschlich grün PASS.

Fix:
`NO_ELIGIBLE_COMPARISONS` statt Success.

WordPress 0.8.1:
8 Kandidaten -> 9 Provider-Aufrufe -> $0.1090 -> 0 SEO-PASS -> 8 blockiert -> 0 Dossiers -> `NO_ELIGIBLE_COMPARISONS`.

WordPress 0.8.2 Wiederholung:
8 Kandidaten -> 0 Provider-Aufrufe -> $0.0000 -> 0 SEO-PASS -> 8 blockiert -> 0 Dossiers -> `NO_ELIGIBLE_COMPARISONS`.

## PV-ERR-004 – PASS ohne realen Dossier-Receipt
STATUS: CLOSED IM 0.8.1+ / REGRESSION AKTIV

Fix:
- Dossier-Rückgabemenge muss exakt stimmen;
- jedes gemeldete Dossier muss im unabhängigen finalen Audit vorhanden sein.

Blocks:
- `UPC_DOSSIER_MATERIALIZATION_COUNT_MISMATCH`
- `UPC_DOSSIER_FINAL_AUDIT_RECEIPT_MISSING`

## PV-COST-082-001 – bezahlte Produkt-/Paar-Zwischenergebnisse nicht dauerhaft genug gebunden

STATUS: CLOSED / LOKAL + WORDPRESS-LIVE-WIEDERHOLUNG PASS

Befund gegen 0.8.1:
Der fertige Kandidatenbefund wurde 90 Tage gespeichert. Einzelne Produkt-/Paar-Providerantworten waren jedoch nur über den nativen PSTE-Cache abgesichert. Der autoritative PSTE-0.56.25-Code hat dort standardmäßig 86400 Sekunden / 24 Stunden.

KISS-Fix 0.8.2:
- persistenter UPC-Probe-Store;
- Produkt + Paar;
- Teilstände nach jedem erfolgreichen Provider-Endpunkt;
- positiv + negativ;
- 90 Tage;
- exakte Hash-/Kontextbindung;
- Wiederverwendung vor PSTE-/Providerzugriff;
- Kostenprognose berücksichtigt vorhandene persistente Evidenz.

Fail-closed:
- manipuliert -> `UPC_PSTE_PROBE_CACHE_INTEGRITY_FAILED`;
- Speichern nach bezahlter Antwort fehlgeschlagen -> `UPC_PSTE_PROBE_PERSISTENCE_FAILED`;
- Ablauf/Kontextdrift -> frische Recherche erforderlich.

Lokaler Beleg:
- finale Fresh-ZIP 20/20 PASS;
- PHP-Lint 40/40 PASS;
- gleicher kompletter Befund erneut -> 0 Provideraufrufe;
- gleiches Produkt in neuem Paar -> Produkt nicht erneut abgefragt;
- Abbruch nach erstem bezahlten Endpunkt -> Retry kauft nur den fehlenden Endpunkt;
- 3 unabhängige Mutationen werden von der Regression verworfen.

WordPress-Live-Beleg:
- vor Wiederholung maximale neue Providerkosten $0.0000;
- erneuter identischer Workflow -> 0 Provider-Aufrufe;
- Kosten $0.0000;
- bestehende 8 terminalen SEO-Befunde weiter vorhanden;
- korrekt `NO_ELIGIBLE_COMPARISONS`.

## Regel

Neue Produktvergleichsfehler werden ausschließlich hier ergänzt.
Das zentrale Fehlerregister bleibt Wegweiser.
