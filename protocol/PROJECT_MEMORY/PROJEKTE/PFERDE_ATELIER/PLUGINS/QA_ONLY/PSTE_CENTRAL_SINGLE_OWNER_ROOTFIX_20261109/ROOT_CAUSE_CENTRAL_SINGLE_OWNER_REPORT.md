# Pferdeatelier — kritische Zentralisierungs- und Ursachenprüfung

**Stand:** 09.11.2026, ausschließlich lokale isolierte TESTKOPIE. **Keine installierbare Pluginfreigabe.** Original PSTE 0.57.144.28 und PSERC 0.28.55 nicht verändert, GitHub-K0 unverändert.

## Entscheidung: zentrale Planung ja, alle physischen Speicher in eine Tabelle zwingen nein

Ein **einziger verbindlicher Redaktionsplan und eine einzige fachliche Entscheidung je Thema** sind sinnvoll. Bei dieser WordPress-Installation ist aber die Gleichsetzung von „ein Plan“ mit „alle technischen Daten in genau einer Datenbankzeile“ nachweislich gefährlich:

| Fachliche Wahrheit | Originalspeicher und Verantwortung | Warum nicht einfach löschen/zusammenkopieren? |
|---|---|---|
| Tatsächlich existierende Beiträge und Kategorien | **WordPress** | Können außerhalb von PSTE verändert/gelöscht werden. Ein grünes Häkchen im Redaktionsplan beweist nicht ihre Existenz. |
| Einmaliges externes SEO-Urteil und freigegebener Titel | **MINI**: `pste_mini_keyword_roundtrip_v1` | 87 dokumentierte Entscheidungen, davon 61 FREI. Eine erneute Entscheidung bei Pluginupgrade wäre falsch. |
| Verbindlicher Produktionsplan, Fachübergabe | **PSERC**: `pserc_plan_active_snapshot_v1` als veröffentlichter, geprüfter Compilerstand | Ein fertiger Compilerstand ist ein signierter Übergabebeleg, **kein zweiter frei veränderbarer Redaktionsplan**. |
| Tatsächlich belegte/reservierte Produktionsplätze | **PPM**: `ppm679_editorial_plan_runtime_state_v1`, plus WP-Beitragsverknüpfungen | Dies sind tatsächliche Platzbelegungen; PSERC liest sie nur, um keine zweiten Plätze zu vergeben. **PPM-Quellplugin liegt hier nicht vor.** |
| Temporäre Arbeitsstände und Wiederanlauf | Kontextindex, Plan-Prüfsummen, einmalige Warteschlange | Ausfälle, parallele Anfragen und technische Prüfwerte benötigen Wiederanlauf/Nachweis. Sie dürfen **nie selbst fachliche Entscheidungen treffen**. |

**Reale Befundlage:** PSTE liest auf der WordPress-Testseite eine einzige aktive importierte Planquelle (`OPTION`) mit neun inhaltslosen alten `Array`-Einträgen. Der aktuelle fachliche Plan ist dadurch `NOT_AVAILABLE`, während gespeicherte technische Baseline und Index noch alte Prüfsummen besitzen. Im zuletzt exportierten 61er-Bericht sind **60 technische Plan-Hash-Abbrüche und 1 echte manuelle Sperre**. Der installierte `.28`-Bericht beweist weder, dass der gesonderte Rebind-Knopf geklickt wurde, noch einen neuen erfolgreichen Reentry.

## Nachgewiesene Ursachen — nicht nur Symptome

1. **Verdeckte Speicherung durch Leser:** `PSTE_Context_Index_Store::runtimeBinding()` konnte einen beschädigten oder abweichenden technischen Index stillschweigend **neu speichern**. In der QA-Kopie ist Lesen strikt lesend; bei Abweichung stoppt es. Die vorhandenen ausdrücklich gestarteten MINI- und Produktionsworker rufen jetzt *dieselbe* Index-Schreibmethode kontrolliert auf. Kein zusätzlicher Entscheider, keine neue Tabelle.
2. **Doppelter Fortschrittsstand:** Eine flüchtige Fortschrittsmeldung (`pste_title_desk_reentry_report`) konnte der dauerhaft gespeicherten 61er-Warteschlange widersprechen. Die QA-Kopie leitet die Fortschrittsanzeige ausschließlich aus der Warteschlange ab; neue Läufe schreiben keinen zweiten Bericht. **Nur für alte Aufträge ohne gespeicherte Einzelergebnisse** bleibt der frühere Bericht als lesbarer Übergangsbeleg erhalten.
3. **Versionsnummer statt Fachentscheidung:** `forwardToPlan()` startete bei einer neuen PSTE-Version unveränderte genehmigte Themen erneut. Selbst `singleOwnerSeoFor()` verlangte bei einer bestehenden Freigabe einen Transportstempel mit *genau der gerade installierten Pluginversion*. Beide Wege und der gezielte Rebind-Vorprüfer wurden an **denselben unveränderten Suchanfrage-/Titelfingerabdruck** gebunden. Damit kein zweites SEO-Urteil nach Update.
4. **Falsche Kategorie bei doppelt sichtbarem Namen:** 45 gleiche sichtbare Namen für je zwei der 1.165 gültigen Kategorien. Die Original-Namenssuche nahm den letzten gleichnamigen Treffer (z. B. `FAQ Sicherheitshalfter`: 942 statt möglicherweise 55). Die QA-Kopie verlangt eindeutige ID/Slug oder exakt einen Namenstreffer; sonst fachlicher Halt. **Fünf exakt doppelte Gesamtpfade** bleiben unangetastet, da mindestens zwei konkrete Kategorien bereits Artikel enthalten.
5. **Technischer Fehler als „fertig“:** Fehlender/abweichender Kontextindex oder Planquelle führt in der QA-Warteschlange zu `PAUSED_CONTEXT_STALE` mit erhaltenen offenen Schlüsseln; nicht zu „61 erledigt“. Das historische `.28`-Ergebnis wird **nicht rückwirkend umetikettiert**.

## Kritisch geprüfte weitere Mehrfachablagen

Statischer Scan von PSTE und PSERC: **89 identifizierbare Speicher-/Optionsreferenzen**; bei **10 Speicherkennungen** schreiben mehrere Komponenten (z. B. Baseline-Schreibung in Snapshot und Runner, Queue/Reset, GSC-Einstellungen, Forschungssperren). **Eine zweite Schreibdatei ist kein Beweis für einen zweiten Entscheider**: ein Cleanup/Reset ist oft bewusst getrennt. Diese 10 Fälle sind im beigefügten `STORE_REFERENCE_AUDIT.json` mit Dateinamen dokumentiert. Es fehlt ein echter WP/SQL-Lauf und der PPM-/K0-Quellcode, um diese Pfade vollständig zu beweisen und ohne Datenverlust physisch zu entfernen. Daher **keine Löschung auf Verdacht**.

Der `pste_context_stage_plan_v1` und das alte Bundle werden durch bestehende Cleanup-Methoden bereits entfernt. Die neun alten Planplatzhalter sind **keine belegten Artikelplätze**, aber auch die importierte Optionsquelle wurde in der QA-Kopie **nicht gelöscht**, solange ihre externen Referenzen nicht durch einen echten WordPress-Speicherbeleg abgesichert sind.

## Positiv- und Negativtests am echten PHP-Code mit echten Exportdaten

| Ausgeführter Test | Ergebnis und Grenze |
|---|---|
| `.28`-Quelle / WordPress-Export, Plan-Rebase, 9 Placeholder, 61er Warteschlange | **51/51** Daten-/Quellenprüfungen; **12/12** Worker-/Wiederanlaufprüfungen mit simulierter WP-Optionsspeicherung |
| Kategorieidentität: 1.165 gültige Kategorien, 45 Namens-Doppelungen | **1.304/1.304** Original-PHP positiv/negativ |
| 61er Queue: 61 offen, Teilverarbeitung, 60 PASS + 1 manuelle Sperre, defekter Index, doppelte Einträge, Legacy | **22/22** am tatsächlichen Warteschlangen-PHP, WP/DB nachgebildet |
| Leserindex: gültiger/fehlender/beschädigter Manifeststand ohne Nebenwirkungen | **9/9**; für positiven Leserfall wurde eine formal signierte *synthetische* Prüfdatei verwendet |
| Versionsfreier Transport und beschädigte Stempel | **188/188** Checkpoint-Proben mit 61 echten Schlüsseln |
| **Tatsächlicher** Titel-Nachweisleser `singleOwnerSeoFor()` nach Versionswechsel | **246/246**: 61 × alter/neuer/gefälschter/geänderter Beleg, plus Schutz/Kein-Schreiben; MINI-WP-Option ist aus echten Exporten **nachgebildet** |
| **Tatsächlicher** Produktionsvorprüfer `productionAutomationBaselinePreflight()` | **16/16**: unverändert, Planwechsel, Strukturwechsel, unvollständiger Kontext, defekter Leseweg, Workerfehler |
| PSERC aktive Compilerdatei, PPM-Reservierungen, kein Doppelplatz und negatives Platzangebot | **13/13** am tatsächlichen PSERC-PHP, **künstliche** signierte Plan-/PPM-Testdaten |
| PHP-Dateien der PSTE-Testkopie | **83/83 Syntax PASS**, genau **5 PHP-Quelldateien geändert** gegenüber `.28`, alle übrigen Originaldateien unverändert |

**Zentraler Abnahmestatus:** `FULL_WORKFLOW_PASSED = false`. Alle oben genannten Tests sind lokal mit Original-PHP und echten exportierten Daten bzw. explizit gekennzeichneten Speicher-/Quellattrappen. **Ein kompletter positiver WordPress/MySQL → PSTE → PSERC → PPM → K0-Lauf unter realen Berechtigungen, Race-Conditions, Transaktionen, Modulversionen und ohne Artikelveröffentlichung wurde nicht durchgeführt.** Daraus darf kein neues installierbares Plugin freigegeben werden. Insbesondere beweisen diese Tests **keine** fachliche Freigabe der 61 Themen oder eine erfolgreiche Live-Reparatur der alten .28-Daten.

## Minimale Umsetzung ohne Überbau

- Nur die **fünf genannten bestehenden PSTE-Quelldateien** wurden in einer **separaten nicht installierbaren QA-Kopie** verändert. Kein zweiter Worker, keine zweite Datenbanktabelle, keine neue zentrale Datenkopie und kein Produktionsmerkmal.
- **Fachentscheidungen bleiben einmalig** beim jeweiligen Owner; die einheitliche Planansicht soll nur Daten *lesen*, nicht einen zweiten „Plan“ schreiben. Technische Prüfsummen dürfen einen veralteten Stand **stoppen**, aber nie eine alternative fachliche Wahrheit darstellen.
- Die bestehenden signierten PSERC-Snapshots, WP-Inventar, tatsächliche PPM-Reservierungen und Nachweise für abgebrochene Arbeit **behalten**; Dubletten im Fortschrittsstatus und Versions-Recheck **nicht mehr schreiben**. Alte Einträge nicht pauschal löschen.
- Vor Freigabe erforderlich: echter, vollständig protokollierter Endtest im **isolierten WordPress-TEST** mit vollständigen PSTE-/PSERC-/PPM-/K0-Versionen und Datenbankkopie, sowohl erfolgreicher als auch fehlerhafter Ablauf; Schutz der 144 reservierten Plätze, der 61 Freigaben und der manuellen Sperre. **Ohne diesen Nachweis keine Plugininstallation.**

**Nachweisarchiv:** enthält echte WordPress-Exporte, originalen Referenzcode PSTE + PSERC, isolierten PSTE-QA-Code, Diff-Patch, alle selbst ausführbaren Tests, maschinenlesbare Einzelresultate, Speicheranalyse und Prüfsummen. Keine Produktionsverbindung und keine Schreibrechte.