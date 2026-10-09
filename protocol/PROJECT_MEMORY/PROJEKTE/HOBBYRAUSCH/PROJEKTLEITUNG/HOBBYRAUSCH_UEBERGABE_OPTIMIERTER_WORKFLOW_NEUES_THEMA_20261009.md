# HOBBYRAUSCH – Übergabe / optimierter Workflow für ein neues Thema

Stand: 2026-10-09  
Zweck: Nachbarchat startet ein neues Thema und führt es **von der Konzeptentwicklung über Kategorien und Inhalte bis zur finalen WordPress-Umsetzung**.  
Priorität: **schnellstmöglich, aber nur mit vollständiger Vorprüfung. Keine Serien von Zwischen-Plugins. Keine Blindfixes.**

---

## 0. Ausgangspunkt – was jetzt als belastbare Wahrheit gilt

Der Hobbyrausch-Kategorienlauf HD-001 ist produktiv abgeschlossen.

Aktueller produktiver Endstand:

| Punkt | Endstand |
|---|---:|
| Plugin-Codebasis | 1.14.8 |
| Live-Status | COMPLETE / TARGET_TREE_SYNC_AND_READBACK_PASS |
| logische Zielknoten | 2371 |
| physische Zielobjekte | 2357 |
| produktiver Readback | 2357 / 2357 |
| beim finalen Sync erstellt | 256 |
| beim finalen Sync aktualisiert | 2100 |
| beim finalen Sync unverändert | 1 |
| archiviert | 1 |
| demoted editorial | 0 |
| terminale CORE-Identitätsseiten geprüft | 330 / 330 |
| Kategorie-Gate-Fehler | 0 |
| ungebundene CORE-Seiten | 0 |
| Frontend-Readback | PASS |
| Welten | 8 |
| Provider-Aufrufe im finalen Dry-Run | 0 |
| WordPress-Strukturwrites im Dry-Run | 0 |
| Live-Profilrevision | `HD-TARGET-3P-RULE27-CATEGORY-GAPFIX-HOBBYFINDER-20261009+0f4dbf59238a7d83` |

Finaler lokaler Kategorienbeweis vor dem Live-Lauf:
- 1920 CORE-Content-Kategorien;
- 1665 vorhandene, bereits akzeptierte Bestands-Leafs unverändert erhalten;
- 255 neue Rule-2.7-Leafs, jeweils mit mindestens 3 unterschiedlichen Supporting Intents;
- 330 terminale CORE-Seiten, davon 0 ohne Leafs;
- Verteilung 129×5 / 139×6 / 55×7 / 7×8 Leafs;
- keine künstliche Gesamtobergrenze für Leafs;
- keine generisch erzwungenen `Ausrüstung & Kosten`-Leafs;
- keine Kategorie unter Kategorie;
- keine doppelten Slugs, fehlenden Parents oder Zyklen.

**Dieser Live-Endstand ist die Baseline für jedes neue Thema.** Ein neues Thema wird als **Delta** modelliert. Der bestehende Gesamtbaum wird nicht erneut erfunden oder flächig umgebaut.

---

## 1. Oberste Arbeitsregel – warum der alte Weg zu langsam war

Der größte Fehler im bisherigen Lauf war nicht ein einzelner PHP-Bug, sondern der Arbeitsmodus:

**Fachliche Modellierung, Prüfung, Pluginbau und Live-Upload wurden zu früh miteinander vermischt.** Dadurch entstanden immer neue Kandidaten, neue Uploads, neue Dry-Runs und neue Folgefehler, obwohl der Kategorienbestand fachlich noch nicht vollständig abgeschlossen war.

Der neue Grundsatz lautet daher:

> **Erst das komplette Thema als Daten-/Strukturmodell fertigstellen und vollständig lokal beweisen. Erst danach genau ein Release-Artefakt bauen und genau einmal live ausrollen.**

Keine Zwischen-ZIPs, nur weil eine Kategorie ergänzt wurde. Keine Mini-Fixes auf dem Server. Keine neue Pluginarchitektur für ein Datenproblem.

---

# 2. Der optimierte Schnellworkflow – Konzept bis Live

## PHASE A – Auftrag und Zielvertrag zuerst vollständig festnageln

Bevor Kategorien, Keywords, Pluginprofile oder Texte gebaut werden, wird für das neue Thema ein kurzer, harter Zielvertrag erstellt.

Er muss mindestens festlegen:
- Thema / Arbeitsname;
- Nutzerproblem und Zielgruppe;
- Portalrolle: `HOBBY_HUB`, `ORIENTATION_UNIVERSE`, `EDITORIAL_TOPIC`, `ARTICLE_ONLY`, `FINDER_ONLY` oder `OUT_OF_SCOPE`;
- natürliche Hauptwelt und Parent-Struktur;
- ob CORE, Magazin und/oder Anbieter/HivePress betroffen sind;
- gewünschte Monetarisierungsrolle, ohne daraus die fachliche Struktur abzuleiten;
- welche sichtbaren Nutzerwege am Ende existieren müssen;
- was ausdrücklich **nicht** verändert werden darf;
- harte Abnahmekriterien.

**Gate A:** Kein technischer Bau, solange Rolle, Parent und Ziel nicht eindeutig sind.

## PHASE B – Fachliches Inventar und Suchintentionen vollständig ausarbeiten

Jetzt wird das Thema fachlich zerlegt, noch **ohne WordPress-Schreibvorgänge**.

Für jede potenzielle unterste Content-Kategorie werden eigenständige Artikel-/Suchintentionen gesammelt. Fachlogik bestimmt die Content Capacity. SEO-Daten dürfen Nachfrage, Formulierung und Überschneidung prüfen, aber nicht die Portalstruktur bestimmen.

Verbindlich:
- Synonyme zählen nicht als mehrere Intents;
- Keyword-Varianten zählen nicht als mehrere Intents;
- jeder primäre Intent bekommt genau einen Owner;
- keine Konkurrenz zwischen CORE, Magazin und Anbieter;
- ein neuer Leaf braucht mindestens **3 eigenständige sinnvolle Beitragsintentionen**;
- bestehende sinnvolle Leafs bleiben erhalten;
- DataForSEO ist **keine Strukturautorität**;
- keine Keyword-Ideas-Tiefenrecherche als Pflichtschritt.

**Gate B:** Für jeden neuen Leaf liegt vor dem Einbau eine explizite Intent-Evidence vor.

## PHASE C – Kategorienbaum als Ganzes fertigstellen

Erst jetzt wird die endgültige Struktur für das neue Thema in Master/Profil modelliert.

Harte Rule-2.7-Regeln:

| Regel | Muss gelten |
|---|---|
| Hauptwelten | die 8 bestehenden Welten bleiben ROOT |
| Hobbywelten | View/Übersicht, niemals Parent der 8 Welten |
| Mega-Menü | je Welt maximal 10 sichtbare Direktkinder; nicht künstlich auf 10 auffüllen |
| Content-Ebene | keine künstliche Gesamtobergrenze |
| neuer Leaf | mindestens 3 echte unabhängige Intents |
| Einstieg | sichtbar abgedeckt |
| FAQ | sichtbar abgedeckt |
| Praxis/Vertiefung | sichtbar abgedeckt; vorhandene Fach-Leafs dürfen dies erfüllen |
| Ausrüstung & Kosten | nur eigener Leaf, wenn >=3 echte unabhängige Intents |
| Parent-Regel | keine Kategorie unter Kategorie |
| Ownership | pro primärem Intent genau ein SEO-Owner |
| Löschung | kein Hard-Delete als Normalweg |
| terminale CORE-Seite | darf nicht ohne tragfähige sichtbare Content-Ebene veröffentlicht werden |

**Wichtig:** Nicht die Zahl 5, 6, 7 oder 8 ist das Ziel. Diese Zahlen sind nur der aktuelle Live-Bestand. Ein neues Thema bekommt genau so viele Leafs, wie fachlich getragen werden. Kein altes 3–6-Limit wieder einführen.

**Gate C:** Der gesamte neue Zielbaum ist fertig. Nicht erst einzelne Hobbys hochladen und später nachbessern.

## PHASE D – Magazin / Hobbyfinder / Anbieter parallel korrekt anbinden

Magazin und CORE dürfen keine konkurrierenden Kopien desselben Suchintents erzeugen.

Aktuelle Magazinlogik:
- `Hobbyfinder` ist direkte Hauptkategorie des Magazins;
- darunter befinden sich `Hobbywelten`, `Alleine`, `Zu zweit`, `Gruppe`;
- das alte `Hobby finden` ist archiviert;
- keine `journal_cat` unter einer `journal_cat` als künstliche zusätzliche SEO-Ebene;
- Situationen, Saison, Alter, Budget, Platz usw. können redaktionelle Einstiege/Filter sein, ohne einen zweiten SEO-Owner zu erzeugen.

Anbieter/HivePress:
- nur echte Anbieter-/Kurs-/Vereins-/Werkstatt-/Shop-/Service-Intents in die DIRECTORY-Säule;
- keine fachliche CORE-Struktur aus Anbieterlogik ableiten.

**Gate D:** CORE, Magazin und DIRECTORY sind gemeinsam ownership-dedupliziert.

## PHASE E – kompletter lokaler Beweis, bevor irgendein ZIP hochgeladen wird

Das ist der wichtigste Unterschied zum alten Arbeitsweg.

Vor dem ersten Live-Upload müssen **alle** folgenden Prüfungen in einem lokalen Abnahmelauf bestanden sein.

### E1 – statischer Kategorienbaum

Pflichtprüfungen:
- alle Parents vorhanden;
- keine Zyklen;
- keine doppelten Node-IDs;
- keine doppelten physischen Slugs;
- keine Kategorie unter Kategorie;
- alle neuen Leafs haben >=3 Supporting Intents;
- Einstieg / FAQ / Vertiefung abgedeckt;
- keine unbewerteten/PENDING Rollen im produktiven Ziel;
- keine terminale CORE-Seite ohne Leafs;
- alle 8 Welten ROOT;
- Hobbywelten nur View;
- Mega-Menü je Welt <=10;
- Magazin-/Hobbyfinder-Hierarchie korrekt;
- Cross-Pillar Intent-Kannibalisierung = 0.

### E2 – kompletter positiver E2E-Lauf

Mit den echten Produktionsklassen lokal simulieren:
- Baseline laden;
- Dry-Run;
- erwartetes Delta prüfen;
- Full Sync;
- Unterbrechung während `WRITING` simulieren;
- Resume bis `COMPLETE`;
- vollständigen Readback prüfen;
- Frontend-/Header-Projektion prüfen;
- anschließend Idempotenzlauf: **0 Delta**.

### E3 – negative E2E-Suite

Mindestens diese Fehler künstlich erzeugen und beweisen, dass der Workflow fail-closed bleibt:
- terminale Seite mit 0 Leafs;
- doppelter Slug;
- Kategorie unter Kategorie;
- fehlender Parent;
- Intent-Kannibalisierung;
- Live-Drift zwischen Dry-Run und Apply;
- manipuliertes Readback;
- absichtlicher Write-Fehler mitten im Lauf;
- Rollback muss exakt auf den Ausgangsfingerprint zurückkehren;
- fehlende Zieltaxonomie;
- stale/alte Revision darf nicht als aktuelles COMPLETE gelten;
- ungültiger/abgelaufener AJAX-Nonce muss JSON liefern und darf den Browser nicht mit `Unexpected token '<'` abbrechen lassen.

### E4 – Releaseprüfung

Vor Freigabe:
- PHP-Lint über alle PHP-Dateien;
- ZIP-Integrität;
- Paketinhalt gegen den tatsächlich getesteten Arbeitsstand hashen;
- keine nicht getesteten Dateien nachträglich ins ZIP kopieren;
- exakte Änderungsliste gegen die freigegebene Codebasis dokumentieren.

**Gate E:** Kein Pluginupload, solange nicht statisch + positiv + negativ + Resume + Rollback + Idempotenz vollständig PASS sind.

## PHASE F – genau ein Release-Artefakt

Erst nach Gate E wird **ein** finales Kandidaten-ZIP gebaut.

Für ein neues Thema gilt grundsätzlich:
- wenn die bestehende Engine alles unterstützt, nur Profil/Master/Evidence ändern;
- keine PHP-Änderung für reine Kategorie-/Text-/Kacheldaten;
- Performanceoptimierungen nicht zurücknehmen;
- keine Architekturänderung;
- keinen neuen Providerpfad aktivieren;
- keine neue Pluginversion nach jedem Datenfix;
- falls ein echter Enginefehler durch Negativtest bewiesen wird: Ursache beheben, danach **gesamte** Suite erneut laufen lassen und erst dann ein einziges neues Release bauen.

## PHASE G – Live-Ausrollung ohne Schleife

Live ausschließlich in dieser Reihenfolge:

1. Exaktes final geprüftes ZIP installieren/ersetzen.
2. `Kategorien → Finaler Zielbaum → Finalen Delta-Dry-Run ausführen`.
3. Dry-Run-JSON herunterladen.
4. Nicht nur die Counts, sondern **jede Archive-/Adopt-/kritische Move-Aktion** gegen das erwartete Delta prüfen.
5. Nur bei vollständiger Übereinstimmung genau **einen** Sync ausführen.
6. Während `WRITING` nichts hochladen, nichts neu starten, nicht parallel eingreifen.
7. Nach `COMPLETE` den finalen Readback als JSON herunterladen.
8. Readback prüfen: Objektzahl, 100% Readback, Frontend, Header, Hubs/Leafs, unbound CORE, errors=[].
9. Danach optional einmal read-only Idempotenz bestätigen: 0 Delta.
10. Dann LIVE-PASS setzen und den Stand einfrieren.

**Kein zweiter Sync, nur weil ein Bildschirm noch alt aussieht. Erst Readback auswerten.**

---

# 3. Benötigte Plugins / technische Bausteine

## HD-001 – Pflicht für Struktur/Kategorien

**Affiliate-Portal Kategorie-Workflow**  
Plugin-ID: `HD-001-KATEGORIE-WORKFLOW`  
aktuelle Codebasis: `1.14.8`

Final lokal geprüftes Artefakt aus diesem Lauf:
`HD001_V1.14.8_RULE27_FINAL_VERIFIED_E2E_20261009.zip`

SHA-256:
`709134631895a901bcb4fc5f5d71889d317954d9928c0ed20700883990a5a52c`

Aufgabe:
- Master/Profil auflösen;
- CORE/Magazin/DIRECTORY-Zielbaum;
- read-only Delta-Dry-Run;
- Fingerprint-/Drift-Gate;
- Sync/Resume/Rollback;
- WordPress-/Frontend-Readback;
- `journal_cat` wird vom Plugin selbst registriert.

## HivePress – Pflicht, solange DIRECTORY/Anbieter aktiv ist

HD-001 verwendet für die Anbieter-Säule die Taxonomie `hp_listing_category` und blockiert fail-closed, wenn diese Zieltaxonomie fehlt.

Daher für den vollständigen 3-Säulen-Pfad erforderlich. Nicht durch einen Dummy oder eine selbst erfundene Ersatz-Taxonomie ersetzen.

## HD-002 – nachgelagert für Text/SEO/Content

**Hobby Depot SEO Themenengine**  
Plugin-ID: `HD-002-TEXT-SEO`

Rolle:
- nach dem finalen Kategorie-/Owner-Handoff;
- Redaktions-/Themen-/SEO-Kontext;
- Contentproduktion bzw. Übergabe in die Produktionsstrecke.

Wichtig für den Nachbarchat:
Der zuletzt dokumentierte technische Stand von HD-002 war `0.1.4` mit lokalem vollständigem Resume-Workflow-Hard-Pass, aber der damalige Livezustand war noch nicht abgenommen. **Vor Verwendung unbedingt dessen aktuelle `CURRENT.md` neu lesen.** Nicht aus diesem Übergabedokument eine aktuelle HD-002-Livefreigabe ableiten.

## DataForSEO

Kein separates WordPress-Strukturplugin und keine Strukturautorität. Nur SEO-Evidence/Anreicherung. Ein neues Thema darf nicht wegen DataForSEO automatisch in eine Welt verschoben, promoted oder als neue Kategorie erzeugt werden.

## Theme / Frontend

Kein bestimmtes Theme wird durch diesen Workflow als Strukturautorität behandelt. Trotzdem muss die Ausgabe im **tatsächlich aktiven Theme** im lokalen E2E und im produktiven Frontend-Readback sichtbar geprüft werden.

---

# 4. Was im Nachbarchat bei einem neuen Thema konkret erzeugt werden soll

Der Nachbarchat soll **nicht sofort Code schreiben**. Er liefert nacheinander diese Artefakte und arbeitet sie ohne Sprünge ab:

| Stufe | Ergebnis |
|---|---|
| 1 | Zielvertrag / Scope / Rolle / Nicht-Ziele |
| 2 | Fachinventar + eigenständige Such-/Beitragsintents |
| 3 | endgültige Parent-/Owner-Entscheidung |
| 4 | vollständige Kategorien/Leafs mit Evidence |
| 5 | Magazin-/Finder-/Directory-Zuordnung |
| 6 | komplettes Delta gegen die aktuelle 2357-Baseline |
| 7 | statisches Prüfprotokoll |
| 8 | vollständige lokale POS+NEG-E2E-Evidence |
| 9 | genau ein Release-ZIP, falls überhaupt ein Pluginpaket nötig ist |
| 10 | ein Live-Dry-Run |
| 11 | ein Live-Sync |
| 12 | finaler Readback / LIVE-PASS |
| 13 | erst danach Text-/Artikelproduktion über den Owner-Handoff |

---

# 5. Fehler- und Irrwegprotokoll – was ausdrücklich NICHT wiederholt werden darf

## Irrweg 1 – Pluginbau vor fertigem Kategorienbestand

**Fehler:** Nach einzelnen fachlichen Funden immer wieder neue ZIPs bauen.  
**Folge:** Uploadschleife, inkonsistente Kandidaten, Zeitverlust.  
**Neue Regel:** Erst kompletter Datenbestand + kompletter lokaler Beweis; dann ein Release.

## Irrweg 2 – technischer PASS wurde mit fachlicher Vollständigkeit verwechselt

Ein Dry-Run kann technisch PASS sein und trotzdem fachlich Kategorien fehlen lassen. Genau das passierte, als 279/279 `HOBBY_HUB` geprüft wurden, obwohl es insgesamt 330 terminale CORE-Identitätsseiten gab.

**Konkreter Fund:** 51 aktive terminale CORE-Seiten hatten überhaupt keine Content-Kategorien.  
**Neue Regel:** Gate immer über **alle terminalen produktiven CORE-Seiten**, nicht nur über eine Rollen-Untermenge.

## Irrweg 3 – PENDING/UNASSESSED Rollen veröffentlicht

46 Orientation-Overrides waren noch `PENDING/UNASSESSED`; 44 davon waren terminal. Dadurch blieben reale Endseiten ohne Leafs.

**Neue Regel:** Kein produktiver Zielbaum mit unresolved Rollen. Rolle vor Materialisierung final entscheiden.

## Irrweg 4 – künstliche 3–6-Leaf-Grenze

Ein altes Frontend-Gate behandelte die frühere Zielspanne wie eine harte Regel und konnte gleichzeitig 0-Leaf-Terminalseiten übersehen.

**Neue Regel:** Keine künstliche Obergrenze. `<3` tragfähige sichtbare Leafs bei einer terminalen produktiven Identitätsseite blockiert; 7, 8 oder mehr sind zulässig, wenn fachlich getragen.

## Irrweg 5 – 46 generische `Ausrüstung & Kosten`-Leafs

Diese Leafs wurden aus generischen Template-Intents abgeleitet und hatten keine echte hobbyindividuelle >=3-Intent-Evidence.

**Neue Regel:** Keine Standardkategorie nur weil sie in einer Schablone steht. Erst 3 echte Intents, dann Leaf.

## Irrweg 6 – Pilot-/Batcharbeit als Dauerproduktionsweg

10er-, 12er-, 16er- und andere Pilot-/Batchstände wurden zu lange wie Produktionsfortschritt behandelt.

**Neue Regel:** Pilot nur, wenn eine völlig neue Regel validiert werden muss. Danach globale Ausarbeitung in einem Datenlauf; keine endlose Batchserie.

## Irrweg 7 – DataForSEO/Keyword-Ideas als zu tiefer Pflichtpfad

Unnötige Keyword-Ideas-/Providerstrecken erzeugten Laufzeit, Kostenrisiko und zusätzliche Fehlerpfade, obwohl die Fachlogik die Struktur bereits bestimmen konnte.

**Neue Regel:** Fachlogik definiert Struktur und Content Capacity; DataForSEO prüft Nachfrage/Dedupe. Keine flächendeckende Tiefenrecherche als Normalweg.

## Irrweg 8 – `Hobbywelten` als Parent der acht Welten

Frühere Entwürfe bauten eine zusätzliche Ebene, obwohl die acht Welten selbst ROOT sein müssen.

**Neue Regel:** 8 Welten ROOT; `Hobbywelten` nur View/Übersicht.

## Irrweg 9 – Header/Frontend las Legacy statt ausschließlich aktives Target

Dadurch konnten alte Seiten, Editorial-Themen und Dubletten sichtbar werden.

**Neue Regel:** Headernavigation ausschließlich aus aktivem Target-Snapshot. Legacy/unmanaged darf nicht in die kanonische Navigation leaken.

## Irrweg 10 – falsche Magazinstruktur / Hobbyfinder

`Hobby finden` war als Hauptkachel vorhanden, `Hobbyfinder` darunter verschachtelt; `Alleine` und `Zu zweit` lagen falsch, `Gruppe` fehlte.

**Finale Regel:** `Hobbyfinder` ist direkte Magazin-Hauptkategorie. Darunter `Hobbywelten`, `Alleine`, `Zu zweit`, `Gruppe`. Altes `Hobby finden` archiviert.

## Irrweg 11 – stale Editorial-Verweise

22 `EDITORIAL_TOPIC`-Overrides verwiesen noch auf den entfernten Knoten `editorial:group:entdecken` und blockierten den Resolver.

**Neue Regel:** Nach Strukturänderungen vollständige Referenzintegrität prüfen; keine stale Node-IDs im Profil.

## Irrweg 12 – alte Revision / stale COMPLETE im UI

Ein gespeicherter `COMPLETE`-State einer alten Revision blendete einen neuen Apply-Schritt aus.

**Neue Regel:** COMPLETE gilt nur, wenn `state.revision === plan.profile_revision`. Alte COMPLETE-Zustände sind stale, nicht aktuell.

## Irrweg 13 – stale Export

Ein früher Download-Handler exportierte einen alten gespeicherten Stand, obwohl die Adminansicht schon neu berechnete Daten zeigte.

**Neue Regel:** Export selbst muss frisch validieren bzw. fail-closed blockieren. Nie UI-Anzeige und Download als identisch annehmen, ohne Hash/Readback.

## Irrweg 14 – Slug-/Legacy-Bindung und Adopt-Fälle

Reale Bestandsobjekte und alte Slugs konnten mit neuem Target kollidieren. Falsches CREATE+ARCHIVE hätte Identitäten zerstört.

**Neue Regel:** Stable IDs/legacy_ids erhalten; Adopt nur bei exakt sicherer Identität. Fremdname, falscher Parent, falsche Säule oder andere Bindung = BLOCKED.

## Irrweg 15 – Rollback war nicht vollständig transaktional

Ein absichtlich ausgelöster Fehler mitten in Metadatenwrites zeigte, dass eine Teiländerung stehenbleiben konnte.

**Fix:** Rollback korrigiert. Negativtest bewies danach `ROLLED_BACK` und identischen Vorher-/Nachher-Fingerprint.

**Neue Regel:** Kein Release ohne injizierten Write-Fehler und exakten Rollback-Fingerprint-Beweis.

## Irrweg 16 – Browserfehler `Unexpected token '<'`

Bei abgelaufenem Nonce bzw. HTML-Fehlerantwort versuchte der Client die Antwort direkt als JSON zu parsen.

**Fix:** AJAX-Pfad liefert kontrolliertes JSON; Client diagnostiziert Nicht-JSON über HTTP-Status + Antwortanfang.  
**Neue Regel:** Admin-/Resume-Pfad positiv **und negativ** mit gültigem und ungültigem Token testen.

## Irrweg 17 – 1.14.9 / 1.14.10 und unnötiger neuer Providerpfad

Zwischenversionen aktivierten unnötig wieder einen timeout-/provideranfälligen Keyword-Ideas-Weg und erzeugten Backend-Risiko.

**Neue Regel:** stabile 1.14.8-Codebasis schützen. Keine Wiederbelebung der verworfenen 1.14.9/1.14.10-Wege.

## Irrweg 18 – Livezahlen aus Erwartung statt aus Readback behauptet

Zwischendurch wurden erwartete Delta-Zahlen genannt, die vom realen Live-Dry-Run abwichen.

**Neue Regel:** Erwartung ist nur Erwartung. Sobald Live-JSON existiert, ist ausschließlich der Readback maßgeblich.

## Irrweg 19 – mehrere konkurrierende „Current“-Wahrheiten

Alte Übergaben/Konzeptstände enthielten überholte Blocker und Zahlen.

**Neue Regel:** `START_HERE → AUTORITAETSPLAN → genau eine Current-Autorität → NEXT ACTION`. Übergaben und Evidence sind Nachweis, niemals zweite Current-Wahrheit.

## Irrweg 20 – nach erstem gefundenen Fehler stoppen

Der alte Arbeitsstil reparierte den ersten sichtbaren Fehler und lieferte erneut aus. Weitere Fehler erschienen erst im nächsten Live-Lauf.

**Neue Regel:** Nach einem Fund nicht ausliefern. Den **gesamten** Baum und die **gesamte** Positiv-/Negativsuite weiterlaufen lassen, bis der komplette Prüfvektor grün ist.

---

# 6. Was beim neuen Thema nicht angefasst werden darf

Ohne einen durch lokalen Negativtest bewiesenen Enginefehler:

- keine neue Pluginarchitektur;
- keine Core-Umbauten;
- keine Rücknahme von Performanceoptimierungen;
- keine neuen DataForSEO-Providerpfade;
- keine Änderung an Writer/Sync/Resume/Rollback;
- keine neue Kategorie-Logik als PHP-Fix, wenn sie als Profildaten ausdrückbar ist;
- keine globalen Umbenennungen oder Reparents außerhalb des neuen Themas;
- keine Bestands-Leafs pauschal löschen;
- kein Hard-Delete;
- keine alten Pluginversionen wiederbeleben;
- keinen produktiven Sync starten, solange der lokale Gesamtbeweis nicht vollständig vorliegt.

---

# 7. Übergabeformat vom Nachbarchat an die Live-Stufe

Bevor der Nachbarchat ein Release freigibt, muss er genau dieses Abschlussprotokoll liefern:

**Zielvertrag**  
Was soll das neue Thema fachlich und geschäftlich leisten? Was bleibt unangetastet?

**Fachlicher Endstand**  
Rolle, Welt, Parent, Leafs, Supporting Intents, SEO-Owner, Magazin/DIRECTORY-Zuordnung.

**Delta gegen Live-Baseline**  
Exakte CREATE / UPDATE / MOVE / ARCHIVE / ADOPT-Liste. Nicht nur Summen.

**Statischer Beweis**  
Alle Baum-/Rule-2.7-/Ownership-/Parent-/Slug-/Terminal-Gates PASS.

**Lokaler E2E-Beweis**  
Positive Suite, negative Suite, Resume, Readback, Frontend, Idempotenz, Drift, Rollback.

**Releasebeweis**  
ZIP SHA-256, PHP-Lint, ZIP-Integrität, Dateidiff zur freigegebenen Codebasis.

**Live-Gate**  
Genau ein read-only Dry-Run. Nur bei exaktem Delta ein Sync.

**Post-Sync-Beweis**  
COMPLETE, 100% Readback, errors=[], Frontend/Header PASS, keine ungebundenen CORE-Seiten, danach LIVE-PASS.

---

# 8. Übergang zur Inhaltserstellung

**Texte beginnen erst, wenn die Owner-/Kategorieentscheidung stabil ist.** Sonst entstehen Artikel für später verschobene oder gelöschte Kategorien.

Für jeden Leaf:
- mindestens die 3 belegenden Artikelintents als Startbestand;
- je Artikel genau ein primärer Such-/Nutzerintent;
- keine zwei Artikel mit demselben primären Owner;
- interne Verlinkung auf Hobby-Hub und passende Geschwister-Leafs planen;
- Affiliate-/Anbieterpfad getrennt von der fachlichen Kategorieentscheidung behandeln;
- FAQ-Fragen nicht doppelt als Einstiegstexte und FAQ-Artikel besitzen lassen;
- Redaktionsplan erst nach Kategorien-LIVE-PASS an HD-002/Produktionsworkflow übergeben.

---

# 9. Exakter Startauftrag für den Nachbarchat

Diesen Block beim Start des neuen Chats verwenden:

> **Aufgabe:** Wir bearbeiten ein neues Thema für Hobbyrausch vom Konzept bis zur endgültigen Live-Umsetzung.  
> Lies zuerst die Datei `HOBBYRAUSCH_UEBERGABE_OPTIMIERTER_WORKFLOW_NEUES_THEMA_20261009.md` vollständig.  
> Lies danach die aktuellen autoritativen Project-Currents über `HOBBYRAUSCH/START_HERE.md → AUTORITAETSPLAN → zuständige Current`.  
> Arbeite ausschließlich als Delta gegen den bestehenden LIVE-PASS-Bestand. Keine Vollrekonstruktion des Portals.  
> Reihenfolge zwingend: Zielvertrag → Rolle/Parent → Intents → kompletter Kategorienbaum → Ownership → Magazin/DIRECTORY → statischer Gesamtcheck → vollständige lokale positive UND negative E2E-Simulation → erst dann ein einziges Release-Artefakt → ein Live-Dry-Run → ein Sync → Readback.  
> **NICHT RATEN. Nicht nach dem ersten Fehler stoppen. Keine Zwischen-ZIPs. Keine Architekturänderung. Keine Performance-Rücknahme.**  
> Wenn ein Fehler gefunden wird, korrigiere ihn lokal und fahre danach mit der gesamten Prüfsuite bis zum Ende fort.  
> Bevor du irgendeinen Upload verlangst, musst du den vollständigen lokalen Beweis vorlegen.

---

# 10. Quellen / belastbare Evidence dieses Abschlusses

Lokale Evidence-Dateien aus dem finalen Lauf:
- `HD001_FINAL_VERIFICATION_20261009.txt`
- `HD001_COMPLETE_CATEGORY_TREE_PROOF_20261009.json`
- `HD001_COMPLETE_LOCAL_E2E_PROOF_20261009.json`
- finales Release: `HD001_V1.14.8_RULE27_FINAL_VERIFIED_E2E_20261009.zip`
- ZIP SHA-256: `709134631895a901bcb4fc5f5d71889d317954d9928c0ed20700883990a5a52c`
- produktiver Abschluss-Readback: `hobby-depot-final-target-readback-20261009-170623-utc.json`

Autoritative Projektquellen:
- `protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH/START_HERE.md`
- `protocol/PROJECT_MEMORY/AUTORITAETSPLAN.json`
- `protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH/SEO_KATEGORIEN/CURRENT_STATE.md`
- `protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH/SEO_KATEGORIEN/ZIELVERTRAG_HD001_AUTOMATISCHE_SEO_HIERARCHIE_20261003.md` – Fassung 2.7
- `protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH/PLUGINS/PLUGIN_AKTEN/HD-001-KATEGORIE-WORKFLOW/CURRENT.md`
- `protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH/PLUGINS/REGISTER.md`

---

## Schlussregel

Der schnellste sichere Weg ist nicht „weniger prüfen“, sondern **nur einmal prüfen, dafür vollständig, bevor irgendetwas live geht**.

**Ein Thema → ein fertiger Datenstand → ein kompletter lokaler Hard-Pass → ein Release → ein Dry-Run → ein Sync → ein Readback.**

Genau diese Kette ersetzt die bisherige Upload-/Fix-/Upload-Schleife.