# MOD-008 – DATENVERTRAG V1

STAND: 2026-09-12
STATUS: PROTOTYPVERTRAG

## Ziel

Ein Glossarbegriff bleibt klein, kann aber später um neue Felder erweitert werden, ohne bestehende Datensätze umzubauen oder zu verlieren.

## Kernobjekt Begriff

Pflichtkern:
- interne WordPress-ID;
- Titel/Begriff;
- Veröffentlichungsstatus;
- Volltext/Erklärung;
- mindestens ein optional zuordenbarer Oberbereich.

Standardfelder:
- Kurzdefinition;
- Synonyme;
- verwandte Begriffe;
- SEO-Titel;
- Meta-Description;
- Canonical URL;
- Indexierungsmodus.

## Erweiterbarkeit

Die Feldliste ist kein festes Pferdeschema.

Neue Felder werden über `uge_field_schema` ergänzt.
Bestehende Begriffe erhalten dadurch keinen Zwangswert; das neue Feld ist zunächst leer.
Alte Felder werden nicht still gelöscht oder umgedeutet.

Beispiel zweite Portalnutzung:
`Quellenhinweis`, `Hersteller`, `Normnummer`, `Epoche` oder ein anderes Fachfeld kann ergänzt werden, ohne den Core zu ändern.

## Oberbereiche

Oberbereiche sind eigene Glossar-Gruppen, getrennt von normalen WordPress-Kategorien.
Sie dürfen umbenannt, ergänzt, verschoben und hierarchisch erweitert werden.
Der Core enthält keine feste Liste.

## URL/SEO

Portalabhängig konfigurierbar:
- URL-Basis;
- Glossarbezeichnung;
- Titel-Schema;
- Description-Schema;
- Index/Noindex.

Einzelwerte können je Begriff überschrieben werden.

## Trennung Fachwissen / Veröffentlichung

Der Core speichert die veröffentlichte WordPress-Fassung.
Eine externe Wissensdatenbank kann per späterem Importadapter liefern, bleibt aber eigene Fachwahrheit.
Keine automatische Veröffentlichung.
