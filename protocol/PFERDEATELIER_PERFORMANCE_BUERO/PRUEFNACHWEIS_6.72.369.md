# Pferdeatelier Affiliate-Zentrale 6.72.369 – Prüfnachweis

Stand: 2026-11-21

## Status
6.72.368 ist Zwischenstand und NICHT zu installieren.
Finales Paket: `PFERDEATELIER_AFFILIATE_6.72.369_KONSOLIDIERT_IMAGE_META_PERFORMANCE_ROOTFIX.zip`
SHA-256: `d1c99b5bc8b0b73b00ddd12bfa6931d1613094068444e5c5f69aa7e74412e98d`

## Fix A – Kausalität
Die strukturelle Produktbildentscheidung hat keinen Slotparameter, wurde aber in mehreren Produktplatz-Familien erneut ausgeführt.
- 11 Familien / 710er-Pool: 5395 → 710 Prüfungen (-86,84 %), Ausgabe identisch.
- 100000 stabile Fälle: 0 Ausgabeabweichungen.
- 100000 dynamische Fälle: 0 Ausgabe-/Aufruffolgeabweichungen.
- 100000 mutierte Kampagnen: 0 Ausgabeabweichungen.
- Isolierter Laufzeittest: Median 3,346 → 1,754 ms (-47,60 %).

## Fix A – Funktionsschutz
Nur normaler stabiler Frontendpfad. Admin/Cron/REST/AJAX/CLI, ext. Objektcache und dynamische Meta-/Option-/Cache-/Sanitizer-/Shortcode-/URL-/Redirect-/Hostzustände behalten die historische Aufruffolge. Geänderte Kampagnenfelder erzwingen Neuprüfung.

## Fix B – Kausalität
Der öffentliche Kampagnen-Snapshot lud bisher den vollständigen Metabestand der ausgewählten ap_campaign-Posts, obwohl der anschließende Rankingpfad zunächst nur `ppar_campaign_data` benötigt. Der neue sichere GET/HEAD-Pfad unterdrückt ausschließlich diese Voll-Hydrierung und liest den benötigten Schlüssel.
- 100000 randomisierte Bestände: 0 Wertabweichungen; 11821987 → 1542421 Meta-Zeilen im Modell (-86,95 %).
- 710er-Modell: 6390 → 710 Zeilen (-88,89 %), Werte identisch.
- 100000 Fehler-/Fallbackfälle: 0 Abweichungen.
- 100000 serialisierte Meta-Werte: 0 Abweichungen.

## Fix B – Funktionsschutz
Bestehende WordPress-post_meta-Cachewerte gewinnen. Kein Teilcache wird in WordPress geschrieben. Bei get_post_metadata/pre_wp_cache_get, persistentem Objektcache, Nicht-GET/HEAD oder DB-/Lesefehler gilt der historische get_post_meta-Pfad.

## Gesamtvergleich 6.72.367 → 6.72.369
- Named functions 1556 → 1561; entfernt 0.
- Dateien 66 → 66; entfernt 0; hinzugefügt 0.
- Actions 176 → 176.
- Filter 30 → 30.
- Shortcodes 6 → 6.
- Produktions-Schreibprimitive vollständig identisch.
- Auswahl, Ranking, Provider, Placement, Fallback, Veto/Control, Health, Tracking, Produktinhalt und Renderingregeln nicht entfernt.
- Design 1.50.616 und Diagnose 7.0.0 unverändert / nicht Bestandteil.
- 23/23 PHP-Lint im Arbeitsstand PASS.
- Finales ZIP erneut entpackt: 66/66 identisch; 23/23 PHP-Lint PASS.

## Nicht eingebaut
wp_options-Wiederholungen, init/Cron-Scheduling, persistenter Objektcache und weitere Auffälligkeiten bleiben unverändert, solange kein vollständiger Kausalitäts- und Funktionsbeweis vorliegt.

## Nächster Schritt
Nur 6.72.369 installieren; danach genau ein vollständiger PASSIV-Gesamtlauf.