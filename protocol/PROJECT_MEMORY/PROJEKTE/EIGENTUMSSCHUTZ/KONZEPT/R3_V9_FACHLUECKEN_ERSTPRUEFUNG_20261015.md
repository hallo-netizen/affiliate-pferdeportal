# HAB & BEWAHR – KATEGORIENNEUPRÜFUNG NACH ZIELVERTRAG 2.0
15.10.2026 · Status: **FACHLICHE KANDIDATEN / NICHT IMPORTIEREN / NOCH KEIN VOLLSTÄNDIGER 1136-ARTIKEL-KOLLISIONSABGLEICH**

## Ausgangsbefund – datenbasiert
Die aktuell von WordPress rückgelesene R3/V8-Hierarchie enthält 6 Hauptwelten, 31 Bereiche, 93 Unterbereiche und 285 CORE-Endkategorien (545 weitere Objekte einschließlich Magazin-/Dienstleister- und Seitenobjekten). Über den originalen Plugin-Snapshot `nodes.json` wurden alle CORE-Eltern/Kinderbeziehungen neu ausgezählt:
- alle 31 Bereiche besitzen **genau 3** Unterbereiche;
- 87 der 93 Unterbereiche besitzen **genau 3**, die übrigen sechs **4** Endkategorien;
- diese unnatürlich gleichmäßige Ist-Verteilung entstand nachweisbar aus der historischen R2-Basis 19×1, 10×2, 2×3 durch das R3/V7-Differenzpaket **+48 Unterbereiche mit je 3 neuen Endkategorien**, nicht durch eine 3-Elemente-Anzeigebegrenzung des Mega-Menüs.
- Der positive 546/546-WordPress-Sync sagt **nichts** über die fachliche Vollständigkeit. Er dokumentiert 0 Löschungen und die Integrität des damaligen Exports. Die neuen Sollregeln lauten **mind. 3, kein Maximum; mindestens 3–5 individuelle Artikelthemen je Endkategorie**. Der alte 3–10-Zielvertrag ist ersetzt.
- Es liegen 432 konkrete neue R3/V8-Artikelideen im Fachplan `R3_V8_144_KATEGORIEN_432_IDEEN_FACHPLAN_20261013.md` vor; die 704 älteren R2-Themen sind historisch als Bestand belegt, aber in dieser Erstprüfung **NICHT einzeln gegen die Vorschläge maschinell gegengeprüft**. Deshalb aus diesen Kandidaten keinen WP-Release-/Dublettensicherheits-PASS ableiten.

## Drei priorisierte fachliche Lücken – ausdrücklich Kandidaten, keine neuen WordPress-Kategorien

### W1 · Wasser & Feuchtigkeit → neues mögliches Themenfeld „Dach & Gebäudehülle“
**Warum neuer fachlicher Bereich:** Aktuelle fünf Wasser-Bereiche sind `Leckage & Rohrbruch`, `Keller & Rückstau`, `Frost & Abwesenheit`, `Camping & Freizeitobjekte`, `Kleine Betriebe & Vereine`. Dach, Dachfenster, Fassadenanschlüsse und die oberirdische Regenabdichtung am Haus stehen nicht als eigene zusammenhängende Schutzprobleme unter Wasser. `Kellerabdichtung & Ursachen`, `Kellerfensterschächte & Nässe` sowie `Wohnmobil-Dachnähte & Abdichtung` sind objektspezifische **andere** Owner, also nicht kopieren.
**Mögliche Unterthemen (noch nicht als vollständiger neuer Bereich freigegeben):** `Dachflächen & Durchdringungen`; `Fassade & Öffnungen`; `Regenentwässerung an der Gebäudehülle`.
**Konkrete Test-Endkategorie „Dachfenster & Wasseranschlüsse“:** 5 verschiedene Artikelintents:
1. Regenwasser am Dachfenster: Dichtung, Anschlussblech oder Dachfläche als Ursache einordnen.
2. Kondenswasser am Dachfenster von eindringendem Regenwasser unterscheiden.
3. Feuchte Dachfenster-Laibung: Schäden an Dämmung und Innenverkleidung erkennen.
4. Dachfenster nach Sturm-/Dacharbeiten auf Undichtigkeiten fachlich prüfen lassen.
5. Wartungs- und Kontrollpunkte an älteren Dachfensteranschlüssen dokumentieren.
**Risiko:** Dach/Fassade bei **Sturm** im Wetterzweig behandelt mechanische Sturmfolgen, Wasserzweig behandelt Einregnen/Abdichtung. Nur ein kanonischer Ratgeber-Owner je konkreter Frage.

### W2 · Wetter & Naturgefahren → neues mögliches Themenfeld „Hitze & Trockenheit“
**Warum:** Aktuelle fünf Wetter-Bereiche decken Starkregen/Hochwasser, Sturm/Hagel, Frost/Schnee, Blitz/Überspannung und Freizeit/Unwetter ab. Hitzewellen, sommerlicher Wärmeeintrag und Dürreschäden am privaten Grundstück werden **nicht als zusammenhängendes Risikofeld** geführt. Der Technikzweig `Überhitzung im Dachgeschoss` ist ein **Temperaturalarm**, nicht baulicher Hitzeschutz.
**Mögliche Unterthemen:** `Gebäude & sommerlicher Hitzeschutz`; `Trockenheit & Grundstück`; `Freizeitobjekte bei Hitze` – mit Prüfung, welche Unterthemen tatsächlich jeweils mindestens drei tragfähige Blattkategorien haben.
**Konkrete Test-Endkategorie „Hitzeschutz am Dachgeschoss“:** 5 unterschiedliche Artikelintents:
1. Außenliegende Verschattung für Dachfenster gegen sommerlichen Wärmeeintrag vergleichen.
2. Dachbodenlüftung und passive Nachtkühlung ohne aufwendige Haustechnik beurteilen.
3. Dämmung im Dachgeschoss auf sommerlichen Wärmeschutz prüfen lassen.
4. Hitzebelastung unter Dachflächen mit einfachen Messreihen dokumentieren.
5. Dachbegrünung, helle Dachoberflächen und deren Grenzen bei Bestandgebäuden einordnen.
**Risiko:** Einzelfragen zur Sensor-/Warntechnik gehören zum bestehenden Technikzweig. Vegetations-/Brandrisiken könnten primär `Feuer & Gase` gehören; Dublettenprüfung nötig.

### W3 · Technik & Ausfälle → neues mögliches Themenfeld „PV, Heimspeicher & Ladebetrieb“
**Warum:** Bestehende fünf Technikbereiche sind `Strom & Notstrom`, `Heizung & Temperatur`, `Pumpen & Haustechnik`, `Alarm & Smart Home`, `Fernüberwachung`. Eigene Betriebsstörungen von Wechselrichtern, Heimspeichern und privater Ladeinfrastruktur fehlen als zusammenhängender technischer Ausfallbereich. `PV & Wallbox Überspannung` im Wetterzweig deckt Blitz-/Überspannung, `PV-Technik & Kabel` unter Vandalismus deckt Sabotage, `Lithium-Akkus & Powerstations` unter Feuer deckt Brand – andere Gefahren, nicht vermengen.
**Mögliche Unterthemen:** `PV-Erzeugung & Wechselrichter`; `Heimspeicher & Ersatzstrom`; `Wallbox & Ladebetrieb`.
**Konkrete Test-Endkategorie „Wechselrichterstörungen“:** 5 eigenständige Artikelintents:
1. Wechselrichter-Fehlermeldungen und Hersteller-Statuscodes systematisch einordnen.
2. PV-Wechselrichter offline: Datenverbindung von realem Erzeugungsausfall unterscheiden.
3. Wiederanlauf einer PV-Anlage nach Stromausfall kontrollieren lassen.
4. Netzseitige Abschaltungen und häufige Wechselrichterstörungen dokumentieren.
5. Warnungen aus dem PV-Monitoring priorisieren und an Fachbetriebe übergeben.
**Risiko:** Kein identischer Owner zu allgemeinem `Notstrom für Privathäuser` bzw. `Router & Mobilfunk-Backup`. Technische Eingriffe in Elektroinstallationen nicht als Heimwerkeranleitung darstellen.

## Freigabelogik für alle 31 Bereiche und 93 Unterbereiche
Jede weitere Ergänzung benötigt: (a) echten bisherigen Elternknoten; (b) Nachweis einer **neuen** fachlichen Schutzintention; (c) klare Grenze zu benachbarten Welten, Kategorien, Glossar und bestehenden Ratgebern; (d) bei *jeder neuen Endkategorie* mindestens **3, idealerweise 5 oder mehr** konkret verschiedene und substanzielle Artikelideen; (e) im neuen Zwischenknoten mindestens **3** eigene Kinder, **kein Maximum**; (f) Beachtung aller vorhandenen ID-/WP-URL-/Verlinkungsbindungen. Ein zusätzlicher Bereich darf erst dann in den Importplan, wenn seine eigene komplette Unter-/Blattgliederung diese Regel erfüllt. Fehlende Teilkategorien niemals durch künstliche Füllung erzeugen; Kandidat bleibt sonst zurückgestellt.

## Abgrenzung und offener Blocker
Dieser Befund ist **nur fachliche Erstprüfung von 3 besonders plausiblen Lücken anhand des echten 31/93/285-Baums**. Die vollständige redaktionelle Einzelprüfung aller 31/93 und Abgleich mit allen 1.136 echten Artikelideen wurde **nicht abgeschlossen**. Insbesondere vor dem vollständigen Importplan die 704 R2-Themen und 19 umzuordnenden Artikel konkret gegen jeden Kandidaten prüfen. So lange keine Automatisierung der WordPress-Kategorieänderung, kein Designplugin-Patch, kein Kategorie-Sync, keine kostenpflichtige SERP-Recherche. Aktuelle Autorität `KONZEPT/CURRENT_STATE.md` und operative Kategoriehoheit `KATEGORIEN/CURRENT_STATE.md`.
