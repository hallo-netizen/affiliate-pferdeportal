# Büro Roboterregister / einheitliche Eigenschaften

## AKTUELL 15.11.2026 – EIN ROBOTERTYPEN-MASTER REVISION 20
- **`../../KATEGORIE/RECHERCHE/PRODUKTE_V2_20261108.json` Revision 20** ist die **einzige** Typen-/Eigenschaftsdatenquelle: 68 ursprüngliche Kandidaten und 189 Forschungsrandfunde, alte IDs erhalten. Fachlicher 19→16+3-Grundlagenabschluss im Feld `category_release_v84`. **Keine weitere breite Rechercherunde erforderlich.**
- Bei **16** für den letzten Kategorie-Nachtrag ausgewählten Typen einige begrenzte, belegte Finderfelder `finder_traits_v1` ergänzt. Noch unbestätigte Eignungs- oder Sicherheitswerte bleiben `NICHT_RECHERCHIERT`, nicht „nein“ oder „passt“. Ein einziger späterer Finder für alle Zielgruppen.
- **Die öffentliche Hersteller-/Modellseite ist ein anderer Datensatztyp**: aktueller Pilot `../../MAGAZIN/ROBOTERREGISTER/MODELLE_PILOT_V2.json` mit 19 eindeutigen Herstellermodellen/Projekten; keine zweite Robotertypenquelle und keine WP-Veröffentlichung. Die älteren Revisionen unten sind Projektgeschichte.

## AKTUELL 15.11.2026 – DATENQUELLE REVISION 18, WISSENSREGISTER BLEIBT EINE ANSICHT
- Der **einzige bestehende Robotertyp-Fachmaster** `../../KATEGORIE/RECHERCHE/PRODUKTE_V2_20261108.json` hat **Revision 18**, weiterhin 68 ursprüngliche Robotertypkandidaten, Forschungsrandbestand jetzt **189** statt 183. Neue V82/V83-Themen nutzen bestehende Forschungskennungen, soweit passend (Enabot `rf143`, Massage `rf158`, Nagelpflege `rf159`), statt doppelte Hersteller- und Produktlisten anzulegen.
- Acht mögliche neue Typseiten in der Kategorie-Fachplanung, **noch nicht WordPress oder Finder**; Stand in `../../KATEGORIE/CURRENT_STATE.md`, Detailbelege in `../../KATEGORIE/RECHERCHE/V82_FUENF_NISCHEN_BESTANDSABGLEICH_20261115.md`. Alles Folgende ist ältere Projekthistorie.

## AKTUALISIERUNG 15.11.2026 – EIN MASTER, KEIN ZWEITES REGISTER
- Der einzige gültige Robotertypen-Forschungsmaster `../../KATEGORIE/RECHERCHE/PRODUKTE_V2_20261108.json` steht auf **Revision 15: 68 unverschobene Basiskandidaten + 183 Forschungsrandkandidaten**. Zwei V80-Vorschläge referenzieren bestehende Typ-IDs `rf142` und `rf148`; neun Forschungsidentitäten `rf175–rf183` neu. **Nicht** in einer zweiten Produktliste ablegen.
- V80 hat die 11 Kandidaten gegen den vorhandenen 188er WordPress-Sollbaum verknüpft und 22 fachliche Rubriken / 88 mögliche Artikelrichtungen dokumentiert. Quelle `../../KATEGORIE/RECHERCHE/V80_11_TYPEN_ABGLEICH_ARTIKELPLAN_20261115.md`; die Such- und Findermerkmale sind **nicht automatisch voll erhoben**. Keine neuen WordPress-Objekte oder Produktkarten als bereits publiziert ausgeben.
- Stand 09.11.2026 und damalige Zählungen weiter unten sind **historisch**; die aktuelle Projektwahrheit steht ausschließlich in `../../KATEGORIE/CURRENT_STATE.md`.

Stand 09.11.2026 · SCHEMA EINGERICHTET, FAKTENRECHERCHE OFFEN

## Bewährtes Vorbild
- Hobbydepot: **862** Hobbyidentitäten mit **57** gemeinsamen Merkmalen, ein zentraler Bestand, lesende Register-/Finderansicht (`HOBBYRAUSCH/WISSENSDATENBANK/HOBBYREGISTER.md`; `HOBBY_EIGENSCHAFTEN_SCHEMA_1_2_DELTA.md`).
- Pferdeatelier: ein zentraler, quellengebundener Rassendatensatz pro Identität und stabiler Vergleich (`PFERDE_ATELIER/.../PFERDERASSEN/RASSEN_DATENMODELL.md`).

## Die eine Robotik-Datenquelle
[**Einziger Robotertypen-Master**](../../KATEGORIE/RECHERCHE/PRODUKTE_V2_20261108.json) – `KATEGORIE/RECHERCHE/PRODUKTE_V2_20261108.json`.

Darin sind **68 bisherige Robotertyp-Kandidaten** mit unveränderten `rb...` IDs und 20 Randkandidaten `rf...`; alle noch ungeprüft für WordPress. Jeder der 68 Kandidaten besitzt ab Revision **5** dieselben Felder `finder_traits_v1` mit Wert **NICHT_RECHERCHIERT**. **Das bedeutet Schema vorbereitet, nicht 68 Robotertypen tatsächlich klassifiziert.**

Das [Eigenschaftsschema](EIGENSCHAFTEN_SCHEMA_V1.md) beschreibt alle Felder und Prüfregeln. Kein zweites JSON/Excel mit denselben Roboteridentitäten oder Eigenschaften anlegen; neue Eigenschaften an derselben Roboter-ID ergänzen. Andere Büros, Kategorieplugin, Glossar und Finder dürfen diese Daten nur referenzieren, nicht heimlich neu klassifizieren.

## Status und nächste Arbeit
- Einheitliches Schema: **angelegt**. Tatsächliche Klassifizierung der Eigenschaften, Modelle/Preis/Finder-Eignung: **OFFEN**.
- Der Produkt-/Kategorien-Status wird **nur** in `../../KATEGORIE/CURRENT_STATE.md` geführt; kein zweiter CURRENT hier.
- Nächster sinnvoller Schritt: bei der ohnehin stattfindenden fachlichen Produktrecherche **zugleich** die passenden Merkmale und Belege erfassen, zuerst Konfliktfälle AMR/FTF/Palettentransport, SCARA/Delta, professionelle/private Fensterreinigung. Kein Nutzer-Upload nötig.

## Klare Rolle zum Magazinbüro
Dieses bestehende WISSENSDATENBANK-Büro definiert nur das Robotertypen-Eigenschaftsschema (eine `rb...`-Quelle). Die **öffentliche Registerfunktion** gehört zu [MAGAZIN/ROBOTERREGISTER](../../MAGAZIN/ROBOTERREGISTER/START_HERE.md) und untersucht **konkrete Hersteller-Modelle** als andere Datensatzart. Keine zweite Robotertypen-Datenwahrheit.
