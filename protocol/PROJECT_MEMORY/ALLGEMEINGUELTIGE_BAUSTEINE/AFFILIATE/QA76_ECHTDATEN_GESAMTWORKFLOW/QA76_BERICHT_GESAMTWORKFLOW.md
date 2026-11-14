# QA76 – eBay Gesamtworkflow: originaler Lauf, 283 Familien, 153 Fehler, vorhandener PHP-Code

Stand: 14. November 2026. **Originaldatenbeweis + kompletter PHP-Workflow unter nachgestellten WordPress/eBay-Diensten. Keine historische Provider-1:1-Simulation und keine Live-Abnahme.**

## Bindender Vertrag

`ZIELVERTRAG_QA69.md`: ein vorhandener GitHub-Zeitgeber, eine kanonische gespeicherte eBay-Run-ID, ein fachlicher Auswahlbesitzer, reine gezielte Frischeprüfung, ein veröffentlichter SAFE-Checkpoint, einmalige anschließende Bereinigung, 283 beweisbare Familienresultate. Keine neue Engine, Tabelle, Cron oder zweite Auswahlentscheidung.

## Echte Eingaben – exakt nachgerechnet

Originalprotokoll `pferdeatelier-ebay-lauf-574cb003b132.csv`: **2.769 / 2.769** echte Ereignisse, alle dieselbe ID `97507628-4f4d-4527-bd77-fa573bce7067`. Originaler Endzustand `running / gapfill_discovery`, Fortschritt **474**, Arbeitstakte **468**, Abdeckung **5 / 283**. Originaldatei `Pferdeatelier_eBay_fehlende_Produktfamilien_97507628-4f4.csv`: **278** namentlich benannte offene Familien. Der mitgelieferte originale eBay-Katalog liefert exakt **283** konkrete Waren-Familien-IDs (324 Pflicht-Konzepte minus 41 ausdrücklich ausgeschlossene Nichtwaren). Die genaue Übereinstimmung ist geprüft.

Alle 283 **historischen** Familienpositionen sind in `QA76_ORIGINAL_283_FAMILIEN_UND_95_FEHLARTIKEL.json` dokumentiert:

| Ergebnis im echten letzten Export | Familien |
|---|---:|
| Laut ursprünglichem Lauf abgedeckt (IDs als Komplement der 278 Fehlfamilien ermittelt) | 5 |
| Gesucht und zulässige Angebote gefunden, aber nicht veröffentlicht | 32 |
| Gesucht, aber keine angenommenen Angebote | 31 |
| Noch kein eigenständiger Einzelabruf in diesem Teilstand | 215 |
| **Summe** | **283** |

Die fünf aus der genauen Originalmengendifferenz abgeleiteten Familien-IDs sind **Anbindestricke, Fieberthermometer Pferd, Heutaschen, Mineralfutter für Pferde, Satteldecken**. Aus dieser Zählung allein lässt sich nicht schließen, dass ihre Produkte gegenwärtig öffentlich angezeigt werden. Für die 32 nicht abgedeckten, aber angenommenen Familien enthält das echte Protokoll **201 angenommene Angebote** aus **120 Suchanfragen** über alle 63 im Teilstand abgefragten Fehlfamilien. Diese Angebote sind **nicht** als bereits öffentlich freigegeben zu behandeln.

**Der tatsächliche Materialisierungsfehler:** 153 Kandidaten wurden bei der Übernahme übersprungen. Die vier protokollierten Erhöhungen betragen 48 + 50 + 50 + 5. Für **95 unterschiedliche echte eBay-Artikel-IDs** enthält das begrenzte Protokoll den Code `business_selected_stale_during_apply` (abgelaufener Quellnachweis). Für 58 zusätzliche übersprungene Artikel ist **keine eigenständige Einzel-ID/Fehlerantwort** vorhanden. Diese 58 dürfen nicht nachträglich erfunden werden.

**Zeit:** Vier große belegte Zeitlücken im Originalprotokoll ergeben **21.324 Sekunden (5 h 55 min 24 s)**. Im echten GitHub-Job 132207303870 (Run 43518738389 vom 13.11.) sind fünf **45-Sekunden-HTTP-Timeouts** belegbar. Im Main-Job 132501390005 (14.11., 15:56 UTC, Run 43612828861) endete der alte GitHub-Runner nach einer `idle`-Antwort bereits beim ersten Aufruf als `success`; der WordPress-`run_status` ist im originalen GitHub-Log nicht enthalten. Ein älterer eigener Beleg vom 11.11. (QA24) verbindet jedoch eindeutig `idle/availability_tick` mit einem **zu diesem Zeitpunkt aktiven Lauf**. Github `success` bedeutet hier keine bestandene eBay-Produktabnahme.

## Vollständiger vorhandener Code – ein gebündeltes Plugin auf Testbasis

Einziges **Testinstallations-Paket**, Paketversion `6.72.351`, auf der unveränderten Original-ZIP 6.72.350 aufgebaut; QA72–QA75-Korrekturen zusammen übernommen. Gegenüber dem Original unterscheiden sich **genau fünf der 66 Dateien**: die beiden vorhandenen eBay-PHP-Dateien sowie der Pluginversionskopf, die bestehende Versionswechsel-Ausnahme und die Readme. **61/66** unverändert. Keine neue eBay-Entscheidungsstelle, keine neue Datenhaltung, kein Frontend-Umbau.

Die vorhandene WordPress-REST-Routine `handle_ebay_external_tick` wurde im ORIGINALEN PHP mit der echten Run-ID und dem echten letzten Stand (Phase `gapfill_discovery`, Schritt 474) in **16** Status-/Stop-/Weiterlauf-Fällen geprüft. Bei aktivem gespeichertem Lauf wird eine intern fälschlich als `idle` gemeldete Arbeit zu `busy` (der vorhandene Live-Main-Runner kann weiterlaufen); ausdrücklich manueller Stopp bleibt `idle`, ein gespeicherter Fehler bleibt `failed`, inkonsistente Zustände werden **nicht** neu gestartet. Damit ist die notwendige Statusverträglichkeit zum **bereits vorhandenen** Main-Zeitgeber im PHP-Code nachgewiesen, ohne eine gesperrte GitHub-Datei zu verändern. Es ist noch **nicht** nachgewiesen, dass die 45s-HTTP-Timeouts auf dem echten Server verschwinden.

Mit den **95 echten Artikelkennungen und ihren echten zugehörigen Familienkennungen** wurde die bestehende PHP-Übernahmemethode ausgeführt. Die fehlenden WordPress-Quellzeilen und echten eBay-`getItem`-Antworten sind dabei **ausdrücklich nachgestellt**. Testbeweis: **95 gezielte Refresh-Aufrufe auf 95 Arbeitstakte**, alle 95 in diesem Modell erfolgreich übernommen. Bei geänderter, beendeter, unterbrochener oder nicht speicherbarer Quelle gilt weiterhin Sperre oder begrenzter Retry: neun weitere Original-PHP-Fehlerfälle bestanden. Das ist **keine Aussage**, dass die 95 Artikel im November tatsächlich verfügbar waren.

Die bestehenden **neun vollständigen** Original-PHP-Controller-Szenarien mit simulierten Servicezuständen sind erneut an den **tatsächlich verpackten beiden PHP-Dateien** ausgeführt. In fünf erfolgreichen Modellketten sind 283 Familien intern bilanziert, einschließlich Negativgründen, und derselbe sicher freigegebene Bestand wird für die Schlussbereinigung verwendet. Das Ergebnis ist ausdrücklich ein **Modell** und die 259 simuliert abgedeckten Familien im Normalfall sind **nicht** die realen historischen fünf. Der gesamte alte QA75-Basistest (5.627 + 5.686 lokale Assertions) ist erneut durchgelaufen. Daneben wurden **11.187 Zeilen-/Zähler-Prüfungen** über die echten CSVs und 127 zusätzliche Integritäts-/Paketprüfungen durchgeführt. Keine dieser Zahlen ist eine Anzahl echter unabhängiger Produkttests.

Plugin-Datei: `Affiliate_6.72.351_EBAY_KISS_GESAMTWORKFLOW_TESTINSTALLATION.zip`, SHA256 `65e6bff15af26ec559ccbb40333ec7168cc5f4a22eb7a77f682f07e5bb47e247`. **23 PHP-Dateien syntaktisch gültig, 66 ZIP-Einträge geprüft.** Es handelt sich um eine **Testinstallation**, nicht um ein abgenommenes Live-Release.

## Exakte Grenze – was mit diesen Originaldaten noch nicht geht

Die beiden aktuellen Original-CSV liefern die realen **Laufereignisse, Produktfamilien, Fehlerkennungen und 95 Artikelkennungen**, aber **keine vollständigen ursprünglichen eBay-`getItem`-Antworten oder dazugehörigen tatsächlichen WordPress-Quellzeilen/öffentlichen IDs zum gleichen Zeitpunkt**. Der WordPress-XML-Export vom 09.11. liegt zeitlich **vor** diesem Lauf und ist keine 1:1-Momentaufnahme der späteren 13./14.11.-Ergebnisse; er ist in dieser Umgebung zudem nicht als Originaldatei kopierbar. Daher kann man die gesamten 153 Produkte nicht auf reale Verfügbarkeit und alle 283 Familien nicht auf reale öffentliche Produktanzeigen vorab **historisch 1:1** durchrechnen. Ausgedachte API-Antworten sind keine Originaldaten.

**Gesamt-Abnahme = NICHT BESTANDEN.** Noch nicht nachgewiesen: tatsächliche Installation des einen konsolidierten Pluginstandes in WordPress; Lauf derselben UUID bis zum echten 283er Endprotokoll, öffentlicher SAFE-Endcheckpoint und verifizierte öffentliche Produktanzeige; echte 45s-Timeout-Freiheit. Der GitHub-Wecker-PR #759 ist unverändert durch den Hardlock geschützt; dessen Freigabe ist ein eigenes autorisiertes Verfahren. Der derzeit vorhandene Main-Wecker lässt sich mit dem aktualisierten PHP-Statusweg grundsätzlich ansteuern, aber dies ersetzt keine Live-Messung.

Der nächste notwendige Test ist **einmal** mit diesem einen Paket auf der bestehenden isolierten WordPress-Testumgebung und ihren echten eBay-Verbindungen/Quelltabellen, anschließend geprüftes vollständiges Endprotokoll. Kein weiterer selbstständiger Prüfarbeitsgang, keine zusätzliche Tabelle, kein zweites Plugin und kein erneuter 150-MB-Export zur Fehlersuche.