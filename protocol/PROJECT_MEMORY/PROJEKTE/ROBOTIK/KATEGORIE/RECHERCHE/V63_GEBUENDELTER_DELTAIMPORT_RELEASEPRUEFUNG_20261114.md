# Robotik V63 – gebündelter, geschützter WordPress-Deltaimport (14.11.2026)

## A. Exakte Basis (nicht geschätzt)

- Echte, nutzerseitig exportierte WordPress-Gesamtvorschau: `robotik-v62-wordpress-gesamtvorschau-20261114-144428.json`, UTC 14:44:28, Plugin 0.4.8, Site `https://robotik.oliver-beil.de/`.
- Vollständige Live-Inventur: **115 Seiten, 90 WordPress-Kategorien, 0 Beiträge, 0 HivePress-Kategorien/Inserate**.
- Mit stabilen Kennungen und Pfaden nachgewiesen: **104/104 alte Seiten, 89/89 alte WordPress-Kategorien**. Null Identitäts-, Pfad- oder Kategorie-Konflikte.
- **11 weitere Seiten und 1 Kategorie** auf dem Portal gehören nicht zu den 104/89 des alten Kategorieplans; der Export liefert zu ihnen keine einzelnen Bezeichnungen. Daher ausdrücklich *nicht* behaupten, diese 11+1 identifiziert zu haben. Sie werden vollständig geschützt.
- Neues Gesamtkonzept: **188 Seiten** (47 Gruppen inklusive fehlender Hauptwelt „Humanoide“, 141 Robotertypen) sowie **296 Inhaltsrubriken** (89 alt, 207 neu).
- 84 zusätzliche Seiten = 15 neue Gruppen und 69 neue Robotertyp-Seiten. Davon bleiben **16 Robotertyp-Seiten** und ihre **48 Inhaltsrubriken** ausdrücklich im SEO-HOLD. Noch keine vollständige Suchergebnis-Gegenprüfung, weil die V61-SERP-URLs nicht als echte Zieladressen verwertbar waren.

## B. Ein vollständig gebündelter, aber eingeschränkt freigabefähiger Importblock

**Nur neue, nicht gesperrte Positionen:**
- **68 neue Seiten** = 15 neue Gruppen + 53 Robotertypseiten, ausschließlich als **WordPress-Entwurf**.
- **159 neue, flache WordPress-Beitragskategorien**, mit Kurzlabel, eindeutiger Robotertyp-Zuordnung und den ursprünglich belegten drei oder mehr Stoffrichtungen.
- **16 gesperrte Robotertyp-Seiten und 48 zugehörige Inhaltsrubriken nicht anlegen.** Nicht aus dem Zielbaum entfernen; ihre ursprünglichen IDs bleiben erhalten.
- Alle vorhandenen 115 Seiten und 90 Kategorien bleiben unverändert, ebenso 0 Beiträge, Magazin, Glossar, Finder, Anzeigenmarkt/HivePress, Menüs, bisherige Veröffentlichungs- und DataForSEO-Abläufe.
- Keine automatische Veröffentlichung, kein Update/Delete alter Inhalte, keine neue Datenbanktabelle, kein Cron und kein API-Aufruf. Der alte 104/89-Erstimport bleibt unverändert und darf für V63 nicht verwendet werden.

## C. Plugin-Korrektur als EIN bestehendes Plugin

- **Version 0.4.9**, Nachfolger von 0.4.8, kein weiteres Plugin.
- Vorhandenes V62-Sollmanifest samt SHA256-Prüfung unverändert. Das neue Schreibmodul nutzt die **gleiche Bestandsaufnahme und dieselbe eindeutige Identitätsprüfung** wie die Gesamtvorschau. Kein zweiter Kategorieentscheider.
- WordPress-Admin-Menü: `Robotik Kategorie → Gesamtübernahme (geschützt)`.
- Die Seite erstellt **automatisch und kostenlos eine aktuelle Nur-Lese-Vorschau** mit 68+159, sodass **kein weiterer manueller Export vor dem Import** notwendig ist.
- Erst nach einer **ausdrücklichen, konkreten Checkbox-Freigabe** startet ein einzelner geschützter Auftrag. Beim Start wird der aktuelle WordPress-Bestand **erneut gegen die angezeigte Vorschau verglichen**. Bei jeder Abweichung wird ohne Schreiben gestoppt.
- Alle Schreibschritte sind nach Elternhierarchie geordnet, status- und ID-gebunden; die acht Aufgaben pro Browserteilaufruf werden gespeichert und eine Unterbrechung kann denselben Lauf fortsetzen. Es werden keine erfolgreichen Aufgaben doppelt erstellt.
- Ein späterer Fehler blockiert den Lauf, ohne bestehende Objekte zu löschen; kein Blind-Retry. Abschlusskontrolle liest 227/227 neue Objekte einschließlich Elternseiten, Slugs, Kurzlabel, Kategorienbesitzer zurück und prüft, dass alle alten WordPress-IDs erhalten bleiben. **16+48 SEO-HOLD bleiben offen**, auch wenn der sichere Block vollständig übernommen wird.
- Danach nur **ein Gesamtbericht als JSON** zum unabhängigen Nachweis – kein weiterer Vorab-Export.

## D. Prüfnachweis – lokal, NICHT WordPress-Live

- Echte V62-Soll- und Ist-JSON-Dateien vollständig programmiert auf Duplikate, Elternpfade, 296 Rubrik-Eigentümerbeziehungen und 16 Hold-Zuordnungen geprüft: **kein struktureller Konflikt**.
- 115 echte Plan-WP-Seitenpositionen mit 90 Kategorien als WordPress-Datenmodell nachgebildet (104 alte Seiten, 89 Kategorien mit realen bestätigten IDs plus 11+1 **synthetische, nicht identifizierbare** Nicht-Plan-Objekte).
- 15 positive und negative Testkontrollen bestanden: 227 geplante Aufgaben, 16+48 Sperren, ursprüngliche 115/90 erhalten, Nur-Lese-Vorschau ohne Schreiben, 8er-Batch, Unterbrechung/Wiederaufnahme, vollständiger 227/227-Readback, 68 Entwurfsseiten/159 Kategorien, Sperre bei veränderter Altseite und Kategoriekennung.
- Alle **7 PHP-Dateien** mit PHP Lint geprüft; ZIP-Dateitests und Inhaltsdateizahl bestanden. Gegen die Originalversion 0.4.8 verändert sind ausschließlich das **Hauptfile** (Version/Boot) und die **Signatur der bestehenden Nur-Lese-Vorschau** (als zentrale Prüfroutine gemeinsam nutzbar). **Eine neue Klasse** wurde ergänzt. Die ursprünglichen 8 verbleibenden Plugin-Dateien/Assets sind bytegleich.
- **Keine echte WordPress-Schreibprüfung durchgeführt.** Live-Daten können sich seit dem V62-Export geändert haben; deshalb ist der *frische* automatische Live-Vorabcheck vor einer Freigabe obligatorisch.

## E. Freigabegrenze

**Noch keine WordPress-Änderung durch diesen Chat.** Das Update ist ein **Test-Installer mit eingebautem Freigabeschutz**. Niemand darf behaupten, 188 Seiten/296 Kategorien seien bereits in WordPress importiert. Nach tatsächlicher Übernahme sind – sofern der Live-Bestand zwischenzeitlich unverändert blieb – 183 Seiten und 249 Kategorien zu erwarten, **davon 16 potenzielle Seiten und 48 Rubriken weiter im Forschungs-/SEO-HOLD**. Andere WP-Änderungen können diese Gesamtsummen beeinflussen.

**Bündelung:** Nicht mehr separat SEO-Resultate, Seitenlisten, Kategorien und Importscreens anfordern. **Eine** Pluginaktualisierung, **eine** ausdrückliche Freigabe des sicheren Blocks und **ein** Abschlussbericht. Die 16 offenen SEO-Fälle werden später gesammelt fachlich entschieden, ohne bereits freigegebene Seiten zu verändern.

**Installer:** `ROBOTIK_KATEGORIE_WORKFLOW_0.4.9_SICHERE_GESAMTUEBERNAHME_TEST.zip` – 100876 Bytes, SHA256 `1829a6b7cf3d243f361431736ebd027949724b293aac40306db60df00f4ff8b0`.