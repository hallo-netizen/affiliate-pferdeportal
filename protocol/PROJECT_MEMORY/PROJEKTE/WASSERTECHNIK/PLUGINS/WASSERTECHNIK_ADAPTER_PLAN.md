# Kategorieplugin – Kopie, Isolation und nötige Anpassungen

## Nachgewiesene Quelle
Original-Vorlage: `HAB-002-KATEGORIE-WORKFLOW` aus dem Campus (Hab & Bewahr), Version 1.14.8.37, unverändert unter `HAB002_ORIGINAL_NICHT_INSTALLIEREN.zip` abgelegt. Herkunfts-Blob `35651f44ac70ed51e663d5dfaf45094bc9f1e3b2`.

## Vorsicht – noch kein funktionsfähiger Wassertechnik-Build
Der Quellcode der 49 ZIP-Einträge wurde hier noch nicht vollständig entpackt, portiert und getestet. Daher ist die Kopie nicht installationsfähig für Wassertechnik. Es wäre falsch, sie nur umzubenennen und als Wassertechnik-Version auszugeben.

## Adapterumfang ohne neue Architektur
- Pluginidentität/Pluginordner sauber auf ein eigenständiges WT-Plugin festlegen, nicht HAB-002 überschreiben.
- Harte Hab-&-Bewahr-Bindungen (IDs, Slugs, Options, Importlauf, Site, Menüs, Cron) im echten Quellcode auflisten und entfernen/parametrisieren.
- An die *noch leere* neue Wassertechnik-Site binden; ausdrücklich fail-closed bei ungebundener Site.
- Originale Workflow-Logik beibehalten soweit kompatibel: Vorschau/Dry-Run → manuelle Einmalfreigabe → ADD-only → Bestands-Readback → Dubletten-/Owner-Prüfung → Fehlerrollback.
- Wörter/Definitionen aus `KATEGORIEKONZEPT/BAUM_ENTWURF.md` erst nach externer fachlicher Freigabe als Daten übergeben, niemals in das Plugin fest einbauen.
- Keine neue Tabelle, kein WP-Core-Eingriff, kein Frontend-HTTP, keine zweite Schreiber-Instanz.
- Positive/negative Tests auf echtem Blank-WordPress, u.a. falsche Site, falsche Parent-ID, Fremdprojekt, Doppelausführung, Importfehler, konkurrierendes Plugin, unveränderte Revision.

**Freigabestatus:** BLOCKED bis alle konkreten Nachweise vorliegen.
