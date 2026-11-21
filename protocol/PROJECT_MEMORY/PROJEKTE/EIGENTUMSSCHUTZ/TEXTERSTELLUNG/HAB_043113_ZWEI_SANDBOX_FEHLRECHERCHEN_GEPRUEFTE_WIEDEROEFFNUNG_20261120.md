# Hab & Bewahr – 20.11.2026 – Freigabe der beiden fehlerhaften Sandbox-Recherchen

Die beiden vorhandenen abgeschlossenen Testrecherchen **Abholbox mit passenden Zugangsrechten und Schutz ausstatten** und **Abluftanlagen & Unterdruck** hatten jeweils neun nutzlose Keywords und null verwendbare Ergebnisse. Wegen gespeicherter `ANALYZED_NO_ELIGIBLE_CANDIDATE`-Original-Läufe stehen sie bisher nicht mehr in der Liste offener Kategorien.

Der Live-Stand vor diesem Fix: WordPress-Plugin **0.4.31.12**, effektive Echtdaten-Verbindung `api.dataforseo.com`. **Neues freigegebenes lokales ZIP: 0.4.31.13**. Es bleibt ein Update des vorhandenen Plugins, kein zusätzliches Plugin.

Eine neue einmalige explizite WP-Admin-Aktion `txe_research_reopen_sandbox_two` lässt nur exakt diese zwei Themenfamilien erneut als `NOT_ANALYZED` zählen. Sie prüft vorhandene Original-Anbieterlaufbelege (`environment=sandbox`, abgeschlossen ohne geeignete Kandidaten), Kategorie- und Laufidentität sowie Abwesenheit einer laufenden Queue. Alte `pste_runs`, Kandidaten, Anbieterbelege, Kosten und K0 bleiben unangetastet. Ein eigener signierter Ausnahmebeleg wird einmalig gespeichert; die ursprüngliche eine `PSTE_Repository::categoryProgress()`-Stelle ignoriert genau diese beiden alten Sandbox-Fertigmeldungen. Sobald echte neue Rechercheergebnisse entstehen, gelten deren reguläre Status. **Keine kostenpflichtige Anfrage bei Installation, Wiederfreigabe oder Statusanzeige**.

**Am endgültigen ZIP geprüft:** 38/38 Wiederfreigabe-Positiv-/Negativfälle, 134/134 bestehende Original-PHP-Funktionstests, 30/30 Echtdaten-Modusprüfungen, 78/78 PHP-Lints, 87/87 ZIP-Einträge. 84/87 Dateien unverändert gegenüber 0.4.31.12. Keine tatsächliche WordPress-Live-Rücksetzung oder bezahlte DataForSEO-Abfrage durchgeführt.

**Installation:** Bestehende 0.4.31.12 mit `Texterstellung_HAB_UND_BEWAHR_0.4.31.13_ZWEI_FEHLRECHERCHEN_WIEDER_OEFFNEN.zip` **ersetzen, nicht deinstallieren**. `Texterstellung → Recherche → Beide Fehlrecherchen wieder öffnen – kostenlos` einmal klicken; danach müssen **2128 offene Themen** statt 2126 sichtbar sein, sofern sich kein anderer Status geändert hat. Unter **Bestimmte offene Kategorien auswählen** gezielt beide auswählen; erst danach mit ausdrücklicher Kostenfreigabe neu recherchieren. Alte Abschlussliste zeigt den archivierten Sandbox-Versuch und ist kein Nachweis eines erneut verarbeiteten echten Ergebnisses.

**Datei SHA256:** `37392e954be2733583282f8a45b8d02400c84d84839fa3c4b0939667a638c304`. ZIP und QA samt Originaldiff/Testprogramm im Hab-Büro gespeichert: `/hab-und-bewahr/TEXTERSTELLUNG/PLUGIN_FREIGABEKANDIDATEN/` und `/hab-und-bewahr/TEXTERSTELLUNG/PRUEFUNG_ZWEI_SANDBOX_RESET_20261120/`.

**Grenze:** Noch keine Live-Bestätigung. Keine weitere Pluginversion ohne neuen konkreten Befund.
