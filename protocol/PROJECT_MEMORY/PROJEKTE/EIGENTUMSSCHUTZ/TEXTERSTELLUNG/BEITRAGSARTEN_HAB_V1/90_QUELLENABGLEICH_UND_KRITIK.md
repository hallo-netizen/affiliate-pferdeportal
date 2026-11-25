# Hab & Bewahr – kritischer Abgleich mit Original-Pferdeatelier (19.11.2026)

**Status:** dokumentierter Fachentwurf. Keine produktive Änderung an K0, K-Multi, Hab-Plugin oder WordPress.

## Verifiziert aus den Originaldateien
- Autoritative K0-Quelle: `hallo-netizen/affiliate-pferdeportal`, Zweig `konzept0-portal-neutral-20261002`.
- `RULE_CATALOG.json`: 117 aufgeführte Einträge (110 HARD, 7 TARGET); `RULE_VALUES.json` enthält 4 Typen **Beratung, FAQ, Pflege, Vergleich**. `ARTIKELTYPEN/Anleitung.json` ist eigenes zusätzliches Fach mit Status READY. **Kein Bericht-Regelfach** vorgefunden.
- `K0_CURRENT_STATE.json`: vor K0 nur eine Artikeltyp-/Kategorie-/Titelentscheidung; K0 prüft unveränderte Bindung. Genau drei interne Links mit definierten Rollen/Positionen und tatsächlich thematisch passenden Zielen.
- Original: harte 750–900 Wörter, mindestens 4 H2/16 Absätze, eigene Tabellen-/Listen-/Metadatenpflichten. **Diese Grenzen heute nicht aufheben oder durch Fachentwurf still umgehen.**
- `K0_GOAL_CONTRACT.json`: offizielle Recherchequellen, echte Wikipedia-Artikel erlaubt, keine eigenen Portalquellen, kein Veröffentlichen. `RULE_CATALOG.json`: Fakten- und Textprüfungen durch je einen vorhandenen Owner.

## Was 1:1 übernommen werden sollte
Einmalige Typentscheidung vor K0, relevante statt erzwungene Fachinhalte, faktengestützte und nachvollziehbare Aussagen, natürliche Sprache, lesergerechte Überschriften, kein Text-/Keyword-Spam, richtige interne Links, keine erfundenen Tests/Quellen, unveränderte Original-Qualitätsstationen und WordPress nur als Entwurf.

## Was fachlich anders werden muss – ohne jetzt die Original-Technik zu ändern
| Frage | Originalstand | Hab-Vorschlag | Warum |
|---|---|---|---|
| Länge | 750–900 Wörter hart | Nach Frage und Risiko, nicht nach starrer Zahl | Ein FAQ darf kurz sein, ein belegter umfangreicher Leitfaden lang |
| Pflichtabschnitte | FAQ Checkliste, Beratung Entscheidung, Anleitung Schritte | Nur wenn echter Nutzwert; Originaltechnikkonflikt separat lösen | Keine Füllinhalte |
| Interne Links | K0 aktuell genau 3 | Fachlich 1–3 sinnvolle, aber **nicht aktiv** | Drei unpassende Ziele sind schlechter; Vertragsänderung wäre separat testpflichtig |
| Quellen | Offiziell plus Wikipedia | Bei Recht/Versicherung/Sicherheitswirkung primäre Originalquelle verpflichtend | Falscher Sicherheitshinweis hat reale Folgen |
| Tabelle | Vergleich Pflicht, sonst definierte Ausnahmen | Nur bei begründeter Gegenüberstellung/Orientierung | Handlungsfolge oder Fallbericht profitiert oft nicht |
| Thematischer Fokus | Pferdehalter, Produkte, Pflege | Eigenschutz, Restgefahr, Rechts-/Datenschutzgrenzen, Ausfälle, Versicherungsbedingungen | Andere Verantwortung und Leserabsicht |

## Die drei Zuordnungsprobleme, die nicht kaschiert werden dürfen
1. **Ratgeber & Wissen ≠ immer Beratung.** Reines Erklären hat kein echtes `decision_goal`; K0-Beratung verlangt dieses Metadatum. Keine Scheinauswahl erfinden.
2. **Anleitung & Checkliste ≠ immer Anleitung.** K0 unterscheidet einmalige Anleitung von wiederkehrender Pflege. Beide Originaltypen bleiben erhalten; die Hab-Oberart darf sie nicht blind zusammenwerfen.
3. **Bericht & Praxisfall** hat weder fertiges Original-K0-Regelfach noch verifizierte konkrete WordPress-Magazinkategorie. Keine Freigabe vortäuschen.

## Zusätzliche Themen, die in der bisherigen Kurzkonzeption zu wenig sichtbar waren
- **Sicherheitswirkung ≠ absolute Sicherheit.** Schutzbereich, Fehlalarme, Strom-/Netzausfälle, Bedienung und Restgefahr sichtbar machen.
- **Schutz von Personen vor Eigentum.** Bei akuten Vorfällen zuerst sichere Handlung, keine Konfrontation, Fallen oder illegale Überwachung.
- **Aktualisierungspflicht nach Aussage.** Tarifbedingungen, Normen, Genehmigung, Preis, Produktstand, Unfall-/Kriminalitätszahlen nur mit Stand/Geltungsbereich.
- **Unabhängigkeit von Affiliate-Provisionen.** Kriterien und Ergebnis dürfen nicht von vorhandenen Partnerprodukten abhängen.
- **Korrektur, Transparenz, Privatsphäre.** Praxisfälle müssen echt belegbar sein; keine wiedererkennbaren Geschädigten und erfundene „echte“ Fälle.
- **Mehrere Lebenssituationen.** Mietwohnung, Haus, Ferienhaus, Boot, Garten, Wohnmobil, kleine inhabergeführte Geschäfte nur dann im Artikel unterscheiden, wenn das Ergebnis tatsächlich anders wird.
- **Eindeutiges Aktualisierungs- und Redaktionseigentum.** Kein zweiter Prüfschritt, keine zweite Typentscheidung, kein K0-/K-Multi-Fallback.

## Originalquellen / eigene Ablage
- `konzept0-portal-neutral-20261002:RULE_VALUES.json`
- `konzept0-portal-neutral-20261002:RULE_CATALOG.json`
- `konzept0-portal-neutral-20261002:K0_CURRENT_STATE.json`
- `konzept0-portal-neutral-20261002:K0_GOAL_CONTRACT.json`
- `konzept0-portal-neutral-20261002:ARTIKELTYPEN/Anleitung.json`
- `work/texterstellung-hobby-hab-arbeitskopien-20261116:protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/WISSENSDATENBANK/RECHERCHE_STANDARD.md`
- `.../TEXTERSTELLUNG/HAB_BEITRAGSARTEN_SEO_KRITISCHE_PRUEFUNG_VORSCHLAG_20261119.md`

**Ablageziel:** Je eine eigenständig abrufbare JSON-Datei pro Hab-Art, gemeinsamer Regelbestand getrennt, Trigger für besondere Hab-Regeln getrennt. Diese Entwürfe sind **nicht** in die K0-Originalpfade geschrieben und ändern keine produktive Prüfung.
