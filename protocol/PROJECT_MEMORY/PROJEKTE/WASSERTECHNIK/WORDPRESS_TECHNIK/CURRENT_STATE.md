# WASSERTECHNIK / WORDPRESS_TECHNIK – einzige aktuelle Büroautorität

**Stand:** 14.11.2026 · **Status:** W9 eine ADD-only-Importfunktion für vorhandenes WT001 in v0.1.5 als **offline geprüfte Test-ZIP** vorbereitet; **noch nicht installiert oder in WordPress ausgeführt**.

**Beleg:** WP-Snapshot `../PRUEFUNG/WORDPRESS_TEST_20261114/wassertechnik-bestand.json`, am 14.11.2026 12:28:47 UTC von `https://wasser.oliver-beil.de/` exportiert, Plugin WT001 Version **0.1.1 beim Export**. Er meldet 2 Seiten (Beispielseite, Datenschutzerklärung), 1 Beitrag (Hallo Welt!) und 1 Beitragskategorie (Allgemein), keine Wassertechnik-Inhalte. HivePress nicht eingerichtet. Das ist eine **historische Bestandsaufnahme**, keine Behauptung über späteren Livezustand.

**W6:** `../KATEGORIEKONZEPT/W6_WORDPRESS_IMPORTVORSCHAU_218_20261114.json` bildet 113 vorgesehene Seiten und 105 Beitragskategorien schreibfrei ab. Im gespeicherten Snapshot kein Namens-/Slugkonflikt. Unterjährige Bestandsänderungen vor echtem Import im **einmaligen gebündelten** Vorabgleich berücksichtigen, nicht für jedes Objekt separat prüfen.

**Technikregel:** WordPress-Core unverändert; nur eine Wassertechnik-Pluginidentität, keine Fremdportal-Schreibaktion, keine doppelten Schreiber. Gegebenenfalls nach ausdrücklicher Freigabe einmaliger ADD-only-Import und eine echte WP-Rücklesung. Keine neue Plugin-Version für die Konzeptvorschau.

**Offen:** Aktueller WP-Livezustand seit Export, Backup-/Produktionsfreigabe und schreibender Import ausdrücklich nicht belegt. Journal und HivePress sind getrennte Säulen und nicht Teil der 218-Owner.

**Historie:** Der Einrichtungsstand vom 08.11.2026 hatte noch keine gebundene WP-Instanz; die WP-Bestandsaufnahme vom 14.11.2026 hat dies für die Testseite konkretisiert.

**W7-Navigation:** Menütiefe Haupt → ggf. Bereich → konkretes Produkt. Darunter zugehörige Inhaltskategorien im Produkt, nicht als vierte Mega-Menüebene. Anzeigespalten der 8 Käuferbereiche + Industrie-Infozugang sind in W7 vorgeschlagen. Zwei Labels sind nur Menübeschriftungen, keine neuen WP-Seiten. Tatsächlichen Menüaufbau später im vorhandenen Design auf Desktop/Mobil testen, keine neue Plugin-Version.

**W8:** Einmalige ADD-only-Erweiterung von WT001 (kein zweites Plugin) ist notwendig, um 113 Seiten und 105 WP-Kategorien anzulegen. Danach echte WP-Readback- und nach Freigabe Desktop/Mobil-Menüprüfung; keine zweite SEO-Entscheidung. Siehe `../PLUGINS/W8_IMPORT_QUELLCODE_PRUEFUNG_20261114.md`. Noch kein neuer Importcode und keine WordPress-Änderung.

**W9:** Nach lokalem PHP-/Mock-Test liegt `../PLUGINS/WASSERTECHNIK_KATEGORIE_WORKFLOW_0.1.5_IMPORT_NUR_TEST.zip` vor (dieselbe Pluginidentität, keine neue Pluginlinie). Die vorhandenen 113 Seiten / 105 Kategorien würden ausschließlich nach ausdrücklicher Admin-Freigabe als **nicht veröffentlichte Entwürfe** angelegt, bisherige Objekte erhalten. Echter WordPress-Test, aktuelle Bestandsaufnahme und Importfreigabe weiterhin offen. Siehe `../PLUGINS/W9_IMPORT_PLUGIN_OFFLINE_ABNAHME_20261114.md`.

## W11 (14.11.2026) – Gesamtumstellung auf 7 Hauptbereiche vorbereitet, NICHT live
W10-Korrektur in WT001 0.1.7 als Test-ZIP im Chat: 7 Reiter sofort (zunächst die unveränderten WP-Pfade), danach nur auf separate Adminfreigabe 2 bestehende WP-Seitenhierarchien verschieben. Im freigegebenen Fall `bewaesserung` unter `brunnen` und `wassertanks` unter `regenwasser`; 17 Seiten bekommen neue Pfade, für die alten Pfade sind 301-Redirects vorgesehen, alle 113 Seiten-/105 Kategorie-Owner bleiben. Lokaler WP-Vollbestand-Mock + Fehlerpfade PASS, realer WordPress-Bestand / Redirect nicht getestet. Quelle `../PLUGINS/W11_WT001_017_SIEBEN_HAUPTBEREICHE_QA_20261114.md`. **Keine WP-Schreibaktion erfolgt.**


## W34 – 16.11.2026: historischer WordPress-Export geprüft; aktuelle öffentliche REST-Schnittstelle liefert HTML
Original-Snapshot 14.11.2026: **2 Seiten (1 veröffentlicht, 1 Entwurf), 1 Beitrag, 1 Kategorie**, keine der 218 W6-Owner im damaligen WP-Bestand; 113 geplante Seiten und 105 Kategorien vollständig und ohne Namenskollision mit diesem historischen Export. Aktueller GitHub-Actions-GET auf die Website lieferte für die WP-REST-Abfrage **HTTP 200, HTML statt JSON**: **kein aktueller Live-WP-Gesamtbestand belegbar**. Nicht behaupten, aktuelle Wassertechnik-Seiten seien leer! Damit künftig **keine weiteren Nutzerdateien** notwendig sind: im **vorhandenen WT001-Offline-Gesamtbau** eine schreibfreie WordPress-Admin-Gesamtlesung `../PLUGINS/QUELLCODE/W34_class-wassertechnik-inventory-readback.php` integriert; auf archivierten 2/1/1-Daten und Konfliktfällen getestet. 218er-Altimport weiterhin deaktiviert (9 statt W27 7 Hauptbereiche); **0 WP-Schreib- und API-Anfragen**. GitHub-W33-/W34-Prüfläufe PASS; **kein installierbares Update** und kein WordPress-Livetest. Beleg `../PRUEFUNG/W34_WORDPRESS_EINMALABGLEICH_20261116.md`, Workflow `.github/workflows/wassertechnik-w34-wp-inventory.yml`, PR #811.
