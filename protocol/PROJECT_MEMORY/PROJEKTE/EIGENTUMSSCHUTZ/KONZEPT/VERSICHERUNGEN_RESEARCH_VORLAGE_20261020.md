# Hab & Bewahr – Versicherungen: Forschungsauftrag und Architektur-Vorentwurf (20.10.2026)
STATUS: KONZEPT / NICHT DATAFORSEO-VALIDIERT / KEIN WP-IMPORT / KEIN SOFTWARE-UMBAU

## Festgelegte Nutzervorgaben
- Vollwertige zusätzliche Hauptkategorie **Versicherungen**, grundsätzlich offen für alle Versicherungsarten, einschließlich Leben, Rente, Gesundheit und Gewerbe, auch wenn außerhalb des bisherigen Eigentumsschutzschwerpunkts.
- Dasselbe vorhandene Seitenmodell: Hauptbereich -> kurze Themenseiten (ggf. mehrere Ebenen) -> letzte konkrete Themenseite = **genau eine Versicherung/Versicherungsart** -> direkt darunter ausreichend differenzierte *flache Beitragskategorien* -> mehrere Einzelbeiträge. Keine neuen Hierarchieebenen oder zweiter WP-Kategorie-Importer.
- Auf vorhandenen Gefahren- und Objektseiten thematisch passende Versicherungs-Banner/Links. Immer auf die exakt einschlägige Versicherungsseite, nicht pauschal auf Homepage. Zentrale Bannerverwaltung wiederverwenden.
- Separater **Versicherungsfinder**: im Magazin auffindbar; Einstiege auf Startseite, Versicherungs-Hub und passenden Beiträgen. Führt zuerst zu Versicherungsarten und erklärenden Seiten, nicht zu Affiliate-Anbieterbewertungen. Keine individuelle Tarifempfehlung ohne rechtliche Prüfung.
- Keywords über **DataForSEO vor endgültiger Hierarchieentscheidung oder WordPress-Schreibvorgang**. Ohne nachgewiesene echte API-Response keine Kennzahlen behaupten.

## Vorläufiger Seitenbaum – ausschließlich Hypothesen für Keyword-Recherche
R1: Versicherungen
R2 / R3 Themensortierung (für Navigation kurze Labels, physische Ebene nach existierendem Schema, keine Pflicht, jede Zwischenebene zu verwenden):
1. Wohnen & Eigentum
   - Hausratversicherung, Wohngebäudeversicherung, Elementarschadenversicherung (Deckungsbaustein; prüfen, ob eigenständige Versicherung oder nur Unterthema Wohngebäude), Glasversicherung, Fahrradversicherung (OWNERSHIP bei Mobilität, hier nur Verweis!)
2. Mobilität & Reisen
   - Kfz-Haftpflichtversicherung, Kaskoversicherung (prüfen ob eigenständiger Owner oder Kfz-Versicherung als eins), Wohnmobilversicherung, Wohnwagenversicherung, Motorradversicherung, Fahrrad-/E-Bike-Versicherung, Bootsversicherung, Auslandskrankenversicherung (OWNERSHIP Gesundheit oder Reisen festzulegen), Reiserücktrittsversicherung, Reiseabbruchversicherung, Reisegepäckversicherung
3. Haftung & Recht
   - Privathaftpflichtversicherung, Tierhalterhaftpflichtversicherung, Haus- und Grundbesitzerhaftpflichtversicherung, Rechtsschutzversicherung (Unterarten nur soweit jeweils eigenständig sinnvoll)
4. Gesundheit & Pflege
   - Private Krankenversicherung, Gesetzliche Krankenversicherung (Informationsbereich; nicht pauschal Affiliate), Krankenzusatzversicherung (Zahnzusatz nur eigener Owner bei Keywordbeleg), Pflegezusatzversicherung, Krankentagegeldversicherung
5. Leben & Vorsorge
   - Risikolebensversicherung, Kapitallebensversicherung, Private Rentenversicherung, Berufsunfähigkeitsversicherung, Erwerbsunfähigkeitsversicherung, Unfallversicherung, Sterbegeldversicherung
6. Beruf & Betrieb
   - Betriebshaftpflichtversicherung, Geschäftsinhaltsversicherung, Betriebsunterbrechungsversicherung, Berufshaftpflichtversicherung, Vermögensschadenhaftpflichtversicherung, Cyberversicherung für Kleinbetriebe; größere Industrie-/Konzern-Risiken sind nicht Zielgruppe.
7. Tiere & Freizeit (nur bei eigenständigem Nachfrage-/Beitragsbeleg)
   - Hundehaftpflicht (OWNERSHIP bei Haftung & Recht), Tierkrankenversicherung, Pferde-OP-Versicherung, Camping-/Sportgeräte-Sachversicherung (Leistungen/Existenz prüfen, keine künstlich benannten Policen); crosslinks statt Seitenkopien.
Diese Liste ist bewusst keine Anzahl finaler physischer Seiten. DataForSEO kann R2 und R3 verdichten/verschieben.

## Rechercheplan/DataForSEO-Input
Pro Kandidat:
- zentraler Suchbegriff: `hausratversicherung`, `wohngebäudeversicherung` usw.
- Varianten: `kosten`, `vergleich`, `leistungen`, `was ist versichert`, `welche schäden`, `selbstbeteiligung`, `ausschlüsse`, `kündigen`, `wechseln`, `schadensmeldung`, `für wen sinnvoll`.
- Standort Deutschland, Sprache Deutsch; monatliches Suchvolumen, Wettbewerbsindikator, ggf. CPC mit Quelle, Abfragezeitpunkt und Datenqualität festhalten.
- Negative/mehrdeutige Begriffe markieren, ähnliche Intentionen clustern, **eine Suchintention/ein konkreter Versicherungsowner**, Querverweise statt doppelter Seite. Unterschiedliche Versicherungen/Deckungsbausteine fachlich prüfen.
- Auf **unterster Themenseite mindestens grob 3–5 fachlich eigenständige spätere Beitragsideen je sinnvoller flacher Beitragskategorie**, keine Artikeltitel jetzt generieren. FAQ und Beratung als Standardprüfungen; Vergleiche bei eigenständigem Mehrwert; weitere Kategorien nur nach Substanz. Nicht jede Versicherung blind nach Schema F auffächern.
- Ergebnisse nach Priorität: 1) Bestandsschutz-Eignung/vernünftige Einordnung, 2) Nachfrage, 3) unabhängige Inhaltsbreite, 4) Wettbewerb/Affiliate-Eignung. Keine künstlichen Lückenfüller.

## Versicherungsfinder – Minimalmodell
1. WEN? privat / kleine Betriebe
2. WAS? Wohnung/Gebäude/Bewegliches Eigentum/Fahrzeug/Tier/Gesundheit/Einkommen/Familie/Alter/Reisen/Betrieb
3. WELCHES ZIEL/RISIKO? Schaden an Sache, Haftung, Krankheit, Ausfall, Hinterbliebene, Ruhestand etc.
4. AUSGABE: maximal wenige *mögliche Versicherungsarten* mit kurzer Erklärung, typischen Lücken/Ausschlüssen, neutrale Links auf zentrale Ownerthemenseiten; optional Vergleichsanbieter erst danach. Keine personenbezogene Risikoanalyse, Gesundheitsdaten oder konkrete Tarifentscheidung ohne gesonderte Datenschutz-/Rechtsprüfung (insbesondere Vermittlungs-/Beratungsabgrenzung).
- Eine zentrale wartbare Zuordnung Risiko -> Versicherungsowner/URL, gemeinsam von Finder, Bannern und Fachbeiträgen genutzt; keine konkurrierenden Linklisten. Bestehendes Affiliate-/Banner-/Textlinksystem prüfen, bevor programmieren.
- Keine Versicherungsbanner an Orten, für die die Police sachlich nicht passt; keine irreführende Behauptung, alles sei gedeckt.

## Exakte Prüfung des vorhandenen Campusstands (20.10.2026)
- `KONZEPT/CURRENT_STATE.md`: vorhandene 265 Themenowners, fachliche 471er Ergänzung (nicht live) und 1.14.8.32 Release.
- `KATEGORIEN/CURRENT_STATE.md`: ein einziges zentrales Kategorieplugin und separater freizugebender C2.3-Import (471; bestehende 1323 Kategorien schützen; 743/472 nie neu importieren).
- Die schon vorhandene WordPress-Backendfunktion **`Portal-Kategorien → SEO-Namen prüfen`**, die Klassen **`APKW_DataForSEO`** und **`APKW_Category_SEO_Audit`** sowie ein echter Germany/de-Export vom 16.10.2026 (570 Begriffe, 51 Ergebnisse, 0,01812 USD) sind in `KATEGORIEN/CURRENT_STATE.md` ausdrücklich belegt. Die neuen Versicherungsbegriffe sind **noch nicht** abgefragt; in diesem Chat keine neue kostenpflichtige DataForSEO-Abfrage ausgeführt und keine Suchvolumina erfunden.
- Neues Versicherungsmodul darf vorherige C2.3-NEXT-ACTION nicht überholen oder heimlich mitschreiben. Reiner Entwurf hier im Konzeptbüro.

## Genau eine nächste fachliche Aktion
Versicherungs-Zielbaum als **nur additive Kandidaten** im vorhandenen Kategorienkonzept erfassen und den bestehenden WordPress-Backendpunkt **`Portal-Kategorien → SEO-Namen prüfen`** für eine gezielte Germany/de-Namensrecherche nutzen; kostenpflichtige Ausführung nur mit expliziter Freigabe. Danach deduplizierten Seitenbaum mit eindeutigen Themenowners und je drei bis fünf eigenständigen Beitragsansätzen ableiten. **Bis dahin keine WordPress-Kategorien oder Versicherungsfinder installieren.**
