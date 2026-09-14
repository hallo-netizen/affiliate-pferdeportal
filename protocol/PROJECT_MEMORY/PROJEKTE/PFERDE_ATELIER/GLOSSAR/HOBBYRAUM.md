# GLOSSAR – HOBBYRAUM

STAND: 2026-09-14
STATUS: BLOCKED

## AKTUELLER SICHERER BEFUND

LIVE PASS und **nicht mehr anfassen**:
- Einzelartikel öffnen;
- Glossar-Fließtext enthält 0 Links;
- rechte Ockerlinie ist dünn.

LIVE offen:
- Breadcrumb-Abstand nach oben auf allen Glossarseiten einheitlich verkleinern;
- komplette Begriffskacheln anklickbar machen;
- Glossar-Hero weiter herauszoomen / Motiv erkennbar machen.

## ARBEITSORT

Branch: `hobbyroom/glossar-livefail-red-green-20260913`

Autorität:
- `CURRENT_STATE.md`
- `FEHLERQUELLEN.md`
- `TEXT_UND_LINKREGELN.md`
- Fachfakten ausschließlich WDB Glossar.

## LOKALE KANDIDATEN

### Core 1.2.3
`UNIVERSAL_GLOSSARY_ENGINE_1.2.3_NEUE_BEITRAEGE_INSTALLIEREN.zip`

SHA-256: `997cd888fe3ea1a102a8d5c9e614497404d5049e5c64086f330f0dc77c07049f`

- 14 bisherige Bestandsbegriffe weiter im Updateweg;
- `Aalstrich` zusätzlich aus WDB `GEPRUEFT` übernommen/überschrieben;
- `Zuchtbuch` neu aus WDB `GEPRUEFT` ergänzt;
- beide 150–200 Wörter und 0 Fließtextlinks;
- State `1.2.3:16`;
- lokale Syntax-/Vertrags-/ZIP-Prüfung PASS.

### Design 1.50.491
`PFERDE_ATELIER_DESIGN_V1.50.491_GLOSSAR_NAV_HERO_FIX_INSTALLIEREN.zip`

SHA-256: `e5913fd60b59ce6b49a354a98f0f2bd132df6356720ed8d5ee76309abd811d51`

- einheitlicher Topabstand 18 px auf Glossar-Startseite, Gruppe und Single;
- ganze Begriffskachel ist Link;
- Hero zeigt mit `contain` und rechter Ausrichtung deutlich mehr vom Originalmotiv;
- bestätigte 0-Link- und 2-px-Regeln bleiben bestehen;
- lokale Syntax-/Vertrags-/ZIP-Prüfung PASS.

## NEXT ACTION – EXAKT

1. Core `1.2.3` installieren.
2. Design `1.50.491` installieren.
3. LIVE prüfen: Startseite, eine Gruppe und `Bandmaß` auf identischem Breadcrumb-Topabstand.
4. komplette Kachel `Bandmaß` außerhalb des CTA anklicken.
5. Hero visuell prüfen: Bücher/Pferdelexikon müssen als Motiv verständlich sein.
6. Regression: 0 Fließtextlinks und dünne Ockerlinie bleiben PASS.
7. `Aalstrich` und `Zuchtbuch` öffnen und real prüfen.
8. Erst danach LIVE PASS / Artefaktsync.

## NICHT ANFASSEN

- funktionierenden Routingweg;
- normale Posts/Seiten;
- 0-Link-Regel;
- dünne Ockerlinie;
- ungeprüfte WDB-Begriffe.
