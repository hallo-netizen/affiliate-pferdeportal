## 08.11.2026 – VERBINDLICHE HAB CURRENT-RELEASE: DESIGN RC18 + AFFILIATE RC17

**Tatsächlich im offiziellen Pluginbüro als vollständig neu gebaute, geprüfte `CURRENT.zip` auf dem geschützten Releasezweig; Veröffentlichung nach Merge:**
- **HAB-001-DESIGN 0.1.191 (RC18)**: `PLUGINS/ISOLIERTE_PLUGINS/HAB-001-DESIGN/CURRENT.zip`; 84.538.023 Bytes; **SHA256 `def9ceb5a99eb965aa55805038d92e93e53747191786edc9f44fe74bbe560a7e`**, Git-Blob `04f8ef38c649049cebcc12f240471a66d270a465`; **432 Dateien**, 35/35 PHP-Lint und 432/432 ZIP-Inhaltsverifikation.
- **HAB-004 Affiliate-Zentrale 0.1.14-rc17**: `PLUGINS/ISOLIERTE_PLUGINS/HAB-004-AFFILIATE/CURRENT.zip`; 2.331.918 Bytes; **SHA256 `b22e4d49a56b25e3fc2e46c9bdd0ccbd7c6c16eb7c1f6bb48ae005db0ba50a03`**, Git-Blob `e8f5d5c77459a2e94b77c093f7c58883a2e4386c`; **36 Dateien**, 25/25 PHP-Lint und 36/36 ZIP-Inhaltsverifikation.
- Ausgangs-ZIPs **wort-/bytegenau aus dem offiziellen Pluginbüro erneut geprüft**: Design 0.1.189 SHA256 `947a950273edb6bf47e76ffeef67ff51425db620adc2650c742831e73093134c`; HAB-004 RC11 SHA256 `cf8cf7946aa7605dadecda1f041cfc6fb150c7971f7c9feb9dbb6dd1ac8eabda`. Alle Altdateien übernommen. Nur belegte Quelländerungen von RC18/RC17 zugespielt; sieben bereits in HAB-001 vorhandene Themenfotos für HAB-004 bytegleich kopiert. **Kein neues Plugin, keine neue DB, keine Änderungen an Pferdeatelier/Hobbydepot, kein bezahlter Suchlauf.**

**Nutzer-Liveabnahme der VORGÄNGER RC17 Design + RC16 Affiliate vom 08.11. 15:25–15:36:** Kachelfotos PASS, Raster-Kacheln formatfüllend PASS. **Noch offen / durch neuen RC18-Kandidaten offline korrigiert:** Einteilungslogik auf allen Kategorieebenen, auch bei vollständig gefüllten Zeilen; hoch-nach-unten-Bildverlauf in Amazon-Rasterkacheln, größerer am unteren Rand platzierter offizieller Amazon-Button, Hover auf Beitragsvorschauen, präzise Produktsuche statt „Wasser & Feuchtigkeit“ → Luftbefeuchter. Browser mit echten Originaldateien/CSS: **42 Konstellationen** aus sechs Bildschirm-/Rastertypen, darunter Hauptwelt/R2/R3, 900/390 px, plus 12 gesonderte Screenshots/Prüfungen bei 1250px, keine Überläufe, CTA sichtbar, Originalbutton und Hover. PHP-Funktionstest: **17 konkrete Zielzuordnungen** bestanden. **Echte WordPress-Liveabnahme dieser NEUEN Versionen noch offen**; nicht als schon installiert ausgeben.

**Korrekturregel Amazon:** Nicht die bloße Themenüberschrift „Wasser & Feuchtigkeit“ als Suchwort: gezielt `Wassermelder Leckagesensor Wasserstopp`; für Leckage/Rückstau/Siphon passende physische Schutz-/Reparaturprodukte; feste Themenbäume statt geratenem Amazon-Kategorieausgang; nur bestehender Hausbanner als nachrangiger Fallback. Benutzerwunsch gilt für alle Schutz-/Kategorienebenen, einschließlich voller Reihen. Versicherungsstrang bietet thematisch Dokumentenschutzartikel, **keine als Versicherungsleistung ausgegebenen Amazon-Produkte**.

**Zulässige nächste Aktion:** Die beiden neuen aktuellen `CURRENT.zip` im WordPress-Backend als Updates installieren; dann an mehreren Hauptwelten und R2/R3 inklusive Vandalismus, Wasser und unterster Kategorie testen, volle Reihen, Handyansicht, Amazon-Ziel und Beitrag-Hover. Keine RC16/RC17-Vorinstallation nötig; immer beide aktuellen Zips zusammen. 

---

# HAB-001-DESIGN – TECHNISCHER PLUGIN-CURRENT

**Plugin:** Hab & Bewahr – Design
**Plugin-Identität/-Ordner:** `hab-bewahr-design-vorschau`
**Aktuelle projektbezogene vollständige Fassung:** **0.1.189**
**Speicherort:** `PLUGINS/ISOLIERTE_PLUGINS/HAB-001-DESIGN/CURRENT.zip` im bestehenden Hab-&-Bewahr-Pluginbüro, Campus-Branch `hobbyroom/project-memory-campus-v1-20260905`.
**Installationsdatei:** vollwertige ZIP, 84.349.647 Bytes, 430 ZIP-Einträge, Version im Hauptplugin 0.1.189.
**SHA-256:** `947a950273edb6bf47e76ffeef67ff51425db620adc2650c742831e73093134c`
**Git-Blob-SHA:** `504fccb82f4e9a3b10bb6405b468e1dbd03c62e1`.
**Freigabebeleg:** Hab-&-Bewahr-Design-Release 0.1.189, isolierter Branch `hbd-design-0189-release-20261106`; GitHub Actions `42223947280`: deterministischer Neuaufbau, ZIP-CRC, 35 PHP-Syntaxprüfungen, JS-Syntax sowie *unabhängiger frischer GitHub-Neuabruf* der ZIP mit vollständig identischer SHA-256, 430/430-Datei-CRC, Versionstest PASS. Kandidaten-PR zum geschützten Campus ist getrennt abzunehmen.
**Livetest:** WordPress-Liveinstallation und genaue Darstellung im echten Theme noch nicht unabhängig geprüft – **LOCAL PASS / LIVE OFFEN**.
**Unverändert:** Kategorie-Workflow, Bildzentrale, K0, die fünf veröffentlichten Beiträge, Kategorien/IDs/Slugs, HivePress-/Yoast-Originale.
**Rollback:** vollständige vorherige Designversion 0.1.184 im Git-Vorgängerstand des Campus (PR #625, 84.339.643 Bytes; SHA-256 `76043e5c093058a4d8aff8fd6642307cade951c8267641dc710b8ed70cd323e3`), nicht löschen. Versionsnummern 0.1.185–0.1.188 waren lokale Zwischenkandidaten, nicht jeweils eigenständige Plugins.

**WICHTIG:** Ein neues Plugin ist nicht angelegt. Der Name `CURRENT.zip` bezeichnet eine echte 84-MB-WordPress-ZIP, kein Patch/Protokoll. Der derzeitige Release-Zweig ist nicht die offizielle Campus-Current, solange der reguläre PR nicht gemergt ist.
