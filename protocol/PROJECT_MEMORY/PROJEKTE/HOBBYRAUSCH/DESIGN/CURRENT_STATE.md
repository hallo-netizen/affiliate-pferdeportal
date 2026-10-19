# HOBBYRAUSCH – DESIGN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-19
STATUS: **1.50.693 DETAIL-TEXTROLLOUT 395/395 LOCAL HARD PASS / LIVE-ABNAHME OFFEN**

Zielvertrag: **ZV-HOBBYRAUSCH-DESIGN-001 Fassung 5.4 / 2026-10-19**

## AKTUELLER BELASTBARER STAND

- Schuhmacherei-Pilotstruktur ist vom Nutzer inhaltlich/visuell als Grundlage für den Gesamtrollout bestätigt.
- Sichtbarer Detail-Hobby-Lead bleibt separat: ca. 45–60 Wörter, erklärt Was ist das Hobby / was macht man / was ist typisch.
- Aufklappbarer Vertiefungstext: ca. 150–200 Wörter **zusätzlich** zum Lead, direkte du-Ansprache, je nach Inhalt 1–2 Absätze; im aktuellen Rollout 2 Absätze.
- Kacheluntertitel: kurze konkrete Inhaltsaussage ohne Füllwörter/Füllverben oder Generatorfloskeln.
- Gesamtrollout **1.50.693** ist lokal gebaut:
  - 395/395 Detail-Hubs;
  - Lead 45–60 Wörter;
  - aufklappbarer Text 150–187 Wörter;
  - zwei Absätze je aufklappbarem Text;
  - 0 Regelverstöße gegen die gebundenen Füll-/Generatorphrasen;
  - 0 interne Textdoppelungen im automatisierten Satzähnlichkeitscheck;
  - semantische Querfehler aus dem Zwischenstand korrigiert, u. a. falsche Pilz-, Meerwasser- und Fundhinweise.
- Schuhmacherei-Lead bleibt exakt wie vom Nutzer bestätigt.
- Kacheltexte wurden auf content-only Kurzfassungen umgestellt; Schuhmacherei besitzt weiterhin neun fachlich konkrete Spezialuntertitel.
- Lokale Technik-/Regression:
  - PHP **123/123 PASS**;
  - Positiv-/Negativ-Render-E2E für Schuhmacherei, Airbrush-Kontrollseite und direkten Category-Term PASS;
  - Release-/Templatekette V150693 PASS;
  - 8/8 Startseiten-Weltbilder byte-identisch zu 1.50.691;
  - Hauptkategorie-Basis unverändert;
  - verbotene Füllphrasen im 395er Textbestand und Kachelrenderer: 0.
- Lokales Artefakt:
  `AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.693_DETAIL_TEXT_ROLLOUT_LOCAL_HARD_PASS.zip`
- SHA-256:
  `558a345042c9acaa488b01ce543c2f9d7defc4406f5243ee17f90b4363975d54`
- **Kein Live-PASS:** 1.50.693 ist noch nicht im echten WordPress-Frontend abgenommen.

## ERSTER OFFENER BLOCKER

Der vollständige 395er Text-/Kachelrollout ist lokal hart geprüft, aber **noch nicht live sichtbar abgenommen**.

## EXAKT EINE NEXT ACTION

**1.50.693 als normales vollständiges Template-Kit installieren und mehrere repräsentative Detail-Hubs live prüfen: Schuhmacherei, mindestens je ein Hobby aus Gestalten/Fertigen/Technik/Forschen/Pflanzen/Tiere/Bewegen/Sammeln sowie einen direkten Category-Term. Bei Abweichung nicht raten, sondern exakt den Livepfad reproduzieren.**

## ARBEITSBINDUNG

- Campus-/Dokubranche: `hobbyroom/project-memory-campus-v1-20260905`.
- Plugin: **HD-003 – Hobby Depot Design / Template Kit**.
- Keine Massen-Wortersetzungen; Textregeln bleiben redaktionelle Qualitätsgrenze.
- Kein Architekturumbau.
- Live bestätigte Header-/Navigations-, Startseiten- und Hauptkategorie-Hero-Bindungen nicht verändern.

## NICHT ANFASSEN

- Kategoriebaum/HD-001/HD-004;
- Affiliate-Slotarchitektur;
- Meta-Titel/SEO-Titel;
- Startseiten-Weltbilder 1.50.691;
- Hauptkategorie-Heros.
