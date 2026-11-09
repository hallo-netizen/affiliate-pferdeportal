## 09.11.2026 – HAB-001 Design RC19 (0.1.192): Mobile Hero, Schriftgleichheit und doppelte Vandalismus-Kacheln

**Physisch vollständige aktuelle Design-ZIP im eigenen Pluginbüro:** `PLUGINS/ISOLIERTE_PLUGINS/HAB-001-DESIGN/CURRENT.zip`, **84.538.795 Bytes, 432 Dateien**, Git-Blob `5b228d917bf8744826f359b71523c5a11c3c5c10`, vom unabhängigen GitHub-Build SHA256 `d8f08ca73da4c56be61d55fdde02dac5ed5a1ecadcbc986221e2c93357ec8302`. **WordPress-Pluginversion 0.1.192**; neu gebaute vollständige ZIP, kein Zusatzplugin. **HAB-004 Affiliate RC18 (0.1.15-rc18) bleibt unverändert.** Keine fremden Portale, Inhalte oder Kategorie-IDs geändert.

**Ursachen & KISS-Änderungen (sechs vorhandene Dateien, keine neue Komponente):**
- *Vandalismus & Zerstörung*: Die beiden bisher unterschiedlichen Dateien `curated-20261019-16.webp` und `fix-130-vandal-fassade.webp` zeigen dieselbe Fassadenszene. Der Weltkachel `Gebäude & Ausstattung` wurde das bereits im Designbestand vorhandene Foto `topic-62-innenwand-vandalismus.webp` zugeordnet (beschädigte Innenwand; eigenständiges Motiv). Die zentrale Bildidentität erkennt die beiden bisherigen Fotos künftig auch als Duplikat. `Fassade & Außenflächen` bleibt mit `fix-130-vandal-fassade.webp`.
- *Nur Mobil bis 760 px*: Bestehende Hero-Bilder waren bereits mit `object-fit:cover` skaliert; das eigentliche „vernebelt“-Problem verursachte ein quer über **das gesamte Bild** laufender, mobil immer noch deckender Verlauf. Für alle sechs Schutzwelten sowie R2 und R3 auf **einen oberen, nach unten transparenten Verlauf** umgestellt: Bild unterhalb des Titels klar, Text oben mit hellem lesbarem Hintergrund, Foto und Schrift bleiben responsive. Desktop-CSS absichtlich unverändert.
- *Aufklappbare Kategorietexte*: Bei R3 und sämtlichen WordPress-Blattkategorien liefert `hbdp-detail-intro` die sichtbare Einleitung und `hbdp-detail-expansion` den ausgeklappten Teil. Beide erhalten mobil identische **16px Schriftgröße und 1,72 Zeilenhöhe**. Sichtbare Einleitung behält ihren farbigen Hintergrund; Ausklappteil bleibt ohne Einfärbung.

**Prüfungen:** Originalzip vom offiziellen Campus als Ausgangsbasis (SHA256 `def9ceb5a99eb965aa55805038d92e93e53747191786edc9f44fe74bbe560a7e`) gegen sechs Original-Dateihashes geschützt. Fertige sechs Dateien gegen sechs unabhängige Soll-Hashes geprüft. **35/35 PHP-Syntax**, **432/432 ZIP-CRC**; lokaler Chromium-Browser (echte ausgelieferte Styles und Fotos, repräsentativer Kategorie-DOM) in **320/375/390/600/760/900/1200 px**: jeweils exakt 16px sichtbarer und geöffneter Einleitungstext; Bild lädt, kein horizontaler Überlauf, Titel nicht abgeschnitten. Bis 760 px vertikaler Verlauf; ab 900 px unveränderte Desktop-Variante. GitHub Actions `HAB Design RC19 build single CURRENT ZIP` erfolgreich. Für reproduzierbare Ablage: `DESIGN/RC19_BUILD_FROM_RC18.py`.

**Wichtig:** Test mit CSS und modellierten Original-Kategorieelementen ist **keine WordPress-Liveabnahme**. Nach Installation der RC19-Design-ZIP bitte mobile Hauptwelt, R2, R3, ein Blatt mit aufgeklapptem Text und Vandalismus-Kachel prüfen. Live-Status bleibt offen, bis Benutzer-Screenshot vorliegt.

---

## 08.11.2026 – VERBINDLICHE HAB CURRENT-RELEASE: DESIGN RC18 + AFFILIATE RC17

**Tatsächlich im offiziellen Pluginbüro als vollständig neu gebaute, geprüfte `CURRENT.zip` auf dem geschützten Releasezweig; Veröffentlichung nach Merge:**
- **HAB-001-DESIGN 0.1.191 (RC18)**: `PLUGINS/ISOLIERTE_PLUGINS/HAB-001-DESIGN/CURRENT.zip`; 84.538.023 Bytes; **SHA256 `def9ceb5a99eb965aa55805038d92e93e53747191786edc9f44fe74bbe560a7e`**, Git-Blob `04f8ef38c649049cebcc12f240471a66d270a465`; **432 Dateien**, 35/35 PHP-Lint und 432/432 ZIP-Inhaltsverifikation.
- **HAB-004 Affiliate-Zentrale 0.1.14-rc17**: `PLUGINS/ISOLIERTE_PLUGINS/HAB-004-AFFILIATE/CURRENT.zip`; 2.331.918 Bytes; **SHA256 `b22e4d49a56b25e3fc2e46c9bdd0ccbd7c6c16eb7c1f6bb48ae005db0ba50a03`**, Git-Blob `e8f5d5c77459a2e94b77c093f7c58883a2e4386c`; **36 Dateien**, 25/25 PHP-Lint und 36/36 ZIP-Inhaltsverifikation.
- Ausgangs-ZIPs **wort-/bytegenau aus dem offiziellen Pluginbüro erneut geprüft**: Design 0.1.189 SHA256 `947a950273edb6bf47e76ffeef67ff51425db620adc2650c742831e73093134c`; HAB-004 RC11 SHA256 `cf8cf7946aa7605dadecda1f041cfc6fb150c7971f7c9feb9dbb6dd1ac8eabda`. Alle Altdateien übernommen. Nur belegte Quelländerungen von RC18/RC17 zugespielt; sieben bereits in HAB-001 vorhandene Themenfotos für HAB-004 bytegleich kopiert. **Kein neues Plugin, keine neue DB, keine Änderungen an Pferdeatelier/Hobbydepot, kein bezahlter Suchlauf.**

**Nutzer-Liveabnahme der VORGÄNGER RC17 Design + RC16 Affiliate vom 08.11. 15:25–15:36:** Kachelfotos PASS, Raster-Kacheln formatfüllend PASS. **Noch offen / durch neuen RC18-Kandidaten offline korrigiert:** Einteilungslogik auf allen Kategorieebenen, auch bei vollständig gefüllten Zeilen; hoch-nach-unten-Bildverlauf in Amazon-Rasterkacheln, größerer am unteren Rand platzierter offizieller Amazon-Button, Hover auf Beitragsvorschauen, präzise Produktsuche statt „Wasser & Feuchtigkeit“ → Luftbefeuchter. Browser mit echten Originaldateien/CSS: **42 Konstellationen** aus sechs Bildschirm-/Rastertypen, darunter Hauptwelt/R2/R3, 900/390 px, plus 12 gesonderte Screenshots/Prüfungen bei 1250px, keine Überläufe, CTA sichtbar, Originalbutton und Hover. PHP-Funktionstest: **17 konkrete Zielzuordnungen** bestanden. **Echte WordPress-Liveabnahme dieser NEUEN Versionen noch offen**; nicht als schon installiert ausgeben.

**Korrekturregel Amazon:** Nicht die bloße Themenüberschrift „Wasser & Feuchtigkeit“ als Suchwort: gezielt `Wassermelder Leckagesensor Wasserstopp`; für Leckage/Rückstau/Siphon passende physische Schutz-/Reparaturprodukte; feste Themenbäume statt geratenem Amazon-Kategorieausgang; nur bestehender Hausbanner als nachrangiger Fallback. Benutzerwunsch gilt für alle Schutz-/Kategorienebenen, einschließlich voller Reihen. Versicherungsstrang bietet thematisch Dokumentenschutzartikel, **keine als Versicherungsleistung ausgegebenen Amazon-Produkte**.

**Zulässige nächste Aktion:** Die beiden neuen aktuellen `CURRENT.zip` im WordPress-Backend als Updates installieren; dann an mehreren Hauptwelten und R2/R3 inklusive Vandalismus, Wasser und unterster Kategorie testen, volle Reihen, Handyansicht, Amazon-Ziel und Beitrag-Hover. Keine RC16/RC17-Vorinstallation nötig; immer beide aktuellen Zips zusammen. 

---

# HAB-001-DESIGN – MANIFEST (Dateinachweis, keine zweite Current)

- Technische Versionsautorität: `../../PLUGIN_AKTEN/HAB-001-DESIGN/CURRENT.md`.
- Vollständige, installierbare Datei im **bestehenden** Pluginordner: `CURRENT.zip`.
- Fassung: **0.1.189**, Plugin-Ordner `hab-bewahr-design-vorschau/`.
- 84.349.647 Bytes, 430 Dateien, ZIP-CRC PASS.
- SHA-256: `947a950273edb6bf47e76ffeef67ff51425db620adc2650c742831e73093134c`.
- Git-Blob: `504fccb82f4e9a3b10bb6405b468e1dbd03c62e1`.
- Unabhängig von GitHub neu abgerufen und geprüft: erfolgreicher GitHub-Actions-Run `42223947280`, Ergebnis `INDEPENDENT_REMOTE_READBACK_PASS`.
- Letzter lokaler Check: PHP 35/35, JS, ZIP-CRC, Wortmarke/Template-Routing und Browser-Mock-Responsive; **keine WordPress-Livefreigabe**.
- Vorheriger unveränderter Original-/Rollbackstand: Design 0.1.184 aus PR #625 (SHA-256 `76043e5c093058a4d8aff8fd6642307cade951c8267641dc710b8ed70cd323e3`), über Git-Historie wiederherstellbar.
- Andere Pluginakten und deren ZIPs bleiben unverändert.
