# EIGENTUMSSCHUTZ – DESIGN – FEHLERQUELLEN

STAND: 2026-10-14

## Noch offene Nachweisgrenzen
- HBD-DESIGN-001: WordPress-Live-Verhalten der Design-Vorschau 0.1.0 noch nicht geprüft. Keine Aussage über Live-Kompatibilität, Seitenqualität oder Laufzeitkosten. Status OFFEN.
- HBD-DESIGN-002: Master-Logodatei nicht separat belegt; Referenzausschnitt vom 8.10. nur für vorläufige Visualisierung. Status OFFEN.
- HBD-DESIGN-003: Vier Beispiel-Fotos stammen aus einem Nutzer-Mockup, keine final lizenzierten/verifizierten redaktionellen Titelbilder. Status OFFEN.

Keine bekannten reproduzierten Live-Probleme der Vorschau; nicht mit Fehlerfreiheit gleichsetzen.


## HBD-DESIGN-004 – Getrenntes Startseitenplugin erzeugt doppelten Design-Pluginbestand (14.10.2026)
STATUS: **LOCAL CLOSED – 0.1.4 IN-PLACE-UPDATE LOKAL PASS; WORDPRESS-LIVE-MIGRATION WEITER OFFEN**.
BEFUND: `HAB_UND_BEWAHR_STARTSEITE_0.1.0.zip` besitzt eigene Plugin-Identität und eigenen Ordner, obwohl bereits das umfassendere `HAB_UND_BEWAHR_DESIGN_VORSCHAU_0.1.3_TEXTMENUE_KLARE_THEMEN.zip` existiert. Nutzer meldet zwei unterschiedliche Designplugins im WP-Backend. Falsch war die Empfehlung, ein zweites Plugin zu installieren.
URSACHE: Startseiten-Modul wurde statt eines In-Place-Updates als separates WordPress-Plugin verpackt.
KISS-KORREKTUR: Bestehenden Original-Designplugin-Quellstand beschaffen, Startseite dort integrieren und Anzeigenamen auf „Hab & Bewahr – Design“ vereinheitlichen, ursprünglichen Plugin-Basename behalten. Zweites Plugin erst deaktivieren, wenn dessen eventuelle Shortcode-Nutzung und das in-place-Update geprüft sind; nie blind löschen. Kein dritter Pluginordner. Primäre Statusquelle: `CURRENT_STATE.md`.
REGRESSIONSSCHUTZ: vor jeder Ausgabe Installationsidentität/Basename gegen bestehendes Plugin prüfen; Performance-Checks verpflichtend.

NACHHOLPRÜFUNG 14.10.2026: Exakte Original-ZIP `0.1.3` wirklich in der bestehenden Library gefunden und hashgleich wiedergewonnen (SHA `f7cd98459fba15fb0d2ec61cb0c837a6d4e77708ae22f910aba8efa7b0d894b8`). Einziges Update 0.1.4 mit unverändertem Plugin-Basename erzeugt, lokaler 57/57-PASS plus sieben Simulationsläufe und ZIP-Integrität; SHA `044a745463fd22ec821ba5d99001264228bef3adbc3abed04b28dfdbddbc25b0`. Doppelung wird nach echtem WP-Update und anschließendem Deaktivieren des separaten 0.1.0-Plugins beendet, NICHT automatisch. Aktueller Stand/NEXT ACTION nur in `CURRENT_STATE.md`.

## HBD-DESIGN-005 – Pluginversion 0.1.3 lud Navigations-JS auf allen Seiten
STATUS: **LOCAL CLOSED in 0.1.4; WORDPRESS-LIVE-PERFORMANCE-OFFEN**.
BEFUND: In der echt wiedergewonnenen 0.1.3-Hauptdatei war `wp_enqueue_script('hbdp-nav',...)` außerhalb der `hbdp_for_query() !== null`-Bedingung und lief site-wide. KISS-FIX: Assets nur auf vom Designplugin gerenderten Seiten und Shortcode laden; shared Header-C-CSS von home-only CSS getrennt. Vollständiges Kategorie-Menü revisions-/weltabhängig transient-gecached; keine neuen Cron-/SEO-/Kategorie-Writes. Lokal durch statische und PHP-Mock-Positiv-/Negativtests geprüft; reale WP-Benchmark ausstehend.


## HBD-DESIGN-006 – Leere Navigations- und Themenkachel-Beschriftungen nach 0.1.4 (14.10.2026)
STATUS: **LIVE 0.1.4 FAIL / LOKAL 0.1.5 FIX-PASS / WP-LIVE-RETEST OFFEN**.
EVIDENZ: Screenshot Nutzer 14.10.2026 15:25: nur Magazin und Dienstleister als Nav-Text, Weltenmenü nur Pfeile, Hochkantkacheln ohne Titel.
URSACHE: 0.1.4-Live-Snapshot-Normalisierung liest `$raw['name']`; die echte zentrale APKW-Workflow-Quelle `active_nodes` speichert `display_name`. Alle importierten Namen gingen dadurch in der Designprojektion verloren. Bestehende transient-gecachte HTML-Navigation war mit falschen Bezeichnungen bereits gespeichert. Zusätzlich verwendeten Fotokacheln fälschlich eine Welt-Schleifenvariable als eigene Bezeichnung.
KISS-FIX: In demselben Plugin 0.1.5 auf `display_name` umstellen, den Titel jeder Fotokachel aus eigenem `$item[0]` rendern; Cacheversion in Navigations-Key aufnehmen. Korrektur isoliert nur 3 ausführbare Dateien plus README, kein Daten-/Kategorie-/Workflow-Eingriff.
REGRESSIONSSCHUTZ: WordPress-Snapshot-Schema **aus dem tatsächlich installierten zentralen Kategorie-Workflow lesen**; 546-Knoten-Simulation mit den richtigen Feldnamen, Browser-Check für sechs Navigations-, sechs Welt- und sechs Fotokacheltitel plus Cache-Neufassung. Lokal 30/30 PASS, Desktop+Mobil 6/6+6/6+6/6. **Nicht als WordPress-live-PASS ausgeben.** Current und NEXT ACTION ausschließlich DESIGN/CURRENT_STATE.md.
