# Pferde Atelier Glossar – verbindliche Regeln für Einzelansichten

STAND: 2026-09-13
ROLLE: Verbindliche Design- und Scope-Regeln für öffentliche Glossarbegriffe.

## Harte Scope-Grenze

1. Das Einzelansichtsdesign gilt ausschließlich für den WordPress-Post-Type `uge_term`.
2. Normale Beiträge (`post`), Seiten (`page`) und andere Post-Types dürfen durch diese Regeln weder optisch noch strukturell verändert werden.
3. CSS für die Einzelansicht muss unter `body.single-uge_term` gescoped sein.
4. Content-Filter müssen zusätzlich `is_singular('uge_term')`, Main Query und Main Loop prüfen.
5. Kein eigenes `single-uge-term.php` und keine Übernahme via `template_include`; WordPress/Kubio bleibt Besitzer des nativen Single-Routings.

## Verbindliche Einzelansicht

- Breadcrumb: Startseite > Glossar > Oberbereich > aktueller Begriff.
- Kein Autor/User und kein Beitragsdatum in der Glossar-Einzelansicht.
- Kicker `WISSEN` + großer Begriffstitel.
- Pflichtfeld Kurzdefinition sichtbar als farbig hervorgehobener Balken `Kurz erklärt`.
- Rechte Box beginnt auf Desktop exakt bündig mit der Oberkante dieses Kurzdefinitionsbalkens, nicht mit der Überschrift.
- Rechte Box enthält `Verwandte Begriffe` als echte Links und `Mehr zum Thema` als passenden Portal-Kategorielink.
- Verwandte Begriffe werden nicht zusätzlich im Fließtext verlinkt.
- Unterer Abschluss enthält nur nutzerrelevante Glossar-Navigation; keine internen Produktionshinweise.
- Keine Schatten- oder Schwebeeffekte. Hover ausschließlich mit Ocker-Akzent.
- Mobile: rechte Box unter den Fließtext umbrechen; keine horizontale Überbreite.

## Freigabeprüfung

- Positiv: uge_term bekommt die vollständige Einzelansicht inklusive Kurzdefinition, Breadcrumb und rechter Box.
- Positiv: Oberkante rechte Box = Oberkante Kurzdefinitionsbalken auf Desktop.
- Negativ: normaler WordPress-Beitrag behält Titel/Meta und erhält keinerlei Glossar-Einzelansichtsmarkup oder -Styling.
- Negativ: keine ungescopten Einzelansichts-CSS-Regeln.
- Kein PASS ohne Prüfung des finalen Installations-ZIPs.