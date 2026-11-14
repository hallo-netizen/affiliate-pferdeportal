# ROBOTIK – V54: WordPress-SEO-Vorabcheck 0.4.3 gegen das Originalmanifest geprüft
**Prüfdatum: 14.11.2026 · Ergebnis: STRUKTUR-/TRANSFER-PASS, KEINE BEZAHLTE SEO-RECHERCHE.**

## Grundlage und Herkunft
- Nutzer hat **`robotik-v52-seo-vorabcheck-kostenlos.json`** aus der WordPress-Administrationsoberfläche hochgeladen; direkte Prüfung des exakten Uploads, nicht nur vorherige Chat-Aussagen.
- Export meldet `schema=robotik-dfs-preflight-v1`, Plugin `version=0.4.3`, `source=V52_SEO_CANDIDATES_NICHT_IMPORT`, Markt Deutschland, Sprache Deutsch. Quellennachweis `source_sha256=c1d298e3777c8276276d2b395a3bc747e52b46ffccaee1428593ad52852c59d0`.
- Abgleich mit dem **lokal tatsächlich gebauten** V53-Quellmanifest `/mnt/data/robotik_v53/V53_SEO_MANIFEST_SOURCE_COMPACT.json`, dessen nachvollziehbare Version in GitHub `PLUGIN/V53_SOURCE/assets/robotik-v52-seo-candidates.json` abgelegt ist. Vergleich der 437 unveränderten IDs, Typen, Hauptwelten, Quellen und HOLD-Markierungen; Suchbegriffe `lower()`-normalisiert **437/437 übereinstimmend**. Labels im WordPress-Export sind **die vollständigen Keywordtexte**, während das Fachmanifest teils Kurzlabels enthält; das ist **keine** inhaltliche Änderung.
- Der SHA256-Fingerabdruck über die ursprünglichen Exportfelder `[keywords,rejected,count,source_sha256]` wurde unabhängig erneut berechnet; stimmt **exakt** mit `fingerprint=6d7cbf8b9f27a97785da59757c3308ab941213533aba6933b91aac441c3c5a82` überein.

## Vollständige maschinelle Prüfung
| Kontrollgröße | Tatsächlicher Upload | Soll/Urteil |
|---|---:|---|
| Geplante letzte Robotertypseiten | 141 | PASS |
| Geplante WP-Inhaltsrubriken | 296 | PASS |
| Eindeutige normalisierte Keywords | 437 | PASS, 437/437 Original-Suchtext zugeordnet |
| Eindeutige fachliche Besitzerkennungen | 437 | PASS, keine doppelte/fehlende ID |
| Keywords mit mehreren Besitzern | 0 | PASS – **nur EXAKTE**, keine semantische SEO-Kollision geprüft |
| Vorabcheck abgewiesene Suchbegriffe | 0 | PASS |
| Suchseiten mit ausdrücklich offenem HOLD | 16 | PASS |
| Mit diesen HOLDs verbundene Rubriken | 48 | PASS, **nicht als separat neue Streitfälle zählen** |
| Weltzugehörigkeit | alle 8 | PASS |
| Tatsächliche Search-Volume-/SERP-API-Daten | 0 | **Noch nicht ausgeführt** |
| Bezahlte API-Aufrufe / bekannte API-Kosten aus diesem Upload | keine | Nicht vorzeitig als Live-SEO-PASS deklarieren |
| WordPress-Seitenimport/-Veröffentlichung | kein Hinweis | Export ist **ausschließlich schreibfreier SEO-Plan** |

### Verteilung der 437 Suchbegriffe nach Hauptwelt (Typseiten und Rubriken zusammen)
**Haushalt 67 · Garten 44 · Freizeit 39 · Sport 53 · Bildung 35 · Pflege 45 · Humanoide 48 · Gewerbe 106**. Die größere Menge für Gewerbe ist kein Fehler und rechtfertigt keine künstliche Gleichverteilung.

### Der richtige, gebündelte nächste Arbeitsschritt
Die kostenlose Prüfung ist **vollständig erledigt**. Nicht erneut exportieren, nicht acht Einzelläufe starten, kein neues Plugin.
- **Nur falls der Nutzer die Anbietergebühren bewusst akzeptiert:** Im **vorhandenen WordPress-Backend** `Robotik Kategorie → DataForSEO` genau **einen** Lauf wählen: `Suchvolumen und Suchabsicht (Keyword Overview)` → `Erweiterter Umfang (Overview alle)` → vorgeschriebene ausdrückliche Kostenbestätigung → `Kostenpflichtige Recherche einmal ausführen`. Der tatsächlich eingebaute Plugin-Code `choose_task()` legt hierbei **alle 437** Suchbegriffe für Deutschland/Deutsch in **einem Auftrag** bereit. Eine automatische Bezahlung oder Wiederholung ist nicht erlaubt.
- Anschließend in derselben Ansicht **einmal** `Gesamter SEO-Bericht als JSON` herunterladen und gesammelt bereitstellen. Daraufhin kann der komplette 437er-Datensatz mit realen Suchvolumina und Suchabsichten gegen alle 16 fachlichen HOLDs, inhaltsnahe Überschneidungen, Fachrubriken und Zielgruppen beurteilt werden. Anschließend **ein** fachlicher Änderungs-/Delta-Vorschlag mit Freigabegrenze, nicht nach jedem Einzelfund ein neue Aufforderung.
- **Noch keine Zusage über die Höhe der Anbietergebühren**: Die konkrete Preisberechnung erfolgt nach DataForSEO-Preisliste/Anbieterrückmeldung. **Bei nicht erteilter Kostenfreigabe** keine bezahlte Abfrage, der Fachentwurf und der kostenlose Transfercheck bleiben vollständig vorhanden.

## Harte Trennung
Eine eindeutige Keyword-Zuordnung im Export sagt **nichts** darüber, ob Google für zwei unterschiedlich formulierte Suchbegriffe dieselbe Seite erwartet. Keine fiktiven Rankings, Suchvolumina oder Keywordwerte. Ebenso wenig sind 141 Seiten in WordPress damit angelegt: der alte Erstimportplan des Plugins ist ausdrücklich weiterhin getrennt. **Null Änderungen an WP-Seiten, URL, Design, alten Importfunktionen oder Forschungsregister aus diesem QA-Schritt.**

**Status:** Der WordPress-zu-Konzept-Datenabgleich ist abgeschlossen, die vollständige kostenfreie Keywordliste bereits beim Nutzer angekommen. Nächster benötigter Nutzerkontakt nur für die kostenpflichtige **einmalige Gesamt-Keywordabfrage** und deren einen gemeinsamen Ergebnis-Export.
