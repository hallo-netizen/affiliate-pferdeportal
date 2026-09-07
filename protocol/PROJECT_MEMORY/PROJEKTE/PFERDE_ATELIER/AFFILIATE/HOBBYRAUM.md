# AFFILIATE – HOBBYRAUM

STAND: 2026-09-07
STATUS: AKTIV

## 1-KLICK-ÜBERSICHT

**AKTUELLER AUFTRAG:**  
OTTO real abnehmen: Produktfeed + Productwissen-Exact-Match + reale Bannerquelle + automatische anteilsgesteuerte Bannerverteilung + manuelle Reparaturprobe.

**BEREITS STRUKTURELL UMGESETZT:**  
Awin/OTTO-Produkte, 1/2/3-Produktplätze, Exact-Consumer, Verkäufer-Gate, automatische Bannerziel-/Slotzuordnung, Relevance-First-Anteilssystem, Reparaturinstanz, automatischer Joined-/Feedlisten-Refresh und snapshot-freier Start explizit freigegebener Awin-Programme.

**NICHT TUN:**  
kein eigenes OTTO-Plugin; keine zweite Providerarchitektur; keine direkte Productwissen-Tabellenkopplung; kein Ersatzprodukt bei Exact Match; kein Produktbild als Banner; keine Quote vor Relevanz; Digistore24 nicht nebenbei öffnen.

## BANNERVERTEILUNG – AKTUELLER VERTRAG

Startanteile:
- OTTO 40
- Awin andere 25
- ADCELL 20
- Direkt 15
- Digistore24 0
- Sonstige 0

Regel:
**Relevanz/Sicherheit zuerst, Anteil nur zwischen gleich relevanten Möglichkeiten.**

Fehlende Quelle:
Anteile automatisch unter den verfügbaren gleich relevanten Quellen normalisieren.

Verteilungseinheit:
Bannerplätze, nicht abrechnungsgenaue Impressionen.

Stabilität:
Kalenderwoche + Kontext + Slot.

## REPARATURINSTANZ

Normalzustand = Automatik.

Intern möglich:
- fest auswählen;
- nicht anzeigen;
- Vererbung auf Unterseiten;
- zurück zur Automatik.

Zusätzlich Control-/Veto-Ebenen und Notabschaltung.

## NEXT ACTION – NUR DIESER WEG

**JETZT ZUERST:** aktuellen gebundenen Source-Stand exakt prüfen:

`bash AFFILIATE_HOBBYRAUM/run_otto_checks.sh`

Falls dieser Direktlauf technisch nicht möglich ist, genau den isolierten Ersatzprüfweg verwenden:

`python3 AFFILIATE_HOBBYRAUM/affiliate_hobbyraum.py AFFILIATE_HOBBYRAUM/TASK.current.json`

**Erst nach PASS dieses aktuellen Source-Standes:**
1. Produktvergleich-Büro prüft/übernimmt den isolierten Brückenkandidaten `hobbyroom/productwissen-affiliate-exact-bridge-20260907`; Affiliate merged ihn nicht selbst.
2. OTTO Advertiser **14336** im eigenen Awin-Zugang real nachweisen.
3. echten OTTO-Produktfeed lesen; reale Verkäufer-Spalte exakt binden.
4. WordPress/MariaDB End-to-End: Hub 1/2/3, Kategorie 1/2/3, Beitrag, Exact Match / kein Ersatz.
5. realen OTTO/Awin-Creative-Bestand bzw. belegten Export/API-Weg anbinden.
6. echtes Banner automatisch prüfen → Ziel → Slot → Anteil → Ausgabe.
7. reale Stichprobe der Anteilverteilung prüfen.
8. manuelle Fehlzuordnung reparieren und Rückkehr auf Automatik belegen.
9. erst danach Release-Gates weiterführen.

## PRODUCTWISSEN-GRENZE

`ppar_affiliate_exact_product_requirements`

Produktwissen = fachlich.
Affiliate = Commerce.

Kein Exact Match = keine Karte.

## BANNERQUELLEN-GRENZE

Zuordnung, Anteilssystem, 0-Anteil-Sperre, Mehrfachplatz-Deduplizierung und manuelle Reparatur sind strukturell vorhanden.

Beschaffung ist erst vollständig automatisiert, wenn ein realer maschinenlesbarer OTTO/Awin-Creative-Weg belegt ist.

Bis dahin:
reales Creative → Automatik.
Kein reales Creative → kein Banner.

## TECHNISCHE AUTORITÄTEN

- `control/release-governance/CURRENT_RELEASE.json`
- `release/affiliate-zentrale/AGENTS.md`
- `release/affiliate-zentrale/current/affiliate-portal-router/`
- `release/affiliate-zentrale/CURRENT_SOURCE_SHA256.txt`
- `protocol/AFFILIATE_RELEASE_OTTO_AUTOMATION_CONCEPT_20260907.md`

## OFFENE RELEASE-GRENZE

GitHub Kandidat: 6.72.1  
WordPress-Livebeleg: 6.72.2

Vor Release auflösen.

Digistore24 bleibt zurückgestellt.


## REALER BANNERQUELLEN-ANSCHLUSS

Technische Anschlussstelle:
`ppar_affiliate_awin_static_creatives`

Nur reale Bannerzeilen:
Advertiser-ID + Creative-ID + Titel + Bild + Tracking.

Ungebunden → vorhandene Banner bleiben erhalten.
Gebunden und leer → `['bound'=>true,'rows'=>[]]` erlaubt kontrollierte Reconciliation.
Kein erfundener Awin-API-Weg.

## PRODUCTWISSEN-BRÜCKE

Offizieller Produktwissen-Branch bleibt unangetastet:
`hobbyroom/productwissen-v1-prototype`

Isolierter Integrationskandidat:
`hobbyroom/productwissen-affiliate-exact-bridge-20260907`

Bridge-Vertrag:
`protocol/PRODUCTWISSEN_AFFILIATE_EXACT_BRIDGE_20260907.md`

Affiliate darf diesen Branch nicht selbst mergen.
Übernahmeentscheidung liegt beim Produktvergleich-Büro.
