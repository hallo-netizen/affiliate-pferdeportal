# HOBBYRAUSCH – DESIGN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-19
STATUS: **1.50.692 SCHUHMACHEREI-TEXTPILOT DOKUMENTIERT GEBAUT / STATISCHE QA PASS / VOLLSTÄNDIGE POSITIV-NEGATIV-E2E-PRÜFUNG OFFEN / KEIN GESAMTROLLOUT**

Zielvertrag: **ZV-HOBBYRAUSCH-DESIGN-001 Fassung 5.4 / 2026-10-19**

## AKTUELLER BELASTBARER STAND

- Letzter ausdrücklich vom Nutzer live abgenommener Detail-Musterfall: **Kettenhemd flechten 1.50.689**.
- 1.50.690 generalisiert dessen Reihenfolge im gemeinsamen WP_Post-basierten Detailseitenrenderer: **Text → Banner → kompletter Kachelblock → Empfehlungen → bis zu 4 Beiträge → vorhandener weiterer Werbeplatz**.
- Die zusätzlich dokumentierten **16 direkten Category-Term-Knoten** sind weiterhin nicht als eigener Runtimepfad live verifiziert; kein PASS raten.
- Vollpaket **1.50.691** wurde gebaut: normale Plugin-Überinstallation, 8 neue ruhige Startseiten-Weltbilder, Querbanner unter den 8 Welten, Hauptkategorie-Heros unverändert. Ein ausdrücklicher Nutzer-Live-PASS für 1.50.691 ist nicht belegt.
- Der vorhandene Detail-Hobbytextbestand enthält nach Nutzerbefund unzulässige Generator-/Schablonensprache. Autoritative Fehlerquelle: **HRD-074**.
- Verbindliche Textlogik ab Zielvertrag 5.4:
  - sichtbarer Lead ca. 45–60 Wörter: **Was ist das Hobby? Was macht man? Was ist typisch?**
  - Lead ohne Navigation/Kachelauflistung; ruhiger heller Petrol-/Türkisblock zulässig;
  - aufgeklappter Rest fachlich zusammenhängend;
  - natürliche Vertiefungsüberschrift; neutral höchstens **Mehr zu <Hobby>**; **Themen im Überblick** entfällt;
  - Kacheluntertitel konkret-fachlich; keine kalten Generatorfloskeln.
- Pilot **1.50.692 – Schuhmacherei** ist im Buildstand dokumentiert:
  - 51-Wort-Einsteigerlead;
  - 164 Wörter Gesamttext;
  - Überschrift `Mehr zur Schuhmacherei`;
  - 9 konkrete Kacheluntertitel;
  - heller Petrolblock nur im Pilot;
  - Startseite, Hauptkategorie-Heros und andere Hobbytexte unverändert.
- Dokumentiertes Artefakt: `AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.692_SCHUHMACHEREI_TEXT_PILOT.zip`
- Dokumentierte SHA-256: `c9a45879b268c60d2d825be0225bfe0d1e03f37f219dd6282498c53b75e2d86a`
- Dokumentierte statische QA: PHP **120/120**, ZIP PASS, aktive V150692-Kette PASS.
- **Nicht belegt:** vollständige lokale Positiv- UND Negativ-E2E-Simulation des realen Schuhmacherei-Renderpfads. Deshalb noch keine Deployment-/Live-PASS-Freigabe.
- Das 1.50.692-Artefakt ist nicht als isoliertes `CURRENT.zip` synchronisiert; das bleibt bis zum vollständigen Hard-PASS korrekt.

## ERSTER OFFENER BLOCKER

Die projektweite Hard Rule verlangt vor Upload/Deployment eine dokumentierte **positive und negative E2E-Simulation des real relevanten Pfads**. Dieser Nachweis ist für 1.50.692 in der aktuellen Evidence noch nicht vorhanden.

## EXAKT EINE NEXT ACTION

**1.50.692 lokal über den tatsächlich gerouteten Schuhmacherei-Pfad vollständig positiv und negativ simulieren – inklusive Kontrollseite ohne Pilotänderung, Release-/Templatekette, Leadblock, Text, Vertiefungsüberschrift, 9 Kacheluntertitel sowie Regression von Startseite und Hauptkategorie-Heros. Erst bei PASS das normale Vollplugin zur Nutzer-Sichtabnahme ausgeben.**

## ARBEITSBINDUNG

- Campus-/Dokubranche: `hobbyroom/project-memory-campus-v1-20260905`.
- Plugin: **HD-003 – Hobby Depot Design / Template Kit**.
- Fachziel: Zielvertrag 5.4 + verbindliche Textregeln.
- Gesamtrollout der 395 Detail-Hubs **erst nach Nutzerabnahme des Schuhmacherei-Piloten**.
- Keine Massen-Wortersetzungen; Texte redaktionell neu schreiben.
- Kein Architekturumbau.

## NICHT ANFASSEN

- live abgenommenen Kettenhemd-Aufbau nicht verändern;
- Startseiten-Weltbilder 1.50.691 nicht erneut umbauen;
- Hauptkategorie-Heros unverändert lassen;
- Kategoriebaum/HD-001/HD-004 nicht verändern;
- Meta-Titel weiterhin separater späterer SEO-Schritt;
- keine neuen Affiliate-Slottypen.
