# HD-003 – ISOLIERTER PLUGINSTAND – MANIFEST

STAND: 2026-11-01
STATUS: **CURRENT.zip BLOCKED / NEUER 1.50.785-DATEIFUND, RAW-READBACK NICHT MÖGLICH**

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

