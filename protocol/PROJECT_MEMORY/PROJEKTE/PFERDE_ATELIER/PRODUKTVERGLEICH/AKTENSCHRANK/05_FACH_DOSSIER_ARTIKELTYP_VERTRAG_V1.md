# PRODUKTVERGLEICH – FACH-DOSSIER-/ARTIKELTYP-VERTRAG V1

Stand: 2026-09-09
Status: VERBINDLICH FÜR PRODUKTVERGLEICH-FACHSEITE / KEINE SEO-TEXT-IMPLEMENTATION

## Zweck

Dieser Vertrag definiert ausschließlich, **WELCHE fachliche Wahrheit** ein Produktvergleich an die spätere SEO/TEXT-Produktion übergeben muss.

Er definiert **nicht**, wie der fertige Text formuliert wird.

Trennung:
- PRODUKTVERGLEICH = Produkte, Vergleichbarkeit, Fakten, erlaubte Aussagen, verbotene Aussagen, SEO-Eignung, Dossier.
- SEO/TEXT = fertige Sprache, Stil, Absatzbau, Überschriftenformulierung, LanguageTool, interne Links und allgemeine Textqualität.
- ACM = Orchestrierung.
- AFFILIATE = Angebot/Preis/Verfügbarkeit/Tracking.

## 1. Vergleichstyp

### PRODUCT_COMPARISON V1
- **exakt 2 konkrete konkurrierende Produkte**;
- mindestens zwei Hersteller;
- gleiche Produktgruppe;
- gleiche fachliche Nutzungsebene;
- keine künstliche Paarung nur wegen Affiliate-Verfügbarkeit.

Der aktive Artikeltyp beantwortet eine gebundene **A-gegen-B-Entscheidung**.

3–4 Produkte werden nicht in V1 hineingemischt. Ein echter Gruppenvergleich benötigt später einen eigenen gebundenen Vergleichstyp und eigenen Vertrag.

### VARIANT
Variantenvergleich bleibt fachlich getrennt:
- Varianten desselben Basismodells;
- eigene eindeutige Variantenidentitäten;
- keine künstliche Variante nur wegen Farbe/Größe ohne eigenständige Kaufentscheidung.

Er ist nicht automatisch Teil des A-vs-B-Produktvergleichsvertrags.

## 2. Pflichtinhalt des gebundenen Vergleichsdossiers

Das Dossier muss mindestens enthalten bzw. eindeutig referenzieren:

1. **Vergleichsidentität**
   - comparison_id / comparison_key;
   - comparison_type;
   - product_group_key;
   - Vertrags-/Profil-/Policy-Versionen und Hashbindungen.

2. **Exakt zwei Subjekte**
   - Hersteller;
   - Modell;
   - Variante, falls relevant;
   - interne stabile Produkt-/Varianten-ID;
   - exakte Identifier soweit vorhanden (GTIN/EAN/MPN);
   - keine fuzzy Ersatzidentität.

3. **Entscheidungsintent**
   - welche reale Kauf-/Nutzungsentscheidung beantwortet wird;
   - kein freier Writer-Intent.

4. **SEO-Eignung**
   - Ursprung: PRODUCT_TO_SEO oder SEO_TO_PRODUCT;
   - exakte geprüfte Suchanfrage(n);
   - direkter A-vs-B-Nachweis oder nachgewiesene Nachfrage beider exakten Produkte gemäß gültigem Vertrag;
   - aktueller Readiness-/Kannibalisierungsstatus;
   - Provider-/PSTE-Kontext und Evidenzbindung;
   - kein SEO-PASS = kein Produktionsauftrag.

5. **Vergleichsmerkmale**
   Für jedes Merkmal:
   - fact_key;
   - verständliche fachliche Bezeichnung;
   - Fakten je Produkt;
   - Faktenstatus;
   - Quelle/Provenance intern gebunden;
   - Vergleichbarkeit der Werte/Einheiten;
   - fachliche Entscheidungsklasse;
   - explizit erlaubte Aussageart oder explizit keine Präferenz.

6. **Erlaubte Aussagen**
   Nur deterministisch aus der gebundenen Produktgruppen-Decision-Policy erzeugte Aussagearten, z. B.:
   - dokumentierter technischer Unterschied;
   - höhere/niedrigere ausdrücklich deklarierte Zahl, wenn die Policy das erlaubt;
   - gebundene Bedarfszuordnung mit festem Need-Code.

7. **Verbotene Aussagen**
   Global und merkmalsbezogen fail-closed, insbesondere:
   - pauschaler Testsieger;
   - Rangliste/Punkte/Sterne;
   - aus Denier allein Haltbarkeit/Qualität/Robustheit;
   - aus unterschiedlich definierten Messwerten künstliche Rangfolge;
   - Passform-/Größenreichweitenurteil ohne normierte Vergleichsbasis;
   - Qualitäts-/Komforturteil ohne gebundene Evidenz;
   - Vorteil/Nachteil nur aus bloßer Andersartigkeit;
   - Affiliate-Verfügbarkeit als fachlicher Vorteil.

8. **Bedarfszuordnungen**
   Nur aus gebundener Policy:
   - fester Need-Code;
   - konkreter Bedarf;
   - genaues Produkt/Position;
   - belegte Faktenbasis;
   - keine freie Ergänzung durch SEO/TEXT.

9. **Quellenwarnungen**
   - NOT_IN_SOURCE;
   - SOURCE_CONFLICT;
   - CONFIGURATION_DEPENDENT;
   - unterschiedliche Messdefinitionen;
   - sonstige Grenzen der Vergleichbarkeit.

   Quellenbegrenzung darf keine Präferenz oder Bedarfszuordnung erzeugen.

10. **Titelbindung für SEO/TEXT**
    Kein fertiger Fließtexttitel wird hier erzwungen.

    Gebunden werden:
    - beide exakten Produktbezeichnungen als Pflichtsubjekte;
    - Vergleichstyp PRODUCT_COMPARISON;
    - Zielkeyword/Suchintent.

    SEO/TEXT darf daraus natürlich formulieren, darf aber kein Produkt ergänzen, austauschen oder weglassen.

## 3. Fachliche Artikelpflichten

Die spätere Beitragsart PRODUCT_COMPARISON muss fachlich:

1. die reale A-vs-B-Entscheidungsfrage klar machen;
2. eine kompakte Tabelle mit entscheidungsrelevanten belastbar vergleichbaren Merkmalen enthalten;
3. nur Unterschiede erläutern, für die das Dossier eine erlaubte Aussage bindet;
4. Bedarfszuordnungen nur verwenden, wenn ein gebundener Need-Code vorliegt;
5. Vergleichs-/Quellengrenzen sichtbar respektieren;
6. ohne pauschalen Sieger enden.

Wenn keine belastbare Bedarfszuordnung existiert, bleibt das Fazit neutral.

## 4. Was ausdrücklich NICHT Pflichtabschnitt ist

Der historische Produktvergleichs-Renderer ist kein Textvorbild.

Nicht automatisch erzeugen:
- leere Vor-/Nachteile-Tabellen;
- Sätze wie „Keine freigegebenen Vorteile vorhanden“;
- leere Unterschiedsabschnitte;
- wiederholte System-/Regelhinweise;
- eigenes Quellenkapitel ohne Nutzwert;
- redundante Wiederholung derselben Bedarfszuordnung.

Eine technische Differenz ist nicht automatisch ein Vorteil oder Nachteil.

## 5. Quellen- und Linkgrenze

Quellen/URLs bleiben als Provenance im Dossier gebunden.

Ob und wie Quellen später sichtbar gemacht werden, entscheidet der bestehende SEO/TEXT-Vertrag.
PRODUKTVERGLEICH baut keinen eigenen externen Linkweg.

## 6. Affiliate-Grenze

Nicht Teil der kanonischen Fachfakten:
- aktueller Preis;
- Händler;
- Lieferbarkeit;
- Provision;
- Affiliate-URL.

Diese Daten dürfen nachgelagert angezeigt werden, aber weder Paarung, Fachurteil noch Fazit verändern.

## 7. Aktualität und Kostenbindung

Hersteller-/Produktfakten folgen dem Produktwissen-Vertrag.

SEO-Zwischenevidenz folgt der gebundenen persistenten 90-Tage-/Kontextregel von UPC 0.8.2+.

Die fachliche Decision-Policy besitzt eine **eigene** Bindung.
Eine reine Policy-Änderung:
- erzwingt Dossier-Neuprüfung;
- darf bereits bezahlte unveränderte SEO-Evidenz nicht erneut kaufen.

0.8.2/0.8.3 Laufzeit-SEO-Binding identisch:
`863a724d9f349770d9f62c7c65ee7c74565d4247f9bf15504984ae4ece2c9003`

Ändert sich ein Produktfakt, wird der betroffene Vergleich fachlich neu geprüft.

## 8. Fail-closed-Abnahme

Kein produktionsfähiges Dossier bei:
- nicht exakt zwei Produkt-Subjekten;
- unklarer Produktidentität;
- nicht vergleichbaren Produkten;
- fehlenden erforderlichen Fakten;
- Fakten-/Profil-/Policy-Hashdrift;
- fehlender Decision-Policy für ein Pflichtmerkmal;
- unbelegter Bedarfszuordnung;
- SEO nicht geeignet;
- Kannibalisierung/Readiness BLOCK;
- Dossier-/Abschluss-Audit-Drift;
- Quellenkonflikt an einer entscheidungsnotwendigen Stelle ohne sichere neutrale Behandlung.

## 9. Technischer aktueller Beleg

UPC 0.8.3:
- Dossier-Vertrag: `UPC_BOUND_COMPARISON_DOSSIER_V2`;
- alle 14 Regendecken-Merkmale mit genau einer Decision-Policy;
- 11 reale herstellerübergreifende 0g-Regendecken-Paare geprüft;
- keine freie fachliche Aussageart;
- Policy-Drift fail-closed;
- keine Writer-/Draft-/Publish-Aktivierung.

## 10. KISS-Leitsatz

**Das Dossier liefert keine Prosa. Es liefert eine versiegelte Landkarte: Das sind exakt A und B, das sind die belegten Unterschiede, das darf daraus gesagt werden, das darf nicht gesagt werden.**
