# ROBOTIK – V42 KORREKTUR: V41-Neuordnung verletzt Zielvertrag

**Datum:** 13.11.2026. **Status:** verbindliche fachliche Korrektur der *Empfehlung*, keine WordPress-/Plugin-/URL-Änderung.

## 1. Geprüfte maßgebliche Vereinbarungen

GitHub `KATEGORIE/ZIELVERTRAG.md`:
- Nachtrag 10.11.2026: **Privatpersonen und kleinere Betriebe** sind Hauptzielgruppe, einschließlich **Handwerk, kleiner Fertigung, Gastronomie, Handel, Landwirtschaft**; industrielle Geräteherkunft schließt diese Käufer nicht aus.
- Industrie erhält einen **nachgeordneten, ausdrücklich vom kaufnahen Handwerk getrennten Zugang** für wirklich exklusive großindustrielle/hochspezialisierte Einsatzfelder mit wenigen groben Landingpages (Fertigung, Anlagen, Medizin & Labor). Gelangen solche Typen auch in Kleinbetriebe, verlinkt die passende Käufer-Kategorie auf die **eine** Produktseite.
- Aktueller V36-Kategorie-/Bestandsvertrag: sieben Hauptpunkte **Haushalt · Garten · Freizeit · Sport · Bildung · Pflege · Gewerbe**. Unter **Gewerbe** bleibt der Industriekomplex mit verlinkten Landingpages fachlich erreichbar, nicht als mit Handwerk vermischter Produkttyp-Baum.
- Magazin/Journal, Glossar, Roboterregister, Roboterfinder, Anzeigenmarkt **einmal gemeinsam** für alle Zielgruppen; Produktseitentyp genau ein Haupt-Owner; Unterkategorien mit echtem Inhaltspotenzial; Informationsportal umfasst jetzt auch Konzept-, Entwicklungs-, Pilot-, Prototyp- und Vorbestellroboter.

Die älteren V5-Formulierungen „7 Käuferbereiche + 1 sichtbarer Industriezugang“ und der **neuere, konkret sieben Hauptkategorien umfassende V36-Baum** beschreiben verschiedene Navigationsstände. Maßgeblich für diese Korrektur ist der zuletzt bestätigte **sieben Kategorien umfassende V36-Baum**, bei dem **Industrie über Gewerbe erschlossen wird**. Der Zugang bleibt als Landingpage regulär verlinkt, aber nicht mit dem Käuferbereich „Handwerk“ verschmolzen. Die frühere V5-Industrie-Präzisierung (nur ausschließlich industrielle Anwendung, getrennte Zielgruppe und Verweise) bleibt unberührt.

## 2. Der belegte Fehler in V41

V41 „A/B“ hat aus dem Gewerbe-Altbestand (34 Funktionen) fälschlich drei **neue Hauptkategorien** konstruiert:
- „**Landwirtschaft**“ (9) – laut Zielvertrag eine Käufer-/Fachgruppe unter **Gewerbe**, **kein** losgelöster Hauptmenüpunkt.
- „**Service & Handel**“ (13) – Handel, Gastronomie, Hotel, Medien, Reinigung, Logistik gehören in sachlich getrennte Unterbereiche des Gewerbekomplexes, **nicht** einen neu erfundenen Hauptbereich.
- „**Handwerk & Industrie**“ (12) – **Zielgruppenbruch**: kaufnahes Handwerk und industrielle Sonderanwendungen dürfen nicht zu einer gemeinsamen Hauptwelt verschmolzen werden. Herkunft aus Fertigung oder Bau entscheidet nicht, ob ein Typ in Kleinbetrieben nutzbar ist; dies muss je Typ belegt werden.

**Ursache:** Die Optimierung „möglichst gleiche Anzahl an Produkten pro Hauptbereich“ hat die harten Vorgaben „Käufer-Zielgruppe“ und „Gewerbe-/Industrie-Trennung“ überschrieben. Die 72 echten alten Produkt-IDs wurden zwar exakt verteilt, aber die darauf basierende Strukturempfehlung war **unzulässig**. V41-A und V41-B sind ab jetzt **VERWORFEN**, nicht „Favorit“, nicht Arbeitsgrundlage. Ihre Rechenwerte dürfen ausschließlich in der Fehlerhistorie stehen.

## 3. Korrigierter aktiver Konzeptbaum (ohne WP-Umschreiben)

- **Haushalt**
- **Garten**
- **Freizeit**
- **Sport**
- **Bildung**
- **Pflege**
- **Gewerbe**
  - fachlich nachvollziehbare Käufer-/Unterbereiche etwa **Handwerk**, **Landwirtschaft**, **Handel**, **Gastronomie**, **Dienstleistungen/Reinigung**, **Logistik**, **Medien** – **keine zusätzliche neue Hauptnavigation**, Zahl/Namen nur nach fachlicher Recherchetiefe festlegen
  - **Industrie** als **getrennter, nachgeordneter Landingpage-Zugang**, grob **Fertigung**, **Anlagen**, **Medizin & Labor**, keine doppelten Produktseiten und keine Vermischung mit `Gewerbe > Handwerk`.

Die 34 bisher Gewerbe zugeordneten Produkttypseiten verbleiben in der Altberechnung **bei Gewerbe**, bis für jeden Einzelfall klar ist, ob er von Kleinbetrieben sinnvoll nutzbar ist oder wirklich ausschließlich großindustriell. **Keine 34 pauschal als Handwerksprodukte ausgeben.** Industrie-Landingpages sind keine separate zweite Datenhaltung und nicht automatisch zusätzliche Roboter-Produktseiten.

## 4. Balance- und Korrekturstatus

| Hauptkategorie | Ursprüngliche 72 Produktseiten | V41 mit 29 **unfreigegebenen** Informationskandidaten (nur Simulation) |
|---|---:|---:|
| Haushalt | 3 | 8 |
| Garten | 7 | 11 |
| Freizeit | 9 | 12 |
| Sport | 8 | 15 |
| Bildung | 3 | 6 |
| Pflege | 8 | 15 |
| Gewerbe | 34 | 34 |
| **Summe** | **72** | **101** |

Der Hauptwelt-Ausgleich ist **nicht erreicht** (Ist 3–34; Forschungssimulation 6–34). Das darf **nicht** durch Verschieben von Landwirtschaft/Handel oder Zusammenlegen von Handwerk/Industrie als „erledigt“ ausgegeben werden. Die 29 Kandidaten einschließlich Entwicklungs- und Konzeptrobotik sind weiterhin **einzeln hinsichtlich Identität und Inhaltsrubriken zu bewerten**. Offen bleiben 51+49 archivierte Überschneidungsfamilien.

## 5. Nächste fachlich zulässige Arbeit

1. 51/49 offene Funktions-/Familiengruppen unterscheiden, besonders Haushalt und Bildung, bei neu freigegebenen Konzept-/Prototypthemen.
2. Echte Inhaltskategorien prüfen; jeder neue Robotertyp erhält nur einen Owner.
3. **Gewerbe intern nach Käuferaufgaben und sauber getrenntem Industrie-Hub gliedern**, ohne eine Hauptkategorie Gewerbe zu streichen.
4. Balance danach neu betrachten. Wenn eine gleichmäßige **oberste** Verteilung unter den verbindlich sieben Kategorien unmöglich ist, **den Zielkonflikt offen darlegen** – nicht eigenmächtig die Käuferstruktur umbauen. Erst dann mögliche Änderungen zur **ausdrücklichen** Entscheidung vorlegen.

### Was V41 weiterhin richtig enthält
Alle 573 Forschungsfunde blieben erhalten; 19 dokumentierte Forschungsgruppen (= 21 doppelte Fundreferenzen) wurden ohne Löschung zusammengeführt. Diese Forschungsergebnisse bleiben erhalten. **Nur die navigationsbezogenen V41-A/B-Empfehlungen sind ungültig.** Keine Änderung von WordPress, Plugins, 72 Originalseiten oder 89 bestehenden Artikelkategorien.

## Ablage
**Führender Recherche-Master** bleibt `/robotik/Recherchebüro/CURRENT.json` mit Version **42**, die historische V41-Navigation ist dort als verworfen markiert. Diese GitHub-Notiz ist die verbindliche **Korrektur des Berichts**, kein zweiter Research-Master.
