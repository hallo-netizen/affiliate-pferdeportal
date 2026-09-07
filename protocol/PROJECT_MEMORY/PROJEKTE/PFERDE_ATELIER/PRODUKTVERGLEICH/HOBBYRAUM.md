# PRODUKTVERGLEICH – HOBBYRAUM

STAND: 2026-09-07
STATUS: AKTIV / V1-PROTOTYP TECHNISCH PASS / ERSTER PLUGINTEST VORBEREITUNG

## 1-KLICK-ÜBERSICHT

**WAS IST DAS?**
Der einzige aktuelle Arbeitsraum des Büros PRODUKTVERGLEICH.

**AKTUELLER AUFTRAG**
Den isolierten allgemeinen V1-Prototyp als installierbare WordPress-Plugins für den ersten manuellen Plugintest vorbereiten.

**DU DARFST NICHT**
STARTMASTER/TEXT umbauen, dessen aktiven Reparaturbereich verändern, Produktfakten erfinden, Affiliate-/SEO-Daten zur fachlichen Produktwahrheit machen oder automatisch veröffentlichen.

## AKTUELLER BELASTBARER TECHNISCHER STAND

Branch:
`hobbyroom/productwissen-v1-prototype`

Letzter technisch geprüfter Stand:
`109890eb7762bac276bc3f42be618e161b003f57`

GitHub Actions:
`Product Knowledge WordPress DB Smoke` -> PASS

Belegt:
- Produktwissen: Produkt, Variante, Identifier, Herstellerfakt, Quelle, Readback, Negativsperren;
- Produktvergleich: 2–4 Produkte, mindestens zwei Hersteller, Variantenvergleich nur gleicher Basistyp;
- gebundener Zero-Freedom-Writer;
- reales Dossier `PV-REG-001`;
- 100/100 byte-identische Writer-Renders;
- WordPress-DRAFT-Materialisierung und Readback;
- SEO nur read-only Signale;
- Affiliate nur GTIN/EAN/echte MPN; Hersteller-Artikelnummer ausgeschlossen;
- Vergleichsarchiv mit Produktgruppen-/Produkt-/Variantenansicht;
- deterministisches Link-Manifest Produktvergleich <-> Variantenvergleich;
- neutraler SVG-Vergleichsgrafikgenerator ohne Produktbilder/Logos/externe Assets;
- 20/20 byte-identische Vergleichsgrafiken;
- finaler WordPress-DRAFT mit gebundenen Links + Grafik + Endhash;
- `publish_allowed=false` bleibt hart erhalten.

## AKTUELLER VERTRAG

Produktwissen:
`PRODUKTWISSEN_V1_VERTRAG.md`

V1-Rollen:
- Produktwissen = Produkt-/Varianten-/Fakten-/Quellen-/Lebenszyklus-Wahrheit;
- Produktvergleich = Vergleichsauswahl, Vergleichsartikel, Variantenvergleich, QA, Grafik, Archiv, interne Verlinkung, WordPress-DRAFT;
- SEO = optionale read-only Signale/Priorisierung;
- Affiliate = Exact-Match + Kaufangebote/Preise/Verfügbarkeit;
- TEXT/STARTMASTER = keine V1-Laufzeitabhängigkeit.

## NEXT ACTION

**Ersten echten Plugintest vorbereiten:**
1. `universal-product-knowledge` als installierbares ZIP paketieren;
2. `universal-product-comparison` als installierbares ZIP paketieren;
3. Installationsreihenfolge hart festhalten: Produktwissen zuerst, Produktvergleich danach;
4. ZIP-Inhalt prüfen: genau ein Plugin-Root, keine Repo-/Test-/Campus-Altlasten außerhalb des Pluginordners;
5. keine Live-Veröffentlichung; erster Test endet bei WordPress-DRAFT.

## Globale Arbeitsort-Sperre

Tresor, Archiv, Backup und Git-Mirror sind niemals Werkbank oder Runner-Quelle.
