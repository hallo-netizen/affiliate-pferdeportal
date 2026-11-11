# Pferdeatelier eBay – QA20: echte Angebotstitel, Freigabestand und sichtbare Ausgabe

Stand 11.11.2026. **Beobachtung / Prüfnachweis, kein Live-Update, keine neue Pluginversion.**

## 1. Originale Laufdaten (hochgeladener vollständiger CSV-Export)

- Gleicher Run `09c34988-7c9f-4090-945c-fdcff6b3393e`: Ereignis 1417 (`public_checkpoint_saved`, Phase `gapfill_select`): **493 BUSINESS-Kampagnen öffentlich freigegeben, 147/298 Familien abgedeckt**.
- Ereignis 1481 (`public_checkpoint_saved`, Phase `public_verify`): **365 BUSINESS-Kampagnen öffentlich freigegeben, 161/298 Familien abgedeckt**.
- Unterschied: **128 weniger in der Freigabeliste**, aber **14 weitere Produktfamilien** abgedeckt. Die Event-Datei enthält **keine vollständigen IDs beider Freigabelisten**. Deswegen sind diese 128 **nicht** als verlorene oder widerrechtlich gelöschte Daten belegt. Eine geänderte, enger auf Familien verteilte Auswahl ist mit den Zahlen vereinbar, aber **nicht bewiesen**.
- Der abgeschlossene Lauf erreichte `completed` und der Folgelauf `refresh_remote`. Die alte Sollzahl 298 stammt vom damaligen Produktionslauf, nicht vom noch nicht installierten QA18-/QA19-Stand mit 283 Zielen.

## 2. Echte, öffentlich gelistete eBay-Angebotstitel am QA19-Originaltrait getestet

Getestet mit dem **wirklichen unveränderten QA19-PHP-Klassifikator**, nicht mit nachgebauter Erkennung. Die Titel stammen aus öffentlich sichtbaren eBay-Listings, **nicht** aus der privaten Browse-API oder dem WordPress-Datenbestand.

| Echte Angebotsbezeichnung | QA19-Klassifikation | Wertung |
|---|---|---|
| `LED-Rückleuchten Pferdeanhänger Beleuchtung Trailer Earpoint 5M Kabelbaum 13 pol` | Anhängerbeleuchtung, 92 Punkte | passende Ware erkannt |
| `Reitbahnplaner Reitplatzplaner 1,5 m PADDOCK EGGE 1500 mm ATV QUAD Pferde` | Reitplatzschleppe 90, Reitplatzplaner 100 | Mehrfachgruppe fachlich plausibel erkannt |
| `Kabellose Rückfahrkamera mit Monitor Magnetische Mount für PKW, Anhängerkupplung` | nicht als Anhängerkamera freigegeben | Fremdprodukt ohne gesicherten Pferdeanhänger-Bezug nicht übernommen |
| `Rückfahrkamera für Anhänger Brian James Trailer oder z.B. Böckmann Digi Max 4` | Anhängerkameras 90 | Titel fachlich klassifiziert, **Listing privat und daher nach BUSINESS-Regel trotzdem nicht freizugeben** |

Marktquellen: https://www.ebay.de/itm/166851846902 ; https://www.ebay.de/itm/155325083557 ; https://www.ebay.de/itm/374429215108 ; https://www.ebay.de/b/Bockmann/bn_21820962 .

- QA19-Sicherheitstest danach erneut ausgeführt: **1711/1711 PASS**.
- Der vollständige sichere eBay-Akzeptanzpfad (Marketplace-ID, Verkäuferstatus, Frische, Partner-URL etc.) wurde mit diesen Webseite-Titeln **nicht** bestätigt. Ein sichtbarer eBay-Kaufartikel ist nicht automatisch ein von der Browse-API geliefertes und im Pferdeatelier freigegebenes Partnerprodukt.

## 3. Öffentliche Pferdeatelier-Seite

- https://pferde-atelier.de/ausruestung/ausruestung-sattel/schabracken/ zeigte im öffentlich abrufbaren Seitentext die Überschriften „Ausgewählter Partner“ und „Produktvorschläge“, darunter jedoch **keine ausgelesenen Produktkarten oder eBay-Links**. Das ist ein **negativer HTML/Text-Befund für diese eine Seite**, kein Nachweis für alle Seiten und kein Browser-/Datenbank-End-to-End-Test. Dynamisch nachgeladene Elemente sind damit nicht ausgeschlossen.

## 4. Die konkrete Lücke für die nächste Ausführung

Die drei bereitgestellten Run-Exports enthalten **keine gespeicherten Original-Angebotstitel pro abgelehntem Artikel, keine kompletten checkpoint-IDs-Listen und keine WordPress-Kampagnen/Seitenzuordnungen**. Mit ihnen lässt sich weder das vollständige Re-Routing aller bereits gespeicherten Kandidaten noch der tatsächliche Grund der 128 Freigabelisten-Differenz beweisen.

**Nächster notwendiger EINMAL-Prüflauf (vor Änderungen am Live-System):** Im isolierten WordPress-Test die bereits gespeicherten eBay-Quellen und Kampagnen unverändert lesen, mit **QA19** durch den vorhandenen einen Klassifikator erneut einordnen, bisherige/neu freigegebene IDs und Familien nebeneinander vergleichen und für jede freigegebene Familie die wirklich sichtbare Kachel auf der Seite nachweisen. Nur nachweislich sichere, gewerbliche `EBAY_DE`-Artikel dürfen erscheinen. Keine erneute 283er Vollsuche, keine neue Logik, keine Löschung, keine neue Pluginversion auf Verdacht.

Prüfskript: `qa19_real_titles.php` (QA19-Trait mit 5 echten öffentlichen Angebots-Titeln), dazu `EBAY_QA20_REALDATEN_UND_CHECKPOINT_20261111.json` mit zählbaren Fakten.