# HD009 – einziges aktuelles Hobby Depot Affiliate-Plugin

**07.11.2026 · Version 0.1.19-dev · vollständig gebaut und in echtem lokalem WordPress erfolgreich geprüft.**

- **Einzige Installationsdatei:** `CURRENT.zip`
- **Größe:** 1.066.241 Bytes
- **SHA-256:** `53f0feb7bf5e97032f840fd5e1fe2ddee80f24b3440202e0c136cf38a67e6579`
- **Git-Blob:** `93c4eca96659a06fbc9a5b7911fa4c1b70ffac93`
- **Original-WordPress-Pluginroot:** `affiliate-portal-router/`.
- **Nur HD009 geändert**, HD003-Design und HD007-Hobbyregister samt Originalinhalt und CSS bleiben bytegleich.

## Neuer verbindlicher Hobbyregister-Platzvertrag

- **Desktop:** im originalen HD007-Profil-Aside `Auf einen Blick` → **bestehender quadratischer Affiliate-Banner** → `Hobbygruppe` → `Ähnliche Hobbys` → Magazin.
- **Im Artikel:** genau **ein zusätzlicher breiter Affiliate-Banner unmittelbar nach dem vollständigen Abschnitt `Kosten und Ausrüstung`**, nicht zwischen Überschrift und Absatz und nicht zusätzlich am Artikelanfang.
- **Mobil (max. 820px):** zunächst `Auf einen Blick`, anschließend **kompletter Haupttext** einschließlich integriertem Querbanner nach `Kosten und Ausrüstung`; danach **der quadratische Seitenleisten-Banner als erstes Element**, erst danach `Hobbygruppe` und weitere Seitenleistenboxen. Kein großes Banner unmittelbar am Seitenanfang.
- Keine neuen Partner, Tabellen, Feed-Pfade, CSS-Frameworks oder Bannerverteiler. Es werden ausschließlich `render_affiliate_slot_for_context` und der bereits vorhandene `hdar_ci_amazon_banner` im einzigen bestehenden HD009-`wp_footer`-Anschluss verwendet. Bei fehlendem freigegebenem, fachlich passenden Motiv bleibt der Platz leer. Keine erzwungene Fremdwerbung.
- Das vorhandene 0.1.18-Design **Variante 4** bleibt vollständig erhalten: Titel im schmalen Verlauf, großes passendes Hobbyfoto, gelb-oranger CTA mit **offiziell zulässiger Original-Grafik `Erhältlich bei Amazon`** und Pfeil, ohne Hobby-Depot-Logo. Querbanner auf Seiten responsiv, Quadrat 1:1 im Register. Nur ein „Anzeige“-Label pro Platz.
- **Bestehende HD007-Ausgabe verändert sich nicht.** Die Banner werden vom vorhandenen HD009-Footer-Anschluss nach Abschluss des Seitenaufbaus an ihren bestehenden HD007-Platz gesetzt; die Mobil-Position verwendet die existierende HD007-Rasterfolge `facts / copy / tail`.
- **Stil-Aktualisierung:** Die bereits vorhandene `hdar-amazon-start.css`-Datei wird unter derselben, unveränderten Betriebsart geladen. Der bestehende Style-Cache-Schlüssel wird auf `0.1.19` aktualisiert. Keine zweite Registrierung und keine zusätzliche CSS-Datei.

## Harte Nachweise

1. Original-HD007-`CURRENT.zip` geprüft: `profile_sidebar` beginnt mit `hdr-facts`, danach Hobbygruppe; `full_article` hat `Kosten und Ausrüstung`; mobile Rasterfolge `facts / copy / tail`. **Beides physisch aus Originalplugins belegt.**
2. Vollständige HD009-`CURRENT.zip`: ZIP-CRC PASS, **24/24 PHP-Syntax PASS**, alte Bannerlogik und Werbemittel erhalten.
3. **ECHTER LOKALER WordPress-Test, nicht nur künstliche Testdaten:** WordPress, MariaDB, WordPress-Theme und unveränderte HD003-/HD007-Plugins zusammen mit der fertig gebauten HD009 0.1.19 installiert. Öffentliche HD007-Route `/hobbyregister/airbrush-modellbau/` über HTTP 200 gerendert. Chromium hat tatsächliche HTML-Elemente nach JavaScript-Platzierung und CSS-Ausgabe gemessen.
4. **Desktop 1420px PASS:** Sidebar-Fakten-Element Index 0, Anzeige Index 1, Hobbygruppe Index 2; Bildbanner 305px sichtbar, Inline-Banner nach Material/Ausrüstung 229px sichtbar. Exakt eine Side-Ad und eine Inline-Ad.
5. **Mobil 500px PASS:** vollständiger Hauptartikel endet vor Quadratbanner; Quadratbanner endet vor Hobbygruppe; Mobil-Rasterplatz `tail`; Seitenleisten-Banner 495px, Inline-Banner 170px, beide sichtbar.
6. Prüfprotokolle: `../../PLUGIN_AKTEN/HD-009-AFFILIATE-ZENTRALE/EVIDENCE/HD009_0119_PROFILE_LAYOUT_REPORT.txt` und `HD009_0119_WP_REAL_BROWSER_PASS.txt`.
7. Vor dem bestandenen Test wurde ein **lokaler WordPress-Installationsfehler bei der Test-URL** behoben (`/site` doppelt), nicht in HD003 oder HD007. Es besteht keine neue technische Abhängigkeit.

**Grenze:** Der erfolgreiche WordPress-Test erfolgte isoliert. Die echte Betreiberseite `https://hobby-depot.de` wurde mit 0.1.19 noch **nicht aktualisiert**; eine Live-Abnahme ist deshalb noch offen.

## Einmaliges Update und zwei Testpunkte

1. `CURRENT.zip` über **WordPress → Plugins → Neues Plugin hinzufügen → Plugin hochladen → Aktuelles Plugin ersetzen** einspielen. Keine separate Installation eines weiteren Plugins.
2. `https://hobby-depot.de/hobbyregister/airbrush-modellbau/` Desktop: nach Auf einen Blick; Mobil: nach Haupttext; zusätzlich im Text nach Kosten und Ausrüstung.
3. `https://hobby-depot.de/gestalten/malen-zeichnen/` zur Kontrolle, dass vorhandene Querbanner und Partner-Ausgabe von v18 unverändert sind.
