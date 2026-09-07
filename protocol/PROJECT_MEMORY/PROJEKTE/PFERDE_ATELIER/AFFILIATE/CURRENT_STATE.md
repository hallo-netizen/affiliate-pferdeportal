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
`df616a8cc6690483538116dc9c57e32028b15ddf`

Aktiver Kandidat:
**6.72.1**

Source-Dateien:
26

Source-Manifest SHA-256:
`b12706416fa7357ddd4b6ac61ed951b0f2b5b88b0ee5ff8577112c1eea2448f4`

Governance Generation:
**15**

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


## Direkter Prüflauf ohne Docker

Im Repository ist jetzt ein read-only Ein-Kommando-Test vorhanden:

`bash AFFILIATE_HOBBYRAUM/run_otto_checks.sh`

Er prüft:
- PHP-Syntax der gebundenen Affiliate-Source;
- OTTO/Awin/Productwissen-/Banner-Vertrag;
- ausführbare Anteil-/Reparatur-/Real-Source-Behavior-Tests.

Zusätzlich bleibt der isolierte Container-Hobbyraum:
`python3 AFFILIATE_HOBBYRAUM/affiliate_hobbyraum.py AFFILIATE_HOBBYRAUM/TASK.current.json`

## Letzte Härtungen

- Anteil `0` = harte automatische Ausschlusssperre.
- Mehrere Bannerplätze derselben Seite erhalten getrennte deterministische Anteilsentscheidungen.
- Platz 2 darf Platz 1 nicht duplizieren.
- reale Awin-Bannerquelle kann über `ppar_affiliate_awin_static_creatives` angeschlossen werden.
- gebundene Quelle mit 0 Creatives ist von „nicht angeschlossen“ unterscheidbar und kann alte Banner kontrolliert reconciliieren.
- manuelle Seitenreparaturen benötigen Begründung und speichern Benutzer + Zeitpunkt.
- Kategorie-/sonstige Zielreparatur nutzt die vorhandene feste Creative→Portalziel/Slot-Entscheidung mit Begründung.
