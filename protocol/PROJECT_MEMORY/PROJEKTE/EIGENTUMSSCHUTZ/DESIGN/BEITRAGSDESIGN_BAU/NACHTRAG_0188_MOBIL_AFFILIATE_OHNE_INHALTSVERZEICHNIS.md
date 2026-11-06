# Hab & Bewahr 0.1.188 – mobile Affiliate-Platzierung und kritische TOC-Entscheidung

Stand 06.11.2026. Dies ist eine **isolierte Entwicklungsakte**, nicht der installierte WordPress-Live-Stand oder eine Änderung der autoritativen Campus-Current.

Ausgangspunkt: vollständige lokal verifizierte Designplugin-Version 0.1.187, SHA256 `4a136af62ed1c1e3a3eb3e334ef37aaf883bafb6127477d23c17b3f22acffc27`.
Neuer kompletter Kandidat: `HAB_UND_BEWAHR_DESIGN_0.1.188_MOBIL_AFFILIATE_OHNE_INHALTSVERZEICHNIS.zip`.
SHA256: `f1c92dc85dd506ecbf08b3ab369b303d7e71bcf2b22e391dae280bc7dc60baf8`; 84.348.820 Bytes; ZIP-CRC PASS.
430 statt 429 Plugin-Dateien. Nur drei Originaldateien geändert: `hab-bewahr-design-vorschau.php` (Version + gezielt nur Beitrags-JS), `includes/article-page.php` (Einfügepunkte + echte verwandte Beiträge statt redundanter Inhaltsnavigation), `assets/article-design.css` (responsive Modulstile). Eine neue Datei `assets/article-mobile-affiliate.js` (bestehenden Produkt-/Banner-DOM-Knoten je Bildschirmbreite einmalig verschieben). Sonst keinerlei Änderungen; kein zweites Plugin, keine Kategorie-/Artikeländerung, kein K0.

Regeln:
- Desktop: Produktgruppe und Banner in der rechten Spalte.
- Mobil/Tablet bis 900px: EINE und dieselbe Produktgruppe nach erstem Fachabschnitt direkt vor zweiter H2, ein Banner nach drittem Fachabschnitt vor vierter H2.
- Keine doppelten Affiliate-Links/Provideraufrufe; bei Rückwechsel Desktop wandert derselbe Knoten zurück.
- Produkt und Banner nur, wenn tatsächlich vorhandener Partnerinhalt, sonst ausschließlich Admin-Vorschaumodule; keine irreführenden Preise/Links.
- Kurze/mittlere Fachartikel brauchen keine weitere Inhaltsübersicht: Sie wiederholt nur H2. Nur echte veröffentlichte verwandte Artikel derselben Kategorie, falls verfügbar; sonst verbleibender Link zur Kategorie.
- Schadensfall-Demo ausgenommen; bestehendes `_hbdp_article_no_ads`-Metafeld blockiert automatische mobile Einfügepunkte, für andere Gefahrentypen weitere redaktionelle Entscheidungen erforderlich.
- Bereits vorhandener Schutz der Beitragsfotos, Quellenunterdrückung, Datumsentfernung, Yoast und alter Seitenstruktur bleibt erhalten.

Lokale Prüfungen (nicht WordPress-live): 35/35 PHP lint PASS, JS syntax PASS, WordPress-Mock: Hauptinhalt vorhanden, kein Inhaltsverzeichnis, zwei Einfügepunkte, öffentlich keine Demoangebote, reale Partner-HTML je genau 1x, Notfall-Demo 0x Einfügepunkte. Chromium 1440/390/768/1440: korrektes Verschieben, 0 Duplikate, Quelle nicht öffentlich, geladenes originales Beitragsfoto, kein horizontaler Overflow. Screenshot ist lokale HTML-Darstellung mit angenähertem Header; kein WordPress-Live-PASS. 
