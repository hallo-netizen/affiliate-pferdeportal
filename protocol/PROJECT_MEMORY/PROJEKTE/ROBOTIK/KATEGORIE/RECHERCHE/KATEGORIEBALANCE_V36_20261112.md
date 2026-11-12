# Robotik Kategorie V36 – sieben Hauptbereiche ausgebaut, 12.11.2026

## Was nachweislich geprüft wurde
- Verbindlicher `ZIELVERTRAG.md` mit drei Säulen, maximal 6–8 Hauptkategorien, einer konkreten Produktart je letzter Seite, genau einem Eigentümer, mindestens drei fachlich verschiedenen Beitragsabsichten je neuer Inhaltskategorie, nur belegten Produkten und KISS.
- `ARBEITSABLAUF.md`, `PRUEFREGELN.md` und exakter `assets/robotik-first-import-plan.json` aus der aktuellen Kategorie-Pluginlinie 0.4.2. Ergebnis: 104 WP-Seiten, 72 konkrete Produktseiten, 89 WP-Inhaltskategorien.
- Vorheriges Forschungsregister `/robotik/Recherchebüro/CURRENT.json` v35 mit 548 Fundnennungen. Alle 548 bestehenden Datensätze in v36 inhaltlich unverändert erhalten. 9 neue Recherche-IDs hinzugefügt; 2 vorhandene (ROB-0509 Katzentoilette, ROB-0524 Badminton) weiterverwendet. **557 Fundnennungen sind keine 557 kaufbaren Robotertypen.**
- 11 zusätzliche **Produktfunktions-Kandidaten** anhand konkreter Hersteller-/Händlerseiten plus je 3 unterschiedliche Fach-Themenrichtungen recherchiert. Herstellerbelege sind **kein** DataForSEO-/WordPress-Live-PASS.

## Neue Navigation bleibt exakt wie beschlossen
`Haushalt · Garten · Freizeit · Sport · Bildung · Pflege · Gewerbe` (7 Hauptpunkte, weder zusätzliche Landwirtschaftswelt noch Zusammenlegung erzwungen). Für Industrie unter Gewerbe weiterhin Verweise auf EINMAL vorhandene Produktseiten.

| Hauptwelt | Bestand | Zusätzliche Vorschläge | Fachentwurf |
|---|---:|---:|---:|
| Haushalt | 3 | 5 | 8 |
| Garten | 7 | 0 | 7 |
| Freizeit | 9 | 2 | 11 |
| Sport | 8 | 1 | 9 |
| Bildung | 3 | 3 | 6 |
| Pflege | 8 | 0 | 8 |
| Gewerbe | 34 | 0 | 34 |
| GESAMT | 72 | 11 | 83 |

Haushalt-Neufunde: eigenständige Wischroboter (Kärcher RCF 3, DE Händler), mobile Luftreinigungsroboter (ECOVACS AIRBOT Z1, DE Hersteller/Händler), mobile Heimüberwachungsroboter (Enabot), Katzentoilettenroboter (Litter-Robot EU), Vorhangroboter (SwitchBot EU). **Letzte zwei technische Grenzfälle** zwischen eigenständiger Robotik und ortsfester Hausautomation. **Heimüberwachung** überschneidet sich teilweise mit vorhandenem Haustierroboter (ROB-0088), braucht vor WP-Anlage eine eindeutige Owner-Entscheidung.

Bildung: Roboterbausätze (Makeblock Deutschland), mobile ROS-Lernplattformen (ROBOTIS Turtlebot bei DE-Händler), Lehrroboterarme (Dobot E6 bei DE-Händler). Lehrroboterarm darf nicht eine zweite URL des bestehenden Freizeit-Tischroboterarms werden.

Freizeit: Unterwasserdrohnen (Chasing, Auslandslieferung nach DE noch offen), Tracking-Kameradrohnen (DJI, autonome Flugleistung nicht übertreiben). Sport: Badminton-Federballwurfmaschinen (Trainbot, DE Händler). Keine pauschale 1:1-Umwandlung in veröffentlichte Webseiten.

## Vorgeschlagene Direkteinstiege im Menü (keine neuen WP-Parents heute)
Haushalt **Reinigung / Haustiere / Wohnen**.
Bildung **Programmieren / Praxis / Unterricht**.
Gewerbe visuell in sechs vorhandene Sachbereiche gruppieren, ohne Eigentümer-IDs oder Permalinks zu verändern. Die ungleiche Zahl von 34 professionellen gegenüber acht häuslichen Produkttypen bleibt transparent. Nicht durch künstliche Seiten neutralisieren.

## Exakter dokumentierter Status
- **Forschungsregister CURRENT v36 jetzt in der Library:** `/robotik/Recherchebüro/CURRENT.json` mit 557 Fundnennungen; sämtliche vorherigen 548 Einträge sind unverändert.
- **Einziger abgeleiteter Entwurf, kein neuer konkurrierender Master:** `/robotik/Konzeptbüro/ROBOTIK_7_HAUPTBEREICHE_V36_KATEGORIEENTWURF.json`.
- **Ausführlicher Bericht mit allen Herstellerlinks, Artikelfragen, Nischen-/Grenzfall-Ausschlüssen:** `/robotik/Konzeptbüro/ROBOTIK_KATEGORIEBALANCE_V36_PRUEFBERICHT.md`.
- **72 unveränderte Original-WP-IDs:** `/robotik/Konzeptbüro/BESTAND_72_UNVERAENDERT_V36.csv`.
- **Maschinelle Verifikation:** `/robotik/Konzeptbüro/V36_VALIDIERUNG.json`.
- **Kein DataForSEO-Live-Lauf und keine Suchvolumenwerte.** Alte Kategorieplugin 0.4.2-Seedliste enthält die 11 neuen Produktbegriffe noch nicht. Nur nach Freigabe bezahlte Keyword-Abfragen.
- **Null WordPress-Writes, kein Plugin-Update, keine Veränderung der bisherigen 104 WP-Seiten und 89 Beitragskategorien.** Ursprünglichen First-Import auf keinen Fall erneut auslösen.

## Nächste tatsächliche Bündelaufgabe
Die offenen **Identitätskonflikte und technischen Grenzfälle** einmal abschließend klären, SEO-Recherche für die echten zusätzlichen Themen im BESTEHENDEN Kategorie-Plugin organisieren (nicht 11 manuelle Läufe), danach alle zugelassenen Ergänzungen über EINEN geschützten Add-only-Deltalauf erzeugen. **Kein separater WordPress-XML-Importer.** Die beiden alten, generischen WP-Produktseiten `Haustierroboter` und `Lernroboter` sind vor Erweiterung ausdrücklich auf zu breite Produktidentität zu prüfen.
