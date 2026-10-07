# HOBBYRAUSCH – SEO_KATEGORIEN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-07
STATUS: V1.12 TECHNISCHE BASIS VORHANDEN / V2-BEWERTUNGSVERTRAG GEBUNDEN / BATCH 001 AUSGEFÜHRT / EVIDENZLÜCKEN OFFEN / KEIN NEUER LIVE-RELEASE

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
- Buchbinden = FIT / HOBBY_HUB aus vorhandener Pilotevidenz, aber noch PARTIAL wegen offener Leaf-/Ownership-Evidenz;
- Treibholz sammeln = IN_SCOPE / Sammeln / EDITORIAL, aber ARTICLE_ONLY vs. EDITORIAL_TOPIC noch offen;
- keine automatische Promotion aus DIRECT/ASSISTED;
- 0 Zielbaum-Writes zulässig.

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
- 13–15 Split-Prüfung;
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

`HD001_V2_BATCH001_EVIDENCE_INCOMPLETE_MASTER_NOT_ASSESSED`

Der Bewertungsvertrag ist jetzt eindeutig gebunden und Batch 001 ist real ausgeführt.

Der aktuelle Blocker ist nicht mehr die fehlende Regeldefinition, sondern fehlende Evidenz:
- 15/16 Batch-Fälle sind noch nicht vollständig bewertet;
- Content Capacity fehlt für fast alle;
- finale Ownership fehlt;
- bei fünf Kandidaten fehlt bereits belastbare Scope-/Weltevidenz.

Solange Batch 001 nicht belastbar durch die Gates läuft, wird die 841er Gesamtbewertung nicht gestartet.

## EXAKT EINE NEXT ACTION

Für die 16 Kandidaten aus `HOBBY_MASTER_V2_BATCH_001_RESULTS_20261007.json` die fehlende Scope-/Content-Capacity-/Ownership-Evidenz erzeugen und denselben Batch anschließend erneut durch `HOBBY_MASTER_V2_ASSESSMENT_RULES_20261007.json` laufen lassen.

Dabei:
- DataForSEO nur für SEO-/Nachfrage-/Intent-Evidenz;
- keine Struktur aus Suchvolumen ableiten;
- keine unbekannten Werte schätzen;
- nur vollständig belegte `ASSESSED`-Fälle freigeben.

Noch keine Pluginänderung.
Noch kein WordPress-Sync.
Noch kein V1.12-Deployment.
