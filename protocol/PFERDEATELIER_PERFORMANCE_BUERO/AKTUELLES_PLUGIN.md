# Aktuelles Performance-Plugin

Stand: 24.11.2026

LIVE:
- Affiliate-Zentrale 6.72.378
- PASSIV Pferdesättel: 2.222,09 ms Wall / 1.092,40 ms CPU / 89.461 Cache-Hits / 310 Queries.
- 6.72.378 ist live kausal bestätigt; voller Wall-Gewinn wird wegen besserer Hostbedingungen nicht komplett dem Plugin zugerechnet.

Aktueller freigegebener Testkandidat:
- Affiliate-Zentrale 6.72.379
- Paket: PFERDEATELIER_AFFILIATE_6.72.379_GEBUENDELT_EXACT_TARGET_ROOTFIX.zip
- SHA-256: 264b872aae3238027b38304282ddc6fcca868cb8a0b46629ad85f67b813ecc67
- Büro: /pferdeatelier/PERFORMANCE_BUERO/AKTUELLES_PLUGIN/PFERDEATELIER_AFFILIATE_6.72.379_GEBUENDELT_EXACT_TARGET_ROOTFIX.zip
- Prüfnachweis Büro: /pferdeatelier/PERFORMANCE_BUERO/AKTUELLES_PLUGIN/PFERDEATELIER_6.72.379_PRUEFNACHWEIS.md
- GitHub-Nachweis: protocol/PFERDEATELIER_PERFORMANCE_BUERO/PRUEFNACHWEIS_6.72.379.md

Gebündelte Maßnahmen H+I:
- H: 2.363 Zielprüfungen enthalten nur 156 eindeutige Zielschlüssel-Sätze. Direkter Abschnitt 6,676 -> 1,649 ms (-75,30 %), Ergebnis-Hash identisch.
- I: 2.363 bereits kanonische Zielschlüssel werden nicht erneut normalisiert. Direkter Abschnitt 12,769 -> 3,618 ms (-71,66 %), Ergebnis-Hash identisch.
- H zusätzlich zu I im Whole-Path: -2,36 %.
- I zusätzlich zu H im Whole-Path: -5,67 %.
- H+I kompletter Realbestand: 198,743 -> 183,221 ms (-7,81 %).
- finaler Lauf direkt aus Re-Extract-ZIP: 201,865 -> 187,102 ms (-7,31 %).

Nicht aufgenommen:
- Meta-Bulk E langsamer (+4,84 %).
- eBay-Meta-Snapshot F im betroffenen Abschnitt langsamer (+3,45 %).
- Gesamthash G langsamer (+8,87 %).
- J im verschärften Einzeltest ohne stabilen Gewinn (+0,13 %); verworfen.

Funktionsschutz – inhaltlich:
- 2.721/2.721 reale Kampagnennormalisierungen Alt=Neu.
- 25/25 reale Seiten-/Providerkombinationen Alt=Neu.
- 75/75 tatsächlich gerenderte Produktkarten inkl. HTML Alt=Neu.
- normal, sanitize_key, get_post_metadata, global pre_option, idealo-pre_option und externer Objektcache: Ausgabe und Meta-/Options-Aufrufzahlen Alt=Neu.
- echte Meta- sowie Provider-/Strategieänderung mitten im Ablauf Alt=Neu.
- 1.593 -> 1.593 Funktionen, entfernt 0, hinzugefügt 0; geändert nur category_product_shared_rank_base() und ranked_campaign_raw_target_keys().
- Produktions-Schreibwege unverändert.
- ZIP 66/66, PHP 23/23 PASS, Re-Extract fehlend 0 / extra 0 / Hashabweichungen 0.

Nächster Schritt:
- ausschließlich 6.72.379 installieren und genau einen PASSIV-Gesamtlauf ausführen.
