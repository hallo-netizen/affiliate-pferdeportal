# Robotik Kategorie-Workflow 0.4.11 – gesicherter Fachnachtrag

**Stand 15.11.2026 | Plugin 0.4.11 als vollständige installierbare ZIP in `CURRENT.zip` sowie identisch `VERSIONEN/0.4.11.zip`.**

## Auslöser / fachliche Entscheidung
Die früheren 16 Google-SERP-HOLDs mit 48 Inhaltsrubriken sind gemäß neuem Zielvertrag V76 **redaktionell freigegeben**. Fehlende Google-Zieladressen dürfen **nicht** länger blockieren. Keine neue kostenpflichtige DataForSEO-Abfrage, keine Löschung.

## Einziger technischer KISS-Ablauf
1. **Bereits gestarteten V63-Auftrag mit originalem Status und Index fortsetzen**, bis **227/227** real nachgelesen sind. Keine erneute Erstinitialisierung und keine Duplikate. Bei `BLOCKED` gibt es nur nach unverändertem Bestandsabgleich die Aktion „Gespeicherten Originalimport sicher fortsetzen“.
2. **Bestehenden V65-Schritt** `Neue Seiten sichtbar machen` **68/68** abschließen. V63 akzeptiert jetzt bereits korrekt veröffentlichte originale neue Seiten als existierend statt fälschlich nur `draft` zuzulassen.
3. **Im selben Admin-Menü `Gesamtübernahme (geschützt)`** erscheint danach der **Fachnachtrag: 16 Seiten + 48 Rubriken**. Einmalige ausdrückliche Checkbox, ein Knopf, ein gespeicherter 64er Arbeitslauf. 16 tatsächlich angelegte Fachseiten werden dort veröffentlicht; 48 flache WP-Kategorien gehören jeweils nur zu ihrem Robotertyp.

**Die alten 227 Aufgaben und der ursprüngliche V62-188/296-Manifestinhalt sind nicht verändert.** Der Nachtrag verwendet die **eine bestehende WordPress-Schreibfunktion** `Robotik_V63_Delta::createOne`, keine neue zweite Kategorie-Entscheidungsfunktion, kein zweites Plugin oder Drittserver-Request. Alle alten Quellkennungen bleiben erhalten.

## Schutz
- Kein Importstart, bevor **227/227** des V63-Originalauftrags **UND 68/68 veröffentlichte Seiten** im WordPress-Status nachgewiesen sind.
- 16 neue eindeutige Seiten-IDs und 48 bestehende fachliche Rubrik-IDs aus dem V62-Profil, Originalparent/Slug/Owner nachzulesen; Quelle und Index nie neu erfinden.
- Bestehende WordPress-Seiten, alte Kategorien, fremde Objekte und bestehende 227er-Pakete niemals löschen oder überschreiben.
- Beim Fehler Status `BLOCKED` plus gespeicherter Index; erst nach Bestandsgleichheit kontrolliert fortsetzen.
- Kein Google-Adressen-Zwang, keine Bezahl-API, keine Änderungen an Industrie/Gewerbe-Hierarchie durch die 64er-Fortsetzung.
- 11 zusätzliche V76-Robotertypkandidaten gehören **noch nicht** zur 16+48 Übernahme; sie bleiben sauber getrennte Fachentwürfe.

## Echte GitHub-Prüfung (nicht als WordPress-Live-PASS ausgeben)
- GitHub Actions: <https://github.com/hallo-netizen/affiliate-pferdeportal/actions/runs/43698916919> – **SUCCESS** am 15.11.2026.
- **PHP `-l`** für die vier geänderten Quell-Dateien und sämtliche **9 PHP-Dateien des ZIPs**: Erfolg.
- **`unzip -t`**: Erfolg, **`CURRENT.zip` = `VERSIONEN/0.4.11.zip` byte-identisch**; alle vier geänderten PHP-Dateien in der ZIP sind byte-identisch mit den GitHub-Quelltexten.
- **Spezialtest mit dem originalen 188/296-Manifest**: laufender 227er Import blockiert korrekt, fehlende 68er Publikation blockiert korrekt, 16+48 Vorprüfung erzeugt genau 64 Aufgaben, vollständige simulierte 188+296 Endkontrolle erfolgreich, veränderter Kategorienbesitzer wird erkannt und blockiert. Ausgabe: `V77 MOCK PASS`.
- Die übrigen 9 unveränderten ZIP-Elemente (Assets und ursprüngliche Klassen) wurden bei der Neupaketierung bitgleich als komprimierte Datenblöcke übernommen.
- **Kein WordPress-Live-Schreibvorgang durch diese Entwicklung; installierter WP-Versionsstand noch unbekannt.** Der erste echte Test erfolgt am tatsächlichen gespeicherten WordPress-Importstand, ohne Neuinitialisierung.

## Installer
- `KATEGORIE/PLUGIN/CURRENT.zip` und `KATEGORIE/PLUGIN/VERSIONEN/0.4.11.zip`; ein und dieselbe Pluginidentität `robotik-kategorie-workflow`.
- Technische GitHub-Blob-ID der bytegleichen ZIPs: `2bfaa950246b2657fc9f0d6db7151f592352f7a2`.
- **Nur diese installierbare Version zum Update verwenden.** Die Zwischenstände 0.4.9/0.4.10 bleiben Versionsarchiv, nicht parallel installieren.

## Benutzerweg
**WordPress-Plugin „Robotik Kategorie-Workflow“ als Update auf 0.4.11 einspielen.** Dann ausschließlich in `Robotik Kategorie → Gesamtübernahme (geschützt)` den vorhandenen Lauf fertigstellen, `Neue Seiten sichtbar machen` ausführen, und danach den **einen** Fachnachtrag 16+48 einmalig ausdrücklich freigeben. Im Backend gibt es einen **Gesamtbericht als JSON**, keine vielen Dateien. **Keine neue Google- oder SEO-Prüfung.**
