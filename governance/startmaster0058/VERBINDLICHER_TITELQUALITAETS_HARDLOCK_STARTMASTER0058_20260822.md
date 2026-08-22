# VERBINDLICHER TITELQUALITÄTS-HARDLOCK – STARTMASTER0058

## Scope

Gilt für **alle künftig neu erzeugten Beitragstitel aller Beitragsarten**. Der Titelpfad liegt upstream vor der Textmaschine. Die Textmaschine selbst bleibt unverändert. Bereits veröffentlichte Titel werden nicht rückwirkend geändert.

## Bestehende Regel wird allgemein hart

Die MASTER enthielt bereits die Regel gegen stereotype Titelschemata. STARTMASTER0058 macht sie ausdrücklich zu einem allgemeinen Batch-/Bestands-Hardlock, nicht nur zu einer Journal-Erweiterungsregel.

## Ein Titel darf nur PASS erhalten, wenn alle Bedingungen erfüllt sind

1. natürliches, idiomatisches Deutsch
2. redaktionell sinnvoll und verständlich
3. Target Keyword/Intent semantisch unverändert
4. kein Keyword-Stakkato
5. keine Suchmaschinen-Rohphrase
6. keine künstliche Generatorformulierung
7. keine stereotype Phrasenfamilie gegen andere Titel desselben Batches und bereits vorhandene Bestandstitel
8. keine mechanische Rotation derselben Schablone durch Synonymtausch
9. keine Dublette/Kannibalisierung
10. keine nachträgliche Titeländerung in Textmaschine/PPM

## Verbotene Serienmuster

Nicht als starre Wort-Blacklist, sondern als Phrasenfamilien-/Schablonenbeispiele:

- „richtig auswählen“
- „passend auswählen“
- „gezielt auswählen“
- „anhand wichtiger Kriterien auswählen“
- „nach wichtigen Kriterien auswählen“
- „richtig einordnen“
- „fachlich einordnen“
- semantisch gleichförmige Varianten, die nur einzelne Wörter austauschen

Ein einzelnes Vorkommen kann sprachlich zulässig sein. **Eine wiederkehrende Serie ist FAIL.** Das Gate muss batch- und bestandsweit prüfen, nicht nur pro Titel isoliert.

## Keine Qualitätsabkürzung

Zur Beschleunigung wird der Titelkorpus einmal pro Inventory Revision geladen und alle Batchtitel werden dagegen geprüft. Es wird kein Gate entfernt.

## Fail-closed

Wenn keine natürliche Variante alle Regeln erfüllt: **BLOCKED**. Kein manueller PASS, kein Fallback auf rohe Suchphrase, kein Generator-Template.

## Technischer Implementierungsstatus

**Contract-Hardlock ab STARTMASTER0058 bindend.** Der beobachtete letzte Beratungsbatch zeigt, dass die praktische upstream Enforcement-Stärke für Phrasenfamilien noch nicht hinreichend belegt ist. Vor dem nächsten neuen Titelbatch muss die bestehende upstream Titelprüfung diesen allgemeinen Batch-/Bestandscheck technisch nachweisbar durchsetzen.

Die dafür ggf. nötige Sourceänderung ist ein separater eng begrenzter Block; keine Änderung an Textmaschine, Content, Design, bestehenden Titeln oder nachgelagerten Gates.
