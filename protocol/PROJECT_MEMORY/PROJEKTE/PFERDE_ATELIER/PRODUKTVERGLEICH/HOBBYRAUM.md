# PRODUKTVERGLEICH – HOBBYRAUM

STAND: 2026-09-07
STATUS: AKTIV / V1-PROTOTYP + ZIP-INSTALLATIONSTEST PASS / MANUELLER WP-TEST BEREIT

## 1-KLICK-ÜBERSICHT

**WAS IST DAS?**
Der einzige aktuelle Arbeitsraum des Büros PRODUKTVERGLEICH.

**AKTUELLER AUFTRAG**
Die zwei geprüften Plugin-ZIPs im ersten manuellen WordPress-Test installieren und aktivieren. Keine Veröffentlichung.

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

## ERSTER ZIP-PLUGINTEST – PASS

Temporärer echter ZIP-Installationssmoke:
- ZIP-Struktur PASS;
- `universal-product-knowledge` per WordPress installiert + aktiviert PASS;
- `universal-product-comparison` danach per WordPress installiert + aktiviert PASS;
- Real WordPress/MySQL Gesamtlauf PASS;
- finales Draft-/Link-/Grafiksystem PASS;
- Publish-Sperre PASS.

Testlauf: `34136786494`.

Finaler Branch nach Entfernen aller temporären Workflow-Dateien:
`38ae1137b5d90d64d28b3f02fc31b85f00ee8375`

`Pferde Atelier Immutable Base Hardlock` -> PASS.

## NEXT ACTION

**Manueller WordPress-Plugintest:**
1. `universal-product-knowledge-0.1.0-prototype.zip` installieren und aktivieren;
2. danach `universal-product-comparison-0.2.0-prototype.zip` installieren und aktivieren;
3. keine Veröffentlichung auslösen;
4. zuerst nur Installation/Aktivierung und eventuelle WordPress-Fehlermeldungen prüfen.

## Globale Arbeitsort-Sperre

Tresor, Archiv, Backup und Git-Mirror sind niemals Werkbank oder Runner-Quelle.
