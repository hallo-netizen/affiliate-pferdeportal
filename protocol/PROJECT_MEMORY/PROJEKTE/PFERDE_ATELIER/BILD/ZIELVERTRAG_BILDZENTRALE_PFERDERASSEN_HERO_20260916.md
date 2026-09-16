# ZIELVERTRAG – BILDZENTRALE / PFERDERASSEN-HERO

STAND: 2026-09-16
STATUS: AKTIV

## Ziel

Die allgemeingültige Bildzentrale besitzt einen generischen Custom-Post-Type-Hero-Weg. Im Pferde Atelier wird dieser Weg für den bestehenden Post Type `pa_breed` genutzt.

## Verbindliche Grenzen

1. Kein `pa_breed`-Hardcoding im allgemeinen Kern; der Ziel-Post-Type muss konfigurierbar sein.
2. Ohne gespeicherten geeigneten Post Type bleibt der Hero-Weg fail-closed.
3. Nur öffentliche Custom Post Types mit Beitragsbild-/Thumbnail-Unterstützung sind auswählbar.
4. Ein Hero wird als WordPress Featured Image des konkret gewählten Posts gesetzt.
5. Ausgabe für den neuen Hero-Weg: 3:1 / 1200 × 400 / WebP.
6. Nach Zuordnung sind Featured-Image-Readback und reale Dateiformatprüfung Pflicht.
7. Bei Readback-/Formatfehler wird die vorherige Featured-Image-Zuordnung wiederhergestellt.
8. Bestehende Beiträge-, WordPress-Taxonomie- und HivePress-Wege dürfen nicht regressieren.
9. Der neue Admin-Bereich `Post-Type-Hero` muss real bedienbar sein: sichtbarer Tab, Klick aktiviert exakt CPT-Button + CPT-Panel; unbekannte oder fehlende Zielpanels bleiben fail-closed.
10. Das Pferde-Design wird nicht ohne nachgewiesenen Bedarf umgebaut. Die vorhandene Fallback-Logik soll zuerst das Featured Image und nur ohne dieses das Standardbild verwenden.
11. Das Wasserzeichen-Konzept ist ausdrücklich nicht Teil dieses Releases; siehe `TODO.md` → `TODO-BILD-WASSERZEICHEN-001`.

## Ausgangsquelle

`ALLGEMEINGUELTIGE_BAUSTEINE/BILDZENTRALE/`  
letzter sicherer LIVE-Ausgang: Version 2.6.9  
Release-Beleg: `ALLGEMEINE_BILDZENTRALE_2.6.9_PROMPTGRENZE_REPARIERT.zip`  
SHA-256: `748f77602bc3d4f64bd24a2f163c53829f0c1e8dc2102a82a642ceb4778e160e`

Zwischenkandidat 2.7.0:
`ALLGEMEINE_BILDZENTRALE_2.7.0_CUSTOM_POST_TYPE_HERO_INSTALLIEREN.zip` / SHA-256 `8403bf1ad06be7c6102c37c53648826663fdcbebbe73d27e011364fab51dc5e4`  
Status: **verworfen als LIVE-Kandidat** – realer WordPress-Befund `Post-Type-Hero` sichtbar, aber nicht anklickbar.

## Zielrelease

Version **2.7.1**  
Datei: `ALLGEMEINE_BILDZENTRALE_2.7.1_POST_TYPE_HERO_TAB_FIX_INSTALLIEREN.zip`  
SHA-256: `4453a39dfda7adc7a849428eca41c8ee0d2410a705011c7c254616a789ad0d21`

Der aktuelle Prüf-/LIVE-Stand wird hier bewusst nicht als zweite Standwahrheit gepflegt. Dafür gelten ausschließlich `CURRENT_STATE.md`, `HOBBYRAUM.md` und der gebundene Testreport.

## PASS-Bedingung

LOCAL PASS:
- PHP-/ZIP-/Versions-/Hashprüfung PASS;
- sichtbarer `Post-Type-Hero`-Tab besitzt ein gültiges `cpt`-Panel-Mapping;
- Klick auf `Post-Type-Hero` aktiviert exakt CPT-Button + CPT-Panel;
- alle bestehenden Haupttabs bleiben klickbar;
- unbekannter Tab / fehlendes Zielpanel bleiben fail-closed;
- positiver `pa_breed`-Pfad PASS;
- falscher Post Type BLOCK PASS;
- leere Konfiguration BLOCK PASS;
- reale 1200×400-WebP-Ausgabe PASS;
- Featured-Image-Readback PASS;
- Rollback bei abweichendem Readback PASS;
- Regression der bisherigen Bildwege PASS;
- Design-Fallback statisch nachgewiesen.

LIVE PASS erst nach:
1. Version 2.7.1 in WordPress installiert;
2. `Post-Type-Hero` real per Klick geöffnet;
3. `pa_breed` als Post-Type-Hero-Ziel gespeichert;
4. für mindestens eine reale Pferderasse ein Hero erzeugt und zugeordnet;
5. WordPress-Readback bestätigt das Featured Image;
6. Frontend zeigt das spezifische Rassenbild und nicht mehr das Standard-Fallback;
7. eine Rasse ohne spezifisches Bild zeigt weiterhin das Standard-Fallback.
