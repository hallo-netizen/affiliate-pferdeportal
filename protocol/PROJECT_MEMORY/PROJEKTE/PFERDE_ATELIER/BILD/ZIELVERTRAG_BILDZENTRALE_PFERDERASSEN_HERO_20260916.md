# ZIELVERTRAG – BILDZENTRALE / PFERDERASSEN-HERO

STAND: 2026-09-16
REVISION: 2
STATUS: AKTIV / TECHNISCHER ZIELWEG 2.7.6 ERREICHT

## Ziel

Die allgemeingültige Bildzentrale besitzt einen generischen Custom-Post-Type-Hero-Weg. Im Pferde Atelier wird dieser Weg für den bestehenden Post Type `pa_breed` genutzt. Für den vorhandenen Rassenbestand steht zusätzlich ein sicherer serieller Batchhelfer zur Verfügung.

## Verbindliche Grenzen

1. Kein `pa_breed`-Hardcoding im allgemeinen Hero-Kern; der Ziel-Post-Type bleibt konfigurierbar.
2. Ohne gespeicherten geeigneten Post Type bleibt der Hero-Weg fail-closed.
3. Nur öffentliche Custom Post Types mit Beitragsbild-/Thumbnail-Unterstützung sind auswählbar.
4. Ein Hero wird als WordPress Featured Image des konkret gewählten Posts gesetzt.
5. **Aktuelles Zielprofil des `post_type_hero`-Rassenwegs: 21:9 / 1260 × 540 / WebP.** Der ursprüngliche Vertragsstand 3:1 / 1200 × 400 ist mit Revision 2 abgelöst.
6. Für diesen Rassen-Hero-Weg findet kein nachgelagerter lokaler 3:1-Recrop statt.
7. Nach Zuordnung sind Featured-Image-Readback und reale Dateiformatprüfung Pflicht.
8. Bei Readback-/Formatfehler wird die vorherige Featured-Image-Zuordnung wiederhergestellt.
9. Bestehende Beiträge-, WordPress-Taxonomie- und HivePress-Wege dürfen nicht regressieren.
10. Der Admin-Bereich `Post-Type-Hero` muss real bedienbar sein: sichtbarer Tab, Klick aktiviert exakt CPT-Button + CPT-Panel; unbekannte oder fehlende Zielpanels bleiben fail-closed.
11. Der Pferde-Designweg nutzt das Featured Image und nur ohne dieses das Standardbild; kein vorsorglicher Designumbau.
12. Der optionale Pferderassen-Batch verarbeitet ausschließlich `pa_breed`, nur Rassen ohne Featured Image, seriell genau eine Aufgabe gleichzeitig und überschreibt kein vorhandenes Featured Image.
13. Standard-Batchgröße: die nächsten 10 offenen Rassen. Daraus folgt kein Anspruch auf automatische Vollbebilderung des Gesamtbestands.
14. Das Wasserzeichen-Konzept ist ausdrücklich nicht Teil dieses Releases; siehe `TODO.md` → `TODO-BILD-WASSERZEICHEN-001`.

## Ausgang / Historie

Sicherer historischer Ausgang: 2.6.9.

2.7.0: LIVE FAIL – `Post-Type-Hero` sichtbar, aber nicht anklickbar.
2.7.1: Tab-Mapping repariert.
2.7.2–2.7.5: Rassen-Hero-Weg bis zum aktuellen 21:9-Zielprofil weitergeführt.
2.7.6: sicherer serieller Rassen-Batchhelfer ergänzt.

Historische Zwischenstände bleiben im Protokoll; sie sind nicht CURRENT.

## Aktuelles Zielrelease

Version **2.7.6**

Datei:
`ALLGEMEINE_BILDZENTRALE_2.7.6_RASSEN_BATCH_AUTOMATIK_INSTALLIEREN.zip`

SHA-256:
`12edc4405560ac3b149cf76a0b6e65694337b1533c0ea5e3a777d3b6c98ccbf0`

Der aktuelle Stand selbst wird nicht hier doppelt gepflegt. Dafür gelten ausschließlich `CURRENT_STATE.md` und `HOBBYRAUM.md`.

## PASS-Bedingung

LOCAL PASS:
- PHP-/ZIP-/Versions-/Hashprüfung PASS;
- `Post-Type-Hero` bedienbar / fail-closed bei ungültigem Ziel;
- positiver `pa_breed`-Pfad PASS;
- 21:9 / 1260×540-Ausgabe ohne nachgelagerten 3:1-Recrop PASS;
- Featured-Image-Readback / Rollback PASS;
- Batchscope ausschließlich `pa_breed` PASS;
- serieller Ablauf PASS;
- No-Overwrite vorhandener Featured Images PASS;
- Regression der bisherigen Bildwege PASS.

LIVE-FUNKTION PASS:
- realer Rassen-Hero-Weg in WordPress funktionsfähig;
- serieller 10er-Batch startet und verarbeitet Rassen ohne vorhandenes Featured Image ohne gemeldeten Systemfehler.

Eine vollständige Bebilderung aller Rassen ist eine separate Bestandsaufgabe und keine PASS-Bedingung dieses Technikvertrags.
