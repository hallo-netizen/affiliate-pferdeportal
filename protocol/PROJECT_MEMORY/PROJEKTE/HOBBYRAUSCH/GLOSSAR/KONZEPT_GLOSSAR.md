# HOBBY DEPOT – GLOSSAR-KONZEPT

STAND: 2026-10-19
STATUS: FACHLICH FREIGEGEBENE BASIS

## Zweck

Das Glossar erklärt Begriffe, die ein Nutzer beim Einstieg oder Vertiefen eines Hobbys kennen muss. Es stärkt Orientierung, interne Verknüpfung und thematische Tiefe, ohne den bestehenden Hobbybaum zu verdoppeln.

## Aufnahmeregel

Ein eigener Glossarbegriff entsteht nur, wenn **die Erklärung des Begriffs selbst** die Nutzerfrage erfüllt.

Nicht als eigene Glossarseite:
- ein vollständiges Hobby;
- eine bestehende Hobbywelt;
- eine bestehende Hub-/Kategorie-Seite;
- ein eigenständiges Ratgeberthema;
- bloße Synonyme;
- Varianten, die keinen eigenen Erklärungsintent tragen.

In diesen Fällen erklärt die bestehende Hauptseite den Begriff; das Glossar darf dorthin verweisen.

## Datenmodell

Pflicht je Begriff:
- stabile term-ID;
- Begriff;
- Slug;
- genau eine primäre Hobbywelt;
- Synonyme;
- Kurzdefinition;
- Facherklärung;
- Abgrenzung;
- mindestens ein verwandter Begriff;
- Quellen;
- Recherche-/Prüfstatus;
- Prüftermin/Intervall;
- individueller SEO-Titel;
- individuelle Meta-Description;
- optional genau eine starke Hauptseite.

## Themenwelten

- Gestalten
- Fertigen
- Technik
- Forschen
- Pflanzen
- Tiere
- Bewegen
- Sammeln

## SEO-Grenze

Das Glossar ist kein Seitenmengen-System.

Ein Glossarbegriff darf nur indexierbar werden, wenn:
1. ein eigenständiger Nutzer-/Suchintent plausibel ist;
2. der Begriff gegenüber bestehenden Hobby-/Kategorie-/Ratgeberseiten eindeutig abgegrenzt ist;
3. Inhalt und Quellen einen echten eigenständigen Nutzwert liefern;
4. keine kannibalisierende Dublette entsteht.

## Produktion

`Begriffspool → Intent-/Dublettenprüfung → Recherche + Text → WDB-Datensatz → Validator → WordPress-Draft → Readback → Freigabe`

Kein Auto-Publish. Keine autonome Discovery-/Cron-Produktion.

## Design

Das funktionale Grundprinzip des Pferde-Ateliers ist übertragbar:
- Glossar-Hauptseite;
- A–Z;
- Suche;
- Filter nach Themenwelt;
- kompakte Begriffskarten;
- Einzelbegriffsseite;
- verwandte Begriffe;
- optional „Mehr zum Thema“.

Farben, Typografie, Header/Footer und Kartenoptik werden ausschließlich aus dem aktuellen Hobby-Depot-Designsystem übernommen, nicht aus dem Pferde-Designplugin.
