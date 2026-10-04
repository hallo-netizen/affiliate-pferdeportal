# Affiliate Router 6.72.181 – KISS Banner Hard Local + Installer

Datum: 2026-10-04
Workstream: AFFILIATE_ZENTRALE
Version: 6.72.181
Branch: affiliate-release-current

## Ziel

Eine zentrale Bannerregel:
1. exaktes Thema;
2. weiterer Themenkreis;
3. allgemeiner Fallback;
4. danach jeder aktive technisch/slotseitig gültige Banner.

Gilt für Seiten, Kategorien, Beiträge und Glossar.
Pferderassen: themenneutral; bestehende stabile Partner-/Creative-Verteilung.

## Harte lokale Positiv-/Negativ-Simulation

Getestet wurde der exakte aktuelle PHP-Methodencode von campaign_match_rank() und slot_required_creative_type() in einer lokalen PHP-Stub-Umgebung.

Ergebnis:
- PHP-Syntax Testharness: PASS.
- 63/63 Assertions: PASS.
- exakte Zielkante vor breitem URL-/Runtime-Treffer auf page/category/post/glossary: PASS.
- Destination exact: PASS.
- Runtime-page exact: PASS.
- Glossar exact: PASS.
- Partner exact: PASS.
- weiterer Themenkreis vor Fallback: PASS.
- allgemeiner Fallback: PASS.
- themenfreier technischer Fallback über alle 28 getesteten Banner-Slots/Aliase: PASS.
- Rassen Single Desktop/Mobile/Generic + Overview themenneutral: PASS.
- Rassen führen keine Auto-/Destination-Themenprüfung aus: PASS.
- Produkt-Slot ohne Zielmatch bleibt fail-closed: PASS.
- unbekannter Slot erhält keinen erzwungenen Banner: PASS.
- direct page exact, hierarchy broad, term, slug, keyword: PASS.
- Target-Rank-Miss wird exakt einmal aufgerufen: PASS.
- Target-Rank-Miss fällt danach trotzdem auf technisch gültigen Banner zurück: PASS.

Lokaler Microbenchmark, je 100.000 Durchläufe:
- exact target: 100.989 ms
- fallback: 154.230 ms
- breed early exit: 87.360 ms

## Performance-Hardlock

Direkter Source-Vergleich:
- 6.72.171 Fast-Selection-/Request-Cache-Funktionen unverändert.
- automation_campaign_exact_target_rank() und uncached helper gegenüber 6.72.171 unverändert.
- Renderer + Ranking-/Distribution-Funktionen gegenüber 6.72.176 unverändert.
- neue KISS-Logik enthält 0 neue DB-Abfragen und 0 neue Remote-Aufrufe.
- ein beim Review gefundener unnötiger zweiter target-rank-Aufruf wurde vor diesem Test entfernt.
- Rassenpfad steigt früher aus als vorher.

## Paketbasis und Delta

Letztes vollständig gebundenes Paket: 6.72.176.
Dessen Full Gate belegt:
- PHP lint 21/21 PASS;
- Performance-Hardlocks PASS;
- Fresh unpack/source ZIP byte identity 27/27 PASS.

Git-Vergleich 6.72.176 -> 6.72.181:
Exakt drei Plugin-Dateien geändert:
- includes/trait-ppar-output-objects.php
- pferdeportal-affiliate-router.php
- readme.txt

Keine weiteren Plugin-Dateien verändert.

## Installerbau

Basis: AFFILIATE_ZENTRALE_6.72.176.zip
Ersetzt: exakt die drei oben genannten aktuellen 6.72.181-Dateien.

Vor Commit wurde das erzeugte ZIP erneut geparst:
- ZIP entries: 27
- Plugin-Dateien: 27
- Manifestpfade fehlend: 0
- Zusatzdateien: 0
- ersetzte Dateien: 3/3 bytegleich zum aktuellen Source
- Root: affiliate-portal-router/
- ZIP SHA-256: 56e2b698361a10d9c83c99b1da9ff82bb3b3f62106811e1ed3f69c6eb44488a3
- ZIP Bytes: 1,537,791

Committed Blob:
- path: release/affiliate-zentrale/artifacts/final/AFFILIATE_ZENTRALE_6.72.181.zip
- git blob sha: 6ab1608a2fe164623e6a6de55bc2ec57bfdae629
- tree-reported size: 1,537,791 bytes
- commit: 29f50c2fe9bc525daf0d8f4c3ed222dc5605ef75

Hinweis: Der GitHub-Connector gibt Binärdateien >1 MB beim nachträglichen fetch_file nicht erneut als Content zurück. Die ZIP-Struktur-/Byteprüfung erfolgte deshalb im selben Buildprozess vor dem Blob-Commit; der committed Tree bestätigt danach denselben Blob und exakt dieselbe Dateigröße.

## Ergebnis

HARD_LOCAL_KISS_POSNEG_PASS
PERFORMANCE_PRESERVATION_PASS
INSTALLER_STRUCTURE_27_OF_27_PASS
INSTALLER_BUILT_6_72_181

Live-Installation/Live-Readback wurde nicht durchgeführt.
