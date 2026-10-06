# PSTE Kurzweg für vorhandenes oder manuell gesetztes Material

## Ziel
Vorhandene PSTE-Themen oder manuell eingereichte Themen dürfen ohne neuen DataForSEO-Aufruf erneut in die PSTE-Themenverwaltung gelangen, sofern der Redaktionsplan und alle PSTE-eigenen Schutzprüfungen eingehalten werden.

## Harte Regeln
1. Der Kurzweg überspringt ausschließlich externe DataForSEO-Recherche. Er überspringt niemals Redaktionsplan, Dublettenprüfung, Themenfamilie/Kategorie oder Artikeltyp.
2. Vorhandenes Material bleibt unverändert erhalten; keine automatische Löschung alter Kandidaten.
3. Exakte oder semantische Bestandsdubletten müssen vor Freigabe blockieren.
4. Ein Thema braucht eine bestehende passende Themenfamilie/Kategorie oder eine explizite Strukturentscheidung. Keine automatische Erfindung neuer Struktur.
5. Der Artikeltyp muss aus dem bestehenden Typ-/Kategorie-System stammen.
6. Erst nach diesen Prüfungen darf der Kandidat den normalen PSTE-Reentry-Status erhalten.
7. Der Kurzweg erzeugt selbst keinen Artikel und besitzt keine Produktionsautorität.
8. Bei fehlender eindeutiger Bindung bleibt der Kandidat REVIEW/STRUCTURE_REQUIRED; niemals still durchwinken.

## Zwei zulässige Einstiege
### A. Existing-Material-Reentry
Für bereits gespeicherte PSTE-Kandidaten mit vorhandener Evidenz.
Aktueller belastbarer Pool: 110 Kandidaten.
- 92: bestehende Familienbeziehung bestätigen
- 9: bestehende Familie binden
- 9: bestehenden Artikeltyp/Kategorie binden

### B. Manual-Topic-Intake
Für ein vom Nutzer bewusst gesetztes Thema ohne neue DataForSEO-Recherche.
Pflichtfelder vor Reentry:
- Arbeitstitel bzw. Thema
- Ziel-Keyword/Schlüsselbegriff
- bestehende Themenfamilie/Kategorie
- Artikeltyp
- Redaktionsplan-/Slot-Bindung
- Bestands-/Dublettenprüfung

Fehlt eines davon oder ist die Bindung widersprüchlich, bleibt der Datensatz blockiert.

## Simulation
Positiv: Kandidat besitzt vorhandene Evidenz, keine exakte Live-Dublette und eine vollständige bestehende Bindung -> REENTRY_ALLOWED.
Negativ 1: exakte Live-Dublette -> BLOCK_EXISTING_CONTENT_DUPLICATE.
Negativ 2: keine sichere bestehende Familie/Kategorie -> STRUCTURE_DECISION_REQUIRED.
Negativ 3: kein zulässiger Artikeltyp -> ARTICLE_TYPE_BINDING_REQUIRED.
Negativ 4: Redaktionsplan-/Slot-Bindung fehlt -> PLAN_BINDING_REQUIRED.
Negativ 5: Kurzweg versucht DataForSEO aufzurufen -> CONTRACT_VIOLATION.

## Ergebnis des aktuellen 110er-Pools
Alle 110 benötigen laut bestehender Evidenz keine neue externe Recherche.
Exakte Titel-Dubletten gegen den aktuellen 92er-Livebestand: 0.
Der Kurzweg darf sie dennoch nicht blind freigeben; jeder Kandidat muss den bestehenden PSTE-Reentry mit Redaktionsplan- und Dublettenprüfung durchlaufen.

