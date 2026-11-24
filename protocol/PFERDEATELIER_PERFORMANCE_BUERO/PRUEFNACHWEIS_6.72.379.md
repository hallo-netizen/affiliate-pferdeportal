# Prüfnachweis 6.72.379

Stand: 24.11.2026
Basis: LIVE 6.72.378
Paket: PFERDEATELIER_AFFILIATE_6.72.379_GEBUENDELT_EXACT_TARGET_ROOTFIX.zip
SHA-256: 264b872aae3238027b38304282ddc6fcca868cb8a0b46629ad85f67b813ecc67

## Kausalitätsbeweis je Maßnahme

### H – identische exakte Zielschlüssel-Sätze
Im echten Kategorie-Produktpfad werden 2.363 Zielprüfungen ausgeführt, aber nur 156 unterschiedliche geordnete Zielschlüssel-Sätze verwendet.
Direktmessung, 40 Wiederholungen:
- 6.72.378: Median 6,6758 ms
- H: Median 1,6486 ms
- -75,30 %
- Ergebnis-Hash Alt=Neu.

Whole-Path innerhalb der finalen Kombination:
- I allein 200,684 ms
- H+I 195,949 ms
- zusätzlicher H-Anteil -2,36 %
- Fachausgabe identisch.

### I – bereits kanonische Zielschlüssel
2.363 reale Zielschlüssel wurden direkt gemessen:
- 6.72.378: Median 12,7692 ms
- I: Median 3,6184 ms
- -71,66 %
- Ergebnis-Hash Alt=Neu: c8b7f086a6a9760dd12fdeb3ca747f31979bac72ee06839c38c4562592bc782a

Sicherheitsgate:
- nur exakt kanonische erlaubte Zieltypen nehmen den schnellen Weg.
- bei nichtkanonischem Wert historischer Normalisierer.
- bei sanitize_key-Filter vollständiger historischer Weg.

Whole-Path innerhalb der finalen Kombination:
- H allein 207,728 ms
- H+I 195,949 ms
- zusätzlicher I-Anteil -5,67 %
- Fachausgabe identisch.

## Gebündelte Wirkung
- 24 alternierende Realbestandsläufe: 198,743 -> 183,221 ms = -7,81 %.
- finaler Re-Extract-Paketlauf, 20 Alternierungen: 201,865 -> 187,102 ms = -7,31 %.
- get_post_meta 3.114 -> 3.114.
- get_option 324 -> 324.
- Produkte 1/2/3 identisch.

Der Gewinn entsteht damit nicht aus weniger Fachprüfung oder weniger Datenzugriff, sondern aus weniger doppelter CPU-Arbeit derselben Zielzuordnung.

## Verworfene Ansätze
- E Meta-Bulk: +4,84 % langsamer.
- F eBay-Meta-Snapshot: betroffener Abschnitt 47,69 -> 49,34 ms = +3,45 % langsamer.
- G Gesamthash: +8,87 % langsamer.
- J Wiederverwendung der zweiten Zielentscheidung: verschärfter Einzeltest 193,116 -> 193,371 ms = +0,13 %; kein stabiler Gewinn. Nicht enthalten.

## Inhaltlicher Funktionsbeweis
Kein Bytevergleich:
- 2.721/2.721 reale Kampagnennormalisierungen Alt=Neu; kombinierter Hash b3ebc847bbf5bfb8927988a96f4c391384ba731e7b798835e418243e6312ba17.
- 25/25 reale Seiten-/Providerkombinationen Alt=Neu.
- 75/75 Produktkarten bis render_banner() inklusive HTML Alt=Neu.
- Kandidatenanzahl/Reihenfolge, Post-ID, Kampagnen-ID, Provider, Titel, URL, Bild, CTA, Preis, Währung und Verfügbarkeit Alt=Neu.
- dynamische Fälle normal/sanitize_key/get_post_metadata/global pre_option/idealo-pre_option/externer Objektcache: Ausgabe UND Meta-/Options-Aufrufzahlen Alt=Neu.
- echte Postmeta-Änderung und Provider-/Strategieänderung im selben Ablauf Alt=Neu.

## Struktur- und Schreibschutz – Zusatzbeweis
- Dateien 66 -> 66; PHP 23 -> 23.
- Funktionen/Methoden 1.593 -> 1.593; entfernt 0; hinzugefügt 0; 1.591 unverändert.
- geändert ausschließlich category_product_shared_rank_base() und ranked_campaign_raw_target_keys().
- Actions 183 -> 183; Filter 30 -> 30; Shortcodes 6 -> 6.
- update/delete option, update/delete postmeta, wp_insert_post, wp_update_post und wpdb insert/update/delete/query alle exakt gleiche Aufrufstellenzahl.

## Paket
- PHP-Lint 23/23 PASS.
- ZIP 66 Dateien / 23 PHP-Dateien.
- Re-Extract: fehlend 0, extra 0, Hashabweichungen 0.
- Re-Extract PHP 23/23 PASS.
- Header/Klassenkonstante/Stable Tag 6.72.379.

Freigegeben ist ausschließlich SHA-256:
264b872aae3238027b38304282ddc6fcca868cb8a0b46629ad85f67b813ecc67
