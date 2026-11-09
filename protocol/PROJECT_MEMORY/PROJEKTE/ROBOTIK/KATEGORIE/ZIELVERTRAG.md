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
- `../PLUGINS/FOOTER_UMZUG_PRUEFUNG_20261109.md`: Original Footer-Umzug 1.1.1 (Hobbydepot) Code geprüft. Übertragungsprinzip nutzbar, **Original nicht unverändert auf Robotik einsetzen**: schreibt/aktualisiert bestehende Seiten, Pferde→Hobby-Alttexte und fehlende Vorschau. Isolation/Prüfmodus und Impressum/Datenschutz-Ausnahme vor echtem Import nötig.
- **Kein neues Plugin/kein WordPress-Inhalt produziert; Nutzer muss nichts tun.**
