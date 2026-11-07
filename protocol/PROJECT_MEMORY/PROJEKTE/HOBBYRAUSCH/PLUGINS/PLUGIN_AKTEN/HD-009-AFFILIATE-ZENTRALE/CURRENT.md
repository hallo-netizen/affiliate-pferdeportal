# Hobby Depot – HD009 Affiliate-Zentrale – einziges Current

**0.1.24, 07.11.2026**

- Voll-ZIP: `../../ISOLIERTE_PLUGINS/HD-009-AFFILIATE-ZENTRALE/HOBBY_DEPOT_AFFILIATE_HD009_0.1.24.zip`
- Voll-ZIP-Werkbank: `../../ISOLIERTE_PLUGINS/HD-009-AFFILIATE-ZENTRALE/CURRENT.zip` (byteidentisch).
- Größe: 1.068.611 Bytes; SHA-256: `e1bc7cc4d7ab69bc711c424c3d1a612c4710f66155eba7a401552329a800f3a6`; Git-Blob: `a803da717395689cfd69698611fdef723f94166c`.
- **Geändert nur HD009:** Kategoriearchiv-Kontext im vorhandenen Slot-Shortcode, einmaliger Artikel-Fallback im `the_content`-Filter, blankes/dupliziertes Fotomotiv durch textlichen Brand-Banner ersetzt, Home-Fallback, CSS und Versionskennungen.
- **Bewährte Auswahl vor Fallback unverändert:** bereits verteilte Banner und ASIN-Produktkarten, Partner-/Bildfreigabe, Kategorie-Elternpfad, DataForSEO, AWIN, idealo, eBay. Bestehende HD003-/HD007-Dateien unverändert.
- Das Hobbyregister nutzt Quadrat als textlichen Themenbanner und Quer als einziges Affiliate-Foto. Der Seiten-Hero bleibt.
- Die aktuelle Artikel-Einbindung verwendet den bestehenden `post_inline_banner` ohne neue Tabelle, Cronjob oder Sonderarchitektur.
- **Tests PASS:** Eingangs-Hash, CRC, PHP 24/24, sechs Originalmethoden-Tests, Browser-Simulation bei 4 Breiten und 4 Seitentypen. GitHub Actions 42394892545 und 42395022776.
- **Liveinstallation offen.** Nach Installation Stichproben `/hobbyregister/muenzen/`, `/hobbyregister/alte-kameras-reparieren/`, `/gestalten/`, `/fertigen/buch-papier/buchbinden/`, `/kettenhemd-ringe-zangen-auswahl/`; Artikel-Sonderfälle mit manuellen Partnern unverändert.
