# PRODUKTVERGLEICH – HOBBYRAUM

STAND: 2026-09-07
STATUS: AKTIV / 0.2.4 ECHTER WP-ADMIN-MENÜTEST + ERSTDRAFT PASS / MANUELLER TEST BEREIT

## 1-KLICK-ÜBERSICHT

**WAS IST DAS?**
Der einzige aktuelle Arbeitsraum des Büros PRODUKTVERGLEICH.

**AKTUELLER AUFTRAG**
Produktwissen 0.1.0 unverändert lassen, Produktvergleich durch den hart geprüften Clean-ZIP-Stand 0.2.4 ersetzen und danach ausschließlich den gebundenen PV-REG-001-Admin-Test ausführen. Keine Veröffentlichung.

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

## 0.2.2 – GEBUNDENER ERSTDRAFT PASS

Neu:
- hashgebundenes Live-Dossier `PV-REG-001`;
- idempotenter Erstimport: exakt 2 Produkte, 28 Fakten, 1 Vergleich, 14 Merkmale;
- Wiederholung erzeugt keine Dubletten;
- Admin-Seite unter Werkzeuge -> Produktvergleich Test;
- genau ein gebundener Knopf: `PV-REG-001 als Draft testen`;
- kein freier Titel, Body, Produkt, Kategorie oder Ruleset;
- Ablauf: Import -> gebundener Core-Draft -> Link-/Grafikfinalisierung;
- Draft bleibt `publish_allowed=false`.

Harter Clean-ZIP-Test:
- Run `34144140088` -> PASS;
- Clean-ZIP enthält **kein** `config/test-project`;
- ZIP-Installation/Aktivierung -> PASS;
- vollständige alte Regression -> PASS;
- frische Datenbank -> gebundener Erstimport -> PASS;
- exakte Kategorie Term-ID 11 -> PASS;
- erster echter gebundener `PV-REG-001` WordPress-Draft -> PASS;
- Wiederholung ohne Produkt-/Vergleichs-/Post-Dublette -> PASS;
- Marker: `UPC_BOUND_LIVE_PV_REG_001_GESAMT_PASS`.

Freigegebene ZIP:
`universal-product-comparison-0.2.2-prototype.zip`
SHA-256:
`683828e03bd4949aa022ccd25fa62ae7ede105ef3921db2e6d0899b66bf29c67`

## 0.2.4 – ECHTER WORDPRESS-ADMIN-MENÜTEST PASS

Korrektur eines Prüfungsfehlers:
- der 0.2.3-Test rief `register_menu()` künstlich direkt auf;
- damit war nur bewiesen, dass die Funktion einen Menüeintrag erzeugen *kann*;
- nicht bewiesen war, dass sie im echten WordPress-Admin-Lebenszyklus tatsächlich erscheint.

Fix 0.2.4:
- Admin-Hooks werden immer registriert;
- Hauptmenü wird im echten `admin_menu`-Hook sehr spät mit Priorität `99999` gesetzt;
- keine Änderung an Writer, Fakten, Import, Kategoriebindung oder Publish-Sperre.

Harter Realtest:
- Run `34154550626` -> PASS;
- Clean-ZIP-Struktur -> PASS;
- Installation + aktiv -> PASS;
- echter WordPress-HTTP-Server gestartet;
- echter Admin-Login durchgeführt;
- echte `/wp-admin/`-Sidebar gerendert;
- `Produktvergleich` als Top-Level-Menü im HTML vorhanden -> PASS;
- echte Menüseite `admin.php?page=upc-first-draft-test` geladen -> PASS;
- gebundener PV-REG-001-Draft weiterhin -> PASS.

Freigegebene ZIP:
`universal-product-comparison-0.2.4-prototype.zip`

SHA-256:
`b74e3c17eb2cb71ebc4c15aab5da6e4133379b124804c920080a33d20fc78054`

## NEXT ACTION

1. Produktwissen `0.1.0` nicht anfassen;
2. Produktvergleich `0.2.4-prototype` über die installierte Version ersetzen;
3. WordPress neu laden;
4. links in der Hauptnavigation muss **Produktvergleich** sichtbar sein;
5. dort `PV-REG-001 als Draft testen` einmal klicken;
6. Draft öffnen und gemeinsam prüfen; nichts veröffentlichen.

## Globale Arbeitsort-Sperre

Tresor, Archiv, Backup und Git-Mirror sind niemals Werkbank oder Runner-Quelle.
