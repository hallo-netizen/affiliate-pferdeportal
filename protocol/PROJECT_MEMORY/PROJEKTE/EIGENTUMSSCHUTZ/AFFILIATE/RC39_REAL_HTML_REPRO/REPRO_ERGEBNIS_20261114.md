# Hab & Bewahr RC39 – Importfehler durch Original-PHP simuliert, 14.11.2026

## Echte Live-Messung vor Test (Nutzer-Screenshot 10:00)
160 Tarifcheck-Banner, 80 aktiv, 80 ohne gespeichertes Versicherungsziel, 0 Formatblockaden. Der gespeicherte Fehlertext für alle 80 ist `No verified specific/general insurance`, Linkquelle `tracking_checked`. RC39 hat die 80 fachlichen Ausfälle **nicht reduziert**.

## Quellprüfung – tatsächliche Ursache des irreführenden Standardtitels
Im Original `creative_library_parse_html_codes()` wird der Bannertitel ausschließlich aus `<img title=...>` gelesen, sonst leer. Die Seite hinter `<a href=...>` wird zunächst nur als Trackinglink gelesen, der Artikeltyp nicht aus dem Code-Namen erschlossen. Bei leerem Title und Alt baut `creative_library_normalize_row()` den künstlichen Titel `Tarifcheck Banner`. Der **HTML-Parser gibt aber in diesem Pfad kein `title_source=manual_missing` mit**. Ohne diese Markierung akzeptiert `hb_rc31_insurance_banner_plan()` den künstlichen Titel als „realen“ Prüfhintergrund, auch wenn darin kein Versicherungszweig steht. Daher kann die Fehlermeldung `No verified specific/general insurance` entstehen, **ohne** dass ein echtes Versicherungsprodukt im gespeicherten Beleg identifiziert wurde.

RC35 kann einzelne tracking_checked-Links mit einem expliziten, bekannten `deep=versicherungsart` auf bekannten Hosts bereits erkennen. RC39s feste Kategorienamen helfen **nur, wenn bereits ein Produktbegriff aus den Quelldaten extrahiert wurde**. Die neue Oberkategorie kann keine unbekannte Produktart erfinden.

## Test statt neuer Pluginversion
[GitHub Actions – RC39 echter Importparser + echtes PHP + 160 synthetische Werbecodes](https://github.com/hallo-netizen/affiliate-pferdeportal/actions/runs/43578958808): **SUCCESS**.

- 160 synthetische, strukturgetreue HTML-Werbebanner durch `creative_library_parse_html_codes()` des **echten RC39-Plugins**.
- 80 Links tragen `deep=hausratversicherung`; ihr Ziel wird dem echten simulierten R3-Hausratknoten zugewiesen.
- 80 Links haben nur einen nichtssagenden Tracking-Parameter ohne Versicherungsart; diese bleiben **alle 80** unzugeordnet. Dabei wird mit dem automatisch erzeugten Titel `Tarifcheck Banner` **exakt dieselbe Fehlermeldung** wie auf der echten Website reproduziert.
- Das Ergänzen einer fachlichen Oberkategorie im simulierten, ansonsten identischen WP-Baum führt **nicht** dazu, dass die 80 nackten Trackinglinks eine gültige Versicherung bekommen.
- Echte andere Bannerregeln und die gesamte RC31/RC39-Regression bestehen.
- **Kein neues Plugin** erzeugt, veröffentlicht oder installiert. Keine Live-Änderungen.

## Wichtige Grenze
Der Test verwendet **keine 160 echten privaten Werbecodes**: Diese sind nicht in GitHub oder den Chat-Dateien zugänglich. Daher ist die Hypothese „bei allen 80 Originalen fehlt eindeutige Produktinformation“ **nicht bewiesen**. Es kann auch sein, dass in deren Original-URL, Bilddateiname, HTML-Text oder Anbieter-Programm eine echte Produktangabe steckt, die RC39 nicht ausliest. Eine sichere endgültige Reparatur erfordert, deren 80 Original-HREFs und bereits gespeichertes HTML **einmal in einer read-only Bestandsauswertung** mit der aktuell aktiven WP-Kategorienliste abzugleichen.

**KISS:** Erst echte Quellen einmal einlesen, Entscheidung an der bestehenden zentralen Importstelle einmal treffen, dort speichern, danach ausschließlich anzeigen. Keine erfundene Kategorienzuweisung, kein erneuter Frontendcheck, kein weiterer Rateschuss als Pluginversion.
