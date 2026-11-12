# EINMAL-SEO-Worker: fachliche Qualitätsabnahme, keine neue Produktionsprüfung

**Ziel:** Einmal prüfen, ob der bereits vorgesehene **eine externe SEO-Entscheider** seine Aufgabe ausreichend gut erfüllt. Danach darf WordPress/PSERC dessen gültige Antwort nur noch technisch übernehmen. **Kein zusätzlicher Prüfer im laufenden Workflow.** Der bestehende Redaktionsplan bleibt unverändert.

## Feste Gegenproben aus der echten MINI-Datei mit 100 Themen
Die folgenden Fälle stammen **1:1** aus `QA_ONLY/MINI_100_ORIGINAL_EXTERNAL_TITLES_20261106.json`. Nummern sind deren Reihenfolge; sie sind keine WP-IDs.

### Gleiche/nahezu gleiche Suchabsicht – nicht blind doppelt FREI
- **007 / 085**: „günstige regendecken für pferde“ / „pferde regendecken günstig“. Gleicher Preis-/Kaufintent. Beide als zwei unabhängige Artikel **FREI** ohne nachweisbar verschiedene echte Suchabsicht = **Worker nicht bestanden**.
- **082 / 084**: „regendecke pferd 0g“ / „regendecke pferd ungefüttert“. Gleicher Füllungsgrad. Zwei unabhängige FREI-Artikel ohne tatsächlichen anderen Suchintent = **Worker nicht bestanden**.
- **009 / 011 / 086**: „pferde regendecken im test“ / „regendecken im test“ / „regendecken für pferde im test“. Reine Wortfolge begründet keine drei eigenen Vergleichsartikel. Mehrere Freigaben ohne nachweisbare unterschiedliche Suchfrage = **Worker nicht bestanden**.

### Wirklich prüfen, nicht allein aufgrund gleicher Wörter sperren
- **001 / 008**: Auswahlberatung vs allgemeiner Überblick. Überschneidung erkennbar; zwei eigenständige Ziele nur nach **begründet unterschiedlicher Suchantwort**, sonst Klärung.
- **003 / 019**: Fleece-Regendecke auswählen vs konkrete Wärmeleistung. Unterschiedliche Intention ist **möglich**, aber nicht wegen unterschiedlicher Titel automatisch bewiesen.
- **094 / 099**: Gebrauchten Pferdeanhänger prüfen vs Schwachstellen. Stark überlappender Gebrauchtkauf – sorgfältig unterscheiden oder zusammenführen.

### Breite/mehrdeutige Suchfragen dürfen nicht auf Titelformulierungen umgelenkt werden
- **076** „pferd decken“: kann Zucht/Bedeckung oder Eindecken mit Pferdedecke bedeuten. Ohne klare eigenständige *Suchfrage* muss es in **KLÄRUNG**; zwei Titel erzeugen nicht automatisch zwei Slots.
- **062** „pferd“: viel zu breit für eine präzise eigenständige Artikelfreigabe allein aus dem ursprünglich gelieferten Keyword. Falls keine genauere echte Suchintention nachgewiesen: **KLÄRUNG**.

### Fachlich verschiedene Suchabsichten nicht versehentlich gleichsetzen
- **087 / 093**: Spielzeug-Schleich-Pferdeanhänger vs realer Pferdeanhänger für zwei Pferde.
- **098 / 094**: Pferdeanhänger mieten vs gebrauchten Pferdeanhänger kaufen.
- **096 / 093**: Pferdeanhänger für vier vs zwei Pferde.
- **089 / 094**: Böckmann-Gebrauchtkauf (Marken-Longtail) vs allgemeiner Gebrauchtkauf – können getrennte Zielgruppen/Suchantworten tragen.
- **021 / 022**: „welche ist die beste“ (Kaufentscheidung) vs „welche können abschwitzen“ (Funktion). Erst fachlich beantworten, nicht nach überschneidenden Produktwörtern entscheiden.

## Verbindliche Freigaberegel des EINEN externen Owners
1. Vollständige **wirklich aktuelle** Quellen: echte WP-Artikel/Seiten/Glossar samt Status und Keywords, die vorhandenen PSTE-Pläne, **unveränderter gespeicherter Redaktionsplan** einschließlich `ppm679_editorial_plan_runtime_state_v1`, aktiver PSERC-Endplan und vorhandene Reservierungen. Kein künstlicher Abriss bei 1.200.
2. Ein Urteil **FREI / BELEGT / KLÄRUNG** pro eindeutiger **Suchabsicht**, nicht pro künstlich neu formulierter Überschrift. Bei **BELEGT** eine tatsächlich im Parkhaus vorhandene Referenz; vorhandener Import prüft deren Existenz **technisch**, nicht nochmals die semantische Ähnlichkeit.
3. Keine Entscheidung FREI ohne vollständige echte Bestandsdaten. Ein Fehler/unklarer Eintrag lässt gültige Geschwister weiter.
4. Der externe Worker selbst muss die obigen Positiv-/Negativfälle bestanden haben. Dies ist **einmalige Abnahme seiner Arbeit**, **kein zusätzlicher Prüfer nach jedem Import**.
5. WP und PSERC akzeptieren für extern geprüfte Fälle nur Quellen-/Titel-/Versionstreue und freie Slotbelegung. **Keine semantische Wiederholung** im WordPress-Backend, in PSERC oder K0.

## Status 07.11.2026 – klar getrennt
- **Technischer Prüfstand PASS:** GitHub-Läufe `42397320753` und `42397670308`: echte 100 ursprüngliche MINI-Keywords als Ausgangsdaten; 87 JA / 9 VIELLEICHT / 4 NEIN, 97 ursprüngliche Titel; keine zweite WP-SEO-Auswertung. Neu bestätigt: *alle vorhandenen PPM679-Artikelplätze werden nur gelesen*; veraltete Quelle verhindert Freigabe; gleichzeitige Importe werden **im selben vorhandenen WP-Optionseintrag atomar** getrennt; erfundene BELEGT-Referenz wird KLÄRUNG. PHP 83/83 Syntaxchecks PASS.
- **Fachliche Abnahme des echten externen SEO-Workers OFFEN:** Die bisher simulierten 87 externen SEO-Urteile waren **hypothetische Testantworten**, kein Ergebnis einer produktiv angeschlossenen KI gegen den echten aktuellen WordPress-Bestand. Dieser Nachweis wurde nicht erbracht, auch nicht durch die vorstehende fachliche Referenzliste.
- **Realer Staging-Endlauf bis K0 OFFEN:** Keine tatsächliche WordPress-/PSERC-/K0-Installation oder Erzeugung von Artikeln auf der Testseite.
- **Produktionsstatus weiterhin NICHT FREIGEBEN.** Kein zusätzliches Plugin, keine neue Datenbank, kein K0-Umbau, keine zweite SEO-Entscheidung.
