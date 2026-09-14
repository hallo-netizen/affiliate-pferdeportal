# GLOSSAR – HOBBYRAUM

STAND: 2026-09-14
STATUS: BLOCKED

## 1-KLICK-ÜBERSICHT

**WAS IST DAS?**  
Der einzige aktuelle Arbeitsraum des Büros GLOSSAR.

**AKTUELLER SICHERER BEFUND**  
Einzelartikel lassen sich im Pferde Atelier real öffnen → **LIVE PASS**. Offen sind ausschließlich die danach gemeldeten Fehler der Glossar-Einzelansicht: Breadcrumb, verwandte Linkbox, doppelte Linkziele/Stockmaß, fehlende Icons und saubere Trennung Fließtext ↔ Seitenbox.

**DU DARFST …**  
nur an genau diesen offenen Single-Layout-/Linkpunkten weiterarbeiten und dabei `TEXT_UND_LINKREGELN.md` zwingend einhalten.

**DU DARFST NICHT …**  
den bereits bestätigten Artikel-Routingweg wieder umbauen, normale WordPress-Artikel verändern, neue ungeprüfte Fachbegriffe erfinden, aus lokalen Tests LIVE PASS ableiten oder alte Pluginartefakte blind als CURRENT ersetzen.

## ARBEITSORT

Branch:
`hobbyroom/glossar-livefail-red-green-20260913`

Autoritative Fehlerquelle:
`FEHLERQUELLEN.md`

Autoritativer Stand:
`CURRENT_STATE.md`

Verbindliche Text-/Linkregeln:
`TEXT_UND_LINKREGELN.md`

## LETZTER LIVE SICHERER STAND

- Glossarbegriffe/Einzelartikel öffnen: **LIVE PASS** – Nutzerreadback dieses Chats: `artikelanzeige pass`.
- Der frühere Single-Routingfehler `GLOSSAR-ROUTE-004` ist damit geschlossen.

## AKTUELLER LIVE FAIL

Auf der Begriffseinzelansicht wurden real gemeldet:

- verwandte Begriffe noch im Fließtext verlinkt;
- `Stockmaß` doppelt verlinkt;
- rechte Box `Verwandte Begriffe` fehlt/ist nicht korrekt ausgegeben;
- Icons fehlen;
- Breadcrumbs stimmen nicht.

Verbindliche Sollregel:
**Verwandte Begriffe als Links ausschließlich in der rechten Box; im Fließtext 0× erneut als verwandte Links.**

## LOKAL GEPRÜFTE, ABER NOCH NICHT RELEASEGEBUNDENE NACHBESSERUNG

### Glossar Core / Engine 1.2.1
Lokales Paket:
`UNIVERSAL_GLOSSARY_ENGINE_1.2.1_GLOSSAR_ARTIKEL_UPDATE_INSTALLIEREN.zip`

SHA-256:
`f6788524f50413541ea40e33bc7005a4e936e2915e4465cf2e7a08e221c900e0`

Lokal erneut PASS:
- 14 Bestandsbegriffe 150–200 Wörter;
- genau 1 Fließtext-Link je Begriff;
- verwandte Begriffe separat in Relation/Meta;
- IDs bleiben beim Überschreiben erhalten;
- Fremdkonflikt fail-closed;
- normaler WordPress-Beitrag unverändert;
- ZIP + Version 1.2.1 PASS.

### Pferde Atelier Design 1.50.489
Lokales Paket:
`PFERDE_ATELIER_DESIGN_V1.50.489_GLOSSAR_EINZELANSICHT_FIX_INSTALLIEREN.zip`

SHA-256:
`fc6bc67a827f314e37c597e4fbb764f616c86d97bfc6d621c238c813a64ab600`

Lokal bei 1200/900/720/500 px PASS:
- Breadcrumb `Startseite > Glossar > Pferd & Biologie > Bandmaß`;
- falscher globaler Breadcrumb auf Glossar-Single ausgeblendet;
- Kurzdefinition + rechte Box bündig am Desktop;
- Boxen `Verwandte Begriffe` + `Mehr zum Thema`;
- Icons vorhanden;
- kein Overflow;
- Ausgabe hart auf `uge_term` begrenzt.

## WARUM BLOCKED

Die lokalen finalen Kandidaten sind noch nicht als eindeutiger autoritativer GitHub-Quellstand/Release gebunden. Daher darf gemäß Plugin-Artefaktpflicht weder ein neues `CURRENT.zip` behauptet noch ein Release/LIVE-PASS daraus abgeleitet werden.

## NEXT ACTION – EXAKT

1. Quellstand von Core `1.2.1` und Design `1.50.489` in der autoritativen technischen Quelle/Branch binden.
2. Paketbytes aus genau diesem Quellstand erzeugen oder Byte-Identität zu den oben genannten ZIPs beweisen.
3. dieselben Positiv-/Negativ-/Regressionstests aus dem gebundenen Stand erneut ausführen.
4. dann PLUGINS-Büro mit `CURRENT.zip` + `MANIFEST.md` synchronisieren.
5. live installieren.
6. **Bandmaß live prüfen:**
   - Breadcrumb korrekt;
   - Icons sichtbar;
   - `Stockmaß` als verwandter Link im Fließtext **0×**;
   - `Stockmaß` in rechter Box **exakt 1×**;
   - Portal-Kategorielink im Fließtext **exakt 1×**;
   - normale Artikel unverändert.
7. Erst nach Nutzer-Readback LIVE PASS.
8. Neue Begriffe erst aus frisch nachgewiesenen `GEPRUEFT`-WDB-Quellen.

## NICHT ANFASSEN

- den bestätigten funktionierenden Single-Routingweg;
- normale WordPress-Posts/Seiten;
- `main` als Experimentierfläche;
- bestehende Glossarbegriffe durch Löschen statt gezieltes Überschreiben;
- Wissensdatenbank-Fakten ohne `GEPRUEFT`;
- andere offene Glossarbereiche, bis die Single-Ansicht sauber geschlossen ist.
