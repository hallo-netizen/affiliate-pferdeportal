# Texterstellung Universal 0.5.2-dev.1 – Arbeitsprotokoll (18.11.2026)

**Status: nicht installationsfreigegeben. Gemäß Benutzeranweisung keine QA-ZIPs, Protokolle oder Quellarchive im Chat als Download.**

## Ausgangslage
- Gemeinsamer, lokal geprüfter Hab-/Universal-Quellstand 0.5.1-dev.1; beide Archivkopien im jeweiligen Library-Büro vorhanden.
- Nur der Kategorienleser und die einmalige MINI-Entscheidungsstelle waren zuvor portalfrei. Der originale PSTE-Recherchepfad ist weiter inaktiv, weil er Artikelart und Kategorie aus alten Namensmustern verknüpft. Kein echter K0/WordPress/DataForSEO-End-to-End-Test.

## Dieser Arbeitsvorgang – konkrete Änderungen
1. `includes/class-txe-universal-research-input.php` neu: Ein read-only Adapter baut aus dem **aktuellen bestätigten** WordPress-Kategoriesnapshot reproduzierbare Recherche-Ausgangspunkte. Er kennt die eigene WordPress-Term-ID, Term-Slug, Hab-R3-Besitzerbindung, aktive Revision und anfangs **keine** Artikelart/SEO-Freigabe. Maximal 40 Kategorien pro Vorbereitung; keine Kosten.
2. `includes/class-txe-k0-registry-check.php` neu: K0-Register nur analysieren, nicht ändern. Prüft registriertes Portal, eindeutige Zuordnung aller Slugs, Kollisionen, nicht aufgelöste Git-Kategoriequellen und fehlende Artikelarten. Ein rein lokaler Registerabgleich kann `production_ready` **nie** setzen.
3. `texterstellung.php`: beide Adapter eingebunden; Original-PSTE-Produktion bleibt inaktiv; keine neuen Cronjobs oder kostenpflichtigen Provideraufrufe.
4. `includes/class-txe-universal-portal.php`: Setup zeigt die kostenlose Vorbereitung der aktuellen Recherche-Eingaben, ohne je SEO- oder Artikelart-Entscheide vorwegzunehmen.
5. `INSTALLATION_UND_PRUEFUNG.txt` + `README-TESTINSTALLATION.txt`: irreführende alte 0.4.24-Installationshinweise beseitigt; beide kennzeichnen 0.5.2 ausdrücklich als **NICHT INSTALLIEREN**.
6. `tests/test_shared.php`: Ergänzt Original-PSERC-Metadatenprüfung (fünf Felder), Negative für zusätzlichen K0-Portalparameter, Artikelinhalt und automatische Veröffentlichung, plus K0-Register-Mismatches; dieselben Tests für Hab und Universal.
7. `tests/archived_k0_main_registry_20261118.json`: exakte historisch gelesene K0-Quellregister-Struktur als ausdrücklich NICHT autoritativer Laufzeit-Testwert. Profile `hobby`, `pferdeatelier`, noch **kein** Hab/Robotik/Wasser. Aktuelle externe Laufzeit nicht dadurch bewiesen.

## Prüfungen und konkrete Freigabegates
- Zwei vollständige ZIPs aus gemeinsamer Quelle; je **93 Dateien, 82 PHP und 9 JSON**, vollständiger PHP-Lint, JSON-Parser und ZIP-CRC bestanden.
- Ausgeführte lokale WordPress- und K0-Mocktests: **Hab 62/62**, **Universal 51/51**, einschließlich Original-PSERC-Metadatenprüfer mit gültigem und mutiertem Fünffeldpaket.
- Quellvergleich zwischen den Varianten: nur `portal-distribution.json` und der Name in `texterstellung.php` unterscheiden sich.
- Hab ZIP SHA256 `ade5b3524977def0a43a082cddfbcd1f67bf86a3e61b51f34c1b74fca0ad350d`.
- Universal ZIP SHA256 `d88e45a39f629161b804fe3b751c9cef1c406fab6e999c29420707fc14bd1887`.
- Gemeinsame Quelle inkl. Tests SHA256 `a815f753f614168d91f80c07a62025fb455dd9a5c8ec6cb50790c4e325676739`.
- Original-Pferdeatelier und K0 nicht verändert. Kein echter WordPress-/DataForSEO-/K0-Schreibvorgang. `productionReady()` bleibt `false`.

## Tatsächlich abgeschlossene Archivierung
- Hab Büro: `/hab-und-bewahr/TEXTERSTELLUNG/UNIVERSAL_ENTWICKLUNG_20261118/V052/` enthält Hab-Plugin-ZIP, gemeinsame Quelle samt Tests, Prüfbericht JSON und ausführliches Protokoll.
- Universal Büro: `/texterstellung-universal/ENTWICKLUNG_20261118/V052/` enthält Blanko-ZIP, dieselbe gemeinsame Quelle/Tests und die Berichte.
- Alle acht Upload-Operationen in die Library mit `succeeded` bestätigt.

## Offen – keine falsche Fertigmeldung
- Neutralisierung des eigentlichen DataForSEO-Ausführungswegs und Original-SEO-Qualitätsprüfungen; bis jetzt ist nur der **Eingang** fertig, nicht der komplette Rechercheablauf.
- K0-Laufzeitregister muss Hab/Robotik/Wasser in der tatsächlich aktiven Fassung eindeutig zuordnen. Das überprüfte Archivregister hat nur Hobby/Pferdeatelier. Der Unterschied K0 4 vs. lokale 5 Artikelarten ist weiterhin nicht produktiv aufgelöst.
- WordPress-Liveabnahme auf einem echten Hab-Testportal, danach vollständiger K0-Hin-/Rücklauf mit einem Entwurfsartikel. Erst nach dieser Testkette: installationsfreigegebene ZIPs für Hab und Universal.
- Keine Benutzerinstallation oder DataForSEO-Ausgabe erforderlich, bevor ein korrekt geprüfter Release bereitsteht.

**Ausgaberegel unverändert:** Nur echte installationsfreigegebene WordPress-Plugin-ZIPs als Chat-Download. Entwicklungs- und Testdateien bleiben ausschließlich im Büro.