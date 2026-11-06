# Hab & Bewahr – Chatwechsel-Wegweiser 06.11.2026
**Nur Übergabeinformation, keine zweite Current-Autorität.** Der vollständige 12-teilige Chatende-Bericht wurde in diesem Chat als `HAB_UND_BEWAHR_CHATUEBERGABE_2026-11-06.md` ausgegeben. **Keine Bibliothek benutzt.**

## Verbindlicher Einstieg
Offizielles Repo: `hallo-netizen/affiliate-pferdeportal`, offizieller Branch: `hobbyroom/project-memory-campus-v1-20260905`.
`protocol/PROJECT_MEMORY/PROJEKTE/EIGENTUMSSCHUTZ/START_HERE.md` → `protocol/PROJECT_MEMORY/AUTORITAETSPLAN.json` → Scopes `EIGENTUMSSCHUTZ_DESIGN` und `EIGENTUMSSCHUTZ_PLUGINS` → jeweils EIN `CURRENT_STATE.md`.
Technische Current: `PLUGINS/PLUGIN_AKTEN/HAB-001-DESIGN/CURRENT.md`. Inventar: `PLUGINS/REGISTER.md`. Fehler: `DESIGN/FEHLERQUELLEN.md` und `protocol/PROJECT_MEMORY/FEHLERREGISTER.md`. Nach jeder Veränderung diese aktuellen Quellen zuerst lesen, nicht diese Übergabe als Current nutzen.

## Tatsächlicher letzter Stand
**Letzter lokal geprüfter Designplugin-Kandidat: v0.1.189**; komplettes ZIP im bisherigen Chatcontainer: `/mnt/data/HAB_UND_BEWAHR_DESIGN_0.1.189_BEITRAGSFEINSCHLIFF.zip`, identisch zur Kurzfassung `Hab_Bewahr_Design_0189.zip`; 84.349.647 Byte, 430 Einträge, SHA-256 `947a950273edb6bf47e76ffeef67ff51425db620adc2650c742831e73093134c`. Kein langfristiger Containerzugriff garantiert. WordPress-Liveinstallation unbekannt und NICHT getestet. Bestehende originale Pluginidentität: `hab-bewahr-design-vorschau/`.

Entwicklung 0.1.185–0.1.189: normaler Artikel statt Demo-only, Yoast-Datumsunterdrückung, zwei Spalten mit Foto und Platz für Affiliateprodukte/Banner, keine öffentlichen Fake-Angebote, Quellen nur aus Frontend ausgeblendet, mobile Produktgruppe vor zweitem Fachabschnitt und Banner später, überflüssiges Inhaltsverzeichnis und redundante „Ratgeber“-/Kategorietitel entfernt, dezente H2-Striche und differenzierte Listen sowie gleiche Abstände. Regel: Ein Design für alle Beitragsarten; Textinhalt/Länge/SEO/Links später separat. K0 und andere Projektplugins nie geändert.

**Lokale Tests:** ZIP-CRC PASS, 35/35 PHP-Syntax PASS, JS-Syntax PASS, WordPress-Mock mit Admin/öffentlich und real simuliertem Affiliate-HTML PASS, Schadensfall-Negativtest PASS, Browser-Layout 1440/768/390/1440 ohne Überläufe oder doppelte Werbeelemente PASS. Kein echter WordPress-Live-, Provider- oder Campus-0.1.189-Readback.

## Offizielle Pluginablage (frisch durch GitHub-Verzeichnis überprüft)
- `HAB-001-DESIGN/CURRENT.zip` **offiziell 0.1.184**, 84.339.643 B, SHA-256 `76043e5c093058a4d8aff8fd6642307cade951c8267641dc710b8ed70cd323e3` (PR #625 gemergt).
- `HAB-002-KATEGORIE-WORKFLOW/CURRENT.zip` **1.14.8.37**, 368.530 B, SHA-256 `ec39080e5350b9f7b3924239376e11580ce7de195a60bb89feafae6152533f98` (PR #622 gemergt).
- `HAB-003-BILDZENTRALE/CURRENT.zip` **1.0.0**, 70.397 B, SHA-256 `58af0d394752e767b5f0c7d6d9901eeaec921331ab6245144859e3e6626e4559` (PR #622 gemergt).
Alte Original-ZIPs unverändert aufbewahrt. Neueste 0.1.189 **noch nicht** als vollständiges offizielles `CURRENT.zip` gesichert/erneut abgerufen; Stand darum **PLUGINABLAGE: BLOCKED**.

## Fehler/Blocker/Genau eine NEXT ACTION
Fehler aus der Beitragsentwicklung sind lokal korrigiert, jedoch nicht WordPress-live bestätigt. Die 45 historischen offenen Foto-Meldungen bleiben separat im Design-Current. PR #633 für einen reinen Entwicklungsbeleg **ist nicht gemergt**: GitHub-Actions-Lauf `42215777312`, Job `hardlock-base`, ruft `control/paul-scope-gate/paul_scope_gate.py verify-pr` auf, obwohl diese Datei im Prüflauf fehlt; Exit-Code 2. Eine vorherige Merge-Anfrage meldete erforderlichen Check `single-current-lock` offen. Dies ist ein **CI-Schutzpfadproblem**, kein Beweis eines Plugin-Lauffehlers. Weder Sicherheitsprüfung umgehen noch Protected-Branch-Current direkt überschreiben.

**GENAU EINE NEXT ACTION:** Über den autorisierten GitHub-/Campus-Wartungsweg die fehlende Pflichtprüfdatei `control/paul-scope-gate/paul_scope_gate.py` wiederherstellen und den geschützten PR-Freigabeweg wieder funktionsfähig machen. Erst danach das vollständige 0.1.189-Paket im offiziellen Hab-Pluginbüro sichern und unabhängig readback-verifizieren.

**Schutz:** Kein zweites Designplugin, keine neue Bibliothek/Current, keine Änderungen an K0, HivePress, WordPress-Core, bestehenden Kategorien/IDs/Slugs, anderen Portalen oder bisherigen Rollbacks.
