# Pferdeatelier – Affiliate 6.72.361 Performance-Rootfix – finale Vollprüfung

Stand: 2026-11-19

## Entscheidung
- 6.72.360: **REVOKED / NICHT INSTALLIEREN**.
- 6.72.361: **installierbarer Testkandidat nach finalen lokalen Gates**.
- Kein automatisches Promotion von `release/current`.

## Scope
Nur der nachgewiesene Performance-Rückschritt in `ebay_filter_ranked_product_candidates_provider_cohort()` wird korrigiert. Keine andere Performancevermutung wird umgesetzt.

## Funktionsschutz
- Dateien: 66 -> 66; entfernt 0; hinzugefügt 0; 63 byteidentisch.
- Benannte Funktionen: 1552 -> 1552; entfernt 0; hinzugefügt 0; Signaturänderungen 0.
- 1551 vorhandene Funktionskörper unverändert.
- Exakt ein bestehender Funktionskörper geändert.
- Statische Hook-Registrierungen: 212 -> 212; entfernt 0; hinzugefügt 0.
- PHP-Lint 23/23 PASS; ZIP CRC PASS.

## Sicherheitsmodell
Cross-Slot-Wiederverwendung nur bei normalem Frontend und `category_product_1..3`, wenn identisch:
- kompletter source-geprüfter geordneter Kandidatenpayload,
- effektiver Provider-Modus,
- idealo-Linkstrategie,
- Otto/Awin-Freigabe,
- aufgelöste eBay-Seller-Identität,
- bei combined/automatic exakte GTIN-Identität.

Bei dynamischen Meta-/Option-/Sanitizer-/Cache-/Shortcode-Filtern oder persistentem Objektcache fällt der Code auf das exakte 6.72.359-Slotverhalten zurück. Admin/AJAX/REST/Cron/WP-CLI benutzen ebenfalls den alten Pfad.

## Semantikbeweis – exakt finales ZIP
- 10.894 Matrixfälle / 26.630 Aufrufe: **0 Output-Abweichungen**.
- Darin 6.000 dynamische Zustandssequenzen / 18.000 Aufrufe.
- 210 dynamische Filter-/Persistent-Cache-Guard-Fälle: Output und Buildzahl exakt wie 6.72.359.
- eBay-Originaltrait-Test: 35/35 PASS alt und neu; stdout byteidentisch.
- Amazon/idealo-Test: 15/15 PASS alt und neu; stdout byteidentisch.
- REST/Cron/WP-CLI: Output identisch; Builds alt=neu=0.
- Die vier nachgewiesenen 6.72.360-Fehlerklassen sind in 6.72.361 geschlossen.

## Performance-A/B
Exakt gepacktes finales ZIP, isolierter Original-Funktionspfad, 710 Kandidaten, 3 Kategorieplätze, 61 Wiederholungen:
- 6.72.359: Median 33.551245 ms / 3 Builds.
- 6.72.361: Median 13.83222 ms / 1 Build.
- **-58.77 %** im bewiesenen Funktionsweg.
- Output-Hash identisch.

Dies ist kein Versprechen für die gesamte Live-Seitenzeit, sondern der Nachweis, dass genau die bewiesene Dreifacharbeit entfernt wird, ohne Outputänderung.

## Paket
`PFERDEATELIER_AFFILIATE_6.72.361_PERFORMANCE_ROOTFIX_FINAL_TEST.zip`
SHA-256: `a42bc2b0fc781f2a8f0e140bb3fa2fd3772fe67bbc7bdba13e8e677a8a278c11`
