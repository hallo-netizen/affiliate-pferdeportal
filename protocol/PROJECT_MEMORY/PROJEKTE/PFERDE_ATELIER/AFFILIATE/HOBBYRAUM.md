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

## NEXT ACTION – ERSTER FUNKTIONSTEST

**JETZT:** WordPress-Backend → **Affiliate-Zentrale → Übersicht** öffnen.

PASS 1:
- Seite öffnet ohne Fatal/weiße Seite;
- Überschrift **Affiliate-Zentrale** sichtbar;
- Navigation/Submenüs sichtbar.

Danach **Netzwerke & API** öffnen.

PASS 2:
- Seite öffnet ohne Fatal;
- Awin-Karte sichtbar;
- Felder für Publisher-ID / Zugang vorhanden;
- Button **Speichern & Zugang prüfen** sichtbar;
- **noch nichts speichern oder starten**.

Bei PASS danach erst der echte OTTO/Awin-Verbindungstest.

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
