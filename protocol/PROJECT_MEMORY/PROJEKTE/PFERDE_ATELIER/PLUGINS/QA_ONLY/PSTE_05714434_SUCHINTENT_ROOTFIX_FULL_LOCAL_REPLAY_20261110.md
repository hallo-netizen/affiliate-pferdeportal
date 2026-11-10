# PSTE 0.57.144.34 – Suchintent endgültig vor K0 binden; realer Drei-Artikel-Replay

**Stand 2026-11-10. Isolierte QA, nicht Live, keine Änderung an K0-Produktion.**

## Bewiesene Ursache (originale .33 gegen QA .34)
Das echte vom Nutzer exportierte PSERC-Manifest enthält drei READY-Artikel mit `PSTE_INTENT_PROFILE_V2...` im Status `PRE_TYPE/PASS`. Die ursprüngliche `PSTE_Normal_Metadata_Path::applyToPayload` gab nach normaler Themenbearbeitung bei allen drei `NORMAL_PASS` zurück, aber speicherte nur die vorläufige Intent-Analyse. Die bereits im originalen PSTE implementierte Funktion `PSTE_Intent_Profile::bindArticleType()` wurde auf dem Normalweg vor Freigabe nicht aufgerufen. PSERC liest/kopiert dieses Profil korrekt weiter und kann folglich keine abgeschlossene SEO-Quellenfreigabe nachweisen. **Original .33: 3/3 NORMAL_PASS + PRE_TYPE. QA .34: 3/3 NORMAL_PASS + BOUND_TYPE/PASS.**

## Minimal-invasive QA-Änderung
Original-Paket `PSTE-0.57.144.33-KISS-BEREINIGT-NUR-TEST.zip` mit 121 Dateien. Neue QA-Datei in persönlicher Library `/pferdeatelier/PLUGINS/QA/PSTE-0.57.144.34-EINMALIGE-SUCHINTENT-BINDUNG-NUR-WP-TEST.zip`, SHA256 `1496567e6433a7d57cdd0e1697ad978babb35ecfd0ca10a5d750da999d47a4ad`.

Exakt **3/121 Dateien** geändert, **118/121 byteidentisch**:
- `includes/class-pste-semantic-classifier.php` gibt den **bereits vorhandenen** übereinstimmenden A/B-Suchintent aus, ohne zusätzliche Entscheidung.
- `includes/class-pste-normal-metadata-path.php` verlangt vor `NORMAL_PASS` die gebundene finale Suchintention, nutzt originale `bindArticleType`, prüft Typ-/Familienübereinstimmung und signiertes Profil, aktualisiert bestehenden Profilbeleg an unverändertem Titel/Keyword. Fehlende/abweichende Freigaben bleiben `REVIEW_REQUIRED`.
- `portal-seo-topic-engine.php` ausschließlich Versionsnummer `.33→.34`.

Keine neuen WP-Tabellen, Cron-Jobs, fachliche Entscheidungen, Recherche-/Kategorien-/Titelworker oder K0-Regeln. PSERC .63 unverändert.

## Umfang der tatsächlich ausgeführten lokalen Tests
Mit PHP 8.4 und ursprünglichen realen **drei Artikelidentitäten** sowie dem echten Benutzer-Manifest:
- **60/60** Positiv-/Negativprüfungen des originalen PSTE-Intent-Binders und PSERC-Manifest-/SEO-Gates, u.a. A/B-Dissens, fehlende/falsche Typ-/Familienentscheidung, beschädigte Profil-/Manifestsignatur, fremder Planplatz, fehlende/alte Profile.
- **330/330** Wiederholungs-/Negativprüfungen der tatsächlichen `PSTE_Normal_Metadata_Path::applyToPayload` mit Originalklassen: 35 Wiederholungen x 3 Artikel x 3 Identitäts-/Profilprüfungen, fehlende/falsche Relevanzbelege, falsche Titel-/Keywordidentität, fehlende Kategorien und fehlende Titel.
- Alle drei Kandidaten: originale PSTE-Normalverarbeitung → `PSERC_SEO_Reader::normalizeCandidate` **3/3 ELIGIBLE** → `PSERC_Compiler::finalizeAllocationRow` **3/3 READY** → originale `PSERC_Admin`-Manifest-/SEO-Quellenprüfung **3/3 PASS**, unveränderter Fünf-Felder-Batch.
- **573/573** separate lokale Prüffälle entsprechend dem bestehenden isolierten K0-Quellenbindungsvertrag, darunter 200 deterministische Wiederholungen, 350 absichtlich manipulierte Versionen, vorläufige Originalprofile BLOCKED, 3 finale QA-Profile PASS. Für **bestehende alte Autor-Kontexte** mit fremdem `DECISION_SUPPORT` erfolgt bewusst **BLOCK** – keine unbewiesene Überschreibung.
- **963/963 ausgeführte positive/negative Checks bestanden**, dazu **83/83 PSTE- und 43/43 PSERC-PHP-Syntax PASS**, ZIP-CRC/Pfad-/Versionsprüfung und Original-3er-Hash-/Identitätsparität PASS.
- Ein erster Test mit fehlendem externen Relevanznachweis zeigte für zwei originäre Pferde-Queries die **korrekte interne Portalkontextfreigabe**, für die markenspezifische Abfrage den **richtigen Sonderfall STOP**. Die Testannahme wurde korrigiert, **ohne Produktcode zu ändern**.

## Ehrliche Freigabegrenze
- QA-Replay verwendet reale 3-Artikel-Metadaten, reale PRE_TYPE-Analysen und die echten PSTE-/PSERC-PHP-Funktionen. **Die WordPress-Kategorienregistrierung und externe Relevanzfreigabe sind im lokalen Test ausdrücklich synthetisch** (originale Kategorie-ID/Slug belegt). Der letztlich im QA-Lauf signierte BOUND_TYPE-Wert ist **Simulation, kein aus realer WP-Datenbank ausgelesener Originalfreigabebeleg**.
- Keine tatsächliche WordPress/MySQL-Installation dieses Pakets; kein kostenpflichtiger DataForSEO-Liveabruf, keine echte K0-Produktion von drei neuen Artikeln, kein WordPress-Import.
- Der bestehende **alte** PSERC-Plan-Snapshot ist durch die korrigierte **PSTE-Quelle** nicht rückwirkend umgeschrieben. Ein neuer, kontrollierter PSERC-Plan aus vorhandenen gespeicherten Daten ist erforderlich, um die neue BOUND_TYPE-Bindung wirklich in den Export zu übernehmen. Dafür ist **keine bezahlte Neurecherche** im Code vorgesehen, aber die genaue WP-Test-Frische-/Rebuild-Kompatibilität ist noch nicht real getestet. Kein Live-GO.
- K0 QA-Binder besitzt eine absichtliche Widerspruchssperre: historischer K0-Kontext-Intent `DECISION_SUPPORT` versus SEO-Owner `EDITORIAL_INFORMATION`. **Alte Writer-Jobs nicht in-place ändern**. Neue Contexts nur mit originalem SEO-Bindungsbeleg erstellen; nicht aus Artikeltyp erneut raten.

**Status:** `ROOT_CAUSE_FIXED_IN_PSTE_QA_CODE`; `LOCAL_METADATA_END_TO_END_PASS`; `LOCAL_POS_NEG_REPLAY_963_PASS`; `LIVE_WP_E2E_NOT_TESTED`; `K0_PRODUCTION_UNCHANGED`; `LIVE_RELEASE_NOT_APPROVED`.

Nächster zielgerichteter Schritt ist EIN WordPress-TEST-Lauf mit bestehenden gespeicherten drei SEO-Quellen, PSTE .34 und vorhandenem PSERC .63: erneute einmalige redaktionelle Planzusammenstellung ohne DataForSEO-Neurecherche, Vorher-/Nachher-3 READY/Hashkontrolle, Download `mit-suchintent-nachweis`, isolierten K0-Quellenwächter PASS. Erst nach diesem echten Beweis eine Live-Freigabe erwägen.

## Bedienablauf NACH Installation auf getrennter WordPress-TEST-Seite (10.11.2026)

**Nur TEST, keine Neuinstallation von PSERC nötig, wenn die vorhandene 0.28.63 aktiv ist. Kein K0:start und kein Import/Live.**

1. WordPress-Testseite → **SEO Themenengine → Produktion**. Prüfen, dass PSTE **0.57.144.34** aktiv ist. **„Automatik starten / fortsetzen“** einmal anklicken. Diese bestehende Automatik ist der bestandsbasierte Normalweg; sie stößt bei Bedarf den Portalabgleich, die vorhandene Bestandsaufbereitung und die PSERC-Redaktionsplanprüfung an. **Nicht** zusätzlich „Longtails recherchieren“/„Produktionswelle“ mit Providerkosten, „Kurzer Dienstweg“, „Neustart“ oder eine manuelle Datenmigration starten. Ein angezeigter Fehler ist ein Blocker und kein Anlass für wiederholtes Klicken.
2. Nach Abschluss in **SEO Themenengine → SEO Redaktionsplan** die Anzeige kontrollieren: **3 freigegebene Artikel** mit den bisherigen Titeln (Horseware-Regendecken, Fliegen-/Regendecke, Regendecke 0g). Keine weitere Neuaufbereitung starten, solange READY angezeigt wird. Wenn dort ein veralteter Snapshot steht, die vorhandene Funktion **„Snapshot nach der Produktionswelle aktualisieren“** genau einmal nach abgeschlossener Automatik verwenden; nur wenn die Planquelle aktuell ist.
3. Im **SEO Redaktionsplan** auf **„Produktionsübergabe herunterladen“** klicken (nicht auf den zusätzlichen älteren PSTE-Download). Erwarteter Dateiname: **`seo-redaktionsplan-mit-suchintent-nachweis-....json`**. Diese Datei hier hochladen, damit das echte Profil und die K0-Quellenbindung geprüft werden können. Wenn **`ohne-suchintent-nachweis`** oder ein Fehlercode erscheint, **nicht an K0 weitergeben**, sondern die Datei bzw. den exakten Fehler hier bereitstellen; keinen weiteren Blindlauf durchführen.

**Präzise Grenze:** Lokale Tests beweisen die Quellcodekorrektur, NICHT die tatsächliche Bestandswiederverarbeitung oder den Export auf dieser WordPress-Testinstallation. Die Automatik kann bei geänderter gespeicherter Abhängigkeit eine vorhandene Bestandsprüfung wiederaufnehmen; kein pauschales Versprechen über ihre Dauer oder Anzahl. Der echte WP-Test soll genau das nachweisen. Nach erfolgtem Schritt 1 keine zweite Automatik auslösen.


## Reale erneute WordPress-Datei nach Installation hochgeladen – Abnahme FEHLGESCHLAGEN

**Neuer echter Benutzer-Export:** `seo-redaktionsplan-ohne-suchintent-nachweis-42619ca7... (2).json`. Bytevergleich mit dem vorherigen vollständigen Export `(1).json`: **identisch 90.640/90.640 Bytes, SHA256 `29638fef9606925b5b6f322fcde695581999ec0c41bd111bca0bcb655fbf1220`**. In beiden: `created_at_utc=2026-11-10T15:47:48+00:00`, `compiler_version=0.28.61`, `bindings.seo_version=0.57.144.32`, identische 3 Planplätze und `manifest_sha256=89d2c9...`.

**Alle 3 `items[*].intent_profile.phase=PRE_TYPE`; alle 3 `search_intent` und `profile_sha256` FEHLEN.** Es wurde **kein neuer PSERC-Produktions-Snapshot erzeugt**, der die aktualisierte PSTE-Normalweglogik enthält. Dies beweist **nicht**, ob PSTE .34 korrekt installiert/aktiv ist: die Angaben im Export stammen vom alten Snapshot und sind keine Live-Plugin-Versionsmessung.

**Zusätzliche Codeursache, Original-Quellen 0.57.144.34 und 0.28.63 hart gelesen:**
- PSTE `productionAutoStepAjax` prüft bestehende `existingOnlyAuditCurrent()` und `PSERC_Plan_Dependency_Fingerprint::isCurrent()`; wenn beide noch wahr sind, wird der alte Redaktionsplan unmittelbar wiederverwendet, ohne `PSTE_Normal_Metadata_Path::applyToPayload` für die alten 3 READY-Quellen nochmals auszuführen.
- PSERC `PSERC_Plan_Compile_Job::start` hat denselben **„active snapshot still current ⇒ return existing snapshot“**-Kurzschluss.
- PSERC `PSERC_Plan_Dependency_Fingerprint::current` bindet bewusst **nicht an den rohen PSTE-Pluginversionsstring**; die Topic-Watermarks sind MAX(id) bestehender Tabellen. Ein reines Plugin-Upgrade von .32→.34 ohne tatsächliche Quellzeilen-Reentry invalidiert die alte PRE_TYPE-Projektion **nicht automatisch**.
- `PSTE_Repository::compilerPlanningTopicPage` liest gespeichertes `payload_json` unverändert aus dem bestehenden Pool; PSERC `PSERC_SEO_Reader` übernimmt das enthaltene PRE_TYPE-Profil entsprechend unverändert. Reines erneutes Ausgeben oder Anklicken von „Snapshot aktualisieren“ **kann daher denselben Stand liefern**.

**Korrektur der vorherigen Bedienungsanweisung:** Der Hinweis „Automatik starten, anschließend JSON laden“ war als echte Abnahme unzureichend. **Nicht** zu mehrfachen Klicks, erneuter Provider-Recherche, Reset, manuellem SEO-Profil-Erfinden oder K0-Start auffordern. Vor einer weiteren Testinstallation muss die bestehende bestandsbasierte Automatik gezielt die bereits READY-3-Zeilen (mit unveränderten Quell-/Titel-/Kategorie-/Planplatzdaten) über den EINMALIGEN existierenden PSTE-`bindArticleType`-Pfad neu binden, mit schreibsicherer Persistenz/Readback, und dadurch den bestehenden PSERC-Plan gezielt invalidieren/neu bilden. Lokale Regression mit dem exakten alten Snapshot, idempotenter Neuprüfung, Source-Drift-/Dubletten-/Sicherheits-Negativfällen, ohne 5.016er Blindscan und ohne Providerkosten. Keine Behauptung, dieser Anschluss sei schon implementiert.

**Neuer Stand:** `LOCAL_BINDER_LOGIC_QA_PASS`, aber `REAL_WORDPRESS_UPDATED_HANDOFF=FAIL_OLD_SNAPSHOT`; `CACHED_PLAN_INVALIDATION_GAP_CONFIRMED_IN_SOURCE`, `PRODUCTION_RELEASE=BLOCKED`. K0-Produktionszweig weiterhin unangetastet.
