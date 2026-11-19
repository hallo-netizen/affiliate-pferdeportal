# Pferdeatelier – Affiliate 6.72.359 Performance-Bundle installiert

Stand: 19.11.2026

## Belegter Stand
- Nutzer bestätigt die Installation von `PFERDEATELIER_AFFILIATE_6.72.359_PERFORMANCE_BUNDLE_TEST.zip`.
- Pluginheader der gesicherten ZIP: **6.72.359**.
- ZIP: **66 Dateien**, Integrität **PASS**, Größe **5.401.550 Bytes**.
- SHA-256: `363082c86c33b5980aa33aea8cfa5a619cc73f4ee6e29577a442f50b3330f28b`.
- Gesicherte Binärdatei im Pferdeatelier-Pluginbüro:
  `/pferdeatelier/PLUGINS/PERFORMANCE/PFERDEATELIER_AFFILIATE_6.72.359_PERFORMANCE_BUNDLE_TEST.zip`
- Zugehöriger QA-Beweis:
  `/pferdeatelier/PLUGINS/PERFORMANCE/PFERDEATELIER_PERFORMANCE_BUNDLE_20261119_QA_BEWEIS.json`
  SHA-256 `6800d1e8f22247fc1b981153e1479df30d0aec4e6de338fdccd01489c7c28eb6`.
- Aktuelle Büro-Standakte:
  `/pferdeatelier/PLUGINS/PERFORMANCE/PFERDEATELIER_PERFORMANCE_AKTUELLER_STAND_20261119.md`.

## Unverändert
- Template-Kit **1.50.616** bleibt unverändert.
- Performance Diagnose Safe **5.0** bleibt unverändert.
- eBay-Funktionsbestand **471 -> 471**; keine eBay-Funktion entfernt, hinzugefügt oder inhaltlich verändert.
- Kein persistenter Objektcache eingebaut.
- Keine Digistore-Drosselung, kein Funktionsabbau, keine weitere Template-Änderung.

## Änderung 6.72.359
20 bereits vorhandene kleine/stabile Affiliate-Optionswerte werden mit der nativen WordPress-Funktion zum gemeinsamen Vorladen in den normalen WordPress-Cache gelegt. Bestehende `get_option()`-Aufrufe, Filter, Prüfungen und Entscheidungen bleiben bestehen.

## Ausgangsmessung
Basis: `pferdeatelier-performance-gesamtanalyse-20261119-074152.json`
- p95: **4,906 s**
- Browser-TTFB Ø: **4,207 s**
- Browser-LCP Ø: **4,619 s**
- einzelne Optionsabfragen im Frontend: **2.218 / 17 Aufrufe**, Ø **130,47**
- persistenter Objektcache: **false**

## Status
**INSTALLIERT / BINAER GESICHERT / QA GESICHERT / WIRKUNG NOCH NICHT LIVE GEMESSEN**

Der formale GitHub-CURRENT-Releasepfad wird durch diese Testinstallation nicht stillschweigend ersetzt. Die 6.72.359 ist als installierter Performance-Teststand dokumentiert, nicht als formaler Release.

## Nächster Schritt
Mehrere normale Seitenaufrufe auf der Testumgebung, danach genau ein PASSIV-Diagnoselauf. Erst dessen Messwerte entscheiden über die nachgewiesene Performance-Wirkung.
