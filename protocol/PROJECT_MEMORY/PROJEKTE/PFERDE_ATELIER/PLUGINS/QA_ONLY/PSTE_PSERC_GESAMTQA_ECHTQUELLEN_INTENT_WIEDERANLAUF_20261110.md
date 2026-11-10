# PSTE + PSERC + K0 – kombinierter QA-Gesamtlauf mit echten drei Alt-Daten (10.11.2026)

**Status: 5562/5562 lokale Positiv- und Negativprüfungen PASS – NO RELEASE; WordPress-/MySQL-Lauf ausstehend.** Es wurde keine neue Plugin-ZIP erstellt, keine WP-Instanz verändert, keine SEO-API aufgerufen und K0-Produktion unangetastet gelassen.

## Woher die Beweise stammen
- Die beiden zuletzt vom Nutzer hochgeladenen ausführlichen WordPress-Exporte sind byteidentisch: 90.640 Bytes, SHA256 `29638fef9606925b5b6f322fcde695581999ec0c41bd111bca0bcb655fbf1220`.
- Drei echte READY Artikel (Horseware Regendecken, Fliegen-/Regendecke, Regendecke 0g) aus Snapshot `PSERC 0.28.61`, `created_at_utc=2026-11-10T15:47:48+00:00`, alter PSTE-Stand `0.57.144.32`. Alle originalen `intent_profile` nur `PRE_TYPE`, aber ihre originalen `analysis_sha256` stimmen.
- Originale *physisch vorliegende* PHP-Klassen aus PSTE `0.57.144.34` und PSERC `0.28.63`. K0-QA-Binder vom GitHub-Zweig `qa/k0-editorial-owner-only-20261110`.

## Drei tatsächliche Ursachen, nicht nur Symptome

1. **Intent vor der Freigabe nicht fertiggestellt:** Der originale PSTE-Normalweg reichte das PRE_TYPE-Profil weiter, ohne immer den bestehenden `bindArticleType`-Schritt durchzuführen; PSERC durfte deswegen den Quellnachweis nicht freigeben.
2. **Die erste .34-Lokalkorrektur hatte eine falsche Schlussfolgerung:** Die originalen A/B-Klassifizierer leiten `search_intent=EDITORIAL_INFORMATION` aus der Artikelart `Beratung` ab – **nicht** aus der ursprünglichen Suchanfrage. Frühere lokale Positivtests (963) bestätigten bloß diese generische Zuordnung und sind als vollständiger SEO-Beweis **überholt**.
   **Aktuelle QA-Korrektur:** Die ursprüngliche kryptografisch gehashte `PRE_TYPE.primary_user_goal` (alle 3 `INFORMATIONAL_FOCUS`) wird unverändert für das BOUND_TYPE-Profil verwendet. A/B dienen nur als Verträglichkeitsprüfung der Artikelart, nicht als erneute Suchintent-Entscheidung. Gespeicherte `PRE_TYPE`-Analyse wird im normalen reinen Bestandswiederanlauf übernommen; bei geändertem Suchbegriff, Manipulation am Originalhash oder abweichendem SEO-Tupel/Providerbeleg folgt BLOCK statt stiller Neuerzeugung.
3. **PSERC verwendete alten Plan trotz korrigierter bestehender Themen:** Fingerprint nur aus `MAX(id)` konnte Aktualisierungen vorhandener Themenzeilen nicht sehen. **Aktuelle QA-Korrektur:** Er bindet die *bereits existierende* Abschluss-Quittung der PSTE-Bestandsprüfung (ein WP-Options-Lesevorgang) ein. Anders als im vorherigen vorläufigen Patch wird die SHA256 dieser Quittung jetzt gemäß originalem `PSTE_Breadth_Research_Queue::backlogAuditReceiptHash` **nachgerechnet**. Manipuliert = BLOCK, echte Änderung = neuer Compilerlauf, identische Quittung = kein unnötiger Neubau. Die Quittung bleibt *kein Ersatz* für die originale `existingOnlyAuditCurrent`-Frischeprüfung.

## Umgesetzte, unverpackte QA-Quelländerungen
**PSTE:** exakt zwei bestehende Dateien gegenüber bisheriger .34, **119/121 Dateien byteidentisch**.
- `includes/class-pste-intent-profile.php`, SHA256 `2b167acec91756ea0f431d0392471cd8e19d5c1aa52e6146cb8237f92872396f`
- `includes/class-pste-normal-metadata-path.php`, SHA256 `cca0af2d1a835c34b77e38ff03a04c8788c095601b49189e10d4f3d8f49721b0`
**PSERC:** genau eine Datei gegenüber .63; alle weiteren Originaldateien unverändert.
- `includes/class-pserc-plan-dependency-fingerprint.php`, SHA256 `bdee6baa73e2022dc862ddafea1d1340947d3a97c647d15502a1cdb2dc6ed7cf`.
- Vollständiger anwendbarer **QA-Quellpatch ohne ZIP**: [PSTE_PSERC_INTENT_UND_PLAN_REBUILD_HARD_QA_20261110.patch](PSTE_PSERC_INTENT_UND_PLAN_REBUILD_HARD_QA_20261110.patch), SHA256 `001bb52f27c1d14db46bebeb8cbb86ea562b477aec9dac81d2444794bbc51743`. Vorheriger Patch `PSERC_AUDIT_RECEIPT_CACHE_FIX_QA.patch` ist **durch diesen Patch überholt** und darf nicht verwendet werden.

## Tatsächlich ausgeführte vollständige lokale Probe
**Ein deterministischer QA-Durchlauf: 1.854 bestandene Einzelprüfungen**, **dreimal komplett wiederholt: 5.562/5.562 bestandene positive und negative Einzelprüfungen**. Kontrolliert mit Original-PHP 8.4 und unverändertem Benutzerexport:
- 72 ursprüngliche Intent-Herkunfts-, Identitäts-, Manipulations- und PSERC-Quellgate-Prüfungen
- 342 Original-PRE_TYPE-Erhalt / Titel-, SEO-Quellen-, Tupel-/Providerkonflikt-Prüfungen
- 330 echter PSTE-Normalweg / fehlende Kategorien, Titel, Nachweis, Fremdquelle etc.
- 573 K0-Quellbeleg- und Manipulationsfälle, inkl. bestehender alter `DECISION_SUPPORT`-Autor-Kontexte **BLOCK** bei Widerspruch
- 537 Original-PSERC-Compiler-Wiederanlauf- und manipulierter Audit-/Plan-Nachweis-Prüfungen

**Erfolg bei allen drei echten Artikelidentitäten:** Original-SEO-Voranalyse bleibt identisch, neue QA-Bindung `BOUND_TYPE` + `INFORMATIONAL_FOCUS`, PSERC normalisiert/kombiniert wieder zu drei READY-Zeilen mit **exakt ursprünglichen 5 Metadatenfeldern**. Lokaler Manifest-/Quellgate PASS. Der planlos wiederverwendete Alt-Snapshot wird bei geändertem signierten Bestandsprüfungsbeleg erkannt. 126 PHP-Dateien Lint PASS. ZIP-CRC des bestehenden PSTE-Basispakets: 121/121 PASS. Wiederholungsausgabe deterministisch.

## Wichtige Grenze – damit es nicht erneut einen Blindversuch gibt
Dieser lokale Komplettlauf benutzt zwar echte Ausgangsdaten und Original-PHP, aber **simulierte WordPress-Optionen, Datenbank-Watermarks, Kategorien, Belege und vorhandene A/B-Typzuordnung**. Es wurde **kein realer WordPress/MySQL-Prüflauf**, **kein echtes Durcharbeiten aller ~5.000 gespeicherten Themen**, **kein neuer echter WP-Snapshot** und **keine echte K0-Artikelproduktion** durchgeführt. Die erzeugte lokale 3-Artikel-Manifestdatei ist **nur ein Prüfstück**, kein hochladbarer Produktionsbeleg.
Kein 0.57.144.35/0.28.64-ZIP, keine Installationsbitte, keine Livefreigabe. Die alten Texte zu `963 PASS` dürfen nicht als Nachweis einer echten Suchintent-Übernahme ausgegeben werden.

**Abnahme:** `LOCAL_FULL_WORKFLOW_SIMULATION_PASS`, `REAL_WORDPRESS_END_TO_END_UNTESTED`, `NO_INSTALLATION`, `NO_LIVE_RELEASE`, `K0_UNTOUCHED`.

## Verbindliche Freigabe erst nach
Einmaliger gezielter TEST-WordPress-Rücklauf (beide bestehenden Komponenten zusammen): vorhandene PSTE-Daten bestandsbasiert neu prüfen ohne Provider-Recherche, signierte aktuelle Prüfquittung erhalten, nur dadurch neuen PSERC-Plan erzeugen, auf **denselben 3 READY-Artikeln** mit BOUND_TYPE/PSTE-originaler Intent-Herkunft prüfen und echten Export `mit-suchintent-nachweis` gegen isolierten K0-Quellwächter abnehmen. Fehlermeldungen dürfen **nicht** still verschluckt werden. Alle Produktionszweige und echte Texte bleiben bis dahin gesperrt.
