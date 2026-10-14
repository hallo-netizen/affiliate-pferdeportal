# EIGENTUMSSCHUTZ – DESIGN – FEHLERQUELLEN

STAND: 2026-10-12

## Noch offene Nachweisgrenzen
- HBD-DESIGN-001: WordPress-Live-Verhalten der Design-Vorschau 0.1.0 noch nicht geprüft. Keine Aussage über Live-Kompatibilität, Seitenqualität oder Laufzeitkosten. Status OFFEN.
- HBD-DESIGN-002: Master-Logodatei nicht separat belegt; Referenzausschnitt vom 8.10. nur für vorläufige Visualisierung. Status OFFEN.
- HBD-DESIGN-003: Vier Beispiel-Fotos stammen aus einem Nutzer-Mockup, keine final lizenzierten/verifizierten redaktionellen Titelbilder. Status OFFEN.

Keine bekannten reproduzierten Live-Probleme der Vorschau; nicht mit Fehlerfreiheit gleichsetzen.


## HBD-DESIGN-004 – Getrenntes Startseitenplugin erzeugt doppelten Design-Pluginbestand (14.10.2026)
STATUS: **OFFEN – WORDPRESS-LIVE-MIGRATION NICHT AUSGEFÜHRT**.
BEFUND: `HAB_UND_BEWAHR_STARTSEITE_0.1.0.zip` besitzt eigene Plugin-Identität und eigenen Ordner, obwohl bereits das umfassendere `HAB_UND_BEWAHR_DESIGN_VORSCHAU_0.1.3_TEXTMENUE_KLARE_THEMEN.zip` existiert. Nutzer meldet zwei unterschiedliche Designplugins im WP-Backend. Falsch war die Empfehlung, ein zweites Plugin zu installieren.
URSACHE: Startseiten-Modul wurde statt eines In-Place-Updates als separates WordPress-Plugin verpackt.
KISS-KORREKTUR: Bestehenden Original-Designplugin-Quellstand beschaffen, Startseite dort integrieren und Anzeigenamen auf „Hab & Bewahr – Design“ vereinheitlichen, ursprünglichen Plugin-Basename behalten. Zweites Plugin erst deaktivieren, wenn dessen eventuelle Shortcode-Nutzung und das in-place-Update geprüft sind; nie blind löschen. Kein dritter Pluginordner. Primäre Statusquelle: `CURRENT_STATE.md`.
REGRESSIONSSCHUTZ: vor jeder Ausgabe Installationsidentität/Basename gegen bestehendes Plugin prüfen; Performance-Checks verpflichtend.
