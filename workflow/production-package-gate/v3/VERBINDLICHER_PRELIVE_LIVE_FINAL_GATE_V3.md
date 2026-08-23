# Verbindlicher PRELIVE/LIVE/FINAL-Gate V3

- Lokale Tests dürfen höchstens `PRELIVE_PASS` erzeugen.
- `FINAL` ist ohne passenden echten PSERC-Live-Result verboten.
- Der Live-Result muss exakt `package_id` und `production_package_source` des Pakets zurückmelden.
- Der vollständige Supervisor-/Bridge-/PPM-Draft-/Readback-Endstatus muss PASS sein.
- `publish_allowed` muss false bleiben.
- Ein lokaler Bootstrap mit `wp_kses_post($html) { return $html; }` ist als Release-Evidenz ausdrücklich verboten.
- Redaktionsplan/READY dürfen zur Fehlerbehebung nicht verändert werden.
