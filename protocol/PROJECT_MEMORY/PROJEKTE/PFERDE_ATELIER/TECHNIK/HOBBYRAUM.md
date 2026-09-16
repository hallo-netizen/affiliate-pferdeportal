# PFERDE-ATELIER / TECHNIK – HOBBYRAUM

STAND: 2026-09-16
STATUS: BLOCKED

## 1-KLICK-ÜBERSICHT

**AKTUELLER AUFTRAG**  
WordPress-Speicherballast ohne Änderung von Inhalt oder Struktur identifizieren und kontrolliert entfernen.

**ERSTER BLOCKER**  
Der neue Kandidat `WordPress Speicheranalyse 1.1.0` ist lokal hart geprüft, aber noch nicht im echten WordPress installiert und live bedient.

**NEXT ACTION**  
`PPA-014 / CURRENT.zip` als Update über 1.0.1 installieren → im Plugin die WPvivid-Dateiliste öffnen → vor jeder Löschung die angezeigten Dateien prüfen.

## Gebundener Arbeitsweg

1. `CURRENT_STATE.md` frisch lesen.
2. `/Campus-Plugins/PFERDE_ATELIER/PPA-014/CURRENT.zip` verwenden.
3. WordPress-Installation über bestehende 1.0.1.
4. Plugin-Seite **WordPress Speicheranalyse** öffnen.
5. WPvivid-Dateien vollständig anzeigen lassen.
6. Nur eindeutig entbehrliche Backup-Dateien markieren.
7. Exakte Bestätigung `LOESCHEN` + Browserbestätigung.
8. Speicheranalyse erneut ausführen.
9. neuen JSON-Scan gegen den Stand in `CURRENT_STATE.md` vergleichen.
10. Erst nach realem Readback WordPress-LIVE-Status nachziehen.

## Rückgabeweg

- technischer Status → `CURRENT_STATE.md`;
- Plugin-Artefakt/Version → `../PLUGINS/REGISTER.md` + `/Campus-Plugins/PFERDE_ATELIER/PPA-014/`;
- Chronologie → `UPDATEPROTOKOLL.md`.

Keine zweite Fehler-, Ziel- oder Pluginwahrheit im Hobbyraum erzeugen.
