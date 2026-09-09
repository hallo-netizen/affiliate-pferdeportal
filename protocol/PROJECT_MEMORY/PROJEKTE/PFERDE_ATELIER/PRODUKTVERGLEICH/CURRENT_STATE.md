# PRODUKTVERGLEICH – CURRENT STATE

STAND: 2026-09-09
STATUS: AKTIV / 0.8.2 LOKAL HART PASS + WORDPRESS-LIVE-CACHE-REUSE PASS

## AUTORITÄT

Diese Datei ist die einzige aktuelle Büro-Standzusammenfassung.

- aktuelle Arbeit: `HOBBYRAUM.md`
- Fehlerdetails: `FEHLERQUELLEN.md`
- Ziel: `ZIELVERTRAG_V1.md`
- lokaler Prüfbeleg: `AKTENSCHRANK/03_V082_HARD_LOCAL_RELEASE_RECEIPT.md`
- Live-Beleg: `AKTENSCHRANK/04_V082_WORDPRESS_LIVE_CACHE_REUSE_RECEIPT.md`

## AKTUELLER KANDIDAT

`universal-product-comparison-0.8.2-prototype.zip`

SHA-256:
`6f0f1f8d62870fd2cd1ee34010c1b157d9ac140327e46cd8a6d0b48a1a05f2ad`

Aktuelle Stufe:
`Produktwissen -> Vergleichbarkeit -> bidirektionales SEO -> persistente Produkt-/Paar-Zwischenevidenz -> aktuelle Readiness/Kannibalisierung -> Dossier -> unabhängiger Abschluss-Audit`

Writer/Draft/Publish bleiben in dieser Prüfstufe dormant.

## KISS-FIX 0.8.2

0.8.1 speicherte den fertigen Kandidatenbefund 90 Tage, verließ sich für Produkt-/Paar-Zwischenergebnisse aber zusätzlich auf den nativen PSTE-Providercache von 24 Stunden.

0.8.2 speichert deshalb hash-gebunden und autoload=false:
- Produktabfrage;
- Paarabfrage;
- bereits erfolgreich bezahlte Teilantworten;
- positiv UND negativ;
- 90 Tage.

Reihenfolge:
`persistente UPC-Zwischenevidenz -> PSTE-Cache -> nur fehlender Provider-Endpunkt`.

Abgelaufen, Kontextdrift oder manipuliert => nicht still weiterverwenden.

## HARTER LOKALBELEG

Exakte finale Fresh-ZIP:
- komplette Regression 20/20 PASS;
- PHP-Lint 40/40 PASS;
- Source↔finale ZIP 51/51 exakt;
- Report-Hashbindung 50/50 exakt;
- echte Product-Knowledge-0.5.0-Abhängigkeit SHA PASS;
- echter PSTE-0.56.25-Installer SHA PASS;
- reale PSTE-Themenmap PASS;
- PSTE nativer Providercache 86400 Sekunden belegt;
- UPC persistente Probe-TTL 7776000 Sekunden / 90 Tage;
- drei unabhängige Rückfallmutationen korrekt ROT.

## WORDPRESS-LIVE-BEFUND 0.8.2

Vor erneutem Start:
- Version: 0.8.2-prototype;
- Kandidaten: 8;
- SEO offen: 0;
- SEO blockiert: 8;
- maximale neue Providerkosten nach Wiederverwendung: $0.0000.

Nach genau einem erneuten `Gesamtworkflow starten`:
- Ergebnis: `NO_ELIGIBLE_COMPARISONS`;
- neue Dossiers: 0;
- bestehende unverändert: 0;
- Provider-Aufrufe: 0;
- Kosten: $0.0000;
- Produktrecherche offen: 0;
- SEO-PASS final: 0;
- blockiert final: 8.

Damit ist für denselben bereits geprüften Live-Bestand belegt:
**kein erneuter kostenpflichtiger Providerabruf.**

Nicht durch diesen einen Live-Lauf bewiesen, aber lokal hart geprüft:
- gleiches Produkt in neuem Paar;
- Teil-Lauf-Retry;
- Manipulations-/Ablauf-/Kontextdrift-Fälle.

## GESAMTWORKFLOW-GRENZEN

Weiter PASS:
- keine freie Produkterfindung;
- Same-Brand-/Profil-Drift fail-closed;
- nur ein Produkt mit Nachfrage reicht nicht;
- null Nachfrage reicht nicht;
- Provider PARTIAL bleibt PARTIAL;
- Dossier muss real im unabhängigen Abschluss-Audit vorhanden sein;
- Affiliate bleibt Exact-Match-Leseschicht;
- kein aktiver WordPress-Post-/Publishweg;
- kein Auto-Publish.

NEXT ACTION ausschließlich `HOBBYRAUM.md`.
