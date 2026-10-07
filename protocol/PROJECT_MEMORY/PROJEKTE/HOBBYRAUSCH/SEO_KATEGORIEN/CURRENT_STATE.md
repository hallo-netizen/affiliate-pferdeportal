# HOBBYRAUSCH – SEO_KATEGORIEN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-07
STATUS: V1.12.1 READ-ONLY V2-BEWERTUNG LOKAL HARD PASS / REGELN 1.2 KONZEPTEXAKT / BATCH 001 IM WORDPRESS-PLUGIN GEBUNDEN / REALER DATAFORSEO-LAUF OFFEN / KEIN ZIELBAUM-WRITE

## Ziel

Zentraler Hobbybestand
→ HOBBY_MASTER V2
→ Scope-/Identitäts-/Größen-/Rollenprüfung
→ 8 geschützte Hauptwelten
→ variable Seitenhierarchie + Content-Kategorien + Magazin + HivePress
→ DataForSEO-SEO-Anreicherung
→ globale Ownership-Prüfung
→ WordPress/HivePress Soll/Ist-Sync
→ Frontend-Readback.

## Geschützte Grundstruktur

Drei Säulen:
- CORE = Hauptportal;
- EDITORIAL = Magazin;
- DIRECTORY = HivePress/Anbieter.

Acht Hauptwelten:
Gestalten / Fertigen / Technik / Forschen / Pflanzen / Tiere / Bewegen / Sammeln.

### Harte Ebenenregel

Die acht Hauptwelten sind die oberste fachliche CORE-Ebene.

`Hobbywelten` ist nur Übersicht/Ansicht/Einstieg und darf NICHT als struktureller Parent über den acht Welten stehen.

Das vorhandene V1.12-Profil mit `core:hub → core:world:...` ist deshalb nur Baseline/Evidence und muss im späteren Zielbaum-Delta korrigiert werden.

## Portfolio- und Navigationslogik

Ziel:
- wirtschaftliche Anker durch große bekannte Hobbys;
- stabiles Mittelfeld;
- Nischen als Longtail/SEO-Differenzierung;
- ohne Navigationsexplosion.

Bekanntheit/Monetarisierungsstärke sind Präsentations-/Prioritätsmerkmale, keine zweite Taxonomie.

Der interne Master darf groß sein.
Die sichtbare Navigation bleibt klein.
Beliebte Hobbys, ungewöhnlich, zuhause, günstig usw. sind Views auf dieselben kanonischen Owner.

## Hobby-Master V2

Persistente Bewertungsbasis:
`/hobby rausch/HOBBY_DEPOT_HOBBY_MASTER_V2_20261007.json`

Current-Zeiger:
`../KONZEPT/VORARBEITEN_HOBBYFINDER/HOBBY_MASTER_V2_CURRENT.md`

Bestand:
- 908 Rohzeilen;
- 844 exakte Namen;
- 841 kanonische Identitäten;
- 329 bestehende V1.12-Monetarisierungs-/CORE-Regeln migriert;
- 286 DIRECT;
- 43 ASSISTED;
- 512 UNKNOWN und weiterhin erhalten.
- zusätzlich 19 Research-Queue-Kandidaten, noch NICHT Teil der 841 Identitäten;
- davon Fotografie durch Pilotbefund für provisorischen Master-Intake vorbereitet, aber noch kein Zielbaumknoten.

Die Rohliste ist Candidate Pool/Provenienz, keine Taxonomie.

## Maschinenlesbare V2-Bewertung

Regelvertrag:
`HOBBY_MASTER_V2_ASSESSMENT_RULES_20261007.json`

Kontrollierter erster Lauf:
`HOBBY_MASTER_V2_BATCH_001_RESULTS_20261007.json`

Research-Queue-Intake:
`HOBBY_MASTER_V2_RESEARCH_INTAKE_20261007.json`

Vorbereitetes Master-Intake-Delta:
`HOBBY_MASTER_V2_INTAKE_DELTA_001_20261007.json`

Batch 001:
- 16 reproduzierbar ausgewählte Master-Identitäten;
- 16/16 ID-Eindeutigkeit PASS; davon 4 aktuelle Alias-/Kanonikbindungen bestätigt, 12 semantische Identitätsprüfungen offen;
- 2 Scope-Fälle fachlich bestätigt;
- 9 Scope-Fälle nur provisional;
- 5 Scope-Fälle benötigen Evidenz;
- Buchbinden = bestehender Live-/Technikpilot bleibt erhalten, aber V2-Hub-PASS wieder OFFEN: echte DataForSEO-Evidence liefert aktuell 4 / 5 / 3 / 4 distinct Intent-Gruppen in den vier aktiven Leafs; nur Ausrüstung liegt bereits im V2-Ziel 5–12;
- Treibholz sammeln = IN_SCOPE / Sammeln / EDITORIAL, aber ARTICLE_ONLY vs. EDITORIAL_TOPIC noch offen;
- keine automatische Promotion aus DIRECT/ASSISTED;
- 0 Zielbaum-Writes zulässig.

## V2-Korrektur: jede unterste Kategorie einzeln prüfen

Verbindlich seit Regelversion 1.2:
- Gesamtzahl der Artikel eines Hobbys reicht NICHT;
- jede unterste Kategorie muss separat 5–12 echte, unterschiedliche Artikelintents tragen;
- 0–3 = keine eigene Leaf-Kategorie;
- 4 = Ausnahmeprüfung;
- 13–14 = oberhalb des Idealbereichs / prüfen;
- ab etwa 15 = Teilung prüfen.

Kleine valide Hobbys dürfen gemeinsam über Übersichten, gemeinsame Leafs oder Magazin-Cluster sichtbar werden.
Ihre kanonischen Hobby-Identitäten bleiben trotzdem getrennt.

Fachvorprüfung:
`HOBBY_MASTER_V2_BATCH_001_SUBJECT_PREFLIGHT_20261007.json`

DataForSEO-Auftrag:
`HOBBY_MASTER_V2_BATCH_001_DATAFORSEO_REQUEST_20261007.json`

Konzeptaudit:
`HOBBY_MASTER_V2_CONCEPT_AUDIT_20261007.md`

## Rollen- und Größenlogik

Publikationsrollen:
- ORIENTATION_UNIVERSE;
- HOBBY_HUB;
- EDITORIAL_TOPIC;
- ARTICLE_ONLY;
- FINDER_ONLY;
- OUT_OF_SCOPE.

Leaf:
- unter 4 zusammenlegen / keine eigene Leaf-Kategorie;
- 4 Grenzfall;
- 5–12 Idealbereich;
- 13–14 oberhalb des Idealbereichs / prüfen;
- ab etwa 15 Teilung prüfen.

Hobby-Hub:
- 3–6 Zielbereich;
- 7–9 oberhalb des typischen Bereichs / prüfen;
- ab etwa 10 Macro-/Split-Prüfung.

## DataForSEO-Vertrag

DataForSEO darf:
- Nachfrageband;
- Primärkeyword;
- Synonyme;
- Longtail-Tiefe;
- Keyword-/Intent-Überschneidung

belegen bzw. innerhalb definierter Kandidaten optimieren.

DataForSEO darf NICHT bestimmen:
- Hauptwelt;
- Parent;
- structural_role;
- neue Zwischenkategorie;
- CORE-Promotion.

## Monetarisierung

Monetarisierung beeinflusst CORE-Priorität, Sichtbarkeit und kommerzielle Tiefe.

Nicht monetarisierbare valide Hobbys werden NICHT gelöscht.
Sie bleiben EDITORIAL-/ARTICLE-/FINDER-Kandidaten.

## Dubletten und Ownership

Prüfung gemeinsam über CORE / EDITORIAL / DIRECTORY.

Treibholz + Treibholz sammeln = eine Identität.

Pro primärem Intent genau ein SEO-Owner.
Andere Säulen dürfen Relation/Filter/Verweis sein, keine konkurrierende Zielseite.

## Technischer V1.12/V1.12.1-Stand

HD-001 V1.12.0 bleibt die vollständig getestete technische Zielbaum-Baseline.

Darauf wurde V1.12.1 als reiner V2-Bewertungskandidat gebaut:
- WordPress-Backend-Unterseite `Kategorien → V2-Hobbybewertung`;
- gebündelter kontrollierter Batch 001;
- 16 Hobbys;
- 34 vorgeschlagene unterste Kategorien;
- 263 vorgeschlagene Artikelintents;
- exakt 1 DataForSEO Keyword-Overview-Aufruf;
- DataForSEO-Core-Keyword-Dedupe;
- Batch-übergreifende Ownership-Overlap-Prüfung;
- 0 WordPress-/HivePress-Strukturwrites;
- alter V1.12-Zielbaum-Runner in diesem Kandidaten deaktiviert.

Lokales V1.12.1-Artefakt:
`HD001_V1.12.1_HOBBY_MASTER_V2_READONLY_ASSESSMENT_HARDPASS.zip`

SHA-256:
`959bc80217aac9b90ac107e6b315908b084704d09777ae9be990c2825245d33d`

Lokaler Prüfstand:
- PHP-Lint 59/59 PASS;
- Legacy Regression 270/270 PASS;
- V1.12 Positiv/Negativ PASS;
- realer 908/844/841-Lauf PASS;
- neue V2-Grenz-/Negativtests PASS;
- 0 Strukturwrites im Bewertungslauf PASS.

V1.12.1 ist KEIN Zielbaum-Deployment und noch KEIN Live-PASS.

Grund:
Die V2-Größen-/Rollenlogik liegt zeitlich danach und das V1.12-Hobby-Profil enthält noch die inzwischen verworfene zusätzliche `Hobbywelten`-Parentebene.

## ERSTER OFFENER BLOCKER

`HD001_V2_BATCH001_WORDPRESS_DATAFORSEO_RUN_PENDING`

Der read-only Bewertungsweg ist jetzt technisch im Plugin umgesetzt und lokal hart geprüft.

Offen ist nur noch der reale DataForSEO-Lauf im echten Hobby-Depot-WordPress:
- Plugin V1.12.1 installieren;
- `Kategorien → V2-Hobbybewertung` öffnen;
- gebündelten Batch 001 kostenlos vorprüfen;
- exakt den angezeigten EINEN DataForSEO-Aufruf bestätigen;
- Ergebnis-JSON herunterladen.

Der Lauf schreibt keine Kategorien und synchronisiert keinen Zielbaum.

## EXAKT EINE NEXT ACTION

Das exakte V1.12.1-ZIP in Hobby Depot installieren und dort den gebündelten Batch 001 über `Kategorien → V2-Hobbybewertung` ausführen.

Danach:
- Ergebnis-JSON gegen Regelvertrag 1.2 prüfen;
- echte distinct Artikelanzahl je unterster Kategorie bewerten;
- mögliche Zusammenfassung kleiner Themen prüfen;
- Ownership-Konflikte klären;
- erst danach den 841er Master weiter bewerten.

Noch kein Zielbaum-Delta.
Noch kein Kategorien-Sync.
Noch kein alter V1.12-Zielbaum-Refresh.
