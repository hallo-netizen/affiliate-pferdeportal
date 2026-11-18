# Pferdeatelier – Texterstellung **0.4.30**: MINI-Kategorie-Ursache behoben

Stand: 18. November 2026. **Live-Einspielung noch nicht bestätigt.**

## Nachgewiesene Ursache
- Von Live exportierte Datei `mini-checkpoint-category-20261118.json` enthält `category: "MAGAZIN"` sowie leeres `category_slug`; korrekte Feldnamen sind `route` und `category_slug`. Original-Live-Diagnose meldet für den Rückimport `MINI_WORKER_FROZEN_FIELDS_CHANGED` auf der CATEGORY-Station; `Auftragsregal: 0`.
- Version 0.4.29 lieferte zwar die komplette WordPress-Kategorieliste, aber keine eindeutig benannte Magazin-Unterkategorieliste und keine direkt aus den unveränderten Ursprungszeilen hergestellte CATEGORY-Vorlage. Die eine vorhandene CATEGORY-Prüfung prüfte bloß eine WordPress-Kategorie per Slug, nicht deren erlaubte Magazin-Zugehörigkeit oder Fach-Unterkategorie.
- `MAGAZIN` ist ein **Bereich**, keine WordPress-Kategorie. Original-PSTE hat einen ausdrücklichen Journal-Kategorievertrag mit neun möglichen Unterkategorien, u. a. `Alltags-Pferde-Haltungsformen` (`alltags-pferde-haltungsformen`). **Die Auswahl ist nur zulässig, wenn die Kategorie im eingefrorenen echten WordPress-Bestand vorhanden ist.**

## Codefix – eine Stelle, keine neue Prüfung
- MINI-Export bindet aus der bestehenden WordPress-Kategorieliste die real vorhandenen ursprünglichen Journal-Unterkategorien in `magazine_categories`; `category_checkpoint_template` enthält für jede ausgewählte Zeile alle unveränderlichen Originalfelder plus **exakt** `route,category_slug,article_type`.
- **Nur die bestehende CATEGORY-Station** prüft die einmal getroffene Entscheidung gegen die eingefrorene WordPress-Kategorieliste. MAGAZIN: ausschließlich konkrete Original-Journal-Unterkategorien; FACH: passende echte Artikel-Unterkategorie, keine Oberkategorie und keine Magazin-Unterkategorie; REDAKTIONSBUERO: ohne Kategorie/Typ. Keine zweite fachliche Entscheidung.
- Generischer Fehler `MINI_WORKER_FROZEN_FIELDS_CHANGED` wird beim konkreten Fehler `category: MAGAZIN` als `MINI_ROUTE_MUST_BE_FIELD_ROUTE_NOT_CATEGORY` erklärt. Bestehender Auftrag bleibt zur **Korrektur durch denselben MINI-CATEGORY-Arbeiter** offen; kein neuer Auftrag und keine neue kostenpflichtige Recherche.
- Auch **eingefrorene 0.4.29-Chargen** werden unverändert wiederaufgenommen; beim Re-Download wird nur die Orientierung ergänzt, ursprünglicher Quellhash/Entscheidungsstand nicht überschrieben. Endgültige Import-Headerprüfung berücksichtigt die hinzugefügten reinen Anzeigeinformationen.
- **MINI-Export** und **MINI-Import** sind ab 0.4.30 zwei separate WordPress-Menüs/Tabs und Seiten, je ein eigenes bisheriges Formular. Vorheriges `texterstellung-redaktion` führt zum MINI-Export.
- Kein K0-Umbau, keine Datenbank-Resetaktion, keine zweite Redaktion, keine automatische Veröffentlichung, keine Änderung bei Hobbydepot/Hab & Bewahr.

## Plugin-Artefakte und technische Tests
- ZIP im Pferdeatelier-Pluginbüro `/pferdeatelier/PLUGINS/ARBEITSRAUM_PSTE_KISS/Texterstellung-0.4.30-KISS-MINI-KATEGORIEN-GETRENNTE-SCHRITTE.zip`.
- SHA256: `34e2b8e955e5bdd077e488248286bf2864050cb9070bbc74e48c06de5d47a825`.
- Basis ist das echte 0.4.29-ZIP. Genau **2 von 88 Dateien** geändert; Original-PSTE, Original-PSERC, K0 und alle anderen 86 Dateien bytegleich.
- `php -l` 78/78; 38/38 Import-/Diagnose-Regressionstests; **16/16 neue MINI-Kategorie-, Alt-Chargen- und UI-Tests**, einschließlich Reproduktion der einen realen fehlerhaften MINI-Datei, fehlender Kategorie, falscher Route, Oberkategorie und korrekt gebundener Journal-Unterkategorie; ZIP CRC ohne Fehler.
- Prüfbericht und beide Testlogs ebenfalls unter `/pferdeatelier/PLUGINS/ARBEITSRAUM_PSTE_KISS/`.
- **Status:** Installationsfähiger, lokal gegen WordPress-Mocks geprüfter Kandidat; kein echter Live-WordPress-Durchlauf. **0.4.29 ist noch die zuletzt aus Nutzerscreenshot bestätigte Liveversion.**

## Einziger Nutzerweg
1. WordPress → Plugins → Plugin hinzufügen → Plugin hochladen → ZIP 0.4.30 installieren → alte Version **ersetzen, nicht löschen**.
2. Texterstellung → MINI-Export → **MINI-Gesamtauftrag herunterladen** (noch laufender Auftrag wird fortgesetzt). Keine Recherche starten.
3. Im selben MINI-Chat die mitgelieferte `category_checkpoint_template` verwenden und Kategorie **aus den angebotenen aktuellen WordPress-Kategorien** einsetzen: `route=MAGAZIN` und `category_slug` exakt aus `magazine_categories`; K0-Typ aus `k0_article_type_capabilities`.
4. Texterstellung → MINI-Import → korrigierten CATEGORY-Zwischenstand hochladen, bestehenden MINI-Arbeitsauftrag danach fortsetzen. Kein Neustart, keine zusätzliche manuelle Zuordnung.
