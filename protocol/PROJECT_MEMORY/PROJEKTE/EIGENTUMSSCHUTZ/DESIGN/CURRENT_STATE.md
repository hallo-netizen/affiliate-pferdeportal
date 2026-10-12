# HAB & BEWAHR – DESIGN – CURRENT STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-12
STATUS: **ISOLIERTER DESIGNKANDIDAT 0.1.1 MIT NAVIGATION LOKAL GEPRÜFT / WORDPRESS-LIVE OFFEN**

## Ziel / bindende Nutzerentscheidung
Erst eine **grobe Visualisierung** der bestehenden echten Website-Struktur, keine fertige CI/SEO-Produktion. Grobe Orientierung am Hub-/Kartenaufbau des Hobby-Depot-Design-Plugins; keine Architekturübernahme. Farbwelt warmes Terrakotta, Salbei, Anthrazit, cremefarbener Hintergrund. Wortmarke **Hab & Bewahr** mit Bogen, Claim **„Wissen. Vergleichen. Besser schützen.“**; Hero **„Was dir gehört, soll dir bleiben.“**. Sechs Gefahrenwelten + Magazin + Dienstleister, vorhandenes R2-Profil. Vier echte, eindeutig markierte Testartikel; dieselben Beispiele nur als Kacheln auf anderen Kategorieebenen.

## Aktueller Kandidat (nur Chat-Artefakt)
`HAB_UND_BEWAHR_DESIGN_VORSCHAU_0.1.1_KATEGORIENNAVIGATION.zip`
SHA-256: `a4f1201fc882227599f0dc3c20fc2abb000e327ef1f7a758b3999a5843abf51a`

- Eigener deaktivierbarer Visualisierungsplugin, ohne Eingriff in HD-001.
- Echtgebundene 354 WP-Zielobjekte / 141 CORE-Kategorien aus R2-Readback vom 2026-10-12, Status COMPLETE/PASS.
- Dynamische Seitenhierarchie per vorhandenen Objekt-IDs.
- Vier DEMO-Artikel werden einmalig bei Aktivierung erstellt, je eine vorhandene CORE-Kategorie. `noindex`; bei Deaktivierung in Entwurf. Kein Content-Massenimport.
- Startseite, 6 Weltseiten, Unterhubs, Terminalkategorien, Demo-Artikelseite; Layoutbeispiele für Magazin und Dienstleister.
- **0.1.1 – Hauptnavigation:** zusätzliche zweite Header-Zeile mit sechs anklickbaren Gefahrenwelten. Klapp-Menüs visualisieren die realen **31 Bereiche → 45 Unterbereiche → 141 Blattkategorien** aus dem unveränderten R2-Baum. Links auf WP-Objekt-IDs, Kategorieblätter optional erweiterbar, ESC/außen klicken, CSS-Layouts für 1440/966/390 vorgesehen.
- Beispielfotos und rasterbasierte Logo-Referenz sind Ausschnitte aus dem bereitgestellten Chat-Mockup vom 8.10.; **Master-Logo nicht separat vorhanden, pixelgenaue Freigabe OFFEN**.
- Arbeitsfarben des Erstwurfs (nicht behauptete finale CI-Farbwerte): Terrakotta `#B35C40`, Salbei `#65745F`, Anthrazit `#252825`, Hintergrund `#FAF8F4`.
- Hobby-Depot-Plugin-Stand 1.50.635 in dessen DESIGN-Current verifiziert, Original-ZIP hier nicht verfügbar; visuelle Orientierung, keine Behauptung einer Codeübernahme.

## Nachweise
`php -l` Hauptplugin und Template PASS. Sechs lokale WordPress-Mock-Seiten PASS; vollständige Menüstruktur (6/31/45/141) und Linkziele PASS; JS-Logik Geschwister schließen / ESC / Klick außerhalb PASS; CSS-Balancierung und ZIP-Integrität PASS. **Automatisierter Chromium-Browser-Test durch Umgebung (ERR_BLOCKED_BY_ADMINISTRATOR) verhindert; echte WordPress-Darstellung OFFEN.** Keine Behauptung von Live-PASS.

## Schutzgrenze
Keine Synchronisierung / Mutation des R2-Kategoriebaums. Kein Update des Hobbyrausch-Template-Kits. Keine zusätzlichen Plugins. Kein Test auf Nutzer-WordPress durch GitHub allein.

## EXAKT EINE NEXT ACTION
Bestehendes Design-Vorschau-Plugin von 0.1.0 auf **0.1.1** aktualisieren; dann live Menü (alle sechs Gefahrenwelten, aufklappbare Bereiche/Blätter) und die Darstellungen bei Desktop und schmalem Fenster prüfen. Nur nötige visuelle Korrekturen, Kategoriebaum und Demoartikel unverändert.
