# HAB & BEWAHR – SICHERHEITSGLOSSAR – KONZEPTENTWURF
**Status: WIP / zur Entscheidung vorgelegt, keine Live-Freigabe.** Dokument ist ein Konzept, KEINE Current-Autorität. Der jeweils verbindliche Projektstand bleibt in `DESIGN/CURRENT_STATE.md`.

## Anforderung und Vergleich
- Nutzerhinweis 14.10.2026: `/glossar/` zeigt auf realer Website nichts; Ursache LIVE noch nicht verifiziert. Release 0.1.7 enthält tatsächlich `data/glossary.json` mit 100 dreiteiligen Einträgen (Term, 6–19 Wörter Definition, Welt-Schlüssel), `includes/glossary.php` und PHP-Rewrite auf `/glossar/`. Vorherige Browser-Simulation beweist **nicht** funktionierenden WordPress-Livepfad.
- Pferde-Atelier hat im `/journal/` die Rubrik „Wissen & Nachschlagen“ mit Teaser zu „Glossar – Wichtige Pferdebegriffe einfach und verständlich erklärt“. Hieraus den eigenständigen redaktionellen Wissensbereich übernehmen; Layout-/Interaktionsidee als Referenz, NICHT ohne Code-Audit Komponenten kopieren. Die konkrete Glossar-Landingpage von Pferde-Atelier war im Web-Review noch nicht zuverlässig erreichbar; über ihre interne Gestaltung kann man deshalb noch keine detaillierte 1:1-Beobachtung behaupten.
- Zentrales Prinzip: Design weitgehend gemeinsam/nach Referenz, **inhaltlich eigene Sicherheitsbegriffe**, Farben, Typografie und Links Hab & Bewahr. Keine siebenfachen Hauptnavigationselemente; Portalhauptnavigation bleibt sechs Welten. Glossar über „Magazin / Wissen & Nachschlagen“ + Footer + interne Fachartikel zugänglich.

## Zielprodukt (KISS + SEO)
**Stufe 1: eine starke native WordPress-Übersichtsseite `/glossar/`.**
- HTML serverseitig abrufbar, HTTP 200, kanonisch, WordPress-SEO-Plugin für Title/Meta; keine alleinige Rewrite-Sonderroute mehr. Seitentitel „Sicherheitsglossar – Begriffe einfach erklärt“.
- Suchfeld (browserlokal), alphabetische A–Z-Filter, optional Weltfilter, je Begriff 1–3 Sätze vollständige korrekte Erklärung. „Mehr dazu“ zu vorhandenen authentischen Themen-/Artikelzielen, keine erfundenen URLs. Alle Begriffe auch ohne JS im HTML, Suche progressive enhancement.
- Zu jedem Begriff eine stabile ID, Lemma, Synonyme/Schreibvarianten, Kurzdefinition, Themenwelt, mögliche Related-Terms, Source/Norm, Prüfdatum, Redaktionsstatus, relevanter Hub-/Artikelbezug, Flag `has_substantive_detail`. Fachliche Details zu Schutzklassen/Normen nur nach Quellenkontrolle.
- Kein Wertlos-Content; Qualitätsgate (verständlich, korrekt, eindeutige Unterscheidung, Quelle wo relevant, passende interne Links), Dublettenprüfung, keine generischen Massenbegriffe.

**Stufe 2: separate URL `/glossar/{slug}/` nur selektiv.**
- Eigene indexierbare URL nur für Begriffe mit eigenständiger Suchintention und hinreichendem Mehrwert, z. B. RC2, Widerstandsklassen, Perimeterschutz, Rückstauebene, Lichtbogen-Fehlerstromschutz. Für Einträge ohne substanzielle Vertiefung KEINE 100 dünnen WordPress-Unterseiten; nur Definition auf der indexierbaren Glossarübersicht.
- Vertiefungsschema: Was bedeutet es? Warum für Privathaushalte relevant? Was wird häufig verwechselt? Welche Sicherheitsschranken oder Grenzen gelten? Fachbezug und belegbare Quellen; verwandte Begriffe; passend verlinkte Ratgeber. Kein Ersatz/SEO-Kannibalisierung für ausführliche How-to-/Produktartikel.
- Linkregeln: von einzelnen Ratgebern nur gezielt Glossarlinks für unklare Fachbegriffe, kein globales String-Replacement / kein ungeprüftes SEO-Autolinking. Von Glossar zu relevanten Ratgebern, Endkategorien und Nachbarbegriffen. Keine falschen Linkziele.

## Technische Entkopplung
- Fachinhalt gehört NICHT in PHP-Layout des Designplugins, sonst bei Updates gefährdet und nicht sinnvoll parallel redigierbar. Redaktionelles Glossar **als separater versionierter Datenbestand** pflegen (zuerst Datei/Repo; bei Livepublikation natives WordPress-Content-Objekt oder – bei großem Umfang – EIN klar begrenztes dediziertes Glossar-Plugin/Content-Modul). Keine Installation im WIP ohne Freigabe.
- Designplugin liefert nur gemeinsame CSS-/Template-Darstellung; Content-Schicht verwaltet Texte, IDs, Prüfstände, Publikationsstatus. Beim späteren separaten Plugin muss das v0.1.7-`/glossar/`-Routing aus der Designsuite konfliktfrei ausgelöst/abgelöst werden, keine zwei Route-Owner.
- Keine Crons, keine DB-Strukturänderung an Kategorie-Workflow, keine automatischen WordPress-Kategoriewrites, Ressourcen nur bei Glossar-Besuch laden.
- Alle vorbereiteten Textänderungen können parallel erfolgen, ohne Live-Veröffentlichung. Große Batches erst nach Qualitätsgate; nur freigegebene Begriffe erscheinen live.

## Aktueller Bestand und redaktionelle Routine
- 100 Kurzbegriffe existieren in v0.1.7-`data/glossary.json` – **Entwurfsbestand**, keine redaktionelle Freigabe/Quellenprüfung nachgewiesen.
- Erst Bestand sichten: Fachbegriff / Synonyme / Duplikate / Normbezug / korrektes Sicherheitsgebiet / Risiko veralteter Standards. Nicht 100 Term-Seiten automatisch veröffentlichen.
- Danach in Paketen z. B. 20–30 Begriffe pro redaktionellem Durchgang recherchieren, fachlich plausibilisieren, redigieren und als einzelnes unabhängiges Review-Produkt ablegen (ID, Quellen, Status WIP/REVIEWED/PUBLISHED).
- Themencluster: Einbruch, Diebstahl, Vandalismus, Wasser/Feuchte, Feuer/Gase, Wetter/Natur, Technik/Ausfall; Querschnitt Normen, Versicherungen, Schadendokumentation, Alarmierung/Datenschutz. Jede Definition mit praktischer Nutzerfrage / Bedeutung.
- SEO-Bewertung pro Begriff separat. Keine Ranking-Versprechen. Google empfiehlt nutzerzentrierte eigenständige Inhalte und warnt vor massenhaft dünn generierten Seiten (Google Search Central).
- **Einzige fachliche NEXT ACTION im Glossar-Unterkonzept (nicht globale DESIGN NEXT ACTION):** Die vorhandenen 100 Term-Definitionen offline nach Schema und Qualität sichten; daraus priorisierten Redaktionsplan und Entwurf für native WordPress-Übersichtsseite erstellen. Live-Route `/glossar/` als separaten Fehler erst anhand echter WP-Antwort prüfen, nicht raten.
