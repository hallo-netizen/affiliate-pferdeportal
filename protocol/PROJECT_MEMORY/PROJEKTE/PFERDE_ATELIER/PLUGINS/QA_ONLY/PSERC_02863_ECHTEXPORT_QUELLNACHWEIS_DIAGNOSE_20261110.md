# PSERC 0.28.63 – Quelldaten nicht mehr still verlieren (QA, 10.11.2026)

**TEST / QA ONLY. Kein Live-Update. K0 aktiv, PSTE, DataForSEO, PSERC-Fachentscheidungen und WordPress-Daten unberührt.**

## Anlass und belegte Grenze
Die aktuelle vom Nutzer direkt aus der installierten WordPress-Testseite exportierte Datei `seo-redaktionsplan-ohne-suchintent-nachweis-42619ca7...json` ist tatsächlich bloß der originale validierte 5-Felder-Batch (3 Beratung-Artikel). Die gespeicherte Suchintent-Entscheidung war schon im PSTE-System vorhanden und wird in den PSERC-`final_item`-Manifestdatensatz kopiert; der bisherige K0-Fünf-Felder-Vertrag enthält sie **nicht**. Es gibt keinen Nachweis, dass die WordPress-Testdaten des Nutzers noch alle drei signierten `final_item.intent_profile` enthalten.

In PSERC 0.28.62: `PSERC_Admin::exportSingleHandoff` versuchte die Manifest-Ausgabe. Bei exception wurde der Fehler **leer gefangen** und nur der alte 5-Felder-Export als `ohne-suchintent-nachweis` ausgeliefert; ebenfalls konnte eine Fehlprüfung der signierten Manifeststruktur ohne konkrete Meldung auf den Alt-Export zurückfallen. Damit wurde ein echtes Problem verborgen und wiederholte Uploads ohne neue Erkenntnis ausgelöst. Dies ist aus Originalcode und exakt dem hochgeladenen Dateiformat verifiziert; **welche konkrete Ursache im echten WordPress liegt, bleibt ohne dessen private gespeicherte Datensätze unbelegt**.

## Gezielt korrigiert
Nur Export-Admin, eng geprüfte `.61/.62 -> .63` Upgrade-Kompatibilität, Versionskopf und signierter Paketvertrag geändert (exakt 4/63 Dateien; 59 vollständig unverändert).
- **Ein** Download bleibt.
- Erfolgreich signiertes Manifest mit PASS-Profilen → unverändertes `mit-suchintent-nachweis`-Manifest. Keine neue Suchintent-Entscheidung.
- Signiertes Manifest mit fehlendem, ungültigem oder manipuliertem PSTE-Profil → Originalmanifest `ohne-suchintent-nachweis`; getrennte K0-Herkunftsprüfung blockiert weiter die fachlich nicht belegte SEO-Freigabe.
- Scheitert bereits das Lesen/Erzeugen/Prüfen des alten Detailmanifests → **statt stiller Fünf-Felder-Datei** ein nicht freigabefähiger, signierter `PSERC_K0_SOURCE_PROOF_DIAGNOSTIC_V1`-Container mit präzisem `source_proof_error_code` und dem **originalen, byte-/hashgleichen Fünf-Felder-Batch verschachtelt unter** `next_textmachine_metadata_batch`. Kein Weg zur K0-Freigabe aus dem Diagnosecontainer und keine Herkunftsbehauptung.
- Bestehende 5-Felder-/Planplatz-/Titel-/Kategorien-/Hash-/Frische-Prüfungen unverändert. Im Manifestvergleich wird die bereits vorhandene kanonische Hashidentität anstelle einer unsachlich von PHP-Array-Schlüsselreihenfolge abhängigen Gleichheitsprüfung verwendet. Die geprüfte Manifestumhüllung wird pro Download **nur einmal** validiert, nicht erneut im Suchintent-Leseschritt.
- K0-Regelkatalog, K0-Writer, LanguageTool, Recherche- und Kategorie-Workflows, Artikel, Tabellen, WordPress-Live, gespeicherte PSERC-Recherchen **nicht** verändert.

## QA (nicht mit echtem WordPress verwechseln)
- Echte aus QA 0.28.62 gelesene 63-Dateien-ZIP als Ausgangsbasis; nur vier Originaldateien gegenüber Ausgangspaket geändert.
- **43/43 PHP-Syntax**, **61/61 Integritätsdateien** mit tatsächlicher `PSERC_Package_Integrity::validate`-Funktion, ZIP CRC PASS.
- 3 echte historische Nutzer-Artikel-IDs und ihr unveränderter 1393-Byte-Export als Eingabedaten; die WordPress-Options-/SQL-Datensätze sind im **lokalen Test bewusst simuliert**. Die Original-PHP-Klassen `PSERC_Admin`, `PSERC_Plan_Snapshot_Store`, `PSERC_Metadata_Boundary`, `PSERC_Stable_Json` liefen tatsächlich.
- Validiertes synthetisches PSTE-Profil für jede Original-ID: vollständiges signiertes Manifest PASS, eine unveränderte Fünf-Felder-Datei darin. Fehlendes bzw. manipuliertes Profil: Manifest vorhanden, fachlicher Nachweis getrennt FAIL, kein positives Umschreiben. Fehlender historischer `final_item`: Diagnoseexport mit konkretem `PSERC_PLAN_READY_DETAIL_INVALID`. Widersprüchliche Metadaten: Diagnose statt falscher Freigabe. Geänderte Reihenfolge identischer Metadatenfelder: kanonische Gleichheit PASS. Korruptes Ready-Index-Binding, altes Header-Hash, veraltete Abhängigkeiten: weiterhin STOPP. In allen sechs erfolgreichen Download-Szenarien 3/3 Originalpositionen exakt und unverändert erhalten.
- Enge Snapshot-Upgrade-Kompatibilität 0.28.61→0.28.63 und 0.28.62→0.28.63 PASS; manipulierter Alt-Hash, Inventaränderung, Produktionskapabilität geändert, falscher alter Build, unbekannte Vorgängerversion und beschädigtes neues Paket werden blockiert (8/8 Testfälle).
- **Nicht getestet:** echte WordPress-Testdatenbank mit ihren vorhandenen originalen PSTE-Intent-Belegen, Installation in WordPress, K0-Produktion und Livebetrieb. Keine Behauptung, das noch unbekannte Detaildatensatz-Problem sei vollständig gelöst.

## Datei, Archiv und nächster Schritt
- TEST-ZIP: `PSERC-0.28.63-QUELLNACHWEIS-DIAGNOSE-NUR-WORDPRESS-TEST.zip`
- SHA256: `c8bde7a453cd8a6b4320fa3d9b2c8e79dce740334bfad959dd54c9d14e3de606`
- Archiv: `/pferdeatelier/PLUGINS/QA/` (separate Plugin-Library).
- **Einziger konkreter Anschluss auf TEST:** bestehendes Plugin auf 0.28.63 aktualisieren, ohne Planneuaufbau genau einmal `Produktionsübergabe herunterladen`, JSON bereitstellen. Falls Diagnosecontainer, enthält er jetzt die tatsächliche ausgelöste konkrete Fehlermeldung und alle 3 Metadaten; falls volles Manifest, Intentprofile ohne weitere Recherche vollständig prüfbar. K0 weiterhin unangetastet.
- **Status:** `QA_PACKAGE_VERIFIED; DUPLICATE_PROOF_CHECK_REMOVED; SOURCES_NOT_FABRICATED; NO_LIVE_GO; WORDPRESS_ORIGINAL_PROFILE_CAUSE_PENDING`.
