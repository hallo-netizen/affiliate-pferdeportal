# Affiliate-Zentrale 6.72.210 — Textlink-Partnercode Rootfix

Status: PASS / EXACT INSTALLER READY

## Anlass
Ein realer Affiliate-Textlink wurde als vollständiger Partnercode geliefert: Anchor + unsichtbares Tracking-Bild. 6.72.209 akzeptierte im Backend ausschließlich eine URL und konnte diesen Code daher nicht vollständig speichern.

## Umgesetzter KISS-Fix
- allgemeingültig, kein PETPROTECT-/LeadAlliance-Sonderpfad;
- bestehender einfacher Modus Linktext + Tracking-URL bleibt kompatibel;
- neuer alternativer Modus: vollständiger vertrauenswürdiger Original-Partnercode;
- vollständiger Partnercode hat bei der Ausgabe Vorrang;
- derselbe stabile `[affiliate_textlink id="..."]`-Platzhalter;
- gleiche nicht-autoloadende Option und gleicher Request-Cache;
- keine neue Tabelle, kein Cron, kein Provideradapter und kein serverseitiger Frontend-HTTP;
- Partnercode wird nur durch `manage_options` + Nonce gepflegt und bewusst unverändert ausgegeben, analog zum bestehenden Tarifrechner-Code.

## Ausgeführter Test
GitHub Actions Run: 37787914399

Resultat:
- WordPress + MariaDB: PASS
- PHP-Syntax: PASS
- bestehende URL-Textlinks: PASS
- vollständiger Partnercode ohne URL-Zwang: PASS
- PETPROTECT-Beispielcode exakt ausgegeben: PASS
- Click-URL `tc.php?...&cons=`: PASS
- eingebettetes Tracking-Pixel `tb.php?...T`: PASS
- Backend-Feld `textlink_partner_html`: PASS
- inaktiv/unbekannt: PASS
- Tarifrechner unverändert: PASS
- keine neue DB-Tabelle: PASS
- DB-Housekeeping Positiv/Negativ: PASS
- Gesamter ausführbarer Gate: **59/59 PASS**
- ZIP-Byte-Identität gegen 28-Dateien-Manifest: PASS 28/28

## Bindungen
- Source manifest SHA256: `8b3552ff93d482525e41bd0d279a609d8dd538bf672313ba29574a07f33992bf`
- getestete ZIP: `AFFILIATE_ZENTRALE_6.72.210.zip`
- ZIP SHA256: `43ca6033a0f8dc929f777fc6580f2b41dfd711c6f561db99658f402cc5af88a1`
- ZIP Bytes: `811373`
- Workflow Artifact ID: `11554788092`

Keine Plugin-Source-Änderung nach diesem PASS.
