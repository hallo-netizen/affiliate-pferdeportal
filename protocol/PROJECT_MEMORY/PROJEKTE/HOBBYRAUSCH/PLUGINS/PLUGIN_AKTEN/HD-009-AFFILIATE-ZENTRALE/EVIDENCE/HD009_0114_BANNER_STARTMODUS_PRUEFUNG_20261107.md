# HD009 0.1.14-dev – Prüfung der tatsächlich kopierten Bannerautomatik (07.11.2026)

## Unveränderte Originalbasis

- Vorheriger GitHub-Current: vollständiges Hobby-Affiliate-Plugin **0.1.13-dev**, PHP-Root `affiliate-portal-router/hobby-depot-affiliate-router.php`.
- Die bereits aus Pferdeatelier übernommene Engine für fachliche Zielauswahl, Elternpfad, Bannerverteilung und Slot-/Formatprüfung steckt weiterhin in `hobby-depot-affiliate-router.php`, `trait-ppar-output-objects.php`, `trait-ppar-creative-library.php` und `trait-ppar-automation-suite.php`. **Keine dieser drei Traits wurde geändert oder neu gebaut.**
- Wirkliche 0.1.13-ZIP wurde direkt geöffnet. Festgestellt: Der neue Startmodus blockierte alle Hub-Kacheln pauschal (`provide_hub_grid_affiliate_data()`), ließ in Standard- und Slot-Rendering nur `network=idealo` zu und sperrte damit auch lokale, bereits von der Creative-Library materialisierte Eigenbanner.

## Minimaler Fix (keine zweite Architektur)

- Entfernt: pauschaler Startmodus-Abbruch in der bestehenden Hub-Kachel-Funktion.
- Erhalten: ursprüngliches Themen-/Kategorienranking, einheitliche kreative Werbemitteldatenbank, bestehende Slot-/Format-/Abmessungsprüfung, automatische Elternpfad-Auswahl, Veto und Anbieterfilter.
- Der vorhandene öffentliche Amazon-/idealo-Startmodus lässt **idealo** und **bereits über die originale Creative-Library materialisierte eigene lokale Banner** zu. Ein eigenes Banner ist nur zulässig, wenn es ausdrücklich `network=manual`, Typ `banner`, Quelle `output_object_v4` hat und sowohl Bild als auch Ziel auf der eigenen Domain liegen. Keine generischen `manual`-Affiliate-Links; kein eBay, OTTO oder externe Bilder.
- Die schon vorhandenen Kandidatenauswahlmethoden filtern den Anbieter VOR ihrer bisherigen Rangfolge, auch in Hub-Kachel-/Zweierverteilung. Keine zweite Engine.
- Eigene Bilddateien im ZIP (Modellbau Querformat/Quadrat) sind **noch nicht** in der bestehenden Creative-Library als freigegebene Werbemittel registriert. Es erfolgt keine automatische öffentliche Veröffentlichung ungeprüfter Entwürfe. Nach Freigabe der Motive ist **ein einmaliger Import in den bereits bestehenden zentralen Werbemittelbestand** nötig; die weitere Seitenzuordnung ist automatisch, keine WP-ID je Seite.

## Reale Testausführung

- Alte 0.1.13-ZIP geprüft (ZIP lesbar und vollständig).
- Neue 0.1.14-ZIP: **708630 Bytes**, SHA-256 `dd7376073c3d9bae80741e4f97cdd7db3e5af4812f80caf88c87ce7da4176d76`, Git-Blob `b048b4de8f223202350db925c9d51c8b2b2b4e82`.
- Zwei von 30 regulären Dateien verändert: Hauptdatei und readme; **28 bytegleich** aus 0.1.13 übernommen.
- ZIP CRC PASS; 24/24 PHP-Syntax PASS.
- 10 isolierte Startmodus-Positiv-/Negativprüfungen PASS: Eigenbanner, idealo, Fremdpartner, externe URLs/Bilder, Legacy-Creatives, Produkte, Startmodus aus.
- Vorhandener DataForSEO-GET-Zugangstest unverändert: vier offline geprüfte Antworten (200=erfolgreich, 401=Zugang verweigert, 429=Limit, 500=Fehler), **kein kostenpflichtiger POST**.
- GitHub-Archiv als vollständige **Binär-ZIP** hochgeladen und im vorhandenen HD009-Current-Verzeichnis mit korrekter Größe und Blob gelesen.
- **Kein echter WordPress-/DataForSEO-/idealo-Live-PASS.** Aktuelle WordPress-Installation der 0.1.14 ist vom Betreiber noch nicht bestätigt.

## Stand im bestehenden Partnernetz

- Amazon-Tracking-ID im vorherigen WordPress-Screenshot gespeichert, Amazon-Direktlinks aktiv.
- Betreiber hat DataForSEO-Zugangstest ausgeführt; **dessen konkretes Ergebnis liegt hier nicht vor**. Nicht automatisch als PASS darstellen.
- idealo: echter API-Key/Adspace/Feed-ID und autorisierte Feed-URL müssen im WordPress-Backend für Hobby Depot bestätigt werden. Der vorhandene Importer und automatische 12-Stunden-Refresh sind implementiert, **kein Neuaufbau nötig**.
- Product-Recherche über DataForSEO erfolgt im aktuellen Plugin weiterhin **nur manuell und kostenpflichtig nach Klick**, mit einer exakt eingegebenen WordPress-ID und anschließender ASIN-Freigabe. Kein automatisierter Massenlauf in diesem Stand; nicht als bereits implementiert behaupten. Automatische Großrecherche ohne Kostenkontrolle ist **nicht** gestartet.
- Keine aktive öffentliche Kampagne/zugeordnetes Produkt im wirklichen Frontend überprüft.
