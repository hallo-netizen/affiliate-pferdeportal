# Robotik – Prüfung Footer-Umzug 1.1.1
09.11.2026 · QUELLCODE DES ORIGINAL-ZIP GEPRÜFT · AUF NUTZERWUNSCH ORIGINAL 1.1.1 WIEDER AKTUELL, RISIKEN DOKUMENTIERT

## Woher?
Original: `PROJEKTE/HOBBYRAUSCH/PLUGINS/ISOLIERTE_PLUGINS/TOOL-FOOTER-UMZUG/CURRENT.zip` (Version **1.1.1**, 9.083 Byte). Das Original-ZIP hat 2 Einträge; PHP `footer-umzug/footer-umzug.php` wurde aus dem ZIP dekomprimiert und untersucht. Andere Portalplugins wurden nicht verändert.

## Was kann es nachweislich?
- Im WP-Backend **Werkzeuge → Footer-Umzug**.
- **Export**: ein JSON mit Footer-Menüplätzen/-menüs, darin verlinkten WP-Seiten, Footer-Widgets und deren Zuordnung.
- **Import**: legt Seiten/Menüs/Einträge an und **AKTUALISIERT bei Treffer auch bestehende Seiten** (`find_existing_page`, `wp_update_post`); kann Footer-Widget-Zuordnungen setzen. Das ist **keine reine Designübertragung**.
- Import ignoriert laut Header und Code Design-/Astra-Layout und Farben; auf Robotik muss ein kompatibler Footer-Bereich des aktiven Themes vorhanden sein.
- Footer-Menü-/Widgetbereiche werden über den Bezeichner **'footer'** erkannt. Ein anderes Theme mit anderen Registrierungsnamen kann Bereiche nicht korrekt treffen.
- Importdialog hat `Zielname`, `Ziel-E-Mail` und die **standardmäßig eingeschaltete** Option `Alte Marken-, Domain- und Themenbezüge neutralisieren`.

## Nachgewiesene Risiken für Robotik
1. Im Original sind feste textliche Ersetzungen **Pferdeatelier → Hobbydepot** enthalten. Bei Pferde-Quellen kann z. B. `Pferde` zu `Hobbys` werden; der Zielname `Robotik` garantiert deshalb **keine** korrekte Robotik-Fachterminologie.
2. Bereits vorhandene Zielseiten mit gleichem Slug/Bezug können durch Import **überschrieben/aktualisiert** werden. Es gibt nicht zunächst einen verpflichtenden Dry-run mit Vorschau.
3. Verlinkte Rechtstexte/Datenschutzerklärung sind **nicht automatisch** für Robotik passend. Gerade Impressum, Cookie-/Datenschutztext und Angebotsbedingungen müssen fachlich und datenschutzrechtlich zum Robotik-Portal passen.
4. Menü-/Widget-Position hängt vom aktiven Theme ab. Das Robotik-WordPress-Inventar 0.3.0 enthält **keine Theme-/Footer-Slot-Prüfung**; kompatibler Live-Footer ist daher **UNGEPRÜFT**.

## Entscheidung
**Prinzip technisch wiederverwendbar, Originalversion 1.1.1 für Robotik aber NICHT blind freigegeben.** Für spätere reale Übertragung erst eine **isolierte Robotik-Kopie** mit
- schreibfreier Vorschau/Diff,
- strikt neutraler Textbehandlung (keine Pferde→Hobby-Austauschtabelle),
- ausdrücklich ausgeschlossenen/gesondert bestätigten Rechtstexten,
- sicherer Zuordnung der aktuellen Footer-Menü-/Widget-Slots,
- gezielter Freigabe je zu erstellender/aktualisierender Seite,
- echter Nachprüfung im WordPress und Frontend.

**Kein neues Plugin hier erzeugt.** Original im anderen Gebäude bleibt unangetastet. Nach tatsächlichem Robotik-Build jedes neue ZIP **im Robotik-Pluginbüro** archivieren und sofort das gemeinsame Versions-/Übergabeprotokoll aktualisieren. Der Benutzer muss dafür jetzt nichts installieren, exportieren oder hochladen.

## Nutzerpräzisierung 09.11.2026
**Ziel ist ausschließlich die Übertragung benötigter Footer-Seiten samt Inhalt und Menüs – niemals Design.** Genaue Regeln im [Footer-Umzug-Zielvertrag](FOOTER_UMZUG_ZIELVERTRAG_20261109.md). Noch keine freigegebene Robotik-Plugin-Datei.

## Letzte Entscheidung, 09.11.2026
Der Nutzer verlangt ausdrücklich die **byteunveränderte bekannte Originalversion 1.1.1** zurück; 1.2.1 hatte Funktionen gekürzt. GitHub-Robotik-CURRENT ist jetzt 1.1.1 und 1.2.1 bleibt Archiv. Diese Entscheidung ersetzt den vorherigen Rat zur isolierten Neuentwicklung. **Die bekannten Risiken aus der Quellcodeprüfung bleiben bestehen**: vorhandene Zielseiten können verändert werden und alte Portalwörter werden unter Umständen umgeschrieben; deshalb Seiten-/Inhaltskontrolle vor dem Import, Rechtstexte prüfen. Keine Änderungen am Original-Plugin.
