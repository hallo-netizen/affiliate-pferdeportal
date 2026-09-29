# Pferde Atelier – Konzept 9

**Rolle dieser Datei:** Überblick / Navigation, **keine CURRENT-Wahrheit**.

## Einstieg

1. Bürotür: `K9:pferdeatelier` im Repo `hallo-netizen/text-start`.
2. Zuständige einzige Current-Autorität: `CURRENT_STATE.json` auf Branch `konzept9/greenfield-20260929`.
3. Frischecheck gegen den dort gebundenen technischen Stand.
4. Danach ausschließlich die `next_action` aus `CURRENT_STATE.json` ausführen.

## Invariantes K9-Prinzip

Recherche, Schreiben, Prüfung und Reparatur erzeugen jeweils vollständige, dauerhaft gespeicherte Produkte. Routing entscheidet nicht der Chat, sondern die feste K9-Zustandslogik. Ein offener Chat-Arbeitsauftrag wird ausschließlich über `runtime/CHAT_ENTRY.json` gebunden. Nach einem Abbruch wird kein alter Chat rekonstruiert; der exakt offene Auftrag wird wiederverwendet.

K9 liest oder importiert keine K4–K8-Laufzustände. Qualitätsgates bleiben LT 6.8, PPM 6.7.9, PSERC, ENDSTEMPEL und WordPress-Endformatprüfung. `publish_allowed=false`.

Aktuelle Status-, Blocker-, Run- oder NEXT-ACTION-Werte stehen **nur** in `CURRENT_STATE.json`.
