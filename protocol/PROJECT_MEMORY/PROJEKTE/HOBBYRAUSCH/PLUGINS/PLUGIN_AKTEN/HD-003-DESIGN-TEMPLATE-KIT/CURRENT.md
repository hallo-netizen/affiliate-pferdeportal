# HD-003 – HOBBY DEPOT DESIGN / TEMPLATE KIT – CURRENT

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-18
STATUS: **LIVE 1.50.677 / 1.50.678 LETZTER GEBAUTER KANDIDAT / 1.50.679 HUB2-ROLLOUT VORBEREITET / KEIN RELEASE-PASS**

## Letzter gebauter Kandidat

AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.678_HOBBY_DEPOT_DYNAMIC_TEXTSAFE_HERO_HARDPASS.zip

SHA-256:
33e35ef638c3564b03343deda6d420f20a85bb387949d017cc75f1d2d9f629f5

Der frühere Local-Hard-PASS bleibt zurückgezogen.

## Neuer verbindlicher Scope 1.50.679

Alle aktuell **69 Hub2-Seiten**:
- Audio-&-HiFi-Fullbleed-/dynamische Beige-Regel portalweit;
- Desktop H1, Claim und Kurzzeile einzeilig;
- <=900 px gestapelt;
- 69 eigenständig redigierte 150–200-Wörter-Kategorietexte statt Generator-Schablone;
- sichtbar ungefähr ein Drittel, nie mehr als die Hälfte;
- Rest über kleinen Chevron/Pfeil aufklappbar;
- kein sichtbarer `Mehr zu <Kategorie> erfahren`-Text;
- zugängliche Screenreader-Beschriftung bleibt;
- kein Hub2-Seitenendtext.

## QA DES VORBEREITETEN ROLLOUTS

Synthetische Kompatibilitätsprüfung:
- 69/69 aktuelle Hub2-Slugs getroffen;
- Texte 150–174 Wörter;
- sichtbare Leads 45–64 Wörter;
- PHP-Lint ohne Fehler;
- 69/69 Test-Render ohne Fehler;
- alte feste Textschablone im Kandidatenpfad entfernt;
- Release-Kette im Testaufbau auf 1.50.679 geschlossen.

Diese Prüfung lief bewusst nur auf einer zugänglichen älteren Quellkopie und ist **kein installierbarer Release-Nachweis**.

## OFFENER RELEASE-BLOCKER

Finales 1.50.679 muss aus dem exakten 1.50.678-Paket gebaut werden. Ein Neuaufbau auf älterer Quelle würde spätere Hero-/Bild-/Responsive-Korrekturen riskieren und ist verboten.

## EXAKT EINE NEXT ACTION

**1.50.679 auf exakter 1.50.678-Quellbasis bauen und anschließend Positiv-/Negativ-/Regressionstest des realen Plugin-Renderpfads durchführen. Vorher kein WordPress-Upload.**
