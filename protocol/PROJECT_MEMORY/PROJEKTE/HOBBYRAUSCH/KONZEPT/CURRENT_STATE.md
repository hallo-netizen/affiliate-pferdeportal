# HOBBYRAUSCH – KONZEPT – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-07
STATUS: 3-SÄULEN-GRUNDKONZEPT FEST / GRÖSSEN- UND ROLLENMODELL EINGEFÜHRT / HOBBY_MASTER V2 AKTIVE BEWERTUNGSBASIS

## Rolle

Einzige aktuelle Zustandsautorität des Scopes `HOBBYRAUSCH_KONZEPT`.

## Unveränderte Grundarchitektur

Marke:
**Hobby Depot**

Drei Säulen:
- Hauptportal / CORE;
- Magazin / EDITORIAL;
- HivePress / DIRECTORY.

Acht Hauptwelten:
**Gestalten · Fertigen · Technik · Forschen · Pflanzen · Tiere · Bewegen · Sammeln**

Diese acht Welten bleiben im ersten Integrationslauf geschützt.

Zwei zentrale Nutzerwege:
1. Nutzer kennt sein Hobby bereits und sucht Einstieg, Ausrüstung, Kosten, Material, Techniken und Vertiefung.
2. Nutzer sucht Inspiration und gelangt über Magazin/Hobbyfinder zu passenden Hobbys.

## Neue verbindliche Portalgrenze

Hobby Depot ist nicht "alles, was Menschen in ihrer Freizeit tun".

Ein Thema wird nur dann regulär aufgenommen, wenn es:
- aktive/wiederholbare Freizeitpraxis ist;
- erlern-/vertiefbaren Tätigkeitsschwerpunkt besitzt;
- natürlich in eine der acht Welten passt;
- nicht nur durch erzwungene Zuordnung integrierbar ist.

Ein echtes Hobby außerhalb dieser natürlichen Passung erzeugt nicht automatisch eine neunte Welt.

## Neue Rollenlogik

Nicht jedes Thema bekommt einen eigenen Hub.

Mögliche Rollen:
- ORIENTATION_UNIVERSE;
- HOBBY_HUB;
- EDITORIAL_TOPIC;
- ARTICLE_ONLY;
- FINDER_ONLY;
- OUT_OF_SCOPE.

Monetarisierung entscheidet nicht über Behalten/Löschen.
Nicht monetarisierbare gültige Themen bleiben für Magazin/SEO/Finder erhalten.

## Größenregeln

Leaf-Kategorie:
- Ziel 5–12 Beiträge;
- 4 nur begründete Ausnahme;
- 13–15 zwingende Split-Prüfung;
- >15 nur explizite Ausnahme.

Hobby-Hub:
- Ziel 3–6 tragfähige Leaf-Kategorien;
- 7–8 Split-/Macro-Prüfung;
- >8 grundsätzlich Macro/Split statt einzelner Hub.

## Zentrale Hobby-Sammelstelle

Rohliste bleibt unveränderte Provenienzquelle.

Neue aktive Bewertungsbasis:
`/hobby rausch/HOBBY_DEPOT_HOBBY_MASTER_V2_20261007.json`

Current-Zeiger:
`KONZEPT/VORARBEITEN_HOBBYFINDER/HOBBY_MASTER_V2_CURRENT.md`

Bestand:
- 908 Rohzeilen;
- 844 exakte Namen;
- 841 kanonische Identitäten nach aktuellen Alias-Merges;
- 329 bestehende V1.12-Monetarisierungs-/CORE-Regeln übernommen;
- 286 DIRECT;
- 43 ASSISTED;
- 512 UNKNOWN, aber weiterhin erhalten.

## Neue bekannte Hobby-Kandidaten

Breite/bekannte Hobbys werden nicht blind publiziert, sondern zuerst als Research Queue geprüft.

Erste Queue:
Fotografie, Malen, Zeichnen, Nähen, Stricken, Häkeln, Holzwerken, Heimwerken, Wandern, Radfahren, Camping, Schwimmen, Klettern, Bouldern, Gärtnern, Gemüseanbau, Briefmarken sammeln, Angeln, Plane Spotting.

## Pilotbefund

Pilotfälle:
- Buchbinden → HOBBY_HUB bleibt stabil;
- Fotografie → Macro-/Orientation-Prüfung statt Riesenhub;
- Garten → kein einzelner Vollhub;
- Treibholz sammeln → im Magazin erhalten, kein CORE-Hub ohne tragfähige Evidenz;
- Musizieren → Scope-Review statt erzwungener Weltzuordnung.

## Autoritative Konzeptdateien

- `HOBBY_GROESSEN_ROLLENMODELL_20261007.md`
- `../SEO_KATEGORIEN/HOBBY_MASTER_V2_INTEGRATION_20261007.md`
- `../SEO_KATEGORIEN/HOBBY_MASTER_V2_PILOT_20261007.md`

## Technische Abgrenzung

Pluginversionen, Live-Status und technische Releasefragen bleiben ausschließlich in:
- `PLUGINS/PLUGIN_AKTEN/<PLUGIN-ID>/CURRENT.md`;
- `SEO_KATEGORIEN/CURRENT_STATE.md`.

## Erster offener Blocker

Die 841 kanonischen Kandidaten sind noch nicht vollständig nach Scope, Größenklasse, Content Capacity und Publikationsrolle bewertet.

## EXAKT EINE NEXT ACTION

Die Bewertungsregeln aus dem Größen-/Rollenmodell maschinenlesbar auf den HOBBY_MASTER anwenden und zunächst kontrolliert als Batch auswerten.

Dabei:
- acht Welten schützen;
- bestehende Zwischenstruktur zunächst schützen;
- keine direkte WordPress-Synchronisierung;
- keine Massenfreigabe;
- erst nach Rollen-/Ownership-Prüfung Zielbaum-Delta erzeugen.
