# HD009 – Affiliate-Zentrale Hobby Depot – gültige Current-Version

**HD009 0.1.27 · 08.11.2026**

- Installationsdatei: `HOBBY_DEPOT_AFFILIATE_HD009_0.1.27.zip`, vollständig und byteidentisch zu `CURRENT.zip`.
- 1.554.012 Bytes, SHA-256 `bba83f67e48039bf921709823d81fc00b7658b7e9c825a833314f6821ff0a2fd`, Git-Blob `68ae6a59b6b1a945eaa24e787fae27178ed55f82`.
- Bisheriger Fehler: Echte WordPress-Leaf-Kategorien wie `sportdrachen-drachen-leinen` haben `parent=0`; die Bannerwelt war aus deren Kategoriepfad nicht erkennbar, obwohl sie in HD003 exakt mit `Bewegen > Wind & Drachen > Sportdrachen` hinterlegt ist. Deshalb wurde ohne Foto ausgegeben.
- **KISS-Korrektur:** Vorhandene Kategorieautorität `HD003/assets/hobby-depot-v150750/leaf-category-map-v150750.json` lesen; passende Welt und Untergruppe übernehmen. Wenn ein passendes genehmigtes Gruppenfoto verfügbar ist, dieses statt des unpassenden Outdoor- oder Textmotivs anzeigen. Sonst die bereits integrierten acht allgemeinen Weltfotos.
- Für `Drachen & Leinen`: vorhandenes `wind-drachen.webp` (Luftdrachen), ausdrücklich keine unpassende Outdoor-Ausrüstung. Keine Doppelung mit dem separaten Sportdrachen-Foto der Beitragsvorschau.
- Alle bestehenden Bannerplätze, Amazon-Button, Farbverlauf, Größe (Kategorie 6:1 / mobil 4,2:1), Tracking, Provider-Prioritäten, Registerbanner und Artikelbanner unverändert. CSS-Versionskennung auf 0.1.27 erhöht.
- **Geprüft:** Quellpaket 0.1.26 SHA-verifiziert; ZIP-CRC PASS, PHP 24/24 PASS, reale PHP-Funktionstests „Sportdrachen-Banner mit Foto“ PASS. Alle 3.376 Leaf-Kategorien lassen sich einer der acht Welten zuordnen. Browser-Simulation auf echter Sportdrachen-Kategorieseite bei 1440, 900, 390 und 360px PASS; originales Amazon-Badge erhalten. Actions 42463656841/42463793782.
- **Echte Installation und anschließende WordPress-Abnahme offen.**
