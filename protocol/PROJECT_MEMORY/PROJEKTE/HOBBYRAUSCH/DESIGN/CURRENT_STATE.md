# HOBBYRAUSCH – DESIGN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-17
STATUS: **1.50.650 GRUNDBASIS / 1.50.664–1.50.667 VERWORFEN / 1.50.668 REGISTRY-RENDERER LOCAL HARD PASS / LIVE NUTZT NOCH ALTEN 330ER SNAPSHOT / V4 NICHT LIVE**

## Live-Erklärung

Affiliate Portal Template Kit **1.50.668** ist installiert, verändert aber die **Strukturinhalte nicht selbst**.
Es rendert, was HD-004 als aktive zentrale Registry liefert.

Darum war live optisch/inhaltlich vieles unverändert:
- HD-004 liefert weiterhin den alten 330er Live-Snapshot;
- V4-Erweiterungen sind noch nicht synchronisiert;
- `Bonsai & Miniatur → nur Bonsai` stammt aus dem alten zentralen Snapshot;
- das Mega-Menü kann keine Kategorien anzeigen, die im aktiven Snapshot nicht existieren.

Die relevante sichtbare 1.50.668-Änderung ist bereits erkennbar:
terminale `category`-Kinder werden jetzt ausgegeben, z. B. 7/7 unter Ameisenhaltung.

## Gefundene Mega-Menü-Datenfehler

Im aktiven/V3-Datenstand fehlt bei 10 direkten Welt-Hubs `nav_order`.
Dadurch wirkt die sichtbare 5er-Auswahl teilweise willkürlich.

V4 korrigiert die Reihenfolge zentral für alle direkten Hubs.

Das Mega-Menü zeigt gemäß Vertrag zunächst bis zu 5 direkte Hubgruppen.
Weitere direkte Hubgruppen liegen hinter `Mehr Kategorien`.
Das ist **kein Datenverlust**.

Die zusätzliche Orientierungsebene je sichtbarer Gruppe zeigt kompakt bis zu 4 Links + `Alle Themen`.
Ein Hub mit nur einem realen Kind zeigt entsprechend nur ein Kind; Beispiel live: Bonsai & Miniatur → Bonsai.
V4 erweitert diesen Hub zentral auf Bonsai / Penjing / Saikei.

## Letzte Inhaltskategorie-Ebene

1.50.668 kann Page- und Category-Kinder getrennt aus HD-004 lesen.
Ameisenhaltung live zeigt bereits:
- Einstieg & Arten;
- Formicarium & Nest;
- Futter & Wasser;
- Winterruhe & Klima;
- Kolonie & Pflege;
- Ausbruchsschutz & Probleme;
- FAQ / Häufige Fragen.

Damit ist diese zuvor fehlende Ebene technisch repariert.

## Registry-Prinzip

Wie beim bewährten Hab-&-Bewahr-Fix:
- zentrale Registry = einzige Strukturwahrheit;
- keine rohen WordPress-Kinder/Geschwister als Ersatz;
- zentrale Revision vorhanden + Registry nicht bereit → fail closed;
- kein zufälliger Weltbild-Fallback.

## 1.50.668 Local QA

- aktuelle 330er Baseline: 0 Strukturabweichungen;
- V3: 0 Strukturabweichungen;
- V4 mit 381 terminalen Hobbyseiten / 2236 Leafs: 0 Strukturabweichungen;
- Trainspotting-Negativfall PASS;
- Ameisenhaltung 7/7 PASS;
- PHP 58/58 PASS.

## Bildhinweis

Zusätzliche alte Hero-Patchplugins 1.50.659 / 1.50.661 / 1.50.662 sind Übergangsstände und dürfen die Bildwahrheit nicht weiter überlagern.
1.50.668 enthält die zentrale Hero-/Preview-Logik.

## Zentrale V4-Abhängigkeit

V4 ist noch nicht live:
`/hobby rausch/KATEGORIE_ZENTRALE/HOBBY_DEPOT_TARGET_PROFILE_AUDIT_CANDIDATE_V4_20261017.json`

Bevor neue direkte Hub2 live gehen, benötigen sie gemäß Bildvertrag ein eigenes geprüftes Hero + daraus abgeleitete Preview.

## PASS-GRENZE

Kein Live-PASS ohne echten WordPress-Readback.

## EXAKT EINE NEXT ACTION

**Nicht am CSS weiterdrehen. Erst den sicheren V4-Struktur-Dry-Run gegen WordPress ausführen; danach Registry synchronisieren/readbacken. Erst dann 1.50.668 gegen den neuen zentralen Snapshot erneut live prüfen.**
