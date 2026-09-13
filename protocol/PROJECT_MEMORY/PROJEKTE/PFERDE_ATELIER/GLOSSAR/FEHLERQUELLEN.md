# GLOSSAR – FEHLERQUELLEN

STAND: 2026-09-13
ROLLE: AUTORITATIVE FEHLERQUELLE FÜR DAS PFERDE-ATELIER-GLOSSAR

## GLOSSAR-FE-001 – Abstand oberhalb Hero zu groß
STATUS: LIVE PASS / 2026-09-13

NUTZER-READBACK:
Der obere Abstand ist korrekt. 0.2.9 verändert diesen Punkt nicht; Regression bleibt grün.

## GLOSSAR-FE-002 – Hero-Bild nicht responsive
STATUS: 0.2.8 LIVE FAIL / 0.2.9 TECHNISCHER FIX PASS / LIVE-READBACK 0.2.9 OFFEN

NUTZER-READBACK 0.2.8:
„Bild höher geworden aber kein responsive.“

KORREKTUR 0.2.9:
Das Bild selbst ist der Größenanker: normale responsive Bildgeometrie mit `width:100%` und `height:auto`; keine künstliche feste Bildhöhe und kein erzwungener 5:2-Hero-Container.

Echter Browser unter realem Design 1.50.469 misst:
- 1200px Viewport → Bild 1096 × 438.39
- 900px → 796 × 318.39
- 720px → 664 × 265.59
- 500px → 444 × 177.59

Natural image: 1400 × 560. Gerendertes Verhältnis bleibt gleich.

BELEG:
Run `34757795593`, Real-Design Job `103725094378` → `REAL_DESIGN_029_TRUE_RESPONSIVE_IMAGE_PASS`.

**Live nicht geschlossen**, bis Nutzer 0.2.9 real bestätigt.

## GLOSSAR-FE-003 – AJAX-Suche Frontenddarstellung
STATUS: 0.2.7 LIVE FAIL / 0.2.8 NUTZER HAT HIER KEINEN NEUEN FAIL GEMELDET / 0.2.9 REGRESSION PASS

0.2.9 prüft weiterhin reale Eingabe, Treffer und sichtbare Geometrie auf 1200/900/720/500.

BELEG:
Run `34757795593`, Job `103725094378` → `REAL_DESIGN_029_AJAX_PASS`.

## GLOSSAR-ROUTE-004 – Einzelbegriffe / Links laufen ins Leere
STATUS: 0.2.8 LIVE FAIL / 0.2.9 ROUTING-HARDLOCK TECHNISCH PASS / LIVE-READBACK OFFEN

NUTZER-READBACK 0.2.8:
„Einzelartikel laufen immer noch ins Leere.“

ENTSCHEIDENDE NEUE ABSICHERUNG:
Schema-Bump allein reicht nicht mehr als Beweis. 0.2.9 besitzt zusätzlich einen direkten `parse_request`-Binder für:
- `/glossar/begriff/{slug}/`
- `/glossar/{gruppe}/`

Der Hardtest löscht nach Installation **alle gespeicherten Glossar-Rewrite-Regeln**, während Schema 7 bereits als aktuell gespeichert bleibt. Damit kann kein weiterer Schema-Upgrade-Lauf den Test heimlich retten. Trotzdem müssen echte Kategorie- und Begriff-URLs funktionieren.

Zusätzlich klickt der Browser den tatsächlich gerenderten Hufbein-Link auf der Kategorie und verlangt anschließend:
- richtige Ziel-URL;
- genau ein `article.uge-single-wrap`;
- echten Hufbein-Inhalt/Sentinel.

Native eingeloggte Draft-Preview wird vom Direktbinder nicht übernommen und bleibt PASS.

BELEG:
Run `34757795593`:
- Fresh/Null-Rewrite `103725094537` SUCCESS
- 0.2.8 → 0.2.9 + erneuter Null-Rewrite `103725094620` SUCCESS
- Real Design + Null-Rewrite + echter Linkklick `103725094378` SUCCESS → `REAL_DESIGN_029_CLICKED_TERM_LINK_PASS`.

**Live nicht geschlossen**, bis Nutzer 0.2.9 real bestätigt.

## GLOSSAR-ROUTE-005 – Kategorien nicht dem Glossar-Design angepasst
STATUS: 0.2.8 LIVE FAIL / ALTE ACCEPTANCE FACHLICH FALSCH / 0.2.9 KORREKTUR TECHNISCH PASS / LIVE-READBACK OFFEN

NUTZER-READBACK 0.2.8:
„Kategorien immer noch nicht dem Design angepasst.“

GEFUNDENER TESTFEHLER:
Die 0.2.8-Acceptance verlangte ausdrücklich, dass Kategorien **keinen Hero und keine Tools** enthalten. Damit wurde genau das Gegenteil der Nutzeranforderung als PASS definiert.

VERBINDLICHE NUTZERANFORDERUNG:
Eine Kategorie besitzt eigenen Kategorieinhalt, verwendet aber denselben vollständigen visuellen Glossar-Rahmen wie die Startseite.

0.2.9 verlangt deshalb für `/glossar/gesundheit/` gleichzeitig:
- `.uge-category-head` + H1 `Gesundheit`;
- `.uge-hero`;
- `.uge-tools`;
- `.uge-topic-nav`;
- echte Begriffskarte/Link.

Hero-Kicker ist `WISSEN`.

BELEG:
Run `34757795593`, Job `103725094378` → `REAL_DESIGN_029_CATEGORY_FULL_SHELL_PASS`.

**Live nicht geschlossen**, bis Nutzer 0.2.9 real bestätigt.

## GLOSSAR-FE-006 – Echter Design-Integrationstest
STATUS: TECHNISCHE TESTLÜCKE GESCHLOSSEN

0.2.9 läuft weiterhin unter dem rekonstruierten echten Pferde-Design-Hauptcode 1.50.469, SHA-256:
`580fa6c7f5566f29df9254ce92f687a4831554e1d84bf03fbd936bb7577edfe5`.

Der bekannte 1.50.472-Projektstand unterscheidet sich in der dokumentierten 31.08.-Änderung im Kategorie-Editorialtext; der hier relevante Glossar-Runtime-/Layoutvertrag wurde im echten 1.50.469-Code ausgeführt. Kein Stub gilt als Real-PASS.

## GLOSSAR-REG-007 – Direktrouting zerstörte Draft-Preview
STATUS: RC1 ROT / RC2 REPARIERT / FINAL 0.2.9 PASS

Beim ersten 0.2.9-RC fing der neue Direktbinder auch eine authentifizierte WordPress-Draft-Preview ab. Die vorhandene Regression erkannte dies korrekt als 404.

RC2/final nimmt native Preview-Query-Parameter ausdrücklich vom Direktbinder aus. Danach:
`REG_PREVIEW_PASS`.

Dies ist ein echter RED→GREEN-Befund und wurde nicht übersprungen.

## ÜBERGREIFENDER STATUS

- 0.2.6: historisch / nicht verwenden.
- 0.2.7: LIVE FAIL / nicht verwenden.
- 0.2.8: **LIVE FAIL / nicht verwenden.**
- 0.2.9: **TECHNISCHER KANDIDAT HARDTEST PASS / PFERDE-LIVE-READBACK OFFEN.**

Finaler Run: `34757795593`
Head: `f2fa6f0c248acfa6978b5faec5daf42a40d0ba3b`

Installierbares ZIP:
`universal-glossary-engine-0.2.9.zip`

SHA-256:
`864befa0d159577e418906e4de3052ad0127b7dbcdad80775ba7e8f734ed1173`

Actions-Artefakt-ID: `10317444708`.

Die aktuellen Live-Fehler FE-002, ROUTE-004 und ROUTE-005 bleiben offen, bis der reale Nutzer-Readback exakt 0.2.9 bestätigt.
