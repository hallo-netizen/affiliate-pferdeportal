# GLOSSAR – BEGRIFFSREGISTER

STAND: 2026-09-14
STATUS: AKTIV
ROLLE: AUTORITATIVES PRODUKTIONSREGISTER FÜR GLOSSARBEGRIFFE

## Zweck

Dieses Register beantwortet ausschließlich, welcher Glossarbegriff redaktionell/technisch bereits vollständig ist und welcher noch Arbeit benötigt. Es ersetzt weder Wissensdatenbank noch WordPress-Inhaltsablage.

## Verbindliche Statuswerte

- `OFFEN` – Begriff vorgesehen, noch nicht als vollständiger Glossarbeitrag vorhanden.
- `IN ARBEIT` – Beitrag/Cluster wird erstellt oder repariert.
- `NACHPRÜFUNG` – Beitrag existiert, aber mindestens eine aktuelle Inhalts-/Link-/Design-/Liveprüfung fehlt.
- `FERTIG` – Beitrag ist gegen die aktuellen Regeln vollständig geprüft und real freigegeben.
- `GESPERRT` – darf nicht als Glossarbeitrag erzeugt werden, z. B. Pferde- und Ponyrassen.

## Harte Regeln

1. Vorhandene Glossarbeiträge werden nicht pauschal gelöscht.
2. Bestehende Begriffe dürfen anhand eindeutiger Slugs/IDs gezielt **überschrieben/aktualisiert** werden; ID und URL müssen erhalten bleiben.
3. Keine automatische Löschung des Gesamtbestands für Regeländerungen.
4. Echte Dubletten-/Test-/Fehldatensätze nur nach Nachweis entfernen.
5. Neue Begriffe nur aus einer frisch nachgewiesenen `GEPRUEFT`-Quelle der Wissensdatenbank.
6. Pferde- und Ponyrassen sind `GESPERRT` und gehören in das separate Pferderassen-System.
7. `FERTIG` nur nach vollständiger Inhalts-, Link-, Meta-, Design- und erforderlicher Liveprüfung.
8. Verwandte Begriffe werden technisch relationiert und als Links in der rechten Box ausgegeben; diese Ziele dürfen nicht redundant im Fließtext verlinkt sein.
9. Dasselbe Linkziel darf in einem Glossarbegriff nicht doppelt gesetzt werden.
10. Verbindliche Detailregeln: `TEXT_UND_LINKREGELN.md`.

## Pflichtfelder je Begriff

| Feld | Bedeutung |
|---|---|
| Begriff | öffentlicher Glossarbegriff |
| Slug | eindeutiger WordPress-Slug |
| Kurzdefinition | sichtbare Zusammenfassung |
| Glossar-Kategorie | zugeordneter Glossar-Bereich |
| Status | OFFEN / IN ARBEIT / NACHPRÜFUNG / FERTIG / GESPERRT |
| Verwandte Begriffe | echte, auflösbare Relationen |
| Fließtext-Link geprüft | genau einmaliges passendes Portal-Ziel |
| Doppellink-Prüfung | kein Ziel doppelt |
| Meta geprüft | JA / NEIN |
| Design/Single geprüft | JA / NEIN |
| Letzte Prüfung | Datum / Nachweis |

## Aktueller belastbarer Produktionsstand

Der reale vollständige WordPress-Livebestand wurde in diesem Chat nicht automatisiert vollständig eingelesen. Deshalb wird keine vollständige Liveinventarliste erfunden.

Für den aktuellen lokalen Bestands-Update-Kandidaten `1.2.1` sind folgende 14 Slugs technisch enthalten und geprüft; wegen offenem autoritativen Release-/Livebeleg bleiben sie im Register auf `NACHPRÜFUNG`:

| Begriff | Slug | Status | lokaler Stand 2026-09-14 |
|---|---|---|---|
| Huf | huf | NACHPRÜFUNG | 150–200 Wörter, 1 Fließtext-Link, Related separat – lokal PASS |
| Hufbein | hufbein | NACHPRÜFUNG | lokal PASS |
| Strahlbein | strahlbein | NACHPRÜFUNG | lokal PASS |
| Hufrolle | hufrolle | NACHPRÜFUNG | lokal PASS |
| Widerrist | widerrist | NACHPRÜFUNG | lokal PASS |
| Stockmaß | stockmass | NACHPRÜFUNG | lokal PASS; LIVE-Doppellinkfehler der vorherigen Fassung muss durch 1.2.1/1.50.489 real verschwinden |
| Bandmaß | bandmass | NACHPRÜFUNG | lokal PASS; Referenzfall für finale Liveprüfung |
| Ganasche | ganasche | NACHPRÜFUNG | lokal PASS |
| Kehlgang | kehlgang | NACHPRÜFUNG | lokal PASS |
| Röhrbein | roehrbein | NACHPRÜFUNG | lokal PASS |
| Kötenbehang | koetenbehang | NACHPRÜFUNG | lokal PASS |
| Hufrehe | hufrehe | NACHPRÜFUNG | lokal PASS |
| Strahlfäule | strahlfaeule | NACHPRÜFUNG | lokal PASS |
| Hufabszess | hufabszess | NACHPRÜFUNG | lokal PASS |

### Weitere bekannte Begriffe

`Aalstrich` war bereits als vorhandener/Nachprüfungsbegriff dokumentiert. Sein heutiger realer WordPress-/WDB-Status wurde in diesem Chat nicht frisch belegt; deshalb keine Hochstufung oder Erzeugung.

## LIVE-Funktionsstand

Nutzerreadback: **`artikelanzeige pass`**. Damit ist die generelle Öffnung von Glossar-Einzelartikeln LIVE bestätigt.

Dies reicht nicht zur Hochstufung der obigen Begriffe auf `FERTIG`, weil die aktuelle Einzelansicht noch den Fehler `GLOSSAR-SINGLE-011` hat bzw. der lokale Fix 1.2.1/1.50.489 noch keinen Live-Readback besitzt.

## Nächste Freigabeschranke

`Bandmaß` muss nach quellgebundener Installation real beweisen:
- Breadcrumb korrekt;
- Kurzdefinition sichtbar;
- Icons sichtbar;
- `Stockmaß` als verwandter Link im Fließtext 0×;
- `Stockmaß` in der rechten Verwandt-Box exakt 1×;
- Portal-Kategorielink im Fließtext exakt 1×;
- normaler WordPress-Artikel unverändert.

Erst danach können betroffene Bestandsbegriffe auf `FERTIG` gesetzt werden.
