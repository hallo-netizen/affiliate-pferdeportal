# HOBBYRAUSCH – SEO_KATEGORIEN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-07
STATUS: V1.12 TECHNISCHE BASIS VORHANDEN / V2-REGELN 1.1 PRO LEAF + ZUSAMMENFASSUNG GEBUNDEN / BATCH-001-FACHVORPRÜFUNG FERTIG / DATAFORSEO-LIVEABGLEICH OFFEN / KEIN LIVE-RELEASE

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

Verbindlich seit Regelversion 1.1:
- Gesamtzahl der Artikel eines Hobbys reicht NICHT;
- jede unterste Kategorie muss separat 5–12 echte, unterschiedliche Artikelintents tragen;
- 0–3 = keine eigene Leaf-Kategorie;
- 4 = Ausnahmeprüfung;
- 13–14 = Split-Prüfung;
- ab etwa 15 = Split erforderlich.

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
- 5–12 Ziel;
- 4 Ausnahme;
- 13–14 Split-Prüfung;
- >15 nur explizite Ausnahme.

Hobby-Hub:
- 3–6 Ziel;
- 7–8 Split-/Macro-Prüfung;
- >8 grundsätzlich Macro/Split.

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

## Technischer V1.12-Stand

HD-001 V1.12.0 ist als lokale technische Basis vollständig POS/NEG getestet.
Der technische Stand beweist Zielbaum-Sync, Idempotenz, Rollback, Cross-Pillar-Gates und generisches Profilverhalten.

Er ist KEIN aktueller Live-PASS und KEIN Installationsauftrag für den fachlich fortgeschriebenen Hobby-Depot-Baum.

Grund:
Die V2-Größen-/Rollenlogik liegt zeitlich danach und das V1.12-Hobby-Profil enthält noch die inzwischen verworfene zusätzliche `Hobbywelten`-Parentebene.

## ERSTER OFFENER BLOCKER

`HD001_V2_BATCH001_HD001_ASSESSMENT_RUN_NOT_BOUND`

Die fachliche Vorprüfung für alle 16 Testhobbys ist vorbereitet.
Die echten Leaf-Zahlen dürfen aber erst nach realem DataForSEO-Abgleich festgeschrieben werden.

Bereits real belegt:
- Buchbinden besitzt vorhandene echte DataForSEO-Evidence;
- diese reicht nach der strengeren V2-Regel noch NICHT für einen endgültigen Hub-PASS.

Für die übrigen Testhobbys liegen keine belastbaren aktuellen DataForSEO-Ergebnisse im geprüften Bestand vor.

Der exakte Request ist vorbereitet.
Der DataForSEO-Zugang ist Bestandteil des bestehenden HD-001-WordPress-Plugins. Der externe Zugang ist daher KEIN Blocker.
Offen ist ausschließlich die Bindung des neuen V2-Batch-Requests an einen read-only Bewertungsmodus in HD-001. Dieser Modus nutzt den vorhandenen APKW_DataForSEO-Client und die bereits in WordPress hinterlegten Zugangsdaten.

## EXAKT EINE NEXT ACTION

`HOBBY_MASTER_V2_BATCH_001_DATAFORSEO_REQUEST_20261007.json` über den bestehenden authentifizierten Hobby-Depot-DataForSEO-Weg ausführen.

Danach:
- Synonyme und doppelte Intents zusammenführen;
- CORE / EDITORIAL / DIRECTORY Ownership prüfen;
- jede unterste Kategorie separat neu zählen;
- kleine valide Themen auf sinnvolle Zusammenfassung prüfen;
- denselben 16er Batch erneut durch Regelversion 1.1 laufen lassen.

Noch keine Pluginänderung.
Noch kein Zielbaum-Delta.
Noch kein WordPress-Sync.
Noch kein V1.12-Deployment.
