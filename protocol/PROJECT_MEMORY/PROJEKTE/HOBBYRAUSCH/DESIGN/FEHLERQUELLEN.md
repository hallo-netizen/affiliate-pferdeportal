# HOBBYRAUSCH – DESIGN – FEHLERQUELLEN

ROLLE: Autoritative Fehlerhistorie dieses Design-Scopes.  
Aktueller Status/NEXT ACTION ausschließlich aus `CURRENT_STATE.md`.

## HRD-001 – Startseite im WordPress-Blogloop

STATUS: CLOSED

Befund:
1.50.593/1.50.594 wurden innerhalb des WordPress-Blog-/Contentloops gerendert; sichtbar waren u. a. `Blog`, `TEST` und Theme-Footer.

Ursache:
Startseite wurde über den bestehenden Contentpfad eingeschoben statt den Root-/Frontpage-Rahmen vollständig zu übernehmen.

Korrektur:
ab 1.50.595 eigenes Fronttemplate.

## HRD-002 – Startseite wich vom freigegebenen Entwurf ab

STATUS: CLOSED FÜR CODEPFAD / LIVE-REGRESSIONSSCHUTZ AKTIV

Befund:
zu schmale/zu kleine Weltkarten, fehlende Mittelbereiche, falsche Portalnavigation, falsche dekorative Elemente.

Korrektur:
1.50.596–1.50.601 schrittweise auf freigegebenen Aufbau zurückgeführt; keine Community-/Shop-Navigation; 8 reale Welten; vollständiger Mittel-/Magazinbereich.

## HRD-003 – Hero-CTAs verschwinden bei Zwischenbreiten

STATUS: LOCAL CLOSED / LIVE OFFEN

Befund:
starre Hero-Geometrie konnte Buttons bei bestimmten Breiten abschneiden.

Korrektur:
flexible Herohöhe; definierte Tablet-/Mobile-Umschaltung; Mobile CTAs stapelbar.

Lokale Prüfung 1.50.601:
16 Breiten 320–1600 px, beide CTAs sichtbar/innerhalb des Hero, kein horizontaler Overflow.

## HRD-004 – Mega-Menü verschwindet beim Mausweg

STATUS: LOCAL CLOSED / LIVE OFFEN

Befund:
vertikale Hover-Lücke zwischen Trigger und Dropdown.

Korrektur:
Dropdown direkt an Navigation + Hover-Brücke; 0-px-Gap lokal gemessen.

## HRD-005 – Weltbilder sichtbar unscharf / unpassende Motive

STATUS: OPEN / LIVE-ABNAHME AUSSTEHEND

Befund:
frühere Weltbilder waren teilweise hochskalierte Mockup-Ausschnitte. Rein höhere Dateiabmessungen erzeugten keine echten Bilddetails. Zusätzlich waren Motive zu generisch; `Tiere = Hund` war fachlich falsch.

Stand 1.50.601:
- 8 unterschiedliche kontrollierte Weltassets;
- 1400×620;
- `Tiere` ohne Hund/Pfotenmotiv, Aquarium/Terrarium-Richtung;
- keine Weltfotos doppelt in Editorial-Karten;
- endgültige Schärfe muss live auf realem Display geprüft werden.

Falls weiterhin weich:
**nicht weiter schärfen/hochskalieren**, sondern betroffene Motive durch echte hochauflösende Originalbilder ersetzen.

## HRD-006 – Startseite unvollständig / TEST-Fallback

STATUS: LOCAL CLOSED / LIVE OFFEN

Korrektur 1.50.601:
- 3/3 redaktionelle Mittelkarten;
- `Wissen & Glossar` real gebunden;
- 5 reale Magazin-Themenseiten;
- kein TEST-Post-Fallback.

## Aktuell erster Fehler-/Abnahmeblocker

Live-Abnahme 1.50.601, mit besonderem Fokus auf:
1. echte Bildschärfe;
2. vollständige Startseite;
3. Header/Topbar;
4. Mega-Menü-Unterpunkte;
5. Desktop/Tablet/Mobile.
