# Kategorie- und Navigationsstandard für folgende Portale
Stand 17.10.2026 · Aus belegten Fehlversuchen bei Hab & Bewahr abgeleitet · PORTALÜBERGREIFENDE ARBEITSANLEITUNG

## Auftrag und Geltung
Ein wiederverwendbarer Leitfaden, **kein zweiter Current-Stand und kein neues Plugin**. Bei jedem neuen Portal zuerst seinen eigenen Zielvertrag, seine tatsächlich vorhandenen Daten und seinen konkreten WordPress-Aufbau prüfen. Hab-&-Bewahr-Zahlen (sechs Welten, 36 Bereiche, 265 Themenseiten, 1.323/471 Inhaltskategorien) sind historische Projektwerte, **keine Vorlage** für andere Portale.

## Fehler → Ursache → künftig verbindlicher Prüfschritt

| Belegter Fehler / Fehllauf | Ursache | Verbindliche Schutzregel |
| --- | --- | --- |
| Der Ausbau wurde künstlich auf genau drei Kinder begrenzt; später versuchten Pläne 3–10 | Optische Musterzahlen statt fachlicher Vollständigkeit | Fachliche Kinder nach sinnvoller Such-/Nutzungsabsicht erfassen; Mindestzahl des jeweiligen Zielvertrags beachten, aber **keine visuell begründete Obergrenze** |
| Konkretes Produkt wurde direkt als letzte WP-Inhaltskategorie behandelt | Letzte WordPress-*Seite* und letzte WP-*category* verwechselt | Vor Planung eindeutige Knotentypen/Parent-Relationen festlegen; bei diesem Portal genau drei Seitenebenen, darunter genau eine flache Inhaltskategorieebene |
| Neue Graffiti-Themenseite duplizierte historischen Graffiti-Intent; Alt-/Neubereiche kollidierten | Unvollständiger Bestand und falsche semantische Rollen | Sämtliche Bestands-IDs, URLs, Kategorierollen, Eltern, Artikelbindungen und ältere Entwürfe prüfen; **pro konkretem Thema ein kanonischer Owner** |
| Die 93 alten Themen fehlten bei der ersten FAQ-/Beratungs-/Vergleichsergänzung | Nur neue 172 statt aller 265 Themen geprüft | **Immer alle alten UND neuen Themen-Owner prüfen**, auch wenn ein früherer Import technisch grün war |
| 566 Kategorien mit provisorischer „Kapazität“ erhielten fachlichen PASS | Ein technischer Zähl-/Schema-Prüfer wurde als fachliche Inhaltsprüfung ausgegeben | Für jede letzte Kategorie individuell den Sinn und das grobe Potenzial für etwa 3–5 eigenständige spätere Beiträge prüfen; keine Scheinkapazität als PASS |
| FAQ/Vergleich zunächst ausgelassen, Beratung erst spät | Ziele wurden nur als Beispiele statt als Pflicht unterschieden | Pflicht-Facetten **explizit im Zielvertrag definieren** und ownerweise prüfen; bei Hab & Bewahr FAQ und Beratung überall, Vergleiche nur wenn eigenständig hilfreich |
| Standardisierte Zusatzrubriken oder global als Dublette gewertete gleiche Namen | Schema F bzw. Namensvergleich ohne Eltern-/Intentkontext | Kosten, Wartung, Installation usw. nur bei eigenem Mehrwert; Dubletten **innerhalb des konkreten Owners und semantisch** prüfen |
| Detaillierte künftige Artikeltitel/SEO-Briefs verzögerten Kategoriearbeit | Kategorienplanung und Artikelproduktion vermischt | In dieser Phase nur Kategorien und grobe Tragfähigkeit; konkrete Artikel und Keyword-Einzeldetails ins spätere SEO-/Textsystem |
| Gegen vermeintlich falschen Renderer mehrfach das Kategorieplugin geändert | Sichtbares HTML wurde vom **Designplugin** geliefert | **Zuerst nachweisen, welcher aktive Renderer die tatsächlich sichtbare Navigation/Kacheln ausgibt**; nur diesen ändern |
| Menüs blieben trotz grüner interner Tests falsch | Simulation prüfte nicht den echten Ausgabeweg/WordPress-HTML | Positive UND negative Tests am Original-Renderer; danach echter WordPress-Frontend-Check für Desktop und Mobil; Lokal-PASS != Live-PASS |
| Labels verschwanden, weil `name` statt `display_name` gelesen wurde | Schema des tatsächlichen aktiven Snapshots nicht geprüft | Gegen echte Datenfelder aus dem aktiven Kategorie-Writer entwickeln, inklusive Cache-Neustart/Versionswechsel |
| Ein zweites Startseitenplugin wurde erstellt | Erweiterung statt Update der bestehenden Design-Identität | **Genau ein bestehendes Designplugin weiterentwickeln**, gleichen Pluginordner/Basename behalten; keine parallel konkurrierenden Schreiber/Renderer |
| Megamenü blendete zwei Wetterbereiche aus; „Alle Themen“ wurde pauschal gezeigt | Fünf *Spalten* als fünf *Bereiche insgesamt* interpretiert; Überlauflink bedingungslos | Inhalte niemals wegen der Rasterbreite abschneiden; Zeilen umbrechen; „Alle Themen“ nur bei echten verdeckten gültigen Direktlinks; Rand-/Mobilcheck |
| Endkategorien zeigten Geschwisterkategorien | Falsche Fallback-Logik beim Rendern | Kinderbeziehung ausschließlich aus korrektem Elternbezug; Endkategorie nie als Geschwister-Navigation umdeuten |
| Abgeschlossene 743/472-Importe drohten erneut zu laufen | Bestand, Zusatzwelle und neue Welle nicht strikt getrennt | Nur ADD-only-Deltas mit eigener Vorschau, Schutz der früheren Revisionen, separater Freigabe und Wiederholsperre |
| Als fertig gemeldete lokale Tests waren keine Live-Tests | Ungenaue Statussprache | Immer `FACHLICH GEPRÜFT`, `LOCAL PASS`, `WORDPRESS LIVE OFFEN` und `LIVE BESTÄTIGT` unterscheidbar ausweisen |
| Veraltete Zwischenstände im Register und in Übergaben | Historie wurde wieder als aktuell behandelt | Genau eine Current-Autorität je Büro, aktuellen Zielvertrag von dort lesen, ältere Protokolle nur als Fehler-/Prüfbeleg behandeln |

## Ablauf – in genau dieser Reihenfolge
1. **Bestand und Auftrag:** Aktive Current + Zielvertrag + Fehlerquelle, sichtbare Live-Seite und vorhandene WordPress-Struktur prüfen. Bestehende IDs, Slugs, URLs, Eltern und Artikelzuordnungen inventarisieren. Keine erneute Vollrecherche, wenn aktuelle eindeutige Quellen vorliegen.
2. **Rollen definieren:** Vor jeder Liste klar zwischen Welt, Bereich, konkreter Themenseite, flacher Artikelkategorie, Beitrag, Magazin, Glossar und Dienstleister unterscheiden. Portalabhängige Ebene-Anzahl nicht ungeprüft übernehmen.
3. **Fachbaum einmal vollständig:** ALLE alten und neuen Themen nach Nutzerbedarf, Produkten, Gefahren und Fragen durchgehen. Mindestkinder laut Portalvertrag ohne künstliche Höchstzahl; fehlende/duplizierte kanonische Owner begründen.
4. **Letzte Inhaltskategorien:** Pflicht-/Wunsch-Facetten im *Portalvertrag* festschreiben und individuell prüfen. Mindestens grob mehrere selbstständige spätere Beiträge möglich. Keine Artikeltitel, keine vorzeitige Texteproduktion.
5. **Prüfung:** Richtiger Owner/Kindtyp, Namens- und Intentdubletten, vorhandene URL/ID, eindeutige physische Bindung, Linkziel, leere/verwaiste Knoten, Grenzen zwischen Alt und Neu; absichtlich defekte Fälle müssen scheitern.
6. **Plugin-Schritt:** Nur bestehender zentraler Kategorie-Writer, erst Dry-Run mit 0 Schreibungen, dann genau **ein** autorisierter ADD-only-Import. Alte Läufe nie wiederholen; Fehler-Rollback darf keine fremden oder belegten Bestandsobjekte löschen.
7. **Sichtbare Navigation:** Original des tatsächlich aktiven Designplugins/Theme-Ausgabewegs verifizieren; echte Seiten-/Kategorien-URLs statt erfundener Testziele; Desktop/Mobil, Überlauf, Dubletten, Endknoten und Cache prüfen.
8. **Live-Abnahme:** An WordPress realen Importabschluss UND echte Frontend-Ausgabe getrennt bestätigen; keine lokale Simulation zu Live hochstufen. Nicht bestätigte Punkte bleiben OFFEN.
9. **Dokumentation:** Ein zuständiger Current je Büro, separat Fehlerquelle, übergeordneter Zielvertrag, verifizierter NEXT STEP; historische Pläne nicht widersprüchlich wiederbeleben.

## Design/Monetarisierung als getrennte Arbeit
Seiten auf derselben Ebene benutzen ein gemeinsames zentrales Layout. Affiliate-Banner (automatisierte Befüllung) und separat vermietete Werbeflächen bleiben unterschiedliche Plätze. **Nur befüllte Werbung öffentlich**, unbelegte Platzhalter ausschließlich für Berechtigte sichtbar. Kein zusätzlicher Frontend-Netzwerkabruf, keine neuen Datenbanktabellen und keine zweite Pluginidentität. Layoutänderungen dürfen niemals Seiten-/Kategorie-IDs, Slugs, URLs oder kanonische Eltern ändern.

## Verbindlicher Freigabesatz
Eine Kategorie-/Navigationsarbeit ist erst als erledigt bezeichnet, wenn **(a)** alle Themen fachlich vollständig und ownerbezogen geprüft, **(b)** Deltas ohne Bestandsverlust übernommen, **(c)** das tatsächliche sichtbare WordPress-Menü und die Seiten geprüft und **(d)** der reale Status mit Nachweis in der richtigen Current-Quelle abgelegt sind. Sonst klar den ersten offenen Punkt nennen.

## Belegquellen dieser Fehlerlehren
- `KONZEPT/FEHLERQUELLEN.md` (V9/C2.2, Dubletten, falsch positive Fachprüfungen)
- `KATEGORIEN/CURRENT_STATE.md` (Importwellen, reale Abschlussgrenzen, Renderpfad)
- `DESIGN/FEHLERQUELLEN.md` und `DESIGN/CURRENT_STATE.md` (Plugin-/Nav-/Label-/Megamenüfehler)
- `KONZEPT/ZIELVERTRAG_KATEGORIEN_MINDESTENS_3_OHNE_MAXIMUM_20261015.md` (projektbezogene Pflichtregeln)
