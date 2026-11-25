# HAB & BEWAHR – Kategorien und K-Multi, Abschluss 19.11.2026

## Getan
Alle 1.323 in C23 dokumentierten Kategorien aus 265 Themenseiten je Welt als sechs Einzelnachweis-JSON-Dateien erfasst. Davon 285 Kategorien mit historischen echten WordPress-Term-IDs aus C22 vom 13.10.; 1.038 weitere aus C23 ohne aktuellen eindeutigen WordPress-Readback. Keine neuen Kategorien und keine falschen Live-IDs angelegt.

Vollinventar unter `ARTIKELARTEN_BESTAND_20261119/`:
- Einbruch & Diebstahl: 187, davon 55 historisch WP.
- Vandalismus & Zerstörung: 131, davon 46.
- Wetter & Naturgefahren: 286, davon 46.
- Technik & Ausfälle: 253, davon 45.
- Feuer & Gase: 215, davon 46.
- Wasser & Feuchtigkeit: 251, davon 47.

Sämtliche sechs Dateien rückgelesen, Summen 1.323/285/1.038 PASS; keine unbekannten Schreibarten.
**Nicht zu Livebestand addiert:** 471 noch nicht importierte C23-Vorschläge, 138 C25-Versicherungskategorien als Konzept und 185 C26-Versicherungserweiterungen ohne bestätigten Live-Readback. Drei getrennte Datensätze unter demselben Inventarverzeichnis.

**Magazin:** Teil-Readback vom 14.11. belegt 14 tatsächlich gespeicherte WordPress-SEITEN: Magazin (106), vier Rubrikseiten (Schutzobjekte 186, Situationen & Lebenslagen 187, Praxis & Checklisten 185, Wissen & Hintergründe 188), acht Schutzobjektgruppen (189–196) und Glossar (184). Vollständige IDs und Slugs als `magazin-14-belegte-wp-seiten.json` hinterlegt. **Das sind keine nachgewiesenen Beitragskategorien.** Originale Hab-ZIP 0.4.31.6 hat `journal_categories.categories=[]` und `runtime_route_activation=NOT_CONFIGURED`; der vorhandene MINI-Worker verlangt für Route MAGAZIN den exakten existierenden WordPress-Beitragskategorie-Slug. **Magazin-Veröffentlichung daher gesperrt, solange keine echte Kategoriebindung nachgewiesen ist.**

**Beitragsarten:** Fünf schon vorhandene MINI-Arten Beratung, FAQ, Vergleich, Pflege, Anleitung als kleinster fachlich sinnvoller Vorschlag. Keine sechste Art, keine feste Artikelart pro Kategorie. Im MINI werden route/category_slug/article_type **einmalig** am konkreten Beitrag entschieden und eingefroren. Automatisch aus Begriffen abgeleitete Typvorschläge in den sechs Einzellisten sind **nicht** verbindlich.

**Hab-spezifische Textregeln – nur Vorschläge:** Gefahr/Schutzobjekt/Wirksamkeitsgrenzen präzise; riskante elektrische, gas-, brand- und bautechnische Arbeiten abgrenzen; Rechts-, Versicherungs-, Datenschutz- und Normenbehauptungen mit vertrauenswürdigen aktuellen Originalquellen und Ausnahmen belegen; Maßnahmen/Produktvergleiche nach gleichen Kriterien und tatsächlichen Grenzen; Magazin ohne Doppelthemen und nur in bestätigter Unterkategorie. Alle originalen globalen K0-Regeln unverändert.

**K-Multi-Gegenprüfung:** Entwicklerzweig `hallo-netizen/k0-multiportal:k0-offline-rule-bindings-20261027`: 177 Offline-Tests, kein freigegebener Original-Gesamtwriter, Hab-Portalprofil `NO_VALUES_BLOCKED`, keine Kategorienbindung, keine Hab-Regelwerte und keine produktiven WordPress-Ziele. K-Multi-Referenz kennt nur vier Schreibarten; Hab-Plugin kennt zusätzlich Anleitung. `KMULTI_QUELLVERTRAG_GEGEN_HAB_04316_20261119.json` enthält den exakten Statusvergleich. Hab-ZIP übergibt fünf Originalfelder: title, target_keyword, category, article_type, plan_slot, Vertrag PSERC_TEXTMACHINE_METADATA_BATCH_V2. Keine Neuentwicklung der MINI-Schnittstelle nötig.

## Nächste Testfolge
1. Echten aktuellen WP-Term-Readback im bestehenden Kategorien-Leseweg prüfen; Magazin-Term-Slug absichern.
2. Je Schutzwelt einen lokalen, kostenlosen Recherche- und MINI-Praxisfall prüfen, MAGAZIN bis zur Kategoriebindung als erwarteten Sperrfall behandeln.
3. K-Multi mit seinen wirklichen Originaldaten und dem vollständigen Writer/Prüfer offline testen; Hab-Profil und fehlende Anleitung-Regel ausdrücklich klären, keinen Pferdeatelier-Fallback.
4. Eine originale Fünffelder-Charge über K-Multi und korrektes Rückgabeformat bis zum WordPress-ENTWURF testen, Fremdportal-/Doppel-/Typfehler abweisen. Erst dann einen kleinen Stapel.

## Unverändert
Hab Texterstellung 0.4.31.6, WordPress, K0, K-Multi, MINI, alle anderen Portale. Keine neue Plugin-ZIP, keine kostenpflichtige Recherche, keine WordPress-Schreibaktion. End-to-End-Produktions-PASS noch nicht behauptet.

Umfangreiches vollständiges Berichtsdokument tatsächlich in Library:
`/hab-und-bewahr/TEXTERSTELLUNG/ARTIKELARTEN_KMULTI_20261119/HAB_TEXTERSTELLUNG_KATEGORIEN_KMULTI_GESAMTSTAND_20261119.md`.
