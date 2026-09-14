# GLOSSAR – PROTOKOLL JSON-UMSTELLUNG – 2026-09-14

ROLLE: AUSFÜHRUNGSPROTOKOLL; keine zweite CURRENT-/Fehler-/Zielwahrheit.

## Ausgangspunkt

Der bisherige Glossar-Core sollte Kandidatenfindung, Research-/Textpaket, Workersteuerung und WordPress-Ausgabe weitgehend automatisieren.

Reale Live-Kette:
- 1.3.5 LIVE FAIL – künstliches 400er-Limit;
- 1.3.6 LIVE FAIL – Planning konnte trotz Promotions ausbleiben;
- 1.3.7 LIVE FAIL – Phase PLANNING korrekt, Folgeworker praktisch WP-Cron-abhängig;
- 1.3.8 lokal hart getestet, LIVE nie abgenommen.

1.3.8-Testreport belegt lokal u. a. E2E, 50/50 simulierte WordPress-Beiträge, 93 explizite PASS-Zeilen und 6/6 Mutanten ROT. Das ist ausdrücklich kein LIVE-PASS.

## Nutzerentscheidung

Der Nutzer hat am 2026-09-14 verbindlich entschieden, die komplizierte autonome Glossar-Textproduktion nicht weiterzuverfolgen.

Neuer gewünschter Weg:
`Glossar-WDB -> Chat erstellt fertige Texte -> JSON-Datei -> Plugin-Import -> WordPress-Draft`.

Das Glossar-Plugin soll dafür analog zum Pferderassen-Manager umgebaut werden.

## Fachbasis geprüft

Der zentrale Aktenschrank existiert bereits:
`../WISSENSDATENBANK/AKTENSCHRAENKE/GLOSSAR/`

Aktuell vorhandene quellengebundene Begriffe dort:
- Stockmaß;
- Widerrist;
- Ganasche;
- Röhrbein;
- Aalstrich;
- Kötenbehang;
- Zuchtbuch / Studbook.

Es wird **kein zweiter Aktenschrank** angelegt.

## Dauerhafte Nachholungen dieses Closeouts

Aktualisiert:
- `CURRENT_STATE.md`;
- `HOBBYRAUM.md`;
- `FEHLERQUELLEN.md`;
- `PRODUKTIONSREGELN.md`;
- `ENTSCHEIDUNGEN_20260914.md`.

Neu festgehalten:
- alter Worker-/Cron-/Loopback-Weg ist abgelöst;
- WDB bleibt Fachautorität;
- JSON ist Transport;
- WordPress ist Ausgabesystem;
- neuer Importer: Draft-first + Readback + fail-closed;
- Auto-Publish ist nicht der Normalweg.

## Nicht ausgeführt

- kein neuer Glossar-Importer gebaut;
- kein neuer JSON-Batchvertrag final versioniert;
- kein neuer Plugin-ZIP-Test für den Importer;
- kein realer JSON->WordPress-Draft-Test des neuen Wegs;
- kein neues isoliertes PLUGINS-`CURRENT.zip`.

## Statusgrenze

Aktueller Stand ausschließlich aus `CURRENT_STATE.md`; aktiver Fehler ausschließlich aus `FEHLERQUELLEN.md`; NEXT ACTION ausschließlich aus `HOBBYRAUM.md`.