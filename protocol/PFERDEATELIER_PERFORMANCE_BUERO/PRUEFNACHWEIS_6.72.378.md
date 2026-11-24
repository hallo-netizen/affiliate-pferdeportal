# Pferdeatelier Affiliate-Zentrale 6.72.378 – korrigierter gebündelter Kausal-Rootfix

Stand: 24.11.2026
Basis: live gemessene 6.72.377
Paket: PFERDEATELIER_AFFILIATE_6.72.378_GEBUENDELT_CAUSAL_ROOTFIX.zip
SHA-256: af39e106c595be83210d2c4a164c1274c723d25c2a2599b77f86488e4eda9839

## Freigabeentscheidung
Die zuerst erzeugte 6.72.378 wurde nach verschärfter Kausalitätsprüfung VERWORFEN und darf nicht installiert werden.
Von vier ursprünglichen Maßnahmen blieben nur zwei übrig, weil nur diese den geforderten Einzel-Kausalitätsbeweis bestanden.

## Maßnahme A – redundante innere eBay-Kohorten-Schlüsselarbeit
Direkt im echten Pferdesättel-Produktpfad gemessen, identischer Kandidatenbestand:
- historischer innerer Schlüsselweg: Median 78,83 ms
- äußerer bereits autoritativer Postprocess-Plan: Median 62,34 ms
- Verbesserung: ca. -20,9 % in genau diesem Produktionsabschnitt
- Metalesungen in diesem Abschnitt: 1.010 -> 393
- Ergebnisanzahl: 315 -> 315
- kompletter Ergebnis-Hash Alt=Neu: e965844054546ec3100094d3b6555c68d89607969d188085d2d00fce7a8b3efd

Damit ist nicht nur weniger Arbeit gezählt; dieselbe Funktion wurde direkt schneller gemessen und liefert exakt denselben geordneten Output.

## Maßnahme C – wiederholte vollständige Kandidaten-Fingerprints für Slot 2/3
Nach dem ersten vollständigen Fingerprint wird ausschließlich der bereits aus dem vollständigen Kandidatenzustand erzeugte interne Token wiederverwendet.
Direkt die reale Schlüsselarbeit für Produktplatz 2+3 gemessen:
- historisch: Median 17,08 ms
- neu: Median 1,67 ms
- Verbesserung: ca. -90,2 %
- Metalesungen: 0 -> 0
- Optionslesungen: 2 -> 2

Der interne Cache-Key ist absichtlich anders aufgebaut; entscheidend ist die Fachausgabe. Diese wird unten vollständig Alt/Neu geprüft.

## Gesamtwirkung A+C im echten 1.010er-Pool
10 wechselnd ausgeführte Alt/Neu-Durchläufe:
- 6.72.377 Median: 220,75 ms
- korrigierte 6.72.378 Median: 188,04 ms
- Verbesserung: ca. -14,82 %
- get_post_meta: 3.731 -> 3.114
- get_option: 324 -> 324
- Produkt 1/2/3: identisch

## Bewusst NICHT aufgenommen
Zusätzliche Maßnahmen wurden getestet und wegen fehlendem Kausalitätsbeweis verworfen:
- Home-Host-Lesecache: Optionslesungen sinken, aber kein belastbarer Zeitgewinn; im Einzeltest ca. +1,3 % statt schneller.
- GTIN-Ergebniscache: reales Aufrufmuster 1.325 Aufrufe / 1.010 eindeutige Kampagnen; Median 17,19 -> 20,25 ms, also langsamer. Verworfen.
- Wiederverwendung bereits berechneter Deferred-Titelsignaturen: Einzeltest 242,72 -> 259,33 ms, also langsamer. Verworfen.
- zusätzlicher Seller-Key-Cache: ebenfalls kein stabiler Gewinn; verworfen.

Es wurden damit keine Änderungen aufgenommen, nur weil sie theoretisch sinnvoll aussehen.

## Inhaltlicher Funktionsschutz – kein Bytevergleich

### 2.721 reale Kampagnen
- 2.721/2.721 Normalisierungen Alt=Neu
- Null-/Fehlerfälle: 0
- kombinierter Hash Alt=Neu:
  b3ebc847bbf5bfb8927988a96f4c391384ba731e7b798835e418243e6312ba17

### 25 reale Seiten-/Providerkombinationen
Geprüfte Seiten:
- Pferdesättel
- Satteldecken
- Reitplatzpflege
- Zeitschalt-Futterautomaten
- Stall Organisation

Je Seite fünf Kombinationen aus Provider-Modus und Linkstrategie.
Ergebnis:
- 25/25 Shared-Ranking-Basen identisch
- 25/25 vollständige Produkt-1/2/3-Auswahlen identisch
- Post-ID, Kampagnen-ID, Provider, Titel, URL, Bild, CTA, Preis, Währung, Verfügbarkeit und vollständiger Kandidatenhash identisch

### Tatsächliches Rendering
Für dieselben 25 Kombinationen wurden alle drei Produktplätze bis render_banner() ausgeführt:
- 75/75 gerenderte Produktkarten identisch
- Campaign-Hash identisch
- Group-Hash identisch
- Banner-Hash identisch
- HTML-Hash identisch

### Dynamische Sonderfälle
Mit explizit aktivierten dynamischen Zuständen wurde Alt gegen Neu geprüft:
- get_post_metadata-Filter
- sanitize_key-Filter
- globaler pre_option-Filter
- idealo-spezifischer pre_option-Filter
- home_url-Filter
- externer Objektcache

Ergebnis in allen sechs Fällen:
- fachliche Ausgabe Alt=Neu
- Shared Base Alt=Neu
- Produkt 1/2/3 Alt=Neu
- Aufrufzahlen Alt=Neu
- damit historischer Einzelweg nachweislich erhalten

### Echte Änderungen während des Ablaufs
- Metaänderung wird nach Mutation erkannt: Alt=Neu
- Provider-/Strategieänderung zwischen Slots: Alt=Neu
- direkte Kandidatenänderung verändert weiterhin den vollständigen generischen Plan-Key

## Struktur- und Schreibschutz – nur Zusatzbeweis
Nach Entfernung aller Testdateien:
- Dateien 66 -> 66
- PHP-Dateien 23 -> 23
- Funktionen/Methoden 1.591 -> 1.593
- entfernt: 0
- 1.584 bestehende Funktionen token-inhaltlich unverändert
- 7 bestehende Funktionen ausschließlich im bewiesenen Postprocess-/Invalidierungspfad geändert
- 2 interne Helfer neu
- geändert nur Hauptdatei, eBay-Trait und readme
- Produktions-Schreibprimitive Alt=Neu: update/delete option, update/delete post meta, wp_insert_post, wp_update_post sowie $wpdb insert/update/delete/query

Dieser Abschnitt allein gilt ausdrücklich NICHT als Funktionsbeweis; der Funktionsbeweis sind die realen Alt/Neu-Ausgaben oben.

## Paketprüfung
- Arbeitsstand: 66 Dateien / 23 PHP-Dateien
- PHP-Lint: 23/23 PASS
- finales ZIP neu entpackt: 66 Dateien / 23 PHP-Dateien
- fehlend 0
- zusätzlich 0
- Hashabweichungen Arbeitsstand vs. Re-Extract: 0
- Re-Extract PHP-Lint: 23/23 PASS
- Paketwurzel ausschließlich affiliate-portal-router/
- Header/Klassenkonstante/Stable Tag 6.72.378

## Freigabegrenze
Freigegeben ist nur dieses korrigierte Paket mit SHA-256 af39e106c595be83210d2c4a164c1274c723d25c2a2599b77f86488e4eda9839.
Die zuvor erzeugte 6.72.378 mit vier Maßnahmen ist verworfen.
Ein Live-Speedup wird erst nach Installation und einem PASSIV-Gesamtlauf behauptet.
