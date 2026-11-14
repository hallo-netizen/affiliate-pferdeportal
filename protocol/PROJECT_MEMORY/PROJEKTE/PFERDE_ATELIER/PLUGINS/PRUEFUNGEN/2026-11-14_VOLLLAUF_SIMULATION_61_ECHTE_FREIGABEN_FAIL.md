# Texterstellung: Vollworkflow-Simulation mit tatsächlichen 61 Altaufträgen – 14.11.2026

**Gesamtergebnis: FAIL – NICHT freigeben.** Dieser Nachweis ist eine ausgeführte Offline-Simulation der gelieferten 0.4.1-Test-ZIP; kein echter WordPress-/DataForSEO-/K0-Serverlauf.

## Exakte Quelle
- Installierte Test-ZIP: `Texterstellung_0.4.1_Planfrei_NUR_TESTWORDPRESS.zip`, SHA-256 `6dd3033029b4c49f0bb277ffba28e949c82fc1f52f73a15af13e31f809a6bcf1`; 172 Dateien, 116 PHP. Der ausführende Test hat die originale `texterstellung.php` aus genau dieser ZIP bytegleich eingelesen.
- Tatsächlicher 61er-Zustand: hochgeladene `texterstellung-diagnose-20261114-135822.json` von der isolierten Testseite; historisches Original-MINI `pferdeatelier-mini-ergebnisse-20261109-074817.json` mit 100 Quelltiteln.
- Unabhängige Original-SEO-Einmalentscheidung `pferdeatelier-seo-einmalentscheidung-20261109.json` tatsächlich gelesen: **87 Entscheidungen (61 FREI, 20 BELEGT, 6 KLÄRUNG)**. Unter den 61 FREI: **0** mit `category_slug`, **0** mit `article_type`, **0** mit `canonical_article_id`, **0** mit `plan_slot`; dagegen **61** mit genehmigtem Titel. Keine Werte erfunden.
- Die 61 wirklichen Auftrags-IDs der Diagnose wurden anhand derselben Pluginfunktion rekonstruiert. Alle 61 Titel passen zu den Original-MINI-Ergebnissen.

## Tatsächlich ausgeführte Tests (keine geschönten Erfolgszahlen)
| Fall | Kontrollen | Ergebnis |
|---|---:|---|
| 61 echte Aufträge aus Diagnose, Doppelübernahme, Originalfreigabe-Gate, Titel-/K0-Gate, Draft-Zähler, Identitäten | 16/16 erwartungsgemäße Prüfungen | **FAIL des Produktionsablaufs: 61 gehalten, 0 K0, 0 Entwürfe** |
| 20 **synthetisch vollständige** Quittungen: Titel, K0-13+7, Entwurfimport, Doppel-/Falschimport und Publish-Sperren | 25/25 | PASS nur mit vorbefüllten künstlichen Metadaten |
| 20 synthetische Themen über echte originale `PSTE_Mini_Workflow::acceptSingleOwnerSeoDecisions` → Titel → 13+7 → Entwürfe | 27/27 | PASS mit künstlicher Quellstruktur und nachgebildetem WordPress |
| Deaktivierte zusätzliche Planungsaktionen | 15/15 | PASS in WordPress-Hook-Simulation |
| Testsite-Start, bestätigter Start, altes Plugin aktiv | 3/3 | PASS in Startsimulation |

**86/86 Prüfaussagen korrekt, aber Gesamtziel nicht erreicht.** Erfolgreiche Kontrollaussagen über Sperren sind **keine** Freigabe des Nutzworkflows.

**Nicht simuliert bzw. nicht belegbar:** echte DataForSEO- und Google-People-Also-Ask-Aufrufe, echte K0-81-Regel-Texterstellung, echter WordPress-Backend-/Datenbank-/PPM-Serverprozess. Bei den 20 Testartikeln bestehen die Texte aus QA-Platzhaltern. Für die 61 Fälle gab es deshalb **keinen** Voll-Lauf bis zu echten WP-Entwürfen.

## Bestätigte Ursache und konkrete Anschlussarbeit
Die alte SEO-Entscheidungsdatei ist kein vollständiger Produktionsauftrag. Der neue Kandidat holt die zur Produktion nötigen Kategorie-, Artikelart- und Identitätsfelder aus dieser Datei statt aus **den tatsächlichen Original-Quellbeständen**. Die ursprünglichen FREI-Themen bleiben korrekt gesperrt, aber der neue Workflow kann sie so nie ausgeben.

**Nächster Produkt-Fix, keine Zusatzprüfungsschleife:** Einen originalgetreuen Leseabgleich der bereits vorhandenen PSTE-Quelldatensätze und Auftragsbindungen in die Altübernahme einfügen. Keine neue SEO-Entscheidung und keine künstlichen Kennungen. Dann exakt dieselbe 61er-Prüfung erneut ausführen. Nicht vor erfolgreichem echtem Datentest als komplett markieren.

## Reproduzierbarer Beleg
Prüfarchiv (nur Benutzerkontext, wegen Diagnose-/Keyworddaten nicht in das öffentliche GitHub gestellt): `Texterstellung_Vollworkflow_Simulationsbeweis_20261114.zip`, SHA-256 `1f44416f2f69f063360ef3667220b489912e3bdfe31e57cd03ff4a672c97e5f7`. Enthält die exakt gelieferte Installations-ZIP, die Benutzerdiagnose, das historische MINI-Original, fünf PHP-Prüfskripte, `verify_full_workflow.py` sowie den JSON- und Klartextbeleg. Teststart mit `python3 verify_full_workflow.py` und PHP >= 8.1. Es wurde **kein Produktcode geändert**.
