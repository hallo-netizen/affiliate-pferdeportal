# ZIELVERTRAG – KATEGORIEN ROBOTIK

## Ziel
Eigenständiges Robotik-Portal auf neuer WordPress-Seite vorbereiten. Alle drei Säulen vollständig durchdenken und nur fachlich sinnvolle Unterkategorien schaffen. Keine Fremdprofile oder alte Daten übernehmen.

## Harte Regeln
1. **Drei Säulen:** CORE/Hauptportal, EDITORIAL/Magazin und DIRECTORY/Anzeigenmarkt (HivePress).
2. **Fachkonzept zuerst:** Kategorien nach Nutzungszweck und sachlicher Logik. Keywords bestätigen die Namen, bestimmen aber nicht allein die Struktur.
3. **Knotenrollen unterscheiden:** WordPress-Seite / Inhaltskategorie / Magazinrubrik / HivePress-Anzeigenkategorie / Beitrag. Keine Vermischung.
4. **Ein Thema – ein Haupt-Owner:** Kein paralleles identisches Hauptthema in Magazin und Portal. Ergänzende Artikel und Inserate dürfen verknüpfen, aber nicht dieselbe Suchaufgabe duplizieren.
5. **Tragfähigkeit:** Letzte Inhaltskategorie muss mehrere klar verschiedene spätere Beiträge ermöglichen. Kein kosmetisches Auffüllen auf feste Zahl und keine künstliche Obergrenze.
6. **Monetarisierung:** Geräte, Zubehör, Dienstleistungen, Wartung, Vermietung, Schulungen und Anbieter prüfen; kein Produktzwang.
7. **Keine Artikelproduktion im Kategoriebüro:** Hier nur Themenstruktur, grobe Inhaltschancen und Keyword-Evidenz, keine fertigen Titel/Beiträge.
8. **WordPress zuerst prüfen, dann schreiben:** Vorschau, Eigentümer und Kollisionen prüfen; Freigabe erforderlich. Keine automatischen Änderungen, keine stillen Zuordnungen, keine Löschung/Überschreibung.
9. **KISS:** eine aktuelle Wahrheit, ein gültiges Profil, eine kontrollierte Importstrecke; weder konkurrierende Plugins noch überflüssige Sperrprüfungen.
10. **Projekttrennung:** keine fremden IDs/URLs/Taxonomiezuordnungen, keine fremden Pluginprofile und keine alten Startdaten.

## Statusgrenzen
Konzept offen → Konzept geprüft → Umsetzung vorbereitet → lokale Tests → echte WordPress-Prüfung → ausdrücklich freigegeben. Vorher keine Behauptung eines Live-PASS.

## Verbindliche Produkthierarchie (08.11.2026 – ausdrücklich bestätigt)
Die CORE-Struktur folgt zwingend: **WordPress-Seite (Hauptwelt) → WordPress-Seite (Bereich) → ggf. weitere WordPress-Seiten → letzte WordPress-Seite = EIN konkret abgrenzbarer Robotertyp / ein spezifisches Produkt → darunter flache WordPress-`category`-Kategorien für dessen Informationsbedürfnisse → darunter einzelne WordPress-Beiträge**.

Eine letzte Seite ist **keine allgemeine Produktfamilie**, sondern ein funktional eindeutig abgrenzbares Produkt/Robotertyp. Das ist keine Forderung nach einzelner Marke oder Modellnummer. Beispiel: „Roboter“ und „Logistikroboter“ sind zu breit; ein konkret funktional abgegrenzter Servierroboter oder Melkroboter kann ein Zielseitenkandidat sein. Ob AMR, FTS, Paletten- oder andere Transportroboter zu einem oder getrennten Zielseitenkandidaten gehören, entscheidet der dokumentierte Fach-/Suchabgleich.

**Kategorien behandeln ausschließlich den Robotertyp der letzten Elternseite** und dürfen nicht untereinander verschachtelt werden. „Kosten“, „Vergleich“, „FAQ“, „Pflege“, „Zubehör“ etc. sind **nur Prüfideen**, niemals automatisch zu erzeugende Standardkategorien. Eine Kategorie wird nur angelegt, wenn dort mindestens drei sachlich unterschiedliche, realistische Beitragsabsichten existieren; kein „drei Synonyme = drei Beiträge“. Die Beiträge werden erst später geplant und geschrieben.

**Doppelte Suchthemen vermeiden:** Jedes Produkt gehört zu genau einer letzten CORE-Seite; Einsatzorte können über Verlinkung auf dieselbe Seite führen. Magazin und Anzeigenmarkt haben eigene Rollen und werden nicht mechanisch gespiegelt.

## Verbindliche Präzisierung 09.11.2026: Kategorie/Beitrag
- **Letzte WordPress-Seite ist IMMER genau ein fachlich konkreter Robotertyp / eine klar umrissene Produktfunktion**, keine generische Branche, keine bloße breite Robotik-Familie und nicht jedes Hersteller-Modell.
- Die zugehörigen flachen WordPress-Inhaltskategorien sind **ausschließlich Vertiefungen genau dieses Produkttyps**: z. B. Kosten, Fragen, Vergleiche, Probleme, Betrieb, Wartung – **nur bei echtem Inhaltspotenzial**, nicht pauschal identisch für alle Produkttypen.
- **Richtgröße: mindestens 3–5 klar verschiedene realistische Beitragsthemen** je neuer Inhaltskategorie. Die harte Mindestschwelle bleibt **3**, ohne Obergrenze. Bei nur 1–2 Themen **KEINE eigene Kategorie**: auf der Produktseite beantworten oder mit einer passenden bestehenden Kategorie desselben Robotertyps zusammenfassen. Keine künstlichen Synonyme oder Fülltexte.
- Jeder spätere Beitrag behandelt ausschließlich **diesen einen konkreten Robotertyp**. Die Kategorien sind fachlich einer Produktseite zugeordnet, in WordPress aber keine tatsächlich unter einer Seite verschachtelbaren Unterseiten-Taxonomien. Zuordnung und Navigation muss das Kategorieplugin später kontrolliert herstellen.
- Magazin/Journal und HivePress haben **eigene Nutzerabsichten**; sie verlinken auf Produktseite, statt dieselbe Frage nochmals zu publizieren.

## Register-/Finder-Folgearbeit
- Eigener Wegweiser im `../WISSENSDATENBANK/ROBOTERREGISTER/`, **KEINE zweite Datenhaltung**. In `RECHERCHE/PRODUKTE_V2_20261108.json` Revision **5** tragen alle 68 bestehenden Produktkandidaten einheitliche `finder_traits_v1`-Felder. Alle Attribute sind ausdrücklich **NICHT_RECHERCHIERT** – technisch gleiche Schemafelder, **keine** 68 fachlichen Trait-PASS.
- Finder liefert später nur geprüfte Produkte passend zur Nutzeraufgabe; auf der Ergebnisansicht dürfen **ergänzend** aktuelle und eindeutig zum Produkt-Owner passende Affiliate-Angebote mit Kennzeichnung **„Anzeige“** erscheinen. Ranking der Typen unabhängig von Provisionshöhe, nie erfundene Produktpreise/Verfügbarkeit, bei fehlenden Angeboten regulär reine Typberatung.
- `../PLUGINS/FOOTER_UMZUG_PRUEFUNG_20261109.md`: Original Footer-Umzug 1.1.1 (Hobbydepot) Code geprüft. Übertragungsprinzip nutzbar, **Original 1.1.1 wird auf ausdrücklichen Nutzerwunsch byteunverändert verwendet; 1.2.1 nur Archiv.** Original kann vorhandene Zielseiten ändern und frühere Portaltexte ersetzen; Importziele und Rechtstexte deshalb vor Übernahme sorgfältig prüfen. Das Original wird ohne neuen Entwicklungsauftrag NICHT umgebaut.
- **Kein neues Plugin/kein WordPress-Inhalt produziert; Nutzer muss nichts tun.**

## Fachlicher Strukturmaßstab für alle Nischen (09.11.2026)
Pro letzte WP-Seite **ein konkreter Robotertyp oder eine konkret umrissene Produktart**. Darunter **beliebig viele sinnvolle**, aber flache WP-Inhaltskategorien zu diesem einen Produkt, **jede** mit mindestens 3 fachlich unterschiedlichen möglichen Beiträgen, typischerweise 3–5. Ein oder zwei Themen bleiben auf der Produktseite bzw. in einer anderen passenden Inhaltskategorie. KEINE SEO-/Keywordrecherche in dieser fachlichen Runde; spätere Kontrolle durch das separate SEO-Plugin. Siehe `RECHERCHE/NISCHEN_KONZEPT_V3_20261109.md`.

## Verbindlicher Navigations-Namensvertrag vom 10.11.2026
1. **Alle sichtbaren Navigations-/Seiten-/Inhaltskategorienamen so kurz wie möglich, grundsätzlich ein oder zwei aussagekräftige Wörter.** Keine Füllwörter, Satzüberschriften, „Wie ...“, „Ratgeber für ...“, „Alles über ...“. Fachlich korrekt statt künstlich ultrakurz. Gleiche kurze Worte unter **anderen konkreten Produkt-Ownern** sind zulässig, gleiche Sachfragen nicht.
2. **Anzeige-Label, vollwertige Seiten-H1, Einführung, SEO-Titel und Metaangaben sind getrennte Felder.** Den vollständigen Fachbegriff im H1/Intro erklären; kein langer Navigationsname aus einer SEO-Suchphrase. Ein Begriff wie „Betrieb“ kann auf vielen *verschiedenen* konkreten Produktseiten stehen, ist keine globale Dublette.
3. **Hauptnavigation:** aus dokumentierter Hobbydepot-Planung (ungefähr **6–8 Slots**) für Robotik **8 Hauptwelten als vorläufiges fachliches Ziel**, **kein** Beweis einer technischen 8-Slot-Begrenzung des Robotik-Designs. Ein Hauptmenü nicht mit zehn überlangen Namen überfüllen; echte Untertypen niemals nur wegen Darstellung verwerfen.
4. **Eine einzige aktuelle Entwurfsnavigation im Master Revision 10:** `navigation_v1`; 10 `worlds_v1` sind Forschungs-Historie. Produkt- und Unterkategorie-Anzeigenamen `nav_short_v1` bzw. `content_nav_short_v1` folgen der 1–2-Wort-Regel.
5. Letzte WordPress-Seite = **konkretes Produkt bzw. konkreter Robotertyp**. Darunter nur individuelle Vertiefungskategorien zu diesem Produkt, jeweils **mindestens drei grob unterschiedliche mögliche Beiträge** (meist 3–5), **keine Obergrenze** pro Produkt. Der Kategorienname allein beweist keine Inhaltskapazität; detaillierte Ideen bleiben in ihren recherchierten Quellen.
6. **Aktuelle Fachphase ohne SEO-Recherche und ohne Schreibzugriff auf WordPress.** Kein Plugin, keine URLs, keine aktiven Kategorien/Artikel und keine anderen Portalbäume ändern. Spätere Keyword-/Kannibalisierungsprüfung macht das andere geplante Plugin. Konzept: `RECHERCHE/KURZNAMEN_HAUPTNAVIGATION_V4_20261110.md`.

## Käuferorientierte Oberfläche, gemeinsames Fachangebot – Nutzerbestätigung 10.11.2026 (AKTUELL)
- Hauptnavigation **7 vorläufige kaufnahe Kategorien + 1 sichtbarer Menüpunkt „Industrie“**. Industrie ist **eigener CORE-Einstieg**, zuerst mit **3** fachlichen Landingpages „Fertigung“, „Anlagen“, „Medizin & Labor“. Forschung als Magazin-Querverweis; keine künstliche vierte Industrieproduktwelt. Seiten müssen direkt per regulärem Link verknüpft und für Besucher und Suchmaschinen erreichbar sein. Die acht gleichrangigen V4-Produktwelten werden **NICHT** als sichtbares Hauptmenü gleichzeitig fortgeführt.
- **Magazin/Journal, Roboterglossar, Roboterregister, Roboterfinder und HivePress-Anzeigenmarkt bleiben jeweils GEMEINSAME Portalfunktionen für Privat, Betriebe, Industrie und Forschung.** Themenrubriken und Filter innerhalb eines gemeinsamen Bereichs sind sinnvoll; zweite Privat-/Industrie-Ausgaben, identische Lexikon-Einträge, Modell- oder Produktkopien sind verboten.
- Alle konkreten Robotertypen/Software-/Komponenten-Produktarten verbleiben auf **je genau EINER CORE-Produktseite**, darunter flache **nur zu diesem Produkt gehörende** Inhaltskategorien mit mindestens 3 unterschiedlichen möglichen Beiträgen, Anzahl ohne Obergrenze. Industrie-Übersichten und Kaufnavigationskarten dürfen über Links auf dieselbe Produktseite verweisen.
- Sichtbare Label 1–2 aussagekräftige Wörter, H1/Intro/Meta ausführlicher möglich. Hauptzielgruppe tatsächliche Käufer (Privatkunden/kleinere Betriebe); Industrie vollständig zugänglich, aber Startseite nicht darauf ausgerichtet. Ob sieben vorgeschlagene Käuferthemen wirtschaftlich tragfähig sind, bleibt **ohne Partnernachweise OFFEN**.
- Fachliche Detailentscheidung im [Zielgruppen-/Navigationskonzept V5](RECHERCHE/ZIELGRUPPEN_NAVIGATION_V5_20261110.md). **Einziger Master jetzt Revision 11, Feld `audience_navigation_v2`.** Kein WordPress-Import, kein SEO-Test und keine Pluginänderung.

## Nachtrag 10.11.2026 – Nutzergrenze: Nutzung statt Herkunft
1. Hauptzielgruppe und Hauptnavigation: Privatkunden UND kleine Betriebe einschließlich Handwerk, kleine Fertigung, Gastronomie, Handel und Landwirtschaft. Auch ursprünglich industriell entwickelte Robotertypen sind dort einzubeziehen, sofern hier sinnvoll einsetzbar.
2. Der nachgeordnete Industrie-Zugang ist für wirklich exklusive großindustrielle/hochspezialisierte Einsatzbereiche und Querverweise. Ausschluss aus dem Käuferteil erst nach Belegprüfung; offene Fälle nicht automatisch als Industrie klassifizieren.
3. Jede konkrete Produktart hat genau EINE sachlich begründete CORE-Produktseite. Mehrere Einstiege verlinken auf dieselbe Seite, keine geklonten Produkt-/Affiliateseiten.
4. Alle weiteren Bereiche **vollständig gemeinsam** für Privat, Kleinbetriebe, Industrie und Forschung: EIN Magazin, EIN Glossar, EIN Hersteller-Modellregister, EIN Roboterfinder, EIN HivePress-Anzeigenmarkt. Fachfilter erlaubt, keine Privat-/Industrie-Kopien.
5. Reale Nutzung, technische Sicherheit, Bezugswege und Affiliate-Partner sind unterschiedliche Prüfungen. Ein Herstellerbeispiel beweist keine Zulässigkeit oder Affiliate-Provision. Master Revision 12: 68 Grundtypen, 140 Randfälle. Kein WordPress-Import.
