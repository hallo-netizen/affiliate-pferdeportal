# Prüfnachweis 6.72.380

Stand: 25.11.2026
Baseline: 6.72.379
Paket-SHA-256: 00da8aa7bf6ff560563433abeb643eb0352b72ef5a97c1314a6a40c365223348

## Performance – finales ZIP nach Re-Extract
20 alternierende vollständige Drei-Slot-Läufe auf echtem 2.721er Pferdeatelier-Kampagnenbestand:
- 6.72.379: Median 465,55 ms
- 6.72.380: Median 248,58 ms
- Verbesserung: -46,61 %
- vollständiger gerenderter HTML-Hash Alt=Neu: 3e3e815fdb4b7e906d8656f86ed324d4ba47620b2f45ea9a0161495797432334
- Meta 3138=3138, Optionen 42=42, Home 5=5

Weitere vollständige Seitenpfade:
- Pferdesättel -41,80 %
- Ausrüstung -46,51 %
- Reithelme -31,04 %
- Schabracken -17,37 %
- Weide-Zauntechnik -11,10 %
Alle Ausgaben und gezählten Datenzugriffe Alt=Neu.

## Inhaltlicher Funktionsschutz
- 2.721/2.721 reale Kampagnennormalisierungen exakt Alt=Neu.
  Hash: ebcf7160d95dd98dbcfb67b3ee490cc7f7cabd42d947dbefa3e2a6667a3127dc
- 25/25 Seiten-/Provider-/Strategiekonfigurationen exakt Alt=Neu.
- 75/75 tatsächlich gerenderte Karten inkl. vollständigem HTML Alt=Neu.
- 2.955/2.955 Inhalts-/Sperrlogikfälle exakt Alt=Neu.
  Hash: f11cf9599932dd3376c6f1c8eb91b62891188b1900f1849a242ef933d5ba9244
- Notabschaltung, eBay-Pause, idealo-Pause, sanitize_key-Filter, Metadata-Filter, pre_option-Filter, externer Objektcache, Locale-Wechsel, REST-Fallback und Cron-Fallback Alt=Neu.
- Vollständiges HTML deckt Provider, Titel, Links/Tracking, Bilder, CTA, Preis, Währung und Verfügbarkeit der tatsächlich ausgegebenen Karten ab.

## Kein Funktionsrückbau – Zusatzbeweis
- Dateien 66 -> 66, fehlend 0, extra 0.
- PHP 23 -> 23.
- erkannte Funktionen/Methoden 1603 -> 1605; entfernt 0; zwei interne Helfer neu.
- geändert nur Hauptdatei und eBay-Trait plus Version/Readme.
- Produktions-Schreibprimitive update/delete option, update/delete postmeta, wp_insert_post, wp_update_post, wpdb insert/update/delete/query exakt gleiche Vorkommenszahlen.

## Paket
- Version Header/Konstante/Stable Tag 6.72.380.
- PHP-Lint 23/23 PASS.
- Re-Extract 66/66, 0 Hashabweichungen, PHP erneut 23/23 PASS.
- Hauptdatei SHA-256: 3dddbb387cac24dbe4492fb507cee5c8c109db3de9b59b20ecf05616d1c7fc91
- eBay-Trait SHA-256: a2e621a9680b2a33bc2fa5364d20862c7282805158bc4c29c1e7c5d736d6b660

Freigegeben ist ausschließlich Paket-SHA:
00da8aa7bf6ff560563433abeb643eb0352b72ef5a97c1314a6a40c365223348
