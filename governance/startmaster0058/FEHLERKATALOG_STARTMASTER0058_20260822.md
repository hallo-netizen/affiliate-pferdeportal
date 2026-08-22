# FEHLERKATALOG – STARTMASTER0058 / PROZESSFEHLER 2026-08-22

## F58-01 – unnötige Plugin-Änderung als frühe Lösung

**Fehler:** Verlust/Unklarheit des Supervisor-Private-Keys führte zu einem neuen PSERC-Keyring-Recovery-Build, bevor der bestehende Signierpfad als Ganzes maximal eng geprüft/erklärt war.
**Risiko:** unnötige Änderung am installierten System.
**Gegenregel:** Vor jedem Pluginupdate `CHANGE_NECESSITY_GATE`: Kann der aktuelle installierte Stand den erforderlichen Pfad mit vorhandenen Artefakten/Keys/Signer/Contracts vollständig ausführen? Wenn ja, Update verboten. Wenn unbekannt, BLOCKED.

## F58-02 – falsches Drei-Dateien-Uploadmodell

**Fehler:** Es wurden drei Einzeluploads verlangt, obwohl der aktuelle Produktionstrigger eine einzige hashgebundene Produktionspaket-Datei verlangte.
**Ursache:** alte Workflowerinnerung wurde über aktuellen Source/UI-Contract gestellt.
**Gegenregel:** Upload-/UI-Anweisungen ausschließlich aus aktuellem installierten Contract/Source oder aktuellem Live-Screenshot.

## F58-03 – unvollständigen Bildschirm als vollständigen Zustand interpretiert

**Fehler:** Oberer Redaktionsplan-Ausschnitt wurde kurzzeitig als vollständige Seite interpretiert.
**Gegenregel:** Bei UI-Anweisungen muss der sichtbare relevante Block selbst belegt sein; kein Schluss aus fehlender Sichtbarkeit.

## F58-04 – alten Screenshotzustand als aktuell bezeichnet

**Fehler:** Nach neuem Redaktionsplanaufbau wurde kurzzeitig ein älterer 5er-Handoff-Screenshot als aktueller Zustand beschrieben.
**Gegenregel:** Live-Belege bekommen `observed_at`/Revision; neuester eindeutiger Live-Beleg schlägt ältere Screenshots/Chattexte.

## F58-05 – unnötige Wiederholungsprüfungen

**Fehler:** statische MASTER-/Source-/Contract-/QA-Belege wurden mehrfach neu geprüft, obwohl die Eingaben unverändert waren.
**Folge:** erheblicher Zeitverlust und zusätzliche Gelegenheit für Fehlinterpretationen.
**Gegenregel:** HASH-EVIDENCE-CACHE; statischer PASS bleibt gültig, solange alle Input-/Contract-/Tool-Version-Hashes identisch sind.

## F58-06 – fehlender Chat-Nullpunkt

**Fehler:** Folgechats mussten zu viel aus umfangreicher Historie rekonstruieren.
**Gegenregel:** jede MASTER enthält einen `CURRENT_POINTER` mit installiertem Stand, aktuellem Livezustand, offenen Punkten, nächstem erlaubtem Schritt, verbotenen Änderungen und GitHub-Branch.

## F58-07 – Titel-Phrasenregel praktisch zu schwach

**Fehlerbild:** mehrere Beratungstitel verwenden wiederkehrende Phrasenfamilien wie „passend auswählen“ bzw. „anhand/nach wichtigen Kriterien auswählen“.
**Bestehende Regel:** keine stereotypen Phrasenwiederholungen / keine Generator-Schablonen.
**Root Cause:** die Regel war für Journal explizit hart dokumentiert, aber im allgemeinen zukünftigen Titelpfad nicht als batchweiter Bestands-/Phrasenfamilien-Hardlock ausreichend erzwungen.
**Gegenregel:** allgemeiner upstream Titelqualitäts-Hardlock vor Textmaschine für alle neuen Beitragsarten.
**Bestandsschutz:** die fünf bereits veröffentlichten Beiträge werden nicht rückwirkend verändert.

## F58-08 – falsches PASS aus Teilbeleg

**Risiko:** ein erfolgreicher Teiltest kann als Gesamtworkflow-PASS missverstanden werden.
**Gegenregel:** Gate-Ergebnis bleibt PASS/FAIL/BLOCKED; Gesamt-PASS nur bei vollständiger Belegkette. Hash-Caching darf nie fehlende Belege erzeugen.

## F58-09 – Redaktionsplan-Replay nach Veröffentlichung

**Risiko:** bereits veröffentlichte Positionen könnten erneut als READY erscheinen, wenn Inventar-/Snapshotfortschreibung nicht greift.
**Aktueller Livebeleg:** nach Neubau Handoff 0 / kein aktueller READY-Block.
**Gegenregel:** vor jedem neuen Produktionshandoff `TERMINAL_EXISTENCE_GATE`: live vorhandene Draft/Publish-Identität oder gebundener terminaler Fingerprint sperrt erneute Produktion derselben Position.
