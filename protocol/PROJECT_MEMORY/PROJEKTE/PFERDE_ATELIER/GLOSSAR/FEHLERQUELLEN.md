# GLOSSAR – FEHLERQUELLEN

STAND: 2026-09-14
ROLLE: AUTORITATIVE FEHLERQUELLE FÜR DAS PFERDE-ATELIER-GLOSSAR

## GLOSSAR-FE-001 – Abstand oberhalb Hero zu groß
STATUS: LIVE PASS / 2026-09-13

Der obere Abstand wurde real als korrekt bestätigt. Nicht regressieren.

## GLOSSAR-FE-002 – Hero-Bild nicht responsive
STATUS: 0.2.8 LIVE FAIL / TECHNISCHE KORREKTUR SPÄTER PASS / PFERDE-LIVE-READBACK NEUER STAND OFFEN

## GLOSSAR-FE-003 – AJAX-Suche Frontenddarstellung
STATUS: FRÜHER LIVE FAIL / SPÄTERE TECHNISCHE REGRESSION PASS / LIVE-NEUBEWERTUNG OFFEN

## GLOSSAR-ROUTE-004 – Einzelbegriffe / Einzelartikel öffnen leer
STATUS: LIVE PASS / 2026-09-14

Nutzerreadback: **„artikelanzeige pass“**. Der funktionierende Single-Routingweg darf nicht erneut umgebaut werden.

## GLOSSAR-ROUTE-005 – Kategorien nicht dem Glossar-Design angepasst
STATUS: FRÜHER LIVE FAIL / TECHNISCHE KORREKTUR VORHANDEN / PFERDE-LIVE OFFEN

## GLOSSAR-FE-006 – Echter Design-Integrationstest
STATUS: TECHNISCHE TESTLÜCKE HISTORISCH ERKANNT / SINGLE-ROUTING LIVE PASS / NEUES SINGLE-DESIGN NOCH LIVE OFFEN

Kein LIVE PASS aus Mock-/Stub-/lokaler Codeansicht ableiten.

## GLOSSAR-REG-007 – Direktrouting zerstörte Draft-Preview
STATUS: REPARIERT / REGRESSION PASS

## GLOSSAR-PROD-008 – Cluster konnte nicht vollständig veröffentlichen
STATUS: REPARIERT / TECHNISCH PASS

## GLOSSAR-LAYOUT-009 – Breadcrumb-Achse im Glossar
STATUS: KATEGORIE-/LISTENSTÄNDE TEILWEISE PASS / SINGLE-BREADCRUMB AKTUELL LIVE FAIL SIEHE 011

## GLOSSAR-PKG-010 – Gated Übergabepaket
STATUS: ALTER RC-STAND HISTORISCH TECHNISCH PASS / AKTUELLE PLUGINARTEFAKT-SYNCHRONISIERUNG NOCH NICHT LIVE ABGENOMMEN

## GLOSSAR-SINGLE-011 – Einzelansicht: Breadcrumb, Fließtextlinks, rechte Boxen
STATUS: LIVE FAIL / KANDIDAT 1.2.2 + 1.50.490 LOKAL POSITIV/NEGATIV PASS / LIVE-READBACK OFFEN

### Realer Nutzerbefund 2026-09-14

Screenshot/Readback zeigt weiterhin:

1. Breadcrumbs sind nicht korrekt; Oberbereich erscheint falsch/doppelt statt sauberer Glossar-Kette.
2. Im Fließtext sind weiterhin Links vorhanden.
3. Der ockerfarbene obere Strich der rechten Blöcke ist zu dick.
4. Bereits bestehende Glossarbeiträge müssen nach der neuen Regel ebenfalls überschrieben/aktualisiert werden.

### Verbindliches Soll

- Breadcrumb Single exakt: `Startseite > Glossar > Oberbereich > Begriff`;
- **0 Links im gesamten Glossar-Fließtext**;
- verwandte Links ausschließlich rechts in `Verwandte Begriffe`;
- Portalziel ausschließlich rechts in `Mehr zum Thema`;
- rechte Boxen mit dünnerer Ocker-Oberkante: Kandidat 2 px statt vorher 4 px;
- bestehende Glossarbeiträge per Update überschreiben, ID/URL erhalten;
- Design ausschließlich auf `uge_term`; normale Artikel unverändert;
- Kurzdefinition und Icons sichtbar.

Verbindliche Produktionsquelle:
`TEXT_UND_LINKREGELN.md`.

### Lokaler Nachbesserungsstand

Core `1.2.2`:
- 14 gebundene Begriffe weiterhin 150–200 Wörter;
- 0 `<a>`-Links im Fließtext;
- Bestandsmigration entfernt Links aus bestehenden `uge_term`-Inhalten und nutzt dieselbe ID;
- normaler Post im Negativtest unverändert;
- ZIP/Version PASS;
- Marker `CORE_122_ZERO_BODY_LINKS_POS_NEG_PASS`;
- Marker `CORE_122_EXISTING_ID_PRESERVE_AND_NORMAL_POST_NEG_PASS`;
- Paket-SHA-256 `3d6ffc2cdfcc4872e49e97f4adc54de31d4ef2714b0af07e399a681f15d1f447`.

Design `1.50.490`:
- globaler Breadcrumb-Payload wird auf `uge_term` serverseitig nicht mehr erzeugt;
- zusätzliche CSS-Restsperre vorhanden;
- eigener Breadcrumb bleibt `Startseite > Glossar > Oberbereich > Begriff`;
- Render-Endschranke entfernt Restlinks aus dem Fließtext;
- rechte Box-Oberkante 2 px;
- Scope `uge_term`, normaler Post ausgeschlossen;
- ZIP/Version PASS;
- Marker `DESIGN_150490_BREADCRUMB_ZERO_LINKS_THIN_STRIPE_POS_NEG_PASS`;
- Paket-SHA-256 `251e90a7c7115cd4ce166ddefb5f0918904f28b89d85f2a173c190201b454657`.

### PASS-Grenze

**Noch nicht LIVE PASS.**

Live schließen erst nach Installation der exakten Pakete und realem Readback von `Bandmaß`:
- Breadcrumb korrekt;
- Fließtext 0 Links;
- `Stockmaß` rechts als verwandter Link;
- Portalziel rechts in `Mehr zum Thema`;
- Ockerlinie sichtbar dünner;
- Bestands-ID/URL erhalten;
- normaler Artikel unverändert.

## ÜBERGREIFENDER STATUS

- Einzelartikel öffnen: LIVE PASS.
- Aktuelle aktive Fehlerarbeit: `GLOSSAR-SINGLE-011`.
- Neue Begriffe erst aus frisch nachgewiesenen `GEPRUEFT`-WDB-Quellen.
- Keine lokale/technische Prüfung als LIVE PASS ausgeben.
