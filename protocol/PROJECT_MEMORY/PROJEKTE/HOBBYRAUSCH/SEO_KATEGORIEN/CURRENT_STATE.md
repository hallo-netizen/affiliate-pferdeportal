# HOBBYRAUSCH – SEO_KATEGORIEN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-07
STATUS: V1.12 TECHNISCHE BASIS VORHANDEN / HOBBY_MASTER V2 VORGESCHALTET / ACHT WELTEN ALS CORE-EBENE 1 FEST / GESAMTBEWERTUNG OFFEN / KEIN NEUER LIVE-RELEASE

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

Die Rohliste ist Candidate Pool/Provenienz, keine Taxonomie.

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

Die 841 kanonischen Kandidaten sind noch nicht vollständig nach:
- Scope;
- Identität/Alias;
- Größenklasse;
- Content Capacity;
- Publikationsrolle;
- 3-Säulen-Ownership

bewertet.

Ohne diese Bewertung gibt es kein belastbares V2-Zielbaum-Delta.

## EXAKT EINE NEXT ACTION

Die maschinenlesbaren Bewertungsregeln auf einen kontrollierten ersten HOBBY_MASTER-Batch anwenden und die Ergebnisse gegen das Rollen-/Größenmodell prüfen.

Erst danach:
- Fehlklassifikationen korrigieren;
- Gesamtmaster batchweise bewerten;
- V1.12-Zielbaum als Delta fortschreiben;
- die acht Welten auf CORE-Ebene 1 korrigieren;
- danach Plugin-/WordPress-Sync erneut komplett POS/NEG testen.
