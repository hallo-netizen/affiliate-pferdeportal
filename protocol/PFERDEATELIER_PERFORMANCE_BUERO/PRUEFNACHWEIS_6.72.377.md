# Pferdeatelier Affiliate-Zentrale 6.72.377 – gebündelter Exact-Read-Rootfix

Stand: 24.11.2026
Basis: live bestätigte 6.72.376
Paket: PFERDEATELIER_AFFILIATE_6.72.377_GEBUENDELT_EXACT_READ_ROOTFIX.zip
SHA-256: df04630d846b0417dd0ddb1341cd2321a308ca189e0ade4c7e6adb11b2fce844

## Live-Ausgangspunkt
6.72.376 reduzierte Pferdesättel live von 135.828 auf 121.246 Cache-Hits (-14.582 / ca. -10,7 %) bei 310 unveränderten Queries. Damit ist bewiesen, dass eng begrenzte Wiederverwendung im aktuellen Kategorie-Produktpfad live greift. Ein Gesamt-Speedup wurde wegen abweichender Serverlast nicht behauptet.

## Ein gebündelter Realbestands-Test
Realer Pferdesättel-Pool: 1.010 aktive Produktkampagnen, 617 idealo + 393 eBay.

### Metadaten-Hotpath
Acht reale Hotpath-Metafelder über 1.010 Kandidaten:
- 6.72.376: 8.080 get_post_meta-Aufrufe
- 6.72.377: 1.010
- -7.070 / -87,5 %
- identischer Ergebnis-Hash: 09d2536acac3233c84ac64f21a58dd7fcde66e62b50a775b84ab3d7a09292360

### Control über alle 1.010 Kandidaten
6.72.376:
- Meta 2.020
- Optionen 9.316
- Portal/Home 3.030
- erlaubt 1.010/1.010

6.72.377:
- Meta 1.010
- Optionen 11
- Portal/Home 3
- erlaubt 1.010/1.010

Identischer Entscheidungshash:
5fb1fa1ec134e9f5b66ddcc08bb79e6607b933b5f1f461cedf9c9f7c3b43d638

### Incident
81 Wiederholungen:
- Optionen 648 -> 8
- identischer Hash e0282413cc00dd110a7b6f578ed4878d39193f989a388b177f7b0f95f73def6a

### eBay Public Checkpoint
393 reale eBay-Kampagnen:
- Optionen 393 -> 1
- erlaubt 393/393 in beiden Versionen
- identischer Hash 4f8e7e133e37c78635fe35d518aab8b405bdaf90add904b3ddeb0657e024d611

### Gemeinsamer Ranking-Grundpool
6.72.376:
- Kandidaten 1.010
- Meta 3.812
- Optionen 648
- Kampagnenabfrage 1

6.72.377:
- Kandidaten 1.010
- Meta 2.721
- Optionen 0
- Kampagnenabfrage 1

Reihenfolge exakt identisch:
f8e93d51f49f87897e4df9289818c644693519b3e2ddc8d05265636e12085481

## Dynamik-/Mutationsschutz
- aktiver get_post_metadata-Filter: Alt 80 Einzelaufrufe / Neu 80.
- externer Objektcache: Alt 80 / Neu 80.
- echte Metaänderung A -> B im selben Ablauf wird sofort gesehen.
- relevante Control-Filter (pre_option control settings, partner gate, externer provider registry): Alt/Neu exakt gleiche Aufrufzahlen und gleicher Hash für 60 reale Kandidaten.
- Provider wird nach fünf Kandidaten pausiert: Alt=Neu [1,1,1,1,1,0,0,0,0,0].
- Notstopp nach fünf Kandidaten: Alt=Neu [1,1,1,1,1,0,0,0,0,0].
- eBay-Checkpoint-Änderung im selben Ablauf: vorher true, danach false, Alt=Neu.

## Vollständiger Bestandsschutz
- Dateien 66 -> 66, entfernt 0, hinzugefügt 0.
- geändert nur Hauptdatei, Control-Trait, eBay-Run-Trait und readme.
- Funktionen/Methoden 1.585 -> 1.591.
- bestehende Funktionen entfernt 0.
- 1.575 bestehende Funktionen token-inhaltlich unverändert.
- 10 gezielt geänderte bestehende Funktionen ausschließlich im bewiesenen Lese-/Invalidierungspfad.
- 6 neue interne Hilfsfunktionen.
- Auswahl, Ranking, Provider-Mix, Fallback, Health, Bilder, Tracking und Rendering token-identisch.
- Filter 30 -> 30; Shortcodes 6 -> 6.
- vier zusätzliche Actions ausschließlich zur Invalidierung bei echten Postmeta-/Postcache-Änderungen.
- sämtliche geprüften Produktions-Schreibwege inkl. $wpdb-Schreibwege unverändert.

## Paketprüfung
- Arbeitsstand PHP 23/23 PASS.
- finales ZIP neu entpackt: 66/66 Dateien, fehlend 0, zusätzlich 0, Hashabweichungen 0.
- Re-Extract PHP 23/23 PASS.
- Paketwurzel ausschließlich affiliate-portal-router/.
- Header/Klassenkonstante/Stable Tag 6.72.377.

## Freigabegrenze
Bewiesen ist die massive Reduktion mehrfach gelesener Daten bei identischer Fachentscheidung und vollständigem Rückfall auf den historischen Pfad bei relevanter Dynamik. Ein Live-Speedup wird erst nach dem nächsten PASSIV-Lauf behauptet.
