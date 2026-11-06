# Hab & Bewahr – Beitragsspalten und Bildvorschau 06.11.2026

## Befund
0.1.186 enthielt ein Bild nur für Beiträge mit gesetztem WordPress-Beitragsbild. Der Artikelrenderer hatte nur eine Inhaltsspalte, keine Sidebar. Im visuellen Entwurf waren dagegen Produktkarten und Banner in einer rechten Spalte zu sehen. Die fünf Musterposts enthielten Quellenabschnitte `p.hb-quellen`, unfertige redaktionelle interne-Link-Hinweise und Affiliate-Platzhalter.

## Isolierter Fix
Lokaler WP-Installationskandidat `HAB_UND_BEWAHR_DESIGN_0.1.187_BEITRAG_ZWEI_SPALTEN_FOTOS.zip`, SHA-256 `4a136af62ed1c1e3a3eb3e334ef37aaf883bafb6127477d23c17b3f22acffc27`. Ausgangspunkt vollständige 0.1.186 mit 429 Einträgen. **Exakt 3 Dateien geändert** (Hauptplugin Version/CSS-Cache, `includes/article-page.php`, `assets/article-design.css`), alle übrigen 426 byteidentisch. Keine neuen Plugins, Datenbankänderungen, K0-Verknüpfung oder Kategorienanpassungen.

- Zwei-Spalten-Layout: links die vorhandenen WordPress-Beitragsinhalte samt H1/H2/Listen/Tabellen/Merksatz, rechts redaktionelle Sprungnavigation, wirkliche Kategorie, Produkt- und Bannerplätze.
- Vorhandenes WordPress-Beitragsbild hat Vorrang; nur für die genau fünf importierten Musterbeitrags-Slugs kommt jeweils ein geprüftes, **schon vorhandenes** passendes einzelnes Themenfoto als reine Anzeige-Fallback zum Einsatz.
- Für Administratoren gibt es bei fehlenden Affiliate-Anbietern gekennzeichnete, **nicht kaufbare** Beispielkarten und Demo-Banner. Öffentlich nie erfundene Preise/Links/Angebote. Reale Affiliate-Filter: `hbdp_article_product_cards_html`, `hbdp_article_auto_banner_html`; echte Partneranbindung noch offen.
- Quellenabschnitte `p.hb-quellen`, unfreigegebene interne Linknotizen und Import-Affiliate-Platzhalter werden nur beim Anzeigen entfernt – **bleiben im WP-Beitragsinhalt erhalten**. Kein sichtbares Datum; Yoast-Datumsregeln aus 0.1.186 bleiben unverändert.
- Sturmschaden-Notfallartikel bekommt keine werbliche Demo-Sidebar.

## Prüfung
ZIP CRC PASS, 35/35 PHP-Lint PASS, PHP-renderer-Probe für Wohnmobil-Betrag PASS: zwei Spalten, Quellen/Notizen/Platzhalter entfernt, Titelbild, drei Admin-Produkte, Sprungmarken, Admin-Banner; öffentliche Ausgabe ohne Fake-Angebote. Lokaler Chromium-Vorschau-Browser: 1440px und 390px, echte Bildladebreite 1672px, keine horizontalen Überläufe, ein H1 und echte Tabellen. Screenshot entspricht geprüftem Artikel-HTML/CSS, Header nur angenähert, da Live-WordPress nicht erreicht werden konnte.

**WICHTIG:** Dieses Entwicklungsdokument ist keine autorisierte neue Campus-Current-ZIP und kein WordPress-Live-PASS. Bestehende offizielle Design-Current 0.1.184 nicht heimlich ersetzen. Nächster Schritt einmaliges Live-Update von 0.1.186 auf 0.1.187 und Sichtprüfung mit dem veröffentlichten Wohnmobil-Musterartikel (Desktop, mobil, privat und eingeloggter Admin).