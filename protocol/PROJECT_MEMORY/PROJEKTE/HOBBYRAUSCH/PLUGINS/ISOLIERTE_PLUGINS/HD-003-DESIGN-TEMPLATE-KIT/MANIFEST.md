# HD-003 – ISOLIERTER PLUGINSTAND – MANIFEST

STAND: 2026-11-01
STATUS: **HD-003 1.50.790 ZUM INSTALLIEREN ALS CHAT-VOLLZIP / GITHUB-CURRENT.zip WEITER OFFEN**

PLUGIN-ID:
`HD-003-DESIGN-TEMPLATE-KIT`

AUTORITATIVE PLUGIN-CURRENT:
`../../PLUGIN_AKTEN/HD-003-DESIGN-TEMPLATE-KIT/CURRENT.md`

AUTORITATIVE FACH-CURRENT:
`../../../DESIGN/CURRENT_STATE.md`

HISTORISCHE CAMPUS-DEKLARATION VOM 24.10.2026 (NICHT WORDPRESS-LIVE):
Version `1.50.744`

In der autoritativen Plugin-Current dokumentiertes Artefakt:
`HOBBY_DEPOT_HD003_CYBERDUCK_1.50.744_ANZEIGENMARKT_STARTSEITE_HARDPASS.zip`

Dokumentierter SHA-256:
`72b048db7516640e19f4432aaf98f5d4fa6ca9cc2fd26964a421e2ac1eece6b8`

CURRENT.zip-SYNC:
**BLOCKED.**

Beim Frischecheck 2026-10-24 waren die exakten 1.50.744-ZIP-Bytes weder im aktuellen Arbeitscontainer noch als Conversation-Artefakt auffindbar. Deshalb wurde `CURRENT.zip` nicht erzeugt oder ersetzt.

HARTE REGEL:
- keine Pointer-/Textdatei als ZIP;
- keine Rekonstruktion auf Verdacht aus 1.50.743;
- `CURRENT.zip` erst nach Wiederherstellung der exakten 1.50.744-Bytes und SHA-/ZIP-/Strukturprüfung synchronisieren.

LETZTER IM ABSCHLUSSCHECK MATERIALISIERTER ZIP-STAND:
`HOBBY_DEPOT_HD003_CYBERDUCK_1.50.743_ANZEIGENMARKT_DESIGN_ENTWURF1.zip`

Dieser 1.50.743-Hinweis ist **keine Current-Wahrheit** und kein Rollforward. Er dokumentiert ausschließlich die Materialisierungsgrenze des Abschlusschecks.

## Nachholcheck 01.11.2026 – keine Campus-Archivierungsbehauptung

- Neuester aufgefundener Dateieintrag: `/hobby rausch/HOBBY_DEPOT_HD003_1.50.785_ORIGINALLOGO_VERIFIZIERT_VOLLPLUGIN.zip` (Library-Metadaten, **63.407.568 Bytes**).
- Vorversion 1.50.784 und 1.50.785-Prüfbericht im selben Ablagebereich ebenfalls gefunden.
- **Kein echter Bytezugriff auf diese ZIP in diesem Prüflauf:** raw-byte materialization verweigert; Textlesen ohne Inhalt. Keine neue Prüfsumme und kein unabhängiger ZIP-/Strukturtest.
- Separate Vorschau `HOBBY_DEPOT_FAVICON_ORIGINAL_VORSCHAU.png` als Bild lesbar; dies beweist **nicht**, dass die ZIP aus dem Campus wiederöffnungsfähig ist.
- Im Campus liegt weiterhin **kein** `ISOLIERTE_PLUGINS/HD-003-DESIGN-TEMPLATE-KIT/CURRENT.zip`.
- Weder 1.50.744 noch die GitHub-dokumentierte 1.50.782 wird als aktuelle Version ausgegeben oder anstelle der gefundenen 1.50.785 installiert.

**Speicherung: BLOCKED. Unabhängiges Wiederöffnen: NICHT BESTANDEN (Zugriffsgrenze). Kein Live-PASS.**

## Betreiber-WordPress-Liste 01.11.2026

**Installiert und aktiv gemeldet: 1.50.783.** **1.50.785** bleibt ein nicht unabhängig wiedergeöffneter Datei-Kandidat. Dieses Manifest enthält weiterhin **keine** gültige CURRENT.zip; die alte 1.50.744 ist historische Deklaration und **nicht** die aktive WordPress-Version. Keine neue Prüfsumme oder ZIP-Datei erfunden. Beleg: `../../EVIDENCE_WP_PLUGINLISTE_20261101.md`. Speicherstatus: BLOCKED.

## Neue aktuelle lokale Voll-ZIP 1.50.786 – Frischeprüfung 01.11.2026

## 01.11.2026 – HD-003 1.50.786: Favicon + Anzeigenmarkt-Banner

**Version in WordPress laut Betreiberliste: 1.50.783 – unverändert.** Neue freigabefähige Installations-ZIP: **1.50.786**, noch nicht auf WordPress installiert; kein Live-Funktions-PASS.

Die neue Voll-ZIP wurde **direkt aus der vollständigen 1.50.785** gebaut. Zusätzlich wurde die vom Betreiber gemeldete 1.50.783 als Rückfallbasis unabhängig geöffnet und mit 1.50.785 abgeglichen. Das freigegebene Original-Favicon wurde aus `hobby_depot_favicon_original_korrigiert_transparent.png` übernommen – **keine Neuzeichnung**. Aus der Originalkomposition wurden PNG-Größen 16/32/48/64/180/192/512 sowie ICO für die vorhandenen Favicon-Dateipfade generiert. Das Headerlogo-Bild ist byte-identisch zur 1.50.785.

**Anzeigenmarkt-Startseite:** bestehende Banner-Ausgabe direkt nach Breadcrumb entfernt und in der ursprünglichen Reihenfolge **Suche → Banner → 8 Kategorie-Kacheln** zwischen Suche und Kategorie-Kacheln verschoben. Gleicher Slot `anzeigenmarkt_top_banner`, keine zweite Engine, keine neue Kategorie- oder Providerlogik. Unterseiten werden weiterhin durch die vorhandene Market-Root-Bedingung ausgeschlossen.

**QA real ausgeführt:** Ausgangs-ZIPs 1.50.783/1.50.785 vollständig geöffnet und ZIP-CRC gelesen; 1.50.783→1.50.785: 8 neue Favicon-Bilddateien und 2 geänderte PHP-Dateien. Ausgabe 1.50.786 vollständig erneut geöffnet: **1.281/1.281** ZIP-Einträge korrekt; **1.271** Einträge gegen 1.50.785 byte-identisch, **10** gezielte Änderungen (8 Favicon-Assets + 2 PHP-Dateien); **11/11 PHP-Syntax PASS**. Markt-Seiten-Positiv/Negativ-Simulation mit der wirklichen Renderfunktion: Hero→Suche→Banner→Kacheln→Anzeigen PASS; Banner genau einmal PASS; 8 Karten PASS; leere Anzeige für Besucher versteckt PASS; eingeloggte Vorschau PASS; Nicht-Markt-Seite PASS; Taxonomie-Unterseite PASS; keine Kategorien PASS. **Kein echter WordPress-Live-Test**.

**Dauerhafte Original-/Sicherungsablage (vollständige Binär-ZIPs):**
- Original 1.50.783: Library `/Hobby Depot/Plugin-Büro/HOBBY_DEPOT_HD003_1.50.783_ORIGINAL_RUECKFALLKOPIE.zip`.
- Original 1.50.785: Library `/Hobby Depot/Plugin-Büro/HOBBY_DEPOT_HD003_1.50.785_ORIGINALLOGO_VERIFIZIERT_VOLLPLUGIN.zip`.
- Neue 1.50.786: Library `/Hobby Depot/Plugin-Büro/HOBBY_DEPOT_HD003_1.50.786_FAVICON_UND_ANZEIGENMARKT_VOLLPLUGIN.zip`.
- Unabhängige Rückfallkopie 1.50.786: Library `/hobby rausch/HOBBY_DEPOT_HD003_1.50.786_FAVICON_UND_ANZEIGENMARKT_RUECKFALLKOPIE.zip`.

**Unabhängige Rückleseprüfung:** Nach dem Upload wurden beide 1.50.786-Library-Kopien über ihren jeweils eigenen neuen File-Eintrag neu materialisiert, als vollständige ZIP geöffnet, 1.281/1.281 Dateien geprüft, Größe, Pluginroot, Hauptdatei und Version geprüft. Beide **63.369.310 Bytes** und SHA-256 `25d8b1ea701139a2cd9b4e4f1cbdcabaa12548f7b2fc2407da8ac44fe58abc3a`. Die beiden gespeicherten Dateien sind byte-identisch zur lokal gebauten ZIP. **Library-Abnahme PASS, GitHub-ISOLIERTE_PLUGINS/CURRENT.zip noch nicht synchronisiert.** Metadaten im GitHub-Campus ersetzen keine ZIP-Bytes.

**NEXT ACTION:** Die fertig geprüfte **1.50.786 Voll-ZIP** in WordPress über die Plugin-Installation mit Ersetzen der installierten **1.50.783** einspielen, danach das Favicon im echten Browser und die Anzeigenmarkt-Seite (Suche→Banner→Kacheln, leere Banner/Unterseiten) prüfen. Keine zweite Installation, keine Änderung an anderen Portalen. Ein tatsächlicher Live-PASS erst nach WordPress-Readback.


## 01.11.2026 – HD-003 1.50.787, Testartikel IN bestehendes Vollplugin integriert

**Abnahme 1.50.786:** Der Betreiber meldet für Favicon und Anzeigenmarkt-Banner „beides pass“. Dies ist Betreiberfeedback, kein von diesem Chat selbst ausgeführter Live-Readback. Die bisher dokumentierte WordPress-Liste mit 1.50.783 ist eine ältere Aufnahme und darf nicht als heutiger Live-Stand ausgegeben werden.

**Neues Full-Plugin 1.50.787:** Basis ist ausschließlich die als echte ZIP erneut geöffnete vollständige 1.50.786. Kein Extra-Plugin, kein zweiter Designweg, keine Veränderung bestehender Kategorie- oder Affiliate-Automatik. Im Hauptplugin Versionswerte aktualisiert und eine einmalige admin_init-Demo-Einbindung ergänzt. Im Hobby-Profil nur Versionswert aktualisiert. Genau zwei Dateien neu im unveränderten Pluginroot:
- `includes/hobby-depot-design-test-v150787.php` (übernommener Testartikel, keine eigenständige Plugin-Kopfdatei)
- `assets/hobby-depot-v150787/lenkdrachen-testfoto.jpg` (gleiches lokales Bild wie in der zuvor getesteten Demo-ZIP).

**Fachlichkeit:** Gezielt aus V7.1-Zielbaum `Sportdrachen → Drachen & Leinen` (Slug `sportdrachen-drachen-leinen`; belegt durch die konkreten Inhalte „Zweileiner und Vierleiner unterscheiden“, „Leinen auswählen“, „Drachen nach Windbereich wählen“). [DESIGNTEST] Zweileiner oder Vierleiner: Gutenberg-Überschriften, Foto, Inhaltsverzeichnis, Liste, Tabelle, Textbanner, drei als Platzhalter gekennzeichnete Produktkarten, nur vorhandene interne Querverweise (sonst interne Sprungmarken) und FAQ. Keine behaupteten aktuellen Partnerpreise.

**Import:** Läuft bei erstem berechtigten Backendaufruf nach Austausch der Voll-ZIP automatisch in `admin_init`, weil WordPress bei einem schon aktiven Plugin nach Upgrade keinen Aktivierungshook erneut ausführt. Erzeugt nur einen Entwurf, niemals automatische Veröffentlichung. Bereits vorhandener Demo-Beitrag mit derselben festen Kennung wird wiederverwendet, nicht dupliziert. Nach erfolgreicher Anlage wird eine einmalige Bestandsmarkierung gesetzt. Beim späteren Löschen entsteht **kein neuer** Demo-Beitrag. Ohne Editorberechtigung, im Frontend oder bei Ajax/Cron kein Schreibpfad. Es werden **keine** Kategorien angelegt; vorhandene Leaf-Kategorie wird nur dann zugewiesen, wenn sie existiert.

**Harte lokale Prüfung (kein Server-Livebeweis):** Die echte Voll-ZIP ist gültig, 1.283/1.283 ZIP-Einträge CRC PASS, WordPress-Hauptordner `affiliate-portal-template-kit`, 12/12 PHP-Lint PASS. Vergleich zu 1.50.786: alle 1.279 übrigen Dateien byteidentisch; nur die beiden Plugin-/Profil-PHPs geändert und zwei neue Dateien hinzugefügt. Positiv-/Negativ-Simulation mit tatsächlichem Importcode: Entwurf und korrektes Foto PASS, Kategorie nur bei Existenz PASS, Tabellen/Banner/Produktflächen PASS, keine Rechte → keine Writes PASS, zweiter Admin-Aufruf → keine Dublette PASS, Löschung → kein Neuimport PASS, vorhandener früherer Testartikel → Wiederverwendung statt zweitem Beitrag PASS.

**Speicherung Original und Rückfall:** Vollständiges 1.50.787 ZIP im bestehenden Library-Plugin-Büro: `/Hobby Depot/Plugin-Büro/HOBBY_DEPOT_HD003_1.50.787_DESIGNTEST_INTEGRIERT_VOLLPLUGIN.zip`. Unabhängige Original-Rückfallkopie: `/hobby rausch/HOBBY_DEPOT_HD003_1.50.787_DESIGNTEST_INTEGRIERT_RUECKFALLKOPIE.zip`. Beide nach Upload als echte Original-ZIPs getrennt zurückgeladen und wiedergeöffnet, CRC- und Versionsprüfung PASS. 63.807.190 Bytes, SHA-256 für beide: `bba4fbf182393265d7d6e55d77d995e1a2d0338da9a247b585c81304b04380d7`. Vorversion 1.50.786 ist separat im Pluginbüro erhalten. **GitHub `ISOLIERTE_PLUGINS/HD-003-DESIGN-TEMPLATE-KIT/CURRENT.zip` ist weiter nicht synchronisiert; Library-Readback und GitHub-Ablage niemals gleichsetzen.**

**NEXT ACTION:** Die neue vollständige 1.50.787 über die vorhandene HD-003-Installation in WordPress hochladen, direkt im Admin unter Beiträge → Entwürfe den [DESIGNTEST]-Beitrag öffnen und seine Frontend-Vorschau beurteilen. Erst bei echtem Frontend-Readback einen Live-PASS für die Artikelansicht dokumentieren.

## 2026-11-01 – HD-003 Vollplugin 1.50.790: Eigenwerbung auf direkt vermietbaren Bannerplätzen

**Quelle:** echte 1.50.789-Voll-ZIP aus dem aktuellen Pluginstand. Daraus **1.50.790 Voll-ZIP** erstellt, Pluginroot `affiliate-portal-template-kit/` unverändert. Ausgabe im aktuellen Chat: `HOBBY_DEPOT_HD003_1.50.790_EIGENWERBEBANNER_ORIGINALLOGO_VOLLPLUGIN.zip`.

**Genau der beauftragte Umfang:** nur der bestehende `rental_slot($placement)`-Pfad des Designprofils Hobby Depot für *noch nicht gebuchte* direkt vermietbare Werbeflächen, inklusive responsive CSS. Freier Platz zeigt neues Eigenwerbemotiv Modellflugzeug/Werkstatt mit beigem Übergang, originalem aus dem aktiven Plugin geschnittenen Logo ohne Unterzeile, Überschrift „Hier könnte Ihre Werbung stehen“, exakt zwei voneinander unabhängigen HTML-Links „Werbebedingungen“ und „Preise“. Keine weitere Unterzeile, kein grelles Grün. Kein nachgezeichnetes Logo. Die Links werden nur mittels `get_page_by_path` und `get_permalink` aus echten veröffentlichten WP-Seiten aufgelöst: Bedingungen bevorzugt `werbebedingungen`/`werb-anzeigebedingungen` inkl. bekannter Varianten; Preise `preise`. Fehlt eine Zielseite, zeigt der Button seinen deaktivierten Zustand ohne erfundenes Linkziel; der echte WordPress-Pages-Readback ist noch offen.

**Harte Abgrenzung:** Bei aktiv gebuchtem Mietslot mit echter Kundenbild-URL/Ziel-URL bleibt das bisherige Kundenbanner völlig unverändert, ebenso der Provider-Filter `pftk_hobby_rental_slot_html`. Die bereits vorhandene zentrale Einmal-Regel `render_rental_for` bleibt erhalten (maximal ein Mietbanner pro Seite). Kein zweiter Werbebanner-Worker, keine Änderung der Affiliate/Partner-Slots, keine Änderung des Pferdeatelier-Zweiges, von Kategorien, Hero oder Suchfunktion.

**Veränderte Dateien im Vollplugin:** exakt zwei PHP-Dateien (Hauptplugin nur Version, Hobby-Profil Version + Austausch der freien Mietbanner-HTML und Ergänzung ausschließlich dazugehöriger CSS) und zwei neue Assets unter `assets/hobby-depot-v150617/eigenwerbung-v150790/`: `logo-original-ohne-unterzeile.png` als unveränderte Original-Pixel des 640×372-Logos, nur auf 640×315 beschnitten; `modellflugzeug-werkstatt.webp` als Ausschnitt aus dem vom Betreiber freigegebenen Modellflugzeug-Banner, ohne eingebrannte Buttons/Schrift. **1283/1285 alte Originaldateien byteidentisch**, neue ZIP enthält **1287/1287** korrekt lesbare Einträge.

**Simulation/QA:** PHP 13/13 Syntax PASS, ZIP CRC 1287/1287 PASS; Privatmethode `rental_slot` anhand des echten Codes mit WordPress-Stub ausgeführt: freie Fläche hat zwei voneinander verschiedene richtige Links, reservierter Platz verwendet Kundenwerbung statt Eigenbanner, Provider-Override unverändert, fehlende Werbebedingungsseite erzeugt keinen falschen Link, doppelte Mietbannerdarstellung wird blockiert – alles PASS. Visualisierung mittels tatsächlichem gerendertem PHP-/CSS-HTML in Chromium bei Desktop 1200px und Mobil 390px; beide Links vorhanden, kein Überlauf. Vorschauen im aktuellen Chat: `HOBBY_DEPOT_WERBEBANNER_1.50.790_VORSCHAU_1200px.png` und `..._390px.png`.

**ZIP-Readback:** SHA-256 `39953565ba8e9d81e5630255f54cee04fe150c54b68b78ad9c5a8ef639dbe9db`; 64.035.283 Bytes. **Kein echter WordPress-Live-PASS**. Die zuletzt bekannte ChatGPT-Library hat Speicherlimit signalisiert; dort ist 1.50.790 nicht als gespeichert verifiziert. Das dokumentierte GitHub-Campus-Protokoll ist **nicht** das Binär-ZIP. Frühere 1.50.789-ZIP und 1.50.787-Library-Backup bleiben erhalten.

**EXAKT NÄCHSTER SCHRITT:** 1.50.790 als *Update des vorhandenen HD-003* installieren; auf einer noch freien mietbaren Werbefläche beide Buttons im echten WordPress-Frontend überprüfen (Ziel-URL, Erreichbarkeit) und eine gebuchte Fläche auf unveränderte Kundenwerbung prüfen. Keine weiteren Pluginänderungen vorher.
