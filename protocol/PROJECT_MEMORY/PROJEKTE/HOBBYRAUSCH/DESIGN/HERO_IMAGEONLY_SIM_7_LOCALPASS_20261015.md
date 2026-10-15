# HOBBYRAUSCH – IMAGE-ONLY SIMULATION 7 – LOCAL PASS

STAND: 2026-10-15
BASIS: `AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.650_HOBBY_DEPOT_HUB2_IMAGE_CURATED_WIDER_CLEARER_NOFRAME_LOCALPASS.zip`
ROLLE: rein lokale technische Simulation. KEIN Release. KEIN Installationspaket.

## Zweck
Beweisen, dass die neuen Bilddateien später ohne Architektur-, Mapping- oder Codeänderung in die eingefrorene 1.50.650-Basis eingesetzt werden können.

## Eingesetzte WIP-Einzelquellen
- Astronomie
- Papierkunst
- Textilgestaltung
- Malen & Zeichnen
- Schrift & Lettering
- Guss & Formen
- Miniaturen & Szenen – WIP-Auswahl Kandidat B

## Basisverifikation
Die echte 1.50.650-Laufzeit wurde vor der korrigierten Simulation geprüft:
- Hub2-Hero-Container: `aspect-ratio: 600/320`;
- Hero-Bild: `width:100%; height:100%; aspect-ratio:600/320; object-fit:cover`;
- Kategorie-Vorschau Desktop: 200×107.

Damit ist **600×320** das korrekte Hero-Dateimaß für den reinen Bildersatz ohne CSS-Eingriff. Der frühere 600×220-Zwischenstand wurde verworfen und nie als Release freigegeben.

## Technische Ableitung
Pro Kategorie:
- Hero: exakt **600×320**, WEBP
- Preview: exakt **200×107**, WEBP
- gleicher bestehender 1.50.650-Zielpfad
- keine Hochskalierung der Quelle

## Positivtest
PASS:
- exakt **14** bestehende Bilddateien geändert;
- **0** Dateien hinzugefügt;
- **0** Dateien entfernt;
- **0** Nicht-Bilddateien verändert;
- **0** PHP-Dateien verändert;
- **0** CSS-/JS-Dateien verändert;
- **0** JSON-/TXT-Dateien verändert;
- `assets/hobby-depot-v150650/hub2-image-map.json` byte-identisch.

Mapping SHA-256 vor/nach:
`0f669f05a232512ad4d4fd386300115f29832c3b249dcb568e7abf957d120a66`

## Zieldatei-Prüfung
PASS:
- 7/7 Hero-Dateien: 600×320 WEBP
- 7/7 Preview-Dateien: 200×107 WEBP
- 14/14 Ausgabedateien eindeutig
- keine zusätzlichen Zielpfade
- keine Datei außerhalb der 14 erwarteten Bildpfade geändert

## Ausgabedatei-Hashes der korrigierten V2-Simulation

Hero-WEBP:
- Astronomie: `d87d38c380d8e719e5dbcf25a66147d4cd0f35df44b48f21d5b16b2abf5c5e9e`
- Papierkunst: `b951daba285657aa23687006d7cc4c6f981c8e77b46786b150939bf70aeb450f`
- Textilgestaltung: `5b6259c7f6fbf40a8733b26588fd89aa8de5261dbee007654d178546c92661f5`
- Malen & Zeichnen: `4e9e584fb183318a0f515bf94578677825e395231584ce19f977dc8673701c8f`
- Schrift & Lettering: `540a176c7896839633668966b50a372a1ebb4be53a85b3841053c15db60045c2`
- Guss & Formen: `594fcec9b5b78a8dc81c31783b2251f5eaa99c826795e577b010898fcb91d6e2`
- Miniaturen & Szenen B: `e3c602e65a138453cf2fa86192f3e8d378bafd34b958d2d33e32b42c5c017395`

Preview-WEBP:
- Astronomie: `7cf5cbb3de6092c6bbf03e1aef2e2e37a61ac883e39eef6a1751deaacba5db7b`
- Papierkunst: `b8b1a89abeedc72a0290c996b3142f8fff9b568c3bd1ea0984ea8a2577061e50`
- Textilgestaltung: `12c29f428ef7422f384816d05e20bc026ed66112f3af37e01f0be76be83ac8ab`
- Malen & Zeichnen: `ecbce49de198b0a8621c8d7b6b2a6a06113f950125182a7c1dfd45542fca9932`
- Schrift & Lettering: `22fd3c004479711ceb97df40d63273e0ae1fd1fd5072fe215fc4c2921239b405`
- Guss & Formen: `827315a7ca6acbdac1416507520bcd757996a0a003471125995322c300eb72a2`
- Miniaturen & Szenen B: `fb78dc4c66ccf69f8ddfb60e65d73de9a210360aefc2e8a7b9b681ed34e76073`

## Roundtrip
Die lokale WIP-Struktur wurde gezippt und erneut entpackt.

PASS:
- **981/981 Dateien** nach ZIP-Roundtrip byte-identisch zum simulierten WIP-Verzeichnis.
- korrigierte V2-Simulation: exakt 14 Bild-Diffs, 0 Code-/Mapping-Diffs.

## Ergebnis
Der KISS-Pfad ist technisch bestätigt:

**1.50.650 unverändert lassen → nur bestehende Hero-/Preview-Bilddateien am bestehenden Pfad ersetzen.**

Es ist kein Helper-Plugin, kein neues Mapping, kein Hook und kein Architekturumbau erforderlich.

Der vollständige Kandidat darf trotzdem erst nach kompletter 30/30-Motivfreigabe gebaut werden.
