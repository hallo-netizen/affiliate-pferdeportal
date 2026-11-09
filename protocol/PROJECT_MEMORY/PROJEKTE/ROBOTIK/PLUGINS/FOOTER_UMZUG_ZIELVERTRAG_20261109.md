# Robotik – Footer-Umzug nur Seiten und deren Inhalt, KEIN Design
**Benutzerwunsch verbindlich (09.11.2026).** Das Footer-Übertragungs-Plugin soll Arbeit sparen: benötigte Footer-Seiten samt Text/Links/Zuordnung, Menüs und – wenn passend – Footer-Widgets von einem der bestehenden Portale nach Robotik übernehmen. **Robotik-Design wird unabhängig im DESIGN-Büro entwickelt.**

## Nachprüfung gegen Original 1.1.1
Original aus Hobbydepot `TOOL-FOOTER-UMZUG/CURRENT.zip` kann tatsächlich Footer-Menüs, verlinkte Seiten samt Inhalt, Footer-Widgets und Zuordnungen übertragen. Design/Astra-Einstellungen werden laut Code nicht übernommen. **Risiken:** alte Ersetzungen Pferde→Hobby, auch `wp_update_post` für bereits bestehende Zielseiten, Menü-/Widget-Areas nach Theme-IDs und **keine obligatorische Vorschau**.

## Für Robotik nur diese sichere Variante zulassen
1. **Seiten auswählen**, die tatsächlich übernommen werden sollen. Keine unnötigen Dateien; ein Footer-Export/Import reicht.
2. **Vorschau vor Import**: alle beabsichtigten neuen Seiten, bestehenden Slug-Treffer, Menülinks und Widgetänderungen anzeigen. Nichts ohne Freigabe überschreiben.
3. Keine Pferde/Hobby-Textumwandlungen; nur klare Portal-/Domain-Verweise zielbezogen ersetzen, ohne Rechts-/Fachbegriffe zu erraten.
4. **Rechtstexte** (Impressum, Datenschutz, AGB, Werbe-/Cookiehinweise) nur als Vorlagen/Entwürfe; je Robotik-Zielseite inhaltlich prüfen, keine automatische unkontrollierte Veröffentlichung.
5. Design, Farben, Spalten, Template- und WordPress-Core-Einstellungen **nicht** übernehmen; Widgetbereiche auf existierendem Robotik-Theme prüfen.
6. Nach einmaliger Freigabe Import durchführen und exakt diese Seiten, Menüs/Links im WP-Backend + Frontend rücklesen. Keine erneuten Vollimporte.

**Stand 09.11.2026:** Robotik-Testvariante **1.2.1** wurde erstellt und als getrenntes ZIP im Robotik-Pluginbüro archiviert (lokale Prüfungen PASS, WordPress-Live-PASS offen; **noch nicht installiert**). Die bestehende 1.1.1 auf Quellseiten braucht nicht ersetzt zu werden. Nur der **sichere** 1.2.1-Importer darf die alte 1.1.1-Exportdatei in Robotik übernehmen – zunächst als **Entwürfe**. Layout/Widgets bleiben Designaufgabe. Andere Portale unverändert.
