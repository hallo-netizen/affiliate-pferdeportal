# AFFILIATE – CURRENT STATE

STAND: 2026-09-07
STATUS: OTTO-AUTOMATISIERUNG STRUKTURELL IMPLEMENTIERT / PRODUCTWISSEN-EXACT-SCHNITTSTELLE BEREIT / REALDATEN + REALE BANNERQUELLE OFFEN

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

## OTTO-Konzept

OTTO wird als breite Commerce-Quelle auf mehreren Ebenen genutzt:

- Startseite: reales passendes OTTO/Awin-Banner, kein neuer beliebiger Produktblock.
- Hub Ebene 1: Banner + bis zu drei passend gerankte Produkte.
- Hub Ebene 2 / Produktgruppe: Banner + bis zu drei Produkte.
- Kategorie / Leaf: Banner + bis zu drei Produkte.
- normale Beiträge: passendes Banner + bis zu drei Produkte.
- Produktvergleich / Variantenvergleich / fachlich exakt gebundene Beratung: Exact Product Match; niemals ähnlich klingendes Ersatzprodukt.

Offizielle Werbeformen werden intern KISS abgebildet:
- Produktfeed → Produktkarten;
- reale Banner/Images → bestehender Bannerweg;
- Deeplinks → Linkziel von Produktkarten/Bannern;
- Logo → kein eigener neuer Slot; nur als reales passendes Creative;
- Sortimentswerbung → reales Sortimentscreative oder konkrete Produktkarten, keine erfundene Bannerform.

Detailkonzept:
`protocol/AFFILIATE_RELEASE_OTTO_AUTOMATION_CONCEPT_20260907.md`

## Produktwissen – relevant, aber getrennt

Die parallel entwickelte zentrale Produktwissen-Datenbank ist relevant.

Verbindliche Rollen:
- Produktwissen = fachliche Produkt-/Variantenidentität + Fakten.
- Affiliate = aktuelles Angebot, Preis, Verfügbarkeit, Verkäufer, Tracking, reale Werbemittel.

Keine direkte Tabellenkopplung und kein Affiliate-Schreibrecht in Produktwissen.

Affiliate-Consumer-Schnittstelle:
`ppar_affiliate_exact_product_requirements`

Exact Match:
GTIN/EAN bzw. belastbare echte MPN.
Kein identisches Angebot = keine Affiliate-Karte.
Kein Ersatzprodukt.

## Technisch umgesetzt

- OTTO wird kanonisch über Awin Advertiser-ID **14336** erkannt, nicht über geratenen Programmnamen.
- Awin-Produktimport stößt Asset-Verifikation an.
- OTTO-Autoaktivierung bleibt fail-closed:
  - Awin-Programme-Gate;
  - aktives Produkt;
  - eindeutige automatische Zielklassifikation;
  - gültiger Trackinglink;
  - reales/verifiziertes Bild;
  - konkreter Verkäufer.
- GTIN/EAN und explizite MPN können als Exact-Product-Identität bis in die Kampagne getragen werden.
- Händler-SKU wird nicht als echte MPN ausgegeben.
- Kategorie-/Hub-/Journal-Produkte nutzen die vorhandenen 1/2/3-Plätze.
- Exact-Product-Anforderungen dürfen generische Provider-/Kohortenlogik überstimmen, aber keine Sicherheits-/Health-Gates.
- fehlender Exact Match → kein Ersatz.
- Verkäufer wird auf konkreten OTTO-Produktkarten ausgegeben.
- Produktänderungen bei Preis/Bestand/Verkäufer verändern den Freshness-Fingerprint.
- nach kompletter Asset-Verifikationswelle werden Artikelpläne gebündelt neu bewertet.
- reale importierte Awin-Banner können bereits über den bestehenden zentralen Ziel-/Slotweg automatisch aktiviert werden.
- Produktbilder werden nicht zu Fake-Bannern umgebaut.

## Banner – harte Trennung

**Automatische Zuordnung/Activation:** strukturell vorhanden.

**Automatische Beschaffung eines OTTO/Awin-Bannerkatalogs:** noch nicht real belegt.

Deshalb:
- reales OTTO/Awin-Creative vorhanden/importiert → automatische Prüfung, Zielzuordnung, Slotwahl und Aktivierung möglich;
- kein belegter Creative-Katalog/API/Export → Bannerbeschaffung bleibt PENDING;
- keine Ersatzkonstruktion.

## Aktueller technischer Stand

Branch:
`affiliate-release-current`

HEAD:
`808ec4f96a42e1647429f318b2fcd035739d9e72`

Aktiver Kandidat:
**6.72.1**

Source-Dateien:
26

Aktuelles Source-Manifest SHA-256:
`7505a05b1a5534f7cfb0d3063b1eb50e40f723e223847299cb3864c5d116cffc`

Governance Generation:
**11**

Release:
**NICHT FREIGEGEBEN**

## Prüfstand

PASS:
- statischer Current-Source-Contract-Test für OTTO-ID, Exact Match, Seller-Gate, Produktverteilung und Bannergrenze;
- lokaler PHP-Behavioral-Test für 14336, GTIN/EAN, MPN, No-Substitution und Kategorie/Artikel-Platzierung.

Noch kein vollständiger Hobbyraum-Runner-PASS in diesem Chat:
Der gebundene Runner benötigt Docker/Podman; die aktuelle lokale Laufzeit hatte PHP, aber weder Docker noch Podman.
Der Test ist jetzt korrekt in `AFFILIATE_HOBBYRAUM/TASK.current.json` gebunden und muss in einer geeigneten Laufzeit real ausgeführt werden.

Evidence:
`release/affiliate-zentrale/evidence/otto_awin_productwissen_banner_contract_20260907.txt`

## Real/LIVE noch offen

- OTTO 14336 im eigenen Awin-Publisherkonto real lesen;
- echten Produktfeed End-to-End verarbeiten;
- tatsächliche Verkäufer-Spalte aus dem realen Feed binden – keinen Feldnamen raten;
- WordPress/MariaDB-End-to-End;
- öffentliche Produktkarten auf Hub/Kategorie/Beitrag;
- realen OTTO/Awin-Bannerbestand bzw. realen Beschaffungsweg prüfen;
- reales Banner automatisiert zuordnen und öffentlich prüfen.

## Bestehende Live-Differenz

Campus-Livebeleg:
WordPress **6.72.2**

GitHub-Kandidat:
**6.72.1**

Diese Differenz bleibt offen und darf vor einem echten Release nicht ignoriert werden.
