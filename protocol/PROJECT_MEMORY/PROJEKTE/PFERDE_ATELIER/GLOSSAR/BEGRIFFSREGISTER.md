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
8. Verwandte Begriffe werden technisch relationiert und als Links ausschließlich in der rechten Box `Verwandte Begriffe` ausgegeben.
9. Der gesamte Glossar-Fließtext enthält **0 Links**.
10. Das Portalziel wird ausschließlich rechts in `Mehr zum Thema` verlinkt; Journal nur ersatzweise, wenn kein passendes Portalziel existiert.
11. Dasselbe Linkziel darf auf einer Glossar-Einzelansicht nicht doppelt gesetzt werden.
12. Verbindliche Detailregeln: `TEXT_UND_LINKREGELN.md`.

## Pflichtfelder je Begriff

| Feld | Bedeutung |
|---|---|
| Begriff | öffentlicher Glossarbegriff |
| Slug | eindeutiger WordPress-Slug |
| Kurzdefinition | sichtbare Zusammenfassung |
| Glossar-Kategorie | zugeordneter Glossar-Bereich |
| Status | OFFEN / IN ARBEIT / NACHPRÜFUNG / FERTIG / GESPERRT |
| Verwandte Begriffe | echte, auflösbare Relationen |
| Fließtext-Linkprüfung | exakt 0 Links |
| Seitenbox-Linkprüfung | Related- und Portalziel korrekt getrennt, kein Ziel doppelt |
| Meta geprüft | JA / NEIN |
| Design/Single geprüft | JA / NEIN |
| Letzte Prüfung | Datum / Nachweis |

## Aktueller belastbarer Produktionsstand

Der reale vollständige WordPress-Livebestand wurde in diesem Chat nicht automatisiert vollständig eingelesen. Deshalb wird keine vollständige Liveinventarliste erfunden.

Für den aktuellen lokalen Bestands-Update-Kandidaten `1.2.2` sind folgende 14 Slugs technisch enthalten und geprüft; wegen offenem realem LIVE-Readback bleiben sie im Register auf `NACHPRÜFUNG`:

| Begriff | Slug | Status | lokaler Stand 2026-09-14 |
|---|---|---|---|
| Huf | huf | NACHPRÜFUNG | 150–200 Wörter, 0 Fließtextlinks, Related separat – lokal PASS |
| Hufbein | hufbein | NACHPRÜFUNG | 0 Fließtextlinks – lokal PASS |
| Strahlbein | strahlbein | NACHPRÜFUNG | 0 Fließtextlinks – lokal PASS |
| Hufrolle | hufrolle | NACHPRÜFUNG | 0 Fließtextlinks – lokal PASS |
| Widerrist | widerrist | NACHPRÜFUNG | 0 Fließtextlinks – lokal PASS |
| Stockmaß | stockmass | NACHPRÜFUNG | lokal PASS; alter LIVE-Doppellink-/Fließtextlinkfehler muss durch 1.2.2/1.50.490 real verschwinden |
| Bandmaß | bandmass | NACHPRÜFUNG | lokal PASS; Referenzfall für finale Liveprüfung |
| Ganasche | ganasche | NACHPRÜFUNG | 0 Fließtextlinks – lokal PASS |
| Kehlgang | kehlgang | NACHPRÜFUNG | 0 Fließtextlinks – lokal PASS |
| Röhrbein | roehrbein | NACHPRÜFUNG | 0 Fließtextlinks – lokal PASS |
| Kötenbehang | koetenbehang | NACHPRÜFUNG | 0 Fließtextlinks – lokal PASS |
| Hufrehe | hufrehe | NACHPRÜFUNG | 0 Fließtextlinks – lokal PASS |
| Strahlfäule | strahlfaeule | NACHPRÜFUNG | 0 Fließtextlinks – lokal PASS |
| Hufabszess | hufabszess | NACHPRÜFUNG | 0 Fließtextlinks – lokal PASS |

### Weitere bekannte Begriffe

`Aalstrich` war bereits als vorhandener/Nachprüfungsbegriff dokumentiert. Sein heutiger realer WordPress-/WDB-Status wurde in diesem Chat nicht frisch belegt; deshalb keine Hochstufung oder Erzeugung.

## LIVE-Funktionsstand

Nutzerreadback: **`artikelanzeige pass`**. Damit ist die generelle Öffnung von Glossar-Einzelartikeln LIVE bestätigt.

Dies reicht nicht zur Hochstufung der obigen Begriffe auf `FERTIG`, weil `GLOSSAR-SINGLE-011` aktuell weiterhin LIVE FAIL ist und 1.2.2/1.50.490 noch keinen realen Live-Readback besitzen.

## Nächste Freigabeschranke

`Bandmaß` muss nach Installation der geprüften Kandidaten real beweisen:
- Breadcrumb exakt `Startseite > Glossar > Pferd & Biologie > Bandmaß`;
- Kurzdefinition sichtbar;
- Icons sichtbar;
- Fließtext insgesamt **0 Links**;
- `Stockmaß` in der rechten Verwandt-Box exakt 1× als Link;
- Portalziel in `Mehr zum Thema` exakt 1× als Link;
- obere Ockerlinie der rechten Boxen sichtbar dünner / 2 px;
- bestehende ID und URL unverändert;
- normaler WordPress-Artikel unverändert.

Erst danach können betroffene Bestandsbegriffe auf `FERTIG` gesetzt werden.
