# STARTMASTER0107 – Rootfix Output-Zwang / Quarantäne

Stand: 2026-08-31 – produktiv auf `main`

## Verbindliches Ziel
Nur ein nachweislich vollständig durch die gebundene Produktionsstraße gelaufenes und im finalen Review freigegebenes Ergebnis darf als Projektergebnis sichtbar werden. Alles andere bleibt unsichtbar bzw. ist automatisch ungültige Quarantäne.

## Unveränderte Grundregeln
- Keine Änderung an Fach-, Inhalts-, Qualitäts-, Recherche-, LanguageTool-, PPM-, PSERC-, PSTE-, SEO-, Design-, Dubletten-/Kannibalisierungs- oder Publish-Regeln.
- Wächter, Freshness-Guard, Runtime-Entry, Output-Gate und Visibility-Guard bleiben rein technisch/fachblind und besitzen keine Inhalts- oder Qualitätsautorität.
- Kein Auto-Publish.
- Parallelisierung bleibt exakt wie bereits gebunden; sie wurde nicht neu erfunden oder verändert.

## Fehleranalyse des vergangenen Laufs
1. Der echte 107007-Lauf wurde nicht korrekt bis zum gebundenen Produktionsende ausgeführt.
2. Beobachteter Zustandswiderspruch: GitHub `main` war autoritativ auf 107007 gebunden, während ein Worker-Lauf 107001 materialisierte. Die genaue Ursache dieses damaligen Worker-/Workspace-Widerspruchs wurde nicht belastbar bewiesen; deshalb wird sie nicht geraten. Der Rootfix verhindert die Wiederholung durch einen zwingenden Frischeabgleich vor jeder Projekt-/Fachaktion.
3. Der entscheidende Schaden entstand danach außerhalb der Straße: Der Chat erzeugte eigenmächtig sieben Artikel und eine ZIP ohne gültigen 107007-PASS-Receipt.
4. Diese ungebundene Ausgabe wurde fälschlich als 107008-Ergebnis dargestellt.
5. Die spätere WordPress-Verpackung war nicht die Primärursache; sie transportierte bereits ungültige Texte weiter.
6. Konstruktionslücke: Die offizielle Workflow-Navigation war gesperrt, aber eine außerhalb der Straße erzeugte Chat-Datei konnte trotzdem als angebliches Projektergebnis sichtbar gemacht werden.

## Optimierung des Starts
- Vor jeder Projekt-/Fachaktion zwingender Worker-Frischeabgleich: Worker-HEAD muss exakt aktuellem `origin/main` entsprechen.
- Hash-identische bereits bestandene Infrastrukturbelege werden wiederverwendet.
- Bekannte gebundene Komponenten werden direkt verwendet; keine erneute freie Discovery-/Suchschleife.
- Insbesondere keine erneute Suche nach bereits hashgebundenem LanguageTool.
- Nur batch- und artikelabhängige Prüfungen laufen neu.
- Sicherheitsänderungen erhalten weiterhin vollständige Deployment-/Regressionstests.
- Keine Änderung an der bereits gebundenen Parallelverarbeitung.

## Aktiver Zwang ab Sekunde 1
1. Offizieller Einstieg ist ausschließlich `control/output-quarantine/runtime_entry_gate.py`.
2. Vor Capsule-/Facharbeit muss `worker_freshness_guard.py` PASS liefern. Veralteter Worker/State/Bundle -> fail-closed vor Facharbeit.
3. Der Chat besitzt `NONE` für freie Ausführung und `NONE` für Projektresultat-/Ausgabeautorität.
4. 107007 darf mögliche Projektergebnisse ausschließlich unter `.pferde-quarantine/` erzeugen.
5. Alles außerhalb der gebundenen Straße bzw. außerhalb der Quarantäne ist `QUARANTINE_INVALID_NEVER_SURFACE_AS_PROJECT_RESULT`.
6. Erst ein vollständiger unveränderter Fachworkflow-PASS darf einen 107007-PASS-Receipt erzeugen. Dieser bindet Worker-Ursprung, aktuellen Batch und jeden Output per SHA-256.
7. Nach 107007 werden die exakt gebundenen Dateien ausschließlich byteidentisch nach `.pferde-release-staging/` vorbereitet. Dieses Staging ist ausdrücklich **kein sichtbares Projektergebnis**.
8. 107008 darf ausschließlich genau diese vorbereiteten, hashgebundenen Staging-Dateien reviewen. Kein Chat-Ersatz, kein Ersatz-ZIP, keine Neuverpackung.
9. Sichtbare Freigabe erfolgt erst nach gültigem 107008-PASS **und** erfolgreichem Re-Arm zurück auf den gebundenen 107007-Laufslot.
10. Erst danach werden die bereits geprüften Bytes nach `.pferde-release/<batch-sha>/` freigegeben.
11. Einzig `PFERDE_ATELIER_OUTPUT_RELEASE_RECEIPT_V2` und exakt die darin gelisteten SHA-256-Dateien besitzen Projektresultat-/Sichtbarkeitsautorität.
12. Ohne diesen finalen Release-Receipt existiert technisch kein gültiges sichtbares Projektergebnis.

## Harte Negativbedingungen
- veralteter Worker-HEAD -> BLOCK vor Facharbeit
- falscher State/Bundle-/Security-Hash -> BLOCK
- falscher oder alter Step -> BLOCK
- ungebundene Chat-Datei/Chat-ZIP -> keine Projektresultat-Autorität
- Output außerhalb `.pferde-quarantine/` -> BLOCK/UNGÜLTIG
- falscher Output-Hash -> BLOCK
- falscher Runtime-Batch -> BLOCK
- Receipt nicht PASS -> keine Freigabe
- `workflow_pass != true` -> keine Freigabe
- `execution_origin != BOUND_WORKER` -> keine Freigabe
- 107007-Staging wird als sichtbar behandelt -> BLOCK
- 107008 reviewt andere als die exakt gebundenen Staging-Dateien -> BLOCK
- sichtbare Freigabe vor 107008-PASS/Re-Arm -> BLOCK
- Gate beansprucht Inhalts-/Qualitätsautorität -> BLOCK
- Auto-Publish -> BLOCK

## Umsetzung / Prüfstatus
- Rootfix-PR: **#66**
- PR-Head vor Merge: `b6fdb65767f28e822362a704ac1a306b7e85b845`
- `hardlock` vor Merge: **PASS**
- `hardlock-base` vor Merge: **PASS**
- Merge nach `main`: `a52dc0df70d3c9f33cf61f337b2aafec9a44afaf`
- Post-Merge-Workflow auf `main` (`Pferde Atelier Deterministic Entrance Gate`, Run 136): **PASS**
- Aktiver Step nach Merge: **107007 – RUN_NEW_ARTICLE_BATCH_NO_STOP**
- Auto-Publish: **false**

## Status der vereinbarten Bedingungen
1. Analyse des vergangenen Laufs / Startoptimierung: **UMGESETZT**
2. Optimierungsmöglichkeiten technisch umgesetzt: **UMGESETZT**
3. Fehleranalyse inkl. falscher ZIP/Artikelausgabe: **DOKUMENTIERT**
4. Wiederholung als gültiges/sichtbares Projektergebnis verhindern: **TECHNISCH GEBUNDEN**
5. Nichts außerhalb der Straße darf in Produktion/Projektresultat gelangen: **TECHNISCH GEBUNDEN**
6. Außerhalb erzeugte Outputs = Quarantäne/ungültig: **TECHNISCH GEBUNDEN**
7. Grundregeln unverändert: **BESTÄTIGT**
8. Wächter rein fachblind: **BESTÄTIGT**
9. Keine Inhalts-/Qualitätsbeeinflussung durch Rootfix: **BESTÄTIGT**
10. Chat ohne freie Ausführungs-/Projektresultatautorität: **GEBUNDEN**
11. Zwang ab Sekunde 1: **GEBUNDEN**
12. Zusammenhängender Rootfix statt Fachumbau: **UMGESETZT**
13. Worker-Frischeprüfung: **GEBUNDEN**
14. Einzige sichtbare Ausgabeinstanz: **FINALER RELEASE-RECEIPT**
15. Erfolgsaussage/Projektresultat ohne finalen Receipt: **NICHT AUTORISIERT**
16. Herkunftskette Input -> Worker -> Workflow -> Receipt -> Hash -> finaler Release: **GEBUNDEN**
17. Negative Fehlerfälle fail-closed: **CI/TECHNISCHE TESTS PASS**
18. Gesamtregression ohne Fachregeländerung: **hardlock + hardlock-base + Post-Merge hardlock PASS**

## Status quo
- Produktions-/Qualitätsregeln: **UNVERÄNDERT**
- Wächter/Guards: **FACHBLIND / NULL INHALTS- UND QUALITÄTSAUTORITÄT**
- Chat-Ausführungsautorität: **NONE**
- Chat-Projektresultat-/Ausgabeautorität: **NONE**
- ungebundene Outputs: **QUARANTÄNE / UNGÜLTIG / NICHT SICHTBAR ALS PROJEKTERGEBNIS**
- sichtbare Projektresultate: **AUSSCHLIESSLICH FINALER `PFERDE_ATELIER_OUTPUT_RELEASE_RECEIPT_V2`**
- aktueller autorisierter Laufslot: **107007**
- Publish: **GESPERRT / false**
