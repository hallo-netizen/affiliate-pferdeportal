# HOBBYRAUSCH – FULL-30 IMAGE-ONLY OVERLAY SYNTHETIC TEST

STAND: 2026-10-15
STATUS: **PASS / TECHNISCHER VOLLTEST / KEIN RELEASE / KEINE ECHTEN MOTIVE**

BASIS:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.650_BASE.zip`

ZWECK:
Den kompletten späteren 30-Kategorien-/60-Bilddateien-Einbau technisch einmal vollständig durchlaufen, ohne die noch fehlenden echten Motive zu erfinden.

Dafür wurden ausschließlich synthetische, eindeutig unterscheidbare Testbilder erzeugt. Diese Testbilder sind **keine** Hobby-Depot-Motive, keine Quellen und kein Releasebestand.

## Erster Volltest
Ergebnis: FAIL mit exakt einem Zielpfadfehler.

Gefunden:
- Hero `Münzen & Geld` korrekt historisch auf `subcategories/sammeln/munzen-geld-v150623.webp`;
- Preview-Ziel war fälschlich ebenfalls mit `munzen-` angenommen;
- aktiver 1.50.650-Renderer besitzt Alias `munzen-geld => muenzen-geld`;
- reale Preview-Datei lautet `subcategories/sammeln/muenzen-geld-v150634.webp`.

Fehler als AF-041 dokumentiert und Manifest korrigiert.

## Zweiter Volltest nach Korrektur
**PASS**

- 30/30 Kategorien durchlaufen;
- 60/60 reale Zielbildpfade vorhanden;
- exakt **60 Bilddateien geändert**;
- **0 Dateien hinzugefügt**;
- **0 Dateien entfernt**;
- **0 unerwartete Änderungen**;
- **0 erwartete, aber unveränderte Bildziele**;
- Dateizahl vor/nach: **981 / 981**;
- `hub2-image-map.json` byte-identisch;
- ZIP-Roundtrip: **PASS / vollständig identisch**.

Technische Test-ZIP SHA-256:
`d91e8496a4c690fb145f919aaa1603ae591d41735205e438d723586105175ec1`

WICHTIG:
Die technische Test-ZIP wird **nicht** als Plugin ausgeliefert und darf nicht installiert werden. Sie enthält synthetische Testbilder und dient nur als Vollnachweis, dass der spätere 30er-Image-only-Einbau auf 1.50.650 technisch ohne Code-/Mapping-/Architekturänderung funktioniert.

## Ergebnis
Der technische Plugin-Pfad ist jetzt vollständig 30/30 bewiesen:

**1.50.650 unverändert → exakt 60 bestehende Bilddateien ersetzen → 0 sonstige Änderungen → Roundtrip PASS.**

Für den echten Plugin-Kandidaten fehlt damit ausschließlich der reale visuell freigegebene 30/30-Bildquellenbestand.
