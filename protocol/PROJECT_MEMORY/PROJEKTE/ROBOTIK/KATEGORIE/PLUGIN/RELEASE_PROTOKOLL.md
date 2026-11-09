# Robotik-Pluginbüro – einziges Release-/Prüfprotokoll
Stand 09.11.2026. **Protokoll nach jedem neuen Plugin im selben Commit mit Installer und CURRENT_STATE.md fortschreiben.**

| Version | Datei im Archiv | Änderung | Prüfstatus | WordPress |
| --- | --- | --- | --- | --- |
| 0.1.0 | `VERSIONEN/0.1.0.zip` | Neutrale JSON-Planungsoberfläche, ohne Import | Historischer ZIP-/PHP-PASS | Archiv; keine eigene belegte Live-Abnahme |
| 0.2.0 | `VERSIONEN/0.2.0.zip` | Produktseitenrollen, Parent-/Kategorieprüfung | Historische lokale Tests (16 Struktur- und weitere Admin-Tests), PHP/ZIP-PASS | Nutzer-Screenshot: grüne formale Prüfung; ersetzt durch 0.3.0 |
| **0.3.0** | **`VERSIONEN/0.3.0.zip`** | **Manuell lesender WordPress-Inventarcheck; ein Gesamtbericht, optional HivePress** | **ZIP-CRC PASS, PHP-Lint 2/2 PASS; 7.926 Byte, SHA256 `3c31aaaf86379a054034a80c8aeb3eaebdf616baa953ac079793f6495f1ecd30`; kein ungeprüfter Altportal-Code** | **09.11.2026: „installiert“ vom Nutzer gemeldet; echter WP-Bestandsscan/Export OFFEN** |

## Welche Datei gilt?
`PLUGIN/CURRENT.zip` und `PLUGIN/VERSIONEN/0.3.0.zip` sind exakt derselbe Installer. Die Vorgänger bleiben unverändert im Versionsarchiv. Es gibt **keine** zweite aktive Plugin-Identität und keinen alternativen Current-Zweig.

## Behauptungsgrenzen
- **DATEI PASS** = ZIP prüfbar; PHP syntaktisch richtig; genau die vorhandenen Dateien.
- **INSTALLIERT LAUT NUTZER** = Nutzer hat Installation gemeldet, kein unabhängiger Backend-Nachweis.
- **LIVE PASS** erst nach erfolgreichem WordPress-Bestandscheck und Stichproben des einen Gesamtberichts, HivePress ggf. separat; aktuell **NICHT** erreicht.
- Die geplante Keyword-/GitHub-Master-/Inhalts-/Anzeigen-Gesamtprüfung ist **noch NICHT in 0.3.0 umgesetzt**.

## Übergabe an den nächsten Chat
1. `PROJEKTE/ROBOTIK/KATEGORIE/CURRENT_STATE.md` zuerst lesen, danach diese Datei und `RECHERCHE/MASTER_ABGLEICH_20261109.md`.
2. **Keine Plugin-Neuerstellung, keine zweite Masterliste.** Nur `robotik-kategorie-workflow` weiterentwickeln.
3. Nächste Live-Prüfung: „Robotik Kategorie → Bestand prüfen“ und ggf. einmaligen JSON-Gesamtbericht prüfen.
4. Anschließend **nur lesenden** GitHub-Master-Abgleich und Research-Gap-Funktionen aus geprüfter allgemeiner Kategorie-Pluginlinie adaptieren. Nicht HAB-spezifische Altlasten/Writer übernehmen.
5. Nach jeder späteren Plugin-Version: ZIP + Changelog + `CURRENT.zip` + `CURRENT_STATE.md` atomar auf GitHub im Robotik-Pluginbüro.

**Keine WordPress-Kategorien/Seiten wurden durch das GitHub-Ablegen verändert.**
