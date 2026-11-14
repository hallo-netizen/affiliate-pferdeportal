# Robotik V53 – vorhandenes Kategorie-Plugin 0.4.3: V52-SEO-Plan im WordPress-Backend
**14.11.2026 | Status: lokal gebaut und funktionsgeprüft; in WordPress NICHT installiert; keinerlei API-Aufruf und keine Live-Änderung.**

## Nachgewiesene Ursache aus Original-ZIP 0.4.2
Das bestehende WordPress-Plugin `Robotik Kategorie-Workflow (Neutralstart)` hat bereits das Menü **Robotik Kategorie → DataForSEO**. Vor V53 holt `Robotik_DataForSEO::build_preflight()` seinen Keywordplan ausschließlich aus dem alten, eingebetteten Erstimport mit **72 Robotertypen und 89 Beitragskategorien**. Der bestätigte V52-Fachentwurf enthält dagegen **141 mögliche Robotertyp-Seiten und 296 Rubriken**, darunter **16 fachliche Prüffälle**. Das bisherige WordPress-SEO-Menü erfasst den neuen Entwurf also nachweislich nicht vollständig.

## Einzige Pluginidentität – zielgerichtete Korrektur ohne WordPress-Import
Das getestete Update **0.4.3** leitet den **kostenfreien SEO-Prüfplan** aus der neuen beigelegten reinen Forschungsdatei `assets/robotik-v52-seo-candidates.json` ab. **Diese ist KEIN WordPress-Importprofil.** Originalimport, Sammelveröffentlichung, WP-Bestandsaufnahme und sämtliche vorhandene API-/Sicherheitsmechanismen sind byte-identisch zur 0.4.2 (siehe Dateiliste unten), bis auf die gezielt angepasste DataForSEO-Datei und Versionsangaben.

- **141** V52-Robotertypen und **296** individuelle Rubriken = **437 eindeutige SEO-Keywords** mit unverwechselbaren Herkunfts-/Owner-IDs. Alle 16 alten fachlichen Prüffälle bleiben erkennbar (`review_hold=true`); auch sie werden als Frage geprüft, **nicht** als Publikationsfreigabe.
- **Nicht als eigene Seite gezählt:** 4 humanoide Zukunftskapitel; sie bleiben als Themen in bestehenden Entwürfen.
- **Spezifische fachliche Korrektur:** Der V51-Namensvorschlag „Programmierung“ war beim bestehenden *Lernroboter* sowohl für die alte Kaufberatungsrubrik als auch für die bereits vorhandene Rubrik „Programmierung“ vergeben worden. Nur im SEO-Kandidatenplan wird die erstgenannte Rubrik jetzt „Schuleinsatz“ genannt, gestützt auf deren vier Original-Themen (Grundschulen, Sprachen, Sensoren, Klassensets). Die ursprüngliche WordPress-Kategorie und ihr Slug werden **nicht verändert**. Dies beseitigt exakt einen doppelten SEO-Keyword-Owner.
- **Neue schreibfreie Admin-Funktion:** `SEO-Keywordliste als JSON herunterladen (kostenlos)` unter **Robotik Kategorie → DataForSEO**. Sie exportiert genau die gegen den aktuellen V52-Prüfplan erzeugte 437er Liste mit Rückverweisen und 16 Prüffallmarkierungen. **Keine Anbieterabfrage, keine WP-Seitenänderung**.
- Bestehender Button `Gesamte Keywordliste prüfen (kostenlos)` berechnet sie direkt in WordPress. **Echte bezahlte DataForSEO-Abfragen** bleiben getrennt und erfordern weiterhin eine explizite Checkbox und einen manuellen Klick. Preflight-Prüfsumme stellt sicher, dass veraltete Daten vor einer bezahlten Abfrage blockiert werden; dieselbe Abfrage wird nicht automatisch wiederholt.

## Prüfnachweise
- Original-ZIP **0.4.2** direkt aus der Library/Projektablage entpackt; Pluginname und Pfade geprüft.
- **Byte-identisch erhalten:** `includes/class-robotik-inventory.php`, `includes/class-robotik-first-import.php`, `includes/class-robotik-publish.php`, `assets/robotik-first-import-plan.json`.
- PHP-Lint **5/5 bestanden**, ZIP-Test **PASS**, originale **208** Plan-Knoten weiterhin vorhanden (davon 104 bisherige Seiten, 72 Produkttypseiten); alter Erstimport weiterhin auf 104 Seiten/89 Kategorien ausgelegt.
- Eigenständiger PHP-Simulationstest: **437/437 gültige SEO-Eigentümer**, **437 eindeutige Keywords**, **0 verworfen**, **16/16 HOLD**, Prüfsummen über zwei Aufrufe identisch; Overview-Test 437 Begriffe unter dem API-Limit 700; Ideas-Test 3 Begriffe. **Keine echte API-Anfrage durchgeführt**.
- Simuliertes WordPress-Backend: die neue kostenlose Download-Funktion sowie alle ursprünglichen Preflight-/Paid-Bedienelemente werden angezeigt.

## Harte Grenze und nächster Nutzerweg
**0.4.3 aktualisiert NUR den SEO-Prüfplan, nicht den WordPress-Importplan.** Daher ist `Robotik Kategorie → Erstimport` weiterhin historisch auf 104/89 begrenzt und darf für V52 **nicht als fertiger 141er-Import verwendet werden**. Dass die Daten nun in WordPress per DataForSEO prüfbar sind, bedeutet **nicht**, dass das Projekt bereits import- oder indexierungsbereit ist.

1. **Nur die gleiche vorhandene Pluginidentität** auf Version **0.4.3** aktualisieren – keine zweite Pluginlinie anlegen.
2. WordPress: **Robotik Kategorie → DataForSEO → Gesamte Keywordliste prüfen (kostenlos)**.
3. **SEO-Keywordliste als JSON herunterladen (kostenlos)** und hier hochladen, damit die vollständige V52-Plan-Soll-Ist-Prüfung im Chat nachvollzogen werden kann.
4. **Noch keine** kostenpflichtige API-Abfrage und **keinen** alten Erstimport anstoßen. SEO-Prüfdaten/Kontextentscheidungen erst im selben vorhandenen Plugin nach Freigabe weiterverarbeiten; der spätere vollständige 141er WP-Delta-/Importplan ist gesondert abzusichern.

**Führender Forschungsbestand bleibt allein Library `/robotik/Recherchebüro/CURRENT.json` Version 52 mit 581 Fundnennungen.** Das SEO-JSON ist eine generierte *Ableitung*, keine zweite Stammliste. Kategoriebaum/Blogartikel/URLs/WordPress/Plugin-Livebestand unverändert.