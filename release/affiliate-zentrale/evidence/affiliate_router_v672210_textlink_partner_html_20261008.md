# Affiliate-Zentrale 6.72.210 — Textlink-Partnercode Rootfix

Status: CANDIDATE / GATE PENDING

## Anlass
Ein realer Affiliate-Textlink wurde als vollständiger Partnercode geliefert: Anchor + unsichtbares Tracking-Bild. 6.72.209 akzeptierte im Backend ausschließlich eine URL und konnte diesen Code daher nicht vollständig speichern.

## Gebundener Fix
- allgemeingültig, kein PETPROTECT-/LeadAlliance-Sonderpfad;
- bestehender einfacher Modus Linktext + Tracking-URL bleibt kompatibel;
- neuer alternativer Modus: vollständiger vertrauenswürdiger Original-Partnercode;
- vollständiger Partnercode hat bei der Ausgabe Vorrang;
- derselbe stabile `[affiliate_textlink id="..."]`-Platzhalter;
- gleiche nicht-autoloadende Option und gleicher Request-Cache;
- keine neue Tabelle, kein Cron, kein Provideradapter, kein serverseitiger Frontend-HTTP;
- Partnercode wird nur durch `manage_options` + Nonce gepflegt und bewusst unverändert ausgegeben, analog zum bestehenden Tarifrechner-Code.

Source manifest SHA256: `8b3552ff93d482525e41bd0d279a609d8dd538bf672313ba29574a07f33992bf`

Gate: PENDING.
