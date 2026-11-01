# HOBBYRAUSCH – PLUGINS – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-11-01
STATUS: **HD-003 1.50.794 VOM BETREIBER FREIGEGEBEN / GITHUB-PLUGINBÜRO-METADATEN AKTUALISIERT / ZIP-BINÄRDATEI FEHLT**

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

## HD-003 Stand 01.11.2026

## 01.11.2026 – HD-003 1.50.789: Suchergebnisse kompakt + Artikel-Hero

**NEUER INSTALLATIONSKANDIDAT: Version 1.50.789.** Vollständiges Plugin im aktuellen Chat unter `HOBBY_DEPOT_HD003_1.50.789_SUCHERGEBNISSE_ARTIKELHERO_VOLLPLUGIN.zip`, lokaler ZIP-Readback 1285/1285 PASS; 13/13 PHP-Lint PASS; vorheriger 1.50.788-Voll-ZIP-Vergleich: **1280 Einträge unverändert, 3 geänderte PHP-Dateien, 2 zusätzliche PHP/Text-Dateien**, Original-Headerlogo und Originalfavicon byte-identisch. SHA-256 **b89784c8ba9296e5f8faf771f2a258565839da7896d5a55f4b4b03019b460b79**; 63.815.168 Bytes.

**Kritische UI-Korrektur 1: Suchergebnisseite.** Einzige bestehende Hauptsuche bleibt zuständig; kein neuer Index, kein zweiter AJAX-Endpunkt. Pro Bereich zunächst fünf Treffer. Jeder Klick auf „Mehr anzeigen“ legt fünf weitere der maximal 50 bestehenden Treffer frei; Button verschwindet nach letztem Treffer. Ruhige zweispaltige Karteikartenansicht mit Trefferzahl; fünf Bereiche Hobbys, Fachwissen, Magazin, Glossar, Anzeigen erhalten. Detail: `includes/class-hobby-depot-profile-v150709.php`, bestehendes `templates/hobby-depot-search-v150732.php`.

**Kritische UI-Korrektur 2: Artikel oben.** Breadcrumb → genau ein H1-Titel oberhalb → breitflächiges Foto-Hero → Artikeltext. Das Hero wird aus dem vorhandenen WordPress-Beitragsbild (Priorität) oder erstem echten Inhaltsbild gespeist und vermiedene Bildduplikate verborgen. Text ist *niemals* ins Foto eingebrannt: links heller automatischer Farbverlauf, links grüner, kurzer Claim plus weicher verwischter Bogen, Fotomotiv möglichst rechts. Kein Pseudofoto bei fehlendem Bild. Textlieferung kann das EINZIGE Beitragsmetafeld `_hd_article_hero_claim` setzen; ohne Feld wird ein kurzer Auszug verwendet. Regeln für spätere Bildzentrale/Texterstellung stehen **im Plugin** unter `ARTIKELBILD_REGELN_150789.txt`: Motiv rechts, links ruhiger Hintergrund, kein Text im Bild. Die Datei ist eine Regelvorgabe und **keine bereits technisch implementierte Änderung am separaten Bildzentrale-Generator**. Nur der Hobby-Depot-Zweig verwendet die neue Hero-Vorlage, nicht Pferdeatelier oder andere Designprofile. Gespeicherter veröffentlichter Artikel wird nicht verändert, seine Tabellen, Werbebanner, Listen und Produktbereiche bleiben erhalten. Der Legacy-Pferde-Artikelheader-Umordner wird für Hobby Depot übersprungen.

**Positiv-/Negativprüfung lokal:** realer Suchgruppen-Code vom Vorrelease gegen Fachartikel, Fachkategorien, CORE-Seiten, Entwurf, Magazin-Dopplung und Nulltreffer erneut PASS. Neue Suchergebnisse: 12 Treffer → nur 5 sichtbar, 7 verborgen, exakt ein aktivierbarer Mehr-Button; 3 Treffer → kein Button; Nulltreffer; Freigabelogik PASS. Header: erstes Inhaltsfoto, neues Beitragsbild, Claim aus Meta, generischer Fallback ohne Foto, genau ein H1 und ein Hero, Überschrift oberhalb, sonst keine Änderung des bestehenden Inhalts PASS. Alle 13 PHP-Dateien fehlerfrei. **Kein WordPress-Livebrowser-Readback für 1.50.789.**

**Speicherung:** Die ChatGPT-Library hat zuletzt beim Versuch, 1.50.788 als Voll-ZIP zu speichern, das Speicherlimit gemeldet. Für 1.50.789 liegt deshalb **keine neu bestätigte dauerhafte Library-/GitHub-Original-ZIP vor**. Das tatsächlich erzeugte und überprüfte vollständige ZIP ist nur als downloadbarer Anhang im aktuellen Chat gesichert; ältere 1.50.787-Rückfallkopie bleibt erhalten. Diese GitHub-Metadaten ersetzen nie ZIP-Bytes.

**NEXT ACTION:** Vollständiges HD-003 1.50.789 im WordPress-Backend über die vorhandene Designplugin-Installation aktualisieren, danach Suchseite „Zweileiner“ und veröffentlichten Testbeitrag am Desktop/Mobil visuell abnehmen. Erst danach Betreiber-Live-PASS.

## EXAKT EINE NEXT ACTION

**1.50.789 Voll-ZIP aus aktuellem Chat in die vorhandene WordPress-HD-003-Installation laden, dann die Suchergebnisseite und den Hero des veröffentlichten Testartikels live ansehen.** Keine zweite Plugin-Installation.

## 2026-11-01 – HD-003 Vollplugin 1.50.790: Eigenwerbung auf direkt vermietbaren Bannerplätzen

**Quelle:** echte 1.50.789-Voll-ZIP aus dem aktuellen Pluginstand. Daraus **1.50.790 Voll-ZIP** erstellt, Pluginroot `affiliate-portal-template-kit/` unverändert. Ausgabe im aktuellen Chat: `HOBBY_DEPOT_HD003_1.50.790_EIGENWERBEBANNER_ORIGINALLOGO_VOLLPLUGIN.zip`.

**Genau der beauftragte Umfang:** nur der bestehende `rental_slot($placement)`-Pfad des Designprofils Hobby Depot für *noch nicht gebuchte* direkt vermietbare Werbeflächen, inklusive responsive CSS. Freier Platz zeigt neues Eigenwerbemotiv Modellflugzeug/Werkstatt mit beigem Übergang, originalem aus dem aktiven Plugin geschnittenen Logo ohne Unterzeile, Überschrift „Hier könnte Ihre Werbung stehen“, exakt zwei voneinander unabhängigen HTML-Links „Werbebedingungen“ und „Preise“. Keine weitere Unterzeile, kein grelles Grün. Kein nachgezeichnetes Logo. Die Links werden nur mittels `get_page_by_path` und `get_permalink` aus echten veröffentlichten WP-Seiten aufgelöst: Bedingungen bevorzugt `werbebedingungen`/`werb-anzeigebedingungen` inkl. bekannter Varianten; Preise `preise`. Fehlt eine Zielseite, zeigt der Button seinen deaktivierten Zustand ohne erfundenes Linkziel; der echte WordPress-Pages-Readback ist noch offen.

**Harte Abgrenzung:** Bei aktiv gebuchtem Mietslot mit echter Kundenbild-URL/Ziel-URL bleibt das bisherige Kundenbanner völlig unverändert, ebenso der Provider-Filter `pftk_hobby_rental_slot_html`. Die bereits vorhandene zentrale Einmal-Regel `render_rental_for` bleibt erhalten (maximal ein Mietbanner pro Seite). Kein zweiter Werbebanner-Worker, keine Änderung der Affiliate/Partner-Slots, keine Änderung des Pferdeatelier-Zweiges, von Kategorien, Hero oder Suchfunktion.

**Veränderte Dateien im Vollplugin:** exakt zwei PHP-Dateien (Hauptplugin nur Version, Hobby-Profil Version + Austausch der freien Mietbanner-HTML und Ergänzung ausschließlich dazugehöriger CSS) und zwei neue Assets unter `assets/hobby-depot-v150617/eigenwerbung-v150790/`: `logo-original-ohne-unterzeile.png` als unveränderte Original-Pixel des 640×372-Logos, nur auf 640×315 beschnitten; `modellflugzeug-werkstatt.webp` als Ausschnitt aus dem vom Betreiber freigegebenen Modellflugzeug-Banner, ohne eingebrannte Buttons/Schrift. **1283/1285 alte Originaldateien byteidentisch**, neue ZIP enthält **1287/1287** korrekt lesbare Einträge.

**Simulation/QA:** PHP 13/13 Syntax PASS, ZIP CRC 1287/1287 PASS; Privatmethode `rental_slot` anhand des echten Codes mit WordPress-Stub ausgeführt: freie Fläche hat zwei voneinander verschiedene richtige Links, reservierter Platz verwendet Kundenwerbung statt Eigenbanner, Provider-Override unverändert, fehlende Werbebedingungsseite erzeugt keinen falschen Link, doppelte Mietbannerdarstellung wird blockiert – alles PASS. Visualisierung mittels tatsächlichem gerendertem PHP-/CSS-HTML in Chromium bei Desktop 1200px und Mobil 390px; beide Links vorhanden, kein Überlauf. Vorschauen im aktuellen Chat: `HOBBY_DEPOT_WERBEBANNER_1.50.790_VORSCHAU_1200px.png` und `..._390px.png`.

**ZIP-Readback:** SHA-256 `39953565ba8e9d81e5630255f54cee04fe150c54b68b78ad9c5a8ef639dbe9db`; 64.035.283 Bytes. **Kein echter WordPress-Live-PASS**. Die zuletzt bekannte ChatGPT-Library hat Speicherlimit signalisiert; dort ist 1.50.790 nicht als gespeichert verifiziert. Das dokumentierte GitHub-Campus-Protokoll ist **nicht** das Binär-ZIP. Frühere 1.50.789-ZIP und 1.50.787-Library-Backup bleiben erhalten.

**EXAKT NÄCHSTER SCHRITT:** 1.50.790 als *Update des vorhandenen HD-003* installieren; auf einer noch freien mietbaren Werbefläche beide Buttons im echten WordPress-Frontend überprüfen (Ziel-URL, Erreichbarkeit) und eine gebuchte Fläche auf unveränderte Kundenwerbung prüfen. Keine weiteren Pluginänderungen vorher.

## Stand HD-003 1.50.794 (01.11.2026)

Betreiber hat 1.50.794 abgenommen. ZIP lokal vollständig als 65.700.802 Bytes/1290 Dateien geprüft. **GitHub-Binärablage kann durch die zur Verfügung stehenden Aktionen noch nicht durchgeführt werden.** Daher werden trotz hinterlegter Prüfakte **kein Vollzugriff oder Github-ZIP-PASS behauptet**. Ziel-Pfad `ISOLIERTE_PLUGINS/HD-003-DESIGN-TEMPLATE-KIT/CURRENT.zip`; Nachweis `PLUGIN_AKTEN/HD-003-DESIGN-TEMPLATE-KIT/EVIDENCE_1.50.794.md`.
