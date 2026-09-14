# GLOSSAR – PRODUKTIONSREGELN

STAND: 2026-09-14
STATUS: VERBINDLICH

## 1. Themencluster statt isolierter Beziehungen

Sobald bei einem neuen Glossarbegriff fachlich sinnvolle verwandte Glossarbegriffe festgestellt werden, werden diese als technische Beziehungen mitgedacht und – nur bei frisch belegter `GEPRUEFT`-WDB-Quelle – im selben Produktionszusammenhang ergänzt.

Ein Glossar-Produktionslauf gilt erst als vollständig, wenn:
- jeder als verwandt ausgewiesene Begriff als echter Glossarbeitrag existiert;
- die Beziehungen technisch auflösbar sind;
- die Box `Verwandte Begriffe` nur echte veröffentlichte Glossarbeiträge verlinkt;
- der gesamte Fließtext **0 Links** enthält;
- die passende Portal-Kategorie ausschließlich rechts in `Mehr zum Thema` verlinkt wird;
- kein Linkziel doppelt gesetzt ist.

## 2. Veröffentlichungsreihenfolge

Für maschinell erzeugte neue Cluster gilt:
1. alle Cluster-Mitglieder zunächst als Entwurf anlegen;
2. Inhalte, Kurzdefinition, Kategorie/Portalbindung, Metaangaben und Beziehungen für alle Mitglieder setzen;
3. Text-/Linkregeln für sämtliche Mitglieder positiv und negativ prüfen;
4. erst wenn der gesamte Cluster vollständig ist, alle Cluster-Mitglieder veröffentlichen.

Damit kann kein halber Cluster öffentlich werden.

## 3. Interne Links

Verbindlich je Begriff:
- im Fließtext **kein Link**;
- verwandte Glossarbegriffe ausschließlich als Links in der rechten Box `Verwandte Begriffe`;
- Portal-Kategorie ausschließlich als Link in der rechten Box `Mehr zum Thema`;
- Journal-Bereich/Kategorie dort nur ersatzweise, wenn kein passendes Portal-Ziel existiert;
- dasselbe Ziel niemals doppelt auf derselben Einzelansicht.

Details ausschließlich in `TEXT_UND_LINKREGELN.md`.

## 4. Verwandte Begriffe

`Verwandte Begriffe` ist kein Freitext-Friedhof.

Ein Begriff darf dort nur erscheinen, wenn:
- ein veröffentlichter `uge_term` dazu existiert;
- der Link auf diesen echten Glossarbeitrag auflösbar ist.

Fehlt der verwandte Begriff, darf er nur erzeugt werden, wenn seine WDB-Quelle frisch als `GEPRUEFT` belegt ist. Keine Erzeugung aus Chatwissen oder Alt-Paketen ohne Fachbeleg.

## 5. Pferderassen

**Pferderassen und Ponyrassen sind im Glossar tabu.**

Sie gehören ausschließlich in das separate Pferderassen-System/Büro und werden weder als Glossarbeitrag noch als automatisch nachgezogener verwandter Begriff erzeugt.

## 6. Textaufbau

Standard und Pflicht für Glossarbeiträge:
- Titel;
- sichtbare Kurzdefinition/Zusammenfassung;
- ca. 150–200 Wörter;
- wenige natürliche Absätze;
- **keine Zwischenüberschriften**;
- **0 Links im Fließtext**;
- verwandte und thematische Links ausschließlich in den rechten Seitenboxen.

Keine H2/H3 im Begriffstext aus SEO-, Schema- oder Gestaltungsmotiven.

## 7. Paketregel

Ein neuer Pluginstand erzwingt **nicht automatisch** neue Glossarbegriffe. Neue Begriffe werden nur erzeugt, wenn die fachliche WDB-Grundlage `GEPRUEFT` vorliegt und der Produktionsauftrag dies tatsächlich umfasst.

## 8. Bestehende Glossarbeiträge

Bereits veröffentlichte oder angelegte Glossarbeiträge werden wegen neuer Regeln nicht pauschal gelöscht.

Stattdessen gilt:
1. vorhandenen Beitrag eindeutig per Slug/ID bestimmen;
2. in `BEGRIFFSREGISTER.md` auf `NACHPRÜFUNG` führen;
3. bestehenden Datensatz gezielt **überschreiben/aktualisieren**, ID und URL erhalten;
4. Inhalt, Kurzdefinition, Metaangaben, Portalbindung und Relationsdaten prüfen;
5. **sämtliche Links aus dem Fließtext entfernen**, Linktext als normalen Text erhalten;
6. verwandte Links ausschließlich rechts in `Verwandte Begriffe`, Portalziel ausschließlich rechts in `Mehr zum Thema` ausgeben;
7. normale WordPress-Beiträge negativ gegen Veränderung prüfen;
8. erst nach vollständiger technischer und erforderlicher Liveprüfung auf `FERTIG` setzen.

Löschen ist nur zulässig, wenn ein echter Dublette-, Fehl- oder Testdatensatz nachgewiesen ist.

## 9. Autoritatives Begriffsregister

Die Produktionswahrheit `OFFEN / IN ARBEIT / NACHPRÜFUNG / FERTIG / GESPERRT` liegt ausschließlich in:

`BEGRIFFSREGISTER.md`

Kein zweites paralleles Erledigt-/Unerledigt-Register anlegen.

## 10. Portal-Kategorien und Portal-Landingpages haben SEO-Vorrang vor neuen Glossarbegriffen

Für neue Glossarkandidaten gilt verbindlich:

1. **zuerst gegen echte WordPress-Kategorien UND gegen starke veröffentlichte Portal-Landingpages prüfen**;
2. technisch sind Portal-Hauptseiten im Pferde Atelier nicht durchgehend WordPress-`category`, sondern teilweise normale hierarchische WordPress-Seiten (`post_type=page`);
3. stimmt der normalisierte Glossarbegriff mit einer solchen Kategorie oder Portal-Landingpage überein, einschließlich gebundener Singular/Plural-Normalisierung wie `Regendecke` ↔ `Regendecken`, wird **kein neuer Glossarbeitrag** erzeugt;
4. Status bei Taxonomie-Treffer: `AUSGESCHLOSSEN_KATEGORIE`;
5. Status bei Portal-Landingpage-Treffer: `AUSGESCHLOSSEN_PORTALSEITE`;
6. danach keine Fachrecherche, kein Textpaket und keine Veröffentlichung für diesen Kandidaten;
7. erst Kandidaten ohne Kategorie-/Portalseiten-Treffer laufen weiter in Glossar-Dublette und sonstige Artikel-/Seiten-Kannibalisierung;
8. normale Beiträge werden durch einen exakten Titel nicht als Portal-Landingpage behandelt; sie bleiben Teil der normalen Kannibalisierungsprüfung;
9. bestehende bereits geprüfte/veröffentlichte Glossarbeiträge werden durch diese neue Kandidatenregel **nicht pauschal gelöscht oder umgeschrieben**.

SEO-Grund: Die starke Portal-Zielseite ist in diesem Fall die bevorzugte Google-Zielseite und soll nicht durch einen zusätzlich neu erzeugten Glossarbeitrag konkurrenziert werden.

## 11. Gate-Hardlock über die komplette Automationskette

Die Ausschluss-/Sicherheitsprüfung darf **nicht nur bei der Kandidatenfindung** stattfinden.

Verbindliche Prüfpunkte:

`Discovery -> Kategorie/Portalseite/Dublette/Kannibalisierung -> Research-Paket-Eingang -> PRE-PUBLISH -> WordPress-Readback`

Harte Regeln:

1. Ein Kandidat, der bei Discovery an Kategorie, Portal-Landingpage oder Kannibalisierung scheitert, darf nicht weiterverarbeitet werden.
2. Am Research-Paket-Eingang werden dieselben Bestands-/SEO-Gates **erneut** gegen den aktuellen WordPress-Bestand ausgeführt.
3. Ein Research-Paket darf keinen neuen Kandidaten aus dem Nichts erzeugen. Neue Begriffe müssen vorher im autorisierten Kandidatenpool existieren; nur ein bereits real vorhandener Glossarbeitrag (`BESTAND`) darf direkt an seine bestehende ID gebunden werden.
4. Ein Research-Paket für Kandidat A muss maschinenfest auch Kandidat A enthalten. Abweichendes Ziel -> `RESEARCH_PACKAGE_TARGET_MISMATCH` und keine Übernahme.
5. Unmittelbar vor jedem WordPress-Write wird der aktuelle Bestand erneut gelesen und dieselbe Kategorie-/Portalseiten-/Kannibalisierungsprüfung ausgeführt.
6. Entsteht zwischen Research und Publish eine neue konkurrierende Portal-/Kategorieseite, muss der Publish dadurch noch gestoppt werden.
7. Neue Beiträge werden zuerst als Draft geschrieben, danach müssen definierte Felder aus WordPress real zurückgelesen werden. Erst bei identischem Readback darf veröffentlicht werden.
8. Bei Update eines bestehenden Glossarbeitrags ist vor dem Write ein Snapshot zu sichern; bei Readback-/Publishfehler wird zurückgerollt.
9. `SANDBOX` darf unabhängig vom Auto-Publish-Häkchen niemals produktiv schreiben. Realer Write ist nur zulässig bei `mode=ARMED` **und** `auto_publish=true`.
10. Der lokale PSTE-Rückstand darf zur Kandidatengewinnung vertieft werden, aber ausschließlich mit `provider_calls=0`. Jede Provider-Anforderung im Backlog-Scan -> `BLOCKED`.
11. Discovery muss vollständig fail-closed vor Research/Publish liegen. Solange Discovery `RUNNING`, `RETRY_WAIT` oder `BLOCKED` ist, dürfen Research und Publish nicht starten.

## 12. Asynchroner, wiederaufnehmbarer PSTE-Rückstand mit Planning-Vorrang

Ein kompletter PSTE-Rückstand darf **niemals** in einem einzigen Browser-/PHP-Aufruf abgearbeitet werden.

Verbindlich:

1. `Pool jetzt aktualisieren` startet/resumiert nur einen persistenten Discovery-Job; der Browserrequest führt **keine schwere Retained-Schleife** aus.
2. Ein Worker verarbeitet exakt **eine schwere Einheit**: entweder einen Retained-Backlog-Batch **oder** eine Planning-Seite. Nicht beides in demselben Request.
3. Aktueller gebundener Stand: Retained-Batch 20, Planning-Seite 25.
4. Cursor, Phase und Fortschritt werden nach jedem sicheren Teilstück dauerhaft gespeichert.
5. Es gibt **kein künstliches Gesamtlimit 400/500**. Die Discovery endet nur bei:
   - `TARGET_REACHED`,
   - echtem `BACKLOG_COMPLETE` nach finalem Planning-Drain,
   - oder hartem Fehler.
6. Liefert ein Retained-Batch `promoted > 0`, muss die Phase zwingend auf `PLANNING` wechseln.
7. Ein offener Planning-Pass hat Vorrang: **kein weiterer Retained-Batch**, bevor dieser Planning-Pass vollständig beendet wurde.
8. Ein alter Zustand mit bereits vorhandenen Promotions, aber noch nicht verarbeitetem Planning, muss beim Upgrade zuerst in `PLANNING` überführt werden. Das gilt auch bei einem bereits geplanten Worker ohne erneuten Nutzerklick.
9. Ein alter, bereits real erreichter Cursor muss bei Upgrade übernommen werden; kein Neustart bei 0 ohne fachlichen Grund.
10. Cursor-Fortschritt und PSTE-`processed` sind getrennte Größen. Für den realen Backlog-Fortschritt ist zusätzlich `traversed` / `Backlog durchlaufen` zu führen; `processed` darf nicht allein als Fortschrittswahrheit dargestellt werden.
11. Vor schwerer Worker-Arbeit muss bereits ein Recovery-Event geplant sein. Stirbt PHP/Proxy hart, setzt ein späterer Worker am letzten sicheren Checkpoint fort.
12. 502/504/Exception dürfen keinen Cursor überspringen. Fehler -> `RETRY_WAIT`; Wiederholung startet am selben Cursor.
13. Parallelworker sind durch einen Lock zu verhindern. Lock-TTL muss die PHP-Ausführungsgrenze berücksichtigen.
14. Nach echtem Ende des Retained-Backlogs ist ein **frischer vollständiger Planning-Drain** Pflicht, damit zwischenzeitlich promotete Themen nicht verloren gehen.
15. Nach Discovery-Abschluss wird die normale Automationskette über einen separaten Continue-Hook fortgesetzt; der reguläre Tages-/Halbtages-Cron darf die Sofortfortsetzung nicht blockieren.

Kein PASS aus Codeansicht. Für Änderungen an diesen Gates/Worker-Regeln sind harte Positiv-/Negativtests erforderlich. Kritische Schutzregeln müssen zusätzlich durch absichtlich gebrochene Mutanten nachweislich ROT werden. Ein lokaler Test ist nur belastbar, wenn er den real beobachteten Zustandsübergang der Live-Strecke reproduziert.
