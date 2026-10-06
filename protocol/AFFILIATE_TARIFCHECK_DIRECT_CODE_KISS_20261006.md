# Tarifcheck Direktcode – KISS-Vertrag

Datum: 06.10.2026

## Verbindliches Ziel

Tarifcheck wird **nicht** als neuer technischer Provider und **nicht** über eine neue API integriert.

Es gilt der bestehende interne Weg:

`manuell eingefuegter HTML-Bannercode -> Trackinglink/Bildquelle lesen -> Ziel-URL einmalig bestimmen und prüfen -> Banner technisch prüfen -> feste Portalzielkarte speichern -> Runtime liest nur gespeicherte Zielkarte`

Tarifcheck wird dabei als bestehender Direkt-/Manuellpartner geführt.

## Verbindliche Entscheidungskette

Es gibt genau diese Reihenfolge:

`HTML-Code -> Trackinglink/Bildquelle -> echte Ziel-URL -> URL-Prüfung -> technische Bannerprüfung -> Tarifart -> erlaubte Zielmenge -> feste Zielkarte -> speichern`

Dabei gilt:
- Die echte Ziel-URL ist die Fachquelle für die Tarifart.
- Titel, Alt-Text, Bannertext, Providername oder Werbemittelbezeichnung dürfen die Tarifart nicht überstimmen.
- Die Ziel-URL wird nur beim Import/Adminlauf dekodiert bzw. einmalig aufgelöst.
- Kredit-/Versicherungsprüfung erfolgt aus dieser Ziel-URL.
- Erst nach erfolgreicher technischer Bannerprüfung wird gegen den realen WordPress-Kategoriebaum geprüft.
- Nur ein Ziel unter der erlaubten Wurzel wird gespeichert.
- Fehlt eine eindeutige Ziel-URL, eine erfolgreiche technische Bannerprüfung, eine eindeutige Tarifart oder eine erlaubte Kategorie: keine Zielkarte, keine automatische Ausspielung.
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

6.72.190 bleibt die bewiesene Hard-KISS-Bannerbasis.

6.72.191 ergänzte den manuellen Direktcode-Weg und die Tarifcheck-Familientrennung, ordnete aber noch vor der realen Bildprüfung zu. Dieser Ablauf wurde verworfen.

6.72.192 ist verbindlich:
1. HTML-Bannercode importieren;
2. Trackinglink/Bildquelle lesen;
3. echte Ziel-URL ermitteln und prüfen;
4. Bannerbild technisch prüfen;
5. **erst danach** Kredit/Versicherung bestimmen und feste Kategorien speichern;
6. Fehler/Unklarheit = keine Zielkarte und keine Ausspielung.

WordPress/MariaDB Source-Beweis: Run `37454893550` PASS.
Exakter Final-ZIP-Beweis: Run `37455039161` PASS.
Finaler Installer: `AFFILIATE_ZENTRALE_6.72.192.zip`, SHA-256 `49add47f6876e78737704b3ca067bf5d931ee68a5f7448f99d8227ee57fc60d9`.

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


## Tarifrechner – bewusst später

Tarifrechner/Formulare/Widgets werden **nicht** in 6.72.192 integriert und nicht als Bildbanner missbraucht.

Späteres KISS-Konzept:
- eigener Werbemitteltyp `Tarifrechner`;
- eigener HTML-/Widget-Prüfweg;
- eigene fachliche Zielmenge;
- keine Vermischung mit der Bannerrotation.

Bis dahin bleibt der Rechner-Strang geschlossen. 6.72.192 beendet ausschließlich die korrekte Banneraufnahme und Bannerzuordnung.
