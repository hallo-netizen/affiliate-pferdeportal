# GLOSSAR – FEHLERQUELLEN

STAND: 2026-09-13
ROLLE: AUTORITATIVE FEHLERQUELLE FÜR DAS PFERDE-ATELIER-GLOSSAR

## GLOSSAR-FE-001 – Abstand oberhalb Hero zu groß
STATUS: KANDIDAT 0.2.7 TECHNISCH PASS / LIVE-SICHTPRÜFUNG OFFEN

BEFUND:
Auf der Glossar-Startseite war zusätzlicher Astra-Desktopabstand oberhalb des Hero sichtbar.

KANDIDAT-FIX:
Nur auf `body.uge-glossary-home` wird der zusätzliche `#primary`-Top-Margin entfernt. Keine globale Astra-Regel.

NACHWEIS:
Run `34749231699` Fresh + Update PASS; exakter 0.2.7-ZIP lokal erneut geprüft.

## GLOSSAR-FE-002 – Hero-Bild nicht responsive
STATUS: KANDIDAT 0.2.7 TECHNISCH PASS / LIVE-SICHTPRÜFUNG OFFEN

BEFUND:
Mobile Hero-Darstellung arbeitete mit fester Höhe `240px`.

KANDIDAT-FIX:
Responsive Regel mit `width:100%`, `max-width:100%`, `height:auto`, `aspect-ratio:16/9`, `object-fit:cover`.

NACHWEIS:
Run `34749231699`; Negativprüfung bestätigt, dass die alte feste Mobile-Höhe im Kandidaten nicht mehr aktiv ist.

## GLOSSAR-ROUTE-003 – Einzelbegriffe/Artikel liefern weiße Seite
STATUS: FEHLERKLASSE TECHNISCH ABGESICHERT / EXAKTE LIVE-URSACHE NICHT BEWIESEN / LIVE-SICHTPRÜFUNG OFFEN

BEFUND:
Vom Nutzer beobachtet: Links auf einzelne Glossarbegriffe führten zu weißen Seiten.

WICHTIG:
Der konkrete Live-Zustand wurde nicht direkt ausgelesen. Deshalb keine behauptete Live-Rootcause.

HARTER REPRODUKTIONSNACHWEIS:
Im Upgrade-Test wurde unter 0.2.5 gezielt die Einzelbegriff-Rewrite-Regel entfernt. Danach war `/glossar/begriff/hufbein/` 404, während Schema 4 gespeichert blieb.

REPARATURWEG:
0.2.7 enthält Rewrite-Schema 5. Der echte WordPress-Plugin-Updater überschreibt 0.2.5 mit 0.2.7. Ein möglicher unmittelbar noch alter Apache-Opcode wird sichtbar protokolliert; nach normaler OPcache-Revalidierung muss Schema 4 → 5 wechseln und die Rewrite-Regel neu aufgebaut sein.

POSITIV:
Danach liefert der Einzelbegriff 200 + echtes `<article class="uge-single-wrap">` + erwarteten Begriffinhalt.

NEGATIV:
Nicht vorhandener Begriff = 404; Entwurf = 404; Legacy-URL = 301; normale WordPress-Beiträge bleiben unverändert; Kartenlinks müssen echten Glossar-Artikelinhalt liefern und dürfen nicht nur HTTP 200 ergeben.

NACHWEIS:
Run `34749231699`, Job `103702569602`.

## GLOSSAR-FE-004 – Breadcrumb auf Kategorieseiten falsch positioniert/dargestellt
STATUS: KANDIDAT 0.2.7 TECHNISCH PASS / LIVE-SICHTPRÜFUNG OFFEN

BEFUND:
Glossar-Breadcrumb lag auf der eigenen 1320px-Glossarachse und wich vom Pferde-Atelier-Standard ab.

KANDIDAT-FIX:
Breadcrumb folgt der Pferde-Atelier-Achse `--pftk-breadcrumb-axis-width` mit Fallback `900px` und der gebundenen Typografie.

DESIGN-ABGLEICH:
Vollständiger Designstand 1.50.469 wurde lokal auf Glossar-relevantes Verhalten geprüft. Der dokumentierte Live-Stand 1.50.472 verändert gegenüber 1.50.469 laut Design-Master weder CSS noch Breadcrumb, Bild, Karten oder Publish-Verhalten.

NACHWEIS:
Run `34749231699` + lokaler exakter 0.2.7-ZIP-Check.

## ÜBERGREIFENDER STATUS

Aktueller technischer Übergabekandidat:
`Universal Glossary Engine 0.2.7`.

0.2.6 ist Entwicklungs-/Testhistorie und kein aktueller Übergabekandidat.

Branch:
`hobbyroom/glossar-027-release-hardtest-20260913`.

Gebundener Run:
`34749231699`.

Innerer Plugin-ZIP SHA-256:
`e9c32fc64db3c64c3b85e0d2692ff200e8f6d60e5827d7ab514657adff2ae831`.

Kein Pferde-Atelier-LIVE-PASS aus diesen isolierten Tests ableiten. Die vier Punkte benötigen nach Installation des exakt hashgebundenen 0.2.7-Kandidaten noch reale Sicht-/Funktionsprüfung im Pferde Atelier.
