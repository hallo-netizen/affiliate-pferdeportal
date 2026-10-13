# HAB & BEWAHR – KONZEPT – CURRENT STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-13
STATUS: **R3/V6 STRUKTUR UND REDAKTIONELLE ABGRENZUNG GEPRÜFT / GOOGLE-SERP-NACHWEISE NOCH OFFEN / WORDPRESS R2 UNVERÄNDERT**

## Zielvertrag – verbindlich
- Sechs bestehende Gefahrenwelten und **31 Hauptthemenbereiche** erhalten; drei Portalsäulen CORE, Magazin, Dienstleister bleiben bestehen.
- **Jede anklickbare Zwischenebene muss 3 bis 10 fachlich sinnvolle unmittelbare Unterpunkte haben.** Keine Klick-Einzelkinder, keine überflüssigen Zwei-Kind-Ebenen.
- Keine künstlichen Kategorien, keine doppelte redaktionelle Zuständigkeit und keine Artikelduplikate. Alle alten Keywords/Artikel-Intents erhalten und bei Umhängung genau einem Owner zuordnen.
- Keine WordPress-Schreibvorgänge, ID-/Slug-/URL-Änderungen oder neue bezahlte DataForSEO-Abfragen ohne abgeschlossene Freigabe.

## Einzige WordPress-Live-Wahrheit: R2
Zuletzt bestätigter WordPress-Readback vom 12.10.2026: Kategorie-Plugin **1.14.8.17**, R2-Revision `HB-SECURITY-CATEGORY-OWNER-CORRECTIONS-20261012-R2+655852190d183cc9`, 354/354 physische Zielobjekte, Status COMPLETE, 0 Fehler. R2: sechs Welten, 31 Bereiche, 45 Unterbereiche, 141 CORE-Blattkategorien und 704 alte Artikelideen. Maßgebliche Ursprungsdatei `HAB_UND_BEWAHR_KATEGORIENPROFIL_20261012_R2.json`, SHA256 `bd1594d7012ae36f787cf9ca2039e657d922e2954f3e097cc3f2b40482d42055`.
**R3/V6 ist NICHT live, wurde NICHT synchronisiert und ist KEIN Importprofil.**

## Einziger aktueller V6-Fachentwurf
- **Vollständiger redaktioneller Plan im GitHub-Büro:** `KONZEPT/R3_V6_144_KATEGORIEN_432_IDEEN_OWNER_BEREINIGT_20261013.md`, Commit `7bbb40b1c44b396490e61b7732ca3001bcf6f9df` (nach finaler Abgrenzung).
- **Strukturdelta:** `KONZEPT/R3_48_UNTERBEREICHE_KANDIDATEN_20261013.md` (48 neue Unterbereiche, 144 Blattkandidaten).
- **V6-QA-Datensatz:** `KONZEPT/R3_V6_QA_20261013.json`, lokal wiederholbare Prüfbedingungen und Grenzen. Lokale vollständige Maschinenkopie `HAB_R3_V6_FACHPLAN_NICHT_IMPORTIEREN_20261013.json` mit SHA256 `e7abdcfa9782940776740cf425d9f0db6f69329d33a6269340123189fc7a25bc`. **Diese JSON liegt nur im Chat-Arbeitscontainer, nicht im Campus.** Der Campus enthält die vollständigen 144×3 Artikelideen im obigen Markdown und das Strukturdelta.
- Ältere V2/V3/V4/V5-Pläne sind **nur Historie**, keine aktuelle zweite Autorität.

## V6 – real geprüft
- 6/6 Welten, 31/31 Themenbereiche **mit 3–10 Unterbereichen**, 93/93 Unterbereiche **mit 3–10 Blattkategorien**, insgesamt 285 CORE-Blätter (= 141 alt und unverändert +144 neue Kandidaten). Auch bestehende Magazin-/Dienstleister-Zweige bleiben strukturell regelkonform.
- 432 konkrete, genau einem neuen Kategorie-Owner zugeordnete Artikelvorschläge; 704 R2-Titel im Original unverändert; **0 exakt gleiche neue/alte/neue-neue Titel**. **Keine vollständige semantische Google-Doppelungsprüfung!**
- 19 fachliche, noch nicht ausgeführte **Umhängungen statt Kopien:** **9 Alt→Alt**, **10 Alt→Neu**. Nach hypothetischer Umhängung behalten alle Quellkategorien >=3 eigene Themen.
- Neu erkannte reale redaktionelle Doppelbelegung bei **Koax/Satellitenschutz**: Altentwurf behandelte sie in „Datenleitungen & Überspannung“ und „Antennen & Blitzschutz“. V6 korrigiert: **Koax/Sat nur Antennen**, Datenleitungen nur DSL/Glasfaser/LAN/Switch/PoE. 3–10-Regel und 432 eindeutige Titel nach Korrektur weiterhin PASS.
- Automatisch alle alten/neuen Titel auf lexikalische Nähe geprüft: **155** Paarsignale Score >=0,29, darunter **3** >=0,50; kein automatischer SEO-Beweis. **14 fachliche Ownership-Kanten** sowie alle **10 auffälligen Kategoriebezeichnungs-Nähesituationen** redaktionell eingeordnet; Details im V6-Plan. Fachquellen VDE für Antennen/Telekommunikations-Überspannung, ADAC für Fahrzeugbrand-/Gas sowie Verbraucherzentrale für Steckersolar herangezogen – **keine Google-Top-10-SEO-Freigabe**.
- Kein WordPress-Schreibvorgang, kein zusätzlicher bezahlter Provideraufruf.

## Erster offener Fehler / harte Release-Sperre
**HB-CONCEPT-002:** Alle 144 neuen Kategorie-Owner benötigen noch organische SERP-/Nachfrage-/Kannibalisierungsprüfung; historische DataForSEO Keyword-Auswertung nur 128 von 282 geliefert, 154 fehlend/UNBEKANNT; historische SERP-Felder 16 von 20 vollständig, vier nicht. Redaktionelle Unterscheidung ist nicht gleich Google-SERP-Unterscheidung. Die 21 alten R2-Owner-Fälle sind nur fachlich vorgeprüft.
**HB-CONCEPT-004:** Der vorhandene Kategorie-Plugin-Validator 1.14.8.17 erzwingt 3–10 noch nicht auf jeder Zwischenebene. Vor einem R3-Release minimal ergänzen und positiv/negativ nachtesten, keine Architekturänderung.
**Weitere Sperre:** Bestehende URLs/Slugs dürfen ohne Folgenprüfung und Redirect-Plan nicht verändert werden.

## EXAKT EINE NEXT ACTION
**R3/V6 Suchintent-/Owner-Abnahme fortsetzen:** alle 144 neuen Kategorie-Owner systematisch mit ihrer bisherigen R2-Zuständigkeit und echten organischen Suchergebnissen abgleichen, zuerst die fachlich besonders nahen Cluster aus V6 (Trocknungsprotokoll Kleinbetrieb, Camper-Löschmittel, Balkonkraftwerk/PV, Heizungs-SMS, Gewächshaus-Frostwarnung, Hausüberspannung/Datenleitungen). Bisherige SERP- und Keyword-Daten nur dort als Evidenz werten, wo die exakten Suchanfragen übereinstimmen; fehlende Daten ausdrücklich unbekannt lassen. Keine kostenpflichtigen Abrufe ohne Freigabe. Erst nach vollständiger sachlicher Abnahme importfähiges R3-Profil plus minimalen 3–10-Validator- und URL-Regressionstest vorbereiten; R2 bis dahin live unverändert.
