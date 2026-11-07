# HD009 – einziges aktuelles Hobby-Depot-Affiliate-Plugin

**07.11.2026 · Hobby Depot Affiliate-Zentrale 0.1.18-dev · fertig gebaut und technisch getestet.**

- **Einzige Installationsdatei:** `CURRENT.zip`
- **Größe:** 1.065.228 Bytes
- **SHA-256:** `130681bc1b695cbb95b08d8d9ac2d575e7142027754ffd1bd051065e462bae7f`
- **Git-Blob:** `5b4ef7b4277b63ab73d0a0ae690186c272c8bc09`
- **Original-WordPress-Pluginordner:** `affiliate-portal-router/`, keine zusätzliche Installation und keine zweite Engine.
- Original-Pferdeatelier-/Hobby-Affiliate-Automatik (Amazon/idealo, Kategorie-/Elternpfad-, Format- und Veto-Logik) bleibt erhalten.

## Verbindlicher CI-Vertrag – Nutzerwahl Variante 4

**Keine Hobby-Depot-Logografik**, kein Slogan „Entdecke deine Ausrüstung“.

1. **Kopf:** schmaler warmer Verlauf mit genau dem aktuellen Hobby-Titel, etwa `Airbrush-Modellbau`.
2. **Bild:** ein großes, vom HD007-/HD003-Fotobestand tatsächlich zum Hobby passendes Bild, ohne Collage. Steht kein fachlich geprüftes Motiv zur Verfügung, kein Eigenbanner.
3. **Button auf dem Foto:** komplementäres Gelb-Orange, original unmodifiziertes offizielles DE-Werbelogo **„Erhältlich bei Amazon“**, separater Pfeil. Nicht das normale Amazon-Logo: dessen Verwendung in diesem Werbekontext bedarf nach Amazons Richtlinien besonderer Genehmigung. Bei Plätzen kleiner als 178px wird aus Platz-/Mindestgrößengründen auf den zulässigen Text „Bei Amazon entdecken“ umgeschaltet. Das Amazon-Logo wird niemals verfälscht oder kleiner als 140px angezeigt.
4. **Bannerformat:** Quadrat 1:1 für einzelne Hobbyregister-/Glossar-Seiten, bei normalen Kategorie-/Hubseiten breiter responsiver Banner; mobiles Layout und tatsächliche verfügbare Platzbreite entscheiden die Höhe. Mindesthöhe des breiten Banners 135px (auf kleinen Bildschirmen 145px), damit das Bild sichtbar bleibt.
5. **Kennzeichnung:** genau ein „Anzeige“-Hinweis. Im bestehenden HD003-Kategorienplatz steht bereits „Anzeige · Partner“; dort wird die innere zweite Kennzeichnung ausgeblendet.
6. **Ziel:** vorhandene getrackte Amazon-Suchlinks für die konkrete Hobby-Ausrüstung. Der tatsächliche Seitenname wird korrekt aus HTML-Sonderzeichen aufgelöst (z. B. Malen & Zeichnen). Keine erfundenen Produktangebote oder Preise.
7. **Wahrung der Systemgrenzen:** Mietbanner („Hier könnte Ihre Werbung stehen“) unverändert ausschließlich im HD003-Designplugin; keine neuen Tabellen, Schnittstellen, Bannerkataloge oder Routing-Wege.

## Ursächlich nachgewiesener Formatfehler

Öffentliches Hobbydepot-HTML auf `/gestalten/malen-zeichnen/` zeigt `.hd-next-partner-banner` als vorhandenen HD003-Werbeplatz. Die vorhandenen Original-CSS-Regeln erzwingen dort `76px !important` auf Werbeplatz, Kinder und Bilder – daher wurde der alte Querbanner zu einem abgeschnittenen Streifen. Der in HD009 0.1.18 hinzugefügte **eng begrenzte** Stil löst diese Höhe nur bei den eigenen `.hdar-ci-amazon-slot`-Anzeigen, sodass sich der originale Platz in seiner Breite erhalten und in seiner Höhe anpassen kann.

## Echte Tests

- Originale unmodifizierte Amazon-DE-Logo-PNG aus offizieller Amazon-Datei verifiziert; SHA-256 `fb6db85f898078fa6df03740b58d65f431b8a6186c97f6b8a72e95f11b9ab8e5`.
- **24/24 PHP-Syntaxprüfungen, vollständige ZIP CRC, PHP-Positiv-/Negativtests PASS.**
- **Chromium-Browser nach echten HD003-76px-Formatregeln:** großes Quadrat 700px PASS, Sidebar-Quadrat 186px PASS, Querformat 770px PASS, schmales Querformat 355px PASS.
- Sichtprüfungsbilder: `EVIDENCE/HD009_0118_VARIANT4_SQUARE-LARGE.jpg`, `EVIDENCE/HD009_0118_VARIANT4_SQUARE-SIDEBAR.jpg`, `EVIDENCE/HD009_0118_VARIANT4_WIDE-PAGE.jpg`, `EVIDENCE/HD009_0118_VARIANT4_WIDE-MOBILE.jpg`.
- Detailbericht: `../../PLUGIN_AKTEN/HD-009-AFFILIATE-ZENTRALE/EVIDENCE/HD009_0118_CI_REPORT.txt`.
- **Live-WordPress-Installation mit 0.1.18 noch nicht bestätigt.** Die vorherige 0.1.17-Produktivversion zeigte nach Verzögerung tatsächlich beide Banner; diese neue Layoutversion wurde nur isoliert geprüft.

## Nach EINMALIGER Installation prüfen

- `https://hobby-depot.de/gestalten/malen-zeichnen/`: eine Anzeige, vollständiger breiter Titel/Foto/Button, keine abgeschnittene Streifenanzeige.
- `https://hobby-depot.de/hobbyregister/airbrush-modellbau/`: schmaler Verlauf/Titel und großes Foto mit gelb-oranger CTA im bestehenden Quadratplatz.
- Bei Browser-Cache ggf. Seite neu laden; keine neuen API-Keys oder DataForSEO-Freigaben notwendig.
