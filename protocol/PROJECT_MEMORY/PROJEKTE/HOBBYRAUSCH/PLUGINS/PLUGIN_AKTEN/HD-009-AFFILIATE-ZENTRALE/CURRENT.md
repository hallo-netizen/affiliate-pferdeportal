# HD009 – Hobby Depot Affiliate-Zentrale – aktuelle technische Plugin-Akte

**Stand 07.11.2026 · einziges CURRENT-Plugin: 0.1.19-dev.**

- Installierbare Voll-ZIP: `../../ISOLIERTE_PLUGINS/HD-009-AFFILIATE-ZENTRALE/CURRENT.zip`.
- Größe **1.066.241 Bytes**, SHA-256 `53f0feb7bf5e97032f840fd5e1fe2ddee80f24b3440202e0c136cf38a67e6579`, Git-Blob `93c4eca96659a06fbc9a5b7911fa4c1b70ffac93`.
- Ein vorhandener Pluginroot `affiliate-portal-router/`, nicht zwei installierbare Module.
- Neuer **Registerplatz-Vertrag**: Desktop nach `Auf einen Blick`, vor `Hobbygruppe`; ein Querbanner im Text nach `Kosten und Ausrüstung`; Mobil nach gesamtem Haupttext die quadratische Anzeige zuerst, vor `Hobbygruppe`.
- Umsetzung ausschließlich über vorhandenen HD009-`hdar_ci_register_footer` + vorhandenen `render_affiliate_slot_for_context`/Amazon-Eigenbanner-Fallback. HD007-`profile_sidebar()` und `full_article()` sind unverändert. HD003-Design unverändert.
- **Vorgänger-Design 0.1.18 Variante 4 vollständig beibehalten:** schmaler Titelverlauf, echtes Hobbyfoto, gelb-oranger Amazon-Originalbutton mit Pfeil, kein eigenes Logo. Keine neue Bannerzuordnung oder Quelle.
- CSS bleibt die bisherige HD009-`hdar-amazon-start.css` unter demselben Modus und demselben Dateinamen, mit Version 0.1.19 als Browsercache-Schutz.
- **Nachweise:** `EVIDENCE/HD009_0119_PROFILE_LAYOUT_REPORT.txt`; `EVIDENCE/HD009_0119_WP_REAL_BROWSER_PASS.txt`. Isoliertes **ECHTES WordPress + MariaDB + HD003 + HD007 + HD009**, HTTP und Chromium Desktop+Mobile, alle Anzeigeplatz-/Layout-Assertions PASS; ZIP-CRC und 24 PHP-Syntaxprüfungen PASS.
- **WordPress-Liveabnahme noch offen:** vorhandener Betreiberstand laut Gespräch vor diesem Update 0.1.17; keine Behauptung, dass 0.1.19 auf dem Live-Server installiert ist.

**Ältere Versionen 0.1.15–0.1.18 sind nur Git-Historie. Die alleinige aktuelle technische Datei ist das oben genannte CURRENT.zip.** Benutzer muss nur einmal die aktuelle ZIP über vorhandene WordPress-Plugininstallation ersetzen.
