# Wassertechnik W17 – breiter neuer Recherchegang und zentrales Produkt-/Glossar-/Anbieter-Verzeichnis
**Stand 15.11.2026. Tatsächlich abgelegter und geprüfter Forschungsstand, keine WordPress-Änderungen.**

## 1. Das Problem wurde an der Quelle gelöst
Bis einschließlich W16 waren **230 Produktbezeichnungen** vorhanden. Die historischen W4–W16-Dateien hatten jedoch teils andere Datenfelder für Produkte, Kategorien und Recherchebewertungen. Das war für spätere Filter von Glossar, Produktverzeichnis und Anbieterregister ungeeignet und begünstigte wieder doppelte Einträge.

**W17 besitzt jetzt EINEN schreibfreien zentralen Registerbestand:**
`W17_ZENTRALES_FACHREGISTER_V1_20261115.json`
W4/W5/W6/W7 und der W16-Forschungsstand bleiben als historische Quellen/WordPress-Autorität erhalten; nur dieses W17-Register ist die aktuelle gemeinsame **Recherche-/Terminologie-Arbeitsliste**. Keine neue Pluginidentität oder doppelte Datenpflege.

## 2. Nachweisbar recherchierte neue Produktarten
**28** zusätzliche, zuvor nicht namensgleich vorhandene Produktarten/Anlagensysteme mit Hersteller-/Fachquellen und **genau einer fachlich formulierten möglichen Inhaltskategorie mit mindestens drei konkret unterschiedlichen Artikeln je Produkt** (= 28 Kategorien, 84 Artikelrichtungen). Fundliste `W17_NEUE_FACHRECHERCHE_28_PRODUKTE_20261115.json`. Auswahl:
- **Gewerbliche Wasserwiederverwendung:** Fahrzeugwaschwasser-Recyclinganlage, Waschwasser-Hydrozyklon. Hersteller https://www.kaercher.com/de/de/professional/produkte/wasserrecycling-c231 . Der Hydrozyklon kann Bestandteil der Gesamtanlage sein, daher zunächst Grenzfall, keine zweite Seite allein wegen Baugruppenbezeichnung.
- **Lebensmittel und Hygiene:** CIP-Reinigungsstation, Wasser-/Spülmedien-Leitfähigkeitsmesssystem. Hersteller/Fachbelege https://www.alfalaval.com/de/products/process-solutions/brewery-solutions/cip-modules/cip-station/ ; https://www.knick-international.com/de/prozessanalytik/branchenloesungen/ueberwachung-von-cip-sip-prozessen/ .
- **Labor- und Gebäudetechnik:** Laborwasseranlagen Typ 1 und Typ 2; hygienespezifische Befeuchtungswasseraufbereitung und Hochdruckbefeuchtung als bewusst abgegrenzte Randfälle. Quellen https://www.merckmillipore.com/DE/de/products/water-purification/type-1/milli-q-iq-7003-7005-7010-7015/sPWb.qB.epcAAAFmBrUSP0Vj%2Cnav ; https://www.hygromatik.com/de/wasseraufbereitung ; https://www.condair.de/de/unternehmen/nachrichten/condair-vita-neues-system-fur-die-direkt-raumluftbefeuchtung .
- **Industrie:** Ionenaustauscher-/Spülwasserkreislauf, Metallrückgewinnung, Wasserstoffelektrolyse-Reinstwasser als möglicher **Anwendungsüberschneidungsfall** mit W4 EDI/Industrie-RO. Belege https://decker-vt.de/produkte/ionenaustauscheranlage/ ; https://www.agw.de/anlagenbau/recyclingverfahren/ ; https://www.envirofalk.com/produkte/greenpure-ptx/ .
- **Wasserleitungs-Lecksuche:** akustische Suchgeräte, Korrelatoren, Geräuschlogger, Leitungslageortung. Quelle https://www.sewerin.com/produkte/wasser . Nicht mit bloßem automatischem Leckageschutzventil gleichsetzen.
- **Dampf/Kesselwasser:** Kondensatrückspeiseanlagen, Kesselspeisewasserentgasung. Quellen https://www.gestra.com/global/de-DE/products/system-and-packaged-solutions/condensate-return-unit ; https://ebooks.spiraxsarco.com/view/77532886/22/ .
- **Analytik:** Online-TOC, Schlammspiegel, Ammonium, Phosphat, Redox-Messung und Multiparameter-Trinkwasserpanel; Herstellerverzeichnis https://www.endress.com/de/messgeraete-fuer-die-prozesstechnik/fluessigkeitsanalyse-produktuebersicht . Einige Gerätevarianten können dem bereits vorhandenen Multimessgerät zugeordnet sein.
- **Spezialabwasser:** Membranbioreaktor-Kompaktanlage, größerer Abwasserwärmetauscher, Sandklassierer und AOP-UV/H2O2-Anlage. Belege https://www.huber-se.com/de-de/anwendungen-loesungen/detail/membran-belebungsverfahren/ ; https://www.huber-se.com/de-de/produkte/detail/huber-abwasserwaermetauscher-rowin/ ; https://www.huber-se.com/de-de/anwendungen-loesungen/detail/sand-fett-abscheidung/ ; https://www.almawatech.com/alma-oxi-uv/ .
- **Neue Technik:** 172-nm-Photolysereaktor aus dem Fraunhofer-Prototypumfeld **ausdrücklich als Prototyp**, nicht als kaufbares Serienprodukt. Direktquelle https://www.cbp.fraunhofer.de/content/igb/de/forschung/greentech-solutions/wasser-abwasser/photolyse.html .

**Aufnahme-Regel:** Echte Produkttypen sind kein automatischer SEO-Owner. **17** der 28 Namen als zunächst fachlich eigenständige Kandidaten, **10** als Funktions-/SEO-Grenzfälle, **1** als Prototyp/Forschungsstand. Google-SERP und Affiliate-Verfügbarkeit nicht gemessen. Keine neuen kostenpflichtigen Datenabfragen.

## 3. Ein Datensatzformat für Produkt, Glossar und Anbieter-Rubrik
`W17_DATENVERTRAG_EIN_REGISTER_20261115.md` definiert ein gemeinsames Grundschema für ALLE Einträge: stabile ID, Eintragstyp, Name, Beschreibung/Definition, Synonyme, kanonische ID für Aliase, Fachbereich, gleiche Filtermerkmale, Status, Technikstand, Quellen mit URL, SEO-Owner/Status, produktbezogene Inhaltskategorien, verwandte Einträge und Aktualisierungsdatum. Vier festgelegte Kernfilter in Arrays: **Funktion, Wasserart, Einsatz, Zielgruppe**. Weitere Merkmale können später in genau diesem zentralen Vokabular ergänzt werden, nicht als neue Paralleldatenbank. Bei unbekannten Merkmalen bleibt ein leeres Array bzw. null; 230 alte Bezeichnungen haben häufig nur aus Titel/Quellbereich *vorläufig* ermittelte Schlagwörter.

**39 konkret formulierte Glossarbegriffe** mit kurzen Erklärungen und Quell-URLs, davon 21 bereits mit einem eindeutigen Produkt-Eintrag verknüpft. Beispiele: CIP, Ionenaustausch, Typ-1-Reinstwasser, Membranbioreaktor, Schlammspiegel, TOC, AOP, Leckagekorrelation und Kondensatrückführung.

**16 Anbieterrubriken** als künftige HivePress-Struktur. Das sind Rubriktypen, **keine echten oder überprüften Betriebe**: beispielsweise Wasseranalyselabore, Pumpenwartung, Leckortungsdienst und Bewässerungsplanung. Keinerlei erfundene Firmenadressen oder Ratings.

## 4. Gemessene Projektzahlen und Qualitätstest
| Registerstand | Zahl |
|---|---:|
| Alte W16-Produktbezeichnungen | 230 |
| Neue W17-Produktbezeichnungen | 28 |
| **Produktbezeichnungen gesamt** | **258** |
| Glossarbegriffe | 39 |
| Anbieterrubrik-Vorschläge | 16 |
| **Einheitliche Registereinträge** | **313** |
| Bereits bekannte Funktionsalias-Beziehungen | 3 |
| Bereits bestehende W4-Fachproduktowner | 79 |
| W4-Produktowner mit schon gemessenem W5-Suchvolumen | 59 |
| W4-Produktowner ohne gelieferten W5-Wert | 20 |
| W17 vorgeschlagene Kategorie-/Einzelartikelrichtungen | 28 / 84 |

Die 258 Produktnamen sind **keine** 258 unterschiedlichen SEO-Seiten: 3 kanonisch erkannte Aliasnamen plus zahlreiche fachlich noch offene Grenzfälle. W17-Inhalt: **313/313 identische Grundfeldstrukturen**, eindeutige IDs, alle Filterwerte aus zentralem Vokabular, kanonische/Glossar-Verweise zeigen auf echte Register-IDs; **28/28 neue Produkte haben mindestens drei verschiedene Artikelansätze in ihrer jeweils vorgeschlagenen Kategorie**. Die alten 79 W4-Fachprodukte wurden **79/79** exakt mit dem bereits gemessenen W5-SEO-Datensatz verbunden, Suchvolumen real für **59/79**. Die übrigen 20 bedeuten **nicht** null Suchnachfrage, sondern keine Anbietermesszahl. Keine neue DataForSEO-Recherche.

**Echte Filter-Beispiele aus der gespeicherten Datei:**
- `funktion=messen & wasserart=trinkwasser` findet u.a. Trinkwasser-Labortestset, Wasserleckortungsgeräte, Redox-Sensoren und die Glossar-Erklärung Leitfähigkeit.
- `funktion=wiederverwenden & wasserart=prozesswasser` findet u.a. Galvanik-Spülwasserkreislauf, Kondensatrückspeiseanlage sowie den passenden Glossar-/Anbieterkontext.
- Die Filter können auf `typ=produkt`, `typ=glossar` oder `typ=anbieterrubrik` eingeschränkt werden.

## 5. Was NICHT abgeschlossen ist
- Die erstmalige Forschungsbreite W13–W17 belegt **keine absolute Marktvollständigkeit**. Neue und historische Forschungsnamen müssen noch **funktional** abgeglichen werden (auch bei unterschiedlichen Begriffen). W17 hat die drei schon bekannten Aliase übernommen, **nicht** sämtliche unklaren Fälle entschieden.
- Zu vielen Altbestandsprodukten fehlen geprüfte Detailmerkmale/Herstellerbelege; diese Felder sind offen gekennzeichnet statt fiktiv ergänzt.
- **Neue konkrete Produktseiten, endgültige Anzahl 6–8 Hauptkategorien, Mega-Menü und tatsächliche WP-Freigabe** sind NICHT Teil von W17. Der bisher sichtbare 7er-WP-Stand bleibt unverändert.
- Ein Live-Frontend für Register/Glossar ist nicht programmiert. Der Datenbestand ist die **schreibfreie Grundlage für spätere Filter**, keine veröffentlichte Website-Suchoberfläche.

## 6. Nächster einheitlicher Arbeitsschritt
Jetzt mit dem **einen W17-Register** weiter recherchieren, doppelte Funktionen zusammenfassen, Quell-/Filterlücken des Altbestands gezielt füllen und nur nach nachgewiesenen unterschiedlichen Produktfunktionen und wenigstens drei möglichen Artikeln je produktbezogener Kategorie neue Endseiten im Schlussbaum zulassen. 6–8 Hauptmenüpunkte erst nach fachlichem Abgleich. Danach **eine** technische Übergabe ans vorhandene WT001 nach ausdrücklicher Schreibfreigabe; kein neues Mini-Plugin für die Recherche.

**KISS:** Ein Register, ein kontrolliertes Vokabular, ein kanonischer Owner je Technikfunktion, eine spätere Freigabe. STATUS AKTIV / RECHERCHE WEITER OFFEN / WP LIVE WRITE NEIN / BEZAHLTE SEO KOSTEN NEIN.