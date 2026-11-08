# ECHTER zweiter MINI-Parkhausexport 08.11.2026, 15:03:46 UTC – Export technisch vollständig; Datenqualitätsfehler noch vorhanden

**Privater Originalexport unverändert** in der Pferdeatelier-Dateibibliothek unter `/pferdeatelier/pferdeatelier-mini-ergebnisse-20261108-150347(1).json` (Library `libfile_7084c8a325c481918d5f9e6d33fc7503`). NICHT ins GitHub-Repo kopiert (unveröffentlichte WordPress-/Redaktionsdaten). 1.043.468 Byte, SHA256 `f31e68a5de77be965e384e4b7517ec7a48a7cd1ca8ae6631b9fb5637dd93a2ba`, als echtes vollständiges JSON lokal eingelesen/geprüft.

## Aus dem tatsächlichen Export, ohne Vermutungen

`contract=PSTE_MINI_RESULTS_FOR_EDITORIAL_V1`, `count=100`; 87 `JA` / 9 `VIELLEICHT` / 4 `NEIN`; `seo_subjects=87` und alle 87 Quellbegriffe aus JA-Einträgen vorhanden. Nach gezieltem PSERC-Snapshot-Refresh `parkhaus_complete=true`, `parkhaus_snapshot.complete=true` und `parkhaus_snapshot.sha256` nicht leer. `status=PARKHAUS_FOR_SINGLE_EXTERNAL_SEO_OWNER_NOT_APPROVED` besagt korrekt: noch KEINE externe FREI/BELEGT/KLÄRUNG-Entscheidung.

Quellen/Einträge: `WORDPRESS 1.024` (`page 425`, `post 163`, `pa_breed 196`, `uge_term 184`, `hp_listing 55`, `hp_vendor 1`), `PSTE_PLAN 1`, `EDITORIAL_PLAN 9`, `PSERC_ACTIVE_PLAN 1`, `PPM679_EXISTING_EDITORIAL_RUNTIME 144`, `MINI_RESERVED 0`. Summe `1.179`. WP 1.004 publish und 20 draft. PSERC-Snapshot jetzt `complete=true`, keine veraltete Planquelle. PPM679 `complete=true`, Status PRESENT. **Dieser Export ersetzt den ersten von 14:45 UTC als aktuelle technische Quelle.**

## Noch nicht vertrauenswürdige Nutzinhalte

- **Neun `EDITORIAL_PLAN`-Einträge haben exakt den Titel `"Array"`**, übrige Felder leer, die Quellenmeldung ist sogar `status=NOT_AVAILABLE` bei 9 Items. Die Daten sind nicht sinnvoll semantisch vergleichbar. Aus dem tatsächlichen installierten PSTE-Code: `PSTE_Snapshot::normalizeEditorialPlanItemsAgainstStructure` konvertiert `$item['title']` per `(string)` statt zu prüfen, ob es eine echte Zeichenkette ist. Bei eingebettetem Array entsteht die wörtliche Zeichenfolge `Array`, die `readParkhausForMini` dann als Titel weitergibt.
- 144 `PPM679_EXISTING_EDITORIAL_RUNTIME`-Einträge enthalten belegte `canonical_article_id` und `plan_slot`, aber alle 144 explizit `title=""`, `target_keyword=""`, `category=""`. 141 von 144 `post_id` verweisen auf einen im selben WordPress-Snapshot vorhandenen Post, dessen Titel sich beim gleichen Export tatsächlich auslesen lässt. Drei `post_id` haben dort keinen Treffer. Der bisherige Export holt keinerlei Darstellung aus der verlinkten WordPress-Zeile nach, obwohl er sie bereits enthält. Nur technische Belegungskennung, nicht genügender semantischer Vergleichstext.
- Das boolesche `complete=true` belegt damit derzeit **technische Quellpräsenz und Prüfsumme**, **nicht** vollständige/brauchbare inhaltliche Artikelbezeichnungen. Kein ungeprüftes FREI-Urteil aus diesem Export.

## Zielkonzept und Bedienung

Extern: EINMAL pro Thema Suchintention und Artikelbelegung anhand des vollständigen realen Parkhausplans, Ausgänge FREI/BELEGT/KLÄRUNG. WP: reine technische Bindung/Frische/Platzprüfung, dann bestehender PSERC→K0-Weg. Die sichtbare PSERC-Metadaten-Vorschau, alte Kategorien-/Titel- und Stichwort-Tests sind vor allem historisch gewachsene Diagnose-/Sonderfunktionen; sie sind keine vom Betreiber regelmäßig zu bedienenden zusätzlichen Fachentscheidungsstellen. Für den neuen Normalablauf soll die UI nur **Export → extern entscheiden → Ergebnis importieren → Status** zeigen, mit alten Diagnoseaktionen in geschütztem Expertenbereich, ohne Sicherheitsprüfungen abzuschalten.

## Konkrete Reihenfolge

1. bestehenden PSTE-Parkhaus-Export korrigieren: Array-Titel nicht mehr in echte Namen umwandeln; den Ursprung korrekt auslesen oder solche Quelle als unverlässlich gesondert markieren. PPM679-Titel aus schon im **gleichen Snapshot** vorhandenen Posts zuordnen; drei verwaiste Bezüge explizit klären, keine erfundenen Titel.
2. Auf der vorhandenen echten JSON-Datei lokal positive/negative Qualitätstests durchführen (kein WP-Live-Schreibzugriff). **Nur nachdem vollständige Titel/Quellen nachgewiesen wurden**, einmalige fachliche SEO-Entscheidung durchführen; keine zweite WP-SEO-Fachprüfung. Kein 5.016er-Gesamtlauf.
3. UI im PSTE/PSERC-Testzweig auf wenige normale Aktionen reduzieren, alte Spezialfunktionen nur ausblenden, nicht Daten/Sicherheitsgates löschen. Testinstallation ausschließlich nach Paket-QA. K0 und Live-Seite unverändert.

Status: Datenexport hat wichtigen technischen Fortschritt; fachliche End-to-End-Freigabe noch NICHT PASS.
