# HAB & BEWAHR – RC17 Kachelfotos und Amazon-Werbekachel, Stand 08.11.2026

**Geprüfte, direkt im Chat bereitgestellte Installationsdateien:**
1. **HAB-001 Design 0.1.190 / RC17**: `Hab-und-Bewahr-Design-RC17-Kacheln-und-Bilder.zip` – 84.534.411 Bytes, SHA256 `5a991c82c44be45bb936b6b138a2b732b232d18d1a982edf8715a9159550d035`, 432 ZIP-Einträge.
2. **HAB-004 Affiliate 0.1.13-rc16 (unverändert)**: `Hab-und-Bewahr-Affiliate-RC16-Design-und-Kategorietexte.zip` – 2.326.838 Bytes, SHA256 `536ae7621c61d3d412e01b5d08ad86d215e335ba038553cef6c6ce665d5fcfec`, 36 ZIP-Einträge.

**KEINE Verwechslung:** Auf offiziellem GitHub-Campus sind weiterhin die alten binären `HAB-001/CURRENT.zip` und `HAB-004/CURRENT.zip` hinterlegt. RC17 und Affiliate RC16 wurden im **Chat** als ZIP abgegeben, **nicht** als neue GitHub-CURRENT-ZIP publiziert. Live-WordPress-Installation/Abnahme der Kombination weiter OFFEN. Kein weiteres Plugin und keine WordPress-Core-Änderung.

## Wirklich implementiert, anhand echter ZIPs geprüft
- Das **originale HAB-001 Design** wurde erweitert, nicht ersetzt: Original 430 Dateien -> 432, keine gelöscht; **sechs vorhandene Dateien** geändert (Hauptdatei mit Version und CSS-Cache, `assets/style.css`, `assets/area-prototype.css`, `includes/area-design-prototype.php`, `includes/world-layout.php`, `data/area-image-mapping-v1.json`) plus genau zwei neue WebP-Fotos.
- Leckage & Rohrbruch: `Badewanne abdichten` → `rc17-badewanne.webp` (Badewanne); `Siphon undicht` → `rc17-siphon.webp` (undichter Siphon). Alle 11 tatsächlichen Wasser-Kachelbilder einzeln als Bilder und Zuordnung betrachtet, unterschiedlich und vorhanden. Alle 265 explizit kartierten Themenbilder sind physisch vorhanden; Bilder in anderen Bereichen nicht pauschal redaktionell freigegeben.
- Der bereits von **HAB-004 RC16** gelieferte Amazon-House-Banner wird im vorhandenen R2- und Hauptwelt-Raster eingesetzt. Keine neue Bannerengine, kein Duplikat, kein zusätzlicher kostenpflichtiger DataForSEO-Lauf. Desktop drei Spalten (R2) / vier Spalten (Hauptwelt), Tablet zwei, Mobil ein/ zwei; dynamische rechnerische Auffüllung von nicht vollständigen Kachelreihen. Der einzelne Amazon-Banner kann mittig stehen; passt sich samt Motiv und Button der tatsächlichen Kachelgröße an, ohne weitere Rahmen/zusätzliche 'Anzeige'-Texte innerhalb der Kachel.
- Das Original-Design-Foto und vorhandene Werbekampagnen haben weiterhin Vorrang; bei deaktiviertem Anbieter/fehlendem Banner wird nicht künstlich ein Amazon-Ziel erfunden.
- Original Amazon-Button aus Hobbydepot sowie der von RC16 korrigierte Header, Verlauf, Kategorietext und Tresorfoto unverändert. Andere Portale und eBay/Idealo nicht berührt.

## Prüfungen und Grenze
- Beide tatsächlichen ZIP-Dateien vollständig CRC-geprüft; **Design 35/35 PHP-Syntaxprüfungen**, Affiliate **25/25 PHP-Syntaxprüfungen** bestanden.
- Browser mit Original-Design- und Affiliate-CSS und den Original-WebP-/Badge-Assets bei **1250px, 900px, 390px** geprüft: R2-Kachelbanner und Welt-Kachelbanner jeweils volle Elternbreite und Höhe, alle CSS-Bilder vorhanden, kein horizontaler Überlauf.
- 40 unterschiedliche Kachel-Anzahlen bezüglich gerader/ungerader Restspalten rechnerisch auf Desktop und Tablet geprüft. Achtung: Dies ist ein echter Browser-Test mit **simuliertem Frontend-DOM** und **echtem Original-CSS**, **keine WordPress-Live-Abnahme**. Nicht behaupten, die vollständige Website sei bereits fehlerfrei.
- Die 11 konkreten Fotos der Wasserkategorie haben eine reale Mindestgröße von 502x285 (dieses Foto ist vorhanden, aber kleiner als die 1672er Fotos); die übrigen zehn ≥1600px. Kein willkürlicher Austausch eines fachlich korrekten Fotos nur wegen der Auflösung.

## Installieren und gezielt live prüfen
**Nur zwei bestehende WordPress-Plugins als Updates:** Design RC17 und Affiliate RC16. Kein eigenes RC17-Affiliate-Plugin. Seite `https://hab-und-bewahr.de/wasser-und-feuchtigkeit/wasser-und-feuchtigkeit-leckage-und-rohrbruch/`: die elf echten Kacheln, Badewanne/Siphon und der mittig platzierte, volle Amazon-Rasterbanner. Seite `https://hab-und-bewahr.de/wasser-und-feuchtigkeit/`: Weltkacheln, passend ausgefüllte Amazon-Kachel ohne weiße Leerflächen; Desktop und Mobil. Ein Button-Klick führt zur passenden Amazon-Suche.
