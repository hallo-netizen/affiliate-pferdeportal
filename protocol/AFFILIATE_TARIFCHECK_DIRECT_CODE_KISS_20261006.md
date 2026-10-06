# Tarifcheck Direktcode – KISS-Vertrag

Datum: 06.10.2026

## Verbindliches Ziel

Tarifcheck wird **nicht** als neuer technischer Provider und **nicht** über eine neue API integriert.

Es gilt der bestehende interne Weg:

`manuell eingefuegter Code -> Ziel-URL einmalig bestimmen -> feste Portalzielkarte speichern -> Runtime liest nur gespeicherte Zielkarte`

Tarifcheck wird dabei als bestehender Direkt-/Manuellpartner geführt.

## Verbindliche Entscheidungskette

Es gibt genau diese Reihenfolge:

`Code -> Trackinglink -> echte Ziel-URL -> URL-Prüfung -> Tarifart -> erlaubter Kategoriepfad -> feste Zielkarte -> speichern`

Dabei gilt:
- Die echte Ziel-URL ist die Fachquelle für die Tarifart.
- Titel, Alt-Text, Bannertext, Providername oder Werbemittelbezeichnung dürfen die Tarifart nicht überstimmen.
- Die Ziel-URL wird nur beim Import/Adminlauf dekodiert bzw. einmalig aufgelöst.
- Kredit-/Versicherungsprüfung erfolgt aus dieser Ziel-URL.
- Erst danach wird gegen den realen hierarchischen WordPress-Kategoriepfad geprüft.
- Nur ein Ziel unter der erlaubten Wurzel wird gespeichert.
- Fehlt eine eindeutige Ziel-URL, Tarifart oder erlaubte Kategorie: keine Zielkarte, keine automatische Ausspielung.
- Runtime prüft weder URL noch Tarifart erneut; sie liest ausschließlich die gespeicherte Zielkarte.

## Harte Fachregel

- **Kredit / Darlehen / Finanzierung:** ausschließlich in **allen real vorhandenen Kosten-Kategorien**. Im aktuellen Kategoriebaum sind Kosten keine gemeinsame Oberkategorie, sondern verteilte Blattkategorien. Zulässig sind deshalb die echten Kosten-Blätter mit sichtbarem Blattnamen `Kosten …` und Slug `…-kosten`.
- **Versicherung / Haftpflicht:** ausschließlich in den echten Blattkategorien des Astes **Wissen > Versicherungen & Recht**.
- Keine Kreuzzuordnung.
- Maßgeblich ist der **reale aktuelle WordPress-Kategoriebaum**, nicht eine erfundene gemeinsame Kosten-Oberkategorie.
- Kredit wird auf die gesamte echte Kosten-Zielmenge gebunden, nicht auf nur eine vermeintlich beste Kosten-Kategorie.
- Versicherung wird auf die gesamte echte Versicherungs-Zielmenge gebunden.
- Ein ähnlich benanntes Blatt außerhalb der erlaubten Struktur bleibt gesperrt.
- Unbekannte oder mehrdeutige Tarifcheck-Ziel-URL: keine Zielkarte, keine automatische Ausspielung.
- Für Tarifcheck entstehen keine automatischen Seiten-/Beitragsziele; nur Kategorieziele sind zulässig.

## KISS-Technik

- keine neue Tabelle;
- keine neue Spalte;
- kein neuer Provideradapter;
- keine Tarifcheck-API;
- keine URL-Neuklassifikation im Frontend;
- kein allgemeiner Banner-Fallback;
- manuelle Bannerimporte laden nach dem Import alle betroffenen Banner in genau einer gebündelten DB-Abfrage;
- Ziel-URL-Auflösung ist ausschließlich Import-/Adminlogik.

## Version

6.72.190 bleibt bewiesene Hard-KISS-Bannerbasis, wird aber vor Live-Installation durch 6.72.191 ersetzt.

6.72.191 ergänzt:
1. den manuellen Direktcode-Import um denselben Zielkarten-Nachlauf;
2. die harte Tarifcheck-Familientrennung Kosten vs. Versicherung;
3. fail-closed für unbekannte/mehrdeutige Tarifcheck-Ziele.

## Abnahme

Vor Installation Pflicht:
- WordPress + MariaDB;
- Kredit positiv unter Kosten;
- Kredit negativ unter Versicherung;
- Versicherung positiv unter Versicherung;
- Versicherung negativ unter Kosten;
- unbekanntes Tarifcheck-Ziel negativ;
- gemischtes Kredit/Versicherung-Ziel negativ;
- Kredit-URL mit irreführendem Versicherungstitel bleibt Kosten;
- Versicherungs-URL mit irreführendem Kredittitel bleibt Versicherung;
- gleichnamige/irreführende Kategorie im falschen Hauptast wird negativ ausgeschlossen;
- Runtime liest gespeicherte Karte;
- Source-Manifest 27/27;
- PHP-Lint;
- Fresh-Unpack/Byteidentität des finalen ZIP.


## Kategoriebaum-Prüfung

Autoritative Portalstruktur geprüft:

`release/affiliate-zentrale/current/affiliate-portal-router/assets/ebay-portal-catalog-v2.json`

Aktueller belegter Stand:
- 1.149 Artikelkategorien insgesamt;
- 67 konfigurierte Kosten-Einträge;
- 67 unterschiedliche Kosten-Slugs;
- 66 unterschiedliche Kosten-Pfade, weil ein Weidezaungeräte-Pfad im Strukturkatalog doppelt mit zwei Slugs geführt wird;
- Kosten-Kategorien liegen verteilt unter Ausrüstung, Fütterung, Stall, Transport, Weide und Wissen;
- 14 konfigurierte Blattkategorien unter `Wissen > Versicherungen & Recht`.

Die Runtime erhält für einen Kredit-Banner eine einzige gespeicherte Kampagne mit allen zulässigen Kosten-Zielschlüsseln. Es werden nicht dutzende Bannerkopien angelegt. Dasselbe Prinzip gilt für Versicherungsbanner mit der Versicherungs-Zielmenge.
