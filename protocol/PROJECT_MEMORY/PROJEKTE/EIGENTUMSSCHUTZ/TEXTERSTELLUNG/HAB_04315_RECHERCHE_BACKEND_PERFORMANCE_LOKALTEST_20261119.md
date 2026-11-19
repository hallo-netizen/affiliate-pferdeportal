# Hab & Bewahr 0.4.31.5 – Recherche-Backend-Performance geprüft (19.11.2026)

**Kurs:** Nur Inspiration aus Nachbarchat Pferdeatelier, keine Codeübernahme. Kein Funktionsabbau. Original-0.4.31.5 und Live-WordPress **unverändert**. Keine neue Installations-ZIP.

## Anlass und Vergleichsquelle
- Nutzer meldet nach PSTE-Migration auf Hab-WordPress sehr langsamen bzw. scheinbar endlosen Seitenaufruf `Texterstellung → Recherche`.
- Im Pferdeatelier-Performance-Nachbarchat waren 2.218 einzelne `option_value`-Abfragen bei 17 Seitenaufrufen und fehlender persistenter Objektcache dokumentiert. Dieser Befund gilt **nur für Pferdeatelier**; Quellcode, Plugins, Design und Optimierungspaket 6.72.359 wurden NICHT kopiert.

## Exakter Hab-Quellcodebefund
- Im unveränderten `TXE_Workshop::researchFamilyDashboard()` wird `PSTE_Category_Context::familyAnchors($baseline)` einmal direkt und erneut **innerhalb** von `PSTE_Breadth_Research_Queue::openFamilies($baseline)` berechnet.
- `PSTE_Repository::categoryProgress(...)` führt dabei zweimal dieselbe **unbegrenzte** SQL-Statusabfrage `SELECT category_id,status,updated_at FROM ...runs ORDER BY id ASC` aus. Das ist nachgewiesene doppelte Arbeit, keine neue Entscheidung.
- `PSTE_Article_Type_Registry::build()` bildet bei häufigen Registry-Cachedurchläufen den SHA256-Fingerprint der gesamten serialisierten Baseline neu; `selectedCategory()` scannt die Baseline pro Familie, somit wächst der CPU-Aufwand stärker als linear.
- Die dynamische Hab-Map führt bei einem synthetischen Bestand aus 285 Kategorien / 93 R3-Seiten 114 `get_post_meta`- und 1.140 `get_term_meta`-WordPress-Funktionsaufrufe aus; WordPress-Cache kann diese bündeln, also **keine Behauptung über reale einzelne SQL-Abfragen**.
- Die alte `PSTE_Research_Job::rawJob()` protokolliert unbedingtes `PSTE_READTRACE` mit drei weiteren get_option-Lesezugriffen pro Aufruf. Im lokalen voll gerenderten Seitenmock kamen 3 solche Logzeilen vor. Diese Logik ist unmodifiziert.

## Vollständiger lokaler Read-only-Seitenlauf
- Original-PHP der **tatsächlichen** Hab 0.4.31.5 mit WordPress-Funktions- und SQL-Mocks ausgeführt, 285 synthetische verwaltete Kategorien und 93 synthetische R3-Seiten plus R1/R2; keine bezahlte Anfrage, keine WordPress-Schreibaktion.
- **Alle sieben Backendansichten PASS:** Übersicht, Recherche, MINI-Export, MINI-Import, K0-Export, Rückimport, Diagnose; das belegt nur die Bedienoberflächen, **nicht** echtes DataForSEO/MINI/K0/WP-End-to-End.
- Recherche-HTML exakt **49.608 Bytes** und **285 offene Familien**; während der Ansicht 74 Optionsleseaufrufe und vier SQL-Abfragen im Mock (davon zwei identische Run-Statusabfragen). Bei inklusive PHP-Bootstrap 85 Optionsleseaufrufe/20 unterschiedliche Optionsnamen.
- In fünf Cold-PHP-Durchläufen: Original-Recherche **Median 587,5 ms, Mittel 599,8 ms**. Bei lokal nachgebautem Bestand KEIN minutenlanger Stillstand.
- Unveränderte ältere Qualitätstests erneut bestanden: Null-Themen-Fortsetzung **16/16**, WordPress-AJAX **19/19**, tatsächlich erzeugter Button-Code **28/28**.

## Isolierter Performanceversuch – NICHT FÜR INSTALLATION
- Nur eine **separate lokale Arbeitskopie**, exakt **zwei bereits vorhandene PHP-Dateien**: `texterstellung.php` und `original/pste/includes/class-pste-breadth-research-queue.php`.
- Die schon einmal berechneten Familien und der schon gelesene Status werden im selben Seitenaufruf an die bestehende `openFamilies`-Methode optional übergeben. Alle alten Aufrufstellen ohne Zusatzargumente funktionieren weiter.
- **Keine neue Klasse, Datenbanktabelle, Fachregel, Entscheidung, Recherchekostenfunktion, MINI-Änderung, K0-Änderung oder Website-Schreibfunktion.**
- Fünf Cold-PHP-Durchläufe: **Median 298,6 ms, Mittel 308,1 ms**; vier → drei SQL-Leseabfragen; **vollständige 49.608 HTML-Bytes bytegenau identisch** (SHA256 `539a3a074b3df46fffb9215c008d332698d29c59901e5d31c9b9a2cefec76b62`).
- **16/16 strikte Ergebnisvergleiche** für 20/93/285/570 simulierte Kategorien und Statusmuster ALL_OPEN / EVERY_THIRD_ANALYZED / BLOCKED_AND_ANALYZED / ALL_CLOSED bestanden. Ausgangs-0.4.31.5 und Pferdeatelier nicht verändert.

## Offene Wahrheitsschranke
- **Die reale Hab-WordPress-Serverzeit, SQL-Ausführungszeit, Cache-Wirkung und eventueller Timeout wurden NICHT gemessen.** Daher erklärt die lokal vermiedene Doppelberechnung allein keine minutenlange Wartezeit auf der echten Website.
- Weitere globale WordPress-/Datenbank-/Objektcache-Effekte sind **mögliche**, aber keine bewiesenen Ursachen. Nicht auf Verdacht Cache oder Server umstellen. Kein unbelegtes Installationsrelease geben.
- Für echtes Problemende zunächst vorhandenen Hab-Request und dessen Lauf-/SQL-Zeiten prüfen, danach die lokal ausgabegleiche Optimierung auf echter WordPress-Testumgebung gegenprüfen, erst dann Freigabe.

## Tatsächlich archiviert
- ChatGPT-Library: `/hab-und-bewahr/TEXTERSTELLUNG/PRUEFUNG_PERFORMANCE_20261119/` mit vollständigem Prüfbericht, QA JSON, 13 Vergleichs-/Simulations-/Testdateien einschließlich genauem Diff. Alle Uploads mit `succeeded` bestätigt.
- **Weder** der nicht freigegebene lokale Optimierungsversuch als ZIP an Nutzer gegeben, **noch** Hab 0.4.31.5, Pferdeatelier, Universal-Blanko, Robotik, Wassertechnik oder K0 verändert.