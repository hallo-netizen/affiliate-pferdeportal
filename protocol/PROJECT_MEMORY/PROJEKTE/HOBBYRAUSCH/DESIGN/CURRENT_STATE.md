# HOBBYRAUSCH – DESIGN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-18
STATUS: **1.50.686 KETTENHEMDFLECHTEN-PILOT NUTZERSEITIG AUF DEN ERSTEN BLICK OK / 1.50.687 GLEICHE DETAIL-EBENE PORTALWEIT AUSGEROLLT / ZENTRALE LAST-LEVEL-ICONS / 4 KETTENHEMD-DUMMYBEITRÄGE / LOKAL PASS / WORDPRESS-READBACK OFFEN**

Zielvertrag: **ZV-HOBBYRAUSCH-DESIGN-001 Fassung 5.1 / 2026-10-18**

## KANDIDAT 1.50.687

Artefakt:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.687_CATEGORY_LEVEL_ROLLOUT_ICONS_DUMMY_POSTS.zip`

SHA-256:
`9a881f3b3b7cf25ab2cfdc5f9a2c62b878fa5cc7513ba8678524f98b7464235b`

## SCOPE – GLEICHE LOGISCHE EBENE WIE KETTENHEMDFLECHTEN

Aktueller Zielbaum:
- **379 Page-Knoten** auf dieser Ebene;
- zusätzlich **16 direkte Category-Term-Knoten** derselben logischen Ebene;
- insgesamt **395** Detail-Hubs;
- unter den 379 Page-Knoten aktuell **2.979 letzte Kategorien**.

Für diese Ebene gilt jetzt zentral:
- kein Hero-Bild;
- kompakter mittiger Kopf mit thematischem Icon + H1;
- 150–200-Wörter-Fachtext nach den bestehenden Textregeln;
- 45–62 Wörter sichtbar, Rest per Chevron;
- Desktop 4er-Raster, Tablet 2er, Mobil 1er;
- vorhandene Produkte/Banner früher zwischen den Inhalten;
- bis zu 4 passende Beitragsvorschauen mit Bild;
- keine neuen Affiliate-Slottypen.

## TEXTE

- 395/395 Texte vorhanden;
- Wortumfang **150–170**;
- sichtbare Leads **45–62 Wörter**;
- 395/395 Volltexte unterschiedlich;
- Kettenhemdflechten bleibt inhaltlich auf dem abgenommenen 162-Wörter-Pilottext;
- offensichtliche Fachfehler der ersten automatischen Rohfassung wurden vor Release nachbearbeitet, insbesondere Genuss/Fermentation sowie Aquaristik, Imkerei, Ameisen/Insekten und Gehegebau.

## ZENTRALE ICON-STEUERUNG LETZTE KATEGORIEEBENE

Keine zufällige/hash-basierte Iconwahl mehr.

Semantische Rollen werden zentral auf Icons abgebildet, unter anderem:
- FAQ;
- Vergleich/Kaufberatung;
- Einstieg/Grundlagen;
- Ausrüstung/Kosten;
- Werkzeuge;
- Materialien;
- Muster;
- Sicherheit;
- Pflege/Probleme;
- Dokumentation;
- Aufbewahrung;
- Bestimmung/Messen;
- Arten/Sorten;
- Klima;
- Futter;
- Standort;
- Technik;
- Projekt/Finish;
- Farbe;
- Vorbereitung;
- Bau/Montage;
- Elektronik;
- Wasser;
- Pflanzen.

Damit erhält z. B. **FAQ portalweit dasselbe FAQ-Icon** und Vergleich/Kaufberatung dasselbe Vergleichs-Icon.

Für nicht explizit klassifizierte letzte Kategorien wird der fachliche Eltern-/Themenkontext verwendet; keine zufällig wechselnden Icons.

## KETTENHEMDFLECHTEN – 4 DUMMYBEITRÄGE

1. `Kettenhemdflechten: Ringe sauber öffnen und schließen`
2. `European 4-in-1: Das Grundmuster sauber aufbauen`
3. `Welche Ringe und Zangen passen für den Einstieg?`
4. `Kanten und Abschlüsse am Kettengeflecht sauber fertigstellen`

Eigenschaften:
- als veröffentlichte Dummy-Posts angelegt;
- jeweils einer passenden Kettenhemd-Unterkategorie zugeordnet;
- jeweils mit Beitragsbild;
- Seeder idempotent;
- Vorschauabfrage zieht maximal 4 Beiträge aus den direkten Unterkategorien.

## QA

- PHP **105/105 PASS**;
- reale Front-Route → V150687 PASS;
- reale Content-Route → V150687 PASS;
- beide V150687-Templates positiv ausgeführt PASS;
- Negativtest mit ausschließlich V150686 scheitert erwartungsgemäß;
- Kettenhemd-Pilotrender: kein Hero, 1 H1, 8 Karten PASS;
- zentrale Iconrollen FAQ / Vergleich / Grundlagen / Ausrüstung geprüft;
- 4 Dummy-Posts + 4 Kategoriebindungen + 4 Featured Images PASS;
- zweiter Seedlauf erzeugt keine Duplikate;
- Postpreview-Abfrage: Limit 4 und alle 8 direkten Kettenhemd-Unterkategorien als Quelle PASS;
- Copy-Coverage: 395/395 PASS;
- 379 Pages + 16 direkte Terms PASS;
- 2.979 letzte Kategorien im Scope;
- Delta zu 1.50.686: **1 bestehende Datei geändert + 4 Dateien neu + 0 entfernt**;
- Dirty Overlay 1.50.686 → 1.50.687 aktive Kette PASS;
- ZIP PASS;
- Roundtrip **1146/1146 byte-identisch**.

## EXAKT EINE NEXT ACTION

**1.50.687 installieren und zuerst Kettenhemdflechten prüfen: 4 Dummy-Beiträge mit Bildern, neue zentrale Icons und gemischte Seitenreihenfolge. Danach zwei weitere Detail-Hubs derselben Ebene stichprobenartig prüfen.**

## NICHT ANFASSEN

- Hub2-Hero-Logik nicht erneut ändern;
- Kategoriebaum nicht ändern;
- keine neuen Affiliate-Slottypen;
- keine zufällige Iconwahl;
- Dummy-Beiträge nicht als finale Fachartikel behandeln.
