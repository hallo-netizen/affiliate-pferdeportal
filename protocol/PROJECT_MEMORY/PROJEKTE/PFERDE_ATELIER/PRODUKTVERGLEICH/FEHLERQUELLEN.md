# PRODUKTVERGLEICH – AUTORITATIVE FEHLERQUELLE

STAND: 2026-09-11
ROLLE: einzige detaillierte Fehlerquelle für den aktuellen PRODUKTVERGLEICH-Arbeitsweg.

## PV-ERR-001 – falsche WordPress-Kategoriehierarchie
STATUS: CLOSED

## PV-ERR-002 – historischer eigener Draftweg
STATUS: CLOSED / NICHT MEHR ZIELARCHITEKTUR

## PV-ERR-003 – falscher Hauptmenü-Positivtest
STATUS: CLOSED / ECHTER WP-LIFECYCLE ALS PFLICHT ERHALTEN

## PV-LIVE-001 – falsches PASS bei null geeigneten Vergleichen
STATUS: CLOSED / LIVE 0.8.1–0.8.4 BESTÄTIGT / REGRESSION AKTIV

## PV-ERR-004 – PASS ohne realen Dossier-Receipt
STATUS: CLOSED IM 0.8.1+ / REGRESSION AKTIV

## PV-COST-082-001 – bezahlte Produkt-/Paar-Zwischenergebnisse nicht dauerhaft genug gebunden
STATUS: CLOSED / LOKAL + WORDPRESS-LIVE 0.8.2–0.8.4 PASS

## PV-FACH-083-001 – Fachinterpretation nicht vollständig im Dossier gebunden
STATUS: CLOSED / 0.8.3 LOCAL HARD + WORDPRESS-LIVE-REGRESSION PASS

## PV-SCALE-084-001 – Proofgruppe statt vollständiger Vergleichsgruppen-Abdeckung
STATUS: INFRASTRUKTUR CLOSED / 175ER RESEARCH-/FACHDISPOSITION CLOSED / V1-READINESS-DATENBINDUNG OFFEN

Geschlossen:
- 175/175 Portalgruppen in Registry;
- jede Gruppe sichtbar;
- keine stille Top-N-/Pair-Cap;
- Research-Evidence bleibt getrennt von Product Knowledge;
- finale V1-Disposition: 150 `PRODUCT_EVIDENCE_PRESENT`, 25 `PRODUCT_COMPARISON_V1_NOT_APPLICABLE`, 0 ungeklärt;
- breite Markt-/Identitäts-/Subtyp-/Registry-/Artikeltyp-Klärung des ersten 175er Laufs abgeschlossen.

Weiter offen:
- exakte UPC-0.8.6-Fresh-ZIP besitzt nur 7 maschinenfeste Vergleichsprofile/Decision-Policies;
- 143 der 150 grundsätzlich V1-fähigen Gruppen fehlen dort noch maschinenfest;
- für 7 weitere Gruppen liegen inzwischen source-bound Profilspezifikationen in Akten 62–64 vor, aber noch **nicht** materialisiert;
- weitere Profil-/Faktenmatrizen source-bound vorbereiten, danach gebündelt materialisieren und erneut hart testen;
- Product Knowledge und daraus entstehende fachlich zulässige Paarabdeckung bleiben je Gruppe fail-closed nachzuweisen.

Dauerbelege:
- `AKTENSCHRANK/60_FINAL_COVERAGE_DISPOSITION_175_V1_20260911.md`;
- `AKTENSCHRANK/61_READINESS_BASELINE_V1_150_20260911.md`;
- `AKTENSCHRANK/62_PROFILE_FACT_MATRIX_HIGH_NECK_DECKEN_V1_20260911.md`;
- `AKTENSCHRANK/63_PROFILE_FACT_MATRIX_DECKENZUBEHOER_V1_20260911.md`;
- `AKTENSCHRANK/64_PROFILE_FACT_MATRIX_HALFTER_V1_20260911.md`.

## PV-FAMILY-085-001 – Readiness zählte Herstellerbezeichnungen statt Herstellerfamilien
STATUS: CLOSED IM 0.8.5 / LOKAL HART PASS

KISS-Fix:
Eine Herstellerfamilien-Wahrheit für Research-Zählung, Inventar-Readiness, Paaruniversum und Planner.

Harter Beleg:
- Aesculap/Kerbl + Kerbl => 1 Familie;
- synthetischer echter zweiter Hersteller => erwartete Cross-Family-Paare;
- drei Mutationen korrekt ROT;
- finale 0.8.5-Regression 35/35 PASS.

## PV-FACH-085-002 – Fachprofile für vorhandene Mehrhersteller-Recherche
STATUS: PROFILE/POLICY LOCAL PASS / ALT-BASIS LIVE MATERIALISIERT / REALE POST-BATCH-PAARZAHL NICHT SEPARAT ABGELESEN / MARKTVOLLSTÄNDIGKEIT NICHT BEHAUPTET

Maschinenfeste 0.8.6-Profile bestehen aktuell für:
- Regendecken;
- Winterdecken;
- Übergangsdecken;
- Stalldecken;
- Unterdecken;
- Schermaschinen;
- Steigbügel.

Die früher lokal berechneten 130 Cross-Family-Paare waren Katalogpotential nach Testmaterialisierung, keine vorab bewiesenen Live-Paarzahlen.

## PV-TEST-085-003 – Recherchekandidaten im Lokaltest als materialisiertes Inventar behandelt
STATUS: CLOSED / TESTGRENZE KORRIGIERT / UPK 0.5.1 LOCAL HARD + WORDPRESS-LIVE-BATCH 17/17 ABGESCHLOSSEN

Der 0.8.5-Live-Gegenbeleg zeigte korrekt:
- Research-Kandidaten werden nicht automatisch Product Knowledge;
- fehlendes Inventar bleibt `PRODUCT_INVENTORY_MISSING`;
- kein Paar/SEO-/Providerlauf wird erfunden;
- Kosten bleiben $0.0000.

UPK 0.5.1 nutzt ausschließlich den kanonischen `UPK_Research::run_product_group()`-Weg.

## PV-LIFECYCLE-086-001 – abgekündigte/unklare Produkte blieben im aktuellen Paaruniversum
STATUS: CLOSED IM 0.8.6 LOCAL HARD + FRESH-ZIP / WORDPRESS-LIVE 0.8.6 OFFEN

Realer Gegenbeweis gegen unveränderte 0.8.5:
- zwei `ACTIVE`-Produkte;
- ein vergleichbares `DISCONTINUED`-Produkt;
- Ergebnis ROT: 3 statt 1 gültigem Paar; Herstellerzählung 3 statt 2.

KISS-Fix 0.8.6:
- `ACTIVE`: paarbar;
- `TEMPORARILY_UNAVAILABLE`: paarbar;
- `DISCONTINUED`: ausgeschlossen;
- `UNKNOWN`/fehlend: fail-closed ausgeschlossen;
- kanonische Deduplizierung vor Lifecycle-Gate.

Exakte Fresh-ZIP:
`universal-product-comparison-0.8.6-prototype.zip`

SHA-256:
`6ad160d18fb0973463c214de4356447923cbb728e222725e5407868e580c24f6`

Harter Beleg:
- Working Tree 38/38 Regression PASS;
- zwei Lifecycle-Mutationen korrekt ROT;
- PHP-Lint 51/51 PASS;
- Source↔Fresh-ZIP 74/74 exakt;
- Report-Hashes 73/73 exakt;
- Fresh-ZIP Regression 38/38 PASS;
- Fresh-ZIP PHP-Lint 51/51 PASS.

Dauerbeleg:
`AKTENSCHRANK/39_V086_LIFECYCLE_REEVALUATION_HARD_LOCAL_RECEIPT.md`.

## 0.8.6 READ-ONLY ARCHITEKTURAUDIT
STATUS: PASS / KEIN WEITERER CODEFIX AUSGELÖST

Belegt:
- Research-Evidence ohne materialisiertes Product Knowledge erzeugt 0 Paare;
- Nicht-V1-/Service-/Knowledge-/Checklisten-Keys bleiben fail-closed;
- SEO-PASS kann fachliches BLOCKED nicht überschreiben;
- bestehendes Dossier verliert READY, wenn ein gebundenes Produkt im aktuellen Product Knowledge entfällt/abgekündigt wird;
- 1000-Pair-No-Cap-Regel bleibt PASS.

Dauerbeleg:
`AKTENSCHRANK/41_V086_READ_ONLY_ARCHITECTURE_AUDIT_RECEIPT.md`.

## AKTUELLER ERSTER OFFENER ARBEITSBLOCK

Kein neuer technischer Pluginfehler ist nach `PV-LIFECYCLE-086-001` belegt.

Aktive Arbeit ist der V2-Readiness-Daten-/Fachblock:
- source-bound Profil-/Faktenmatrizen in Registry-Reihenfolge;
- Akten 62–64 sind erstellt, aber nicht materialisiert;
- nächster zusammenhängender Profilblock: `pferdebuersten`, `striegel`, `kardaetschen`;
- erst ein sinnvoll gebündelter Profil-/Faktenstand darf technisch materialisiert werden;
- danach wieder vollständiger Positiv-/Negativ-/Mutation-/Fresh-ZIP-Weg.

WordPress-Live für UPC 0.8.6 bleibt offen und wird nicht als PASS behauptet.

Kein SEO vor fachlich zulässigem Kandidatenuniversum.
Kein Writer/Draft/Publish aus diesem Büro.
Kein Merge.
Kein Publish.

## Regel

Neue Produktvergleichsfehler werden ausschließlich hier ergänzt.
Das zentrale Fehlerregister bleibt reiner Wegweiser.
