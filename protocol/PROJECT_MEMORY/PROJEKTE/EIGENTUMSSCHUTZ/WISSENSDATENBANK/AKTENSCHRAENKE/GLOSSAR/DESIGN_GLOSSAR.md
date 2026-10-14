# SICHERHEITSGLOSSAR – DESIGNVERTRAG
**Vergleich:** Pferde-Atelier Design 1.50.541 (Journal-Startseite Glossar/Regionen, LIVE PASS 2026-09-16), dokumentiertes Glossar-Relationendesign 1.50.528. Übernahme des **Layoutprinzips**, kein Kopieren von Pferde-Texten, Markengrafiken oder CSS-Dateien.

## Übersicht / A–Z
- Hab-&-Bewahr-Header C, Creme `#FAF8F4`, Terrakotta `#B35C40`, dezente Salbeiakzente.
- Breadcrumb `Startseite / Magazin / Wissen / Glossar`, H1 „Sicherheitsglossar“, 1 Kurzunterzeile, A–Z-Leiste, schlichte Volltext-Suche nach Begriff+Synonym, sechs optional sichtbare Weltfilter.
- Dokument auf Desktop max. 1200–1280px, luftiges lesbares Raster; auf mobil eine Spalte, Knöpfe fingerbedienbar, kein horizontaler Überlauf; keine überladene Mega-Navigation auf Glossar-Seite.
- In A–Z nur **freigegebene** Begriffe. Kein veröffentlichter Platzhalter pro KANDIDAT, keine Thin-Content-URLs.
- Begriffe mit 1–2 Sätzen Anrisstext und Klick auf echte Glossar-Detailseite.

## Detail
- H1 Begriff; direkt eine präzise Kurzdefinition; 150–200-Wort-Fachtext, individuelle Zwischenüberschriften, Abgrenzung, kein erzwungenes Layoutfilling.
- Rechte Kontextspalte in genau dieser Reihenfolge (von Pferde-Atelier): 1. **Schutzwelt**, 2. **Verwandte Begriffe**, 3. optional **Mehr zum Thema** (starke existierende WP-Zielseite). Related nur verlinken, falls vorhanden und veröffentlicht; sonst Text ohne erfundene URL.
- Fußhinweis redaktionelles Prüfdatum, in Hochrisikofeldern ggf. Norm-/Rechtsstand. Technische Rohquellen intern in Forschungsakte.
- Nativer WordPress-Draft-Manager (vom Layout getrennt), individuelle SEO-Felder, Prüfung vor Publish.
- Kein zweites Designplugin: Rendering übernimmt das bestehende Hab-&-Bewahr-Design; Content-Verwaltung darf technisch separat sein, ohne Hauptkategorien zu ändern.

## Live-Konflikt
Im R3/V8-Readback bereits `editorial:glossar` (WP-Seite ID 184, `magazin-glossar-a-z`). Design 0.1.7 erzeugt parallel die Sonderroute `/glossar/`, laut Nutzer derzeit leer. **Keine zweite kanonische Seite**; zuerst vorhandenen Page-Readback/live prüfen und dann einen Owner wählen. Bis dahin keine SEO-Freigabe.
