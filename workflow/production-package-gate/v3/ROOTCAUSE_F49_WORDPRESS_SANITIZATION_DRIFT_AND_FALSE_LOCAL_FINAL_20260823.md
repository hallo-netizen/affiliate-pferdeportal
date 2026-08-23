# F-49 – WordPress-Sanitization-Drift / falscher lokaler FINAL-Status

## Status
ROOT CAUSE IDENTIFIED / PACKAGE CORRECTED / PRELIVE PASS / LIVE REPLAY REQUIRED

## Live-Beleg
Der Serverlauf des STARTMASTER0073-Pakets erreichte PPM 6.7.9, scheiterte in der Content-Generation mit `CANONICAL_ARTICLE_WORDPRESS_SANITIZATION_DRIFT` und führte keinen WordPress-Write aus.

## Root Cause
Der lokale PPM-Test der vorherigen Etappe war nicht gleichwertig mit der echten WordPress-Sanitization. Der alte Bootstrap konnte `wp_kses_post()` als vereinfachte/identische Testfunktion behandeln. Dadurch wurde ein Byte-Drift im HTML vor dem Live-Lauf nicht erkannt.

Im Artikel existierte genau ein rohes `&` im sichtbaren Linktext `Boxen & Türen`. WordPress-KSES normalisiert ein rohes Ampersand in Post-HTML zu `&amp;`. PPM 6.7.9 verlangt vor der Generation absichtlich Bytegleichheit zwischen eingereichtem `body_html` und `wp_kses_post(body_html)`; deshalb war der Live-Block korrekt.

## Korrektur
- ausschließlich Quell-HTML: `Boxen & Türen` -> `Boxen &amp; Türen`
- gerenderter Text bleibt `Boxen & Türen`
- `body_text` unverändert
- Redaktionsplan, READY, Planplatz, Kategorie, Keyword, Titel, Fact-Pack, Tabellenwerte und Design unverändert
- hashgebundene technische Evidenzen und Supervisor-Signatur wurden wegen der geänderten HTML-Bytes neu gebunden
- kein Plugin geändert

## Systemzustand nach Fehlversuch
PPM setzt einen abgebrochenen Lauf auf `ABORTED`. Ein Lease hat laut `PPM679_Normal_Draft_Pipeline::LEASE_SECONDS` 900 Sekunden. Der Live-Fehler war am 2026-08-23 18:50:44 UTC; der damalige Lease ist damit zeitlich abgelaufen. Der Fehlerpfad lag vor dem Draft-Write und vor dem `record_readback()` des kanonischen Redaktionsplans.

## Dauerhafte Prozesskorrektur
Vor einem echten Live-Ergebnis darf kein Produktionspaket mehr als `FINAL` bezeichnet werden.

Zulässige Stufen:
1. `PRELIVE_PASS` nach lokaler Paket-/Supervisor-/PPM-Prüfung.
2. Live-Upload in PSERC.
3. `FINAL` ausschließlich, wenn der heruntergeladene PSERC-Result für exakt dieselbe `package_id` und `production_package_source` Folgendes belegt:
   - `ok=true`
   - `status=PSERC_APPROVED_PRODUCTION_TRIGGER_EXECUTED`
   - `workflow_supervisor_status=PSERC_WORKFLOW_SUPERVISOR_PASS`
   - `bridge_status=PSERC_PPM_INTAKE_BRIDGE_EXECUTED`
   - `ppm_status=NORMAL_DRAFT_END_TO_END_READBACK_PASS_AWAITING_USER_CONTENT_REVIEW_NO_PUBLISH`
   - `publish_allowed=false`
   - keine terminale Veröffentlichung

Damit kann ein lokaler Mock-/Harness-PASS nie wieder als echter Gesamtworkflow-PASS ausgegeben werden.
