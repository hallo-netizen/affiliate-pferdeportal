# ZIELVERTRAG – BILDZENTRALE / PFERDERASSEN-HERO

STAND: 2026-09-16
STATUS: AKTIV

## Ziel

Die allgemeingültige Bildzentrale wird um einen generischen Custom-Post-Type-Hero-Weg erweitert. Im Pferde Atelier wird dieser Weg für den bestehenden Post Type `pa_breed` genutzt.

## Verbindliche Grenzen

1. Kein `pa_breed`-Hardcoding im allgemeinen Kern; der Ziel-Post-Type muss konfigurierbar sein.
2. Ohne gespeicherten geeigneten Post Type bleibt der Hero-Weg fail-closed.
3. Nur öffentliche Custom Post Types mit Beitragsbild-/Thumbnail-Unterstützung sind auswählbar.
4. Ein Hero wird als WordPress Featured Image des konkret gewählten Posts gesetzt.
5. Ausgabe für den neuen Hero-Weg: 3:1 / 1200 × 400 / WebP.
6. Nach Zuordnung sind Featured-Image-Readback und reale Dateiformatprüfung Pflicht.
7. Bei Readback-/Formatfehler wird die vorherige Featured-Image-Zuordnung wiederhergestellt.
8. Bestehende Beiträge-, WordPress-Taxonomie- und HivePress-Wege dürfen nicht regressieren.
9. Das Pferde-Design wird nicht ohne nachgewiesenen Bedarf umgebaut. Die vorhandene Fallback-Logik soll zuerst das Featured Image und nur ohne dieses das Standardbild verwenden.
10. Das Wasserzeichen-Konzept ist ausdrücklich nicht Teil dieses Releases; siehe `TODO.md` → `TODO-BILD-WASSERZEICHEN-001`.

## Ausgangsquelle

`ALLGEMEINGUELTIGE_BAUSTEINE/BILDZENTRALE/`  
Version 2.6.9  
Release-Beleg: `ALLGEMEINE_BILDZENTRALE_2.6.9_PROMPTGRENZE_REPARIERT.zip`  
SHA-256: `748f77602bc3d4f64bd24a2f163c53829f0c1e8dc2102a82a642ceb4778e160e`

## Zielrelease

Version 2.7.0  
Datei: `ALLGEMEINE_BILDZENTRALE_2.7.0_CUSTOM_POST_TYPE_HERO_INSTALLIEREN.zip`

Der aktuelle Prüf-/LIVE-Stand wird hier bewusst nicht dupliziert. Dafür gelten ausschließlich `CURRENT_STATE.md`, `HOBBYRAUM.md` und der gebundene Testreport.

## PASS-Bedingung

LOCAL PASS:
- PHP-/ZIP-/Versions-/Hashprüfung PASS;
- positiver `pa_breed`-Pfad PASS;
- falscher Post Type BLOCK PASS;
- leere Konfiguration BLOCK PASS;
- reale 1200×400-WebP-Ausgabe PASS;
- Featured-Image-Readback PASS;
- Rollback bei abweichendem Readback PASS;
- Regression der bisherigen Bildwege PASS;
- Design-Fallback statisch nachgewiesen.

LIVE PASS erst nach:
1. Version 2.7.0 in WordPress installiert;
2. `pa_breed` als Post-Type-Hero-Ziel gespeichert;
3. für mindestens eine reale Pferderasse ein Hero erzeugt und zugeordnet;
4. WordPress-Readback bestätigt das Featured Image;
5. Frontend zeigt das spezifische Rassenbild und nicht mehr das Standard-Fallback;
6. eine Rasse ohne spezifisches Bild zeigt weiterhin das Standard-Fallback.
