# HOBBYRAUSCH – SEO_KATEGORIEN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-07
STATUS: 3-SÄULEN-ZIELBAUM V1.12 ALS BASIS VORHANDEN / HOBBY_MASTER V2 VORGESCHALTET / GESAMTBEWERTUNG OFFEN / KEIN NEUER LIVE-RELEASE

## Ziel

Konzept + zentraler Hobbybestand → Scope-/Größen-/Rollenprüfung → 8 geschützte Hauptwelten → variable Seitenhierarchie + Content-Kategorien + Magazin + HivePress → globale Ownership-Prüfung → WordPress/HivePress Soll/Ist-Sync → Readback.

## Geschützte Grundstruktur

Acht Hauptwelten:
Gestalten / Fertigen / Technik / Forschen / Pflanzen / Tiere / Bewegen / Sammeln.

Drei Säulen:
- CORE = Hauptportal;
- EDITORIAL = Magazin;
- DIRECTORY = HivePress/Anbieter.

Die acht Welten werden im ersten neuen Integrationslauf nicht neu erfunden.

## Neuer vorgeschalteter Hobby-Master

Persistente Bewertungsbasis:
`/hobby rausch/HOBBY_DEPOT_HOBBY_MASTER_V2_20261007.json`

Current-Zeiger:
`../KONZEPT/VORARBEITEN_HOBBYFINDER/HOBBY_MASTER_V2_CURRENT.md`

Bestand:
- 908 Rohzeilen;
- 844 exakte Namen;
- 841 kanonische Identitäten nach aktuellen Alias-Merges;
- 329 bestehende V1.12-Monetarisierungs-/CORE-Regeln migriert;
- 286 DIRECT;
- 43 ASSISTED;
- 512 UNKNOWN und weiterhin erhalten.

Die Rohliste ist weiterhin nur Provenienz/Candidate Pool und keine Taxonomie.

## Neue Rollen- und Größenlogik

Mögliche Publikationsrollen:
- ORIENTATION_UNIVERSE;
- HOBBY_HUB;
- EDITORIAL_TOPIC;
- ARTICLE_ONLY;
- FINDER_ONLY;
- OUT_OF_SCOPE.

Leaf-Kategorie:
- 5–12 Beiträge Ziel;
- 4 nur Ausnahme;
- 13–15 Split-Prüfung;
- >15 nur explizite Ausnahme.

Hobby-Hub:
- 3–6 tragfähige Leafs Ziel;
- 7–8 Split-/Macro-Prüfung;
- >8 grundsätzlich Macro/Split.

## DataForSEO-Vertrag

DataForSEO darf:
- Nachfrageband;
- Primärkeyword;
- Synonyme;
- Longtail-Tiefe;
- Keyword-/Intent-Überschneidung

belegen.

DataForSEO darf NICHT:
- Hauptwelt;
- Parent;
- structural_role;
- neue Zwischenkategorie

selbst bestimmen.

SEO-Evidenz unterstützt die Größenprüfung, ist aber keine Taxonomieautorität.

## Monetarisierung

Monetarisierung beeinflusst CORE-Priorität und kommerzielle Tiefe.

Nicht monetarisierbare gültige Hobbys werden NICHT gelöscht.
Sie bleiben EDITORIAL-/ARTICLE-/FINDER-Kandidaten.

## Dubletten und Ownership

Prüfung gilt gemeinsam über CORE / EDITORIAL / DIRECTORY.

Beispiel:
Treibholz und Treibholz sammeln = eine Identität.

Pro primärem Intent genau ein SEO-Owner.
Andere Säulen dürfen Relation/Filter/Verweis sein, keine konkurrierende Zielseite.

## V1.12-Status

Das vorhandene `HD001_V1.12.0_HOBBY_DEPOT_TARGET_PROFILE.json` bleibt wichtige Basis:
- 3-Säulen-Struktur;
- 8 Welten;
- Magazinstruktur;
- HivePress-Struktur;
- Aliasgruppen;
- 329 Monetarisierungs-/CORE-Regeln.

Aber:
Die neue Größen-/Rollenlogik liegt zeitlich danach.

Daher darf das vorhandene V1.12-Zielprofil NICHT ungeprüft als endgültiger neuer Livebaum behandelt werden.
Es muss aus dem bewerteten HOBBY_MASTER per Delta fortgeschrieben werden.

Der gespeicherte `HD001_CURRENT_INSTALL.zip` bleibt bis dahin der vorherige belastbare Installationsstand; kein neuer Live-Release aus der neuen Konzeptfortschreibung.

## Pilot

Geprüfte Regeltypen:
- Buchbinden → stabiler HOBBY_HUB;
- Fotografie → Macro-/Orientation-Research statt Riesenhub;
- Garten → kein Vollhub;
- Treibholz sammeln → Magazin erhalten / kein unbelegter CORE-Hub;
- Musizieren → Scope-Review statt erzwungener Weltzuordnung.

Referenz:
`HOBBY_MASTER_V2_PILOT_20261007.md`

## ERSTER OFFENER BLOCKER

Die 841 kanonischen Kandidaten sind noch nicht vollständig nach:
- Scope;
- Identität/Alias;
- Größenklasse;
- Content Capacity;
- Publikationsrolle;
- 3-Säulen-Ownership

bewertet.

## EXAKT EINE NEXT ACTION

Bewertungsregeln maschinenlesbar auf den HOBBY_MASTER anwenden und einen kontrollierten Batch erzeugen.

Danach:
- Verteilung prüfen;
- Fehlklassifikationen korrigieren;
- erst dann vollständigen Master bewerten;
- anschließend V1.12-Zielbaum als DELTA neu generieren;
- erst danach Plugin-/WordPress-Sync.
