# Hab & Bewahr – 20.11.2026 – Version 0.4.31.14: breite Recherche, weniger enge Portaleignung, drei Wiederfreigaben

## Ausgangslage und Befund
Die DataForSEO-Recherche mit 4 Originalwegen ist auf Hab breit gewünscht; beim dritten Echtlauf `Alarm & Kamera ohne Netz: Häufige Fragen` lieferte sie 100 Roh-Keywords. Die ursprüngliche sehr enge Prüfung verwarf 99 von 99 Aliasgruppen als nicht zur Ausgangsfamilie gehörend; 98 gespeicherte Kandidaten, 0 direkt nutzbar. Zwei frühere abgeschlossene Sandbox-Recherchen (Abholbox; Abluftanlagen) enthielten je 9 unbrauchbare Rohwörter. Alle drei Familien gelten dadurch als abgeschlossen.

Die frühere manuelle Offline-Simulation mit allen 118 Wörtern ergab 5 potenziell themennahe + 29 potenziell andere Sicherheits-Kandidaten + 17 unklar + 49 sachfremd beim Kamera-Lauf. Das war ein redaktionelles Urteil und **kein automatischer Produktionsnachweis**.

## Gebündelter KISS-Fix 0.4.31.14
1. **Breite Suche unverändert.** Original-Research-Job, Runner, Queue, DataForSEO-Client, 4 Methoden, Kosten, Cache, MINI, K0, Import und Artikelregeln byteidentisch zu 0.4.31.13.
2. **Nur ein Portal-Entscheidungsort:** Die bisherige `PSTE_Category_Context::portalContextEvidence`-Quelle der ursprünglichen `PSTE_Portal_Relevance_Gate` darf zusätzlich zwei unterschiedliche bedeutungstragende Wörter aus **ein und derselben aktuell vorhandenen Hab-WordPress-Themenfamilie** als Portal-Kontextbeleg verwenden. Ein einzelnes „Kamera“ oder redaktionelle Wörter zählen nicht. Kein automatisches Setzen einer Zielkategorie oder Artikel-PASS; unklare Wörter verbleiben in Review. Für Pferdeatelier/Hobbydepot greift diese Erweiterung nicht. Das Kategorie-Wortregister wird bei gleichem Struktursnapshot pro Request nur einmal aufgebaut. Keine nachgelagerte zweite Prüfung.
3. **Drei statt zwei alte Nullergebnisse gezielt wieder öffnen:** Neue einmalige, ausdrücklich vom Administrator auszulösende kostenlose Aktion. Genau zwei nachgewiesene Sandbox-0er und ein nachgewiesener Produktions-0er; strenge Identitäts-, Lauf-, Ergebnis- und Kostenprüfungen. Keine alten Belege gelöscht, keine automatische Anbieteranfrage, kein Zurücksetzen weiterer Kategorien. Ein bereits gesetzter v0.4.31.13-Zwei-Läufe-Beleg bleibt kompatibel.

## Tests am endgültigen ZIP
- ZIP SHA256 `6406d4b24124d04d5cef212a8383d12a1b1712b51b734bed287a8754676f56c2`; 87/87 ZIP-Inhalte CRC gültig; 78/78 PHP-Dateien syntaktisch gültig.
- 134/134 Original-PHP-Regressionen.
- 30/30 Echtdaten-Modusprüfungen.
- 38/38 alte Reset-Tests.
- 46/46 neue Drei-Reset- und Negativtests inklusive alter Reset-Kompatibilität und neuer erfolgreicher Originalrecherche.
- Original-PHP-Portal-Gate direkt an 118 gespeicherten Raw-Keywords mit **12 ausdrücklich synthetischen** Kategoriebeispielen geprüft: 11 starke Portalbelege, 40 weiter offen/unklar, 67 sachfremd nicht freigegeben, 0 Falschfreigaben gegen die manuelle Klassifikation. Diese 12 Kategorien sind **kein** Live-WordPress-Kategorieexport. Nicht behaupten, dass automatisch 34 Keywords den Produktions-PASS bestehen.
- 83/87 Plugin-Dateien bytegleich zu 0.4.31.13; Änderungen nur `class-pste-category-context.php`, `class-pste-repository.php`, `texterstellung.php`, README. Keine neue kostenpflichtige Anfrage in Tests.

## Ablage
Finales ZIP `Texterstellung_HAB_UND_BEWAHR_0.4.31.14_BREITE_SUCHE_KISS_DREI_RESET.zip` unter `/hab-und-bewahr/TEXTERSTELLUNG/PLUGIN_FREIGABEKANDIDATEN/`, ausführlicher Bericht, QA, Originaldiff und Testquellen unter `/hab-und-bewahr/TEXTERSTELLUNG/PRUEFUNG_BREITE_KISS_DREI_RESET_20261120/`.

## Konkreter Betreiber-Nächster-Schritt
Altes Texterstellungs-Plugin in WordPress **ersetzen, nicht deinstallieren** (vorher WP-Backup). `Texterstellung → Recherche → Drei Fehlrecherchen wieder öffnen – kostenlos` **einmal** klicken. Danach ohne neue Recherche Diagnose-JSON ausgeben und prüfen: erwarteter Zähler **2128 offen statt 2125**, sofern nicht zwischenzeitlich weitere Läufe stattfanden. Erst nach Prüfung der echten Kategoriebelege eine gesondert kostenbestätigte Recherche als Live-Test erwägen. **Keine Live-Produktionsabnahme behauptet.**
