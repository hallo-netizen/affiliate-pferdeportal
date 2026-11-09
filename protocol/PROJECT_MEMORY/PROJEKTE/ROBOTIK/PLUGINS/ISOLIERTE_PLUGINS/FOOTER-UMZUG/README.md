# ROBOTIK / Pluginbüro – Footer-Umzug 1.2.1 (TEST)
Stand 09.11.2026

- **Aktueller Installer**: [CURRENT.zip](CURRENT.zip) = [VERSIONEN/1.2.1.zip](VERSIONEN/1.2.1.zip), identische Bytes (Git-Blob `6158877b77b5444b3f0ce31bd9ac6fdfc3ed2f88`).
- **Versionen-/Prüfprotokoll:** [RELEASE_PROTOKOLL.md](RELEASE_PROTOKOLL.md).
- **Zielvertrag:** [../../FOOTER_UMZUG_ZIELVERTRAG_20261109.md](../../FOOTER_UMZUG_ZIELVERTRAG_20261109.md).
- Altes Original 1.1.1 liegt im Hobbydepot-Gebäude, nicht als Robotik-Current.

## Was die Datei macht
Überträgt nur die im Footer verlinkten **Seiten mit Inhalten** sowie neue Footer-Menüs. Kein CSS, Theme, Design oder Widgets. Vor dem Import **Vorschau und Freigabe**. Vorhandene Seiten/Menüs werden niemals aktualisiert; neue Seiten bleiben **Entwürfe**, insbesondere Impressum/Datenschutz/AGB.

## Klickweg
**Quellportal**: WordPress → Werkzeuge → Footer-Umzug (vorhandene 1.1.1) → **Footer exportieren** → eine JSON-Datei.
**Robotik**: WordPress → Plugins → Installieren → ZIP **1.2.1** → Aktivieren → **Werkzeuge → Footer-Umzug** → JSON hochladen → **Nur Vorschau** → Freigabe nur wenn korrekt.
Danach neue Entwurfsseiten im Backend auf Robotik-Namen, Kontakte, Pflichten, Marken und Links prüfen und erst bewusst veröffentlichen.

**WICHTIG:** Altes 1.1.1-Exportformat ist mit 1.2.1 verarbeitet; das neue Plugin muss **nicht** auf dem Quellportal installiert werden. Das alte ZIP ist für Robotik wegen Hardcoded-Umwandlung und Überschreibungsrisiko **nicht** freigegeben.

**Prüfstand:** php -l PASS, ZIP CRC PASS, Originalformat-JSON-Test PASS, ungültiges JSON-Schema abgewiesen. Noch kein echter Live-Test; es wird nicht behauptet, das Theme habe bereits einen passenden Footer-Platz. Nicht als bereits installiert melden.
