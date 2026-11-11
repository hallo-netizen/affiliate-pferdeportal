# K0 bleibt unberührt: Quelle, vermeintliche Entscheidungssperre und echter TXT-Export – 11.11.2026

**Ziel:** Nicht erneut an einem alten K0-Testjob festbeißen und keine abgeschafften Entscheidungen wieder einführen. K0-Produktionszweig bleibt read-only.

## 1. Harter Quellvergleich (GitHub, gleiche Branchstände 11.11.2026)

- `engine/k0_writer_station.py` in `konzept0-portal-neutral-20261002` und `qa/k0-editorial-owner-only-20261110` **identisch** (GitHub Blob SHA `7c3ad1ead844c1126338b3556af804d69407ca08`).
- `engine/k0_full_rules.py` in beiden Branches **identisch** (SHA `da82fbd6c40184db8e6ce9b59b8c9d1e328acc27`).
- `.github/workflows/k0-authoring-context.yml` auf dem AKTIVEN K0-Zweig enthält **keinen** Aufruf von `engine.k0_seo_owner_binding`. Der neue SEO-Owner-Binder ist **ausschließlich** auf dem isolierten QA-Zweig eingerichtet, nicht K0-Produktion.
- Die zuletzt diskutierte Sperre `K0_OWNER_INTENT_CONFLICT_WITH_EDITORIAL_APPROVAL` ist damit **kein aktiver Produktions-Stopper** und kein Grund, vorhandene K0-Regeln zu verändern.
- Der historische `content_profile.search_intent=DECISION_SUPPORT` im *bereits abgeschlossenen* Horseware-Lauf ist eine Eigenschaft seines damaligen Schreibauftrags, nicht eine neue Entscheidung über die aktuelle PSTE-Suchintention `INFORMATIONAL_FOCUS`. Den abgeschlossenen Job nicht überschreiben; keine angebliche Inkonsistenz in der aktiven Produktion daraus ableiten.

## 2. Geprüfter EXISTIERENDER K0-Originalartikel statt künstlichem Text

Quelle: `real_runs/k0/k0-20261110-42619ca7-01-r2/` auf aktivem Branch `konzept0-portal-neutral-20261002`, lesend abgerufen.

- `SEALED_WRITER_PRODUCT.json`: `K0_ARTICLE_PACKAGE_V1`, `writer_provenance.status=PASS`, K0-Fachregelbindung 85 harte Artikelregeln, `publish_allowed=false`.
- `WORDPRESS_SINGLE.json`: `SYSTEM4_WORDPRESS_HANDOFF_V1`, **1** Artikel, `test_suite_status=PASS`, `batch_gate_status=SYSTEM4_BATCH_FULL_PASS_COLLECTED`, `wordpress_review.direct_wordpress_upload_ready=true` (d. h. Paket zur direkten WordPress-Importprüfung vorbereitet; **kein Nachweis eines tatsächlich angelegten WordPress-Beitrags**).
- Für denselben Artikel: **Original-HTML-Text byteidentisch** zwischen SEALED_WRITER_PRODUCT und WORDPRESS_SINGLE, selbe Artikelidentität und `final_draft_sha256=0cb4186767b56e4eb08e158b0397ff15f77034f9b53f1d21395700924c8facb0`.
- `languagetool.status=PASS`, Engine `LanguageTool 6.8`, `finding_count=0`.
- `ppm679.status=PASS`, `content_quality_status=CONTENT_QUALITY_CHECK_OK`, `fail_closed_aggregate_status=PASS`.
- `WORDPRESS_VERIFY.json`: `K0_WORDPRESS_EXPORT_VERIFY_V3`, `status=PASS`, `canonical_binding=PASS`, `publish_allowed=false`.
- Derselbe versiegelte Artikel liegt auf dem QA-Branch unverändert mit gleicher Blob-Identität; keine Neugenerierung.

## 3. Neue, wirklich erzeugte TXT aus diesem echten Bestand

[**K0_HORSEWARE_GEPRUEFTER_BESTANDSARTIKEL_TEXTEXPORT_20261111.txt**](K0_HORSEWARE_GEPRUEFTER_BESTANDSARTIKEL_TEXTEXPORT_20261111.txt)

Die TXT ist eine reine textuelle **Ableitung aus dem originalen, bereits vorher geprüften K0-Artikeldokument**, nicht aus dem künstlichen DataForSEO-Testtext. Ohne Quell-Spuren-Tags, aber mit Abschnittsüberschriften und Linkzielen; **853 Wörter im Textkörper, 7 Zwischenüberschriften**, 7.026 Zeichen gesamte TXT, danach per GitHub `fetch_file` bytegenau zurückgelesen. Writer-/WordPress-Ausgangsdateien unverändert. Kein erneuter Artikelstart, keine Veröffentlichung.

Die TXT darf nicht als neu aus PSTE .35/PSERC .65 hergestellter Artikel bezeichnet werden: Der zugrunde liegende K0-Job wurde mit der früheren Suchintent-Beschreibung geschrieben. Sie beweist den **vorhandenen realen K0-Schreib-/Dateiausgabe-Endpunkt** und die Unnötigkeit eines erneuten K0-Laufs zur Prüfung dieses Teilabschnitts.

## 4. Echte verbleibende Lücke – isoliert VOR K0

Der neue PSTE→PSERC-Quellweg muss auf der getrennten WP-Testinstallation einmal mit echten gespeicherten Datensätzen die alte PRE_TYPE-Planversion vollständig ersetzen und `mit-suchintent-nachweis` exportieren. Das ist **noch nicht bewiesen**. Die vorangegangene 20-malige DataForSEO→TXT-Simulation enthält künstliche Texte und einen K0-Schnittstellenmock; zusammen mit dem hier geprüften bestehenden K0-Original ergibt sie **keinen frisch durchgelaufenen einzigen Echtlauf von DataForSEO bis neuem K0-Text**. Bestehende Autorensysteme, K0 und WordPress-Live bleiben unberührt.

**Ergebnis:** K0-Produktionssperre **NICHT vorhanden**; K0-Originalartikel/WordPress-Export/TXT **geprüft**; PSTE→PSERC realer WordPress-Datenbank-Wiederanlauf **weiter offen**. Kein neues Plugin, keine neue SEO-Recherche, keine K0-Regeländerung.
