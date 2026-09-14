# GLOSSAR – HOBBYRAUM

STAND: 2026-09-14
STATUS: BLOCKED

## 1-KLICK-ÜBERSICHT

**AKTUELLER SICHERER BEFUND**  
Einzelartikel öffnen real → **LIVE PASS**. Die Einzelansicht selbst ist weiter **LIVE FAIL**: Breadcrumb falsch/doppelt, Links im Fließtext, rechte Ockerlinie zu dick. Bestehende Begriffe müssen nach der neuen Regel überschrieben werden.

**VERBINDLICHE NEUE REGEL**  
Glossar-Fließtext enthält **0 Links**. Links stehen nur rechts in `Verwandte Begriffe` und `Mehr zum Thema`.

**DU DARFST …**  
nur diese offene Single-/Bestandsreparatur fortsetzen und die neuen Pakete 1.2.2 / 1.50.490 real prüfen.

**DU DARFST NICHT …**  
den bestätigten Routingweg umbauen, normale WordPress-Posts verändern, bestehende Glossarbeiträge löschen statt aktualisieren oder lokale Tests als LIVE PASS ausgeben.

## ARBEITSORT

Branch:
`hobbyroom/glossar-livefail-red-green-20260913`

Autoritative Fehlerquelle:
`FEHLERQUELLEN.md`

Autoritativer Stand:
`CURRENT_STATE.md`

Verbindliche Text-/Linkregeln:
`TEXT_UND_LINKREGELN.md`

## LOKALER KANDIDAT

### Core 1.2.2
`UNIVERSAL_GLOSSARY_ENGINE_1.2.2_ZERO_BODY_LINKS_BESTAND_UPDATE_INSTALLIEREN.zip`

SHA-256:
`3d6ffc2cdfcc4872e49e97f4adc54de31d4ef2714b0af07e399a681f15d1f447`

PASS lokal:
- 14 gebundene Begriffe 150–200 Wörter;
- 0 Links im Fließtext;
- bestehende `uge_term` werden per gleicher ID aktualisiert;
- normaler Post Negativtest unverändert;
- ZIP/Version PASS.

### Design 1.50.490
`PFERDE_ATELIER_DESIGN_V1.50.490_GLOSSAR_BREADCRUMB_STRIPE_FIX_INSTALLIEREN.zip`

SHA-256:
`251e90a7c7115cd4ce166ddefb5f0918904f28b89d85f2a173c190201b454657`

PASS lokal:
- globaler Breadcrumb auf `uge_term` serverseitig ausgeschaltet + CSS-Failsafe;
- eigener Breadcrumb `Startseite > Glossar > Oberbereich > Begriff`;
- Fließtext-Renderendstufe entfernt Restlinks;
- rechte Box-Oberkante 4 px → 2 px;
- Scope ausschließlich `uge_term`;
- ZIP/Version PASS.

## WARUM BLOCKED

Die Pakete sind **noch nicht live installiert/readback-bestätigt**. Deshalb bleibt `GLOSSAR-SINGLE-011` LIVE FAIL und kein LIVE-/Release-PASS wird behauptet.

## NEXT ACTION – EXAKT

1. Core `1.2.2` über den vorhandenen Glossar-Core installieren.
2. Design `1.50.490` über das vorhandene Designplugin installieren.
3. `Bandmaß` real neu laden.
4. Prüfen:
   - Breadcrumb exakt `Startseite > Glossar > Pferd & Biologie > Bandmaß`;
   - Fließtext **0 Links**;
   - `Stockmaß` rechts in `Verwandte Begriffe` als Link;
   - Portalziel rechts in `Mehr zum Thema`;
   - Ockerlinie rechts 2 px / sichtbar dünner;
   - bestehende URL/ID erhalten.
5. normalen WordPress-Beitrag negativ prüfen.
6. Erst nach Nutzerreadback LIVE PASS und Plugin-Artefaktsync.

## NICHT ANFASSEN

- funktionierenden Single-Routingweg;
- normale WordPress-Posts/Seiten;
- `main` als Experimentierfläche;
- WDB-Fakten ohne `GEPRUEFT`;
- Bestandsbegriffe nicht löschen.
