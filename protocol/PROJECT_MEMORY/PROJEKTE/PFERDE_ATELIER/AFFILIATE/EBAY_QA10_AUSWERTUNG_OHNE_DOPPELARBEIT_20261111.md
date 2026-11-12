# Pferdeatelier eBay – QA10: fehlende Transparenz der Ablehnungen / Backend-Last

**11.11.2026. ISOLIERTE STAGING-ARBEITSKOPIE, NICHT INSTALLIEREN, KEINE FREIGABE.** Grundlage exakt das QA9-Archiv 6.72.321, SHA256 `4a84696bdd10d5c32f3ab5d4e4583fc9029ef673403f43eebfe2217ffd72e47a`. Der Live-Worker, die Datenbank, Kunden- und WordPress-Zugangsdaten, die Hauptseite, alle Fremdportale und der aktuelle Lauf wurden **nicht verändert**.

## Neue nachweisbare Ursache: Der vorhandene CSV-Bericht blendet bereits gespeicherte Gründe aus

Reale Nutzerdaten (CSV `Pferdeatelier_eBay_fehlende_Produktfamilien_3e9e9207-d82.csv`): **138 offene Familien / 1.329 Angebotsvorkommen / 764 als blockiert gezählt / 0 angenommen in genau diesem offenen Teilbestand**. Aus der bisherigen Liste bleiben somit **565 Angebotsvorkommen unaufgeschlüsselt**. Das beweist ausdrücklich **nicht**, dass 565 eindeutige Produkte verlorengegangen sind: Profiltreffer können mehrfach gezählt werden, Kandidaten bleiben offen, Duplikate werden getrennt übersprungen. Die bisherige CSV zeigt diese Zahlen *gar nicht*, obwohl sie im gespeicherten `profile_stats` vorhanden sind.

Der Quellnachweis in `ebay_missing_family_diagnostic_rows` und dem CSV-JavaScript zeigt: Ursprünglich wurden nur `requests`, `received`, `accepted`, `hard_blocked + technical_blocked` und **aggregierte** Ablehnungs-Codes ausgegeben. Die bereits in `ebay_sync_summary_new` vorhandenen Werte `duplicates_skipped`, `review_pending` und `capacity_skipped` wurden ignoriert; außerdem fehlte das Feld `complete` des einzelnen Suchprofils. `ebay_summary_reason_add` speichert nur den Code und seine Häufigkeit. Konkrete ursprüngliche eBay-Angebotstitel oder Negativmarker sind aus **dieser CSV allein** nicht wiederherstellbar. Diese Grenze nicht als „jetzt wissen wir genau, welche 234 Produkte fachlich falsch sind“ verkaufen.

### Schon erledigtes ausdrücklich NICHT wiederholen

- 26 Nicht-Waren/Versicherungen/Services sind aus dem 298er eBay-Warenkatalog bereits herausgenommen; kein neues Versicherungs-Gate.
- Ein im selben Run bereits geprüfter Familienbereich wird von `ebay_run_schedule_new_business_gap_revalidation` nicht erneut gesucht. Erfolglos geprüfte Kategorien dürfen bis zum nächsten regulären Gesamtzyklus als belegte Versorgungslücken offen bleiben.
- Ein dritter Synonymcontroller oder weitere pauschale Wortersetzungen sind nicht nötig; die Kamera-CSV-Ablehnung beruht auf Fachnegativ/Marktplatz, **nicht** auf fehlendem Kamera-Alias.
- Marketplace-Filter `EBAY_DE` bleibt unverändert.
- Gespeicherte Angebote, Materialien, zugeordnete Seiten, Checkpoints, Produktgrundstock, Verlauf, Alter und ursprüngliche Job-Zustände bleiben erhalten.

## Harte Eingrenzung auf 55 Familien aus der echten CSV

| Familie / Grundgruppe | Anzahl |
|---|---:|
| Keine Treffer im begrenzten Suchausschnitt | 43 |
| Ausschließlich bewusster EBAY_DE-Herkunftsfilter | 39 |
| Technischer Abruffehler | 1 |
| Weitere fachliche/technische Annahmegründe – **nur diese vertiefen** | **55** |

Auswertung liegt maschinenlesbar mit **den vollständigen 55 Original-Familienkennungen, Produktnamen, Suchbegriffen, Trefferzahlen und ursprünglichen Gründen** in `EBAY_QA10_55_FAMILIEN_ZIELGRUPPE_20261111.json`. Die Menge 55 ist ein Untersuchungsfokus, **nicht** ein Beweis, dass für alle 55 passende EBAY_DE-Angebote existieren. Die 43 Nulltreffer-Familien sind nicht als grundsätzlich eBay-warelos bewiesen, aber dürfen nicht dauernd neu recherchiert werden.

## Mini-KISS-Änderung in getrennter QA10-Quelle – ausschließlich Auswertung und Backend

**Nur eine Datei:** `affiliate-portal-router/includes/trait-ppar-ebay.php`; alle **65 weiteren von 66** Dateien vollständig bytegleich mit QA9. Kein neuer Worker, keine neue Datenbanktabelle, kein API-Aufruf, keine neue PHP-Methode, keine zusätzliche WordPress-Option, keine Änderung an Suche, Annahmeregeln oder Veröffentlichung.

1. `ebay_missing_family_diagnostic_rows` zeigt die **schon vorhandenen** Familien-Zähler für `duplicates_skipped`, `review_pending`, `capacity_skipped` und unvollständigen Suchprofilstatus als zusätzliche Felder. Die ersten elf CSV-Spalten bleiben in ursprünglicher Reihenfolge; vier neue werden rechts ergänzt. Das verhindert, dass andere Programme die bisherigen Spalten nicht mehr finden.
2. **Backend-Leistungsweg:** Die bisherige volle Katalog-/Profil-Berichtserstellung auf jedem Seitenaufruf – selbst wenn das `<details>`-Element geschlossen war – ist nun **nur auf ausdrücklichen Klick** (`Gespeicherten Bericht bei Bedarf laden`) berechnet. Bestehender Admin-Screen, bestehender Bericht, bestehende CSV, kein neuer Ajax-Aufruf. Normale Admin-Seitenaufrufe rufen die volle Berichtsmethode **nicht** mehr auf. Das ist ein konkreter eliminierten Zusatzlast-Weg; Gesamt-Backend-Beschleunigung auf WordPress ist noch nicht gemessen.
3. **Sicherheitsgrenzen:** Der Bericht ist weiterhin nur lesend; ungültige oder fremde Familienkennungen bleiben gesperrt. Ein URL-Parameter als Array löst keine PHP-Warnung aus. Es werden keine Produkte gelöscht, neu gesucht oder entsperrt.

## Tests der tatsächlich ausgeführten QA9/QA10-Originalmethode

- **23/23** PHP-Dateien der QA10-Stagingquelle Syntax PASS.
- **66/66** ZIP-Quell-Dateien vorhanden, nur **1** Datei geändert, Rest bytegleich.
- `QA10_REPORT_REAL_SOURCE_TEST.php`: führt die **echte private Berichtsmethode** der ursprünglichen QA9-Quelle und der QA10-Arbeitskopie via PHP-Trait aus. Alter Bericht mit 298 Pflichtfamilien und unveränderten bisherigen Zahlen PASS; neuer Bericht zusätzlich **13 Duplikate, 4 Review, 2 Kapazität, einen unvollständigen Teilabschnitt**, alle ursprünglichen Angaben unverändert. Ungültige Familien-ID fail-closed.
- `QA10_REPORT_LAZY_REAL_CODE_TEST.php`: führt das aus dem tatsächlichen PHP-Template **ausgeschnittene Originalstück** in 6 URL-Szenarien aus: ohne Parameter / abweichender Parameter / Parameter als Array => **0 Berichtsberechnungen**; nur `?ppar_ebay_report=1` => **ein** Bericht auf ausdrückliche Anforderung.
- **Nicht bestanden / offen:** realer WordPress+MariaDB+eBay-Gesamtlauf, Veröffentlichung der eBay-Kacheln, tatsächliche Ladezeitmessung und genaue Zuordnung der schon abgelehnten realen eBay-Artikeltitel. Deshalb **kein neues installierbares Plugin und keine Release-Aussage**.

## Fachliche Fortsetzung ohne erneut bei null anzufangen

Beim **bereits gespeicherten** Kandidatenbestand beginnen, niemals erneut eine pauschale 298er Suche. Durch neue transparente Zähler kann der nächste tatsächliche Bericht die 55 untersuchungswürdigen Familien ehrlicher nach Duplikat/Review/Auswahlstatus trennen. Die tatsächlichen pro-Artikel-Negativmarker, die in der bestehenden Aggregation nicht gespeichert sind, dürfen aus den alten CSV-Zählern **nicht erfunden** werden. Wenn weitere Änderungen nötig werden, erst nach Vorlage echter Angebotsdetails oder nach direkt am Quellcode bewiesenem Regelwiderspruch – nicht als neuer Synonym- oder Suchmaschinen-Umbau.

**GitHub:** Separater QA-Branch/PR #748 für Pferdeatelier; Änderungsregister-PR #751 für Hobbydepot und Hab & Bewahr. Keine direkte Änderung am geschützten Campus, keine Fremdplugin-Übernahme.