# BÜRO GLOSSAR – CURRENT_STATE

STAND: 2026-09-14
STATUS: EINZELARTIKELANZEIGE LIVE PASS / EINZELANSICHT-DESIGN + LINKAUSGABE LIVE FAIL / TECHNISCHE NACHBESSERUNG LOKAL PASS, NICHT LIVE

## Belastbarer aktueller Stand

- Büro `GLOSSAR` steuert das öffentliche Pferde-Atelier-Glossar.
- Fachwahrheit bleibt ausschließlich in `../WISSENSDATENBANK/AKTENSCHRAENKE/GLOSSAR/`.
- Öffentlicher Begriffstyp: `uge_term`; Glossar-Oberbereiche: `uge_group`.
- Arbeitsbranch: `hobbyroom/glossar-livefail-red-green-20260913`.
- Branch-Head vor dieser Nachholprüfung: `b22e1bde509c53a3daf4337edf6535c03c9b80a4`.

## LIVE bestätigt

Der Nutzer hat in diesem Chat ausdrücklich bestätigt:

**„artikelanzeige pass“**

Damit ist der frühere Fehler `GLOSSAR-ROUTE-004` – Einzelbegriffe/Einzelartikel öffnen nicht – im realen Pferde-Atelier als **LIVE PASS** geschlossen.

## LIVE offen / fehlerhaft

Nach dem Single-Design-Umbau wurden real folgende Fehler gemeldet:

1. verwandte Begriffe erscheinen noch als Links im Fließtext statt ausschließlich in der rechten Box;
2. dasselbe Linkziel wurde doppelt ausgegeben, konkret `Stockmaß`;
3. die rechte Box `Verwandte Begriffe` fehlte bzw. war nicht korrekt befüllt/positioniert;
4. die vorgesehenen Icons fehlten;
5. die Breadcrumbs der Begriffseinzelansicht waren falsch;
6. Nutzerregel bestätigt: sobald verwandte Begriffe rechts als Linkbox ausgegeben werden, dürfen diese Ziele im Fließtext nicht nochmals verlinkt werden.

Diese Punkte sind in `FEHLERQUELLEN.md` als aktueller Single-Layout-/Linkfehler gebunden.

## Verbindliche Text-/Linkregeln

`TEXT_UND_LINKREGELN.md` ist Pflichtquelle für jede Glossarproduktion. Kern:

- ca. 150–200 Wörter;
- keine Zwischenüberschriften im Begriffstext;
- individuelle Formulierungen, keine wiederkehrenden Floskeln;
- nur geprüfte Fakten aus der Wissensdatenbank;
- Kurzdefinition/Zusammenfassung ist Pflichtfeld;
- dasselbe Linkziel nie zweimal im selben Begriff;
- Fließtext bevorzugt passende übergeordnete Portal-Kategorie, Journal nur ersatzweise;
- verwandte Glossarbegriffe als Links ausschließlich im Block `Verwandte Begriffe`, nicht zusätzlich im Fließtext.

## Aktuelle technische Nachbesserung – noch kein Release/LIVE

Lokal im Arbeitscontainer liegen zwei nachgebesserte Kandidaten:

### Glossar Core / Engine 1.2.1
Paket:
`UNIVERSAL_GLOSSARY_ENGINE_1.2.1_GLOSSAR_ARTIKEL_UPDATE_INSTALLIEREN.zip`

SHA-256:
`f6788524f50413541ea40e33bc7005a4e936e2915e4465cf2e7a08e221c900e0`

Tatsächlich erneut ausgeführte lokale Prüfungen am 2026-09-14:
- 14 vorhandene Begriffe: 150–200 Wörter → PASS;
- genau 1 Fließtext-Link je Begriff → PASS;
- verwandte Begriffe separat gespeichert → PASS;
- Bestands-IDs beim Überschreiben erhalten → PASS;
- Fremdbegriff-Konflikt fail-closed → PASS;
- normaler WordPress-Beitrag bleibt unberührt → PASS;
- ZIP-Lesetest → PASS;
- Version `1.2.1` → PASS.

Marker:
- `CORE_121_POS_NEG_PASS`
- `CORE_121_EXISTING_IDS_OVERWRITE_POS_NEG_PASS`
- `CORE_121_FOREIGN_FAILCLOSED_AND_NORMAL_POST_NEG_PASS`

### Pferde Atelier Design 1.50.489
Paket:
`PFERDE_ATELIER_DESIGN_V1.50.489_GLOSSAR_EINZELANSICHT_FIX_INSTALLIEREN.zip`

SHA-256:
`fc6bc67a827f314e37c597e4fbb764f616c86d97bfc6d621c238c813a64ab600`

Tatsächlich erneut ausgeführte lokale Browserprüfung am 2026-09-14 bei 1200/900/720/500 px:
- Breadcrumb: `Startseite > Glossar > Pferd & Biologie > Bandmaß` → PASS;
- globale/falsche Breadcrumb-Ausgabe auf `uge_term` ausgeblendet → PASS;
- `Kurz erklärt` + rechte Box bei Desktop bündig → PASS;
- 2 rechte Boxen (`Verwandte Begriffe`, `Mehr zum Thema`) → PASS;
- mindestens 3 Icons → PASS;
- kein horizontaler Overflow → PASS;
- Glossar-Single hart auf `uge_term` begrenzt → PASS.

Marker:
`DESIGN_150489_POS_NEG_PASS`

## Harte Grenze / kein falscher PASS

Diese beiden lokalen Kandidaten sind **noch kein belastbarer Plugin-Release und kein LIVE-PASS**, weil ihr finaler Quellstand noch nicht als autoritativer GitHub-Quell-Commit/Release synchronisiert ist und kein realer Pferde-LIVE-Readback dieser exakten Paketbytes vorliegt.

Deshalb darf `PLUGINS/ISOLIERTE_PLUGINS/.../CURRENT.zip` aus dieser Nachholprüfung nicht blind auf diese lokalen Pakete umgestellt werden.

## Neue Begriffe

Neue Glossarbegriffe dürfen erst geschrieben/produziert werden, wenn die jeweilige Wissensdatenbank-Quelle tatsächlich `GEPRUEFT` ist. In diesem Chat wurde kein weiterer neuer Begriff nachweisbar aus einer frisch gelesenen `GEPRUEFT`-Quelle fertig freigegeben. Keine Erfindung aus Chatwissen.

## Nächster belastbarer Schritt

1. finalen Quellstand von Glossar Core `1.2.1` und Design `1.50.489` in der autoritativen technischen Quelle/Branch eindeutig binden;
2. exakt aus diesem Quellstand neu paketieren bzw. Byte-Identität zum vorhandenen Paket beweisen;
3. Positiv-/Negativ-/Regressionstests aus dem gebundenen Quellstand erneut ausführen;
4. erst danach PLUGINS-Büro `CURRENT.zip` + `MANIFEST.md` aktualisieren;
5. exakt diese Pakete live installieren;
6. auf `Bandmaß` live prüfen: Breadcrumb korrekt, Icons sichtbar, Stockmaß **0× als verwandter Link im Fließtext und exakt 1× in der rechten Box**, Portal-Kategorielink einmalig;
7. erst bei realem Nutzer-Readback LIVE PASS setzen;
8. anschließend neue `GEPRUEFT`-Begriffe produzieren.
