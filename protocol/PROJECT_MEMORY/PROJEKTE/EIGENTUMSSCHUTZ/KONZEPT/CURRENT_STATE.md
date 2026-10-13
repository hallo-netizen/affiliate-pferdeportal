# HAB & BEWAHR – KONZEPT – CURRENT STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-13
STATUS: **R3/V5 GESAMTSTRUKTUR UND ARTIKELENTWURF LOKAL PASS / ORGANISCHE SEO-OWNER-FREIGABE OFFEN / WORDPRESS R2 UNVERÄNDERT**

## Verbindlicher Zielvertrag
Nutzer hat ausdrücklich festgelegt:
- **Jede anklickbare Zwischenebene: mindestens 3 und höchstens 10 unterschiedliche direkte Auswahlmöglichkeiten.**
- Keine Dopplungen, keine künstliche Auffüllung, keine inhaltlich identischen Artikel in verschiedenen Kategorien.
- 6 vorhandene Gefahrenwelten, 31 bestehende Themenbereiche, 3 Portalsäulen und sämtliche vorhandenen Keywords, IDs, URLs und 704 Artikelideen als Ausgangsbasis erhalten.
- Erst sinnvolle Erweiterung/Umsortierung; **nicht** blind Zwischenebenen löschen.
- Keine WordPress-Synchronisierung vor vollständiger Konzept-/SEO- und URL-Folgenprüfung; keine kostenpflichtigen Provideraufrufe ohne Einverständnis.

## Realer WordPress-Stand (Current Live, getrennt von R3)
Autoritativ für WordPress **weiterhin R2**, Revision `HB-SECURITY-CATEGORY-OWNER-CORRECTIONS-20261012-R2+655852190d183cc9`. Nutzer-Readback 2026-10-12 13:06:45 UTC: Plugin `1.14.8.17`, `sync_state.status=COMPLETE`, Runner `COMPLETE`, 354/354 Objekte geprüft, 2 erstellt / 352 aktualisiert / 0 archiviert, `frontend_readback.valid=true`, 0 Fehler. R2 enthält 6 Welten, 31 Themenbereiche, 45 Unterbereiche, 141 CORE-Blattkategorien und 704 konkrete redaktionelle Artikelideen.
R2-Quelldatei `HAB_UND_BEWAHR_KATEGORIENPROFIL_20261012_R2.json`, SHA256 `bd1594d7012ae36f787cf9ca2039e657d922e2954f3e097cc3f2b40482d42055`.

## EINZIGE aktuelle R3-V5-Arbeitsfassung
**Vollständige redaktionelle Büroakte:** `KONZEPT/R3_V5_144_KATEGORIEN_432_IDEEN_EDITORIAL_FACHPLAN_20261013.md`, Commit `fa3338f68b05384a1c913d93ea6357f9522cea71`. Enthält **alle 144 neuen Kategoriekandidaten und jeweils 3 aktuelle Artikelentwürfe**. Deren Einordnung als eigenständiger Google-SERP-Owner ist ausdrücklich **nicht** bewiesen.
**Struktur-Delta:** `KONZEPT/R3_48_UNTERBEREICHE_KANDIDATEN_20261013.md`, enthält die 48 neuen Unterbereiche und 144 Kandidaten. Historische Erstfassungen V2/V3/V4 und ursprüngliches 17er-Umhängungsregister nicht als aktuelle Planfassung verwenden.
**QA-Beleg:** `KONZEPT/R3_V5_QA_20261013.json`. Lokale vollständige **nicht importierbare** JSON-Arbeitskopie `HAB_R3_V5_FACHPLAN_NICHT_IMPORTIEREN_20261013.json`, SHA256 `e77863a7c13080e316c89a5de8a01c8fd519eae78b717dc335b1dbd1bce34b08`; **nicht behaupten, dass diese JSON in GitHub abgelegt wurde.** Der vollständige redaktionelle Text und der Strukturplan liegen dort als obige Büroakten.

## Belastbarer V5-Konzept- und Qualitätstest
- **6/6** Gefahrenwelten, **31/31** Themenbereiche mit 3–10 Kindern; **93/93** Unterbereiche mit jeweils 3–10 Blattkategorien. **285 CORE-Blattkategorien** = 141 bestehende unverändert +144 neue Kandidaten.
- 432 neue redaktionelle Titelvorschläge (mindestens drei pro Kandidat) plus 704 alte. **0 exakt gleiche Titelformulierungen** innerhalb aller Vorschläge. Dies ist keine automatische Zusicherung semantisch verschiedener Artikel!
- Seit V2 **14 redaktionelle Präzisierungen** nach fachlicher Überlappungsprüfung (6 V3 + 2 V4 + 6 V5); u.a. Löschmittel Camper Befestigung vs Gerätevergleich, Datenleitungen DSL/Glasfaser vs Koax, Kühlgeräte nach Netzausfall.
- **19** konkrete Vorschläge, bestehende Themen zu spezielleren Eigentümern **umzuhängen statt zu kopieren**: 17 in historischer `KONZEPT/R3_BESTANDSOWNER_21_FACHPRUEFUNG_20261013.md` und 2 zusätzliche `core:leaf:162` → Zählerschrank / Datenleitungen im V5-Hauptdokument. **Jede alte Quellkategorie behält nach diesen Vorschlägen >=3 Artikelideen**; tatsächliche R2-Artikel/IDs unverändert.
- 21 ältere R2-SEO-Owner-Fälle fachlich vorläufig zugeordnet, **nicht** anhand Google SERP vollständig freigegeben. Die drei Portalsäulen inklusive Magazin und Dienstleister bleiben unverändert und erfüllen die im Konzept geprüfte 3–10-Regel.
- **Keine WordPress-Schreibvorgänge, keine neuen DataForSEO-Aufrufe.**

## Redaktionelle Prioritätskonflikte nachgearbeitet
Die fünf zuvor priorisierten Themenpaare wurden **fachlich** hinsichtlich genau eines Content-Owners entschieden: Trocknungsprotokoll Kleinbetrieb (Betriebs-/Vermieterprozess statt allgemeiner Schadensbericht), Camper-Löschmittel, Steckersolar, Heizungs-SMS-Meldeweg und Gewächshausalarm. Konkrete alte/neue IDs, Keyword-Alias-/Kopierverbot und qualitative Sachquellen: `KONZEPT/R3_V5_FUENF_SEO_OWNER_ABGRENZUNGEN_20261013.md` (Commit `d4af8171e993513884a86d239cab504e7a6b6c9c`). **Keiner dieser fünf redaktionellen Entscheide ist schon durch getrennte organische Google-SERP-Ergebnisse bestätigt; Trocknungsprotokoll bleibt der kritischste Fall.** Drei lexikalisch ähnliche alte/neue Artikelpaare wurden als unterschiedliche Objekte/Arbeitsphasen eingeordnet, nicht als automatische SERP-PASS-Werte.

## Erster offener Blocker und harte Release-Sperre
**HB-CONCEPT-002 – Suchintent-Owner für 144 neue Kategorien nicht belegt.** Historischer Keywordüberblick: 282 angefragt, nur 128 Anbieter-Treffer (154 unbekannt ≠ 0). Historische SERP-Kontrolle: 16/20 R2-Vergleichspaare vollständig, vier nicht. Externe Sachquellen stützen punktuell Thema-/Geräteunterschiede, **nicht** vollständige Google-SEO-Abgrenzung, Nachfrage und Kannibalisierungsfreiheit der R3-Artikel.
Außerdem **HB-CONCEPT-004**: WordPress-Plugin `1.14.8.17` erzwingt die neue 3–10-Regel nicht auf jeder Zwischenebene. Erst vor Release minimal an bestehendem Validator nachrüsten, Regressionstest inkl. negatives Szenario. Bestehende WordPress-URLs und Slugs bleiben unverändert bis geklärter Link-/Redirect-Folgenprüfung.
**R3/V5 ist KEIN gültiges WordPress-Importprofil, nicht veröffentlichen, neue Seiten nicht indexieren.**

## EXAKT EINE NEXT ACTION
**Die übrigen R3-Kategorien systematisch auf fachliche Doppel-Owner prüfen:** die in der V5-Abgrenzungsakte schon redaktionell entschiedenen fünf Fälle als feste Grenzen verwenden, anschließend bei den 144 neuen Kategorien vor allem benachbarte Blattkategorien mit demselben Schutzobjekt und derselben Gefahr auf Doppelartikel untersuchen; bei echten Überschneidungen Thema zu *einem* Owner verschieben/als Alias führen und aus dem anderen Zweig einen nachweisbar eigenständigen Artikelintent formulieren. Danach verbleibende Google-SERP-/Keyword-Evidenzlücken exakt bestimmen; ohne bezahlte Providerfreigabe keine neuen Kosten. R3-Live/Import bis vollständiger Abnahme weiterhin gesperrt.
