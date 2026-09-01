# AFFILIATE-ZENTRALE V6.64.0 — Repository-native Implementierungsauftrag BANNERAUTOMATION

Stand: 2026-09-01
Repository: `hallo-netizen/affiliate-pferdeportal`
Branch-Autorität: `affiliate-release-current`
Workstream: `AFFILIATE_ZENTRALE`
Status: `READY_FOR_REPOSITORY_NATIVE_IMPLEMENTATION`

## Pflichtstart

Arbeite ausschließlich repository-nativ. Keine Uploads, ZIPs, Base64-Patches, Parallelbranch oder neue Pluginarchitektur.

Lies zuerst vollständig:

1. `control/release-governance/CURRENT_RELEASE.json`
2. `protocol/AFFILIATE_RELEASE_MASTER_CURRENT.md`
3. `protocol/AFFILIATE_RELEASE_ERROR_REGISTER.md`
4. `protocol/AFFILIATE_RELEASE_BANNER_AUTOMATION_TARGET_CONTRACT_20260901.md`
5. die dort bezeichnete aktuelle kanonische Source.

Führe vor jeder technischen Änderung den im Fehlerregister verlangten `ERROR-REGISTER PRECHECK` aus. Relevante Fehler-IDs für den Gesamtblock: `AFF-ERR-001`, `002`, `003`, `004`, `005`, `006`, `008`, `009`, `010`.

## Einziger Auftrag

Implementiere den Zielvertrag `protocol/AFFILIATE_RELEASE_BANNER_AUTOMATION_TARGET_CONTRACT_20260901.md` **vollständig als einen gebündelten Root-Cause-Block** in der bestehenden Architektur.

Nicht in Einzelprobleme zerlegen und nicht nach dem ersten positiven Teilergebnis stoppen.

## Vor Codeänderung zwingend lokal im Repo prüfen

1. vorhandene many-to-many Target-Edge-Logik und Output-Object-Key-Semantik,
2. aktuelle Campaign-Zielauflösung und tatsächliche Frontend-/Campaign-Unterstützung für Seiten/Kategorien/Beiträge,
3. vorhandene Design-/Slot-Schnittstellen und Filter,
4. zentrale Automation-Dispatch-/Job-/Recheck-Mechanik,
5. DS24-Bulk-/Marketplace-/Affiliation-/Vendor-Creative-Pfade,
6. bestehende Two-Phase-/LKG-/Persistenzlogik,
7. Backend-Readback des zentralen Laufs.

Bestehende geeignete Mechanismen wiederverwenden. Keine zweite Tabelle/Queue/Zuordnungsarchitektur erfinden, wenn der bestehende Vertrag erweiterbar ist.

## Harte Implementierungsanforderungen

- DS24: mehrere bestätigte Partner zentral synchronisieren; Einzelpflege nur Fallback.
- Nur reale Banner; DS24 bleibt Banner-only.
- Seiten + Kategorien + veröffentlichte Beiträge als reale Bannerziele unterstützen, soweit die bestehende Campaign-Ausgabe sie technisch sicher rendern kann. Falls ein bestehender Renderer einen Zieltyp noch nicht unterstützt, ausschließlich den bestehenden zentralen Renderer erweitern; keine Provider-Sonderausgabe.
- Mehrfachnutzung: ein Banner darf mehrere jeweils eigenständig sichere Ziele/Slots erhalten; Deduplizierung auf Creative + Portal + Ziel + Slot.
- Semantik: spezifische Fachnähe vor generischen Pferdebegriffen/Pfadtiefe; breiter Pferde-Fallback nur bei belegter Pferderelevanz und ohne fachfremdes Ziel.
- Slotdefinitionen providerunabhängig und austauschbar; keine DS24-/Awin-Größen oder Positionen im Provideradapter.
- Design-/Slotänderungen müssen ohne Providercodeänderung wirksam werden.
- Kein Verzerren eines unpassenden Banners; ungeeignetes Format bleibt für spätere Neubewertung erhalten.
- Re-entrant: neue/geänderte Banner, Seiten, Kategorien, Beiträge und Slots werden im zentralen Workflow erneut bewertet; kein Provider-Cron.
- Draft → vollständiger Provider-/Zentralgate → persistiert published → erst danach Supersede/LKG-Ablösung.
- Persistenzfehler = Rollback, LKG bleibt.
- Zentraler Backend-Readback muss den gespeicherten Endzustand des Laufs zeigen.

## Scope

Primär innerhalb:

- `release/affiliate-zentrale/current/affiliate-portal-router/includes/trait-ppar-output-objects.php`
- `release/affiliate-zentrale/current/affiliate-portal-router/includes/trait-ppar-automation-suite.php`
- `release/affiliate-zentrale/current/affiliate-portal-router/includes/trait-ppar-digistore24.php`
- `release/affiliate-zentrale/current/affiliate-portal-router/includes/trait-ppar-creative-library.php` nur wenn zwingend nötig
- `release/affiliate-zentrale/current/affiliate-portal-router/pferdeportal-affiliate-router.php` nur wenn zwingend nötig

Weitere kanonische Current-Source-Dateien nur bei belegter unmittelbarer Notwendigkeit.

Nicht ändern: eBay-Run/Source, idealo-Semantik, Archive, `.github/workflows/**`, immutable Guards/Tests, neue Pluginversion nur wegen Folgefehler, neue Scheduler/Worker/Queues.

## Pflichtprüfung

Die vollständigen POSITIV-/NEGATIV-/Regressionstests aus dem Zielvertrag sind bindend. Zusätzlich:

- PHP-Lint für jede geänderte PHP-Datei,
- `git diff --check`,
- Tests mit realistischen Rohdaten, einschließlich der bekannten Klassifikationsproblemfälle,
- Provider-Regression eBay/idealo/Awin ohne erneutes Ausführen bereits hash-identisch bestandener historischer eBay-Gates,
- `ERROR-REGISTER POSTCHECK`.

Kein `PASS` aus Teiltests.

## Fehler während der Umsetzung

Wird ein neuer, bisher nicht registrierter Fehler gefunden:

1. **vor dem Fix** neue `AFF-ERR-...`-ID in `protocol/AFFILIATE_RELEASE_ERROR_REGISTER.md` anlegen,
2. Root Cause, gescheiterten Weg, Nicht-Wiederholungsregel, POSITIV-/NEGATIV-/Regressionstest dokumentieren,
3. erst dann Root-Cause-Fix fortsetzen.

Bekannter Fehlerweg erneut getroffen = Gate `FAIL`, nicht kaschieren.

## Source-Binding nach lokalem Gesamt-PASS

Erst nach vollständiger lokaler Evidence:

1. kanonische Current-Source hashen,
2. `release/affiliate-zentrale/CURRENT_SOURCE_SHA256.txt` exakt aktualisieren,
3. Manifest-SHA berechnen,
4. ausschließlich notwendige aktuelle Manifest-Bindungen in `control/release-governance/CURRENT_RELEASE.json` aktualisieren,
5. `active_candidate.version=6.64.0`, `status=WORKING`, `release_allowed=false` beibehalten,
6. historischen PASS nicht umetikettieren,
7. kein finales Installer-ZIP erzeugen.

## Abschlussausgabe

Nur nach vollständigem lokalem Gesamtworkflow-Test berichten:

- geänderte Pfade,
- Root Cause(s),
- ERROR-REGISTER PRECHECK/POSTCHECK,
- exakte POSITIV-/NEGATIV-/Regressionsergebnisse,
- Source-Hashes und Manifest-SHA,
- Governance-Bindungsstatus,
- `release_allowed=false`,
- klar: realer WordPress/MariaDB-/Provider-Live-Nachweis weiterhin offen, sofern er nicht tatsächlich ausgeführt wurde.
