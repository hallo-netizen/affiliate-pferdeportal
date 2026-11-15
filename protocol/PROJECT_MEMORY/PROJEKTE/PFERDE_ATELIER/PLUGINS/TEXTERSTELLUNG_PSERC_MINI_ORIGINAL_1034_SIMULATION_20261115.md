# Pferdeatelier – PSERC/MINI: echte 1.034er-Fehlersimulation (15.11.2026)

**Nur lokale PHP-Simulation. KEIN installiertes Plugin verändert, keine neue Installations-ZIP, kein Live-Eingriff.**

Ausgangslage aus tatsächlicher WordPress-Diagnose (oliver-beil.de 15.11.2026, 08:54 UTC): MINI-Export wegen PSERC_PLAN_NOT_PROVEN_COMPLETE und PSERC_ACTIVE_PLAN_INCOMPLETE_OR_STALE gesperrt. WORDPRESS, PSTE_PLAN, EDITORIAL_PLAN jeweils complete=true. Parkhaus bereits 1.034 Zeilen; 61 gespeicherte Themen, davon 1 FREI und 60 METADATEN_OFFEN.

Simulation A: In der ORIGINALEN vorhandenen PSTE_Mini_Workflow::readExistingPsercPlanForParkhaus() sind sechs Fallzustände mit nachgebildeten PSERC-Quellen durchlaufen: gültiger Plan, vollständige alte aber nicht aktuelle Abhängigkeit, fehlender Plan, manipulierte Planunterschrift, fehlender Datensatz, Plan während Lesen ausgetauscht. **6/6 PASS**. Alter aber vollständiger Plan wird von der Originalprüfung genauso wie fehlender/defekter Plan gesperrt.

Simulation B: Die TATSÄCHLICHE Original-PSTE-Funktion readParkhausForMini() mit 1.034 synthetischen WP-Einträgen, Original-PSTE-Plan und Editorial als vollständig getestet. Bei technisch intaktem historischen, aber nicht aktuellem PSERC-Plan entsteht der REALE Fehlertyp PSERC_PLAN_NOT_PROVEN_COMPLETE; 1.034 WordPress-Einträge sind vorhanden, dennoch kein Export.

Simulation C: Rein lokale QA-Kopie derselben schon bestehenden Funktion; nur im bereits aktiven plan-freien KISS-Modus wird ein nachweislich originalsignierter, vollständig lesbarer historischer PSERC-Plan als alte BELEGUNGSINFORMATION akzeptiert, auch wenn seine aktuelle Produktions-Abhängigkeit nicht mehr stimmt. Keine neue fachliche Entscheidung. Prüfung der Header-Unterschrift, Vollständigkeit ALLER erwarteten Datensätze und der zweiten unveränderten Lesung bleibt zwingend.

QA-Kandidat: alter intakter PSERC-Plan => 1.035 Einträge (1.034 WP + 1 historischer Planplatz), complete=true. Fehlender oder manipulierter Header => Sperre bleibt. Während der Lesung veränderter Plan und fehlender Einzeldatensatz => Sperre bleibt. **6/6 zusätzliche 1034er-Gesamtproben PASS**, Syntaxprüfung PASS. Alle Simulationszustände sind synthetisch, WordPress/PPM wurde NICHT real verbunden. Keine Plugin-ZIP ausgegeben.

**Die echte WP-Diagnose trennt alt, fehlend und manipuliert nicht. Die Simulation beweist also noch NICHT, welche dieser drei Ursachen bei oliver-beil.de vorliegt.** Eine pauschale Freigabe/Bypass wäre unsicher. Nächster korrekter Schritt: vorhandenen aktiven PSERC-Header und vorhandene Plan-Datensätze nur LESEN; prüfen ob gültig und nur veraltet oder tatsächlich unvollständig. Erst dann die passende minimale Korrektur in einem einzigen bestehenden Weg freigeben.

Lokale Original-Gegenprobe: /mnt/data/simuliere_pserc_mini_20261115.php und /mnt/data/mini_ps_sim_20261115/full_1034_original_parkhouse.php, QA-only Patch /mnt/data/mini_ps_sim_20261115/QA_ONLY_HISTORICAL_PSERC_READER.patch, Ergebnis /mnt/data/mini_ps_sim_20261115/SIMULATION_ERGEBNIS_20261115.json. Diese lokalen Pfade sind kein öffentliches Installationsartefakt.

release_allowed=false.