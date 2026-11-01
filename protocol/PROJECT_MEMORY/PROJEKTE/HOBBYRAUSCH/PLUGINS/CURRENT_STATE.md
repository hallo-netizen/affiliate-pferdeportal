# HOBBYRAUSCH – PLUGINS – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-11-01
STATUS: AKTIV / HD-003 1.50.786 LIBRARY-VOLLZIP-READBACK PASS / ISOLIERTE GITHUB-CURRENT.ZIP NOCH OFFEN

## Regel

Für jedes einzelne Plugin gilt ausschließlich dessen Plugin-Akte als aktuelle technische Wahrheit.

## HD-001 – Kategorie-Workflow

Plugin-Wahrheit:
`PLUGIN_AKTEN/HD-001-KATEGORIE-WORKFLOW/CURRENT.md`

Rolle:
schwerer Bearbeitungs-/Dry-Run-/Sync-/Rollback-Workflow; künftig nicht zwingend dauerhaft aktiv.

## HD-002 – Text/SEO

Plugin-Wahrheit:
`PLUGIN_AKTEN/HD-002-TEXT-SEO/CURRENT.md`

Vor späterem Liveeinsatz muss eine direkte HD-001-Runtime-Abhängigkeit auf den neutralen Kategorie-Registry-Vertrag geprüft/umgestellt werden.

## HD-003 – Design

Plugin-Wahrheit:
`PLUGIN_AKTEN/HD-003-DESIGN-TEMPLATE-KIT/CURRENT.md`

Fach-Current:
`../DESIGN/CURRENT_STATE.md`

## HD-004 – Kategorie-Kern

Plugin-Wahrheit:
`PLUGIN_AKTEN/HD-004-KATEGORIE-KERN/CURRENT.md`

Rolle:
schlanker read-only Normalbetriebs-Kern für `journal_cat` + zentrales Kategorie-Snapshot-API.

Fach-Current:
`../SEO_KATEGORIEN/CURRENT_STATE.md`

## HD-005 – Glossar Core

Plugin-Wahrheit:
`PLUGIN_AKTEN/HD-005-GLOSSAR-CORE/CURRENT.md`

Fach-Current:
`../GLOSSAR/CURRENT_STATE.md`

## HD-006 – Bildzentrale

Plugin-Wahrheit:
`PLUGIN_AKTEN/HD-006-BILDZENTRALE/CURRENT.md`

Fach-Current:
`../BILD/CURRENT_STATE.md`

## HD-007 – Hobbyregister Core

Plugin-Wahrheit:
`PLUGIN_AKTEN/HD-007-HOBBYREGISTER-CORE/CURRENT.md`

Rolle:
schlanker read-only Laufzeitkern für das zentrale Hobbyregister und die Hobbyfinder-Lese-API; keine zweite fachliche Datenhaltung.

Fach-Current:
`../WISSENSDATENBANK/CURRENT_STATE.md`

## HD-008 – SEO-Metadaten

Plugin-Wahrheit:
`PLUGIN_AKTEN/HD-008-SEO-METADATEN/CURRENT.md`

Rolle:
schlanke automatische SEO-Titel-/Meta-Description-Ausgabe.

Fach-Current:
`../SEO/CURRENT_STATE.md`

## HD-009 – Affiliate-Zentrale

Plugin-Wahrheit:
`PLUGIN_AKTEN/HD-009-AFFILIATE-ZENTRALE/CURRENT.md`

Rolle:
bereinigte Hobby-Depot-Portierung der Affiliate-Zentrale; technische Arbeitsquelle branchgebunden, keine Pferdeatelier-Statusübernahme.

Fach-Current:
`../AFFILIATE/CURRENT_STATE.md`


## Nachholprüfung vom 01.11.2026

Die technisch gültigen Einzelstände bleiben ausschließlich in `PLUGIN_AKTEN/<PLUGIN-ID>/CURRENT.md`. Der konkrete Nachholnachweis steht in `EVIDENCE_PLUGINABLAGE_20261101.md` und ist **keine zweite Current-Autorität**.

**Gesamtablage: BLOCKED.** In den geprüften `ISOLIERTE_PLUGINS`-Ordnern ist nur für HD-009 ein `CURRENT.zip` nachweisbar. Für HD-001, HD-003, HD-004, HD-005, HD-006, HD-007 und HD-008 (SEO-Metadaten) fehlen dort die vollständigen ZIP-Dateien; HD-002 besitzt am geprüften Zielort noch keinen isolierten Ordner. HD-008 Anzeigenfüller besitzt eine zusätzliche Akte mit ungeklärter ID-Kollision.

Bei HD-003 existiert ein Library-Dateieintrag zur **1.50.785**, jedoch konnte dessen ZIP-Inhalt am 01.11.2026 nicht erneut ausgelesen werden. **Keine Beförderung des ungeprüften ZIPs zu Campus-CURRENT, kein Live-PASS.**

## Live-Inventarfrischecheck 01.11.2026

Die vollständig übermittelte WordPress-Pluginliste weist **15 aktive Plugins** aus. Zuständiger Betriebsstand: `../WORDPRESS_TECHNIK/CURRENT_STATE.md` (eine WordPress-Current); Nachweis: `EVIDENCE_WP_PLUGINLISTE_20261101.md`.

Besonders wichtig: HD-003 **1.50.783 aktiv** (1.50.785 nur unbestätigter ZIP-Kandidat), HD-001 **1.14.17 aktiv** (1.14.16 nur älterer Testkandidat), HD-009 **0.1.7-dev aktiv** (0.1.2-dev nur älterer Campus-Installer). Der FAQ Frontend Fix 1.0.2 und die Performance Diagnose 1.1.0 waren im Register noch nicht verzeichnet und sind als noch nicht gebundene Eigenplugins aufgenommen. **Keine alten Versionen überinstallieren.**

PLUGINABLAGE bleibt BLOCKED, da keine unabhängigen ZIP-/Rohdatei-Readbacks vorliegen. Die Listenaufnahme ist kein Live-Funktions-PASS.
## Neuer HD-003-Readback 01.11.2026

Die frühere Behauptung, der 1.50.785-Inhalt lasse sich nicht abrufen, ist **überholt**: der vorhandene Library-Dateieintrag wurde über die autorisierte Plugin-Büro-Ablage kopiert, danach ließ sich die vollständige echte 1.50.785 unabhängig öffnen. Auch die aktive Betreiber-ZIP 1.50.783 wurde auf demselben Weg gelesen und verglichen. Die neuen freigegebenen Änderungen wurden als **1.50.786 Vollplugin** umgesetzt und gegen die 1.50.785 geprüft.

**Neue 1.50.786-ZIP inkl. Favicon und Anzeigenmarkt-Banner** liegt im bestehenden Library-Pluginbüro und als getrennte Rückfallkopie vor, beide nach Upload frisch geöffnet und hash-identisch geprüft. Der unveränderte Pluginroot ist `affiliate-portal-template-kit`; 1.281 Einträge, davon 1.271 byte-identisch zu 1.50.785; PHP 11/11 PASS, simulierte Markt-Positiv-/Negativprüfungen PASS. **GitHub `ISOLIERTE_PLUGINS/HD-003-DESIGN-TEMPLATE-KIT/CURRENT.zip` weiterhin nicht synchronisiert.** Kein WP-Live-PASS; laut Betreiber bleibt 1.50.783 installiert. Die genaue technische Wahrheit/Byte-Nachweise und Installationsdatei stehen nur in `PLUGIN_AKTEN/HD-003-DESIGN-TEMPLATE-KIT/CURRENT.md` und dem zugehörigen MANIFEST.

## EXAKT EINE NEXT ACTION

**HD-003 1.50.786-ZIP über die tatsächlich installierte 1.50.783 einspielen und live sowohl Favicon als auch Anzeigenmarkt-Banner zwischen Suche und Kategorie-Kacheln prüfen.** Andere Plugins und Portalbereiche unangetastet. GitHub-Isolations-ZIP bleibt als separater Speicher-Abgleich offen.
