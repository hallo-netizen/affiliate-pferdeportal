#!/usr/bin/env python3
"""Archive ONLY after full HD009 PHP & ZIP regression tests have succeeded."""
from pathlib import Path
import hashlib, os, shutil

root = Path("protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH")
office = root/"PLUGINS/ISOLIERTE_PLUGINS/HD-009-AFFILIATE-ZENTRALE"
src = Path("/tmp/HOBBY_DEPOT_AFFILIATE_HD009_0.1.33_DIRECT_IDEALO.zip")
digest = hashlib.sha256(src.read_bytes()).hexdigest()
assert (office/"HOBBY_DEPOT_AFFILIATE_HD009_0.1.32.zip").exists()
assert hashlib.sha256((office/"HOBBY_DEPOT_AFFILIATE_HD009_0.1.32.zip").read_bytes()).hexdigest() == "d433db74b493407a4c26faef591574e644201846078b7aa7aa3541126f9359b8"
for path in [office/"CURRENT.zip",office/"HOBBY_DEPOT_AFFILIATE_HD009_0.1.33.zip"]:
    shutil.copy2(src,path)
    assert hashlib.sha256(path.read_bytes()).hexdigest()==digest

run=os.environ["GITHUB_RUN_ID"]
tag="hobby-hd009-0.1.33-idealo-direct-20261112"
report="""# HD009 0.1.33 – direkter idealo-Feedimport
Datum: 12.11.2026. Ziel ausschließlich Hobby Depot, HD009.

## Beweis – Warum?
Die bereits aktivierte iPN-API Hobby Depot 568912 / Feed 2747 meldet PASS und Produkte, aber
der vorhandene HD009-Import, der Button und die 12h-Automatik verlangten zusätzlich eine
manuelle Download-URL. Staged 0, Materialisiert 0. Screenshot im Auftrag 12.11.2026.

## Was wurde geändert?
Exakt 2 Dateien des aus dem vollständigen unveränderten HD009 CURRENT 0.1.32 geprüften ZIP:
- includes/trait-ppar-idealo.php: Wenn bestehende API-Verbindung für die eigene Hobby-Adspace
  geprüft, Export aus bestehenden Zugangsdaten serverseitig über
  api.ingenious.cloud/creatives/productdata/export mit CSV+GZIP; bisherige manuelle URL
  bleibt optional; bestehender Download-Worker, Parser, Staging, Zielzuordnung,
  GTIN, Materialisierung, Berechtigungs- und Veröffentlichungsprüfung bleiben identisch.
- hobby-depot-affiliate-router.php: Header/Versionsstand 0.1.33.

Keine zweite Affiliate-Zentrale, kein Core, keine zusätzlichen Tabellen, kein Frontend-HTTP,
keine Fremdportal-Version übernommen. Weder eBay noch Amazon/DataForSEO verändert.
Kein öffentliches Idealo vor Abschluss des tatsächlichen Imports und bewusster Freigabe.

## Prüfvertrag
Quellbasis SHA-256: d433db74b493407a4c26faef591574e644201846078b7aa7aa3541126f9359b8
Neues ZIP SHA-256: %s
41 Originaldateien, 41 Dateien vollständig CRC-PASS, alle PHP-Dateien Syntax-PASS.
Original Importer, Materialisierung, GTIN-Sperren, Provider-Prüfung und
Hintergrundworker-Methode unverändert (method-by-method geprüft).
Echte PHP-Funktionstests gegen Originalmethoden mit synthetischem Test-API-Key:
own adspace/Feed, falscher Adspace, nicht geprüft, deaktiviert, fehlender Key,
GZIP-Download, JSON-Status, HTTP 429, Doppelstart-Sperre, optionale alte URL.
Runner: https://github.com/hallo-netizen/affiliate-pferdeportal/actions/runs/%s

## Live-Status und Next Step
Kein echter privater WordPress-/iPN-Feed-Import in GitHub durchführbar.
Nach Installation: Affiliate-Zentrale → Anbieter & APIs → idealo:
Feed jetzt aktualisieren, nach Abschluss Staged/PASS/Materialisiert/Ziele kontrollieren.
Erst dann Ausgabe von bisher ebay_only auf freigegebenen Modus einstellen,
Frontend auf richtige Produkte, Bilder, Zuordnung, Tracking überprüfen.
Release: https://github.com/hallo-netizen/affiliate-pferdeportal/releases/tag/%s
"""%(digest,run,tag)
(root/"AFFILIATE/HD009_DIRECT_IDEALO_EXPORT_0.1.33_20261112.md").write_text(report)
for path in [office/"MANIFEST.md",root/"PLUGINS/PLUGIN_AKTEN/HD-009-AFFILIATE-ZENTRALE/CURRENT.md"]:
    old=path.read_text()
    header=("# HD009 AKTUELL: 0.1.33 – direkter iPN-Export\n\n"
        "Vollständiges geprüftes CURRENT.zip und HOBBY_DEPOT_AFFILIATE_HD009_0.1.33.zip. "
        "SHA256: "+digest+". Unverändertes 0.1.32 als Sicherung.\n"
        "Nur unnötigen URL-Zwang des bestehenden Imports beseitigt. "
        "Keine ungeprüfte Freigabe am öffentlichen Frontend.\n"
        "Vollbeleg: AFFILIATE/HD009_DIRECT_IDEALO_EXPORT_0.1.33_20261112.md; "
        "Run "+run+".\n\n"
        "---\n\n## ARCHIV: bisheriges 0.1.32\n\n")
    path.write_text(header+old)
print("SAVED_HD009_0133",src.stat().st_size,digest,"OLD_0132_ARCHIVED")
