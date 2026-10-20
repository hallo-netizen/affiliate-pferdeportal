# HOBBYRAUSCH – WISSENSDATENBANK – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-20
STATUS: **ZENTRALE HOBBY-KLASSIFIKATION V1 / 20ER-PILOT VOLL KLASSIFIZIERT / 54 EIGENSCHAFTEN GETESTET / MASSENBEFÜLLUNG NOCH OFFEN**

## Rolle

Einzige aktuelle Zustandsautorität des Scopes `HOBBYRAUSCH_WISSENSDATENBANK`.

## Entscheidung

Für Hobby Depot existiert genau **eine zentrale Hobbyidentität je Hobby**. Hobbyfinder, Inspirations-/SEO-Ansichten und spätere Darstellungen greifen auf dieselben Hobbyidentitäten und denselben zentralen Eigenschaftsbestand zu.

Es wird **keine zweite Hobby-Datenbank und keine parallele Hobby-Taxonomie** für Finder oder Magazin angelegt.

## Zentrale Klassifikation V1

Persistente Datenbasis:
- Library: `/Hobby Depot/Hobby-Klassifikation/HOBBY_EIGENSCHAFTEN_SCHEMA_V1.json`
- Library: `/Hobby Depot/Hobby-Klassifikation/HOBBY_KLASSIFIKATIONSREGISTER_V1.json`
- Library: `/Hobby Depot/Hobby-Klassifikation/README.md`

Hashes:
- Schema SHA-256: `eb416346148badb7934ea1bee86c8dffde2f56e0a323c64846a298761b83c592`
- Register SHA-256: `df5e2d50ff73c7d4c91e94a9faef184738f5918573b89544c03492dc9cda0c97`
- README SHA-256: `1327d79d262e44f992c4be93b30cf5cc2c59533ffc04f8f8531e12de7f8f6b85`

## Datenmodell

Schema:
- **54 Eigenschaften in 8 Gruppen**;
- Eigenschaftskatalog ist global und unabhängig von einzelnen Hobbys;
- neue Eigenschaften werden mit stabiler ID ergänzt;
- bestehende Hobbydatensätze müssen dafür nicht umgebaut werden;
- entfernte/veränderte Eigenschaften werden versioniert/deprecated, nicht still umgedeutet.

Hobby-Register:
- **862 kanonische Hobbyidentitäten**;
- darunter alle **381 terminalen CORE-Hobbyseiten**;
- normale, kleine, schräge und Finder-/Editorial-Hobbys bleiben im selben Register;
- Aliasnamen erzeugen keine zweite Hobbyidentität;
- neuer Hobbyeintrag = genau ein neuer kanonischer Datensatz.

Trait-Speicherung:
- `traits` ist sparse;
- jeder Hobbydatensatz erbt automatisch das aktuelle Schema;
- nicht geprüfter Wert = `UNKNOWN`, niemals automatisch `false`;
- Zuordnung speichert `value`, `confidence`, `basis`, `reviewed_at`;
- niedrige Sicherheit darf im Hobbyfinder niemals hart ausschließen.

## Eigenschaftsgruppen

1. Sozial
2. Ort & Umgebung
3. Platz & Logistik
4. Zeit & Bindung
5. Kosten & Ausrüstung
6. Anforderungen & Lernkurve
7. Erlebnis & Motivation
8. Grenzen & Eignung

Bewusst zusätzlich berücksichtigt:
Lautstärke, Schmutz, Geruch/Dämpfe, Tageslicht, Wetter, Anfahrt, Lagerbedarf, Transportierbarkeit, Spontanität, feste Termine, laufende Pflegepflicht, Leihbarkeit, Bildschirmanteil, Ergebnisgeschwindigkeit, rechtliche Hürden, Motivation, frei-vs-regelgebunden, privat-vs-öffentlich und technische Grundvoraussetzungen.

Nicht verwendet:
- keine Klassifikation `männlich/weiblich`;
- Alter nur als reale Zugangs-/Eignungsdimension, keine Stereotype.

## Finder-/SEO-Vertrag

**Eigenschaft ist nicht gleich Finderfrage.**

Der zentrale Datensatz darf reich sein; der spätere Funnel fragt nur ca. 6–8 besonders trennscharfe Merkmale ab.

Eigenschaften haben Rollen:
- harter Filterkandidat;
- weiche Gewichtung;
- reine Information.

SEO-/Inspirationsseiten wie „Hobbys alleine“, „Hobbys draußen“, „wenig Zeit“, „kleines Budget“ oder „ungewöhnliche Hobbys“ sind Views über dieselben Traits und verlinken auf dieselben kanonischen Hobbyziele.

Kombinationsbegriffe wie „wenig Zeit“ werden aus Grundmerkmalen abgeleitet und nicht redundant in jeden Hobbydatensatz geschrieben.

## Lokale QA

- Schema: **54/54 eindeutige Property-IDs PASS**;
- Gruppen: **8 PASS**;
- Register: **862/862 eindeutige kanonische Namen PASS**;
- Register-IDs: **862/862 eindeutig PASS**;
- terminale CORE-Hobbyseiten: **381/381 enthalten PASS**;
- Alias-Dubletten aus altem Master: **entfernt/gebunden PASS**;
- schräge Testidentitäten (u. a. Lockpicking, Mushroom Spore Printing, Koji-Kultivierung, Räuchermischungen komponieren): **vorhanden PASS**;
- Eigenschaftswerte wurden **nicht aus Namen geraten**; aktuell 862/862 `PENDING_REVIEW`.

## 20er-Pilot 2026-10-20

Vollständig klassifiziert:
3D-Bogenschießen, 3D-Druck, Amateurastronomie, Amateurfunk, Ameisenhaltung, Buchbinden, Filzen, Wabikusa, Lockpicking, Koji-Kultivierung, Mushroom Spore Printing, Parfüm komponieren, Magnetfischen, Geocaching, Wandern, Stricken, Imkerei, Malen, Drohnenfotografie, Goldwaschen.

Ergebnis:
- 20 Hobbys × 54 Eigenschaften = **1080 schema-valide Zuordnungen**;
- jede der 54 Eigenschaften zeigt im Pilot mindestens zwei unterschiedliche Ausprägungen;
- keine Eigenschaft ist im Pilot vollständig wirkungslos;
- schwach getestete Bereiche: gruppenabhängige Hobbys, Wettbewerb, öffentliche Aufführung, laute Werkstatt, Wassersport;
- deshalb vor dem Einfrieren des Schemas noch ein gezielter Gegenprobe-Satz nötig.

Persistenter Audit:
`/Hobby Depot/Hobby-Klassifikation/HOBBY_KLASSIFIKATION_PILOT20_AUDIT_V1.json`

Register-SHA nach Pilot:
`55d6a0d0281affb1342f63fa7cbf591951a76077c29036e97920c52c3378fbdd`

## ERSTER OFFENER BLOCKER

Der 20er-Pilot ist vollständig befüllt. Vor der Massenklassifikation fehlen noch gezielte Gegenproben für im Pilot unterrepräsentierte Hobbytypen.

## EXAKT EINE NEXT ACTION

**Einen kleinen gezielten Gegenprobe-Satz für gruppenabhängige, wettbewerbliche, öffentliche, laute und wassergebundene Hobbys klassifizieren. Danach Schema einfrieren und erst dann die 842 übrigen Hobbyidentitäten systematisch befüllen.**
