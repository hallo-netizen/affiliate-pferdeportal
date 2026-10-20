## HB-INS-20261020-07 – Begleitkategorie irrtümlich zum Vollportal ausgeweitet
**STATUS: FACHLICHE DIMENSIONIERUNG KORRIGIERT / WP-IMPORT UND PLUGIN-MOCK WEITERHIN OFFEN.**
FEHLER: Die 7. Hauptkategorie Versicherungen war auf 118 Seiten und 358 weitere Kategorien (476 Objekte) angewachsen und damit dem ursprünglich nur begleitenden Thema unverhältnismäßig groß. Auch der 433er-Vorläufer war bereits zu groß.
WARUM: Die 105 verschiedenen Versicherungsarten wurden fälschlich mit 105 eigenständigen WordPress-Seite3-Themen gleichgesetzt. Umfangreiche Detailprüfung einzelner Kategorien löste die übergeordnete Portal-Dimensionierung nicht.
KORREKTUR: Beschlossene Inhalte inklusive Renten-, Lebens- und Kapitalversicherungen **nicht streichen**; alle 105 eindeutig in nur 20 thematischen Sammelseiten unter fünf Bereichsseiten aufnehmen. 28 seltene Typen als künftige Einzelbeitrag-Kandidaten nur routen, ohne Artikel/Titel zu planen. 1+5+20+68=94 vorgesehene Objekte. Die 476/481/433-Importvorlagen sind abgelöst.
NACHWEIS: `KONZEPT/VERSICHERUNGEN_KOMPAKT_26_SEITEN_68_KATEGORIEN_105_THEMEN_20261020.json`; `KONZEPT/VERSICHERUNGEN_KOMPAKT_94_STRUKTURTEST_20261020.json`, 105/105 exakt einmal abgedeckt, 10/10 datenbezogene Negativfälle blockiert.
GRENZE: Diese Prüfungen validieren den neuen Plan, nicht die Live-Installation. Noch kein neues WP-/Plugin-Release, kein Import, kein kostenpflichtiger Provider-Aufruf.

## HB-INS-20261020-06 – Pauschale Drei-Kategorien-Schablone und fremde Artikelplanung
**STATUS: FACHLICHER ENTWURF KORRIGIERT / PLUGIN UND LIVE WEITERHIN OFFEN.**
FEHLER: Bei allen 105 Versicherungsseiten waren pauschal FAQ, Beratung und Leistungen & Praxis eingefügt; zusätzlich wurden 945 konkrete Artikelideen als Prüfnachweis mitgeführt. Das war keine ausreichend individuelle Kategorienprüfung und überschritt die Zuständigkeit.
WARUM: Zählen dreier Unterkategorien oder dreier hypothetischer Artikeltitel pro Rubrik ersetzt keine Prüfung des eigenen fachlichen Kategorie-Nutzens. Benutzerregel ausdrücklich: nur grob abschätzen, ob die letzte Kategorie etwa 3–5 spätere Beiträge tragen kann.
KORREKTUR: Alle 105 Owner auf grobe Themenfelder je Kategorie durchgegangen; FAQ/Beratung als regelmäßig sinnvolle Kategorien beibehalten, Sonderkategorien individuell. Fünf schwache Bereiche zusammengefasst. Aus 315 pauschalen Kategorien wurden 358 individuell bestimmte Vorschläge (68×3, 31×4, 6×5). Kein Artikelvorschlag und keine Artikelprüfung in der neuen Kandidatenvorlage.
NACHWEIS: `KONZEPT/VERSICHERUNGEN_KATEGORIEN_FACHPRUEFUNG_105_OWNER_20261020.json`, `KONZEPT/VERSICHERUNGEN_ADDONLY_476_FACHVORLAGE_20261020.json`, `KONZEPT/VERSICHERUNGEN_476_STRUKTURTEST_20261020.json`. Lokaler Datenstrukturtest 7/7 negative Mutationen abgewehrt; KEIN WordPress/Plugin-Test, keine Fachgarantie für jede spätere SEO-Veröffentlichung.
SPERRE: Die alten 433er-/481er-Kandidaten werden nicht importiert. Keine C2.3-471er-Wiederverwendung. Erst echtes Pluginverfahren mit Live-Readback und gesonderter Freigabe.

## HB-INS-20261020-01 – Falscher DataForSEO-Backendpfad
**STATUS: CLOSED für die beiden Originalabfragen; kein neuer Recherchelauf nötig.**
FEHLER: Nutzer wurde zunächst auf `Portal-Kategorien → SEO-Namen prüfen` verwiesen und aufgefordert, den DataForSEO-Zugang erneut zu überprüfen.
BEWIESENE URSACHE: `APKW_Category_SEO_Audit::profile/plan` arbeitet am aktuellen fest gebundenen CORE-Profil, nicht am neuen unimportierten Versicherungs-Seedinput. Der vorhandene `class-apkw-final-target-admin.php` enthält bereits **`Portal-Kategorien → DataForSEO Recherche`** mit JSON-Upload, kostenlosem Preflight und gesonderter kostenpflichtiger Ausführung.
KORREKTUR: Exakte Germany/de Keyword-Overview-JSONs mit 68 und 70 Seeds über vorhandenen Rechercheweg benutzt.
NACHWEIS: Zwei vom Nutzer gelieferte Originalproviderexporte vom 20.10.2026, 68/62 (0,01944 USD) und 70/66 (0,01992 USD), HTTP 200 / Status 20000. Kein Pluginumbau nötig.

## HB-INS-20261020-02 – Keywordmessung mit Discovery/Vollständigkeit verwechselt
**STATUS: PARTIAL CLOSED / FACHLICHE VOLLSTÄNDIGKEIT UND SEO-ARTIKELRECHERCHE NOCH OFFEN.**
FEHLER: Der erste 68er-Keyword-Overview wurde als weitreichende Kategorienrecherche nahegelegt, obwohl nur bekannte Eingaben gemessen wurden.
BEWIESENE URSACHE: Genutzter Endpoint `/v3/dataforseo_labs/google/keyword_overview/live` und die tatsächlichen Request-Arrays lieferten ausschließlich Keyword Overview; keine Keyword Ideas/Suggestions/organische SERP-Vollständigkeitsprüfung.
KORREKTUR: Zusätzliche 70 deduplizierte manuell recherchierte Seeds, zweiter echter DataForSEO-Lauf; Synonyme und Nebenpolicen einzeln geroutet. Nicht behaupten, die gesamten 105 Versicherungs-Owner seien Discovery-vollständig oder 945 Titel SEO-abgenommen.
NACHWEIS: Originalproviderexporte; `VERSICHERUNGEN_138_FACHENTWURF_105_R3_20261020.json`; `VERSICHERUNGEN_105_GESAMTPLAN_945_IDEEN_20261020.md`. Ein SEO-Volumen 0/null bleibt keine automatische Streichbedingung.

## HB-INS-20261020-03 – 471er-Importmodul für neue Versicherungsseiten fehlinterpretiert
**STATUS: LOCAL CLOSED (FALSCHE ROUTE ERKANNT) / VERSICHERUNGS-WP-INTEGRATION BLOCKED BIS GEPRÜFTEM ADAPTER.**
FEHLER: Die bestehende C2.3-471er-Importfunktion wurde zunächst pauschal als Pfad für alle neuen Versicherungsseiten nahegelegt.
BEWIESENE URSACHE: Das tatsächliche `includes/class-apkw-c23-471-add-only.php` ist auf 471 Blattkategorien **unter 265 bestehenden physischen R3-Ownern** gebunden und prüft diesen alten Livebestand. Es erzeugt **keine** neue R1/R2/R3-Versicherungswelt.
KORREKTUR: Keine Zweckentfremdung; 433 neue Versicherungsobjekte nur als ADD-only-Prüfvorlage gespeichert. **Künftige Umsetzung ausschließlich im vorhandenen zentralen Kategorieplugin nach Prüfung seiner tatsächlichen Erweiterbarkeit; kein Parallelplugin.**
NACHWEIS: `KATEGORIEN/C23_THIRD_WAVE_SOURCE/includes/class-apkw-c23-471-add-only.php`, `KATEGORIEN/CURRENT_STATE.md`, `KONZEPT/VERSICHERUNGEN_ADDONLY_433_OBJEKTE_VORLAGE_20261020.json`. Noch kein Plugin- oder WordPress-Live-Dry-Run für diese 433.

## HB-INS-20261020-04 – Artikelideen-Titeltest nicht mit SEO-/Fachendfreigabe gleichsetzen
**STATUS: OPEN / EDITORIAL-SEED, KEIN WP-RELEASE.**
FEHLER/RISIKO: Die Zahlen 315 Beitragskategorien und 945 voneinander unterschiedliche Artikelideen können einen nicht belegten redaktionellen End-PASS suggerieren.
URSACHE: Der aktuelle lokale Validator prüft Struktur, numerische Mindesttiefe, eindeutige Owner-/Slug-Bindung und exakte Titeldoppelungen, **nicht** die fachliche Notwendigkeit aller Kategorien, organische SERP, Textsubstanz oder Tarifbedingungen.
KORREKTUR: `VERSICHERUNGEN_105_GESAMTPLAN_945_IDEEN_20261020.md` und `KONZEPT/CURRENT_STATE.md` kennzeichnen alle Kategorien und Artikel als **vorgeschlagen/nicht importfreigegeben**; vor Live-Änderungen fachlicher und technischer Freigabepfad.
NACHWEIS: 105/315/945 lokal erneut gezählt; sechs negative Manipulationstests der 433er Kandidatenvorlage PASS_BLOCKED. **Nicht durchgeführt:** echter WP-Live-Readback, ZIP-/Plugin-Integration der Versicherungs-433, organische SERP-Artikeltitelvalidierung.

## HB-INS-20261020-05 – JSON-Übergabeartefakt nur lokal statt dauerhaft im Campus
**STATUS: CLOSED für die Sicherung / VERWENDUNG ALS WP-IMPORT BLEIBT BLOCKED.**
FEHLER: `HAB_BEWAHR_VERSICHERUNGEN_ADDONLY_433_OBJEKTE_VORLAGE_20261020.json` existierte nach der 105er-Planung zunächst nur in der lokalen Chat-Laufzeit, nicht im GitHub-Konzeptbüro; ein neuer Chat hätte die vollständigen Parentbindungen nicht direkt abrufen können.
URSACHE: Persistierung des Strukturbelegs war beim ersten Durchlauf nicht erfolgt.
KORREKTUR: Aus der **bereits dauerhaften GitHub**-Quelldatei `VERSICHERUNGEN_105_GESAMTPLAN_945_IDEEN_20261020.md` unabhängig 105/315/945 eingelesen und die rein additive 433er-Vorlage mit ihren Parent-Ownern erneut erzeugt und in derselben Konzeptablage unter `VERSICHERUNGEN_ADDONLY_433_OBJEKTE_VORLAGE_20261020.json` gespeichert. Keine zweite Current-Autorität.
NACHWEIS: GitHub-Commit `df6bc8dfdaedd4ba3c3e375d514fafb5da801d5c`; 433/433 Strukturbelege, 6/6 gezielte Negativfälle lokal abgewiesen. Die GitHub-Prüfvorlage ist **nicht** behauptet byteidentisch mit der vormals lokalen JSON-Arbeitskopie.

## HB-C22-20261017-INTENT-QA – Fachlich falscher PASS, Pflichtintents nicht abgesichert
STATUS: **OPEN / KEIN FACHRELEASE / KEIN LIVE-WRITE**.
FEHLER: Alle 566 importierten C2.2-Kategorien hatten `capacity_status=PLAUSIBLE_PROVISIONAL`, `indicators=[]`. Der C2.2-Fachvalidator nahm Zahl und behauptetes Beitrags-Potenzial als ausreichenden PASS; eine themenspezifische 3–5-Beitragsrichtungen-Eignung wurde nicht geprüft. Gleiche FAQ-Labels unter unterschiedlichen Seite-3-Ownern wurden durch einen globalen Namensvergleich fälschlich als Dublette gemeldet. Historisch fehlten FAQ und Vergleiche als konkrete Kategorien vollständig. Fachliche Zweifachrolle Seite3/WP-`category` wurde zeitweise verwechselt.
URSACHE: Schwacher C2.2-Validator; programmweit globale Label-Dublettenprüfung; statt individueller Intent-Abnahme nur pauschaler Kapazitätswert. Ursprünglicher Zielvertrag sah FAQ und Vergleich nur beispielhaft vor, obwohl der Nutzer am 17.10. ausdrücklich beides je konkrete Seite3 verbindlich erklärte.
KORREKTUR: Verbindlicher Nutzernachtrag wurde am 17.10. direkt in derselben C2.2-Zielvertrags-Hauptdatei ergänzt (GitHub Commit `033a55c0ff58aa6492a5f11ab761932a5883b440`). 172 FAQ und 172 Vergleichs-**WP-`category`-Kandidaten**, themenbenannt; 166 weitere Optionen geprüft, 103 beibehalten, 63 verworfen; Bestand 93/285/4 geschützt. Quelle für V3-Arbeitsstatus ausschließlich `KONZEPT/CURRENT_STATE.md`. Keine vierte WP-`page`-Ebene, keine verschachtelte `category`; keine unbelegten Editor-PASS-Claims.
TEST: Struktur-QA V2 19/19, V3 GitHub-Current 12/12 absichtlich beschädigte Fälle, später lokale ungebundene V3-Arbeitsdatei mit 566 Inhaltskategorien je drei themenspezifischen Richtungen und 15/15 negativen Mutationen. Dies **ist keine** unabhängige semantische Gesamtabnahme und kein Live-WP-Test.
REST: Redaktionsentscheidung und Migration/Owner für Altbestand, konkreter aktueller WP-Readback, Dry-run, kontrollierter Writer-Delta. Der neuere lokale 566-Scope-Entwurf ist noch nicht auf GitHub zur Current-Autorität gebunden; CURRENT bleibt bis dahin verbindlich bei **102/566 geprüft, 464/566 offen**. Zentrales ZielvertragsREGISTER enthält noch alte FAQ/5/4-Formulierung; Schreibversuch Sicherheitsblockade, Register-Sync **BLOCKED**.

## 16.10.2026 – ABSCHLUSSPRÜFUNG C2.2: ZENTRALE REGISTER NOCH HISTORISCH

## C2.2 Nachprüfung 16.10.2026 – 18 falsche potenzielle Altseitenrollen
Die frühere Vorprüfung ließ 31/93 alte Sammelseiten noch als möglicherweise C2.2-geeignete Themen stehen. Die konkrete erneute Betrachtung der vorhandenen 285 Child-Termnamen zeigt **18** davon mit objekt- und themengemischten Kindern (z. B. Stromausfallmelder / USV / Notstromversorgung). Die neue zurückhaltende Vorbewertung ist **75 breit**, **12 nur möglicherweise geeignet**, **5 unklar**, **1 Graffiti-Hub mit plausiblen Intentkategorien aber Artikelkapazität offen**. Die eigentlichen WordPress-Artikelzuordnungen sind aus dem 13.10. PostSync-Readback nicht ablesbar; deshalb bleibt jede Umhängung gesperrt. Nachweis: `C22_93_SEITEN_ALTE_SAMMELHUBS_KRITISCHE_NACHPRUEFUNG_20261016.json`.

## C2.2 Fehlerkorrektur 16.10.2026 – falsche neue Graffiti-Themenseite
Im 174/573-Entwurf wurde der alte echte Intent-Term **Graffiti entfernen** (historische WP-Term-ID 202) fälschlich nochmals als neue konkrete Seite3 mit vier weiteren Artikelkategorien geplant. Die schon existierende Seite **Graffiti: Schutz & Hilfe** (historische WP-Page-ID 158) umfasst die drei vorhandenen passenden Artikelkategorien „Graffiti vorbeugen“, „Graffiti entfernen“, „Graffitischäden & Kosten“. Fachliche Korrektur: neue Doppel-Seite samt vier Vorschlagkategorien aus `C22_GESAMTBAUM_KORRIGIERT_173_THEMEN_569_ARTIKELKATEGORIEN_20261016.json` entfernt; kein WordPress-/Plugin-Write. Die alten 174/573-Akten sind historischer Datenbeleg, **nicht aktueller Sollbaum**. Vier weitere alte Kategorie-Namenskollisionen mit neu vorgeschlagenen Themenseiten sind getrennt unter `C22_285_ALTKATEGORIEN_TERM_ID_ROLLEN_OWNER_MIGRATIONS_MATRIK_20261016.json` gesperrt.
Das bisherige Menü-„36 von 36 Bereiche brauchen Mehr“-Ergebnis galt nur für den falschen Vorentwurf. Korrekt ist **35 mit Mehr-Link, einer (Fassade & Außenflächen) ohne**. Aktueller Live-Readback fehlt weiterhin. Kein C2.2-Release.


## Nachtrag 16.10.2026 – C2.2-Kategorie-/Navigationsfehler und Registerbereinigung
- **Alte künstliche Dreiergrenze:** In der ersten C2.2-Entwurfsausarbeitung wurden alle neuen konkreten Themenseiten zunächst wieder mit genau drei Contentkategorien versehen. Dies wurde nach fachlicher Prüfung korrigiert: jetziger Gesamtentwurf hat 3/4/5 Artikelkategorien je konkreter Themenseite, ohne Maximalregel. Das ist weiterhin ein redaktioneller Entwurf, kein PASS für 285 historische Kategorien.
- **Widerspruch im zentralen Zielvertragsregister:** `protocol/PROJECT_MEMORY/ZIELVERTRAEGE/REGISTER.md` wurde am 16.10.2026 auf den aktiven C2.2-Vertrag korrigiert; historischer 3–10-Eintrag trägt jetzt ABGELÖST. Dieser konkrete Registerfehler ist damit `CLOSED`. Alte V9-Fehler und nicht bestätigte WordPress-Live-Revision bleiben separat offen.
- **Verhinderte Namensdubletten:** 52 wiederverwendete Artikelkategorielabels in vier ursprünglichen Entwurfsdateien themenspezifisch eindeutig benannt, anschließend die Kollision mit geschützten WordPress-Altkategorien korrigiert. All diese Handlungen betreffen nur GitHub-Fachentwürfe, keine WP-Terminhalte.
- **Bestand vs. Sollentwurf:** 57/93 bisherige Seite-3-Bündel sind nach erster manueller Prüfung zu breit, 31 thematisch eventuell geeignet und fünf Grenzfälle; nichts automatisch umzubenennen, umzuhängen oder zu löschen. Benötigt identitäts-/URL-sichere Einzelentscheidung.

- Zentraler Zielvertragswegweiser `protocol/PROJECT_MEMORY/ZIELVERTRAEGE/REGISTER.md` führt den historischen HB-R3/3-bis-10-Vertrag noch mit `STATUS: AKTIV`; dies ist ein nachgewiesener veralteter Registereintrag, **nicht** der gültige Zielvertrag. Verbindlich ist Fassung 2.2 in `KONZEPT/ZIELVERTRAG_KATEGORIEN_MINDESTENS_3_OHNE_MAXIMUM_20261015.md`, im Konzept-Current als aktiv geroutet.
- Der zentrale `FEHLERREGISTER.md` zeigt einen alten V9-/R2-Zwischenstand. Auch dieser Wegweiser ist keine Current-Wahrheit. Autoritative Fehler stehen in dieser Fehlerquelle, Current nur in Konzept-Current.
- Mehrere Versuche, das zentrale Zielvertragsregister zu korrigieren, wurden vom GitHub-Schreibzugriff mit einer Sicherheitsblockade abgewiesen; **nicht als aktualisiert bezeichnen**. Für die Übergabe: Register-Nachholung BLOCKED bis Schreibzugriff diese Änderung zulässt. Keine zusätzliche Current-Datei anlegen.

## 16.10.2026 – V9.23 KATEGORIENROLLEN-FEHLER (LETZTE SEITE ≠ LETZTE CONTENTKATEGORIE)
**Ursache:** Sach-/Produktnamen (z. B. `Garagentor-Funksteuerung`) wurden in V9.13/V9.18 direkt als `category`-Endknoten unter `Garagentore & Antriebe` statt als **konkrete letzte Themenseite** mit weiter darunter passenden **intentbezogenen flachen Artikelkategorien** vorgeschlagen. 46×3 allgemeine Sachfelder in V9.22 belegen nicht 3–5 Artikel pro tatsächlichem Intent-Leaf. Die zuvor behauptete universelle fachliche Eignung der 46 Einträge ist daher keine Releasefreigabe.
**Belegte Architektur ohne Neuerfindung:** Plugin 1.14.8.21 `includes/class-apkw-target-tree.php` fordert optional `require_three_page_levels` und hat `NODE_CATEGORY_UNDER_CATEGORY`; Quelle Pferdeatelier `protocol/PFERDE_ATELIER_CATEGORY_CHANGE_MASTER_20260922.md` zeigt bereits reale Produktseite + FAQ/Beratung/Vergleich/etc. als nicht bindende BEISPIELE. Keine übertragene Hobby-/Pferde-Kategoriemenge.
**Künftig richtig:** Weltseite → Bereichsseite → **konkrete Themen-/Produktseite** → **variable passende Artikelkategorien nur zu diesem Thema** → Beiträge. Min3 sinnvoll eigenständige spätere Beiträge je letzte Kategorie, FAQ/Beratung/Vergleich/Kosten nur Optionen. Mindest-3-Kinder ohne Obergrenze für höhere Ebenen; Thema-/Produktseite hat keine eigene Artikelquote. Keine vollständigen Artikeltitel- und Textproduktionsaufgaben im Kategorieplugin. Spätere SEO-Engine kann zusätzliche Kategorien vorschlagen.
**Sicherheit:** R3/V99-Bestand möglicherweise live, gemeldete V99-Revision und Export, kein frischer Readback; keine Auto-Umbenennung, -Verschiebung, -Löschung oder -Synceingriffe. Vor Freigabe neues korrektes ADD-Delta und positive/negative echte WP-/Plugin-Simulation. Aktive Autorität nur `KONZEPT/CURRENT_STATE.md`, Writer nur `KATEGORIEN/CURRENT_STATE.md`.

## 16.10.2026 – ROLLENTRENNUNG: KATEGORIEN VS. ARTIKEL SEO/TEXT (V9.22)
- **Vormals falsch:** Das Konzept-/Kategorienbüro schrieb für 46 neue Blätter 214 detaillierte Artikelideen und prüfte einzelne künftige Artikelüberschriften gegen tausende alte Artikel – obwohl der Nutzer nur eine **grundsätzliche 3–5-Beiträge-Füllbarkeit der untersten Kategorieebene** verlangt. Es erschwerte und verzögerte die Freigabe durch künstliche Artikel-Owner- und SEO-Textgates.
- **Korrektur:** Aktiver Zielvertrag 2.1 (16.10.2026) ersetzt die Pflicht zu 3–5 ausformulierten Artikeltiteln durch **ein kurzes 3–5-Themenfeld-Potenzialprofil ausschließlich der untersten Kategorie**; 3+ fachlich sinnvolle direkte Kinder in Zwischenbereichen **ohne Obergrenze**. Detailartikel, Suchfragen, Titel, SEO-Briefs, Textproduktion, Post-Kategorie-Zuordnung sind Aufgabe späterer getrennter SEO-/Text-Plugins. Artikelnotizen aus V9.x bleiben historisch und nicht bindend.
- **Pferdeatelier ausdrücklich NUR gelesen:** Projektgebäude START_HERE, eigene TEXT-Produktion, separate 4a-Produktionssteuerung, Wissensdatenbank `Rechercheobjekt ≠ Artikel ≠ Kategorie`, SEO-Handoff ohne WP-Kategorie-ID/nachgelagerte Kategorieauflösung. **Nichts im Pferdeatelier geschrieben oder übernommen**.
- **V9.22 korrekt fachlich nachgearbeitet:** 46/46 zusätzlichen Kategorien 3 allgemeine Themenfelder als grundsätzliche Tragfähigkeitsprüfung, **keine fertigen Artikel**, kein WP-Write. 81 ältere V99-Neublätter noch für diese schlankere Prüfung offen.
- **Nicht wiederholen:** Kategorien nur deshalb blockieren, weil zwei hypothetische künftige Artikelüberschriften sich ähneln oder der DataForSEO-Dienst keinen Suchvolumenwert liefert. Echte doppelte Kategorie-Owner oder nur 1–2 tragfähige Themenfelder weiterhin fachlich untersuchen.
- Einzige aktuelle Arbeit und NEXT ACTION: `KONZEPT/CURRENT_STATE.md`, technischer Writer `KATEGORIEN/CURRENT_STATE.md`.

## HB-ERR-20261016-V918 – Dreierdeckel und SEO-Volumen NICHT wieder einführen
- **Ursache:** Der R3-Code und die alte V9-Planung erzwangen künstlich Dreiergruppen, obwohl seit 15.10.2026 **mindestens drei und keine Obergrenze** verbindlich ist. Formale 3-von-3-Prüfungen sind KEINE vollständige Sachthemenprüfung.

## 16.10.2026 – V9.20/V9.21 ARTIKELINTENT-QUALITÄT / ALTOWNER
- **Nachgewiesener Altartikelkonflikt:** Originales R2-Blatt `Garagenzufahrt & Hofabläufe` besitzt bereits den Artikel `Tiefgaragenzufahrt an einem Wohnhaus gegen Starkregen schützen`. Der in V9.17/V9.18 geplante Beitrag `Tiefgaragenzufahrt bei Starkregen gegen Wasserzufluss sichern` bediente dieselbe Suchintention. Entwurfsbeitrag in beiden Quelldateien ersetzt, alter Artikel/WordPress unverändert.
- **Zwei weitere Textwiederholungen innerhalb der NEUEN Entwürfe** bei Boiler-Temperatur/Thermostat und Video-Sprechanlage Bildausfall/Nachtsicht korrigiert. Explizite inhaltliche Begründung in `V9_20_46_ENDBLAETTER_ARTIKELQUALITAET_R2_ABGRENZUNG_20261016.json`.
- **Warnung gegen Dreierzahl-Schein-PASS:** Drei neue Tor-/Funkkategorien haben 4 Titel, aber teilweise denselben Fehlersuchintent; deshalb **EDITORIAL_DEPTH_HOLD**, keine Freigabe nur anhand der Artikelanzahl. Insgesamt 12 manuell gekennzeichnete Problem-/Grenzfälle unter 46 Vorschlagsblättern.
- **Aliasse:** `V9_21_46_KURZE_MENUEALIASE_OHNE_WP_UMBENENNUNG_20261016.json` bietet 46 eindeutige kurze UI-Bezeichnungen, die NICHT als durch echten DataForSEO-Task gemessene Keywordnamen gelten. Lange H1 erlaubt; kein blindes Live-Rename oder neues Plugin.
- **Nischen-Schutz:** Auch bei DataForSEO 0/null/kein Treffer niemals allein wegen Nachfrage gering löschen, umhängen oder abwerten. Min3 sinnvoll, keine Obergrenze, inhaltlicher Scope vor Keyword-Zählung.
- **Autorität/Next Action:** ausschließlich `KONZEPT/CURRENT_STATE.md`, technischer Schreibweg ausschließlich `KATEGORIEN/CURRENT_STATE.md`.

- **Nachprüfung heute:** Echter Originaldatenbestand vollständig nach 31/31 Bereichen, 93/93 bestehenden Unterbereichen und 285/285 vorhandenen Blättern einzeln inventarisiert; noch KEIN vollständiger semantischer PASS aller 1136 historischen Artikel.
- **Konkret ergänzte Themen:** V9.10 6 Blätter/30 Ideen; V9.12 21/105; V9.13 16/64; V9.17 3/15. Im zentralen Büro als **ein einziges Entwurfsdelta V9.18: 46 Blätter/214 Artikelideen** gesichert, 11 sinnvolle neue Unterbereiche und ein eigener Bereich Tore & Zugangstechnik; alle alten IDs/Namen/URLs unverändert.
- **DataForSEO richtig verwenden:** Aus dem echten Germany/de-Export 570 angefragte Wörter, 51 Treffer nur zur Benennung/Suchintentionshilfe. V9.15 dokumentiert 21 mögliche kurze Anzeige-Aliasse mit jeweils wörtlich genanntem Referenzkeyword (ggf. nur inhaltlich verwandt). 519 Null-/Kein-Treffer sind niemals Kategorie-Verwerfungsgrund.
- **Dubletten-Gate:** V9.18 0 exakt identische neue Blattnamen zu 285 CORE +81 V99 und 0 exakte Titeldubletten zu V99, zusätzlich V9.19 0 exakt gleiche neue Artikelüberschriften zu aus R3/R2-Crossmatch greifbaren Quellwortlauten, aber 11 lexikalische Ähnlichkeitsmeldungen (nur zwei neue Blätter, überwiegend verschiedene Schutzobjekte). Nicht mit vollständiger SEO-Semantikprüfung verwechseln.
- **Tests:** 1 korrekter V9.18-Datensatz und 6 absichtlich fehlerhafte Varianten lokal geprüft, alle Prüfungen verhalten sich entsprechend; **kein WordPress-/PHP-Livetest für neues Delta**. Kein Plugin/ZIP aus dieser unfertigen SEO-Fachplanung erstellen.
- **Aktueller Einzelstand / genau eine NEXT ACTION:** Nur in `KONZEPT/CURRENT_STATE.md`, technischer Writer nur `KATEGORIEN/CURRENT_STATE.md`.

## V9.8 BESTANDSSCHUTZ / WEITERE SACHLÜCKEN – 15.10.2026 (keine zweite Current-Autorität)
- **Zwingende Nutzerregel:** Alle 285 vorhandenen Endkategorien plus 6 Welten / 31 Bereiche / 93 Unterbereiche behalten Namen, IDs, Slugs, Parent, Artikelzuordnung und URLs unverändert. Keine Bestandsumbenennungen. Neue Daten ausschließlich unter dem zentralen Kategorienbüro schreiben, nicht aus Konzept.
- **Dublettenbremse:** Historisches R2 `Diebstahl an Außentechnik` enthält Ladekabelschutz bereits; daher kein neuer Ladezubehör-Blattowner. Vorhandenes `Oldtimer & Privatwagen` gehört dem ganzen Fahrzeugdiebstahl, neue R2/R3-unbesetzte Kandidaten erhalten spezifische **Bauteildiebstahl**-Scopes. `Sturm & Hagel beim Camping` bleibt Wohnmobil-Owner, keine Umbuchung.
- **V9.8 reine Konzeptverbesserung:** Drei ergänzende Fachunterbereiche und zwei Einzelblätter an bestehender Subarea: 11 Blattkandidaten / 55 verschiedene Artikelideen, davon zwei früher falsch zugeordnete **unveröffentlichte Entwürfe** jetzt im Konzept mit passendem Parent. Zusammen mit V9.6/V9.7 bei separater Freigabe rechnerisch 81 Blätter / 364 Themen; drei Tor-/Zugangstechnik-Parentfragen weiter zurückgestellt. Neun ältere zurückgestellte V9-Kandidaten weiterhin nicht freigegeben.
- **QA:** 11/11 Endblattideen mit fünf eigenen Artikelthemen; 55/55 Titel eindeutig; lokaler Einzel-Positivtest PASS, sieben absichtlich falsche Negativfälle erfolgreich gesperrt. Keine vollständige 1136-Titel-Intent-Bewertung; sechs R2-Originaltitel unbekannt.
- **Beleg:** `V9_8_11_NISCHEN_55_ARTIKEL_BESTANDSFEST_NICHT_IMPORTIEREN_20261015.json`. Aktueller fachlicher Status und GENAU EINE NEXT ACTION nur `KONZEPT/CURRENT_STATE.md`. Kein WordPress-Write, kein Plugin-Download.

## V9.6 / V9.7 Quellen- und Elternpruefung – 15.10.2026
- Historisches Kategorie-Workflow-Plugin 1.14.8.9 im Eigentumsschutz-Archiv vorhanden. Originalprofil liefert 686 Alt-Titel aus 137 Bestandskategorien, alle 137 logischen IDs passen. Das Plugin ist NICHT die aktive 1.14.8.19 und darf nicht installiert werden.
- Insgesamt 1130/1136 originale Titel lesbar; sechs R2-Titel bleiben offen. Der Vergleich 686 zu den urspruenglichen 212 V9-Ideen zeigt null exakte Duplikate, jedoch lexikalische Verdachtsfaelle und keine komplette semantische Freigabe.
- V9.6: 67 Redaktionskandidaten, 294 Ideen, sechs Elternkonflikte; Dachgeschoss- und PV-Themen redaktionell schaerfer getrennt.
- V9.7: Drei eigenstaendige Pool- und Teich-Endkategorien unter einem neuen Vorschlags-Unterbereich, je fuenf Themen. Bei spaeterer Freigabe 70 Kandidaten mit 309 Ideen und fuenf offenen Elternkonflikten.
- Zustaendige aktuelle Arbeit und exakt eine NEXT ACTION: KONZEPT/CURRENT_STATE.md. Technischer WordPress-Schreiber: ausschliesslich zentrales KATEGORIEN-Buero. Kein Plugin-Download, kein Live-Write.

## V9.5 Audit-Nachtrag (15.10.2026)
- Nach verschärfter Drei-bis-fünf-Artikel-Regel sind 67 von 73 neuen Vorschlägen konzeptionell weiter tragfähig; 6 wegen unpassender Elternkategorie zurückgestellt.
- In 12 Kategorien wurden Überschriften für unterscheidbare Sachfragen korrigiert.
- Positivprüfung bestanden; fünf absichtlich fehlerhafte Eingaben wurden im lokalen Datencheck korrekt abgewiesen.
- Ungeklärte Bestandsartikel und ein vollständiger WordPress-Test bleiben Blocker. Keine Installation.
- Genaue Nachweise und einzelne nächste Aktion ausschließlich unter KONZEPT/CURRENT_STATE.md; Einzelakte V9_5_73_ENDBLATT_3_BIS_5_ARTIKEL_FACHPRUEFUNG_NICHT_IMPORTIEREN_20261015.json.

## NACHHOLBELEG V9.4 – 15.10.2026 (KEIN CURRENT)
**Status-/NEXT-ACTION-Autorität ausschließlich `KONZEPT/CURRENT_STATE.md`.**

- **HB-CONCEPT-V9-012 – weiterer Sachschutz fehlt:** Nach Sichtung aller sechs Hauptgefahren und der 31/93/285-Bestandsstruktur zeigen sich vor allem Tier- und Schädlingsschäden an Haus/Fahrzeug/Außentechnik, Gebäudefolgeschäden nach Brand, Ausfälle motorisierter privater Tore, Hagelschaden an normalen Privatwagen sowie spezifische Feuchtefolgeschäden (Hausschwamm/Poolleitungen) ohne ausgewiesene eigenständige Endkategorie. Ein Katalysatordiebstahl-Thema gehört zunächst zum bestehenden Pkw-Owner. **Vandalismus und weitere Einbruch-Kategorieäste nicht künstlich aufblasen.**
- **Fachgegenmaßnahme nur als Audit:** `V9_4_GESAMTLUECKENPRUEFUNG_6_WELTEN_31_93_NICHT_IMPORTIEREN_20261015.json` enthält **19 neue potenzielle** Einzelblätter / 76 Artikelideen (9 Tier/Schädlinge, 3 Brandfolgen, 3 Tor-/Zutrittsantriebe, 4 Einzelkandidaten), noch **NICHT** in den 54/242-V9.3-Kandidatenstand integriert. Drei vollständige neue Gruppen erfüllen lokal mindestens drei Kinder; 5/5 beschädigte Negativfälle wurden von der isolierten Datenprüfung erkannt. Dies ist kein echter Google-SERP- oder WordPress-/Plugin-PASS.
- **Quellen-/Owner-Grenze:** Vergleich der aktuell textgenau erreichbaren Titel enthält nur 510 individuell ausgewiesene alte R2-Match-Titel von ursprünglich 704, dazu 432 R3/V8- und 242 V9.3-Titel. Die ursprünglichen sechs R2-Delta-Titel bleiben offen. 19 neue Vorschlagskategorien daher fachlich nicht releasefreigegeben; Vegetationsbrand und Hausschwamm benötigen besonders Eltern-/Owner-Prüfung. Wortgleichheit 0 beweist keine semantische Dublettenfreiheit.
- **Installationsregel:** Nur ein wirklich zur Nutzung freigegebenes und reproduzierbar getestetes Plugin-ZIP an den Nutzer ausgeben; Konzept-/Prüfarchive nicht als Download anbieten. Kein V9.4-Plugin, kein WP-Write.

## NACHHOLPRÜFUNG V9.3 – Brand an Auto / Wohnmobil / Freizeitboot – 15.10.2026 (kein Current)
**Fach-Status und NEXT ACTION:** nur `KONZEPT/CURRENT_STATE.md`.

- **HB-CONCEPT-V9-011 – Echte thematische Brandlücke:** R3/V8 hat unter `Feuer & Gase` spezifischen Camper-/Wohnmobil-Brandschutz, aber weder eigenständige PKW-/Oldtimerbrand- noch Bootsbrand-Endkategorien. Die vorher vorgeschlagenen drei Bootskategorien unter `Camping` waren wegen falschem Elternbereich zu Recht nicht importierbar. **Korrektur ausschließlich im V9.3-Konzept**: neue Untergruppe `Brände an Privatfahrzeugen & Freizeitbooten` unter `Rauch & Brand`, sechs Blätter (inklusive Elektroauto/Bootsmotor/Bordgas/Bordstrom/Kajütenwarnung), fünf Artikelideen je Blatt. Vorhandenes Camping nicht kopieren.
- **Beleg und QA:** `V9_3_BRAND_AUTO_BOOTE_54_KATEGORIEN_242_IDEEN_NICHT_IMPORTIEREN_20261015.json`: 54 V9.3-Kandidaten / 242 Titel, 9 Blätter gesperrt, **11/11 lokale Zusatzprüfungen PASS**. Keine vollständige semantische oder technisch/WordPress-live Freigabe.
- **Noch offen:** sechs Originaltitel im 12.10. R2, abschließende SEO-Owner-Abgrenzung, Kategorie-Workflow-Delta mit Slug-/URL-/Artikel-/Link-Prüfung sowie vollständigem WordPress-Readback. Plugin-Quellpaket 1.14.8.19 nicht als prüfbarer Installationsstand bestätigt. **Release BLOCKED.** Keine neue Plugin-ZIP anbieten, bevor wirklich installationsfertig.

## NACHHOLPRÜFUNG V9.2 – 15.10.2026 – STATUS NUR IN CURRENT_STATE
- **V9-008 – doppelter Frost-Artikel:** V9.1-Entwurf `Dachrinnen & Fallrohre` hatte „Frostschäden an Regenfallrohren frühzeitig erkennen“; bestehende R3/V8-Kategorie `Gefrorene Außenentwässerung` führt bereits „Frostschäden an Dachentwässerung erkennen“. **Korrigiert im V9.2-Entwurf:** loser Halt von Fallrohrschellen an der Hauswand statt zweiter Frost-Ratgeber. Kein WordPress-Write.
- **V9-009 – keine aktuelle Pluginquelle:** Installation des bestehenden Kategorie-Workflow 1.14.8.19 im historischen WP-Readback bekannt; Original-Plugin-ZIP/kompletter aktueller Quellcode nicht in vorliegenden Dateien bestätigt. **Daher kein installierbares V9.2-Plugin freigeben und keinen Entwurf als Plugin ausgeben.**
- **V9-010 – neue Einzelprüfung:** `V9_2_48_KATEGORIEN_212_IDEEN_REDAKTIONELL_NICHT_IMPORTIEREN_20261015.json` im Konzeptbüro; 48/212 weiterhin nur Kandidaten; 9/27 separat zurückgestellt; 4 konkrete redaktionelle Revisionen seit V9; 16/16 lokale Datenintegritätsprüfungen PASS. **Nicht** ein 1.136-Ideen-Semantik-/WordPress-Live-PASS. Zum individuellen Originalabgleich dieser Runde waren 510 R2-Titel als Matchtexte in der R3-V8-Originalprüfung und 432 R3-Titel benannt; sechs 12.10.-R2-Titel weiterhin nicht belegt.
- **Erster offener Blocker:** sechs verbleibende Originaltitel + Fach-Owner-Abnahme; technische Preflight-/WordPress-/URL-/Rollback-Prüfung später im zentralen Kategorienbüro. Einzige aktive NEXT ACTION siehe KONZEPT/CURRENT_STATE.md.

## NACHHOLBELEG V9.1 – 15.10.2026 (kein eigener Current)
**EINZIGE AKTUELLE STATUS-/NEXT-ACTION-QUELLE:** `KONZEPT/CURRENT_STATE.md`. Die historischen Formulierungen „18 fehlende Originaltitel“ und „zwei nicht belegte Moves“ in den weiter unten archivierten V9-Akten sind durch Originalquellenfund **teilweise bzw. vollständig überholt**.

- **V9-002 Fortschritt:** In `R3_V8_R2_VOLLSTAENDIGER_INTENT_ABGLEICH_144_20261013.json` wurden 12 von 18 zuvor nicht ausgelesenen R2-Originaltiteln mit genauem Wortlaut und Original-Owner wiedergefunden und im `V9_R2_12_ORIGINALTITEL_19_TRANSFERS_QUELLENFUND_20261015.md` archiviert. Nur **6 exakte Titel bleiben offen**. Keine Ersatzformulierungen als angebliche Originale.
- **V9-006 historische Transfer-Beleglücke GESCHLOSSEN:** Neben den 17 einzeln gelisteten Moves stehen zwei zusätzliche, vom alten `Überspannung im Haus` ausgehende Transfers wortgenau in `R3_V8_33_OWNER_GRENZEN_R2_ORIGINAL_20261013.md`. Das 19er-Original-QA bestätigt 19 geplante Vorgänge. **0 Moves jetzt durchgeführt**, kein Live-Transfer nachträglich behaupten.
- **V9-007 Konzept-Draft lokal verbessert, WP unverändert:** 48 Kandidaten/212 Ideen und 9 Zurückstellungen getrennt gehalten, 3 Kandidaten/Ideenpakete redaktionell umformuliert, 1 bestehender Artikel-Owner als Transfer-Gate erkannt. 12/12 lokale Datenchecks, 5/5 absichtliche Beschädigungen erkannt. Noch KEINE semantische Vollfreigabe, kein tatsächlicher WordPress-Release.
- **Release:** BLOCKED, bis sechs verbliebene Originaltitel und technische Kategorie-Workflow-Prüfung geklärt sind.

## NACHHOLPRÜFUNG V9 – AKTUELLE FEHLERKETTE, 15.10.2026 (kein eigener Current)
**Einzig maßgeblicher STATUS und NEXT ACTION:** `KONZEPT/CURRENT_STATE.md`. **LIVE-R3/V8-Readback 546/546 PASS vom 13.10.2026.** Die unten historisch fortgeschriebenen Behauptungen „R3 nicht live“, „WP-Sync ausstehend“ und „maximal 10“ sind für den gegenwärtigen Fachauftrag **ÜBERHOLT**. Gültiger Zielvertrag: `ZIELVERTRAG_KATEGORIEN_MINDESTENS_3_OHNE_MAXIMUM_20261015.md`.

### HB-CONCEPT-V9-001 – Künstlich auf drei gestoppter Ausbau
- **Fehler:** 31/31 Bereiche besitzen exakt drei Unterbereiche, 87/93 Unterbereiche exakt drei Blätter, sechs je vier, obwohl allein fachliche Notwendigkeit die Zahl bestimmen sollte.
- **Belegte Ursache:** R2 hatte 19×1, 10×2, 2×3 Unterbereiche; R3/V7 ergänzte rechnerisch genau 48 Unterbereiche mit je drei Endblättern. Der so erreichte 3–10-Struktur-PASS beweist **keine fachliche Vollständigkeit**. Es ist keine Menü-Anzeige-Abschneidung belegt.
- **Korrektur:** Alter 3–10-Vertrag als HISTORISCH markiert; Zielvertrag V2 fordert mindestens 3, keine Obergrenze, pro CORE-Blatt ≥3 (vorzugsweise 5+) individuelle Artikelideen. 31/31 Bereiche und 93/93 Unterbereiche in V9-Daten erneut aufgenommen.
- **Test:** Original-V9-JSON mit 31 Bereichen, 93 Unterbereichen, 285 bestehenden Blättern; 546/546 V8-Readback laut Current und V9-Fachprotokoll. **Status: FACHREGEL KORRIGIERT / WP-V9-ERWEITERUNG BLOCKED.**

### HB-CONCEPT-V9-002 – Achtzehn nicht textgenau verfügbare R2-Originalideen
- **Fehler/Blocker:** Für vier am 12.10. ergänzte Kategorien fehlen **18 exakte alte Titel**: `core:leaf:exp:c140`, `core:leaf:exp:c216`, `core:leaf:exp:gartenhaus-feuchte-20261012`, `core:leaf:exp:gartentor-20261012`.
- **Ursache:** Im tatsächlich textgenau gelesenen alten Paket vom 10.10. nur 686 Ideen/137 Blätter; spätere R2-Stufe meldete 704/141, die 18 Titel sind aus den bisher zugänglichen Originaldateien nicht belegt. Sie **dürfen nicht rekonstruiert** werden.
- **Gate:** 686 R2 + 432 R3/V8 = 1.118 von 1.136 Originaltiteln lexikalisch prüfbar. **Status: OPEN / ERSTER OPERATIVER BLOCKER.**

### HB-CONCEPT-V9-003 – Fachliche Doppelungen / falsche Eltern
- **Fehler:** V9 enthielt 57 Kandidatenblätter und 239 Ideen, davon 3 Kandidatengruppen mit **9 Blättern/27 Ideen** wegen möglicher Dublette oder falscher Elternzuordnung zurückgestellt.
- **Gegenmaßnahme:** nicht still umbenennen/importieren; nur 48/57 Blätter mit 212 Ideen **weiter prüfen**, nicht freigeben. **Status: BLOCKED FÜR 9; WEITERE 48 IN REVIEW.**

### HB-CONCEPT-V9-004 – Fehlende SEO-Owner-Abnahme
- **Fehler:** 57 neue Blatttitel/239 neue Artikeltitel sind zwar textuell eindeutig; vollständige Alt-Themenabdeckung und eindeutige semantische SEO-Owner sind damit nicht bewiesen. Vier+ weitere auffällige lexikalische Nähen erfordern Prüfung.
- **Nachweis:** Current nennt lokale 57/57-Gegenprüfung und 6/6 Negativfälle mit absichtlich falschen Daten, darunter 2-Ideen-Blatt, doppelte Titel und unberechtigtes WP-Write. Die im Arbeitsverzeichnis separat vorhandenen V9-Entwurfsdateien enthalten 31/93/285 Bestandsregister und 57/239 Vorschläge. Die V9-Zweitprüfung ist nicht gleich WP-/SEO-Release-PASS.
- **Status: OWNER-FREIGABE OFFEN / RELEASE-GATE BLOCKED.** Keine kostenpflichtige SERP-Pflicht, keine automatischen neuen Provideraufrufe.

### HB-CONCEPT-V9-005 – Fehlerquelle/Routinghistorie veraltet
- **Fehler:** Ältere Teile dieser Fehlerakte, das zentrale Fehlerregister, der Konzept-Hobbyraum und die Projekt-Bürotür verwiesen noch auf R2/3–10 bzw. R3-live-offen.
- **Korrektur:** V9-Nachholvermerk hier; zentraler Fehler-Wegweiser und rein navigierende Projekt-/Hobbyraumtexte auf Current-Routing und Vertragsautorität korrigiert. Nicht die historisch dokumentierten Tests umetikettieren.
- **Status: NACHGEHOLT, Delta vom 15.10.2026.**

# EIGENTUMSSCHUTZ – KONZEPT – FEHLERQUELLEN

## HB-CONCEPT-001 – Ein-Kind-/Zwei-Kind-Klickebenen
Status: bestätigt in WordPress-R2-Konzept, **R3 nur strukturell gelöst; Live-Fix NICHT umgesetzt**.
Befund: 19 von 31 L2-Bereichen nur 1 L3, 10 nur 2; Nutzerregel 3–10 direkte Unterebenen. Nicht durch ein rein optisches Menü kaschieren.

## HB-CONCEPT-002 – SEO-Owner- und Artikel-Doppelungsrisiko
Status: **EDITORIAL-VORPRÜFUNG ERLEDIGT, SEO-SERP-FREIGABE OFFEN**. Für 144 R3-Kandidaten sind je drei konkrete Vorschläge (432) formuliert, exakt mit den 704 alten Titeln abgeglichen und 17 lexikalische Nähen fachlich vorsortiert. Die 21 früher offenen R2-Owner haben vorläufige redaktionelle Abgrenzungen; im aktuellen V8-Fachplan insgesamt 19 vorgeschlagene Themenumhängungen (keine Kopien), eine Keyword-Aliasregel. Trotz exakter Titeldeduplizierung sind semantisch getrennte Suchintents und organische SERP-Owner weiterhin nicht nachgewiesen. Autoritative Detailakten im KONZEPT-Büro: `R3_REDAKTION_144_KATEGORIEN_432_IDEEN_20261013.md` und `R3_BESTANDSOWNER_21_FACHPRUEFUNG_20261013.md`.

V5-Arbeitsfassung: `R3_V5_144_KATEGORIEN_432_IDEEN_EDITORIAL_FACHPLAN_20261013.md`. Trotz 14 redaktionellen Titelpräzisierungen und 0 exakten Wiederholungen **bleibt echte organische Suchintent-/Google-SERP-Überschneidung offen**. Quelle für verbindlichen Status und NEXT ACTION: `CURRENT_STATE.md`.


Aktuelle V6-Gegenprüfung vom 13.10.2026: 144 neue Kategorien mit 432 konkreten Artikeltiteln, 0 exakte Titelduplikate, 155 automatisch markierte lexikalische Paare (Schwelle 0,29), davon 3 ab Score 0,50. Koax-/Satellitenschutz war tatsächlich in Datenleitungen und Antennen doppelt vorgesehen, **in V6 auf nur Antennen-Owner korrigiert**. 14 konkrete fachliche Paargrenzen sowie alle 10 auffälligen neuen/bisherigen Kategoriebezeichnungs-Nähen wurden redaktionell eingeordnet. 19 Umhängungen: 9 Alt→Alt, 10 Alt→Neu, noch nicht ausgeführt. **V6 redaktionell verbessert, organische SEO-Kannibalisierungsfreiheit weiterhin NICHT NACHGEWIESEN.** Maßgeblich: `R3_V6_144_KATEGORIEN_432_IDEEN_OWNER_BEREINIGT_20261013.md`; nur `CURRENT_STATE.md` ist aktuelle Zustandsautorität.

## HB-CONCEPT-002a – Konkrete V7-Korrekturen wegen semantischer Wiederholung
Status: **IM V7-KONZEPT KORRIGIERT / SEO-SERP-FREIGABE NOCH OFFEN**.
- Neuen Blattkandidaten `Eiszapfen & Dachkanten` aufgrund der bestehenden Kategorie `Schnee & Eis am Grundstück` als zu nah erkannt und im Entwurf in `Glatteis an Garagenzufahrten` geändert; drei eigenständige Zufahrts-/Rampen-Artikelvorschläge.
- Fünf weitere Artikelintents eindeutiger abgegrenzt: Camper-Gasinstallation vs Gasprüfungen; Ladentrocknung vs allgemeines Verfahren; Wohnmobil-Löschmittel vs Fettbrand-Grundregel; Offline-Smart-Home-Automation vs bereits vorhandene Offline-Alarmtechnik (zwei Artikel).
- Alte 223 CORE-Objekte inklusive Elternzuordnung unverändert, alle 144 neuen Kandidaten weiterhin 3 Artikelentwürfe, Struktur 3–10 PASS, **keine Live-Umsetzung**.
- **WICHTIG:** redaktionelle Doppelungsvorsorge ist kein gemessener Google-SERP-/Keyword-Nachweis. Status/next action ausschließlich im `CURRENT_STATE.md`; Volltext in `R3_V7_144_KATEGORIEN_432_IDEEN_FACHPLAN_20261013.md`.

## HB-CONCEPT-002b – V8: reale Alt-Neu-Artikelüberschneidungen
Status: **REDAKTIONELLE PRÜFUNG FÜR DIESE FÄLLE ERLEDIGT / ORGANISCHE GOOGLE-SEO-FREIGABE UNERLEDIGT**.
- 432 neue konkrete Titelformulierungen gegen 704 R2-Originale mit **304.128** realen Textpaaren gegengeprüft, statt nur Kategorienamen. Fünf bisher zu allgemeine R3-Titel fachlich präzisiert (Camper-Feuerlöscher, Alarmquittierung, manuelles Markisen-Einfahren bei Sensorsignalfehler, Akku-Ladehalterung, Kunden-/Lieferfluchtwege).
- **17** verbliebene textähnliche Neu-Alt-Top-Paare bei Schwelle 0,48 sowie **zwei** textähnliche Neu-Neu-Paare einzeln im Konzeptbüro erörtert. Die **zwei besonders grenznahen fachlichen Owner** sind Heizungsalarm/Mobilfunkempfang ↔ Router-/Mobilfunk-Backup und Sumpfpumpen-Wartung ↔ USV-/Notstromwartung. Für alle bleibt echter organischer Google-SERP-Vergleich offen.
- Positiver Konzept-Regressionsstatus: 6/31/93/285, keine <3/>10-Zwischenstufen, 223/223 Original-Core-ID/Name/Eltern identisch, **704+432** Titel, keine exakt wiederholten Titel, **19 geplante** Umsortierungen nur als TRANSFER, nicht COPY, Quellkategorien jeweils >=3. **0 WP-Writes**.
- **Autoritativer Status:** `CURRENT_STATE.md` V8. **Vollständiger Plan:** `R3_V8_144_KATEGORIEN_432_IDEEN_FACHPLAN_20261013.md`. **Prüffälle:** `R3_V8_17_NEU_ALT_OWNER_PRUEFFELLE_20261013.md`. **Maschinen-QA:** `R3_V8_QA_20261013.json`. Die V7-Historie nicht zur Live- oder SEO-Freigabe heranziehen.

## HB-CONCEPT-002c – aktueller V8-Gesamtstatus
**STATUS: NICHT GELÖST FÜR GOOGLE-SEO-/WORDPRESS-RELEASE.** Der echte V8-Neu-vs-R2-Titelvergleich (432×704) führte zu fünf redaktionellen Titelkorrekturen; alle 17 deutlichsten Alt-Neu-Signale und zwei Neu-Neu-Signale wurden einzeln redaktionell eingeordnet. Zwei technische Überschneidungsfragen wurden mit Handbuch-/Fachquellen präzisiert. **Keine vollständige SERP-/Keyword-Freigabe** für 144 neue Kategorien.
Der aktuelle V8-Entwurf bestand eigene lokale **15/15 Negativtests**, nicht das unveränderte WordPress-Plugin. Quellen: `R3_V8_144_KATEGORIEN_432_IDEEN_FACHPLAN_20261013.md`, `R3_V8_QA_20261013.json`, `R3_V8_17_NEU_ALT_OWNER_PRUEFFELLE_20261013.md`, `R3_V8_2_TECHNISCHE_OWNER_GRENZEN_20261013.md`, `R3_V8_15_NEGATIVTESTS_20261013.json`. **Einzige Current-Autorität und NEXT ACTION: `CURRENT_STATE.md`.**

## HB-CONCEPT-003 – Beleggrenze für Live
Status: **OFFEN**. R3 weiterhin ausdrücklich nichtimportierbarer Konzeptentwurf, trotz Struktur- und Redaktionstiteltests. Keine neuen WordPress-Kategorien, keine neue veröffentlichte URL. R2 weiter maßgeblich für WordPress.

Sperre: Vor tatsächlichem Umbau erst vollständige fachliche Abnahme, Kollisionstest, Redirect-/URL-Prüfung und freigegebenes Zielprofil.

## HB-CONCEPT-004 – 3–10-Auswahlregel im Live-Validator fehlt noch
Status: **TECHNISCHE REGEL-LÜCKE BESTÄTIGT / NICHT MODIFIZIERT**. Prüfung der lokalen Original-ZIP `HAB_UND_BEWAHR_KATEGORIE_WORKFLOW_1.14.8.17_SERP_FORTSETZUNG_34V40.zip` vom 13.10.2026: `class-apkw-target-tree.php` validiert bereits das Minimum an Artikeltiteln je Blattkategorie und `min_categories_per_third_page` (3); `class-apkw-target-tree-dry-run.php` begrenzt `max_megamenu_children` auf 10 und fordert bei Welten bisher nur **mindestens 1** direktes Kind. **Ein allgemeiner harter Mindestwert 3 für jeden anklickbaren Zwischenknoten wird im geprüften Plugin noch nicht erzwungen.** Die R2-Struktur mit 19/10 Ein-/Zwei-Kind-Bereichen konnte daher gültig sein. Vor R3-Release muss die verbindliche 3–10-Strukturprüfung im bestehenden Validator nachvollziehbar ergänzt und mit Negativfällen getestet werden; keine Architekturänderung und kein vorgezogenes Pluginupdate nötig.


## HB-CONCEPT-006 – Organische Webbelege vor Fachbehauptung nicht belastbar geöffnet
Status: **QUELLENFEHLER KORRIGIERT; SEO-BLOCKER 002 WEITER OFFEN (13.10.2026)**.
- Zwei vormals angeführte DEHN-Unterseiten leiten auf die allgemeine Startseite und sind kein belastbarer, spezifischer Fachnachweis.
- Ein zuvor behaupteter Pumpen-USV-Beleg auf einer Merten-Seite ist für Pumpenanwendungen nicht bestätigt; diese Aussage wurde ausdrücklich zurückgezogen.
- Angeblicher neuer V8-Doppelartikel „Outdoor-Ethernet“ ist nach Lesen der drei tatsächlichen Außenkabel-V8-Titel **nicht vorhanden**. Allgemeine Keyword-/Leitungsüberschneidungen bleiben möglich und Google-SERP-UNBEKANNT.
- Einzelfall-Nachprüfung und 15 priorisierte, unterschiedlich starke Fachbelege im `R3_V8_PRIORITAET_15_QUELLENAUDIT_20261013.md`; beide vorherigen Stichproben am Dokumentanfang mit klaren Warnungen ergänzt.
- Gegenprobe: weiterhin 144/144 gelistete Kategorien, 432/432 V8-Ideen, keine SERP-/Suchvolumen-Freigabe; keine Änderungen am R2-WordPress oder Plugin.

## HB-CONCEPT-005 – Übergaberouting und Zielvertragsablage lückenhaft
Status: **LOCAL CLOSED – 2026-10-13; FRISCHE-READBACK BESTÄTIGT**.
- Fehler 1: Die Eigentumsschutz-Bürotür enthielt den veralteten Satz, eine Konzept-Current sei nicht unabhängig verifiziert. Das widersprach dem vorhandenen `AUTORITAETSPLAN.json` mit dem eindeutigen `EIGENTUMSSCHUTZ_KONZEPT`-Routing und der real existierenden `KONZEPT/CURRENT_STATE.md`.
- Fehler 2: Der `KONZEPT/HOBBYRAUM.md` referenzierte als Arbeitsbindungsquelle noch einen alten R3-Delta-Pfad, obwohl die Current inzwischen einen V8-Fachplan bindet.
- Fehler 3: Das zentrale Zielvertragsregister enthielt bisher keinen eigenen Hab-und-Bewahr-Kategorienzielvertrag, obwohl die neue 3–10-Nutzerentscheidung im Current bindend war.
- Korrektur: Tür auf die vorhandene Current geroutet, Hobbyraum auf ausschließlich aus Current abgeleitete Daten umgestellt, `ZIELVERTRAG_KATEGORIEN_3_BIS_10_20261013.md` angelegt und in `ZIELVERTRAEGE/REGISTER.md` registriert. WAS/WARUM im `AENDERUNGSREGISTER.md`, Türänderung im `BAUCONTAINER/BAUPROTOKOLL.md`.
- Testbedingung: Frischer Readback von Tür, Routing, Current, Hobbyraum und Zielvertrag; **genau eine Current und genau eine NEXT ACTION**. Keine WordPress-/Pluginänderung.


## NACHHOLPRÜFUNG 13.10.2026 – LIVE PREFLIGHT PASS, ÄLTERE FEHLERSTATUS GELTEN NUR HISTORISCH
Quelle und Statusautorität: `KONZEPT/CURRENT_STATE.md`, dortiger Abschnitt `LIVE-R3/V8-PREFLIGHT PASS – Nutzer-Rückmeldung 13.10.2026`. **Dies ist ausschließlich das Fehler-/Korrekturdokument, KEINE zweite Current-Quelle und KEINE eigene NEXT ACTION.**

- **HB-CONCEPT-001 (Ein-/Zwei-Kind-Zwischenebenen):** Frühere R2-Strukturschwäche im R3/V8-Zielbaum behoben; nach gemeldetem **echten WordPress-Preflight PASS** enthält das finale **geprüfte** Profil 6 Welten, 31 Bereiche, 93 Unterbereiche, 285 Kategorien und 1.136 Artikelideen. **Status: LOCAL CLOSED / LIVE PREFLIGHT PASS / LIVE-SYNC OFFEN.** Dies bedeutet noch nicht, dass der Baum WordPress-live geschrieben wurde.
- **HB-CONCEPT-002, 002a–c (SEO-/Owner-Dubletten):** Alle 19 vorgesehenen Artikelideen-Transfers sind vom echten WordPress-Preflight als **exakt einmal verschoben** geprüft, bestehende R2-Knoten, Live-IDs, Slugs und Eltern geprüft. **Status: REDAKTIONELLE SCOPE-GRENZEN VORLIEGEND / ORGANISCHE SEO-GESAMTMESSUNG OPTIONAL, NICHT BLOCKIEREND.** Explizite Nutzerentscheidung: fachlich sinnvolle Kategorien brauchen keine Google-Treffer, kein gemessenes Suchvolumen und keine 144/144-SERP-Prüfung. Historische Formulierungen `SEO-BLOCKER` und `SERP-Pflicht vor R3-Import` sind **überholt und NICHT als aktive Release-Sperre zu verwenden**.
- **HB-CONCEPT-003 (R3 nicht live bereitgestellt):** Nach gemeldetem WordPress-Preflight **PASS**, aber Meldung sagt ausdrücklich **0 WordPress-Daten geschrieben**. Das geprüfte R3-Profil wurde noch nicht als bereitgestellt bestätigt; Live-Sync/Readback noch offen. **Status: LIVE OFFEN**, keine zusätzliche SEO-Sperre.
- **HB-CONCEPT-004 (3–10-Validator in altem Plugin fehlte):** Ursprüngliche Quellbeobachtung bezog sich auf Plugin `1.14.8.17`; neuere gebaute Hab-&-Bewahr-Version `1.14.8.19` hat nach lokalem Arbeitsnachweis 28/28 Sicherheits-/Negativtests bestanden; WordPress-Preflight wurde vom Nutzer mit Struktur-PASS gemeldet. **Status: HISTORISCHER CODEFEHLER / LOKAL CLOSED / LIVE PREFLIGHT PASS.** Installierte Live-Versionsnummer und schreibender WordPress-Sync sind durch die PASS-Nachricht allein **nicht** unabhängig nachgewiesen.
- **URL-/Live-Schutz:** Die PASS-Rückmeldung bestätigt Prüfen der bestehenden IDs, Slugs, Eltern und R2-Knoten. **Noch nicht nachgewiesen**: schreibende Live-Umsetzung, vollständiger Post-Sync-Readback, Redirect-Verhalten im Frontend und ein möglicher Live-Rollback. **Status: LIVE OFFEN**, nicht mit bereits bestandenem Preflight verwechseln.

**Befundgrenze:** Das PASS-Zitat stammt aus der WordPress-Oberfläche, vom Nutzer in den Chat übertragen. Es ist echte Nutzer-Rückmeldung über einen durchgelaufenen Preflight, jedoch kein hier separat per WordPress-API erhobener Post-Sync-Datensatz. Fehlende spätere Stufen nicht als FAIL raten.
