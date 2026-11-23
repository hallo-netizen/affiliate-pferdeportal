# Pferdeatelier Affiliate-Zentrale 6.72.373 – Provider-Image-DNS-Rootfix – Prüfnachweis

Stand: 2026-11-23
Basis: exakt installierte 6.72.372
Paket: PFERDEATELIER_AFFILIATE_6.72.373_PROVIDER_IMAGE_DNS_ROOTFIX.zip
SHA-256: 1a46c3f98b4df0cc5ac59eabe7962bcecd7d52513b58e7b6a9111aaf2b18aefe

## Live-Ausgangspunkt 6.72.372
PASSIV:
- Pferdesättel 12.714,99 ms Wall / 3.579,54 ms CPU / 135.614 Cache-Hits / 310 Queries.
- 6.72.371 auf derselben Route 8.463,96 / 3.745,47 / 139.475 / 310.
- 6.72.372 reduziert CPU nur ca. 4,4 % und Cache-Hits ca. 2,8 %; Hauptlast bleibt bestehen.

## Ursächlicher Restfehler
product_campaign_public_image_ready() führt nach bereits erfolgter Provider-Bildprüfung für jedes Produktbild zusätzlich wp_http_validate_url() aus.
Die aktuelle WordPress-Implementierung führt bei externen Hostnamen gethostbyname($host) und die private/reservierte-IP-Prüfung aus. Damit wird dieselbe Host-/DNS-Sicherheitsentscheidung für viele unterschiedliche Bilder desselben Providerhosts wiederholt.

Realer Pferdeatelier-WXR-Bestand 22.11.2026:
- 2.181 aktive Produktkampagnen.
- 1.285 aktive idealo-Bilder lösen auf cdn.idealo.com auf.
- 881 aktive eBay-Bilder sind bereits gültige ebayimg.com-Bilder.
- 15 stale eBay-Bild-URLs scheitern bereits an der unveränderten Providerprüfung.
- 2.166 provider-validierte aktive Bilder liegen damit auf genau zwei realen Providerhosts.
Pferdesättel-spezifisch: 1.010 aktive fachlich relevante Produktkampagnen, davon 617 idealo und 393 eBay.

## Exakte Änderung
Neu nur provider_product_image_http_validate_v672373().
product_campaign_public_image_ready() ruft diesen Helfer statt wp_http_validate_url() direkt auf.
- Jede URL behält Protokoll-, Parse-, Credential-, Hostzeichen- und Portprüfung.
- Erstes Bild je Providerhost: vollständige WordPress-Prüfung inkl. DNS/IP.
- Weitere Bilder desselben Hosts im selben Request: Wiederverwendung nur des bereits vollständigen Host-Ergebnisses.
- Dynamische URL-/HTTP-/Option-Filter, unbekannte Netzwerke, explizite Ports und nicht stabile Requestzustände: historischer WordPress-Weg vollständig.

## Inhaltlicher Alt/Neu-Beweis
Echter Bestand:
- 2.166 reale provider-validierte Bild-URLs.
- 0 Ausgabeabweichungen.
- vollständige WordPress-Prüfungen 2.166 -> 2.

Dynamischer Sicherheitszustand:
- 2.166 Fälle.
- 0 Ausgabeabweichungen.
- vollständige WordPress-Prüfungen 2.166 -> 2.166.

100.000 Struktur-/Randfälle:
- https/http, Providerhost/Subhost, Benutzer/Passwort, Ports 80/443/8080/81, Pfade/Querystrings.
- 0 Ausgabeabweichungen.
- vollständige Prüfungen 100.000 -> 27.063; unsichere Fälle bleiben auf Altweg.

Exakter gepackter PHP-Helfercode zusätzlich per Reflection getestet:
- 2.166 Providerhost-Fälle: 0 Abweichungen, 2.166 -> 2 vollständige Prüfungen.
- dynamischer Fallback: 0 Abweichungen, 2.166 -> 2.166.
- 100.000 Randfälle: 0 Abweichungen.

## Funktionsschutz 6.72.372 -> 6.72.373
Exakter PHP-Tokenvergleich:
- Funktionen 1.563 -> 1.564.
- bestehende Funktionen entfernt: 0.
- 1.563/1.563 bestehende Funktionen vorhanden.
- 1.562 bestehende Funktionen körperlich unverändert.
- geändert genau 1: product_campaign_public_image_ready().
- neu genau 1: provider_product_image_http_validate_v672373().
- Properties 31 -> 32; entfernt 0; neu nur request-lokaler Hostprüfungs-Cache.
- Actions 176 -> 176.
- Filter 30 -> 30.
- Shortcodes 6 -> 6.
- Produktions-Schreibprimitive vollständig identisch.
Alle Auswahl-, Ranking-, Provider-, Placement-, Fallback-, Veto-, Health-, Tracking-, Rendering-, Artikel-, Banner- und Schreibfunktionen außerhalb der einen Bildfreigabe-Aufrufstelle sind körperlich unverändert.

## Andere Plugins
Paketwurzel ausschließlich affiliate-portal-router/.
Keine Datei von Template Kit, HivePress, Texterstellung, Astra, WordPress-Core oder anderen Plugins ist enthalten.
Damit kann dieses Paket keine Funktion eines anderen Plugins ersetzen oder zurückbauen.

## Paketprüfung
- Dateien 66 -> 66; entfernt 0; neu 0.
- geändert nur Hauptdatei plus Stable-Tag in readme.
- PHP 23 -> 23, Lint 23/23 PASS.
- finales ZIP erneut entpackt: 66/66 Dateien, 0 Hash-Abweichungen.
- ZIP-Integrität PASS.
- Header/Klassenkonstante/Stable Tag 6.72.373.
- SHA-256: 1a46c3f98b4df0cc5ac59eabe7962bcecd7d52513b58e7b6a9111aaf2b18aefe

## Freigabe
6.72.373 ist als einzelner gebündelter Rootfix-Kandidat freigegeben. Live-Gesamtspeedup wird erst nach genau einem PASSIV-Lauf behauptet.