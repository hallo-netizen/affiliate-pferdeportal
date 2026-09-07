# PRODUKTVERGLEICH – HOBBYRAUM

STAND: 2026-09-07
STATUS: AKTIV / V1-PLUGINENTWICKLUNG

## 1-KLICK-ÜBERSICHT

**AKTUELLER AUFTRAG**  
V1 als unabhängigen, allgemeingültigen Produktwissen-/Produktvergleichsweg bis WordPress-DRAFT entwickeln.

**HARTE GRENZEN**
- STARTMASTER/TEXT nicht umbauen;
- keine Produktfakten erfinden;
- SEO/Affiliate schreiben keine Produktwahrheit;
- kein main, kein Live-Publish.

## BELEGTER STAND

Technik-Branch:
`hobbyroom/productwissen-v1-prototype`

Draft-PR:
#142 gegen Campus-Branch.

PASS:
- `UPK_WORDPRESS_DB_GESAMT_PASS`;
- `UPC_WORDPRESS_DB_GESAMT_PASS`;
- `UPC_REAL_DOSSIER_PV_REG_001_PASS`;
- letzter belegter WordPress+MySQL Run: `34109264265` SUCCESS.

Damit sind Produktwissen, Vergleichspaarung, Merkmalsmatrix und deterministisches Writer-Dossier real gegen WordPress+MySQL geprüft.

## NEXT ACTION

**Vergleichsarchiv als dünne, read-only Frontendschicht auf bestehende WordPress-Beiträge setzen.**

Pflicht:
1. Produkt-/Variantenvergleiche ausschließlich über ihre gebundenen UPC-Metadaten erkennen;
2. Produktgruppenvergleiche erst anbinden, wenn ihr bestehender WordPress-Artikeltyp-Marker real belegt ist – nichts erfinden;
3. Hauptfilter: Alle | Produktgruppenvergleiche | Produktvergleiche;
4. innerhalb Produktvergleiche: Produkte | Varianten;
5. Produktindex zeigt nur Produkte mit vorhandenem Vergleich;
6. Produktsuche liefert Produkt- und Variantenvergleiche;
7. Filter/Search verändern keine Beiträge und erzeugen keine indexierbaren SEO-Duplikate;
8. Design nur über Klassen/Contract konsumieren, DESIGN nicht technisch umbauen.

Affiliate Exact-Match:
PASS / Run `34131779064`.

SEO:
bewusst keine V1-Laufzeitkopplung, bis der echte SEO-Vertrag geprüft ist.

## Globale Arbeitsort-Sperre

Tresor, Archiv, Backup und Git-Mirror sind niemals Werkbank oder Runner-Quelle.
