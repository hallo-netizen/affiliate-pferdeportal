# AFFILIATE – CURRENT STATE

STAND: 2026-09-07
STATUS: OTTO-AUTOMATISIERUNG + PRODUCTWISSEN-EXACT + ANTEILSGESTEUERTE BANNERVERTEILUNG STRUKTURELL IMPLEMENTIERT / REALDATEN + REALE BANNERQUELLE OFFEN

## AUTORITÄT

Diese Datei ist die einzige aktuelle Campus-Standzusammenfassung des Büros AFFILIATE.

- aktuelle Arbeit / NEXT ACTION → `HOBBYRAUM.md`
- Fehler → `protocol/PROJECT_MEMORY/FEHLERREGISTER.md` → Originalquelle
- Zielvertrag → `protocol/PROJECT_MEMORY/ZIELVERTRAEGE/REGISTER.md`
- Warum/Änderungen → `protocol/PROJECT_MEMORY/AENDERUNGSREGISTER.md`
- technische Release-Autorität → `control/release-governance/CURRENT_RELEASE.json`
- kanonische Source → `release/affiliate-zentrale/current/affiliate-portal-router/`

## Nutzerpriorität

- OTTO ist der aktuell gebundene Affiliate-Auftrag.
- Digistore24 bleibt zurückgestellt und nicht blockierend.
- Kein eigenes OTTO-Plugin.
- OTTO läuft technisch über Awin.
- Normalbetrieb soll weitgehend vollautomatisch sein.
- Menschliche Eingriffe sind Reparaturinstanz, nicht Hauptworkflow.

## Produktwissen

Produktwissen bleibt die fachliche Produkt-/Variantenwahrheit.

Affiliate bleibt Commerce-Schicht für:
- Angebot;
- Preis;
- Verfügbarkeit;
- Verkäufer;
- Tracking;
- reale Werbemittel.

Schnittstelle:
`ppar_affiliate_exact_product_requirements`

Exact Match:
GTIN/EAN bzw. belastbare echte MPN.

Kein identisches Angebot = keine Affiliate-Karte.
Kein Ersatzprodukt.

## OTTO-Produkte

Strukturell umgesetzt:

- kanonische Awin-Advertiser-ID **14336**;
- nur eine technische ID-Hauptwahrheit im Product Source Plan;
- Awin-Produktimport → Asset-Verifikation;
- Verkäufer-Gate;
- echtes Tracking;
- reales/verifiziertes Bild;
- GTIN/EAN und echte MPN bis in die Kampagne;
- Händler-SKU ist keine Exact-MPN;
- Hub/Kategorie/Journal Produktplätze 1/2/3;
- normale Beitragsprodukte;
- Productwissen-Exact-Match;
- kein Ersatzmodell;
- Preis/Bestand/Verkäufer verändern Freshness;
- Artikelpläne werden nach Verifikationswellen neu bewertet.

## Vollautomatische Bannerverteilung

Die vorhandene automatische Ziel-/Slotzuordnung wird jetzt zusätzlich durch eine **Relevance-First-Anteilssteuerung** ergänzt.

Verbindliche Reihenfolge:

1. manuelle Reparatur/Festzuordnung/Veto;
2. technische und rechtliche Freigabe;
3. Ziel-/Themenrelevanz;
4. Slot-/Formatpassung;
5. nur innerhalb der besten aktuell verfügbaren Relevanzstufe → Anteilssystem;
6. innerhalb der gewählten Quelle bleibt die bestehende Qualitäts-/Prioritätsreihenfolge.

Konfigurierbarer Startwert:

- OTTO: **40**
- andere Awin-Programme: **25**
- ADCELL: **20**
- Direktpartner: **15**
- Digistore24: **0**
- Sonstige: **0**

Die Werte sind relative Zielanteile.
Fehlt eine Quelle, werden nur die vorhandenen gleich relevanten Quellen automatisch neu normalisiert.

V1 verteilt **Bannerplätze**, nicht abrechnungsgenaue Impressionen.

Die Wahl bleibt deterministisch pro:
- Kalenderwoche;
- Seite/Kontext;
- Banner-Slot.

Damit:
- kein Request-Zufall;
- kein Flackern;
- cachefreundlich;
- reproduzierbar;
- trotzdem regelmäßige Rotation.

Banneranteile greifen auf allen relevanten Bannerfamilien:
- Startseite;
- Hub;
- Kategorie/Produktseite;
- Beitrag;
- Journal;
- Anzeigenmarkt.

## Manuelle Reparaturinstanz

Die bestehende interne Seite **Zuordnungen** ist ausdrücklich Reparaturinstanz.

Möglichkeiten:
- Automatik;
- festes Banner/Produkt;
- keine Ausgabe;
- Vererbung auf Unterseiten.

Zusätzlich bleiben:
- Provider-Veto;
- Partner-Veto;
- Creative-Veto;
- Target-Veto;
- Slot-Veto;
- Output-Veto;
- globale Notabschaltung.

Wichtig:
Auch der gespeicherte Artikelplan prüft jetzt die manuelle Bannerzuordnung **vor** der Automatik.

## Bannerquelle

Automatische Zuordnung/Verteilung: strukturell vorhanden.

Automatische Beschaffung eines realen OTTO/Awin-Creative-Katalogs: noch nicht real belegt.

Deshalb:
- reales OTTO/Awin-Creative vorhanden/importiert → automatisch prüfen, Ziel bestimmen, Slot bestimmen, Anteil anwenden, aktivieren;
- kein reales Creative → kein Banner;
- kein Produktbild als Fake-Banner.

## Technischer Stand

Branch:
`affiliate-release-current`

HEAD:
`99553e1f94cfde57187b671f23cadb09b0e7c417`

Aktiver Kandidat:
**6.72.1**

Source-Dateien:
26

Source-Manifest SHA-256:
`1140bba9bd2db78d4a347f1d6ad23ee82e17213fff33270f0ffb169b6d0973fb`

Governance Generation:
**12**

Release:
**NICHT FREIGEGEBEN**

## Prüfstand

PASS:
- statische Current-Source-Prüfung der zentralen OTTO-ID;
- statische Prüfung der Anteilskonfiguration;
- Relevanz vor Quote;
- deterministische Wochenverteilung;
- automatische Normalisierung bei fehlenden Quellen;
- alle realen Bannerplatzfamilien eingebunden;
- manuelle Reparaturinstanz vorhanden;
- manuelle Reparatur greift vor Artikelplan-Automatik;
- Digistore24-Anteil 0;
- Productwissen-Exact-Logik bleibt getrennt.

Evidence:
`release/affiliate-zentrale/evidence/otto_awin_banner_distribution_contract_20260907.txt`

Noch **kein** exakter Hobbyraum-Runner-PASS in diesem Chat.
Der gebundene Test wurde aktualisiert, aber der vorgesehene Docker/Podman-Lauf konnte in der aktuellen Laufzeit nicht ausgeführt werden.

## Real/LIVE noch offen

- OTTO 14336 im eigenen Awin-Konto real belegen;
- echten OTTO-Produktfeed durch WordPress/MariaDB;
- reale Verkäufer-Spalte binden;
- reale Produktkarten auf Hub/Kategorie/Beitrag;
- echten OTTO/Awin-Bannerbestand bzw. realen Beschaffungsweg;
- echtes Banner automatisch zuordnen und ausspielen;
- reale Stichprobe der Anteilverteilung über genügend Bannerplätze;
- manuelle Reparatur + Rückkehr zur Automatik real prüfen.

## Bestehende Live-Differenz

WordPress-Livebeleg:
**6.72.2**

GitHub-Kandidat:
**6.72.1**

Vor Release auflösen; nicht still ignorieren.
