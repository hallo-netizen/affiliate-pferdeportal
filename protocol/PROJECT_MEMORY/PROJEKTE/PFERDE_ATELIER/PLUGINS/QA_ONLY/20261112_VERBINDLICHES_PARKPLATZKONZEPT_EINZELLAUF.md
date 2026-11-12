# VERBINDLICH: Parkplatzkonzept – **ein einzelner Produktionslauf**, 12.11.2026

## Festgelegte Fakten und Annahmen des Nutzers
- Es läuft **maximal ein** Produktionsauftrag gleichzeitig. Keine konkurrierende Herstellung/Importierung.
- **Änderungen von außen während des Auftrags sind zu 100 % ausgeschlossen.** Nicht erneut als normalen Risikofall unterstellen.
- MINI und externe Agenten sind **fester Bestandteil** des Produktionswegs, keine Beta, keine zweite SEO-Instanz.
- Abbruch/Wiederanlauf gesondert betrachten: Jeder Agent muss den **zuletzt gespeicherten Bearbeitungsstand** offenlegen; nach Neustart Fortsetzung an diesem Stand, **keine neue fachliche Entscheidung**.
- Keine WordPress-Core-Änderung, keine neuen Agenten, Gate-Plugins, Datenbanken oder Wiederholschleifen; KISS.
- Eine fachliche Entscheidung pro Thema/Planplatz; von WordPress und späteren Stationen nur **lesend weitergegeben**.

## Einfache verbindliche Sequenz
0. **Ausgangslage**: ein gültiger, aktueller Redaktions-/Parkhausplan (mit vorhandenem WP-Artikelbestand und allen früheren reservierten/belegten Plätzen).
1. **Genau einmal** Planplatz *P* anhand dieses Ausgangsplans bestimmen und **reservieren**. Die SEO-/Intent-/Belegtheitsentscheidung fällt in der vertraglich vorgesehenen einzigen externen MINI-/SEO-Instanz; die Themenengine stellt Quellen bereit, übernimmt die einzige Entscheidung.
2. Nur *P*, die ursprüngliche Keyword-Quelle und den maßgeblichen Planstand an MINI/externe Agenten übergeben; Titel und fachliche Zuarbeit erstellen lassen. Der Plan wird während dieses *einen* Produktionslaufs nicht durch Dritte verändert.
3. MINI-Ergebnis **dem reservierten P zuordnen**. Nur eindeutige Identität/Herkunft technisch binden; **keine erneute Parkplatzsuche, kein neuer Redaktionsplan, kein erneuter semantischer/SEO/Titel-Entscheid**.
4. Den bereits zugeordneten Platz/Artikelauftrag als *bereit für K0* kennzeichnen und vorhandene fünf Metadatenfelder unverändert an K0 übergeben.
5. K0 erstellt Artikel und prüft **nur den neu erzeugten Text** (81 vereinbarte Inhaltsregeln, LanguageTool); keine erneute Keyword-/Intent-/Platzentscheidung.
6. WordPress-Import nimmt den fertigen Artikel zu P, verbucht **P als abgeschlossen** in der vorhandenen PPM-/Redaktionsplanbelegung. **Ab hier** wieder einen aktuellen Ausgangsplan für den nächsten Auftrag verwenden.
7. Ein Abbruch belässt *P* als reserviert; gespeicherte Stufe zeigt **was fertig und was offen** ist, der Neustart führt nur die unvollständige Stufe fort. Kein fingiertes Grün, kein neues Thema und keine Doppelproduktion.

## Wo technische Prüfungen erlaubt sind
- **Einmal bei Auftragseröffnung:** Vollständigkeit und Eindeutigkeit des Ausgangsplans, freie Belegung, Original-Keyword; sichere Reservierung vor dem Export.
- **Bei Übergaben:** Darf ausschließlich kontrolliert werden, dass *dasselbe Originalpaket* und *derselbe reservierte P* übergeben werden. Falls Paket oder Stand beschädigt, den betroffenen Auftrag halten; nicht inhaltlich neu entscheiden.
- **Bei K0:** Qualität des *neuen Artikels*, nicht Suchintent oder Redaktionsplatz.
- **Beim Import:** Ergebnis zum reservierten P korrekt verbuchen; keine eigene Neubeurteilung; atomarer Abschluss/Idempotenz für Neustart.
- **Nicht im normalen Einzelauftrag:** Nachgelagerte Vollplan-Frische-, Neu-SEO-, Kannibalisierungs-, Titel- oder globale Kontext-/Status-Neubewertungen. Solche Checks sind nur für wirklich andere fachliche Änderungsaufträge relevant.
- **Keine Freigabe aus fehlenden Nachweisen:** Ohne beweisbare ursprüngliche Entscheidung oder unveränderte Originalquelle keinen neuen Pass fingieren. Erstzustand/Abbruch sind nicht mit einer nachträglichen Fachentscheidung gleichzusetzen.

## Konkreter IST-Code (QA-Ausgang PSTE 0.57.144.45 / PSERC 0.28.69)
Bereits belegte Doppelwege/Abhängigkeiten im letzten Audit:
1. `PSTE_Mini_Workflow::forwardToPlan` vergleicht **den gesamten** Parkhaus-Hash mit dem ursprünglichen externen Ergebnis **nach** der Entscheidung. Unter den obigen Serienlaufbedingungen vergleicht dies einen späteren Zustand, obwohl der Platz beim Start festgelegt wurde; falsches Rückstellen möglich.
2. `PSTE_Mini_Workflow::readExistingPsercPlanForParkhaus` verlangt PSERC-`isCurrent` und kann schon wegen rein technischen Context-/Jobänderungen einen **bestehenden** gültigen Plan als nicht vollständig markieren. Der vorhandene Planbestand darf nicht mit einem noch ausstehenden zukünftigen Neubau verwechselt werden.
3. `PSERC_Compiler::compile` und `PSERC_Plan_Compile_Job::tickCandidate` rufen bei einem bereits in PSTE entschiedenen Kandidaten **ohne** spezialisierten MINI-Beleg nochmals den semantischen Duplicate-Gate; beim MINI-Kandidaten wird der Gate übersprungen. Das muss als **eine Zuständigkeitsregel für alle wirklich zentral signierten Kandidaten** festgelegt werden.
4. `PSERC_Plan_Dependency_Fingerprint::current` bindet global `context_status`, `context_generation`, `job_uuid`, obwohl sich daraus allein keine andere fachliche Belegung ergibt. Die Abhängigkeit von bloßen technischen Zwischenständen ist vom fachlichen Ausgangsplan zu trennen.
5. `PSERC_System4_Import::importPayload` schreibt Entwürfe und meldet an `PPM679_Editorial_Plan_Runtime_Gate::record_readback`; die PSTE-Themenliste wird nicht direkt mit »fertig« beschrieben. Nach Import die **bereits bestehende** PPM-Verbuchung als alleinige Abschlusswahrheit berücksichtigen; nicht wegen eines anderen Status alles neu berechnen.

## Umsetzung und Test, kein voreiliges GO
- Änderungen nur an **bestehenden** PSTE-/PSERC-Funktionen, gestützt auf echten Aufrufpfad. Kein Entfernen von MINI, K0-Regeln, Bestandsschutztabellen oder persönlichen Testdaten.
- Tests ausschließlich gegen **finale installierbare ZIP-Dateien**, nicht gegen eine andere Arbeitskopie.
- In schon vorhandener WordPress-TEST-Installation braucht der reale Durchlauf: *P reserviert → MINI erledigt → K0-Artikel hergestellt → WordPress importiert → P geschlossen*. Nach Neustart genau dort weitermachen, wo der letzte Schritt endete.
- Solange der echte WP-Lauf nicht nachgewiesen ist, bleibt alles QA. Das Speichern dieses Vertrags auf GitHub ist **keine Live-Änderung und keine Behebung**.
