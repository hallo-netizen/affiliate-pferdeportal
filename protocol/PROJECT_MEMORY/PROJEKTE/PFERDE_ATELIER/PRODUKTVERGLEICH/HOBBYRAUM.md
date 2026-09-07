# PRODUKTVERGLEICH – HOBBYRAUM

STAND: 2026-09-07
STATUS: AKTIV / KATEGORIEBINDUNGSFIX 0.2.1 ZIP-PASS / MANUELLER ERSETZUNGSTEST BEREIT

## 1-KLICK-ÜBERSICHT

**WAS IST DAS?**
Der einzige aktuelle Arbeitsraum des Büros PRODUKTVERGLEICH.

**AKTUELLER AUFTRAG**
Das bereits installierte Produktwissen 0.1.0 unverändert lassen und nur das installierte Produktvergleich-Plugin 0.2.0 durch den hart geprüften Ersatz 0.2.1 ersetzen. Keine Veröffentlichung.

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

## ZIP- UND KATEGORIEBINDUNG – AKTUELLER PASS

Altstand:
- Produktwissen `0.1.0-prototype` unverändert;
- Produktvergleich `0.2.0-prototype` war ZIP-technisch PASS, hatte aber für Pferde Atelier eine falsche Taxonomie-Annahme: echte Vergleichskategorien sind technisch flach (`parent=0`).

Realer Kategorienachweis für ersten Test:
- Term-ID: `11`;
- Name: `Vergleich Regendecken`;
- Slug: `pferdedecken-regendecken-vergleich`;
- Parent: `0`.

Fix:
- Produktvergleich `0.2.1-prototype`;
- reale Kategoriebindung ist hashgebunden;
- Term-ID/Name/Slug/Parent werden exakt geprüft;
- bestehende Live-Kategorie wird **nicht** automatisch neu angelegt;
- unerwarteter Parent wird BLOCKED.

Harter ZIP-/WordPress-/MySQL-Test:
- Run `34141063395` -> PASS;
- Zero-Freedom Static Guard -> PASS;
- saubere ZIP-Struktur -> PASS;
- ZIP-Installation/Aktivierung -> PASS;
- reale Pferde-Atelier-Regendecken-Konfiguration -> PASS;
- flache Kategorie positiv -> PASS;
- falscher Parent negativ -> BLOCKED/PASS;
- Produktwissen-/Vergleich-/Realdossier-/Archiv-Gesamttests -> PASS.

Bereinigter Branch nach Entfernen des temporären Testworkflows:
`89651722cae1fd2c60ddc8a9d288a3d17e71e105`

Immutable Base Hardlock -> PASS.

Wichtig:
Der beim Nutzer bereits installierte `0.2.0`-Stand führt von selbst keine Artikelproduktion oder Veröffentlichung aus. Er bleibt bis zum manuellen Ersatz unangetastet.

## NEXT ACTION

**Manueller Ersetzungstest in WordPress:**
1. Produktwissen `0.1.0` **nicht anfassen**;
2. Produktvergleich `0.2.1-prototype` über das bestehende `0.2.0` installieren/ersetzen;
3. aktiv lassen/aktivieren;
4. noch keinen Beitrag erzeugen oder veröffentlichen;
5. zuerst nur prüfen: WordPress akzeptiert den Ersatz ohne Fehlermeldung und zeigt Version `0.2.1-prototype`.

Erst nach diesem manuellen Installations-PASS folgt der erste gebundene `PV-REG-001`-Draft-Test gegen die reale Kategorie ID 11.

## Globale Arbeitsort-Sperre

Tresor, Archiv, Backup und Git-Mirror sind niemals Werkbank oder Runner-Quelle.
