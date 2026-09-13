# GLOSSAR – FEHLERQUELLEN

STAND: 2026-09-13
ROLLE: AUTORITATIVE FEHLERQUELLE FÜR DAS PFERDE-ATELIER-GLOSSAR

## GLOSSAR-FE-001 – Abstand oberhalb Hero zu groß
STATUS: KANDIDAT 0.2.6 TECHNISCH PASS / LIVE-SICHTPRÜFUNG OFFEN

BEFUND:
Auf der Glossar-Startseite war zusätzlicher Astra-Desktopabstand oberhalb des Hero sichtbar.

KANDIDAT-FIX:
Nur auf `body.uge-glossary-home` wird der zusätzliche `#primary`-Top-Margin entfernt. Keine globale Astra-Regel.

NACHWEIS:
GitHub Actions Run `34748541630` Fresh-Install + Upgrade PASS; lokaler exakter ZIP-Check bestätigt die eng begrenzte Regel und das Fehlen der früheren globalen Spacing-Hacks.

## GLOSSAR-FE-002 – Hero-Bild nicht responsive
STATUS: KANDIDAT 0.2.6 TECHNISCH PASS / LIVE-SICHTPRÜFUNG OFFEN

BEFUND:
Mobile Hero-Darstellung arbeitete mit fester Höhe `240px`.

KANDIDAT-FIX:
Responsive Regel mit `width:100%`, `max-width:100%`, `height:auto`, `aspect-ratio:16/9`, `object-fit:cover`.

NACHWEIS:
Run `34748541630` + lokaler exakter ZIP-Check; Negativprüfung bestätigt: `height:240px!important` ist im Kandidaten nicht vorhanden.

## GLOSSAR-ROUTE-003 – Einzelbegriffe/Artikel liefern weiße Seite
STATUS: FEHLERKLASSE TECHNISCH ABGESICHERT / EXAKTE LIVE-URSACHE NICHT BEWIESEN / LIVE-SICHTPRÜFUNG OFFEN

BEFUND:
Vom Nutzer beobachtet: Links auf einzelne Glossarbegriffe führten zu weißen Seiten.

WICHTIG:
Der konkrete Live-Zustand konnte nicht direkt ausgelesen werden. Deshalb keine behauptete Live-Rootcause.

HARTER REPRODUKTIONSNACHWEIS:
Im Upgrade-Test wurde unter 0.2.5 gezielt die Einzelbegriff-Rewrite-Regel entfernt. Danach war der bekannte Begriff `/glossar/begriff/hufbein/` nachweislich 404, während Schema 4 gespeichert blieb.

REPARATURWEG:
0.2.6 besitzt Rewrite-Schema 5. Der echte WordPress-Plugin-Updater überschreibt 0.2.5 mit 0.2.6; beim ersten normalen Request wird 4 → 5 migriert und die Regel neu aufgebaut.

POSITIV:
Danach liefert der Einzelbegriff 200 + echtes `<article class="uge-single-wrap">` + erwarteten Begriffinhalt.

NEGATIV:
Nicht vorhandener Begriff = 404; Entwurf = 404; Legacy-URL = 301; normale WordPress-Beiträge bleiben normale Beiträge; Kartenlinks müssen echten Glossar-Artikelmarkup enthalten und dürfen nicht nur HTTP 200 liefern.

NACHWEIS:
Run `34748541630`, Job `103700782306`.

## GLOSSAR-FE-004 – Breadcrumb auf Kategorieseiten falsch positioniert/dargestellt
STATUS: KANDIDAT 0.2.6 TECHNISCH PASS / LIVE-SICHTPRÜFUNG OFFEN

BEFUND:
Glossar-Breadcrumb lag auf der eigenen 1320px-Glossarachse und wich vom Pferde-Atelier-Standard ab.

KANDIDAT-FIX:
Breadcrumb folgt der Pferde-Atelier-Achse `--pftk-breadcrumb-axis-width` mit Fallback `900px` und der gebundenen Typografie.

DESIGN-ABGLEICH:
Vollständiger Designstand 1.50.469 wurde lokal auf Glossar-relevantes Verhalten geprüft. Der dokumentierte Live-Stand 1.50.472 verändert gegenüber 1.50.469 laut Design-Master weder CSS noch Breadcrumb, Bild, Karten oder Publish-Verhalten.

NACHWEIS:
Run `34748541630` + lokaler exakter ZIP-Check.

## ÜBERGREIFENDER STATUS

Technischer Kandidat: `Universal Glossary Engine 0.2.6`.
Branch: `hobbyroom/glossar-026-upgrade-hardtest-20260913`.
Gebundener Run: `34748541630`.
Innerer Plugin-ZIP SHA-256: `e0717db3aa247edc30b0fe84a261aa59037050d593e3432a6fb460f6d96f3b09`.

Kein Pferde-Atelier-LIVE-PASS aus diesen isolierten Tests ableiten. Die vier Punkte benötigen nach Installation des exakt hashgebundenen Kandidaten noch die reale Sicht-/Funktionsprüfung im Pferde Atelier.
