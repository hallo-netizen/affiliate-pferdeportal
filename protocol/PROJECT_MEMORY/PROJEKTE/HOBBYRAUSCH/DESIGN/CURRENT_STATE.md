# HOBBYRAUSCH – DESIGN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-19
STATUS: **1.50.693 VERWORFEN / LEAD-TEXTREGEL + FARBRAHMEN NICHT KORREKT AUSGEROLLT / NEUAUFBAU AUF 1.50.692-BASIS**

Zielvertrag: **ZV-HOBBYRAUSCH-DESIGN-001 Fassung 5.5 / 2026-10-19**

## AKTUELLER BELASTBARER STAND

- Schuhmacherei bleibt der inhaltlich bestätigte Musterfall.
- Der sichtbare Lead muss ca. 45–60 Wörter haben und einem Leser ohne Vorwissen unmittelbar erklären:
  1. was das Hobby bzw. der unbekannte Begriff ist;
  2. was man dabei konkret tut;
  3. was dafür typischerweise gebraucht/vorausgesetzt wird;
  4. was daran charakteristisch oder reizvoll ist, soweit es natürlich in den Kurzüberblick passt.
- Bei unbekannten Begriffen beginnt der Lead mit einer echten Definition/Erklärung. Kein vorgeschalteter Kurs-/Anmoderationssatz.
- Der aufgeklappte Text umfasst ca. 150–200 Wörter zusätzlich zum Lead, direkte natürliche du-Ansprache, 1–2 Absätze.
- Kacheluntertitel bleiben kurz, konkret und ohne Füllwörter/Füllverben.
- Nutzer-Livebefund 1.50.693:
  - zahlreiche Leads beginnen mit künstlichen Vorsätzen wie „Wenn du loslegst …“, „Zum Kennenlernen …“, „Am Anfang bekommst du …“;
  - diese Sätze tragen kaum Fachinformation und verstoßen gegen die Textregel;
  - bei erklärungsbedürftigen Themen wie Cyanotypie, Bromelien oder Asselhaltung fehlt die unmittelbare Begriffserklärung;
  - der helle Petrol-/Türkisblock wurde technisch nur für Schuhmacherei per Sonderklasse ausgerollt statt für alle Detail-Hubs.
- Root Cause im 1.50.693-Generator belegt:
  - separate Liste künstlicher Lead-Vorsätze;
  - CSS-Selektor `.hd-catlevel-intro-schuhmacherei-v150693 .hd-catlevel-lead` begrenzt den Farbrahmen auf Schuhmacherei.
- Deshalb ist 1.50.693 **kein gültiger Kandidat** und kein Hard-PASS mehr.

## ERSTER OFFENER BLOCKER

Der komplette 395er Detail-Hub-Bestand muss nach der bereits vorhandenen Textregel **inhaltlich neu geschrieben** werden; keine kosmetische Ersetzung der Vorsatzphrasen.

## EXAKT EINE NEXT ACTION

**Auf sauberer 1.50.692-Basis den 395er Detail-Hub-Rollout neu bauen: jeder sichtbare Lead beginnt mit echter Erklärung/Definition und liefert in 45–60 Wörtern einen konkreten Kurzüberblick; Farbrahmen für alle Detail-Leads; aufgeklappter Text 150–200 Wörter zusätzlich, natürliche direkte Ansprache, 1–2 Absätze; Kacheluntertitel knapp und sachlich. Danach vollständige POS/NEG-/Regression-QA.**

## ARBEITSBINDUNG

- Campus-/Dokubranche: `hobbyroom/project-memory-campus-v1-20260905`.
- Plugin: **HD-003 – Hobby Depot Design / Template Kit**.
- Keine neue Architektur.
- Keine Massenersetzung schlechter Vorsätze durch neue Vorsätze.
- Fachinhalt vor Wortzahl; jeder Satz muss Information tragen.
- Pferdeatelier dient nur als redaktionelle Referenz, nicht als Statusquelle.

## NICHT ANFASSEN

- Kategoriebaum/HD-001/HD-004;
- Affiliate-Slotarchitektur;
- Meta-/SEO-Titel;
- Startseiten-Weltbilder;
- Hauptkategorie-Heros;
- live bestätigte Header-/Navigation.
