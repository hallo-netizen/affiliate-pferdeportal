# HD-007 – HOBBYREGISTER CORE – FEHLERQUELLEN

ROLLE: Autoritative Fehlerchronik für HD-007. Kein CURRENT, keine eigene NEXT ACTION.
Aktueller Stand ausschließlich aus `CURRENT.md`.

## HD007-20261023-01 – Breite mehrfach falsch nachgebaut
STATUS: CLOSED

BEFUND:
Mehrere Zwischenstände 1.2.1–1.2.9 versuchten die Hobbyregister-Breite über eigene Pixelwerte bzw. eine falsche Pferdeatelier-Referenz nachzubauen. Dadurch blieb die sichtbare Breite abweichend.

URSACHE:
Die numerische Breite wurde kopiert, statt denselben echten Hobby-Depot-Container wie HD-003 zu verwenden.

FIX:
Ab 1.2.10 verwendet HD-007 denselben Hobby-Depot-Containerpfad:
- `hd-content-v150616`
- `hd-portal-section`
- `hd-breadcrumb-wrap`

NACHWEIS:
Lokaler Chromium-Vergleich Kategorie gegen Hobbyregister bei 1600/1440/1366/1180/1024/761/760/390 px jeweils 0 px Differenz an linker Kante, rechter Kante und Gesamtbreite. Nutzer bestätigte anschließend den Live-Stand mit „pass“.

## HD007-20261023-02 – Kritischer Fehler nach 1.2.6
STATUS: CLOSED / LIVE-STACK NICHT GESICHERT

BEFUND:
Nach Installation von 1.2.6 meldete WordPress einen kritischen Fehler.

GRENZE:
Der exakte Live-PHP-Stack wurde nicht gesichert. Daher keine erfundene Live-Ursache.

LOKAL REPRODUZIERT:
Eine doppelte Hobbyregister-Ladung konnte Klassen-/Funktionskollisionen und einen PHP-Fatal auslösen.

FIX:
1.2.6 vollständig verworfen. 1.2.7 kehrte auf den stabilen JSON-Laufzeitweg zurück und machte den Runtime-Pfad kollisionsrobuster. Spätere Stände bauen auf dem stabilisierten Stamm weiter.

NACHWEIS:
Doppelplugin-Simulation alt→neu und neu→alt PASS; danach Website wieder erreichbar.

## HD007-20261023-03 – Register/Artikel zeitweise nicht gefunden
STATUS: CLOSED FÜR AKTUELLEN LOKALEN STAND

BEFUND:
Zwischenstände zeigten live „Hobby wurde im Register nicht gefunden“ bzw. fehlende Artikel.

GRENZE:
Der exakte Live-Serverzustand war nicht vollständig gesichert; deshalb keine unbelegte Ursachenbehauptung.

NACHWEIS AKTUELL:
1.2.13 Fresh-Unpack enthält 862 Registerdatensätze und 862 Artikel; lokale Runtime-Simulation rendert 862/862 Detailseiten und die Registerübersicht.

## HD007-20261023-04 – Bildproduktion erzeugte Dubletten/falsches Vorgängermotiv
STATUS: PROZESSFEHLER GESCHLOSSEN / AUSSCHUSS DOKUMENTIERT

BEFUND:
Bei der Bildgenerierung wurden wiederholt nahezu identische Geocaching-, Telefon-, Werbe- und Werkzeugmotive erzeugt bzw. das Vorgängermotiv trotz Themenwechsel fortgeführt.

REGEL:
- 1 Hobby = 1 finales Masterbild;
- Dubletten und Fehlversuche zählen nicht als DONE;
- gleiches 3:2-Master für Hero + Beitrag;
- keine Collagen.

KONSEQUENZ:
Nur 14 eindeutig ausgewählte/verifizierte 1500×1000-Master sind final DONE. Zusätzliche Varianten wurden nicht als final übernommen.

## HD007-20261023-05 – 382 CORE-Bildkandidaten nicht mastertauglich
STATUS: OFFEN ALS BILDPRODUKTIONSBEDARF / KEIN PLUGIN-RUNTIME-FEHLER

PRÜFUNG:
- 382/382 CORE-Zuordnungen;
- 212/212 unterschiedliche Bilddateien visuell geprüft;
- 81 semantisch passend;
- 301 semantisch unpassend;
- 0/382 technisch als 1500×1000-Master ohne Hochskalieren geeignet.

GRUND:
Kein vorhandener CORE-Kandidat erreicht 1000 px Höhe; vorhandene Kandidaten reichen technisch nicht für den verbindlichen gemeinsamen Hero+Beitrag-Master.

DETAILNACHWEIS:
`EVIDENCE_1.2.13_CORE_IMAGE_AUDIT.md`

Aktueller Status und genau eine NEXT ACTION ausschließlich:
`CURRENT.md`.
