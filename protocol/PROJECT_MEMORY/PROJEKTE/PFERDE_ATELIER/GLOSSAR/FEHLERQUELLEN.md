# GLOSSAR – FEHLERQUELLEN

STAND: 2026-09-14
ROLLE: AUTORITATIVE FEHLERQUELLE FÜR DAS PFERDE-ATELIER-GLOSSAR

## GLOSSAR-FE-001 – Abstand oberhalb Hero zu groß
STATUS: LIVE PASS / 2026-09-13

NUTZER-READBACK:
Der obere Abstand wurde real als korrekt bestätigt. Spätere Kandidaten dürfen diesen Punkt nicht regressieren.

## GLOSSAR-FE-002 – Hero-Bild nicht responsive
STATUS: 0.2.8 LIVE FAIL / TECHNISCHE KORREKTUR SPÄTER PASS / PFERDE-LIVE-READBACK NEUER STAND OFFEN

Kein neuer Nutzer-Readback in diesem Chat. Nicht als LIVE PASS behaupten.

## GLOSSAR-FE-003 – AJAX-Suche Frontenddarstellung
STATUS: FRÜHER LIVE FAIL / SPÄTERE TECHNISCHE REGRESSION PASS / LIVE-NEUBEWERTUNG OFFEN

Kein neuer Nutzer-Readback in diesem Chat.

## GLOSSAR-ROUTE-004 – Einzelbegriffe / Einzelartikel öffnen leer
STATUS: LIVE PASS / 2026-09-14

Historische Ursache:
UGE hatte Singular-Requests über ein eigenes klassisches Full-Document-Single-Template gerendert und unter Kubio/FSE eine zweite Dokumenthülle erzeugt.

Technische Korrektur:
Single-Template-Übernahme entfernen; `uge_term` nativ durch WordPress/Kubio rendern lassen.

ENTSCHEIDENDER LIVE-BELEG:
Nutzerreadback dieses Chats: **„artikelanzeige pass“**.

Damit ist dieser Routing-/Öffnungsfehler real geschlossen. Den funktionierenden Single-Routingweg nicht erneut umbauen.

## GLOSSAR-ROUTE-005 – Kategorien nicht dem Glossar-Design angepasst
STATUS: FRÜHER LIVE FAIL / TECHNISCHE KORREKTUR VORHANDEN / PFERDE-LIVE OFFEN

Verbindlich bleibt: eigener Kategorieinhalt plus vollständiger Glossar-Rahmen mit Hero, Suche/A–Z und Icon-Navigation. In diesem Chat kein neuer finaler Live-Readback.

## GLOSSAR-FE-006 – Echter Design-Integrationstest
STATUS: TECHNISCHE TESTLÜCKE HISTORISCH ERKANNT / SINGLE-ROUTING LIVE PASS / NEUES SINGLE-DESIGN NOCH LIVE OFFEN

Lehre bleibt verbindlich: kein LIVE PASS aus Mock-/Stub-/lokaler Codeansicht ableiten.

## GLOSSAR-REG-007 – Direktrouting zerstörte Draft-Preview
STATUS: REPARIERT / REGRESSION PASS

Kein neuer Fail in diesem Chat.

## GLOSSAR-PROD-008 – Cluster konnte nicht vollständig veröffentlichen
STATUS: REPARIERT / TECHNISCH PASS

Die primäre Portal-Kategorie muss vor Veröffentlichung gültig gebunden sein.

## GLOSSAR-LAYOUT-009 – Breadcrumb-Achse im Glossar
STATUS: KATEGORIE-/LISTENSTÄNDE TEILWEISE PASS / SINGLE-BREADCRUMB AKTUELL LIVE FAIL SIEHE 011

Der neue Single-Fehler wird nicht hier dupliziert; maßgeblich ist `GLOSSAR-SINGLE-011`.

## GLOSSAR-PKG-010 – Gated Übergabepaket
STATUS: ALTER RC-STAND HISTORISCH TECHNISCH PASS / AKTUELLE PLUGINARTEFAKT-SYNCHRONISIERUNG BLOCKED

Der alte isolierte MOD-008-Stand im PLUGINS-Büro darf nicht als heutiger Glossar-Release interpretiert werden. Aktuelle lokale Kandidaten 1.2.1 / 1.50.489 sind noch nicht autoritativ quell-/releasegebunden und dürfen deshalb `CURRENT.zip` noch nicht ersetzen.

## GLOSSAR-SINGLE-011 – Einzelansicht: Links, rechte Box, Icons, Breadcrumbs
STATUS: LIVE FAIL / LOKALE NACHBESSERUNG TECHNISCH PASS / LIVE-READBACK OFFEN

### Realer Nutzerbefund

Nach dem Single-Design-Umbau wurden real gemeldet:

1. verwandte Begriffe sind noch als Links im Fließtext vorhanden;
2. `Stockmaß` ist doppelt verlinkt;
3. die rechte Box `Verwandte Begriffe` fehlt bzw. zeigt die Beziehungen nicht korrekt;
4. die vorgesehenen Icons fehlen;
5. die Breadcrumbs stimmen nicht.

### Verbindliches Soll

- Breadcrumb Single: `Startseite > Glossar > Oberbereich > Begriff`;
- Design ausschließlich auf `uge_term`, normale Artikel unverändert;
- Kurzdefinition sichtbar;
- rechte Box oben auf Desktop bündig mit Kurzdefinitionsbalken;
- Box `Verwandte Begriffe` mit echten Links und Icons;
- Box `Mehr zum Thema` mit passender Portal-Kategorie und Icon;
- verwandte Begriffe im Fließtext **nicht** zusätzlich verlinken;
- dasselbe Linkziel im gesamten Begriff nicht doppelt setzen;
- bevorzugter Fließtext-Link auf passende übergeordnete Portal-Kategorie, Journal nur ersatzweise.

Verbindliche Produktionsquelle:
`TEXT_UND_LINKREGELN.md`.

### Lokaler Nachbesserungsstand

Glossar Core / Engine `1.2.1`:
- 14 Bestandsbegriffe 150–200 Wörter;
- exakt 1 Fließtext-Link je Begriff;
- verwandte Begriffe separat gespeichert;
- IDs beim Überschreiben erhalten;
- Fremdkonflikt fail-closed;
- normaler Post unverändert;
- Marker: `CORE_121_POS_NEG_PASS`, `CORE_121_EXISTING_IDS_OVERWRITE_POS_NEG_PASS`, `CORE_121_FOREIGN_FAILCLOSED_AND_NORMAL_POST_NEG_PASS`.

Design `1.50.489`:
- Browser 1200/900/720/500;
- Breadcrumb korrekt;
- falscher globaler Breadcrumb auf `uge_term` verborgen;
- 2 Sideboxen + mindestens 3 Icons;
- Desktop-Ausrichtung bündig;
- kein Overflow;
- Marker: `DESIGN_150489_POS_NEG_PASS`.

### PASS-Grenze

**Noch nicht LIVE PASS.**

Live schließen erst, wenn exakt quellgebundene Paketbytes installiert wurden und real insbesondere `Bandmaß` beweist:
- `Stockmaß` im Fließtext als verwandter Link 0×;
- `Stockmaß` in der rechten Verwandt-Box exakt 1×;
- Portal-Kategorielink exakt 1×;
- Breadcrumb korrekt;
- Icons sichtbar;
- normaler Artikel unverändert.

## ÜBERGREIFENDER STATUS

- Einzelartikel öffnen: LIVE PASS.
- Aktuelle aktive Fehlerarbeit: ausschließlich `GLOSSAR-SINGLE-011`.
- Neue Begriffe erst aus frisch nachgewiesenen `GEPRUEFT`-WDB-Quellen.
- Keine lokale/technische Prüfung als LIVE PASS ausgeben.
