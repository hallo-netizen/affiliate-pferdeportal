# PRODUKTVERGLEICH – HOBBYRAUM

STAND: 2026-09-07
STATUS: AKTIV / V1-PLUGINPLANUNG

## 1-KLICK-ÜBERSICHT

**WAS IST DAS?**  
Der einzige aktuelle Arbeitsraum des Büros PRODUKTVERGLEICH.

**AKTUELLER AUFTRAG**  
V1 als unabhängigen, allgemeingültigen Produktwissen-/Produktvergleichsweg bis WordPress-DRAFT vorbereiten.

**DU DARFST NICHT**  
STARTMASTER/TEXT umbauen, dessen aktiven Reparaturbereich verändern, Produktfakten erfinden oder Affiliate-/SEO-Daten zur fachlichen Produktwahrheit machen.

## AKTUELLER VERTRAG

Produktwissen:
`PRODUKTWISSEN_V1_VERTRAG.md`

V1-Rollen:
- Produktwissen = Produkt-/Varianten-/Fakten-/Quellen-/Lebenszyklus-Wahrheit;
- Produktvergleich = Vergleichsauswahl, Vergleichsartikel, Variantenvergleich, QA, Grafik, Template, WordPress-DRAFT;
- SEO = optionale Signale/Priorisierung;
- Affiliate = Exact-Match + Kaufangebote/Preise/Verfügbarkeit;
- TEXT/STARTMASTER = keine V1-Laufzeitabhängigkeit.

## NEXT ACTION

**Ersten minimalen Produktvergleichskern auf den jetzt WordPress-/DB-geprüften Produktwissen-Kern setzen:**
1. Vergleich besitzt eigene stabile `comparison_id`;
2. Produktvergleich = 2–4 Produkte, mindestens zwei Hersteller;
3. alle Produkte müssen derselben Produktgruppe angehören;
4. Variantenvergleich = 2–4 Varianten desselben Basismodells;
5. Dubletten und unzulässige Paarungen fail-closed blockieren;
6. Vergleich speichert nur Produkt-/Varianten-IDs und eigene Vergleichsmetadaten, **keine Kopie der Produktfakten**;
7. vollständiges Readback aus PRODUKTWISSEN positiv/negativ prüfen.

Technik-Branch bleibt:
`hobbyroom/productwissen-v1-prototype`.

Produktwissen WordPress/MySQL:
`UPK_WORDPRESS_DB_GESAMT_PASS` / Run `34108014923`.

Noch **kein Writer, kein Frontend, keine Affiliate-Integration**. Erst Vergleichskern beweisen.

## Globale Arbeitsort-Sperre

Tresor, Archiv, Backup und Git-Mirror sind niemals Werkbank oder Runner-Quelle.
