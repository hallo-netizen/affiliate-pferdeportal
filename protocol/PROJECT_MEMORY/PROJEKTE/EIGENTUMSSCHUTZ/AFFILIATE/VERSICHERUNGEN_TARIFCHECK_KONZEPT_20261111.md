# Hab & Bewahr – Versicherungswerbung exklusiv / Tarifcheck zuerst
Stand 11.11.2026 · **Konzept und geprüfter Änderungsbedarf, KEIN bereits eingebautes Update**

## 1. Verbindliches Ziel

In **der gesamten siebten Hauptwelt „Versicherungen“** – deren R1-Hauptseite, allen fünf R2-Seiten, sämtlichen 46 R3-Versicherungsseiten, allen WP-Blattkategorien, eindeutig zugeordneten Beiträgen und fachlich eindeutig verknüpften Glossareinträgen – darf **nur Werbung für nachweislich passende Versicherungs-Partnerprogramme** erscheinen.

**Ausdrücklich auszuschließen:** Amazon (auch Bücher, Tresore und Dokumententaschen), eBay, idealo, allgemeine Produktanbieter, fachfremde Direktbanner, Kredit-/Girokonto-Werbung. Gilt für breite Banner, quadratische Banner, Produktkarten, interne Fallbacks, freie Werbeplätze und Artikelhybrid-Ausgaben. Versicherungswerbung muss außerdem zur **konkreten** Versicherungsart passen. Ohne passendes freigegebenes Angebot bleibt der Platz öffentlich leer; keine thematisch falsche Ersatzwerbung.

Die sechs bisherigen Schutzwelten sind funktional und optisch **unverändert** zu lassen. Keine Änderung der Kategoriehierarchie, Artikelinhalte, WordPress-IDs, Affiliate-Tracking-Kennungen oder anderer Portale.

## 2. Nachgewiesener Ist-Stand 11.11.2026

**Physische CURRENT-ZIPs bereits vorhanden** im offiziellen HAB-Pluginbüro: Design HAB-001 RC19/0.1.192 und Affiliate HAB-004 RC18/0.1.15-rc18. Die ZIPs werden durch dieses Konzept nicht verändert.

Am **tatsächlichen vollständigen HAB-004-RC18-Archiv (36 Dateien)** im unabhängigen GitHub-Runner read-only geprüft:
- Bereits vorhanden: reguläre Partner-/Bannerkampagnen, `direct` (Direktpartner), `awin`, `adcell`, Partner-/Werbemittelverwaltung, Zielzuordnungen, Freigabe, Mehrformate und Artikel-/Glossar-Slots. Awin und ADCELL haben bestehende Provider-/Import-/Synchronisationswege; technisch vorgesehen bedeutet **nicht**, dass die Konten verbunden oder Tarife freigeschaltet sind.
- Im WordPress-Backend bereits zugänglich: **Affiliate-Zentrale → Anbieter & APIs → Netzwerke & API, Awin, ADCELL**; daneben **Ausspielung → Ausgaben & Freigabe, Zuordnungen, Einzelbeiträge, Vorschau**. Für Tarifcheck zunächst **Direktpartner mit freigegebenen Original-Werbemitteln**, kein zweiter Provider-Stack.
- **Nachweislich vorhandene Lücke**: `includes/trait-ppar-hb-amazon.php` enthält weiterhin `core:world:insurance` mit Amazon-Fallback „Feuerfeste Dokumententasche Versicherungsunterlagen“ und Motiv `hb-amazon-kategorie-tresore.webp`. Die bestehende Amazon-House-Ausgabe läuft im Kampagnen-Fallback; es fehlt eine durchgängige versicherungszweigbasierte Sperre vor allen Ausgabepfaden. Allein das Motiv zu löschen würde nicht reichen.
- **Zweite relevante Lücke:** `includes/trait-ppar-output-objects.php` enthält zwar eine Tarifcheck-Versicherungs-Familienzuordnung für einen **anderen Pfad** („Wissen > Versicherungen & Recht“, nur Blattkategorien); dies ist **nicht** gleichbedeutend mit dem siebten HAB-Versicherungs-Hauptzweig mit R1/R2/R3/Beiträgen. Kein vermeintlicher Live-PASS.
- Die bestehende Artikelvorlage ruft bereits einen freigegebenen Artikelbanner über die zentrale Affiliate-Zentrale auf. Deshalb keine manuellen Artikelarbeiten oder zweiten Inhaltsfilter einbauen.

Der offizielle Versicherungs-Kategorieplan (C2.5/C2.6) sieht **1 R1, 5 R2, 46 R3 und 323 Endkategorien** vor (vor C2.6 waren 138 vorgesehen). Dies ist die **fachliche Soll-Struktur** des vorhandenen Kategorieplugins 1.14.8.37. Kein erneuter Import, kein stillschweigendes Versprechen, dass alle 323 live synchronisiert sind. Laufzeit-Snapshot beim späteren Test read-only prüfen.

## 3. Partnerstrategie

**Phase 1: Tarifcheck DIREKT**, weil dieses Partnerprogramm laut offizieller Anbieterinformation für Sach-, Kfz-, Haftpflicht-, Kranken- und Vorsorgeversicherungen Banner in verschiedenen Größen, Deeplinks und Vergleichsrechner bietet. Nutzer hat ein Tarifcheck-Partnerkonto und im Screenshot den Bereich „Werbemittel“ mit passenden Rubriken geöffnet.

**Phase 2: Awin und ADCELL als Reserve** für Versicherungsarten, bei denen Tarifcheck nachweislich kein passendes Ziel/Banner bietet oder nach Vergleich der Konditionen schlechter passt. Die bestehenden Awin-/ADCELL-Integrationen dafür unverändert behalten; zunächst **keine ungezielte Vollsynchronisierung/Produkteinspeisung**. Tarifcheck selbst wird auch über Awin angeboten, jedoch ist das nicht automatisch dasselbe Tracking und nicht notwendig die gleiche Vergütung – **nicht doppelt zuordnen**.

**Tarifchecks Rubrik „Finanzen“ (Girokonto, Kredit, Kreditkarte, Baufinanzierung) ist ausdrücklich KEINE Versicherungswerbung**. Nicht im Versicherungszweig ausliefern. Ein späterer separater Finanzstrang kann diese Angebote nutzen; diesen jetzt nicht neu anlegen.

## 4. Mapping: vorhandene HAB-Versicherungskategorien ↔ Tarifcheck

Die **fünf HAB-R2-Bereiche bleiben bestehen**, die Tarifcheck-Menügruppen ersetzen NICHT unseren Kategoriebaum:

| Bestehendes HAB-R2 | Erstes passendes Tarifcheck-Ziel | Nur nach Ziel-/Programmbestätigung |
| --- | --- | --- |
| Hausrat & Gebäude | Hausratversicherung, Wohngebäudeversicherung | Bauleistung, Elektronik, Mietausfall: kein Tarifcheck-Ersatz ohne echtes Ziel |
| Fahrzeuge & Reisen | Kfz-Versicherung, Motorradversicherung | Wohnmobil, Fahrrad, E-Scooter, Boot, Reisepolicen nur bei fachlich korrektem Programm |
| Haftpflicht & Rechtsschutz | Privathaftpflicht, Rechtsschutz, Haus- & Grundbesitzerhaftpflicht, Tierhalter-/Pferdehaftpflicht | Hunde-/Pferde-spezifisch nur wenn Versicherungsart passt; Drohne, Verein u.a. nicht pauschal „Haftpflicht“ |
| Krankenversicherung & Vorsorge | PKV (mit passenden Zielgruppen), Krankenzusatz, Pflegezusatz, BU, Unfall, Risiko-Leben, Renten-/Lebensversicherung | Kein allgemeines PKV-Banner als Behauptung für gesetzliche KV oder exotische Vertragsformen |
| Gewerbeversicherungen & Finanzen | Firmenversicherung bei belegtem Leistungsumfang | Für Cyber, D&O, Kaution, Warenkredit, Betriebsunterbrechung u.a. nicht ungeprüft den allgemeinen Firmenlink verwenden |

**Matching-Regel:** Erst exakt passendes Ziel zur R3-Versicherungsart oder Endkategorie. Bei Elternpfad nur zurückfallen, wenn das allgemeine Versicherungsprogramm den konkreten Leistungsbereich sachlich wirklich abdeckt. Versicherungsfremder Banner wird IMMER verworfen. Beschriftung/Affiliate-Links nur mit echtem freigegebenem Werbemittel und bestätigtem Tarifcheck-Ziel, keine erfundenen Links.

## 5. Technische Anpassung HAB-004 – ausschließlich im bestehenden Plugin

1. **Ein einheitlicher zentraler Schutzfilter** ermittelt aus dem aktuellen, verifizierten HAB-Kategorie-Snapshot den Root `core:world:insurance`. Er greift vor jeder Kampagnen-Auswahl und vor Produkt-/Amazon-Fallbacks. Versicherungs-R1, R2, R3, Endkategorie, Post und eindeutig verknüpfter Glossareintrag sind erfasst; bei widersprüchlichen/unbekannten Zuordnungen keine Fallback-Werbung. Diese Schutzregel darf auch von manuellen, bereits gebuchten fachfremden Kampagnen nicht umgangen werden.
2. **Nur Versicherungs-Partnerkampagnen zulassen:** nicht allein nach Netzwerk `direct`/`awin`/`adcell`, sondern nach bestätigtem **Programm + Versicherungsprodukt + echtem Ziel**. Jede Anbieterwerbung außerhalb dieser Fachklasse wird im Versicherungsbaum blockiert. Das bestehende Bannermatching/Zielkatalog benutzen, nicht ersetzen.
3. **Amazon vollständig ausschalten**, inklusive `hb_amazon_house_banner`, `hb_amazon_article_fallback`, `hb_amazon_area_product_fallback`, `render_affiliate_slot`-Fallbacks und Karten/Artikel-Hybrid; die Amazon-Suche für Versicherungsknoten nicht mehr beauftragen. Kein bloßes CSS-Verstecken, kein globales Amazon-AUS für die sechs anderen Welten.
4. **Vorhandene Werbeplätze nutzen:** breite Banner auf R1/R2/R3/Kategorie und in geeigneten Artikelpositionen; Quadrate in Artikel-Sidebar/Glossar und der vorgesehenen Mobilansicht. Nicht zusätzlich an allen möglichen Stellen duplizieren. Ein auf Mobil umgestellter Slot rendert keine zweite sichtbare Kampagne.
5. **Originalformat wahren:** Querbanner und 1:1-Quadrat getrennt auswählen. Herstellerbilder weder stauchen noch ungeprüft zuschneiden. Ein 300×250-Original ist kein 1:1-Quadrat. Wenn kein zulässiges quadratisches Werbemittel vorhanden, bleibt der Quadratplatz leer oder Tarifcheck wird um ein passendes Motiv gebeten. Eindeutiges Label „Anzeige“, freigegebener Affiliate-Link, rel=sponsored/nofollow, gesetzliche Werbe-/Datenschutzregeln einhalten.
6. **KISS:** Keine neue Tabelle, keine neue Pluginidentität, keine zusätzlichen Frontend-HTTP-Aufrufe, keine Neuanlage einer Werbeengine, keine zweite Sonderarchitektur für Tarifcheck. Bestehende Import-/Freigabe-/Ausspielungslogik und den bestehenden 14-Tage-Prüfzyklus wiederverwenden. Ablehnungsgrund im vorhandenen Protokoll vermerken; keine vollgepackte Backend-Seite.

**Backend – nur notwendige Anzeigen:** Unter bestehenden Werbemitteln/Zuordnungen künftig klarer Filter „Versicherungen“ und Übersicht „PASS / kein passendes Banner / gesperrt“. Tarifcheck als freigegebener Direktpartner. Für Awin/ADCELL später Partner-ID + Vertrags-/Freigabestatus und korrektes Versicherungsangebot. Keine 46 Einzelzuordnungen per Hand im WordPress-Editor, zentraler Match aus dem bestehenden Baumsnapshot.

## 6. Umsetzung in Reihenfolge – sauber und klein

1. **Sperre zuerst** in einem Update HAB-004 einbauen und offline gegen realen RC18-Stand simulieren. Keine Amazon- oder fachfremde Werbung irgendwo unter dem Versicherungsroot; Gegenproben: alle sechs übrigen Welten unverändert, gemischte Post-Kategorien, fehlende Zuordnung, undefinierte R2/R3 und gespeicherte Fremdkampagnen.
2. **Tarifcheck in der Affiliate-Zentrale als Direktpartner anlegen**: vorhandene Partner-ID über WordPress speichern, nicht in GitHub. Nach Freigabe im Tarifcheck-Konto unter **Werbemittel** konkrete Original-Links/Bannerdaten sammeln; zunächst vier gut passende Testzweige: Hausrat, Wohngebäude, Privathaftpflicht, Kfz. Für jeden zunächst ein Querformat und, sofern tatsächlich vorhanden, ein freigegebenes Quadrat. Nicht davon ausgehen, dass jedes im Screenshot sichtbare Tarifcheck-Produkt auch 1:1-Banner bietet.
3. **Zentrale Kampagnen- und Zielzuordnung automatisieren**: Originalziel → konkreter Versicherungs-R3-/Endkategorie-Pfad → Format-/Linkprüfung → priorisierte Ausspielung. Nur auf wirklich passenden Seiten, Artikeln und Glossaren. Selbst gesetzte Werbemittel werden einmal zentral gespeichert, nicht in Beiträgen.
4. **Kontrolllauf:** Hauptwelt Versicherungen, jede der 5 R2-Seiten, Stichprobe aller vorhandenen R3- und WP-Endkategorien, Artikel Desktop/Mobil (Quer + Quadrat), leere Bannerplätze und 6 Nicht-Versicherungs-Welten testen. Test der realen Tarifcheck-Zielseite und provisionsfähigen URL mit eigener Partnerkennung (keine künstlichen Abschlüsse).
5. Erst bei Live-PASS **weitere freigegebene Tarifcheck-Angebote** einpflegen; danach gezielte Recherche für konkret unbesetzte Versicherungsarten bei Awin und ADCELL. Partnerwahl regelmäßig nach Relevanz, Bestätigung, Provisionsmodell und Leistung statt pauschalem Netzwerk-Ranking.

## 7. Was bereits sicher ist, was offen bleibt

**Bestätigt:** vorhandenes HAB-004 RC18 hat Direct-, Awin-, ADCELL-Provider, Bannerformate und Slot-Steuerung; versicherungsbezogener Amazon-Fallback existiert; bestehender Versicherungsbaum als Fachplan; Tarifcheck bietet laut offizieller Anbieterwebseite Versicherungskategorien, Banner/Deeplinks und Vergleichsrechner.

**Noch nicht bestätigt:** bestehende Versicherungs-Sperre (ist unvollständig), gespeicherte Tarifcheck-Links/Bilder in HAB-004, genaue Square-Werbemittel pro Produkt, aktueller Freigabestatus der einzelnen Tarifcheck-Kampagnen, aktuelle Provisionsbedingungen im eingeloggten Benutzerkonto und Live-Importstatus aller 323 Endkategorien. Daher **noch kein WordPress-Pluginupdate und keine Live-Freigabe** behaupten.

Offizielle Anbieterquellen:
- https://www.tarifcheck-partnerprogramm.de/werbemoeglichkeiten/
- https://www.tarifcheck-partnerprogramm.de/provisionen/
- https://www.tarifcheck.de/partnerprogramm/
- Awin-Tarifcheck-Programm (separate Vermittlungsstrecke): https://ui.awin.com/merchant-profile/11202

**Verbindlicher nächster Arbeitsschritt nach diesem Konzept:** HAB-004-Update mit vollständig durchgesetztem Versicherungs-Ausschluss und sauberen Versicherungsziel-Filtern bauen und offline testen; danach erst Tarifcheck-Werbemittel zentral aktivieren. Diese Konzeptdatei verändert die CURRENT.zip ausdrücklich nicht.


## 8. Ergänzung 11.11.2026 – Hausrat: Werbemittel und konkrete Darstellung (Nutzer-Screenshots 11:43–11:44)

### Nachgewiesene Tarifcheck-Werbemittel im angemeldeten Nutzerkonto

Im Anbieter-Menü **Sachversicherungen → Hausrat** sind drei **unterschiedliche Werbearten** zugänglich:

1. **Tarifrechner / Formulare:** vollständiger Hausrat-Rechner mit Eingaben für persönlichen Versicherungsbedarf und Vergleich; Screenshot zeigt Backend-Optionen „Verhalten auf Mobilgeräten: Mobilrechner einbinden“, „Scrolling-Verhalten: Kein Scrolling“ sowie Vorschau mit mehrstufigen personenbezogenen Formfeldern. Die konkrete originale Einbettungsdatei, Datenschutzbedingungen und Erfolgstracking werden vor Verwendung geprüft; kein aus dem Screenshot erfundener HTML-/JavaScript-Code.
2. **Direktlinks:** separater Menüpunkt mit zum Vergleich führenden Partnerlinks. Exakte registrierte Ziel-URL/Tracking-ID im bestehenden WordPress-Backend speichern, **keine Partner-ID oder persönlichen URLs in GitHub protokollieren**. Zielseite und provisionsfähige Weiterleitung real testen.
3. **Banner:** tatsächlich angebotene Maße **120×60, 120×600, 125×125, 160×600, 234×60, 300×250, 468×60 und 728×90 px**. Nur vorhandene Originalgrafiken verwenden; keine selbst angenommene Variante 300×300. Ein 300×250-Banner ist **kein Quadrat**. Nicht verzerren oder 125×125 auf 300×300 hochziehen.

Tarifcheck bestätigt zusätzlich öffentlich, dass White-Label-Tarifrechner mobilgeeignet und ggf. gestaltbar sind, als eigene Landingbereiche eingebunden werden können und es auch Kurzrechner für Content gibt: https://www.tarifcheck-partnerprogramm.de/werbemoeglichkeiten/ . **Aus dem Nutzer-Screenshot folgt nicht, dass für Hausrat ein eigener Kurzrechner bereitsteht.**

### Darstellung auf der Website – verbindliche erste Belegung für Hausrat

| Hab-&-Bewahr-Ort | Werbeart | Platzierung und Verhalten | Warum |
| --- | --- | --- | --- |
| Versicherungen (R1, Hauptwelt) | **Keine isolierte Hausratkampagne** | Übersicht der fünf Versicherungsbereiche mit neutralen, echten Fachlinks; kein aufgedrängtes Hausratbanner | Sonst werden andere Versicherungssparten thematisch falsch beworben |
| Hausrat & Gebäude (R2) | Fachliche Links/Teaser **Hausrat vergleichen** und **Wohngebäude vergleichen** | Als getrennte Ziele an den passenden thematischen Kacheln, nicht ein einheitlicher Hausratbanner über allen | Bereich enthält mehrere Versicherungsarten |
| Hausratversicherung (konkretes R3) | **Breites Originalbanner** (Desktop 728×90, alternativ 468×60; mobil 234×60), kombiniert mit schlankem **Direktlink** | Ein Banner in bestehendem Quer-Slot unter fachlicher Einführung oder den vorhandenen Kacheln; Textlink „Hausrat-Tarife vergleichen“ als klare Handlung. Nicht gleichzeitig zwei inhaltlich identische Banner | Gute Sichtbarkeit, Fachtext bleibt dominant |
| Bestehende Endkategorie „Hausratversicherung vergleichen“ | **Eingebetteter Tarifrechner** | Auf der bestehenden Vergleichs-Kategorieansicht an einem einzigen, klar bezeichneten Rechner-Slot; möglich nach kurzer fachlicher Erklärung und Werbekennzeichnung. Auf Mobil die vom Anbieter vorgesehene Mobilvariante. Wenn es keinen sicher nutzbaren Einbau-/Datenschutzweg gibt: **Direktlink zum echten externen Rechner** statt unzulässiger Einbettung | Rechner nur dort, wo die Besuchenden tatsächlich vergleichen wollen |
| Hausrat-Beratung, FAQ und thematisch passende Ratgeberbeiträge | **Kontextbezogener Direktlink** + maximal **ein** passendes Banner | In Fachtext nach einem sachlich geeigneten Abschnitt Textlink/Button, nicht vor den notwendigen Hinweisen; Desktop in bestehender Artikel-Seitenleiste bevorzugt Originalbanner 300×250; mobil dasselbe Banner unter geeignetem Textabschnitt (nicht eine zweite Kopie) | Informationen bleiben vorrangig, kein Werbeübergewicht |
| Kleine Glossar-Slots mit sicher nachgewiesenem Hausratbezug | **Echtes Quadrat 125×125** *nur wenn ausreichend groß lesbar*; sonst eindeutiger Direktlink oder leer | Nicht auf 300×300 strecken; wenn vorhandener Sidebar-Slot zwingend ein großes Quadrat erwartet, keine Grafikzwangsanpassung | Vorhandenes Tarifcheck-Quadrat ist klein |
| Fremde Versicherungsarten oder sechs Nicht-Versicherungswelten | **Keine Hausrat-Werbung** | Kein Hausrat- oder Versicherungsfallback; bestehende fremde Ausgaben bleiben unverändert | Fachliche Trennung |

**Formatregeln:** 120×600 und 160×600 (lange Hochkantbanner) zunächst NICHT benutzen; 120×60 zu klein für die großen Portalplätze. 468×60/728×90 als responsive Querbanner proportional verkleinern (keine horizontale Überlappung); 234×60 mobil möglich. 300×250 als **Rechteck** in Sidebar, bei schmalen Handys proportional max. containerbreit. 125×125 als kleines echtes Quadrat, wenn optisch lesbar; sonst Direktlink. Originalgröße, Einbaucode, Gewicht und Verfügbarkeit erst nach Öffnen des jeweiligen Angebots im Partnerkonto final abnehmen. Keine ungetesteten Bild-URLs, keine erfundenen Direktlinks.

### UX-Skizzen (konzeptionell, keine schon umgesetzte Frontend-Ansicht)

**Hausratversicherung R3 – Desktop**

```text
[Überschrift Hausratversicherung]
[Fachliche Einführung / Themenübersicht]
                 Anzeige
[  ORIGINAL TARIFCHECK-QUERBANNER 728×90  ]
[Hausrat-Tarife vergleichen → geprüfter Direktlink]
[Weitere Themenkacheln, Beratung, FAQ und Artikel]
```

**Passender Fachartikel – Desktop**

```text
[Artikelüberschrift]                 [Anzeige]
[Ein redaktionelles Beitragsfoto]    [Hausrat 300×250]
[Fachlicher Text]                     [kein zweites Werbebild]
[Tarife vergleichen → Direktlink]
[Weiterer Fachtext]
```

**Hausratversicherung vergleichen – eigene bestehende Kategorieansicht**

```text
[Hausratversicherung vergleichen]
[Kurze fachliche Erklärung]
[Anzeige / Tarifvergleich von Tarifcheck]
[Nach explizitem Aufruf: ORIGINAL-TARIFRECHNER, Mobilversion für Smartphones]
[Weiterführende Fachinhalte, Bedingungen, FAQ]
```

### Einbau über die vorhandenen Plugins – minimal

- **Affiliate-Zentrale HAB-004** übernimmt alle drei Werbearten über die vorhandene Direktpartner-, Creative-, Slot-, Zuordnungs- und Tarifrechner-/Textlink-Steuerung. Die vorhandene Tarifrechner-Verwaltung ist code-seitig nachgewiesen; **ob** Tarifchecks konkreter Embed-Code ohne weitere Kompatibilitätsanpassung funktioniert, bleibt ein expliziter Pflicht-Test. Kein neues Plugin, keine zusätzliche Tabelle, keine neuen Frontend-HTTP-Aufrufe durch eigene Bannerprüfung.
- **Design HAB-001** stellt vorhandene breite/seitliche/mobil verlegte Werbeslots bereit; nur wenn die **bestehende** Vorlage auf dem Vergleichs-Kategorien-Slot technisch keinen Tarifrechner einsetzen kann, einen kleinen zentralen Anschluss im bestehenden Designplugin ergänzen, ohne am WordPress-Artikelinhalt oder den Kategorien manuell zu arbeiten.
- Original-Rechner **nicht auf jeder Beitragsseite** automatisch laden: große Eingabeoberfläche, hohe Wartezeit und mögliche Drittanbieter-Cookies/Datenerhebung. Wenn externes Script/iframe nötig, erst nach dokumentierter Datenschutzprüfung und geeigneter, ggf. nutzerinitiierter Freigabe laden. Anbieterangaben bei Formulareingaben werden im Original-Tarifcheck-Rechner erfasst, nicht durch selbst erzeugte Formulare.
- **Nur eine Auslieferung pro Werbeplatz**, keine Doppelung durch Desktop- und Mobil-Variante. Vor jeder Ausgabe die im vorherigen Kapitel definierte Versicherungs-Exklusivsperre prüfen. Priorität: exakter Hausrat-Anbieter und passendes Format → geprüfter allgemeiner Versicherungs-Fachlink nur wenn sachlich passend → sonst leer. **Nicht** Amazon/eBay/idealo/Finanzen.
- Backend-Verwaltung KISS: drei Werbemittelarten „Tarifrechner“, „Direktlink“, „Banner“ (mit Originalmaßen, Ziel, Freigabestatus), zugeordnet zum bestätigten Hausrat-R3/-Vergleichs-Endkategorie-Baum; Anzeige eines Tests „Desktop/Mobil, Ziel, Tracking, Sponsor-Label“. Partnerkennung geheim halten.

### Offene Umsetzung und Kontrolllauf

1. Partnerkonto: tatsächlichen **Originalcode für Hausrat-Tarifrechner** und originale **Direktlink-URL** sowie Code/Bild-URL für **728×90**, **234×60**, **300×250**, optional **125×125** getrennt einsehen. Diese Angaben sind auf Screenshots nicht sichtbar und dürfen nicht erraten werden.
2. Zunächst die fachlich zwingende **Amazon-/Nichtversicherungs-Sperre im Versicherungszweig** in HAB-004 implementieren, dann testbare Versicherungs-Creatives erlauben. Das Konzept ist **keine** Behauptung, dass die Sperre bereits live ist.
3. Offline testen: echte R3-Hausratseite, echte Vergleichs-Endkategorie, echter Artikel und mobiles Rendering (360–390px), fehlender Banner, gemischte Kategorien, Datenschutz-/iframe-Fallback; Gegenproben R2 „Hausrat & Gebäude“, andere Versicherungs-R3 und sechs andere Welten.
4. Nur nach bestandener Prüfung der echten Werbemittel und Einbindung eine installierbare Folgeversion der vorhandenen Plugins als vollständige ZIP bereitstellen und **danach** WordPress-Abnahme.

**Explizit weiterhin ausgeschlossen:** manuelle Änderung von WP-Artikeltexten, pauschale Display-Werbung auf jedem Versicherungs-R3, neue Vergleichsseiten/Kategorien ohne Prüfung, selbst erfundene Tarifcheck-Werbemittel oder ein zweites Affiliate-System.

## 9. Verbindliche Ergänzung 11.11.2026 – ALLE Versicherungs-Werbeplätze fachlich belegen; genaue Backend-Prüfung

**Nutzerentscheidung:** Möglichst alle vorhandenen Bannerplätze im gesamten Versicherungsbaum (R1, alle fünf R2, alle R3, Blattkategorien und passende Artikel) mit **echter Versicherungs-Partnerwerbung** belegen. Keine Amazon-/Produktwerbung. Fachlich passende Ersatzbanner sind ausdrücklich erwünscht, aber keine unrichtige Versicherungsaussage. Fehlende Positionen werden systematisch dokumentiert, Anbieter gesucht und abgearbeitet. Nicht aus Fantasie behaupten, 100 % seien belegt.

### 9.1 Tatsächlich vorhandene Bedienung im HAB-004 RC18 (Quellprüfung, keine Vermutung)

**Backend Affiliate-Zentrale → Banner & Werbemittel** (`affiliate-portal-creative-library`):
- Dropdown **„Aufgenommener Partner“ → „Direktpartner · Tarifcheck“** existiert bereits. Provider/Partner werden zentral gespeichert.
- **Mehrere Banner-Codes gesammelt einfügen:** akzeptiert vollständige Bildlink-Banner-Codes in der Form `<a ...><img ...></a>` (nicht iframe, JavaScript-Tarifrechner oder bloße Textlinks), oder CSV/JSON/TXT.
- **Banner händisch einfügen:** einzelne Bild-URL und Tracking-Link **beide Pflicht**; optional Banner-ID, Titel, reale Ziel-URL, Beschreibung, Tags/Kategorie, Breite, Höhe. Button „Banner händisch speichern“.
- Ergebnis ist **Import/Speicherung und technische Freigabeprüfung**, keine automatische Veröffentlichung. Die existierende Zuordnung aus Ziel-URL ist bereits vorhanden, zielt jedoch bei Tarifcheck bislang auf einen abweichenden „Wissen > Versicherungen & Recht“-Pfad. Das neue Versicherungs-Welt-Mapping und vollständige Sperre sind Teil der laufenden HAB-004-Entwicklung; **vor dem fertigen Update keine Garantie für die richtige Ausspielung**. Acht Originalgrößen je Angebot können getrennt eingefügt werden; doppelte identische Codes nicht mehrfach importieren.
- **Tarifcheck „Finanzen“ nicht unter dem Versicherungsbereich einsetzen.**

**Backend Affiliate-Zentrale → Rechner & Textlinks** (`affiliate-portal-tariff-tools`):
- **Tarifrechner anlegen:** Felder „Rechnername / Typ“, „HTML-Code“, Checkbox „aktiv“. Beim Speichern entsteht ein stabiler Platzhalter; die bestehende Technik rendert ihn nur, wenn er im vorgesehenen Inhalt/Template aufgerufen wird. **Wichtig: Speichern allein platziert keinen Rechner automatisch in jeder passenden Versicherungsseite.** Für die zentral gesteuerten Vergleichs-Kategorieseiten ist eine gezielte, geprüfte Übergabe an den bestehenden Designslot nötig; kein manuelles Einsetzen in WP-Artikel.
- **Affiliate-Textlinks:** Felder „Partner / Programm“, „Bezeichnung“, kompletter Partnercode optional ODER sichtbarer Linktext + Tracking-Link, reale Ziel-URL optional, Status. Auch hier speichert das Plugin einen stabilen Platzhalter, die automatische fachliche Ausspielung ist **nicht** durch das bloße Speichern gewährleistet.
- Externe Rechner/iframes nur mit echten Partnercodes und Datenschutz-/Mobilprüfung aktivieren.

### 9.2 Verbindliche Ausspielungsrangfolge (100-%-Abdeckungsziel)

1. **Passender Originalbanner der exakten Versicherung** (Priorität 1, jeweils zum Platzformat passend).
2. **Nachweislich passende verwandte bzw. übergeordnete Versicherung** (Priorität 2). Nur wenn tatsächlich dieselbe Produkt-/Risikoart, Zielgruppe und Leistung umfasst ist. Beispiel: Motorrad-Kfz nur wenn das Ziel Motorrad wirklich einschließt. Sonst keine suggerierte spezifische Deckung.
3. **Konkreten fehlenden Versicherungsanbieter bei Awin und ADCELL recherchieren** (Priorität 3). Nur tatsächlich freigegebene, provisionsfähige Programme ergänzen, keine zweite technische Partnerengine bauen.
4. **Originaler allgemeiner Versicherungs-/Vergleichsbanner von Tarifcheck (oder einem belegten Versicherungsvergleichspartner)** (Priorität 4), **nur wenn ein solches Werbemittel samt richtiger allgemeiner Versicherungszielseite und Partnerlink wirklich existiert** und auf der konkreten Seite keine falsche Spezialdeckung suggeriert. Der vorhandene Tarifcheck-Auftritt bewirbt Versicherungen UND Finanzen; nicht jeden Shop-/Startseitenbanner blind für Versicherungen freigeben. Für R1 kann alternativ eine fachlich ausgewogene Rotation mehrerer zugelassener Einzelversicherungsbanner verwendet werden, wenn es keinen belegten allgemeinen Versicherungsbanner gibt.
5. **Soll weiterhin ein Platz unbelegt bleiben**, wird der echte fehlende Banner im Prüfbericht/Export ausgewiesen und gezielt ein neuer Partner gesucht. Keine erfundenen Werbemittel, kein beliebiger „Versicherungen“-Kreativtext als nicht provisionsfähiges Fantasiebanner, kein Rückfall auf Amazon/Produkt-/Finanzwerbung. Das Abdeckungsziel ist **100 %**, aber ohne echte Partnerassets ist eine bereits erreichte 100-%-Belegung nicht nachweisbar.

**Wichtig:** Rangfolge gilt für **alle** R1/R2/R3/Blatt-/Artikelplätze; ein großer R1-Bereich bekommt mindestens eine echte Versicherungswerbung, eine R2-Seite mindestens ein Produkt ihrer Gruppe, eine fachlich spezifische R3-Seite bevorzugt exakt diese Versicherung. Bei Artikeln breite oder rechteckige/square Slots formatgerecht; nicht dasselbe Motiv mehrfach pro Seite durch Desktop- und Mobilcontainer. Rechnermodul einmal in passender Vergleichsumgebung, keine pauschale Formularüberflutung.

### 9.3 Benutzer-Workflow vor der Plugin-Freigabe

1. **Jetzt darf der Nutzer alle vorhandenen echten Bildbanner aus Tarifcheck zentral eintragen.** Ideal: pro Versicherung sämtliche geeigneten Formate in einem Import mit vollständigen `<a><img>`-Codes; zuordnungsrelevanten Produkttitel/Tags nennen. Einzelbanner optional über Bild-URL+Tracking-Link. Möglichst **auch** das jeweils vorhandene große Querbanner und 300×250; 125×125 nur für kleine Quadratslots.
2. **Tarifrechner separat** unter „Rechner & Textlinks → Tarifrechner anlegen“ sammeln. **Direktlinks separat** unter „Rechner & Textlinks → Affiliate-Textlinks“. Nicht alle drei Werbearten in dieselbe Banner-Importmaske kopieren.
3. **Im Weiteren übernimmt das Plugin** nach fachlicher Kontrolle: belegte Originalziel-URL → tatsächliche Versicherungsart → sicherer Zweig im aktuellen Kategorie-Snapshot → Freigabe/Format → beste passende Platzierung; globaler Versicherungsschutz gegen Amazon und andere Nichtversicherungs-Provider. Bei unklaren Versicherungsarten genaue Lückenliste und Partnerrecherche statt Spekulation.
4. **Neue Version vor Livebetrieb umfangreich testen:** Import aller Tarifcheck-Rubriken, echte R1/R2/R3/Blatt-/Artikelkontexte, andere Hauptwelten, alte manuelle Fremdbanner, fehlender Aktionslink, offene Datenschutzprüfung für Rechner, unpassende Versicherung, Platzhalter und Desktop-/Mobilformate. Kein automatisch veröffentlichter Banner ohne echte Partnerlinks.

**Quellnachweis Backend:** aktuelles HAB-004 RC18/CURRENT.zip, `includes/trait-ppar-creative-library.php` und `includes/trait-ppar-tariff-tools.php`, Menü in `affiliate-portal-router.php`; isoliert am 11.11.2026 erneut geprüft. Tarifcheck bietet öffentlich Banner, Direktlinks, Rechner an, aber der **konkrete allgemeine Versicherungsbanner** ist mit den Nutzer-Screenshots noch nicht belegt.

**Status:** Diese Eintrags-/Fallback-Regel ist Konzept und Anweisung. Der Stand **RC19 wird separat entwickelt und geprüft**. Bestehendes offiziell abgelegtes HAB-004 RC18 bleibt bis zur Freigabe unverändert.


## 10. RC19-IMPLEMENTIERUNG (überschreibt ältere Leerstand-Regeln) 11.11.2026 – Alle Versicherungs-Bannerplätze belegt

Dieser Abschnitt ersetzt ältere widersprechende Leerstelle-/Fallback-Hinweise der Abschnitte 1–8.

**Umfang:** Hauptseite Versicherungen (R1), fünf R2-Hauptbereiche, alle vorgesehenen 46 R3-Themenseiten, alle 323 vorgesehenen WP-Endkategorien, eindeutig zugeordnete Fachbeiträge sowie sicher erkennbare Versicherungs-Glossareinträge. Keine Änderung des bestehenden Kategoriebaums.

**Belegungsreihenfolge pro Werbeplatz:**
1. Fachlich EXAKT passendes, freigegebenes Tarifcheck-Versicherungsangebot inklusive Original-Werbemittel und Ziel.
2. Fachlich EXAKT passendes Angebot von Awin bzw. ADCELL, sofern zugelassen und geprüft.
3. Tatsächlich zum konkreten Themenkreis PASSENDER Versicherungsvergleich eines übergeordneten Bereichs; niemals Kfz als Ersatz für Boot oder PKV als Ersatz für Pflege.
4. ECHTER allgemeiner Versicherungsvergleich von Tarifcheck, nur wenn hierfür eine freigegebene Original-Versicherungszielseite, Banner und Partnerlink verfügbar sind. Nicht die pauschale Tarifcheck-Startseite mit Kredit, Strom und Girokonto.
5. Als letzter verlässlicher Fallback ein **eigener Hab-&-Bewahr-Versicherungs-Themenbanner mit geprüftem internen R1-/R2-Link**. Dieser enthält keine erfundenen Leistungs- oder Provisionsversprechen und ist als „Eigener Themenhinweis“ erkennbar.

**Achtung:** „alle Plätze belegt“ bedeutet die auf den Seiten VORGESEHENEN Bannerpositionen – nicht, dass ehemalige Produktkarten oder doppelte Desktop-/Mobilwerbung zwanghaft mit Reklame vollgestopft werden. Keine Fake-Tarifcheck-Anzeige. Im Versicherungszweig keinerlei Amazon-/eBay-/Idealo-Produkte, Dokumententaschen, Produkt-Demos oder Kreditbanner.

| Webseite | Belegung |
| --- | --- |
| R1-Versicherungen | mindestens ein breiter Fachbanner; bei Partnerlücke interner R2-Themenbanner |
| Fünf R2-Bereiche | mindestens ein breiter Banner passend zum Bereich; bei Lücke interner Bereichshinweis |
| 46 R3-Themenseiten | jeweilige Versicherung, sonst sachlich passende allgemeine Versicherung, sonst eigener interner Banner |
| 323 WP-Endkategorien | passende Versicherung im vorhandenen Querplatz, sonst interner Themenbanner |
| Fachbeiträge | vorhandener Seitenleistenbanner: Original 300×250 oder kleines 125×125 oder interner Themenhinweis, keine zweite automatische Bild-/Produktkarte |
| Vergleichen | nur auf fachlich richtiger Vergleichsseite vollständiger Original-Tarifrechner nach Datenschutzfreigabe; Direktlink an passenden Ratgebern |
| Glossar | nur bei sicherer Versicherungs-Zuordnung, dann echter geeigneter Partnerbanner oder interner Themenhinweis; keine thematisch erratene Werbung |

**RC19-Umsetzung:** Das vorhandene Affiliateplugin HAB-004 wird als vollständige Folgeversion 0.1.16-rc19 gebaut. Die zentrale Kategorie-Abstammung wird aus dem bereits aktiven WordPress-Snapshot gelesen; Auswahl, Freigabe, Bannerplatz, erlaubtes Format und das Verbot von Amazon-Fallbacks liegen im bestehenden Plugin. Alle sechs anderen Schutzwelten und das Design RC19 bleiben unangetastet. Keine neuen Tabellen, keine neuen Frontend-HTTP-Suchen. Die geprüften Originalgrößen von Tarifcheck (728×90, 468×60, 300×250, 125×125) behalten ihre Originalproportionen; das 300×250 ist KEIN Quadrat.

**Prüfung:** ausgeführter PHP-Test der tatsächlich gebauten ZIP mit 1 R1, 5 R2, 46 R3, 323 Endkategorien und Fachartikeln, negative Fälle, fremde Welten, Formatregeln und interne Fallback-Banner. Erst nach grünem Test und GitHub-Merge ist die vollständige ZIP offiziell im HAB-Pluginbüro. Echte WordPress-Liveabnahme ist separat erforderlich.

**Offen bis Originaldaten verfügbar:** Die echten Tarifcheck-Banner-Einbettungscodes und Direktlinks (Partnerkonto) sind noch nicht übergeben. Deshalb können hier keine echten Tarifcheck-Provisionen oder 100 % bezahlte Werbeflächen zugesichert werden. Das Plugin sorgt zunächst für sichtbare, interne Themenbanner in jedem unbesetzten Versicherungs-Bannerplatz. Awin und ADCELL bleiben für nachgewiesene Lücken integrierbar. Keine manuellen Änderungen an WP-Beiträgen.
