# UNIVERSAL GLOSSAR ENGINE – TESTPROTOKOLL 0.2.9

STAND: 2026-09-13
ERGEBNIS: TECHNISCHER KANDIDAT PASS / PFERDE-LIVE-READBACK OFFEN

## Anlass

0.2.8 wurde im realen Pferde-Frontend widerlegt:
- Hero höher, aber nicht real responsive;
- Kategorien nicht an den vollständigen Glossar-Startseitenrahmen angepasst;
- Einzelbegriff-Links laufen weiterhin ins Leere.

Zusätzlich wurde eine fachlich falsche Acceptance entdeckt: der 0.2.8-Test verlangte auf Kategorien explizit **kein Hero / keine Tools**, obwohl die Nutzeranforderung den vollständigen Glossar-Rahmen auf jeder Kategorie verlangt.

## RED→GREEN während 0.2.9

RC1 führte einen direkten Request-Binder ein, um Begriff-/Kategorie-Routing von gespeicherten Rewrite-Regeln unabhängig zu machen.

Die vollständige alte Regression wurde ausgeführt und fand einen echten neuen Fehler:
- `REG_DRAFT_PUBLIC_PASS`
- danach authentifizierte Draft-Preview → 404

Ursache: Direct Binder fing native WordPress-Preview-Requests ab.

RC1 wurde nicht freigegeben. Neue Produktbytes erhielten korrekt neue Kennung `0.2.9-rc2`.

RC2 nimmt `preview`, `preview_id`, `preview_nonce` vom Binder aus. Danach `REG_PREVIEW_PASS` und vollständige Matrix PASS.

## RC2-Hardtest

Run: `34757648732`

PASS:
- Build `103724706302`
- Fresh + alte Regression + Null-Rewrite `103724706154`
- 0.2.8 → RC2 + Null-Rewrite `103724706246`
- Real Design 1.50.469 + Browser + Null-Rewrite `103724706256`
- no-package gate `103724900368`

Kein RC-Paket wurde an den Nutzer ausgegeben.

## Finaler 0.2.9-Hardtest

Workflow:
`.github/workflows/glossar-029-final-hardtest.yml`

Run: `34757795593`
Head: `f2fa6f0c248acfa6978b5faec5daf42a40d0ba3b`

Alle Gates PASS:
- Build `103725094481`
- Fresh/Regression/Null-Rewrite `103725094537`
- Update vom tatsächlich ausgegebenen 0.2.8-Stand → 0.2.9 plus erneuter Null-Rewrite `103725094620`
- echter Design-1.50.469-Runtime + Browser + Null-Rewrite `103725094378`
- gated Package `103725295224`

Final 0.2.9 unterscheidet sich von dem grünen RC2 ausschließlich in der Versionskennung.

## Hero / echtes Responsive-Verhalten

Echter Browser, echter gerenderter `<img>`, Viewports 1200 / 900 / 720 / 500.

Natural size: 1400 × 560.

Gemessen:
- 1200 → 1096 × 438.390625
- 900 → 796 × 318.390625
- 720 → 664 × 265.59375
- 500 → 444 × 177.59375

Prüfung:
- Breite sinkt mit Viewport;
- Höhe sinkt mit Viewport;
- gerendertes Verhältnis entspricht Natural-Verhältnis;
- Bildbreite entspricht Hero-Breite;
- keine feste Bildhöhe / kein erzwungener Aspect-Ratio-Kasten als Ersatz für Responsivität.

Marker:
`REAL_DESIGN_029_TRUE_RESPONSIVE_IMAGE_PASS`.

## Kategorien – korrigierter Fachvertrag

`/glossar/gesundheit/` muss gleichzeitig enthalten:
- `.uge-category-head`;
- H1 `Gesundheit`;
- `.uge-hero`;
- `.uge-tools`;
- `.uge-topic-nav`;
- realen Begriff-Link.

Damit bleibt Kategorie fachlich eigenständig, nutzt aber denselben vollständigen visuellen Glossar-Rahmen wie die Startseite.

Marker:
`REAL_DESIGN_029_CATEGORY_FULL_SHELL_PASS`.

## Einzelbegriff-Links / Routing-Hardlock

0.2.9:
- Rewrite-Schema 7;
- zusätzlicher `parse_request`-Binder für Glossar-Begriffe und Glossar-Gruppen.

Härtester Routing-Negativfall:
1. Schema 7 ist bereits aktuell.
2. **Alle gespeicherten Glossar-Rewrite-Regeln werden gelöscht.**
3. Es findet kein notwendiger Schemawechsel statt, der den Zustand automatisch retten könnte.
4. Kategorie und Einzelbegriff müssen trotzdem echte Renderer erreichen.

Zusätzlich im Browser:
- tatsächlichen Hufbein-Link auf Kategorie finden;
- echten Link anklicken;
- Ziel muss `/glossar/begriff/hufbein/` sein;
- `article.uge-single-wrap` genau einmal;
- erwarteter Inhalt vorhanden.

Marker:
`REAL_DESIGN_029_CLICKED_TERM_LINK_PASS`.

## Weitere Positiv-/Negativprüfung

PASS:
- AJAX reale Treffer/Position;
- A–Z;
- Draft öffentlich gesperrt;
- unbekannter Begriff 404;
- authentifizierte Draft-Preview;
- Duplicate Guard;
- normale WordPress-Beiträge unverändert;
- Kategorie/Begriff-Routing;
- echter Designcode statt Stub.

Real Design Hauptcode SHA-256:
`580fa6c7f5566f29df9254ce92f687a4831554e1d84bf03fbd936bb7577edfe5`.

## Gated Paket

Actions-Artefakt-ID:
`10317444708`

Outer digest:
`sha256:98513772d72fc65dc4d01520086b4c7e56e165cceeea1e31147a9d6cf830c6ff`

Inneres installierbares ZIP:
`universal-glossary-engine-0.2.9.zip`

SHA-256:
`864befa0d159577e418906e4de3052ad0127b7dbcdad80775ba7e8f734ed1173`

Das Actions-Artefakt wurde heruntergeladen und das innere ZIP lokal erneut geprüft:
- ZIP-Integrität PASS;
- Pluginversion 0.2.9 PASS;
- `UGE_VERSION` 0.2.9 PASS;
- Rewrite-Schema 7 PASS;
- Direct Binder vorhanden PASS;
- Kategorie-Vollrahmen-Code vorhanden PASS;
- keine `0.2.9-rc*`-Kennung PASS;
- Hash stimmt mit Paketjob überein PASS.

## Grenze

Technischer Kandidat 0.2.9: PASS.

Pferde-LIVE-PASS: **noch offen**. Nur der reale Readback des exakt hashgebundenen Pakets darf die aktuellen Live-Fehler schließen.
