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
2. Bestehende Beiträge werden auf `NACHPRÜFUNG` gesetzt, bis sie gegen die aktuellen Regeln geprüft sind.
3. Bei der Nachprüfung werden fehlende verwandte Begriffe als geschlossener Cluster im selben Produktionslauf ergänzt.
4. Ein bestehender Artikel wird nur ersetzt/gelöscht, wenn er ein echter Dublette-, Fehl- oder Testdatensatz ist und dies vorher nachgewiesen wurde.
5. Pferde- und Ponyrassen sind `GESPERRT` und gehören ausschließlich in das separate Pferderassen-System.
6. `FERTIG` darf nur gesetzt werden, wenn alle Links tatsächlich auflösbar sind; reine Textnennungen zählen nicht.

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

Der vollständige Live-Bestand ist noch nicht autoritativ eingelesen. Deshalb werden hier keine weiteren vorhandenen Begriffe geraten.

Bereits im Arbeitsverlauf ausdrücklich bekannte vorhandene Glossarbeiträge müssen beim nächsten Live-Bestandseinzug übernommen und zunächst auf `NACHPRÜFUNG` gesetzt werden, sofern nicht bereits ein vollständiger Nachweis nach aktueller Regel existiert.

### Bekannter Prüfauftrag

| Begriff | Slug | Status | Hinweis |
|---|---|---|---|
| Aalstrich | aalstrich | NACHPRÜFUNG | bereits vorhanden; verwandte Begriffe müssen als echte Beiträge existieren und direkt verlinkt sein |

## Neue Cluster

Neue Begriffe werden nicht einzeln als `FERTIG` markiert. Zuerst wird der gesamte verwandte Cluster geschlossen, danach werden alle Cluster-Mitglieder gemeinsam auf `FERTIG` gesetzt.
