# EIGENTUMSSCHUTZ – KONZEPT – FEHLERQUELLEN

## HB-CONCEPT-001 – Ein-Kind-/Zwei-Kind-Klickebenen
Status: bestätigt in WordPress-R2-Konzept, **R3 nur strukturell gelöst; Live-Fix NICHT umgesetzt**.
Befund: 19 von 31 L2-Bereichen nur 1 L3, 10 nur 2; Nutzerregel 3–10 direkte Unterebenen. Nicht durch ein rein optisches Menü kaschieren.

## HB-CONCEPT-002 – SEO-Owner- und Artikel-Doppelungsrisiko
Status: **EDITORIAL-VORPRÜFUNG ERLEDIGT, SEO-SERP-FREIGABE OFFEN**. Für 144 R3-Kandidaten sind je drei konkrete Vorschläge (432) formuliert, exakt mit den 704 alten Titeln abgeglichen und 17 lexikalische Nähen fachlich vorsortiert. Die 21 früher offenen R2-Owner haben vorläufige redaktionelle Abgrenzungen; im aktuellen V5-Fachplan insgesamt 19 Themenumhängungen (keine Kopien), eine Keyword-Aliasregel. Trotz exakter Titeldeduplizierung sind semantisch getrennte Suchintents und organische SERP-Owner weiterhin nicht nachgewiesen. Autoritative Detailakten im KONZEPT-Büro: `R3_REDAKTION_144_KATEGORIEN_432_IDEEN_20261013.md` und `R3_BESTANDSOWNER_21_FACHPRUEFUNG_20261013.md`.

V5-Arbeitsfassung: `R3_V5_144_KATEGORIEN_432_IDEEN_EDITORIAL_FACHPLAN_20261013.md`. Trotz 14 redaktionellen Titelpräzisierungen und 0 exakten Wiederholungen **bleibt echte organische Suchintent-/Google-SERP-Überschneidung offen**. Quelle für verbindlichen Status und NEXT ACTION: `CURRENT_STATE.md`.

## HB-CONCEPT-003 – Beleggrenze für Live
Status: **OFFEN**. R3 weiterhin ausdrücklich nichtimportierbarer Konzeptentwurf, trotz Struktur- und Redaktionstiteltests. Keine neuen WordPress-Kategorien, keine neue veröffentlichte URL. R2 weiter maßgeblich für WordPress.

Sperre: Vor tatsächlichem Umbau erst vollständige fachliche Abnahme, Kollisionstest, Redirect-/URL-Prüfung und freigegebenes Zielprofil.

## HB-CONCEPT-004 – 3–10-Auswahlregel im Live-Validator fehlt noch
Status: **TECHNISCHE REGEL-LÜCKE BESTÄTIGT / NICHT MODIFIZIERT**. Prüfung der lokalen Original-ZIP `HAB_UND_BEWAHR_KATEGORIE_WORKFLOW_1.14.8.17_SERP_FORTSETZUNG_34V40.zip` vom 13.10.2026: `class-apkw-target-tree.php` validiert bereits das Minimum an Artikeltiteln je Blattkategorie und `min_categories_per_third_page` (3); `class-apkw-target-tree-dry-run.php` begrenzt `max_megamenu_children` auf 10 und fordert bei Welten bisher nur **mindestens 1** direktes Kind. **Ein allgemeiner harter Mindestwert 3 für jeden anklickbaren Zwischenknoten wird im geprüften Plugin noch nicht erzwungen.** Die R2-Struktur mit 19/10 Ein-/Zwei-Kind-Bereichen konnte daher gültig sein. Vor R3-Release muss die verbindliche 3–10-Strukturprüfung im bestehenden Validator nachvollziehbar ergänzt und mit Negativfällen getestet werden; keine Architekturänderung und kein vorgezogenes Pluginupdate nötig.
