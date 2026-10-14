# HOBBYRAUSCH – DESIGN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-14
STATUS: **1.50.655 LIVE FAIL / VERWORFEN / 1.50.656 AUF FUNKTIONIERENDEM 1.50.651-RUNTIME NEU GEBAUT / LOKALER RENDER-PASS / KEIN LIVE-PASS**

## Exakter Befund zu 1.50.655
1.50.655 ist verworfen.

Die Prüfung gegen den letzten funktionierenden 1.50.651-Stand zeigte:
- nicht nur Bilder/CSS waren geändert;
- in `class-hobby-depot-profile-v150651.php` waren auch funktionale Bild-/Mapping-Methoden verändert worden:
  - `next_level_card_photo()`
  - `hub2_image_map()`
  - `hub2_mapped_image_url()`
  - `hub2_card_photo()`
  - `hub2_hero_asset()`
- zusätzlich wurden neue Early-Returns eingebaut.
Damit war 1.50.655 entgegen der Vorgabe **kein reiner Bildfix auf unverändertem funktionierendem Runtime-Code**.
Der konkrete Live-Fatal wurde ohne Server-Fehlerlog nicht belastbar auf eine einzelne PHP-Zeile eingegrenzt; daher keine erfundene Ursache.

## 1.50.656 – Sicherheitsaufbau
Basis ist das echte funktionierende 1.50.651-Paket.

Unverändert gegenüber 1.50.651:
- Routinglogik;
- sämtliche aktiven Template-Dateien byte-identisch;
- sämtliche PHP-Methodenlogik für Hobby Depot;
- Profilklasse bleibt `Hobby_Depot_Profile_V150651`;
- aktive Templates bleiben `hobby-depot-front-v150651.php` und `hobby-depot-content-v150651.php`.

Geändert:
- Plugin-Version auf 1.50.656;
- Profil-RELEASE auf 1.50.656 für Cache-Busting;
- 65 neue Hero-Dateien wurden direkt an die bereits von 1.50.651 verwendeten alten Assetpfade kopiert;
- 65 neue 200×107-Vorschaubilder wurden direkt an die bereits von 1.50.651 verwendeten `*-v150634.webp`-Pfade kopiert;
- CSS-only: Claim/Pinselstrich nicht mehr als Flex-Item strecken;
- CSS-only: Hero-Anzeigeverhältnis auf 600×220.

## Lokale Prüfung 1.50.656
- kompletter PHP-Syntaxlauf PASS;
- Templates byte-identisch zu 1.50.651;
- gerenderter Hub2-Test `Druck & Fotografie` bis `RENDER_OK` PASS;
- Hero-URL im Render zeigt auf den bewährten 1.50.651-Pfad mit neuem Bild;
- 65 Hero-Quellen vorhanden und 600×220;
- 65 Vorschauen vorhanden und 200×107;
- ZIP-Integrität PASS.

Paket:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.656_HOBBY_DEPOT_651_RUNTIME_IMAGE_ONLY_FIX.zip`

SHA-256:
`1588afb145ca14de87188f22c22389f9a71f2cce456bce2c82e84f00c30ba0f7`

## EXAKT EINE NEXT ACTION
**1.50.655 nicht mehr verwenden. 1.50.656 installieren und nur /gestalten/druck-foto/ live prüfen. Erst nach realem Live-PASS weiterarbeiten.**
