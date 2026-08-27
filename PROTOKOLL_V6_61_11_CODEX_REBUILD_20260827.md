# V6.61.11 – Codex-Ergebnis lokal rekonstruiert und geprüft

Stand: 27.08.2026

Das von Codex erzeugte Installer-ZIP war für den Nutzer nicht direkt herunterladbar. Das vollständige Codex-Ergebnis mit Root-Cause-Report, Changed-Files-Patch und Byte-Identity-Hashes lag jedoch vor.

Daher wurde V6.61.11 lokal aus CURRENT_V6.61.10 exakt anhand des Codex-Patches rekonstruiert.

## Byte-Beweis gegen Codex-Ergebnis
Die drei laut Codex geänderten Dateien stimmen bytegenau mit den von Codex gemeldeten SHA-256-Werten überein:

- assets/frontend.css = `0a02369d8824e96879aea45a6ab54fc1a8de5230d1b5dd99a9f18a31710725f0`
- pferdeportal-affiliate-router.php = `78ad046725c2ac08251117dee2ac1771d3bb02c9bf9f6084683c0071ed4a4a53`
- readme.txt = `8b2eb45961d17a465f86a19105e9f754ca68a788a38c789934149986f0821f95`

Alle übrigen 16 Plugin-Dateien sind gegenüber CURRENT_V6.61.10 byteidentisch.

## Zusätzlicher lokaler Browser-Test
Anders als im Codex-Lauf war lokal ein echtes Chromium verfügbar. Die rekonstruierte V6.61.11 wurde deshalb mit Chromium gegen den relevanten realen Design-Kontext getestet.

Testbreiten: 1440, 1280, 1024, 900, 768, 700, 620, 480, 390, 360 px; zwei Provider-Reihenfolgen; kurze, mittlere und lange Titel; Preis vorhanden/nicht vorhanden; drei Bilder.

Ergebnis:
- 20/20 V6.61.11 Browserfälle PASS
- Desktop-Außenkarten exakt gleich hoch
- Button-Unterkanten exakt gleich
- Bilder 150x150
- Abschnittsabstand gegenüber V6.61.8-Baseline unverändert
- kein horizontaler Overflow
- PHP-Lint alle 14 PHP-Dateien PASS
- Fresh-Unpack 19/19 byteidentisch

Finaler Zustand: `LOCAL_BROWSER_HARD_PASS_AWAITING_LIVE` – ausdrücklich kein LIVE PASS.

## Prozessregel
Wenn Codex viele Arbeits-/Evidence-Dateien anzeigt, ist nur der finale Installer als Nutzerdownload vorgesehen. Falls Codex den Installer nicht direkt bereitstellt, darf aus einem vollständigen Changed-Files-Patch nur dann lokal rekonstruiert werden, wenn die resultierenden geänderten Dateien anschließend exakt gegen die von Codex gemeldeten Datei-Hashes verifiziert werden.
