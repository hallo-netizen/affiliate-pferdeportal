# Pferdeatelier – Ein einziger zentraler Entscheid: belegte Korrektur am Original

**Stand:** 12.11.2026. **Nur QA-Arbeitsstand, NICHT als WordPress-Plugin installieren.**

## Die eine tatsächlich neu vorgenommene Codeänderung

**Originalfehler nachgewiesen:** `PSTE_Runner::applyInternalDuplicates()` sperrt bei der abschließenden Stapelentscheidung ein nachweislich doppeltes Thema (`decision=BLOCKED`), lässt aber in **demselben Datensatz** `planning_readiness_gate.status=PASS`, `decision=PASS`, `ok=true` unverändert. Das ist eine widersprüchliche Übertragung, *nicht* eine weitere fachliche Meinung. Zwei unterschiedliche Stationen können deshalb unterschiedliche Ergebnisse aus demselben Thema lesen.

**Quellort:** `Portal SEO Topic Engine/includes/class-pste-runner.php` bei der schon bestehenden zentralen Methode `applyInternalDuplicates()` (nach dem bestehenden Setzen von `DUPLICATE_WITHIN_RESEARCH_RUN`). Die Funktion wird schon beim **Fertigstellen der Recherche** ausgeführt; hier findet **keine nachgelagerte Prüfung** statt.

**Minimaländerung:** Nur wenn die bestehende endgültige Stapelentscheidung ein Thema als doppelt blockiert, wird der bereits vorhandene `planning_readiness_gate` **im selben Datensatz** auf `BLOCKED`, `ok=false` und denselben begründenden Fehlercode gesetzt. Keine neue Funktion, kein neuer Worker, keine Tabelle, kein zweiter Prüfaufruf. Für unveränderte positive Themen und fremde historische Vertragsformen wird **gar nichts** verändert.

**Vertrag:** Eine zentrale Entscheidung und danach widerspruchsfreie Übergabe. Der Worker nach der Recherche muss keine zweite Entscheidung treffen. Das ist noch **nicht** die vollständige verlangte Vor-MINI-Reservierung – kein solcher Erfolg wird behauptet.

## Positive und negative Beweise aus den Originalmethoden

`QA_FINALER_STAPELBESCHEID_ORIGINALMETHODE.php` ruft die **echte unveränderte Originalmethode** und die **echte geänderte Arbeitsmethode** mit identischen Daten auf. **Vorher**: endgültig `BLOCKED` bei echter Doppelung, aber alter Gate-PASS bleibt. **Nachher**: dieselbe Sperre, Gate ebenfalls `BLOCKED`. Alle bestehenden Entscheidungen bleiben gleich: 2 `PASS`, 3 `BLOCKED`; unabhängiger Fachbereich weiterhin freigegeben; Quertyp-Doppelung weiterhin gesperrt; alte abweichende Gate-Verträge unverändert; zweiter Durchlauf ohne zusätzliche Änderung.

Die Rohresultate stehen in `VORHER_ORIGINAL.json` und `NACHHER_ARBEIT.json`. Der exakte minimale neue Quellunterschied steht in `EINZIGE_NEUE_QUELLENKORREKTUR.patch`.

## Unveränderte bekannte Ausgangsbasis

- PSTE **0.57.144.45**, Originaldatei SHA-256 `d3057946defc035af7abe5522c4845625c98ebd3f2cf621e1b3c5ce019f230a4` (121 Dateien, 83 PHP).
- PSERC **0.28.69**, Originaldatei SHA-256 `576e58b51db3f348210dc3d47a894d6551558acc0c6900505be5e11257d2e41b` (63 Dateien, 43 PHP).
- Bereits zuvor geprüfte **zwei** Arbeitsänderungen bleiben erhalten: PSTE `includes/class-pste-repository.php`; PSERC `includes/class-pserc-plan-dependency-fingerprint.php`.
- **Neu** ist genau *eine* Arbeitsänderung: PSTE `includes/class-pste-runner.php`.
- Alle weiteren **181 Quelldateien** sind zu den Originalen byteidentisch. **126/126 PHP-Syntaxprüfungen bestanden**.
- Bestehende Offline-Gesamtsimulation **18/18 bestanden**, mit nachgebildeter WordPress-Datenbank und **zwei simulierten Entwürfen** – kein echter K0-Text und keine Live-WordPress-Ausführung.

## Was nicht als erledigt ausgegeben werden darf

Die **dauerhafte physische Slot-Reservierung vor MINI** mit der vorhandenen PPM-Planverwaltung, die ausschließliche Titelrolle von MINI und der Wegfall nachträglicher SEO-Bewertungen im PSERC sind **noch nicht vollständig programmiert oder live nachgewiesen**. Auch der ursprüngliche Doppelungsalgorithmus bleibt bei einigen inhaltlich unterschiedlichen Fragen ungenau; dieser Fehler wird **nicht** durch eine unsichere Heuristik umgangen.

**Regel für Fortsetzung:** Keine ungesicherten .46/.70-Pauschaländerungen übernehmen. Mit genau diesem einem Arbeitsstand an den **vorhandenen** Quellen weiterarbeiten. Keine neuen Prüfstationen, kein neuer Slot-Speicher. Erst ein vollständig verifizierter Pluginstand darf als testweise installierbar bezeichnet werden.

**Verifizierter privater Arbeits-ZIP-Stand:** `AKTUELLER_GEAENDERTER_ARBEITSSTAND_BEWIESENER_TEILSCHRITT_NUR_QA_20261112.zip`, 1.834.028 Bytes, SHA256 `2e1e0c839d99bd00deb34cae9dbacb58d34e5aac78b2e885df4d161c2436d63b`, unter `/pferdeatelier/PLUGINS/ARBEITSRAUM_PSTE_KISS/`. Ein neues Produktions- oder Installationspaket wurde **nicht** erstellt.
