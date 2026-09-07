# AFFILIATE – CURRENT STATE

STAND: 2026-09-07
STATUS: OTTO-AUTOMATISIERUNG + PRODUCTWISSEN-EXACT + BANNERVERTEILUNG STRUKTURELL IMPLEMENTIERT / PRODUCTWISSEN-BRÜCKE INTEGRIERT / 6.72.1 ACTIVATION-SMOKE BEREIT / BOUND CHECK + REALDATEN OFFEN

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
- Joined-Awin-Programmliste und offizielle Produktfeedliste werden zu Beginn eines neuen Automationszyklus aktualisiert.
- Bei Refreshfehler bleibt Last-Known-Good erhalten.
- explizit `allow_local` + aktuell `joined` Programme können ohne vorhandenen Partner-Snapshot selbstständig in die Automation starten.

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

Branch-HEAD:
`d6f34efc5af36b45aaa5f907f8d7fd505c20b416`

Source-tragender 26-Dateien-Stand:
`84390240b87e510349c636b9dd9f1a5dfc8ce5d7`

Aktiver Kandidat:
**6.72.3**

Source-Dateien:
26

Source-Manifest SHA-256:
`680fe0078071dcaba63372f4dbd0caf5dab0d5c5c711439d69adf992d9e258cf`

Governance Generation:
**20**

Release:
**NICHT FREIGEGEBEN**

## Prüfstand

- **6.72.3 WordPress-Aktivierung: PASS** (Nutzer bestätigt am 07.09.2026; kein PHP-Fatal, Plugin aktiv).

CURRENT-SOURCE STATIC PASS:
- zentrale OTTO-ID;
- Productwissen Exact Match / kein Ersatz;
- Verkäufer-Fail-Closed;
- Relevanz vor Quote;
- Anteil 0 = automatische Sperre;
- deterministische Mehrfachplatzverteilung ohne Creative-Dublette;
- manuelle Reparatur vor Automatik + Begründung/Benutzer/Zeit;
- reale Awin-Creative-Anschlussstelle fail-closed;
- Joined-Programmliste wird vor neuem Awin-Zyklus aktualisiert;
- offizielle Produktfeedliste wird vor neuem Awin-Zyklus aktualisiert;
- Refreshfehler bewahrt Last-Known-Good;
- explizit freigegebene + aktuell joined Awin-Programme starten ohne Snapshot-Voraussetzung.

Evidence:
- `release/affiliate-zentrale/evidence/otto_awin_productwissen_banner_contract_20260907.txt`
- `release/affiliate-zentrale/evidence/otto_awin_banner_distribution_contract_20260907.txt`

Zusätzlicher exakter Source-Readback am 07.09.2026:
- 30/30 OTTO/Awin/Productwissen-/Banner-Strukturassertionen gegen Source-Head `84390240...` PASS;
- dies ersetzt ausdrücklich **nicht** den direkten PHP-Lauf `run_otto_checks.sh`.

OFFEN:
- exakter aktueller Repo-Checkout-Lauf `bash AFFILIATE_HOBBYRAUM/run_otto_checks.sh` bzw. gebundener Containerlauf;
- erster WordPress-Aktivierungs-Smoke des gebauten 6.72.1-Testpakets;
- frühere lokale Behavior-PASS-Belege gelten nach der letzten Source-Änderung nicht als Current-Source-PASS und wurden entsprechend als stale markiert.

## Real/LIVE noch offen

- OTTO 14336 im eigenen Awin-Konto real belegen;
- echten OTTO-Produktfeed durch WordPress/MariaDB;
- reale Verkäufer-Spalte binden;
- reale Produktkarten auf Hub/Kategorie/Beitrag;
- echten OTTO/Awin-Bannerbestand bzw. realen Beschaffungsweg;
- echtes Banner automatisch zuordnen und ausspielen;
- reale Stichprobe der Anteilverteilung über genügend Bannerplätze;
- manuelle Reparatur + Rückkehr zur Automatik real prüfen.

## Erster Plugin-Test – PASS

Installierter Testkandidat: **6.72.3**

Belegt:
- WordPress akzeptiert das Plugin;
- Plugin lädt ohne PHP-Fatal;
- Aktivierung läuft ohne PHP-Fatal;
- Plugin bleibt aktiviert.

Status: **PASS**.

Nächster Funktionstest: WordPress-Backend → **Affiliate-Zentrale → Übersicht** öffnen; danach **Netzwerke & API** öffnen und prüfen, ob die Awin-Karte vollständig sichtbar ist. Noch nichts speichern oder starten.

## Bestehende Live-Differenz

WordPress-Livebeleg:
**6.72.2**

GitHub-Kandidat:
**6.72.3**

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

## Productwissen-Brücke – offizieller Status

Die read-only Productwissen→Affiliate-Brücke ist inzwischen vom Produktvergleich-Büro offiziell integriert.

Offizieller Produktwissen-/Produktvergleich-Branch:
`hobbyroom/productwissen-v1-prototype`

Head bei letzter Prüfung:
`020ba35e7d304407e8b71e0751b6f4167b93427d`

Bridge-PASS-Head:
`f16f9d9b54a2df9397ef6d5d361b4a61f10347de`

WordPress+MySQL-Beleg:
GitHub Actions Run `34131779064` → SUCCESS.

Belegt:
- `ppar_affiliate_exact_product_requirements` wird read-only geliefert;
- EAN/GTIN Exact Match PASS;
- MPN Exact Match PASS;
- kein Identifier = keine Affiliate-Anforderung;
- kein Ersatzprodukt;
- bestehende Anforderungen bleiben erhalten;
- keine direkte Productwissen-Tabellenkopplung;
- Zero-Freedom-/Golden-Output-Regressions bleiben PASS.

Der frühere Branch `hobbyroom/productwissen-affiliate-exact-bridge-20260907` ist nur noch historischer Integrationskandidat, keine aktuelle Arbeitsquelle.

Status:
**OFFIZIELL INTEGRIERT / BRIDGE WORDPRESS+MYSQL PASS / AFFILIATE-REAL-OTTO-E2E OFFEN.**
