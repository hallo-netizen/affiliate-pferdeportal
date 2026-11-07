#!/usr/bin/env python3
"""Promote only a fully tested RC11 Hab Affiliate installer into its ONE office CURRENT."""
from pathlib import Path
from hashlib import sha256
from zipfile import ZipFile
import sys,os
assert len(sys.argv)==2
candidate=Path(sys.argv[1])
root=Path("protocol/PROJECT_MEMORY/PROJEKTE/EIGENTUMSSCHUTZ")
rel="PLUGINS/ISOLIERTE_PLUGINS/HAB-004-AFFILIATE/CURRENT.zip"
target=root/rel
baseline="f3b6b0ac4fd05310fa32ce68e2715b29d022003ac68f32ceb051443832364ced"
assert sha256(target.read_bytes()).hexdigest()==baseline,"Unexpected original HAB current: STOP"
data=candidate.read_bytes()
digest=sha256(data).hexdigest()
with ZipFile(candidate) as z:
    assert len(z.namelist())==28 and z.testzip() is None
    info=z.read("affiliate-portal-router/affiliate-portal-router.php").decode("utf8")
    assert "0.1.8-rc11" in info
    assert all(not name.startswith("../") for name in z.namelist())
assert len(data)>600000 and len(data)<700000
target.write_bytes(data)
assert target.read_bytes()==data
heading=f"""## 07.11.2026 – HAB-004 0.1.8-rc11 – EINZIGER AKTUELLER STAND

**Installations-ZIP:** `{rel}`; **{len(data):,} Bytes**, **SHA-256:** `{digest}`; 28 ursprüngliche Dateien, davon **24 gegenüber RC10 unverändert**. WordPress-Pluginordner bleibt `affiliate-portal-router/`. Vorgänger RC10 ist nur noch über Git-Historie, kein zweites CURRENT.

**Ursache beseitigt (Quell- und offline simulierte Frontend-Ausgabe):** HAB-001 reicht echte WordPress-Kategorien an den bestehenden Filter weiter; HAB-004 wies bislang alle Kategorien ab. RC11 verbindet **nur den vorhandenen Kategorie-Anschluss** mit `provide_leaf_category_affiliate_slot_html`, priorisiert die unveränderte Kampagnenauswahl und zeigt bereits gespeicherte, fachlich passende DataForSEO-Amazon-ASINs als **einzelne Produktkarten** mit dem ursprünglichen `render_banner`. R3-Themenseiten erhalten ebenfalls einzelne Karten statt zusammengeklebter Textlinks. **Ohne gespeicherte gültige ASIN kein leeres/erfundenes Produktangebot.** Keine falschen Bilder, Preise oder Verfügbarkeit.

**Abnahme:** Original-RC10-Fehler reproduziert; vollständiges HAB-004-RC11 samt tatsächlichem HAB-001-Designaufruf offline getestet. Kategorie „Wassermelder“ und R3 „Leckwarnung & Absperrung“ jeweils zwei getrennte geprüfte Amazon-Testlinks mit Hab-Tracking-ID, gebuchte Anzeigen haben Vorrang, Hauptschalter AUS respektiert, unbekannte/produktlose Kategorien bleiben leer. **18 getrennte PHP-Regressionstests, 34 PHP-Syntaxprüfungen (einschließlich Prüfscripten), 28/28 ZIP-CRC, alle erfolgreich.** Testnachweis `AFFILIATE/IMPLEMENTIERUNG_RC11/PRUEFBERICHT.md`. Pferdeatelier 6.72, Hobbydepot HD009 0.1.19 und HAB-001/002/003 nicht geändert. Kein weiterer bezahlter DataForSEO-Auftrag.

**Noch nicht live abgenommen:** RC11 muss als **Update des bestehenden HAB-004** in WordPress installiert werden; dann die vorhandene Kategorie „Wassermelder“ und R3 „Leckwarnung & Absperrung“ im Frontend prüfen. Hauptschalter der Affiliate-Zentrale muss eingeschaltet sein. Die separate serverseitige WP-Cron-Ursache ist nicht hiermit repariert. **Keinen neuen kostenpflichtigen Suchlauf anstoßen**; gespeicherte ASINs genügen zum Test.

---

"""
files=[
"PLUGINS/ISOLIERTE_PLUGINS/HAB-004-AFFILIATE/MANIFEST.md",
"PLUGINS/CURRENT_STATE.md",
"PLUGINS/PLUGIN_AKTEN/HAB-004-AFFILIATE/CURRENT.md",
"AFFILIATE/CURRENT_STATE.md",
]
for relative in files:
    f=root/relative
    old=f.read_text()
    assert "HAB-004 RC10" in old[:2000] and "f3b6b0ac4fd05310" in old[:2600], f"Office changed: {f}"
    new=heading+old
    f.write_text(new)
    print("UPDATED OFFICE",relative)
original_check=root/"AFFILIATE/PRUEFUNG_BESTEHENDE_AUSGABE_20261107.md"
old=original_check.read_text()
assert "LESENDE CODEPRÜFUNG" in old
original_check.write_text(
    "# Abschluss der bisherigen Prüfung: RC11 seit 07.11.2026 im Pluginbüro als CURRENT; Tests bestanden. Die folgende Prüfung dokumentiert den **vorherigen RC10-Ausgangszustand**. Die RC11-Liveabnahme in WordPress ist weiterhin offen.\n\n---\n\n"+old)
report=root/"AFFILIATE/IMPLEMENTIERUNG_RC11/PRUEFBERICHT.md"
report.write_text(f"""# HAB-004 RC11 – abgeschlossene Ursachenprüfung und gesicherte Installations-ZIP

- Version 0.1.8-rc11, {len(data)} Bytes, SHA-256 `{digest}`.
- Verifiziertes Ausgangs-ZIP RC10: SHA-256 `{baseline}`.
- Keine neuen Plugins, Hooks, Datenbanken, Imports, Worker oder bezahlten Provider-Aufträge. Nur bestehendes HAB-004.
- Vollständige aktuellen Original-ZIPs von Pferdeatelier, Hobbydepot HD009 0.1.19, HAB-004 RC10 und HAB-001-Design vor Korrektur untersucht.
- Verbindlich festgestellte Ursache: HAB-001 filtert mit Kategorie-Knoten, HAB-004s `area()` akzeptierte nur `page`; RC10 R3-Amazon-Fallback verkettete ASINs mit ` · `.
- In RC11: bestehender `provide_leaf_category_affiliate_slot_html` leitet die verifizierte WP-Term-ID zu `render_affiliate_slot_for_context` weiter; bestehende Kampagnenvorwahl unverändert. Nur bei leerer Werbekampagne zeigen drei originale Produktplätze je EINEN verifizierten Amazon-Treffer über den bisherigen `render_banner`.
- R3: bisherige `hb_amazon_area_product_fallback` befüllt bis zu drei vorhandene `category_product_[1-3]`-Plätze mit jeweils einem einzelnen tatsächlich gespeicherten ASIN-Titel/Trackinglink, keine gekoppelten Textzeilen. Fehlende ASIN: kein Produktkartenersatz.
- Baseline mit tatsächlichem RC10-Code und HAB-001-Hook reproduziert: Wassermelder leer, R3-Treffer als Textzeile.
- RC11 in vollständigem ursprünglichem Plugin/HAB-001-Design-Filterlauf geprüft: zwei getrennte `data-ppar-category-product-card`-Karten auf Kategorie und R3, echte gespeicherte ASINs, `habundbewahr-21`, keine gefälschten Bilder/Preise.
- Vorrang einer eingebuchten Anzeige, zentrale Abschaltung, fremde unbekannte Kategorie, keine ASIN und kostenfreies Rendern: PASS.
- Bestehende RC10-Szenarien (inklusive Cron/Provider/Beitragsfreigabe) und die RC5-/RC6-/RC7-/Amazon-Regressionsskripte: **18 getrennte PHP-Prozesse PASS**; **34 PHP-Syntaxprüfungen PASS**; **28/28 ZIP-Dateien CRC PASS**.
- ÄNDERUNGEN: `includes/class-ppar-hab-bewahr-bridge.php` (Kategorie anschließen), `includes/trait-ppar-hb-amazon.php` (ASIN-Karten über Originalrenderer), `affiliate-portal-router.php` und `readme.txt` (nur Versionsnummer). Übrige 24 Plugindateien bytegleich.
- RELEASE: nur `PLUGINS/ISOLIERTE_PLUGINS/HAB-004-AFFILIATE/CURRENT.zip` aktualisiert; alle vier aktuellen Plugin-Akten konsistent aktualisiert. Ursprüngliches ZIP in der Git-Historie.
- Sicherer offener Livepunkt: WordPress-Pluginupdate und öffentliche Sichtprüfung; kein echter IONOS-WordPress-/DataForSEO-Livetest und keine serverseitige Cron-Reparatur behauptet. **Kein neuer DataForSEO-POST für die bereits gespeicherten Produktdaten nötig.**
""")
print("RELEASE SUCCESS",len(data),digest,flush=True)
