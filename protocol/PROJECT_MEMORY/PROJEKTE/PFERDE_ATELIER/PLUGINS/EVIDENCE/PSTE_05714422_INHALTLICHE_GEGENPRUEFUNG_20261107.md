# PSTE 0.57.144.22 — unabhängige inhaltliche Gegenprüfung (07.11.2026)

**Status: NICHT ZUR WORDPRESS-INSTALLATION FREIGEGEBEN.** Die bisherigen 23/23 automatischen Positiv-/Negativtests haben konkrete inhaltliche Gegenbeispiele nicht abgedeckt. In diesem Prüfauftrag wird keine weitere Plugin-Version erstellt und kein K0/PSERC geändert.

## Gesicherte Prüfgrundlage
- Original: 100 WordPress-MINI-Einträge, darunter **87 JA**, 9 VIELLEICHT, 4 NEIN. Alle **87** JA-Quellsuchanfragen und gespeicherten Titel wurden 1:1 gegen den bestehenden 87er-Fixture-Abzug abgeglichen.
- Bestehender Original-WordPress-Bericht v21, Stand 2026-11-07T13:29:30Z: **48/87** bearbeitet, 39 noch PENDING; für bearbeitete Fälle echte vorhandene WordPress-Beitragsnummern und Titel verfügbar. Für 39 Fälle fehlt ein abgeschlossener Live-Befund.
- Prüfobjekt: tatsächliche ZIP-Version 0.57.144.22; SHA-256 `479260fc210683b0e4867588bafa0889a66af3443341c69ec19452d9476b403a`; PHP-Klassen aus dem entpackten ZIP unter `/mnt/data/pste-qa-v22/final-extracted/` über `PSTE_ROOT` geladen. Der scriptbasierte Negativtest nutzt **denselben** `PSTE_Planning_Readiness_Gate::evaluate` wie die vorhandene Programmfunktion.
- Inhaltliche externe Bestätigung: Pferdeatelier-Live-Kategorieseite „Beratung 2er Pferdeanhänger“ listet den vorhandenen 2er-Beratungstext; Pferdeatelier-Publikationen zu Halsteil und Regendecken-Reparatur wurden im Volltext gelesen; Fedimax und Equiva nennen 0 g als ungefüttert.
- Die nachgestellten Inventargegenproben nutzen tatsächliche WordPress-Titel und Kennungen, bei fehlenden Live-Metadaten **simulierte** gleiche Kategorie/Artikelart (als Annahme ausdrücklich gekennzeichnet). Keine Verbindung zur produktiven WordPress-Datenbank oder Produktionsfreigabe.

## Ergebnis: inhaltliche Gegenbeispiele gegen die zentrale Prüfung

| Test mit der echten v22-Zentralfunktion | Ist-Entscheid | Fachliche Bewertung |
|---|---|---|
| Existierender WP-Titel „2er Pferdeanhänger für zwei Pferde richtig auswählen“, neue Quelle „pferdeanhänger 2 pferde“ | **PASS** | **Zu großzügig:** Äquivalente Auswahlabsicht wird nicht zuverlässig erfasst. |
| Bereits im 87er-Batch: „0 g“ und „ungefüttert“ gegenseitig als vorhandener Redaktionsplan-Titel/SEO-Keyword eingespeist | **PASS und PASS** | **Zu großzügig:** Beide decken dieselbe Füllung und Suchabsicht ab. |
| Vorhandener Titel ist *buchstäblich gleich* der ursprünglichen Quellsuchfrage „Frieren Pferde unter Regendecken?“ | **REVIEW_REQUIRED** | Vorsichtig, aber keine definitive Dublettenentscheidung; deshalb entsteht dauernde Zurückstellung statt klarer Abschluss. |
| Allgemeiner Bestandsartikel Regendecken; spezieller Brand-Longtail „horseware regendecken“ | **PASS** | Plausible korrekte Freigabe **dieser** Dublettenregel, sofern keine Horseware-spezifische Bestandsseite existiert. |
| Existierender 2er-Artikel mit bekanntem Hauptkeyword „2er pferdeanhänger“; neue Quelle „pferdeanhänger 2 pferde“ | **PASS** | **Zu großzügig:** Synonyme/Zahlenschreibweisen verschleiern gleiche Suchabsicht. |

Unveränderte rohe Ausgaben der sechs PHP-Gegenproben:
```json
{"label": "A_EXISTING_REAL_2ER_ARTICLE", "q": "pferdeanhänger 2 pferde", "title": "Pferdeanhänger für zwei Pferde nach Platz und Zuladung auswählen", "inventory": ["2er Pferdeanhänger für zwei Pferde richtig auswählen"], "result": "PASS", "reason_codes": ["PORTAL_INTERNAL_FAMILY_CONTEXT_CHECKED"]}
{"label": "B_0G_WITH_UNGEFUETTERT_IN_PLAN", "q": "regendecke pferd 0g", "title": "Regendecken ohne Füllung für Pferde richtig einsetzen", "inventory": ["Ungefütterte Regendecken für Pferde bei Regen und Wind nutzen"], "result": "PASS", "reason_codes": ["PORTAL_INTERNAL_FAMILY_CONTEXT_CHECKED"]}
{"label": "C_UNGEFUETTERT_WITH_0G_IN_PLAN", "q": "regendecke pferd ungefüttert", "title": "Ungefütterte Regendecken für Pferde bei Regen und Wind nutzen", "inventory": ["Regendecken ohne Füllung für Pferde richtig einsetzen"], "result": "PASS", "reason_codes": ["PORTAL_INTERNAL_FAMILY_CONTEXT_CHECKED"]}
{"label": "D_SAME_SOURCE_TITLE_EXISTS", "q": "Frieren Pferde unter Regendecken?", "title": "Können Pferde trotz Regendecke frieren?", "inventory": ["Frieren Pferde unter Regendecken?"], "result": "REVIEW_REQUIRED", "reason_codes": ["PRE_TITLE_POTENTIAL_COVERAGE_ALTERNATIVE_INTENT"]}
{"label": "E_HORSEWARE_DISTINCT_OLD_GENERIC", "q": "horseware regendecken", "title": "Horseware-Regendecken und ihre Unterschiede bei Schnitt und Ausstattung", "inventory": ["Die passende Regendecke für Wetter und Pferd auswählen"], "result": "PASS", "reason_codes": ["PORTAL_INTERNAL_FAMILY_CONTEXT_CHECKED"]}
{"label": "F_OLD_HEAD_FOR_2ER_EXACT_SEO", "q": "pferdeanhänger 2 pferde", "title": "Pferdeanhänger für zwei Pferde nach Platz und Zuladung auswählen", "inventory": ["2er Pferdeanhänger für zwei Pferde richtig auswählen"], "result": "PASS", "reason_codes": ["PORTAL_INTERNAL_FAMILY_CONTEXT_CHECKED"]}
```

## Inhaltliche Zusammenhänge, die innerhalb der 87 JA-Themen gesondert auffallen

1. **Günstige Regendecken:** Nr. 7 und 72 haben dieselbe Preisberatungs-Suchabsicht (Wortfolge geändert).
2. **Regendecken im Test:** Nr. 9, 11 und 73 haben denselben Suchwunsch. Drei Varianten von Vergleichskriterien ersetzen keinen tatsächlichen Produkttest und begründen keine drei getrennten Artikel.
3. **Ungefütterte Decke:** Nr. 69 und 71 bezeichnen dieselbe 0-g-Produktart. Bei Test mit der echten Planungsgate-Funktion wurden beide trotz gegenseitiger Aufnahme in den Bestandsplan freigegeben.
4. **Pferd decken:** Nr. 63 ist mehrdeutig. Im Originaldatensatz stehen zwei alternative Titel, einer über Zucht, einer über Eindecken; die schon gewählte Zucht-Auslegung darf ohne belegte Suchabsicht nicht als zweifelsfrei gelten.
5. **Vorhandene Artikel:** Nr. 80 gegen Live-Artikel 10669, Nr. 5 gegen Live-Artikel 15493, Nr. 16 gegen Live-Artikel 15617 und direkte Quell-/Titeltreffer Nr. 17–19, 21 zeigen konkrete Überschneidungen. Nur bei 2er und 0-g wurde jetzt die Freigabe gegen den echten PHP-Code mit nachgebildetem Inventar ausgeführt; andere Beispiele sind inhaltliche Prüffälle, keine behaupteten neuen Runtime-Befunde.

## Vollständiger 87er-Herkunfts-/Titelabgleich
Alle 87 sind tatsächlich aus den Original-JA-Einträgen übernommen. Diese Tabelle ist ein **inhaltlicher Sichtabgleich** der Suchfrage und des gewählten Titels; sie ist **kein 87er-Live-Artikeltextvergleich**. Nicht markierte Zeilen sind nicht als semantisch 100 % konfliktfrei zertifiziert.

| Nr. | Ursprüngliche Suche (JA) | Gespeicherter Titel | Konkreter inhaltlicher Prüfhinweis |
|---:|---|---|---|
| 1 | pferde regendecken | Regendecken für Pferde passend zu Wetter und Haltung auswählen | Inhaltlich nahe beim existierenden Artikel 9108 „Die passende Regendecke für Wetter und Pferd auswählen“ (Live-Titel). |
| 2 | horseware regendecken | Horseware-Regendecken und ihre Unterschiede bei Schnitt und Ausstattung | — |
| 3 | regendecken mit fleece | Wann ist eine Regendecke mit Fleece für Pferde sinnvoll? | Im .21-Bericht BLOCKED, weil der Fragetitel nicht als FAQ klassifiziert ist. Inhaltliche Frage ist sinnvoll; Typ/Titelfreigabe inkonsistent. |
| 4 | regendecken mit abschwitzfunktion | So funktionieren Regendecken mit Abschwitzfunktion beim Pferd | Überschneidung zu existierender Abschwitzfunktion-Erklärung (Webseite publiziert). Abgrenzung der Antwort unklar. |
| 5 | regendecken mit halsteil | Wann lohnt sich eine Regendecke mit Halsteil fürs Pferd? | Live-Artikel 15493 „Regendecken mit Halsteil richtig auswählen“ erklärt, wann Halsteil sinnvoll ist; erhebliche Überschneidung. |
| 6 | regendecken für ponys | Regendecken für Ponys mit der richtigen Größe und Passform finden | — |
| 7 | günstige regendecken für pferde | Günstige Regendecken für Pferde und worauf es beim Kauf ankommt | Suchabsicht nahezu identisch zu Thema 72 (günstige Regendecken). |
| 8 | regendecken | Die wichtigsten Arten von Regendecken für Pferde im Überblick | — |
| 9 | pferde regendecken im test | Worauf es beim Vergleich von Regendecken für Pferde ankommt | Suchabsicht „im Test“ fast identisch zu 11 und 73; titelbezogene Vergleichskriterien sind keine selbst durchgeführten Produktprüfungen. |
| 10 | regendecken sale | Regendecken für Pferde im Sale kaufen und Fehlkäufe vermeiden | — |
| 11 | regendecken im test | Regendecken für Pferde anhand von Passform und Wetterschutz vergleichen | Suchabsicht fast identisch zu 9 und 73. |
| 12 | regendecken imprägnieren | Regendecken fürs Pferd richtig imprägnieren und pflegen | Existierender Artikel 10500 „Wie kann man Regendecken imprägnieren?“; erhebliche Überschneidung. |
| 13 | regendecken krämer | Regendecken von Krämer nach Passform und Ausstattung auswählen | — |
| 14 | pferdedecken regendecken | Die Unterschiede zwischen Regendecken und anderen Pferdedecken | — |
| 15 | shetty regendecken | Gut sitzende Regendecken für Shetlandponys finden | — |
| 16 | regendecken reparieren | Eine beschädigte Regendecke fürs Pferd selbst reparieren | Existierender Artikel 15617 „Schritt für Schritt Regendecken reparieren“; dessen Live-Text deckt Reparaturschritte ab. |
| 17 | Frieren Pferde unter Regendecken? | Können Pferde trotz Regendecke frieren? | Quelle stimmt wörtlich mit existierendem Artikel 972631 überein; aktuelle Prüfung nur REVIEW_REQUIRED. |
| 18 | Wie warm ist eine Regendecke mit Fleece? | Wie warm hält eine Regendecke mit Fleece wirklich? | Quelle stimmt wörtlich mit existierendem Artikel 15618 überein; aktuelle Prüfung nur REVIEW_REQUIRED. |
| 19 | Kann ich eine Regendecke mit Fleece auf ein nasses Pferd legen? | Darf eine Regendecke mit Fleece auf ein nasses Pferd? | Quelle stimmt wörtlich mit existierendem Artikel 10498 überein; aktuelle Prüfung nur REVIEW_REQUIRED. |
| 20 | Welche Regendecke mit Abschwitzfunktion ist die beste? | Welche Regendecke mit Abschwitzfunktion passt zu meinem Pferd? | Beste-Produkt-Frage, Sonderweg bleibt BLOCKED; kein automatischer Produktsieger. |
| 21 | Welche Regendecken haben eine Abschwitzfunktion für Pferde? | Welche Regendecken für Pferde können auch Feuchtigkeit ableiten? | Quelle stimmt wörtlich mit existierendem Artikel 10670 überein; aktuelle Prüfung nur REVIEW_REQUIRED. |
| 22 | magnetfeld gamasche pferd | Magnetfeld-Gamaschen für Pferde und was über ihre Wirkung bekannt ist | — |
| 23 | solarium pferd selber bauen | Pferdesolarium selber bauen und mögliche Sicherheitsrisiken kennen | — |
| 24 | teuerstes pferd deutschland | Welches Pferd gilt als das teuerste Deutschlands? | — |
| 25 | anhängerkamera pferd | Anhängerkameras zur Überwachung beim Pferdetransport auswählen | — |
| 26 | bronzefigur pferd | Eine Pferdefigur aus Bronze als Geschenk oder Dekoration auswählen | — |
| 27 | überwachungskamera pferd | Eine passende Überwachungskamera für den Pferdestall finden | — |
| 28 | transportunternehmen pferd | Ein zuverlässiges Transportunternehmen für Pferde finden | — |
| 29 | wasserführanlage pferd | Wasserführanlagen für Pferde und ihre Einsatzmöglichkeiten | — |
| 30 | lebermoos pferd pilz | Hilft Lebermoos tatsächlich gegen Pilzprobleme beim Pferd? | — |
| 31 | fliegeneier pferd | Fliegeneier beim Pferd erkennen und entfernen | — |
| 32 | eierstöcke pferd | Aufbau und Funktion der Eierstöcke bei der Stute | — |
| 33 | kompost einstreu pferd | Gebrauchte Pferdeeinstreu richtig kompostieren | — |
| 34 | pfriemenschwanz pferd eier | Pfriemenschwanz-Eier beim Pferd erkennen und einen Befall abklären | — |
| 35 | namensschild pferd selber machen | Ein individuelles Namensschild für die Pferdebox selber machen | — |
| 36 | west nil virus pferd verbreitung deutschland | Die Verbreitung des West-Nil-Virus bei Pferden in Deutschland | — |
| 37 | wassertröge selber bauen | Einen sicheren Wassertrog für Pferde selber bauen | — |
| 38 | pferdeweiden dünger raiffeisen | Dünger für Pferdeweiden bei Raiffeisen auswählen | — |
| 39 | unkraut auf pferdeweiden | Unkraut auf Pferdeweiden erkennen und zurückdrängen | — |
| 40 | bäume für pferdeweiden | Geeignete Bäume als Schattenspender auf Pferdeweiden | — |
| 41 | giftpflanzen auf pferdeweiden | Gefährliche Giftpflanzen auf Pferdeweiden erkennen | — |
| 42 | wassertröge kaufen | Den passenden Wassertrog für Pferde kaufen | — |
| 43 | beheizbare wassertröge | Beheizbare Wassertröge für Pferde sicher auswählen | — |
| 44 | dünger auf pferdeweiden | Wann und womit sollte man eine Pferdeweide düngen? | — |
| 45 | rasensaat für pferdeweiden | Geeignete Rasensaat für die Nachsaat von Pferdeweiden | — |
| 46 | gülle für pferdeweiden | Gülle auf Pferdeweiden und mögliche Risiken für Pferde | — |
| 47 | giftige gräser auf pferdeweiden | Giftige Gräser auf Pferdeweiden erkennen und Risiken einschätzen | — |
| 48 | mineraldünger für pferdeweiden | Mineraldünger für Pferdeweiden bedarfsgerecht einsetzen | — |
| 49 | darf man pferdeweiden mit gülle düngen | Darf man Pferdeweiden mit Gülle düngen? | Alte Relevanzstruktur-Sperre im nicht bearbeiteten Bestand, im Bericht PENDING; Neuentscheidung live nicht belegt. |
| 50 | gräsermischung für pferdeweiden | Die passende Gräsermischung für eine Pferdeweide finden | — |
| 51 | pferd | Was braucht ein Pferd für eine artgerechte Haltung? | Extrem breite Quelle „pferd“ lässt die konkret gewählte Haltungsintention ohne Suchabsichts-Nachweis offen. |
| 52 | pferd kaufen | Worauf sollte ich achten, bevor ich ein Pferd kaufe? | — |
| 53 | schimmel pferd | Schimmel als Fellfarbe beim Pferd erkennen | — |
| 54 | pferd zeichnen | Ein Pferd mit stimmigen Proportionen Schritt für Schritt zeichnen | — |
| 55 | pferd malen | Fellfarben und Bewegung beim Malen von Pferden darstellen | — |
| 56 | heuraufe pferd | Die passende Heuraufe für Pferde finden | Existierender Artikel 17126 „So findest du ideale Heuraufen für Pferde“; Abdeckung wahrscheinlich, genauer SEO-Nachweis fehlt. |
| 57 | westfale pferd | Herkunft und Eigenschaften des Westfälischen Warmbluts | — |
| 58 | pferd ausmalen | Pferde-Malvorlagen für Kinder auswählen und nutzen | — |
| 59 | strahlfäule pferd | Strahlfäule beim Pferd erkennen und behandeln lassen | — |
| 60 | kolik pferd | Woran erkenne ich eine Kolik beim Pferd und was muss ich tun? | — |
| 61 | pferd gamaschen | Gamaschen fürs Pferd sicher anpassen und sinnvoll einsetzen | — |
| 62 | teuerste pferd der welt | Welches Pferd war das teuerste der Welt? | — |
| 63 | pferd decken | Die Bedeckung einer Stute richtig vorbereiten | Original-Rohsuche „pferd decken“ hat in den Originaldaten ZWEI verschiedene angebotene Intentionen: Stute decken / Pferd eindecken. Vorhandene Auswahl ist allein kein Beleg für Nutzerintention. |
| 64 | pferd gewicht | Das Gewicht eines Pferdes ohne Waage einschätzen | — |
| 65 | heucobs pferd | Heucobs für Pferde richtig einweichen und füttern | — |
| 66 | apfelschimmel pferd | Wie entwickelt sich die Fellfarbe eines Apfelschimmels? | — |
| 67 | pferd anatomie | Körperbau und Anatomie des Pferdes verständlich erklärt | — |
| 68 | spat beim pferd | Spat beim Pferd erkennen und tierärztlich abklären lassen | — |
| 69 | regendecke pferd 0g | Regendecken ohne Füllung für Pferde richtig einsetzen | Gleiche Suchabsicht wie 71: 0 g = ungefüttert; die .22-Zentralfunktion lässt beide trotz gegenseitiger Existenz durch. |
| 70 | fliegen regendecke pferd | Kombinierte Fliegen- und Regendecken für Pferde sinnvoll nutzen | — |
| 71 | regendecke pferd ungefüttert | Ungefütterte Regendecken für Pferde bei Regen und Wind nutzen | Gleiche Suchabsicht wie 69: ungefüttert = 0 g; die .22-Zentralfunktion lässt beide trotz gegenseitiger Existenz durch. |
| 72 | pferde regendecken günstig | Günstige Pferde-Regendecken mit gutem Wetterschutz finden | Suchabsicht nahezu identisch zu 7 (günstige Regendecken). |
| 73 | regendecken für pferde im test | Regendecken für Pferde nach Wasserdichtigkeit und Passform vergleichen | Suchabsicht nahezu identisch zu 9 und 11 („Regendecken im Test“). |
| 74 | schleich pferdeanhänger | Schleich-Pferdeanhänger und passendes Zubehör für Spielsets | — |
| 75 | gasdruckfeder pferdeanhänger | Die richtige Gasdruckfeder für einen Pferdeanhänger finden | — |
| 76 | böckmann pferdeanhänger gebraucht kaufen | Worauf sollte ich beim Kauf eines gebrauchten Böckmann-Pferdeanhängers achten? | — |
| 77 | planen pferdeanhänger | Passende Planen für Pferdeanhänger auswählen | — |
| 78 | deichselabdeckung pferdeanhänger | Deichselabdeckungen für Pferdeanhänger als Wetterschutz nutzen | — |
| 79 | humbaur pferdeanhänger | Humbaur-Pferdeanhänger nach Ausstattung und Nutzung vergleichen | — |
| 80 | pferdeanhänger 2 pferde | Pferdeanhänger für zwei Pferde nach Platz und Zuladung auswählen | Existierender live sichtbarer Artikel 10669 „2er Pferdeanhänger für zwei Pferde richtig auswählen“; .22-Zentralfunktion gibt neuen Titel auch mit diesem Treffer frei. |
| 81 | pferdeanhänger gebraucht kaufen | Wie prüfe ich einen gebrauchten Pferdeanhänger vor dem Kauf? | — |
| 82 | pferdeanhänger gewicht | Leergewicht und Zuladung beim Pferdeanhänger verstehen | — |
| 83 | pferdeanhänger 4 pferde | Pferdeanhänger für vier Pferde und die Anforderungen an das Zugfahrzeug | — |
| 84 | pferdeanhänger 3 pferde | Pferdeanhänger für drei Pferde nach Platzangebot und Gewicht auswählen | — |
| 85 | pferdeanhänger mieten | Was sollte ich beachten, wenn ich einen Pferdeanhänger miete? | — |
| 86 | pferdeanhänger gebraucht | Typische Schwachstellen gebrauchter Pferdeanhänger erkennen | — |
| 87 | pferdeanhänger sirius | Sirius-Pferdeanhänger und ihre Ausstattungsvarianten im Überblick | — |

## Ursache auf Systemebene und Konsequenz (KISS)

- **Nicht** „mehr technische Tests“; der Mangel ist die zu grobe **inhaltliche Bedeutungserkennung innerhalb genau derselben zentralen Planung**. Ähnliche Bedeutung kann mit anderen Wörtern formuliert sein (2er/zwei Pferde, 0g/ungefüttert). Die vorhandene Wort-/Vergleichslogik erkennt sie nicht immer.
- Eine einzelne zentrale Planung muss **sowohl den echten WordPress-Bestand als auch die anderen JA-Themen im aktuellen Stapel** inhaltlich abdecken. Danach exakt drei mögliche Ergebnisse: PASS, eindeutig DUBLETTE, oder als eigenständige Suchintention zurückstellen. Eine zusätzliche zweite Prüfstufe wäre **gegen das vereinbarte Konzept**.
- **Keine neue ZIP und kein neuer WordPress-Test empfohlen**, bevor diese konkreten Gegenbeispiele einschließlich positiver Nicht-Dubletten und der inhaltlichen Mehrdeutigkeit innerhalb der 87 in einer einzigen Ende-zu-Ende-Simulation bestanden sind.
- **Grenze:** Ohne vollständige aktuelle WordPress-Artikeltexte/SEO-Metadaten und vollständigen 87er-Live-Endbericht lässt sich nicht beweisen, dass jeder mögliche Bestandskonflikt erkannt wird. Die inhaltlichen Fehler bei den gezeigten konkreten Fällen sind dagegen durch Originaldatensatz, echte PHP-Ergebnisse und öffentliche Pferdeatelier-Texte begründet.

## Öffentliche Belegseiten
- Pferdeatelier 2er-Beratung: https://pferde-atelier.de/category/2er-pferdeanhaenger-beratung/
- Pferdeatelier Halsteil: https://pferde-atelier.de/regendecken-mit-halsteil-richtig-auswaehlen/
- Pferdeatelier Reparatur: https://pferde-atelier.de/schritt-fuer-schritt-regendecken-reparieren/
- Fedimax Regen/Winterdecken 0g/ungefüttert: https://www.fedimax.de/regen-winterdecken
- Equiva Pferdedecken 0g/ungefüttert: https://www.equiva.com/ratgeber/pferdeausruestung/pferdedecken