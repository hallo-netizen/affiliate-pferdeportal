# Roboter-Footer-Umzug: isolierte Testversion 1.2.1
**Stand 09.11.2026. ZIP ist auf GitHub im Robotik-Pluginbüro bytegleich zum lokalen Download hinterlegt.**

Original 1.1.1 (Hobbydepot) durch GitHub-ZIP PHP-Code geprüft. Für Robotik wurde eine isolierte sichere 1.2.1-Fassung mit gleicher WordPress-Plugin-Slug `footer-umzug` erstellt und lokal getestet:
- Übernimmt Footer-Menüs und die darin verlinkten WP-Seiten samt Inhalt; **KEIN Design, keine Farben, keine Layoutübertragung**.
- Versteht das echte Export-JSON-Format der alten 1.1.1; **bestehende Quellseiten brauchen keine neue Plugininstallation**.
- Zwingend **Vorschau vor Import** und ausdrückliche Bestätigung. Neue Seiten nur **als Entwurf**; bestehende Seiten, bestehende Menüs und deren Inhalte werden **nicht** überschrieben.
- Portalfremde Marken-/Domaintexte werden **nicht geraten/automatisch umgeschrieben**, sondern als Hinweis gemeldet. Impressum/Datenschutz dürfen nicht ohne Fachprüfung veröffentlicht werden.
- Keine Übernahme alter Footer-Widgets; dies ist bewusst **nur Seiten- und Menüziel**, das Design/Widgets kommen aus dem Robotik-Designbüro.
- Export 1.2.1 optional auf Quellseite möglich, Legacy-Export 1.1.1 wird auf Robotik eingelesen.
- Keine WordPress-Core-Änderung/keine Zusatz-DB.

**Technische Prüfungen**: PHP `php -l` PASS; ZIP CRC PASS; mit simuliertem ORIGINAL-1.1.1-JSON-Format zwei Seiten, verknüpften Menüpunkt und Footer-Location erfolgreich normalisiert; ungültiges Exportformat abgewiesen. **WordPress-LIVE-TEST noch NICHT erfolgt**.
**Versionsstand**: Testversion 1.2.1, noch keine Nutzerinstallation bestätigt; andere Portale nicht angefasst. Installation nur auf Robotik, Quellseite darf altes 1.1.1 behalten.
