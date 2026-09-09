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

### PRODUCT
- 2 bis 4 konkrete konkurrierende Produkte;
- mindestens zwei Hersteller;
- gleiche Produktgruppe;
- gleiche fachliche Nutzungsebene;
- keine künstliche Paarung nur wegen Affiliate-Verfügbarkeit.

Standardfall:
**2 Produkte**, wenn eine direkte A-vs-B-Entscheidung bzw. entsprechende Nachfrage vorliegt.

3–4 Produkte nur, wenn der gebundene Such-/Entscheidungsintent tatsächlich einen Gruppenvergleich trägt. Nicht zum künstlichen Auffüllen.

### VARIANT
- Varianten desselben Basismodells;
- eigene eindeutige Variantenidentitäten;
- keine künstliche Variante nur wegen Farbe/Größe ohne eigenständige Kaufentscheidung.

## 2. Pflichtinhalt des gebundenen Vergleichsdossiers

Das Dossier muss mindestens enthalten bzw. eindeutig referenzieren:

1. **Vergleichsidentität**
   - comparison_id / comparison_key;
   - comparison_type;
   - product_group_key;
   - Vertrags-/Ruleset-Versionen und Hashbindung.

2. **Exakte Subjekte**
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
   - Fakten je Produkt/Variante;
   - Faktenstatus;
   - Quelle/Provenance intern gebunden;
   - Vergleichbarkeit der Werte/Einheiten;
   - fachliche Bedeutung des Unterschieds oder explizit: keine belastbare Bedeutung ableitbar.

6. **Erlaubte Aussagen**
   Nur explizit gebundene Aussagen, z. B.:
   - dokumentierter technischer Unterschied;
   - dokumentierte höhere/niedrigere Herstellerangabe;
   - freigegebene Bedarfszuordnung mit Begründung.

7. **Verbotene Aussagen**
   Für alle nicht gedeckten Ableitungen ausdrücklich fail-closed, insbesondere:
   - pauschaler Testsieger;
   - Rangliste/Punkte/Sterne;
   - aus Denier allein pauschale Haltbarkeit;
   - aus unterschiedlich definierten Messwerten künstliche Rangfolge;
   - Passform-/Größenreichweitenurteil ohne normierte Vergleichsbasis;
   - Qualitäts-/Komfort-/Robustheitsurteil ohne gebundene Evidenz;
   - Vorteil/Nachteil nur aus bloßer Andersartigkeit;
   - Affiliate-Verfügbarkeit als fachlicher Vorteil.

8. **Bedarfszuordnungen**
   Je erlaubter Zuordnung:
   - konkreter Bedarf;
   - genaues Produkt/Position;
   - belegte Begründung;
   - Herkunft aus Ruleset/Faktenbindung.

9. **Quellenwarnungen**
   - NOT_IN_SOURCE;
   - SOURCE_CONFLICT;
   - CONFIGURATION_DEPENDENT;
   - unterschiedliche Messdefinitionen;
   - sonstige Grenzen der Vergleichbarkeit.

10. **Titelbindung für SEO/TEXT**
    Kein fertiger Fließtexttitel wird hier erzwungen.
    Gebunden werden:
    - alle Produktnamen, die im Titel zwingend vorkommen müssen;
    - Vergleichstyp;
    - Zielkeyword/Suchintent.

    Für einen 2er-Produktvergleich müssen beide exakten Produktbezeichnungen im Titel sichtbar sein. SEO/TEXT darf daraus eine natürliche Form wie „A gegen B im Vergleich“ bilden, darf aber kein drittes Produkt ergänzen oder eines weglassen.

## 3. Fachliche Artikelpflichten

Die spätere Beitragsart PRODUCT_COMPARISON muss fachlich folgende Aufgaben erfüllen:

1. **Entscheidungsfrage klar machen**
   Nicht mit System-/Methoden-Disclaimer beginnen, sondern die reale Nutzerentscheidung erklären.

2. **Vergleich auf einen Blick**
   Eine kompakte Vergleichstabelle mit den entscheidungsrelevanten, belastbar vergleichbaren Merkmalen.

3. **Entscheidende Unterschiede erklären**
   Nicht bloß Tabellendaten wiederholen. Nur Unterschiede erläutern, für die das Dossier eine fachliche Bedeutung bindet.

4. **Bedarf statt künstlicher Gewinnerlogik**
   Wenn belastbar gebunden: welches Produkt passt zu welchem konkreten Bedarf und warum.

5. **Grenzen sichtbar machen**
   Wo Werte nicht sauber vergleichbar sind oder Quellen fehlen/widersprechen, darf daraus kein Vorteil erzeugt werden.

6. **Fazit**
   - kein pauschaler Sieger;
   - kurze Entscheidungshilfe anhand der tatsächlich gebundenen Bedarfszuordnungen;
   - wenn keine Bedarfszuordnung belastbar ist: neutral sagen, welche Unterschiede belegt sind und dass daraus keine allgemeine Präferenz folgt.

## 4. Was ausdrücklich NICHT Pflichtabschnitt ist

Der alte Renderer ist kein Textvorbild.

Nicht automatisch erzeugen:
- leere „Vor- und Nachteile“-Tabellen;
- Sätze wie „Keine freigegebenen Vorteile vorhanden“;
- leere Unterschiedsabschnitte;
- wiederholte System-/Regelhinweise;
- ein eigenes Quellenkapitel ohne konkreten Nutzwert;
- redundante Wiederholung derselben Bedarfszuordnung in Tabelle, Abschnitt und Fazit.

Eine technische Differenz ist nicht automatisch ein Vorteil oder Nachteil.

## 5. Quellen- und Linkgrenze

Quellen/URLs bleiben als Provenance im Dossier gebunden.

Ob und wie Quellen im veröffentlichten Artikel sichtbar gemacht werden, entscheidet der bestehende SEO/TEXT-Vertrag. Das Produktvergleichsbüro erzeugt keinen eigenen externen Linkweg.

## 6. Affiliate-Grenze

Nicht Teil der kanonischen Fachfakten:
- aktueller Preis;
- Händler;
- Lieferbarkeit;
- Provision;
- Affiliate-URL.

Diese Daten dürfen nachgelagert angezeigt werden, aber weder Paarung, Fachurteil noch Fazit verändern.

## 7. Aktualität

Hersteller-/Produktfakten folgen dem Produktwissen-Vertrag.
SEO-Zwischenevidenz folgt der gebundenen 90-Tage-/Kontextregel von UPC 0.8.2.
Dynamische Affiliate-Daten werden separat aktualisiert.

Eine Änderung gebundener Produktfakten markiert betroffene Vergleiche zur fachlichen Nachprüfung; sie darf nicht still mit altem Ruleset weiterproduziert werden.

## 8. Fail-closed-Abnahme

Kein produktionsfähiges Dossier bei:
- unklarer Produkt-/Variantenidentität;
- nicht vergleichbaren Produkten;
- fehlenden erforderlichen Fakten;
- Regel-/Fakten-Hashdrift;
- fehlender Regel für einen relevanten Unterschied;
- unbelegter Bedarfszuordnung;
- SEO nicht geeignet;
- Cannibalization/Readiness BLOCK;
- Dossier-/Abschluss-Audit-Drift;
- Quellenkonflikt an einer für die Entscheidung zwingenden Stelle ohne sichere neutrale Behandlung.

## 9. KISS-Leitsatz

**Das Dossier liefert keine Prosa. Es liefert eine versiegelte Landkarte: Das sind die Produkte, das sind die belegten Unterschiede, das darf daraus gesagt werden, das darf nicht gesagt werden.**
