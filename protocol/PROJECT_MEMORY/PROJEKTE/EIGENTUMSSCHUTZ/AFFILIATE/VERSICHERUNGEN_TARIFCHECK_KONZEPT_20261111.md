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
