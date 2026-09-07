# AFFILIATE – HOBBYRAUM

STAND: 2026-09-07
STATUS: AKTIV

## 1-KLICK-ÜBERSICHT

**AKTUELLER AUFTRAG:**  
OTTO real abnehmen: Produktfeed + Productwissen-Exact-Match + reale Bannerquelle + automatische anteilsgesteuerte Bannerverteilung + manuelle Reparaturprobe.

**BEREITS STRUKTURELL UMGESETZT:**  
Awin/OTTO-Produkte, 1/2/3-Produktplätze, Productwissen-Exact-Bridge offiziell integriert, Verkäufer-Gate, automatische Bannerziel-/Slotzuordnung, Relevance-First-Anteilssystem, Reparaturinstanz, automatischer Joined-/Feedlisten-Refresh und snapshot-freier Start explizit freigegebener Awin-Programme.

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

## NEXT ACTION – ERSTER PLUGINTEST

**JETZT:** den gebauten 6.72.1-Aktivierungs-Smoke in einer isolierten/testweisen WordPress-Instanz installieren und aktivieren:

`release/affiliate-zentrale/evidence/affiliate-zentrale_v6.72.1_ACTIVATION_SMOKE_ONLY.zip`

PASS für diesen ersten Plugintest bedeutet ausschließlich:
- ZIP wird von WordPress als Plugin akzeptiert;
- Plugin lädt ohne PHP-Fatal;
- Aktivierung läuft ohne PHP-Fatal;
- Plugin steht danach als aktiviert.

Harte Grenze:
Dieses Paket enthält absichtlich nicht die beiden großen eBay-Laufzeitkataloge. Deshalb **kein eBay-/Vollfunktions-/Release-Test** damit.

**Danach bleibt der gebundene technische Releaseweg:**
1. exakten Current-Source-Lauf `bash AFFILIATE_HOBBYRAUM/run_otto_checks.sh` bzw. den vorhandenen isolierten Containerweg ausführen;
2. OTTO Advertiser **14336** im eigenen Awin-Zugang real nachweisen;
3. echten OTTO-Produktfeed lesen und reale Verkäufer-Spalte exakt binden;
4. WordPress/MariaDB End-to-End: Hub 1/2/3, Kategorie 1/2/3, Beitrag, Exact Match / kein Ersatz;
5. realen OTTO/Awin-Creative-Bestand bzw. belegten Export/API-Weg anbinden;
6. echtes Banner automatisch prüfen → Ziel → Slot → Anteil → Ausgabe;
7. reale Stichprobe der Anteilverteilung prüfen;
8. manuelle Fehlzuordnung reparieren und Rückkehr auf Automatik belegen;
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

Offizieller Produktwissen-/Produktvergleich-Branch:
`hobbyroom/productwissen-v1-prototype`

Aktueller Head bei letzter Prüfung:
`020ba35e7d304407e8b71e0751b6f4167b93427d`

Bridge-PASS-Head:
`f16f9d9b54a2df9397ef6d5d361b4a61f10347de`

WordPress+MySQL Run:
`34131779064` → SUCCESS.

Status:
**OFFIZIELL INTEGRIERT / READ-ONLY EXACT-BRIDGE PASS.**

Der frühere isolierte Bridge-Branch bleibt nur historischer Beleg. Affiliate merged dort nichts mehr.
