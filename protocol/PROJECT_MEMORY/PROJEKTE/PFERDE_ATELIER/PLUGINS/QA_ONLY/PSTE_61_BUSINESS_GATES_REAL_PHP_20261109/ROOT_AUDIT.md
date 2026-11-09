# Pferdeatelier – der nächste echte Engpass der 61 Themen

**09.11.2026 – Nur Prüfung. Keine Plugininstallation, kein K0-Eingriff.**

## 1. Stand

Der zuletzt tatsächlich aus WordPress exportierte Bericht der PSTE-Version **0.57.144.28** ist gegenüber dem alten Bericht inhaltlich **nicht weitergekommen**: `COMPLETE`, 61 von 61 gezählt, **61 zurückgestellt**, 0 offen, 0 nachweislich übergeben. Die Meldung `COMPLETE` ist daher kein Abschluss der gesamten Artikelplanung.

Die alte Planabweichung steht weiterhin bei 60 der 61 Einträge. Ein Eintrag bleibt ausdrücklich manuell gesperrt. **Das Exportformat zeigt nicht, ob die gesonderte Rebind-Aktion in WordPress tatsächlich lief.**

## 2. Warum der Planfix allein nicht reicht

Die **anderen, im selben realen Stapelbericht dokumentierten Fachprüfungen** zeigen:

| Noch bestehender Weg | Anzahl | Schlussfolgerung |
|---|---:|---|
| Themen im Kategorie-Büro, noch ohne Fachzuordnung | **52** | Kategorie-Worker muss eindeutig vorhandene Kategorie verwenden oder eine fehlende Kategorie nach seinen verbindlichen Regeln klären; niemals blind einen Artikelplatz vergeben. |
| Normalweg, aber Abgrenzung gegen bestehende Artikel offen | **7** | Einmalige Dubletten-/Suchabsichtsentscheidung erforderlich. Kein Doppelartikel. |
| Normalweg, reine Verkaufssuche | **1** | Nicht als redaktionellen Artikel durchdrücken. |
| Manuell gesperrt | **1** | Sperre beibehalten; keine automatische Freigabe. |
| **Summe** | **61** | **Keiner** ist in diesem Bericht als neue erfolgreiche Produktionsübergabe belegt. |

### Kritische Gegenprobe am originalen Plugin

Der originale PSTE-Magazin-Klassifizierer wurde mit **allen 61 tatsächlichen Suchanfragen** ausgeführt: **61/61** ergeben `NOT_APPLICABLE` (60 kurze Suchbegriffe ohne ausdrückliche redaktionelle Frage, ein syntaktisch nicht zulässiger Fall). Dagegen erkennt derselbe Originalcode **3/3 absichtlich klare redaktionelle Fragen** korrekt.

Gleichzeitig konnten **9/9 Magazin-Zielkategorien** anhand der echten WordPress-Slugs über die ursprüngliche Pluginfunktion eindeutig aufgelöst werden. Die Magazin-Kategorien **existieren also**. Sie sind nur absichtlich von der produktbezogenen Kategorie-Bestandsaufnahme getrennt; der Magazin-Worker sucht sie separat. Eine fehlende Magazin-Tabelle ist **nicht** als allgemeine Ursache bewiesen.

**Wichtig:** Die Journalprobe mit kurzen Suchbegriffen beweist, dass diese automatische Auswahl **für genau diesen 61er-Satz** nicht greift, nicht dass jeder dieser Begriffe in das Magazin gehört. Ein blindes Umschalten auf Magazin wäre fachlich falsch und würde neue Doppelentscheidungen schaffen.

**Negativprüfungen am Originalcode:** Fehlende Magazin-Kategorie `NOT_FOUND`; zwei mögliche Magazin-Kategorien `AMBIGUOUS`. Beide werden wie vorgesehen geblockt. Die gültigen 9 Kategorien funktionieren. 61 Pool-IDs sind eindeutig.

## 3. Zentrale KISS-Lösung und benötigter Endnachweis

- Einziger produktiver Plan-Eigentümer, **keine parallele Fachersatzliste**. WordPress-Beiträge und PPM-Reservierungen bleiben als *tatsächliche Bestände* erhalten.
- Die technisch veraltete Planbindung nur durch den ausdrücklich zuständigen Worker neu aufbauen – nicht beim Lesen.
- Die **52 Kategorie-Fälle** müssen durch den **einen Kategorie-Owner** in bestehende Kategorien oder in einen begründeten Strukturauftrag aufgelöst werden. Die vorhandenen Magazinkategorien als gleichwertige mögliche Ziele berücksichtigen, ohne alle 52 zwangsweise dorthin zu schieben.
- Die **7 Dubletten-/Suchabsichts-Fälle** sollen denselben bereits zuständigen Prüfer durchlaufen; **1 Kaufanfrage** und **1 manuelle Sperre** erhalten eigene korrekte Endzustände.
- Der Gesamttest besteht erst, wenn die tatsächliche Übergabe – nicht nur der Transport – für die fachlich wirklich freigebbaren Themen belegt ist, Fehlfälle abgesichert bleiben, PPM keine Plätze doppelt vergibt und K0 die geprüften Produktionsaufträge **ausschließlich auf einer isolierten Testumgebung** annimmt.

## 4. Harte Prüfgrenze

Das zuletzt vorliegende Beweispaket besitzt keinen **aktiven PPM679-Pluginquellstand** und kein vollständiges **aktives** K0. In GitHub liegen K0-Quellen ausschließlich in einem separaten Quarantänebestand; sie dürfen nicht als aktive Produktion ausgeführt werden. Aktuelles WordPress/MySQL ist im Testcontainer nicht verfügbar. Weitere GitHub-Prüfbranches zeigen historische PPM-/K0-Tests, ersetzen jedoch keinen Versionsbeleg der aktiven Produktion.

**Deshalb:** `FULL_WORKFLOW_PASSED=false`. Es wurde **kein** Plugin ausgegeben und **kein** Produktionssystem verändert. Der hier ausgeführte neue Test ist ein **echter Original-PHP-/Original-Export-Nachweis** für einen bislang verdeckten weiteren Gate-Blocker, **nicht** der vollständige WordPress/PPM/K0-Endtest.

## 5. Reproduzierbarer Beleg

`php pruefe_61_original_php.php` führt die tatsächliche PSTE-Originalklassifizierung und Originalkategorieauflösung gegen die vollständigen WordPress-Exporte aus und erzeugt `PRUEFRESULTATE_61.json`. Die mitgelieferten Original-Quelldateien sind unverändert. Der Test braucht nur PHP, keine Website und keine Schreibrechte. Alle Eingaben und den Testcode enthält das ZIP.