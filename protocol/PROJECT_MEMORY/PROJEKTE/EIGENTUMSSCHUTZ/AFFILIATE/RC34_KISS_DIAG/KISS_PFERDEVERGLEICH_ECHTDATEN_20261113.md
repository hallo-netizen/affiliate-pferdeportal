# Korrektur 13.11.2026 – Original-HTML enthält möglicherweise bereits das eindeutige Ziel

Die frühere Aussage, der gespeicherte HTML-Code enthalte keine verwertbare Zielinformation, war nicht belegt und ist zurückgezogen. Im vorhandenen Import sind das originale HTML, das href und eventuell ein Tiefenziel wie `deep=kfz-versicherung` bereits gespeichert. Der Code hat diese Evidenz für bestimmte Tracking-URL-Zustände **ignoriert**. Der fixierte Einleseweg und die Tests stehen unter `RC35_HTML_LINK_KISS/`. Eine tatsächliche Prüfung aller 160 privaten Original-Codes steht weiterhin aus. Keine Banner neu importieren.

---

# Hab & Bewahr – KISS Bannerablauf und echter Datenblocker, 13.11.2026

## Ist anhand des Nutzer-Screenshots nach RC34
- Die private Werbemittel-Seite meldet 160 Tarifcheck-Banner, keine offenen/fehlerhaften Bilder, aber 160 fehlende Zielzuordnungen und 0 aktive Ausgaben.
- Die genannten Beispiele heißen lediglich „Tarifcheck Banner“. Aus diesem Platzhalternamen folgt keine Versicherungsart.
- Daraus ist **nicht** bewiesen, ob alle 160 Original-URLs bzw. ihre gespeicherten Rohdaten ohne verwertbare Hinweise sind. Sie wurden hier nicht aus der privaten WordPress-Datenbank gelesen.

## Quellennachweis, keine Vermutung
- `creative_library_parse_html_codes()` übernimmt aus einem eingefügten HTML-Banner nur `<img title>`, `<img alt>`, Bild-URL, Tracking-Link und Größen; die Einlesezeile enthält ausdrücklich `destination_url => ''`.
- `creative_library_normalize_row()` ersetzt fehlende Angaben zu Name/Alt durch `$partner_name . ' Banner'`, also „Tarifcheck Banner“. Diese künstliche Bezeichnung enthält keine fachliche Kategorie.
- `creative_library_destination_from_tracking()` und `creative_library_resolve_tracking_destination_import()` versuchen **einmal beim Import** eine echte Zielseite zu ermitteln. Ein unauflösbarer Tracking-Link bleibt nur Tracking-Link und darf nicht als fachliche Zielseite gelten.
- `hb_rc31_insurance_banner_plan()` benötigt als eindeutige Zuordnung reale Ziel-URL, Partner-Kategorie oder aussagekräftigen Originaltext; andernfalls sperrt es die Themenzuordnung. Das ist bei einem unbeschrifteten Original korrekt.
- Die RC33/34-Versionen haben bereits einen zentralen Import-Zuordnungspfad und lesen dessen gespeicherte Schlüssel im Frontend. Die bloße Umbenennung bzw. nochmalige Installation dieses Pfades erzeugt keine fehlende fachliche Information.
- Ein zweiter Zielkarten-Schreiber und spätere eigene Titel-/Partner-Entscheidungen waren RC33-Ursachen; sie sind im RC34-Build für kanonische Quellen abgeschaltet. **Keine** neue konkurrierende Zuordnung einführen.

## Zielvertrag wie Pferde Atelier (für Hab verbindlich)
1. ORIGINAL EINLESEN: Originalbild, echtes Partnerziel/Tracking, ursprüngliche Bezeichnung/Kategorie/Beleg unverändert sichern. Keine erfundene Kategorie.
2. EINMAL ENTSCHEIDEN: Nur belegte echte Ziel-URL -> originale Partner-Kategorie -> originaler Bannertitel. Genau ein richtiger Versicherungszweig und seine echten Unterseiten; allgemeiner Vergleich nur bei ausdrücklichem Nachweis. Einmalig und zentral im Import, nicht im Frontend.
3. SPEICHERN: Eine vorhandene Zielkarte je Banner/Portal. Kein zweiter Schreiber, kein nachträgliches Überschreiben der Unterseiten.
4. ANZEIGEN: Die gespeicherte Zielkarte lesen, nicht erneut inhaltlich zuordnen. Bild/Tracking/Veto-Sicherheit behalten, nicht durch Themenheuristik ersetzen.

## Vor jedem weiteren Release
- Kein „alle 160 gelöst“ und keine neue RC-ZIP, solange nicht mindestens eine echte gespeicherte Tarifcheck-Originalzeile mit echter Zielseite, Alt-/Titeltext, Provider-Kategorie und bisheriger Zuordnung nachgewiesen ist.
- Echte Altbestände **nicht** neu importieren und nicht pauschal einem Versicherungszweig zuweisen.
- Falls diese Beweise in den vorhandenen 160 Rohdaten tatsächlich fehlen, ist eine fachlich korrekte automatische Einzelzuordnung aus den Daten logisch unmöglich: fehlende Anbieter-Rubrik muss aus der Originalquelle beigebracht werden. Kein Bugfix darf diese Information erfinden.
- Nach Einsicht einmalige zentrale Quelle korrigieren, anschließend echte unveränderte Originale end-to-end bis zur Webseite prüfen. Keine weiteren Diagnose-Plugins oder doppelten Prüfketten.

## Trennscharfer Stand
Die **Ursache für 160 leere Zielkarten** ist noch nicht vollständig bewiesen, weil die 160 privaten Originalzeilen nicht direkt vorliegen. Bewiesen sind der Verlust fachlicher Information beim HTML-Rohimport **wenn** Titel, Alt, echte Ziel-URL und Rubrik im HTML fehlen sowie die 160 derzeit leeren Karten im Screenshot. Zielvertrag festgehalten, **kein neues Plugin veröffentlicht, keine Live-Änderung behauptet**.
