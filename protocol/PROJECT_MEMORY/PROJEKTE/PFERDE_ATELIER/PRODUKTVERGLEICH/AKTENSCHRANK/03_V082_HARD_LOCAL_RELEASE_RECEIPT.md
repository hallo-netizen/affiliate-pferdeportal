# PRODUKTVERGLEICH 0.8.2 – HARD LOCAL RELEASE RECEIPT

Stand: 2026-09-09
Status: LOCAL + FINAL-FRESH-ZIP HARD PASS / WORDPRESS-LIVE-RETEST OFFEN

Artefakt:
`universal-product-comparison-0.8.2-prototype.zip`

SHA-256:
`6f0f1f8d62870fd2cd1ee34010c1b157d9ac140327e46cd8a6d0b48a1a05f2ad`

## Anlass

Kosten-Hard-Rule:
Bereits bezahlte Produkt-/Paar-Zwischenergebnisse dürfen bei Wiederholung nicht unnötig erneut gekauft werden.

Autoritativer PSTE-0.56.25-Befund:
nativer DataForSEO-Cache default `86400` Sekunden.

## KISS-Fix

Nur vorhandenen PSTE-Bridge-Weg erweitert:
`persistente UPC-Zwischenevidenz -> PSTE Cache -> fehlender Provider-Endpunkt`.

Persistiert werden:
- Produktprobe;
- Paarprobe;
- PARTIAL nach jedem erfolgreich erhaltenen Endpunkt;
- COMPLETE positiv oder negativ;
- Response-Hash;
- Bindungs-Hash;
- Provider/PSTE-Version;
- Umgebung;
- Land;
- Sprache;
- Gültigkeit 90 Tage.

Keine neue Architektur, kein zweiter SEO-Providerweg.

## Harte Prüfung

Exakte Abhängigkeiten:
- UPK 0.5.0 SHA `80218ec721631353d62a7e3058e76d9c4a4829802c4d5c6bd6f1f2014b6879e3`
- PSTE 0.56.25 SHA `8122e3fa2273fe4d8e53476f557ed0ddd99a197e8b1c40302f35db245ebb0f95`

Finale ZIP:
- 20/20 Tests PASS;
- PHP-Lint 40/40 PASS;
- Source↔ZIP 51/51;
- Report-Hashbindung 50/50;
- reale PSTE-Themenmap PASS;
- Same-Brand/Profile/Null-/Einprodukt-Nachfrage/PARTIAL/Stale/Dossier-Drift Negativtests PASS;
- kompletter bestehender Workflow weiterhin PASS.

Neue Positivtests:
- gleicher Befund erneut -> 0 Provider;
- gleiches Produkt in neuem Paar -> keine neue Produktabfrage;
- Teil-Lauf abgebrochen -> vorhandener Endpoint wiederverwendet;
- persistente Evidenz reduziert Kostenprognose.

Neue Negativtests:
- abgelaufen -> frische Abfrage;
- Kontextdrift -> frische Abfrage;
- manipuliert -> BLOCK ohne stilles Nachkaufen;
- Persistenzfehler -> kein falsches PASS.

Unabhängige Mutationen:
- Load entfernt -> Test ROT;
- PARTIAL-Speicherung entfernt -> Test ROT;
- Integritätsguard entfernt -> Test ROT.

## Grenze

Lokale Freigabe für WordPress-Live-Retest.
Noch kein WordPress-LIVE-PASS für 0.8.2.
Writer/Draft/Publish weiterhin außerhalb dieser Stufe.
