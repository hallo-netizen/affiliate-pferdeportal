# Pferdeatelier – Texterstellung: endgültiger KISS-Zielvertrag
**Betreiberentscheidung vom 14.11.2026.** Dieses Dokument fixiert das SOLL-Konzept. Noch keine Implementierungs- oder Installationsfreigabe. Bei Widerspruch zu älteren internen/externen Mehrstufen-Skizzen gilt diese jüngste Betreiberentscheidung für den künftigen Aufbau. Änderungen am Original-K0, Frontend und WordPress-Core sind nicht beauftragt.

## Ein einziger MINI-Außengang: nur fünf Hauptstationen
1. **WordPress – Recherche:** Keywords sammeln, Pferde-/Portalrelevanz JA/NEIN genau einmal bestimmen. Kein weiterer Pferde-JA/NEIN-Entscheider in MINI.
2. **Extern – EIN gemeinsamer MINI-Workflow:** WordPress gibt eine einzige kompakte Datenübergabe mit neuen Keywords, vorhandenem und geplantem Content, vollständiger Hierarchie der WordPress-Kategorien samt übergeordneten Seiten, Fach-/Magazin-Zugehörigkeit und Deckungszahlen an ChatGPT. Innerhalb **derselben** MINI-Runde arbeiten disjunkte Teilworker: (A) Kategorie plus Artikelart genau einmal festlegen (oder KLÄRUNG), (B) Redaktionsplan einmalig auf gleiche bzw. andere Suchabsicht, vorhandene/geplante Artikel, Kannibalisierung, Dubletten, Inhaltslücken, Kategorieverteilung und Priorität prüfen und FREI/BELEGT/KLÄRUNG entscheiden, (C) genau einen Titel für jedes FREI-Thema erzeugen. Jede Fachfrage hat genau einen Owner; kein anderer Teilworker entscheidet sie erneut. Titelworker ändert weder Suchabsicht noch Kategorie, Artikelart oder FREI-Entscheid.
3. **WordPress – EIN Rückimport von MINI, zentrales Redaktionsregal:** Bewilligte Themen, Kategorie, Artikelart, Titel, Freigabe und Priorität im bestehenden EINEN zentralen Regal speichern. Das Regal ist die **einzige Bestands- und Statuswahrheit** (recherchiert, vorhanden, geplant, freigegeben, offen, in K0, Entwurf). Es darf technisch prüfen, ob ein Kategorie-Term/eine Auftragskennung tatsächlich existiert und die Quellbindung stimmt, aber **keine inhaltliche Entscheidung nachprüfen, verändern oder doppeln**. Es erstellt aus FREI den vollständigen K0-Auftrag mit weiterhin genau fünf Feldern: `title`, `target_keyword`, `category`, `article_type`, `plan_slot`. Der technische `plan_slot` ist eine Identitäts-/Zuordnungsangabe im K0-Vertrag, **kein separates Planungsbüro**. Die technische Verträglichkeit zum originalen K0 und Reimport ist vor jeder Release-Freigabe zu beweisen.
4. **Extern – K0:** einen vollständigen Artikel nach den gültigen K0-Qualitätsregeln schreiben; keine fachliche Doppelprüfung von Keyword, Kategorie, SEO, Titel, Themenpriorität.
5. **WordPress – Rückimport:** K0-Artikel unter der bestehenden Auftrags-ID als unveröffentlichten Entwurf speichern und zentralen Regalstatus aktualisieren. Keine zweite Fachentscheidung.

## Einziger Eigentümer jeder Frage
- Pferderelevanz = WP-Recherche.
- Kategorie, Fach/Magazin, Artikelart = Kategorie-/Typ-Teilworker **innerhalb des EINEN MINI**.
- Bestandabgleich, Doppelung/Kannibalisierung, Leserabsicht, thematische Abdeckung, FREI/BELEGT/KLÄRUNG und Priorität = Redaktionsplan-Teilworker **innerhalb desselben MINI**. Mehr Beiträge in nachgefragten Bereichen sind erlaubt; keine starren gleichen Artikelzahlen. Auffallende Lücken oder Überdeckung steuern die Priorität.
- Titel = Titel-Teilworker **innerhalb desselben MINI**.
- Zentrale Übersicht, dauerhafte Auftrags-/Regalverwaltung = WordPress (reine Speicherung, Status, technische Gültigkeit).
- Artikelinhalt = K0.
- Unklare Kategorien bleiben gesammelt als KLÄRUNG, statt eine Kategorie zu erfinden oder nachträglich einen zweiten Worker entscheiden zu lassen.

## KI-Datenmenge: tragbar, aber kompakt
**Verbindliche fachliche Einschätzung: JA**, eine gemeinsame MINI-Runde kann genügend Kontext bekommen, wenn WordPress **kompakte Registerdaten** statt vollständiger Artikeltexte/ungefilterter Rohdaten liefert:
1. Vollständiger aktueller Kategoriebaum einschließlich Seiten-/Elternpfad, echte ID/Slug, Fach/Magazin; Stand und Version, nicht nur historische Liste von Produktfamilien.
2. Vorhandene veröffentlichte und entworfene Artikel sowie geplante/freigegebene Aufträge (IDs, Keyword, Titel, Suchabsicht/Kurzinhalt, Kategorie, Status) als kompakte Bestandsliste; dazu Aggregatzähler nach Kategorie/Ast.
3. Neue begrenzte Keyword-Charge, z. B. 20–50. Für echte Zweifelsfälle kurze relevante Vergleichsauszüge, innerhalb derselben MINI-Runde und ohne neuen Entscheidungs-Worker.
4. Wenn der globale Datensatz in einer Datei zu groß ist: Dateiteile oder kompakte Inhaltsverzeichnisse plus themenrelevante Vergleichszeilen **vor** der einmaligen Fachentscheidung aufbereiten; niemals wissentlich ohne ausreichenden globalen Bestand FREI erteilen. Technische Vorselektion ist keine SEO-/Kategorieentscheidung. Datenvolumen vor Einsatz messen und vollständigen Original-WP-Bestand samt 61 Altfragen nachweisbar testen.
**Einschränkung:** Eine genaue 90%-Zuordnungsquote oder fehlerfreie Dublettenabwehr lässt sich erst im Echttest belegen; die bloße technische Möglichkeit ist keine Produktionsabnahme. Vollständige Langtexte aller Kategorien/Artikel/5.000 Suchanfragen zusammen ungefiltert zu übergeben ist NICHT vorgesehen.

## Bestehendes ersetzen, nicht duplizieren
- Bisherigen internen PHP-Kategorieentscheid als nachgelagerten fachlichen Entscheider nicht fortführen.
- Bereits abgeschlossene Altentscheidungen und Titel der 61 historischen Themen nicht erneut beurteilen. Offene Felder nur mit expliziter bisheriger Entscheidung und gesichertem Zielstatus ins eine MINI-Konzept übernehmen.
- Keine zweite externe SEO-/Redaktions-/Titelrunde, keine semantische WordPress-Nachprüfung, kein neues Planungsbüro, keine neuen parallelen Datenbanken/Regale.
- WordPress-Quelle und einziger Speicher bleiben die Ist-Basis, ChatGPT ist die eine externe fachliche Entscheidungsrunde, K0 die zweite externe Textrunde.
- Stand 14.11.2026: originale Tests von QA 046 mit 61 Themen haben **keine** Mehrheit zur Kategoriezuordnung erreicht; die 0.4.5 WIP ist **nicht** zur Installation freigegeben. Vor Umsetzung: Originalpfade und Datenscope mit dem endgültigen Vertrag abgleichen, echt bei WordPress und mit 61 Fragen nachprüfen, keine Änderung ohne Zielvertragsabnahme.
