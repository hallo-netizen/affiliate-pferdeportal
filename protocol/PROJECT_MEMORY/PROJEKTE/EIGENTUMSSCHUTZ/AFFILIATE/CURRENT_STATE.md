## 07.11.2026 – AMAZON-/EBAY-EINRICHTUNGSSTAND (AKTUELLE OPERATIVE FORTSETZUNG)

**Verbindlicher Gesprächs-/Kontostand:** [SETUP_EBAY_AMAZON_BANNER_20261107.md](SETUP_EBAY_AMAZON_BANNER_20261107.md). Amazon-Tracking-ID für Hab & Bewahr laut Nutzer **bereits angelegt**; Website-Liste und Anbindung im WP-Plugin noch zu prüfen. Amazon im Plugin „Adapter vorbereitet“, nicht live verbunden. Eigene breite/quadratische Banner sind Designentwürfe, noch keine Produktions-/Amazon-Freigabe. eBay: eigene Hab-EPN-Kampagne im Plugin gespeichert; Zusatz-Keysets für Hobby Depot und Hab & Bewahr beantragt, Ticket 261106-000039, eBay-Rückfrage zur Begründung, Antwortversand noch unbestätigt. **Pferdeatelier-/Hobbydepot-Developer-Einstellungen und Plugins nicht verändern.**

**NEXT ACTION:** Amazon PartnerNet → Kontoeinstellungen → Website-Liste bearbeiten: `hab-und-bewahr.de` auf Vorhandensein prüfen. Tracking-ID nicht noch einmal erstellen; danach einen Testlink ausschließlich mit Hab-Tracking-ID erzeugen. Keine automatische Auslieferung einschalten. Der folgende RC3-Stand bleibt die autoritative Plugin-Basis.

---

## 06.11.2026 – RC3 BEREINIGUNG / OFFIZIELLE HAB-004-PLUGINABLAGE

**Neue gültige Version:** 0.1.0-rc3, vollständige ZIP im ursprünglichen `../PLUGINS/ISOLIERTE_PLUGINS/HAB-004-AFFILIATE/CURRENT.zip` (605.196 Bytes; SHA-256 `2e5f6790ab3a64b446e34d132037684ad8fa637f76f43974e2816a1f75bc11eb`). RC2 unten ist nur Historie.

**Ursache und Korrektur:** Die RC2-Produktlistenprüfung bezog sich ausschließlich auf Produktbegriffe in Seitenüberschriften. Der tatsächliche Design-Kategoriebaum liegt in der bestehenden WordPress-Zielrevision mit 6 Schutzwelten. In RC3 werden 285 Artikelkategorien und 13 klar benannte Produktprofile aus dem offiziellen Design-Nodes-Stand erkannt; nicht pauschal jedes Sicherheitsthema als Produkt deklariert. Die Werbung nutzt die echten gemappten WP-Zielseiten, nie die Pferde- oder Hobby-Quellkataloge. Welt-/Unterbereich-/Magazin-/Anzeigenmarkt- und Artikel-Brücken nach tatsächlichen Designfiltern, 92 reale Boot-Hooks, 24/27 Dateien gegenüber RC2 unverändert, keine Funktionen aus neutraler Engine gelöscht.

**Performance mit Beleg:** Einmaliger, pro Seitenaufruf zwischengespeicherter WP-Seitenindex ersetzt wiederholtes Durchsuchen des gesamten Zielbaums. Keine unbelegte globale Laufzeitverbesserung behauptet. ZIP-Bau zweimal identisch, alle PHP/JS-Tests, 546 Design-Knoten als Testkorpus, negative und positive Tests, SHA + unabhängiger GitHub-Readback PASS (GitHub Run 42252394077).

**Restgrenzen:** noch kein echter WordPress-/Provider-Livetest; eBay-Quellstand 6.72.306 als 66-Datei-Referenz nicht physisch im Hab-Büro, daher keine zugesagte vollständige Parität; Glossar-Einzelseiten ohne echte CPT-Zielbindung bleiben sicher leer statt erfundene Werbung zu zeigen. Automatische Affiliate-Ausgabe standardmäßig inaktiv.

---

## 06.11.2026 – HAB-004 AFFILIATE – ISOLIERTER WORDPRESS-RELEASE 0.1.0-rc2
<!-- HAB_AFFILIATE_RC2_20261106 -->
**Neue Ausgabe im zuständigen eigenen Pluginbüro:** `../PLUGINS/ISOLIERTE_PLUGINS/HAB-004-AFFILIATE/CURRENT.zip`, 27 Dateien, 603.323 Bytes, SHA-256 `014e42b9657eed74b4d2e1f29ea51c6c6bf5c276ec30402011289b3821cbe153`. Build und Prüfquellen ausschließlich auf isoliertem Zweig `hbd-affiliate-port-20261106` in `AFFILIATE/HAB_BAU`; unveränderter fachlicher Originalstamm `NEUTRAL_STAMM` bleibt erhalten.

**Belegt:** Vollständiger neutraler 26-Dateien-Grundstock mit eBay, idealo, Awin, ADCELL, Digistore24, Tarifen, Werbebannern, manuellen Kampagnen, Affiliate-Automatisierung, Chefsteuerung, Ausgabeobjekten, Produktkarte und Artikelplanung erhalten. PHP-Signaturen der 26 Originaldateien nicht entfernt. Fünf vorhandene Zusatzmodule (Produkt-Source-Plan, Admin KISS, Deal-Radar, Partneranalytik, DS24-Nachverarbeitung) waren in neutraler Quelle nicht am Bootstrap angebunden; im neuen Paket geprüft gestartet. Alle Horse-/Hobby-Designreferenzen aus Installationscode entfernt; Hab-Adapter liest nur aktive, passende WordPress-Revision aus Kategorie-Workflow. Anbindung an HBDP-Artikel-/Bereichsfilter (Design 0.1.189) und fail-closed ohne Kategorievertrag. 27/27 ZIP CRC, alle PHP-Lints, JS Syntax, echte Start-Hooks (90), Positiv-/Negativkatalogtests sowie unabhängig über frischen GitHub-Klon erneut gelesene ZIP: **LOCAL PASS** (GitHub-Run 42246580133).

**Harte Grenzen:** Vollständiges Pferdeatelier 6.72.306 Paket mit 66 Files / 5.343.938 Bytes ist lediglich als Referenz beschrieben und befindet sich nicht als Vollarchiv im Hab-Büro. Deshalb **keine behauptete volle Versions-/Featuregleichheit zu 6.72.306**; belegt ist die neutrale Stammfunktions-Erhaltung. Kein realer WordPress-/Provider-/eBay-API-/HivePress-Livetest und keine Lastmessung im Live-Hosting. Kein belegter genereller Performancefehler, daher keine blind gelöschten Alt- oder Sicherungsfunktionen. Standardeinstellung Auslieferung deaktiviert. Der neue Hab-Katalog benötigt aktive WP-Kategorien, echte veröffentlichte Produktziele und kann andernfalls leer bleiben.

**NEXT ACTION (einziger freigegebener operativer Schritt):** Hab-Plugin als neue, bereits separat benannte Instanz unter `affiliate-portal-router` auf Hab-&-Bewahr-WordPress kontrolliert installieren, aktivieren, im Backend Ist-Zustand/Partner-Sperre prüfen. Erst nach klarem WordPress-Readback Providerdaten neu für Hab & Bewahr hinterlegen und Tests durchführen. K0 und alle anderen Projekte unverändert.

---

# HAB & BEWAHR – AFFILIATE CURRENT

STAND: 2026-10-26
STATUS: NEUTRALER STAMM GESICHERT / NO LIVE PASS / HAB-&-BEWAHR-ANPASSUNG NOCH OFFEN

## Verbindlicher Stand

Für Hab & Bewahr wurde ein eigenes Affiliate-Büro angelegt.

Gesicherte technische Ausgangsbasis:
`NEUTRAL_STAMM/affiliate-portal-router/`

Der Stamm basiert auf der bereits pferdeatelier-bereinigten HD-009-Engine, wurde aber vor Ablage hier zusätzlich von Hobby-Depot-spezifischer Bindung getrennt.

Entfernt bzw. neutralisiert wurden insbesondere:
- Hobby-Depot-Pluginidentität und Routerklassenbindung
- HD-004-Kategorie-/Zielquellenbindung
- HD-003/Hobby-Depot-Designprofilbindung
- fest verdrahtete Hobby-Depot-Slotmatrix
- Hobby-Depot-spezifische eBay-/idealo-Zieltexte, Defaults und Zielquellenklassen
- Hobby-Depot-spezifische Provider-/Deal-Radar-Bezeichnungen

Erhalten wurden:
- allgemeine Affiliate-Engine
- eBay- und idealo-Providerlogik
- Awin / ADCELL / Digistore24 / Direktpartner-Basis
- Kontroll-, Veto-, Output- und Automationslogik
- bestehende Credential-/Konfigurationsschnittstellen

Zugangsdaten sind nicht im Campus gespeichert.

## Wichtig

Der neutrale Stamm ist **keine installierbare Hab-&-Bewahr-Livefreigabe**.
Die Portal-Zielquelle ist absichtlich ungebunden und fail-closed.

## Herkunft

Hobby-Depot-Arbeitsquelle:
`hobbyrausch/hd009-affiliate-port-20261026`
Head bei Ableitung:
`56b91b171cb68129369b67e411da5345957af4f2`

Die Hobby-Depot-Entwicklung bleibt davon getrennt und wird nicht zurückgesetzt.

## NEXT ACTION

Für den späteren Hab-&-Bewahr-Chat:

1. Hab-&-Bewahr-Zielquelle aus dem zuständigen Kategorie-/Portal-Current anbinden.
2. Hab-&-Bewahr-Design-/Slotvertrag separat anbinden.
3. Portalnamen und projektspezifische Defaults setzen.
4. Positiv-, Negativ-, Regression-, Installations- und Runtimeprüfung durchführen.
5. Erst danach einen Hab-&-Bewahr-Installationskandidaten bauen.

Nicht HD-004 übernehmen. Nicht Hobby-Depot-Slotmatrix übernehmen. Nicht wieder aus Pferdeatelier kopieren.
