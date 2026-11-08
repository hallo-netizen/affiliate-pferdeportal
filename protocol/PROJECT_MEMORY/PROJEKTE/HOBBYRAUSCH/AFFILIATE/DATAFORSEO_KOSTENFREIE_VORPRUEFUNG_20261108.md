# Hobbydepot: DataForSEO-Produktbefüllung – Quellenprüfung vom 08.11.2026

Status: ausschließlich Datenprüfung. Keine kostenpflichtige DataForSEO-Abfrage, kein Produkt veröffentlicht, keine neue Plugin-Version.

## Echte Quellen
- HD009 0.1.28: DataForSEO-Recherche derzeit nur nach Klick im Backend. Einzelne ASINs benötigen manuelle Freigabe in der vorhandenen WordPress-Option hdar_amazon_approved_v1. Ohne Freigabe bleibt eine Produktbox leer.
- Hab & Bewahr HAB-004: eigener geprüfter DataForSEO-Automatiklauf mit Tageslimit, Auftragsabfrage und eindeutigen Fehlerhinweisen. Der vollständige Produktkartenbetrieb ist aber noch nicht abgenommen; echte Amazon-Produktbilder fehlen.
- HD007: 862 von 862 Hobbydatensätzen haben einen geprüften Text zum benötigten Material oder zur Ausrüstung.
- HD003: der aktuelle Kategoriestamm liefert die fachliche Zielzuordnung für sämtliche Kategorieseiten.

## Abgleich Register zu bestehenden Hobbyzielen
- Distinkte Hobby-Slugs der aktuellen HD003-Kategoriemappe: 381
- Eindeutiger Namensabgleich mit Hobbyregister: 381
- Ohne automatischen Namensabgleich: 0
- Mehrdeutige Mehrfachkandidaten: 0
- Erste kompakte Ausrüstungsphrasen als mögliche Recherchewörter: 246
- Erster Ausrüstungsbegriff für direkte Recherche zu ungenau: 135

Diese Begriffe sind keine fertig geprüften Produktempfehlungen. Keine automatische Übernahme fachlich ungeeigneter Artikel.

## Beispielhafte Eingaben zur Prüfung
| Welt | Hobby | Ausrüstungsphrase | Einschätzung |
|---|---|---|---|
| bewegen | 3D-Bogenschießen | Bogen | Noch prüfen |
| bewegen | Angeln | Rute | Noch prüfen |
| bewegen | Balance Board | Balance Board und eine freie | Noch prüfen |
| fertigen | Automodellbau | Modellbausatz | Suchwort-Kandidat |
| fertigen | Bean-to-Bar-Schokolade | Kakaobohnen | Suchwort-Kandidat |
| fertigen | Besenbinden | Reisig oder Fasern | Noch prüfen |
| fertigen | Buchbinden | Papier | Noch prüfen |
| forschen | Amateurastronomie | Freier Himmel; optional Fernglas | Noch prüfen |
| forschen | Astrofotografie | Kamera | Noch prüfen |
| forschen | Bioakustik | Audiorecorder oder Mikrofon | Noch prüfen |
| gestalten | Airbrush | Airbrushpistole | Suchwort-Kandidat |
| gestalten | Architekturmodellbau | Karton | Noch prüfen |
| gestalten | Batik | Stoff | Noch prüfen |
| pflanzen | Aeroponik | Aeroponik-System | Suchwort-Kandidat |
| pflanzen | Bonsai | Bonsai oder Jungbaum | Noch prüfen |
| pflanzen | Bromelien | Bromelie | Suchwort-Kandidat |
| pflanzen | Chili-Zucht | Saatgut | Noch prüfen |
| sammeln | alte Computer | Platz | Noch prüfen |
| sammeln | alte Schlüssel | Aufbewahrung | Suchwort-Kandidat |
| sammeln | Banknoten | Schutzhüllen oder Album und verlässliche Bestimmungshilfen | Noch prüfen |
| technik | 3D-Druck | 3D-Drucker | Suchwort-Kandidat |
| technik | 3D-Scanning | Scanner oder Smartphone | Noch prüfen |
| technik | alte Spielekonsolen restaurieren | Werkzeug | Noch prüfen |
| tiere | Ameisenhaltung | Formicarium | Suchwort-Kandidat |
| tiere | Artemia-Zucht | Behälter | Suchwort-Kandidat |
| tiere | Asselhaltung | Behälter | Suchwort-Kandidat |
| tiere | Käferzucht | Zuchtboxen oder Terrarium | Noch prüfen |
| tiere | Quallen-Aquarium | Kreisel- oder Quallenaquarium | Noch prüfen |

## Fehlende Zuordnungen
Keine.

## Bewährte und offene Schritte
1. Bereits vorhandene DataForSEO-Verbindung und Produktplatzierung in HD009 behalten; keinen zweiten Workflow, keine neue Produktdatenbank und keine weitere Portalverknüpfung.
2. Hab-Worker nur mit seinem mehrfach getesteten Status-/Tageskostenlimit und kostenfreiem Task-GET als Muster benutzen, nicht das fremde Kategorie-/Tracking-Setup übernehmen.
3. Recherchebegriff aus dem geprüften Materialbedarf ableiten; zunächst sichere Beispiele wie Sportdrachen: Lenkdrachen und 3D-Druck: 3D-Drucker. Die unklaren Fälle bleiben gesperrt.
4. Nach dem Abruf exakte Amazon.de-Ziel-URL, Produkt-ASIN, Produkttitel und fachliche Eignung gegenprüfen. Keine Preise, Bestände oder Bilder aus DataForSEO ungeprüft übernehmen.
5. Amazon-Bilder für einzelne Produktkarten nur über eine vertraglich freigegebene Amazon-Inhaltsquelle wie Creators API oder PA API. Erst danach gelten bebilderte Produktboxen als fertig.

Dieses Protokoll ist ein Prüfstand, kein Live-Nachweis und kein freigegebenes Installations-Plugin.

## Geprüfter ausführbarer Nachweis

- Prüfskripte nur auf der isolierten Arbeitsbranch `hobbyroom/hd009-amazon-dfs-products-audit-20261108`; die zwei produktiven Plugin-ZIPs HD009 und HAB-004 wurden **nicht verändert**.
- GitHub Actions Lauf 42473803764: 381/381 aktuelle Hobbyseiten eindeutig mit dem Register verbunden; 246 konservative erste Suchwörter, 135 unklare und deshalb vor einer automatischen Bezahlung gesperrte Startwörter; zehn synthetische positive und negative ASIN-/Host-/Titelprüfungen bestanden.
- Die automatischen DataForSEO-Aufträge aus Hab sind ein **Ansatz**, nicht auf Hobbydepot live übernommen. Keinen bezahlten DataForSEO-Aufruf ohne aktivierte Kostenfreigabe auslösen.
- Offizielles Hab-GitHub-CURRENT ist HAB-004 0.1.8-rc11. Spätere RC12 bis RC15 sind laut den abgelegten Statusdokumenten Test-/Chat-Stände, **nicht** als amtlicher GitHub-CURRENT nachgewiesen. Die Live-Produktdarstellung der RC11 hatte belegte Bildprobleme.
