# GLOSSAR – BEGRIFFSREGISTER

STAND: 2026-09-13
STATUS: AKTIV
ROLLE: AUTORITATIVES PRODUKTIONSREGISTER FÜR GLOSSARBEGRIFFE

## Zweck

Dieses Register beantwortet ausschließlich die Frage, welcher Glossarbegriff redaktionell/technisch bereits vollständig ist und welcher noch Arbeit benötigt.

Es ersetzt weder die Wissensdatenbank noch den Themenpool noch WordPress als Inhaltsablage.

## Verbindliche Statuswerte

- `OFFEN` – Begriff vorgesehen, noch nicht als vollständiger Glossarbeitrag vorhanden.
- `IN ARBEIT` – Beitrag/Cluster wird gerade erstellt oder repariert.
- `NACHPRÜFUNG` – Beitrag existiert bereits, muss aber gegen die aktuellen Produktionsregeln geprüft werden.
- `FERTIG` – Beitrag ist vollständig geprüft: Inhalt, Metaangaben, Glossar-Kategorie, mindestens ein sinnvoller interner Link zu einem verwandten Glossarbeitrag und funktionierende Verwandt-Verlinkung.
- `GESPERRT` – darf nicht als Glossarbeitrag erzeugt werden, z. B. Pferde- und Ponyrassen.

## Harte Regeln

1. Bereits vorhandene Glossarbeiträge werden **nicht gelöscht**, nur weil neue Produktionsregeln eingeführt wurden.
2. Die vorhandenen Live-Glossarbeiträge bleiben bestehen, bis der Nutzer nach technischem Klickbarkeitsnachweis selbst entschieden und real geprüft hat, ob der Altbestand gelöscht wird.
3. Das Plugin löscht oder überschreibt diese Altbeiträge nicht automatisch.
4. Bestehende Beiträge werden bis zur fachlichen Nachprüfung auf `NACHPRÜFUNG` geführt.
5. Bei der Nachprüfung werden fehlende verwandte Begriffe als geschlossener Cluster im selben Produktionslauf ergänzt.
6. Ein bestehender Artikel wird nur ersetzt/gelöscht, wenn er ein echter Dublette-, Fehl- oder Testdatensatz ist und dies vorher nachgewiesen ist.
7. Pferde- und Ponyrassen sind `GESPERRT` und gehören ausschließlich in das separate Pferderassen-System.
8. `FERTIG` darf nur gesetzt werden, wenn alle Links tatsächlich auflösbar sind; reine Textnennungen zählen nicht.

## Pflichtfelder je Begriff

| Feld | Bedeutung |
|---|---|
| Begriff | öffentlicher Glossarbegriff |
| Slug | eindeutiger WordPress-Slug |
| Glossar-Kategorie | zugeordneter Glossar-Bereich |
| Status | OFFEN / IN ARBEIT / NACHPRÜFUNG / FERTIG / GESPERRT |
| Verwandte Begriffe | nur echte bzw. im selben Cluster erzeugte Begriffe |
| Interne Links geprüft | JA / NEIN |
| Kategorie-Link geprüft | JA / NEIN |
| Meta geprüft | JA / NEIN |
| Letzte Prüfung | Datum / Nachweis |

## Aktueller Bestand

Der vollständige reale Live-Bestand ist noch nicht autoritativ eingelesen. Deshalb werden keine weiteren vorhandenen Begriffe geraten.

Bereits bekannte vorhandene Glossarbeiträge müssen beim nächsten realen Bestandseinzug übernommen und zunächst auf `NACHPRÜFUNG` gesetzt werden, sofern nicht bereits ein vollständiger Nachweis nach aktueller Regel existiert.

### Bekannter Prüfauftrag

| Begriff | Slug | Status | Hinweis |
|---|---|---|---|
| Aalstrich | aalstrich | NACHPRÜFUNG | bereits vorhanden; fachliche/Meta-/Link-Nachprüfung noch offen |

## Neue Cluster

Neue Begriffe werden nicht einzeln als `FERTIG` markiert. Zuerst wird der gesamte verwandte Cluster geschlossen, danach werden alle Cluster-Mitglieder gemeinsam bewertet.

Aktueller technischer Testcluster in 0.2.10-rc7:
- Hufrehe
- Strahlfäule
- Hufabszess

Dieser Cluster ist **technisch im Testsystem grün**, aber nicht als realer Pferde-Live-Bestand in diesem Register auf `FERTIG` hochzustufen.

## Klickbarkeitsnachweis – technisch erbracht

Die bisherige technische Freigabeschranke verlangte mindestens:
- Klick auf einen gerenderten bestehenden Glossarbegriff aus einer Glossarübersicht → echte Einzelansicht;
- Klick auf einen gerenderten neuen Cluster-Begriff → echte Einzelansicht;
- Klick auf `Verwandte Begriffe` → echte verwandte Einzelansicht;
- Klick auf den Kategorienlink → echte Glossar-Kategorie.

**Diese technische Schranke ist mit 0.2.10-rc7 im Testsystem erfüllt.**

Beleg:
- Run `34762048546`
- Real-Design-Job `103736483696`
- `UGE0210_EXISTING_SINGLE_CLICK_PASS`
- `UGE0210_NEW_CLUSTER_CLICK_CHAIN_PASS`
- `UGE0210_SINGLE_SURVIVES_EMPTY_MAIN_LOOP_PASS`

Reale Browserklicks:
`Gesundheit → Hufbein` sowie `Gesundheit → Hufrehe → Strahlfäule → Hufabszess → Gesundheit`.

**Grenze:** Dies ist kein Pferde-LIVE-Readback. Der Nutzer hat angekündigt, den Altbestand erst nach eigenem realen Prüfzugriff zu löschen. Diese Entscheidung bleibt ausdrücklich beim Nutzer; keine automatische Löschung.
