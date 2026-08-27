# Affiliate-Zentrale V6.61.1 – idealo Async Timeout Hotfix

## Ursache des Livefehlers
V6.61.0 hat den manuellen Button „Feed jetzt aktualisieren“ synchron im Admin-HTTP-Request ausgeführt. Der Ablauf bestand aus Metadatenprüfung, Remote-Download des Standardfeeds 2901 und anschließendem vollständigem 2.041.826-Zeilen-Abgleich. Obwohl der Import `set_time_limit(0)` und `ignore_user_abort(true)` verwendet, kann der vorgeschaltete Webserver/Proxy den wartenden Admin-Request mit Gateway Timeout abbrechen.

## Korrektur
- Der manuelle Button startet keinen Vollfeed-Download mehr im Admin-Request.
- Er stellt genau einen Hintergrundjob in WP-Cron ein und kehrt sofort zur Admin-Seite zurück.
- `spawn_cron()` stößt den fälligen Job nicht-blockierend an.
- Gemeinsamer idealo-Refresh-Lock verhindert parallele manuelle/automatische Vollfeed-Läufe.
- Status `queued/running/success/unchanged/failed` wird in der idealo-Fachseite und Synchronisierung angezeigt.
- Fehler bleiben providerlokal; Last-Good bleibt bestehen.

## Unverändert / Hardlock
- eBay-Providerlogik, eBay-Run, Heartbeat und eBay-Katalog unverändert.
- idealo Standardfeed 2901 bleibt alleinige idealo-Quelle.
- Hybrid-Strategie bleibt unverändert.
- gemeinsame Karte weiterhin nur bei exakter GTIN.
- keine Änderung am Designplugin.

## Prüfungen
- PHP-Lint 14/14 PASS.
- Async-Queue-Test PASS: erster Klick plant genau einen Hintergrundjob; zweiter Klick erzeugt keinen Doppeljob.
- Fresh-Unpack-Parität 19/19 PASS.
- Gegen V6.61.0 sind nur `trait-ppar-idealo.php`, Plugin-Version und `readme.txt` verändert; eBay-Dateien byteidentisch.
