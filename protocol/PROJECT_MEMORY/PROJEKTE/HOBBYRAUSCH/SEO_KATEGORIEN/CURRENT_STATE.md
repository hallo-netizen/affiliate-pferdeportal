# HOBBYRAUSCH – SEO_KATEGORIEN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-17
STATUS: **LIVE-BASELINE UNVERÄNDERT / V4 2743-KNOTEN-AUDIT PASS / HD-001 1.14.9 VERWORFEN / 1.14.10 MANUAL-ONLY LOCAL PASS / ECHTER WORDPRESS-DRY-RUN OFFEN**

## Live-Baseline

Produktiv unverändert:
`HD-TARGET-3P-RULE27-CATEGORY-GAPFIX-HOBBYFINDER-20261009+0f4dbf59238a7d83`

- 2357 aktive physische Zielobjekte;
- 2357/2357 Readback;
- 8 Hauptwelten;
- 330/330 terminale CORE-Seiten;
- LIVE-PASS.

## Zentraler V4-Kandidat

Profil:
`/hobby rausch/KATEGORIE_ZENTRALE/HOBBY_DEPOT_TARGET_PROFILE_AUDIT_CANDIDATE_V4_20261017.json`

SHA-256:
`96b09a55047cb43b286a3d2fe4f11232ee98a8c6a0abab7d5818f1d21cb04e27`

Audit:
`/hobby rausch/KATEGORIE_ZENTRALE/HOBBY_DEPOT_FULL_STRUCTURE_AUDIT_V4_20261017.json`

Delta:
`/hobby rausch/KATEGORIE_ZENTRALE/HOBBY_DEPOT_TARGETTREE_DELTA_V4_20261017.json`

## Voll-Audit V4

- 8/8 Hauptwelten unverändert;
- 381 terminale Hobbyseiten;
- 2236 unterste Inhaltskategorien;
- je terminaler Hobbyseite 5–8 Inhaltskategorien;
- 381/381 mit `FAQ / Häufige Fragen`;
- unterste Inhaltskategorie hat keine weitere Kategorie darunter;
- jede unterste Inhaltskategorie muss grob mindestens 3–5 eigenständige Beiträge tragen können;
- Kosten / Vergleich / Pflege / Ausrüstung sind **keine Pflichtlabels**: eigener Leaf nur wenn das Thema 3–5 eigenständige Beiträge trägt, sonst als Artikel in einem breiteren passenden Leaf;
- keine fehlenden Parents;
- keine doppelten Node-IDs/Slugs;
- kein direkter Hauptwelt-Hub mehr ohne `nav_order`;
- HD-001 TargetTree Validator: 0 Errors / 0 Warnings;
- Design-Registry-Vollsimulation: 0 page/category/type/world/render mismatches.

## Fachliche Korrekturen/Erweiterungen

V3 bleibt enthalten:
- Spotting & Verkehr;
- Citizen Science;
- Natur bestimmen;
- Plane Spotting aus Messen & Analysieren heraus;
- Suchen & Finden;
- Modellbau unter Fertigen;
- Miniaturen & Szenen erweitert;
- Naturfunde erweitert;
- Schneckenhaltung;
- Quilten-Leaf = `Quiltmuster & Stichführung`.

V4 ergänzt gezielt dünne, fachlich sinnvolle Hubs:
- Schrift & Lettering → Federkiel-Schreiben;
- Leder → Lederprägen, Schuhmacherei;
- Bonsai & Miniatur → Penjing, Saikei;
- Essbare Pflanzen → Kräuteranbau, Obst im Kübel;
- Imkerei & Bestäuber → Wildbienenhotels, Hummelkästen;
- Gehegegestaltung → Paludarium, Terrarienbau.

Bewusst **nicht künstlich aufgefüllt**:
- Smart Home bleibt fokussiert auf Heimautomatisierung;
- Pilze & Kulturen bleibt Pilzzucht + Speisepilzzucht; Pilzklonen/Substrate sind tiefere Themen, keine künstlichen Geschwister-Hobbys.

## Mega-Menü-Datenursache

Im Live-/V3-Bestand fehlte bei 10 direkten Welt-Hubs `nav_order`.
Dadurch wurden z. B. bei Pflanzen `Bonsai & Miniatur`, `Gärtnern` und `Moos & Miniaturgärten` vor Kategorien mit echter Reihenfolge sortiert.

V4 setzt für **alle direkten Hubs aller acht Hauptwelten** eine vollständige, eindeutige Reihenfolge.

`Bonsai & Miniatur → nur Bonsai` war kein CSS-Fehler, sondern ein zu dünner zentraler Hub. V4 ergänzt dort Penjing und Saikei.

## Letzte Inhaltskategorie-Ebene

Diese Ebene ist vorhanden und im Registry-Renderer sichtbar.
Beispiel Ameisenhaltung:
- Einstieg & Arten;
- Formicarium & Nest;
- Futter & Wasser;
- Winterruhe & Klima;
- Kolonie & Pflege;
- Ausbruchsschutz & Probleme;
- FAQ / Häufige Fragen.

FAQ ist im V4-Kandidaten für 381/381 terminale Hobbyseiten vorhanden.

## Timeout-Korrektur

HD-001 1.14.9 ist verworfen.

Sicherer Kandidat:
`/hobby rausch/KATEGORIE_ZENTRALE/HD001_V1.14.10_MANUAL_ONLY_TIMEOUT_FIX_LOCALPASS.zip`

SHA-256:
`f9500d051249b239ca3215754eff54d37244fb80ef612ce54cfd5f722db7f243`

1.14.10:
- kein automatischer Runner-Bootstrap;
- Installation/Aktivierung startet keine Vollbaum-Verarbeitung;
- Dry-Run nur manuell;
- Sync separat bestätigungspflichtig.

## Betriebsregel

DataForSEO = Evidence, nicht Strukturautorität.
Kategorie-Zentrale = alleinige Strukturwahrheit.
Design liest ausschließlich HD-004, nicht rohe WordPress-`get_pages()`-Kinder.

## ERSTER OFFENER BLOCKER

**V4 ist lokal vollständig geprüft, aber noch nicht gegen die echte WordPress-Datenbank als manueller Delta-Dry-Run gelaufen.**

## EXAKT EINE NEXT ACTION

**Noch keinen Sync. Zuerst HD-001 1.14.10 sicher bereitstellen; danach ausschließlich den manuellen V4-Final-Dry-Run ausführen und Ergebnis gegen das V4-Delta prüfen.**
