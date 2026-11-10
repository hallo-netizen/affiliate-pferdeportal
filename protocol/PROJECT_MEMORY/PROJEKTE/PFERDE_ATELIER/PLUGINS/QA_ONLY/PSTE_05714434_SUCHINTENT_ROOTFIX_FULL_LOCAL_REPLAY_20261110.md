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
