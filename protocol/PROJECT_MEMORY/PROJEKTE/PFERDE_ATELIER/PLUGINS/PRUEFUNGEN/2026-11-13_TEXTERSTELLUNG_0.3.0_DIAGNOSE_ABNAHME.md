# Pferde Atelier – TEXTERSTELLUNG 0.3.0-test, Diagnose und Chatübergabe
**Datum:** 13.11.2026 · **Status:** Nur TESTINSTALLATION, KEINE Livefreigabe.

## Was wurde wirklich erledigt?
- Extern sichtbar heißt das separate WordPress-Plugin **Texterstellung**. Eigener Ordner `texterstellung`, eigene Klassen `TXE_*`, eigener Auftragsbereich `texterstellung_orders_v1`; keine Abhängigkeit von aktiven PSTE-/PSERC-/PPM-Klassen. Kein altes Plugin wurde verändert.
- **Integrierte Diagnose**, kein zweites Plugin und kein weiterer fachlicher Worker. Im WordPress-Backend unter **Werkzeuge → Texterstellung → Diagnosebericht für die Fehlersuche herunterladen (JSON)**.
- Der Diagnosebericht ist **für den Assistenten/Entwickler** gedacht: einzelne tatsächliche Verarbeitungsschritte und Fehler mit Zeit, Aktionsnamen, Fehlercode, Anweisungscode-Stelle, einzelne fehlerhafte Rückläufe mit Index, alte/new Statuszählungen, sichtbare Freigabedaten, Kategorien, fehlende Pflichtfelder, ursprüngliche vs lokal erzeugte Artikelplätze, Lieferbatch, Entwurfs-/Statusdaten, WordPress-Umgebung und boolesche DataForSEO-Credential-Präsenz. Keine API-Schlüssel, Passwörter, vollständige Texte, Nonces oder rohe Anbieterfehlermeldungen. Schlüsselwörter und Titel sind enthalten und dürfen beim Teilen bewusst geprüft werden.
- Eigene begrenzte Historie (letzte 160 Ereignisse), lesend für den Auftragsbestand und nur bei expliziten Schritten/protokollierten Fehlern geschrieben. Keine automatische Übermittlung an ChatGPT oder Dritte, nur manuell herunterladbar mit Administratorrecht und Nonce.
- Die Einmalprüfung von Suchintention/Kategorie wird dadurch **nicht wiederholt**. Diagnose meldet Tatsachen und trifft keine neuen fachlichen Entscheidungen.
- Bestandsabläufe: externe Titeldatei und **genau fünf K0-Felder** bleiben erhalten; der K0-Rückimport erzeugt weiterhin nur WordPress-Entwürfe. Getrennte Tests bestätigen, dass das Plugin auch ohne aktive alte Klassen startet.

## Tatsächliche Quell- und QA-Basis
- Angefertigt aus einer **getrennten Kopie** der vollständig geöffneten, zuvor lokal bestandenen `Artikelwerkstatt_KISS_0.2.0_TEST_INSTALLIEREN.zip` (SHA256 `f381f622af5eca5714a2f289169ce3774ef9afdf68423b9f2be416fcb1830171`). Die Datei blieb unverändert.
- PSTE 0.57.144.50 QA original ZIP `7fc98a17e4c2319a66afd23c0ad944a07b4492e7a9982933205f29069fdcd121` und PSERC 0.28.71 QA original ZIP `fd80f7ec3451b437be0eaeedabf2142c5eb1b5130939f7b8dba3b3a2f9d2b59f` blieben unverändert.
- **119 bestandene lokale Tests** (gegen PHP-/WordPress-Funktionsnachbildungen), darunter 35 reale historische Freigabe-/K0-Gegenproben, 28 Integrationsprüfungen, 15 20er-Chargen/Backend-Prüfungen, 5 fehlerhafte Einzelrückläufe, 27 Diagnoseprüfungen, 9 weitere Fehler-/JSON-Download-Gegenprüfungen. 6/6 PHP-Syntaxprüfungen und ZIP-CRC PASS.
- Bei den 61 alten Freigaben erkennt der Diagnoseexport belegte Lücken in Kategorien und Artikelart. **61 intern erzeugte Platzkennungen** werden nun ausdrücklich als *lokal erzeugt* gekennzeichnet; es wird nicht behauptet, sie seien echte PPM-Buchungen.
- Ein absichtlich fehlgeschlagener Testexport erzeugte `ACTION_FAILED: NO_APPROVED_READY_ARTICLES` im Ereignisverlauf, einschließlich betroffenem Aktionsnamen. Ein fehlerhafter Rücklauf erzeugte `RETURN_ITEM_HELD` für den betroffenen Einzelartikel, ohne die anderen zu stoppen.
- Die neue Plugin-Hauptdatei lautet `texterstellung/texterstellung.php`. Requires PHP **8.1** (alte Angabe 8.0 für `array_is_list` wurde korrigiert).

## Paket zum Installieren – nur auf geklonter Testseite
`Texterstellung_0.3.0_TEST_INSTALLIEREN.zip` · **30.973 Bytes** · SHA256 **`9fe7d4a3e4f168bace01f014ff4f358db2f01b6b8b9e532734f2085bfbb91974`**.
ZIP enthält acht Dateien, darunter sechs PHP-Quelldateien, ein Regel-JSON und ein knappes README. Kein zusätzliches Plugin. Eigener WordPress-Name `Texterstellung`.

## Genaue nächste Aktion (nächster Chat)
1. Die **neueste** ZIP `Texterstellung_0.3.0_TEST_INSTALLIEREN.zip` auf der ausdrücklich getrennten WordPress-Testseite installieren und aktivieren; nicht mit alter Pluginversion 0.2.0 verwechseln. Die alten PSTE-, PSERC- und PPM-Plugins auf der **Testseite** ggf. vom Benutzer selbst deaktivieren. Live nie anfassen.
2. WordPress → **Werkzeuge → Texterstellung**. Diagnose direkt vor dem ersten Versuch herunterladen. Einen Sofortartikel, eine Titelrunde und einen K0-Import mit echten Testdaten versuchen. Bei einem Fehler **nach dem Versuch** erneut Diagnose-JSON herunterladen und im Chat hochladen.
3. Den Diagnosebericht zuerst auf **exakte Fehlercode/Status-/Einzelauftrags-Beweise** prüfen. Nur die nachgewiesene fehlerhafte Funktion isoliert korrigieren; keine neue SEO-Prüfung, kein neuer Worker, kein zusätzlicher Diagnose-Pluginbau.
4. Vollständige echte WordPress-/DataForSEO-/K0-Funktion ist **noch nicht nachgewiesen**. Die automatische vollständige semantische Themenfreigabe der bisherigen PSTE ist **noch nicht gleichwertig eingebaut**; sie läuft derzeit nur als einmalige manuelle Redaktionsfreigabe. Die echte K0-PPM-Slot-Kompatibilität muss in der Testumgebung noch belegt werden. **Nicht als Liveersatz freigeben.**
5. Falls das frühere Pilot-Plugin schon auf der Testseite installiert wurde: Es besitzt einen **anderen Datenspeicher**. Kein stillschweigendes Übernehmen seiner Pilotaufträge; alte Archiv-/PSTE-Daten bleiben nur lesend.

## Hard-Regeln
Keine Änderung an Live, WP-Core, Frontend, externem Titelworker, K0 oder Original-Importformat. Nicht behaupten, dass lokale Tests die echte WordPress-Testseite beweisen. Originale unverändert, ein separates Testplugin, ein konkretes Diagnose-JSON pro Fehlersuche, ein Entscheidungseigentümer pro Fachfrage. Das GitHub-PR-Dokument ist ein Arbeitsnachweis, keine offizielle neue Campus-CURRENT-Autorität.