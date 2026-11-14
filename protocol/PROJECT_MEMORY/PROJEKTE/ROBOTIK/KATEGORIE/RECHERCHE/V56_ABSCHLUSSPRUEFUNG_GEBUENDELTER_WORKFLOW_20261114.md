# Robotik V56 – Abschlussprüfung: Benutzeraktionen bündeln, vorhandenen SEO-Klick NOCH NICHT als endgültig ausgeben
**Datum: 14.11.2026 · Grundlage:** V54 freier WP-Export, V55 16er-HOLD-Review, V53 tatsächlicher PHP-Code, verbindlicher Zielvertrag, DataForSEO-API-Dokumentation. **Nur Ablaufprüfung; kein bezahlter Aufruf, kein WP-Import, keine zweite Pluginlinie.**

## Belegte Lücken des alten Anweisungswegs
1. `Keyword Overview / Erweiterter Umfang` in Version 0.4.3 nimmt **nur die bereits vorgedachten 437 SEO-Planphrasen**. Es findet **keine fehlenden Keywordvarianten**. Es kann daher keine vollständige abschließende Keyword-Recherche versprechen.
2. Der Original-Code setzt `include_serp_info=false` und speichert nur `keyword, linked_owners, search_volume, competition, cpc, intent, updated_at`. Damit fehlen echte organische Suchresultat-URLs. Auch `include_serp_info=true` im Keyword-Overview liefert laut Anbieter nur SERP-Überblick (u.a. Ergebnistypen/Anzahl), **keine Top-10-URL-Überlappungsprüfung**. 16 HOLDs und weitere semantische Kollisionen können damit nicht beweisfest gelöst werden.
3. Die vorhandene Alternative `Keyword Ideas / Erweiterter Umfang` nimmt `array_slice($products,0,10)` – bloß die **ersten 10 Roboterarten**, nicht eine strukturierte Repräsentation aller acht Welten. Zusätzlich `limit=25`, also kein vollständiger Missing-Keyword-Gap-Check.
4. Das v0.4.3-SEO-Manifest ist **absichtlich nicht** der WordPress-Importplan. Der alte Importer/Plan (104 ursprüngliche WP-Seitenpositionen/89 Inhaltskategorien; darunter 72 Typseiten) bleibt unverändert. 141 neue Typkandidaten sind **keine** vollständige bzw. sichere WP-Deltavorlage.
5. Das GitHub-`PLUGIN/CURRENT.zip` lag im geprüften Stand weiterhin auf historisch 0.3.0; der WP-V54-Export belegt aber eine **ausgeführte 0.4.3-Datenausgabe**. Nicht den historischen Installer empfehlen oder bei Versionsbezeichnungen blind auf GitHub-`CURRENT.zip` verweisen. V53_SOURCE auf GitHub enthält nur geänderte/quellgeprüfte Komponenten, nicht alle Original-Includes des kompletten 0.4.3 ZIP.
6. Die tatsächliche WordPress-Inventur vom **14.11.2026** ist nicht dokumentiert; allein die frühere WP-Inventur vom 09.11. oder der Keyword-Export beweisen keine aktuellen Seiten/Eltern/URLs.

## Korrigierter zusammengefasster Endablauf – keine wiederholten Nutzerschleifen
**Phase A – einmalige Vorab-Fertigstellung durch Assistenz, OHNE Nutzeraktion:**
- Den vereinbarten **V52-Master und V55-HOLD-Fachentscheid beibehalten**; keine neue fachliche Hauptstruktur und kein zweiter Forschungsbestand.
- **Eine kontrollierte Ergänzung DESSELBEN Kategorieplugins** planen: kostenloses vollständiges SEO-Preflight und repräsentative Keyword-Gap-Ermittlung aus allen acht Welten statt nur den ersten zehn Produkten. Nur tatsächlich erforderliche API-Methoden verwenden.
- Im selben einzigen SEO-Auftrag/Ablauf: vorhandene Keywords messen, fehlende Käufer-/Info-/Forschungsfragen ermitteln, erkennbare Überschneidungen zuerst fachlich schließen, echte Google-Suchresultate nur bei verbleibenden relevanten Konfliktgruppen vergleichen (organische URLs). Falls mehrere API-Endpunkte erforderlich sind, intern getrennte Requests, aber **EIN Benutzerstart mit einem vorher ausgewiesenen verbindlichen Maximalbudget, keinem automatischen Wiederholungslauf und vollständiger Fehler-/Kostenerfassung**. **Diese Funktion ist NICHT in 0.4.3 implementiert; nicht behaupten, dass aktueller Button sie ausführt.**
- Resultat: **EIN gemeinsamer kompletter SEO-Bericht**, mit Einzelstatus gemessen/nicht verfügbar/nachzuprüfen, Belegquelle, Suchintent, realem Volumen sofern vorhanden, Alternativbegriffen, Kandidaten-Owner-ID und SERP-Konflikten. Kein Automatismus, der aus niedrigen Suchvolumina ganze Forschungsseiten löscht.

**Phase B – Nutzeraktion 1 (erst wenn Phase A lokal nachgewiesen ist):**
- **Einmal Kostenrahmen freigeben**, **einmal Gesamtprüfung starten**, **einen Gesamtbericht exportieren**. Bei unbekannten/überschrittenen Kosten keine Anbieterabfrage. Ein Report ersetzt mehrere kleine Dateien. Keine zweite bezahlte Prüfung nachträglich ohne erneute ausdrückliche Zustimmung.

**Phase C – ohne Nutzeraktion:**
- SEO- und Fachbefunde über **alle 437 bekannten Owner inklusive 16 HOLDs sowie ggf. neu entdeckte Suchbegriffe** in einem Gesamtdelta entscheiden: beibehalten / benennen / zusammenführen / getrennt begründen / vorerst zurückstellen; nicht 16 Einzelfreigaben verlangen.
- **Ein einziges, bestehendes Kategorieplugin** für V52/V56-Struktur als geschützten **Soll-Ist-Vergleich** vorbereiten; tatsächliche WordPress-Objekte *unmittelbar vor Schreiben* vom Plugin lesen, alte IDs, Slugs, Veröffentlichungen und drei Säulen schützen. Korrekte freigegebene neue Typseiten, individuelle flache Kategorien, ggf. Industrie-Landingpages; keine Inhalte durch das Kategorieplugin produzieren.
- **EINE WordPress-Gesamtvorschau** aus dem vollständig geplanten Delta für acht Welten, Magazin und Finder/Glossar/Register/Anzeigenmarkt ohne zusätzliche Detail-Exports. Fehlende Funktionen klar als offen anzeigen.

**Phase D – Nutzeraktion 2 (ausdrückliche Schreibfreigabe):**
- **Einmal die komplette geprüfte WordPress-Deltaübernahme freigeben**, darauf ein kontrollierter Writer mit sauberem Readback im selben Plugin und einem Gesamtbericht. Keine nachgelagerte manuelle Einzelprüfung je Kategorie. Im Fehlerfall kein fiktiver PASS und keine automatische neue teure SEO-Runde.

## Hartes Urteil
- **NEIN:** Die vorher empfohlene einzelne 0.4.3-Overview-Abfrage ist *nicht* der endgültige umfassende SEO-Strang. Sie wäre nur eine Teilmessung und würde anschließende weitere bezahlte/technische Zusatzschritte provozieren.
- **JA:** Zwei getrennte **notwendige Benutzerfreigaben** bleiben (Kosten, später WordPress-Schreibvorgang). Dazwischen kann praktisch alles zur **einen Recherche → Entscheidung → Vorschau → Import**-Strecke gebündelt werden. Zusammenlegen der fachlichen Recherche mit der gesamten späteren Veröffentlichung in EINEN vorab freigegebenen Knopf ist *nicht* fachlich sicher, da SEO-Befunde den Seitenbestand noch ändern können.
- **Arbeitsreihenfolge ab hier:** nicht den bisherigen Paid-Button starten; erst nachweislich den allumfassenden, einmalig kostenbestätigten SEO-Lauf in derselben Pluginidentität technisch fertigstellen und als geschütztes Update prüfen. Keine Zahl/Preisobergrenze erfinden.

**Anbieter-Dokumentation:** https://docs.dataforseo.com/v3/dataforseo_labs-google-keyword_overview-live/ ; https://docs.dataforseo.com/v3/dataforseo_labs-google-keyword_ideas-live/ ; https://docs.dataforseo.com/v3/serp/google/organic/live/advanced/ .
