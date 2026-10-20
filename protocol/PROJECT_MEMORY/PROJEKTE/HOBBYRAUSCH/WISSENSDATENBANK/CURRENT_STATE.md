# HOBBYRAUSCH – WISSENSDATENBANK – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-20
STATUS: **KLASSIFIKATIONSSCHEMA 1.1 / 505 HOBBYS VOLL GEPRÜFT / KURZPROFILE 505/862 / 357 OFFEN**

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
- Schema 1.1 SHA-256: `0518309b6cd7e71ee607180291d6a024f8306fefdccd4824718b7fac9784e703`
- Register nach 30er-Prüfung SHA-256: `198b87b5b939feea57d6638d1dcc00000b2b37c8aef049b2c796103ab4e2fd32`
- Gegenprüf-Audit SHA-256: `f88201c87e7f5bdd8f007d62523cc572738efe14c028995c3b84b809b3210c23`

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
- Eigenschaftswerte werden **nicht aus Namen geraten**; aktuell **30 geprüft / 832 `PENDING_REVIEW`**.

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

## 10er-Gegenprobe / Schema 1.1

Zusätzlich vollständig klassifiziert:
Unterwasserhockey, Bubble Soccer, Drone Soccer, Pen-&-Paper-Rollenspiele, Historical Reenactment, Holzwerken, Kanutouren, RC-Segelboote, Slotcar Racing, Tabletop Wargaming.

Ergebnis:
- insgesamt **30 Hobbys × 54 Eigenschaften = 1620 geprüfte Zuordnungen**;
- Gruppenpflicht, zentraler Wettbewerb, öffentliche Ausübung, laute/staubige Werkstatt, Schwimmbad, Gewässer und sehr großer Platzbedarf: **PASS**;
- echter Modellfehler gefunden und korrigiert: `active_space` vermischte Größe und Ortsart;
- Schema 1.1 trennt Platzgröße sauber von Ort/Infrastruktur;
- Sportanlage/Halle, Schwimmbad/Pool und Gewässer als Ortswerte ergänzt;
- danach vollständige Gegenprobe ohne weiteren Schemafehler: **PASS**;
- Schema 1.1 ist damit für die Massenklassifikation **eingefroren**.

Audit:
`/Hobby Depot/Hobby-Klassifikation/HOBBY_KLASSIFIKATION_COUNTERCHECK30_AUDIT_V1.json`

## Hobbyfinder V1

Maschinenlesbares Konzept:
`/Hobby Depot/Hobby-Klassifikation/HOBBYFINDER_FUNNEL_V1.json`

Lokale Simulation:
`/Hobby Depot/Hobby-Klassifikation/HOBBYFINDER_FUNNEL_SIMULATION_V1.json`

Klickbarer Prototyp:
`/Hobby Depot/Hobby-Klassifikation/HOBBYFINDER_PROTOTYP_V1.html`

Funnel: 8 Schritte – Motivation, Sozialform, Ort, Zeit, Budget, Platz, Aktivität, Verbindlichkeit. Die übrigen Traits bleiben Hintergrundlogik bzw. Feinfilter. Vier unterschiedliche Testprofile lieferten vier unterschiedliche Top-Treffer.

## Zentrales Kurzprofil für Ergebnis-/Hobbykarten

Neu verbindlich:
Jede kanonische Hobbyidentität besitzt zusätzlich zu den Filter-Traits einen **separaten Präsentationsblock**. Dieser ist ausdrücklich **keine Filtereigenschaft**.

Schema:
`/Hobby Depot/Hobby-Klassifikation/HOBBY_KURZPROFIL_SCHEMA_V1.json`

Pflichtfelder:
- `what_is_it` = Was ist das?
- `what_do_you_do` = Was macht man?
- `what_do_you_need` = Was braucht man?
- `appeal` = Was ist der Reiz?

Stil:
kurz, konkret, keine Füllwörter, keine Werbesprache, keine Wiederholung des Hobbynamens.

Stand:
- Struktur bei **862/862** Hobbydatensätzen vorhanden;
- **55/862** Kurzprofile fachlich formuliert;
- **807/862** bleiben `PENDING_PROFILE`, bis das jeweilige Hobby regulär bearbeitet wird;
- Kurzprofilwerte werden nicht aus dem Hobbynamen automatisch erzeugt.

Finder-Prototyp:
`/Hobby Depot/Hobby-Klassifikation/HOBBYFINDER_PROTOTYP_V1.html`
zeigt die vier Kurzprofilfelder nun direkt auf den Ergebniskarten.

## Regulärer Klassifikationsbatch 001

Am 2026-10-20 wurden weitere **25 Hobbys** vollständig nach Schema 1.1 klassifiziert und gleichzeitig mit dem vierteiligen Kurzprofil versehen.

Stand danach:
- **55/862** Hobbys vollständig geprüft;
- **55/862** Kurzprofile REVIEWED;
- **807/862** offen;
- je bearbeitetem Hobby **54/54 Traits vorhanden**;
- alle Traitwerte gegen das zentrale Schema validiert;
- Kurzprofil je Hobby **4/4 Felder vorhanden**;
- keine Name-only-Autoklassifikation.

Audit:
`/Hobby Depot/Hobby-Klassifikation/HOBBY_KLASSIFIKATION_BATCH001_AUDIT.json`

Register-SHA:
`95c3c9608fff4db87d4540ecc1cbadc698f90bd2290b87cd4dc5629843b0a572`

Finder-Prototyp nutzt nun **55** vollständig klassifizierte Hobbys und zeigt auf jeder Ergebniskarte die vier Kurzprofilfelder.

## Klassifikationsbatch 009

- 50 Hobbys zusätzlich REVIEWED;
- Gesamtstand **455/862**;
- offen **407/862**;
- je Hobby 54/54 Traits schema-valide;
- je Hobby 4/4 Kurzprofilfelder vorhanden;
- zentraler Register-SHA: `4dd3af722977ac0d62830ad31d7252532d7437574adccf633ecea3c5fb7ecc92`;
- Audit: `/Hobby Depot/Hobby-Klassifikation/HOBBY_KLASSIFIKATION_BATCH009_AUDIT.json`.

## Klassifikationsbatch 010

- 50 Hobbys zusätzlich REVIEWED;
- Gesamtstand **505/862**;
- offen **357/862**;
- 54/54 Traits + 4/4 Kurzprofilfelder je Hobby PASS;
- Register-SHA: `28898b8506cd32ce18879086f44c3da4704b6618f45935670175f7451548ae01`;
- Audit: `/Hobby Depot/Hobby-Klassifikation/HOBBY_KLASSIFIKATION_BATCH010_AUDIT.json`.

## ERSTER OFFENER BLOCKER

Die zentrale Logik und Grundoptik des Finder-Prototyps sind vom Nutzer bestätigt. **357 Hobbyidentitäten sind noch nicht fachlich klassifiziert und besitzen noch kein geprüftes Kurzprofil.**nd noch nicht fachlich klassifiziert und besitzen noch kein geprüftes Kurzprofil.**nd noch nicht fachlich klassifiziert und besitzen noch kein geprüftes Kurzprofil.**

## EXAKT EINE NEXT ACTION

**Die restlichen 357 Hobbyidentitäten in kontrollierten Batches nach Schema 1.1 klassifizieren und im selben Arbeitsschritt jeweils das vierteilige Kurzprofil erstellen. Unklare Trait-Werte bleiben UNKNOWN; keine ungeprüfte Auto-Klassifikation.**n kontrollierten Batches nach Schema 1.1 klassifizieren und im selben Arbeitsschritt jeweils das vierteilige Kurzprofil erstellen. Unklare Trait-Werte bleiben UNKNOWN; keine ungeprüfte Auto-Klassifikation.**n kontrollierten Batches nach Schema 1.1 klassifizieren und im selben Arbeitsschritt jeweils das vierteilige Kurzprofil erstellen. Unklare Trait-Werte bleiben UNKNOWN; keine Name-only-Autoklassifikation.**
