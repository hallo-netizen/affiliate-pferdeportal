# Pferdeatelier – Affiliate 6.72.362 Performance Rootfix GTIN-Set – 2026-11-19

Status: **FREIGABEKANDIDAT / NOCH NICHT LIVE INSTALLIERT**

## Ausgangsstand
- Installiert: Affiliate-Zentrale 6.72.361
- Performance Diagnose Safe 6.0.0
- Hauptproblem: tiefe Kategorie-/Produktseiten, besonders Pferdesättel.
- Belegt Pferdesättel 6.72.361: Ø CPU 4.368,68 ms, 320 Queries, 138.150 Object-Cache-Hits, 0 externe HTTP-Aufrufe.
- Vergleich Schabracken: gleicher grundsätzlicher Kategoriepfad und 320 Queries, aber deutlich weniger CPU/Cache-Arbeit.

## Bewiesene Ursache dieses Rootfixes
Im bestehenden `multiprovider_reorder_candidates()` wurde für jeden Kandidaten geprüft, ob mindestens eine GTIN bereits gesehen wurde:

`array_intersect($gtins, array_keys($seen_gtins))`

Dabei wird für jeden Kandidaten die komplette, immer größer werdende Menge der bereits gesehenen GTIN-Schlüssel neu materialisiert. Die Arbeit wächst deshalb quadratisch mit der Zahl eindeutiger Produktidentitäten.

Historischer 2012er Produktbestand:
- Pferdesättel breites relevantes Band: 709 Kandidaten
- davon historisch 507 idealo / 202 eBay
- Schabracken zusätzliches Exaktband: 43 Kandidaten, davon 38 idealo / 5 eBay

Die vorhandene fachliche GTIN-Menge selbst wird **nicht** geändert. Nur die Mitgliedschaftsprüfung wird direkt im bereits aufgebauten Set ausgeführt.

## Verworfen / nicht Bestandteil der Version
Folgende untersuchten Ansätze wurden ausdrücklich **nicht** aufgenommen:
- weitere globale Option-/Provider-Caches: messbarer Gewinn zu klein
- zweite ähnliche GTIN-Stelle in `multiprovider_prefer_shared_offer_cards()`: kein messbarer Gewinn
- `array_shift()`-Umbauten in Provider-Mix/Reorder: nur ca. 0,2 % Gewinn
- Banner-/Glossar-Ranker: bei Produktkampagnen sofortiger Abbruch, kein Root
- GTIN/DFS/Amazon als alleiniger Root: echte Mehrfacharbeit, aber zu klein
- Vollbestand-/postmeta-Umbau: derzeit zu hohes N+1-/Semantikrisiko
- eBay-Quellenfilter vor Control: semantisch nicht sicher
- Ranking-/Elternpfad-/Fallback-Kürzung: nicht zulässig, da inhaltliche Auswahl verändert werden könnte

## Ursächlichkeitsbeweis
Exakter 6.72.361-Code, gleicher 709er Kandidatenbestand, gleiche Providerdaten.

Isolierte `multiprovider_reorder_candidates()`-Skalierung, alt -> Kandidat:
- 43 GTINs: 0,242 ms -> 0,122 ms
- 118: 1,699 ms -> 0,382 ms
- 202: 6,063 ms -> 0,628 ms
- 507: 45,106 ms -> 1,490 ms
- 709: 90,310 ms -> 2,651 ms
- 1.090: 236,011 ms -> 3,307 ms

Alle jeweiligen Ausgabehashes identisch.

Gesamter historischer Pferdesattel-Selector:
- 6.72.361 Median lokal: ca. 123–127 ms
- Kandidat nur mit ursächlicher GTIN-Set-Änderung: ca. 51–52 ms
- Verbesserung: ca. 58–60 %
- ausgewählte IDs Slot 1/2/3 identisch
- vollständige Kandidatenarray-Hashes Slot 1/2/3 identisch
- Anzahl der Daten-/Metadatenlesevorgänge identisch

Schabracken:
- keine Verlangsamung nachgewiesen; kleine Laufzeit im Bereich ca. 13–15 ms, gleiche drei Ergebnisse.

## Funktions- und Inhaltsbeweis
- 300.000 randomisierte GTIN-Mengenfälle, einschließlich führender Nullen: **0 Abweichungen**
- 3.000 randomisierte exakte Mehranbieter-Funktionsläufe: identischer Gesamthash
  - Hash: `ac3911e99e51df3b3d1615a8f5ed9ef324d2a11c3209f2d8d0440c7d96901f76`
- historischer Gesamtselector Schabracken: vollständige Kandidatenhashes alt/neu identisch
- historischer Gesamtselector Pferdesättel: vollständige Kandidatenhashes alt/neu identisch
- 1.561 -> 1.561 Funktionen
- entfernt: 0
- hinzugefügt: 0
- Signaturänderungen: 0
- funktionaler Quellcode geändert: **genau eine Funktion in genau einer PHP-Datei**
  - `includes/trait-ppar-idealo.php`
  - `multiprovider_reorder_candidates()`
- 23/23 PHP-Dateien Lint PASS

## Paketbeweis
Paket:
`PFERDEATELIER_AFFILIATE_6.72.362_PERFORMANCE_ROOTFIX_GTIN_SET_FINAL.zip`

SHA-256:
`fc254a4ae4caac07ad98141fb38da3a59f812993865623ddbf7a8cb52e3cb4ff`

Fresh-Unpack:
- ZIP-Test PASS
- 66/66 Dateien byteidentisch zum geprüften Build
- Plugin-Header: 6.72.362
- interne VERSION: 6.72.362
- Fresh-Unpack 23/23 PHP-Lint PASS
- Fresh-Unpack Gesamtselector-Hashes identisch
- Fresh-Unpack 3.000-Fälle-Funktionshash identisch

## Funktionsvertrag
Unverändert:
- Kandidatenbestand
- Ranking und Relevanzbänder
- Eltern-/Semantikpfade
- Provider-Mix
- eBay-/idealo-/Amazon-Regeln
- GTIN-Autorität
- Produkt-Deduplizierung
- Fallback
- Control/Veto
- Health
- Bildprüfung
- Tracking
- Rendering
- Slot 1/2/3

6.72.362 ändert ausschließlich die interne Methode, mit der geprüft wird, ob eine bereits bekannte GTIN im vorhandenen Set liegt.

## Live-Status
**6.72.362 ist noch nicht installiert.**
Installierter Stand bleibt bis zur manuellen Überinstallation: **6.72.361**.
