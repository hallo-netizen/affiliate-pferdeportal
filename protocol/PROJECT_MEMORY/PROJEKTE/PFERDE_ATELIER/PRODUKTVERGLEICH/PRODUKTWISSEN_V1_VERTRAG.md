# PRODUKTWISSEN – V1 DATENVERTRAG

STAND: 2026-09-07
STATUS: V1-KONZEPT / PROTOTYP-BASIS

## ZWECK

Eine einzige interne, quellengebundene Produktwahrheit für:
- Produktvergleich;
- Variantenvergleich;
- Beratung;
- Affiliate-Exact-Match.

Keine öffentliche WordPress-Kategorie und keine eigene Content-Welt.

## KISS-DATENMODELL

### 1. PRODUKT
Pflicht:
- `product_id` – stabile interne ID
- `manufacturer`
- `model_name`
- `product_group_key`
- `manufacturer_product_url`
- `lifecycle_status` – ACTIVE | TEMPORARILY_UNAVAILABLE | DISCONTINUED | UNKNOWN
- `last_verified_at`

Optional:
- `model_family`
- `generation`
- `successor_product_id`

### 2. PRODUKTIDENTIFIER
Mehrere Kennungen pro Produkt/Variante erlaubt:
- `product_id` oder `variant_id`
- `identifier_type` – GTIN | EAN | MPN | MANUFACTURER_ARTICLE_NUMBER
- `identifier_value`

Regel:
Kennungen identifizieren exakt, entscheiden aber nicht allein, ob etwas Produkt oder Variante ist.

### 3. VARIANTE
Nur kaufrelevante Ausführungen desselben Basismodells:
- `variant_id`
- `product_id`
- `variant_name`
- `variant_key`
- eigene Identifier soweit vorhanden
- `lifecycle_status`
- `last_verified_at`

Keine künstlichen Varianten nur wegen Farbe/Größe, wenn daraus keine eigenständige sinnvolle Kaufentscheidung entsteht.

### 4. FAKT + QUELLE
Je belegter Produkteigenschaft:
- `subject_id` – Produkt oder Variante
- `fact_key`
- `fact_value`
- `unit` optional
- `source_url`
- `source_type` – MANUFACTURER | OFFICIAL_DOCUMENTATION | APPROVED_SECONDARY
- `verified_at`
- `fact_status` – VERIFIED | NOT_IN_SOURCE | SOURCE_CONFLICT | CONFIGURATION_DEPENDENT

Hard Rule:
Keine unbelegte Ableitung als Herstellerfakt speichern.

## LESERECHTE / SCHNITTSTELLEN

### PRODUKTVERGLEICH liest
- Produkte/Varianten
- Fakten
- Quellenstatus
- Lebenszyklus
und speichert nur eigene Vergleichsdefinitionen, keine Kopie der Fakten.

### BERATUNG/TEXT liest
- verifizierte Produkteigenschaften
- fachlich abgeleitete Bedarfszuordnungen, wenn separat belegt
und darf die Produktfakten nicht verändern.

### AFFILIATE liest
- stabile Produkt-/Varianten-ID
- Hersteller
- exakte Modell-/Variantenbezeichnung
- Identifier
und liefert separat aktuelle Angebote/Preise/Verfügbarkeit.

Affiliate darf Produktfakten nicht überschreiben.

## SEO

SEO schreibt nichts in PRODUKTWISSEN.
SEO liefert nur Signale an PRODUKTVERGLEICH:
- Nachfrage;
- Keyword;
- Priorität;
- Kannibalisierungswarnung.

## UPDATE-PRINZIP

Standard:
- Produkt-/Herstellerfakten zyklisch prüfen, V1-Zielwert 6 Monate;
- ereignisbasiert früher prüfen bei Quellenänderung, Discontinued, Nachfolger oder Konflikt;
- Affiliate-Verfügbarkeit separat und häufiger.

Änderung eines Produkts markiert nur die Beiträge/Vergleiche zur Nachprüfung, die dieses Produkt verwenden.

## FAIL-CLOSED

BLOCKED statt raten bei:
- unklarer Produktidentität;
- unklar Produkt vs. Variante;
- Quellenkonflikt;
- fehlender erforderlicher Herstellerinformation;
- unklarem Nachfolger.

## V1-GRENZE

Noch nicht enthalten:
- automatische Veröffentlichung;
- vollständige SEO-Engine;
- Preise als Produktfakt;
- Affiliate-Produktbestand als fachliche Hauptquelle;
- tiefe STARTMASTER/TEXT-Laufzeitkopplung.

## LEITSATZ

**Eine Produktwahrheit. Viele Leser. Genau ein fachlicher Schreiber.**
