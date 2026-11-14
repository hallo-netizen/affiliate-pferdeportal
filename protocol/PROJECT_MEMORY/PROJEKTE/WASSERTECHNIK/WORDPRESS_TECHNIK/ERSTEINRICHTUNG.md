# Wassertechnik – WordPress-Ersteinrichtung / KISS-Checkliste

**Nur vorbereiten, nicht am bestehenden Portal ausführen.**

1. Neues Hosting/neue Domain und isolierte, leere WordPress-Instanz als Eigentum des Projekts nachweisen; kein Login/DB/Uploads eines anderen Portals nutzen.
2. WordPress-Core unverändert installieren; saubere Permalink-Struktur und Sprache/Zeitzone festlegen; keine Astra-/Kubio-Altlasten kopieren.
3. Backup/Restore für die neue Instanz mit Test-Restore sicherstellen; Original-Datenbank vor jedem ersten Import sichern.
4. Die tatsächlich geplante Theme-/Design-Identität festlegen, erst dann genau ein eigenes Designplugin; kein zweites Navigations-/Kachel-Plugin.
5. Benötigte Plugins einzeln prüfen: HivePress (Anzeigen), Yoast SEO/Sitemap, ggf. WPForms (Kontakt), eigenes Wassertechnik-Kategorie-Workflow-Plugin **erst nach neutraler Portierung**, später Affiliate-Zentrale. Keine Plugin-Dopplung.
6. Pflichtseiten und Navigation: Startseite, Impressum, Datenschutz, Kontakt, Werbekennzeichnung, Magazin, Anzeigenmarkt; tatsächliche Formulare testen.
7. Zielstruktur Hauptseite → Unterseite → Inhaltskategorie → Beitrag und getrennte HivePress-Anzeigenkategorien festlegen; keine Blindimporte.
8. SEO: URLs, Indexierungsfreigaben, Canonicals, Sitemap, robots, Menüs, interne Links; Staging bis zur Abnahme nicht indexieren.
9. Bilder: zentrale Bildlogik der anderen Portale nur als Lesevorlage; Motive fachlich Wassertechnik und nicht aus Fremdprojekten live übernehmen.
10. Erster Import ausschließlich als Vorschau mit 0 Änderungen; nach Freigabe ADD-only auf neuer Site. Danach WordPress-IDs, Slugs, Menüs, Desktop/Mobil und Darstellungsweg prüfen.
11. Sicherheit/Performance: Updates, Zugänge, Rollen, Caching, Bildgrößen, Datenschutz; kein Frontend-Netzwerkabruf zur Affiliate-Bannerzuordnung.
12. Abschluss erst nach echter Staging-/Live-Prüfung, nicht nach bloßer lokaler Simulation.

**Aus dem Archiv darf aktuell nichts automatisch in WordPress geschrieben werden.**
