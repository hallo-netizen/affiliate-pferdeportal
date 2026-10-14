# HAB & BEWAHR – KATEGORIENTEXT-VERTRAG V2
Stand: 2026-10-14
Status: **VERBINDLICHE NUTZER-MINDESTREGELN / EDITORIAL-DESIGN ALS ENTWURF, NOCH NICHT ABGENOMMEN / ALTE 0.1.9-TEXTE NICHT FREIGEGEBEN**.

Dies ist der verbindliche FACHVERTRAG im Konzeptbüro, **keine weitere Current-Autorität**. Autoritativer Status weiterhin in `KONZEPT/CURRENT_STATE.md`, Designfortschritt in `DESIGN/CURRENT_STATE.md`.

## 1. Quelle Pferde-Atelier: ausschließlich TEXTREGELN
Die echte Referenz `pferde-template-kit-1.50.560.php` wurde geprüft. Übernommen: redaktionelle individuelle Kategorie-Intros; manuell hinterlegte Texte haben Vorrang; leere optionale Textbereiche werden nicht gerendert; individuell fachlich passende statt generischer Texte. Die historischen PA-Obergrenzen von Start 65 / Hub1 90 / Hub2 80 / Kategorie 70 Wörtern beziehen sich auf eine spezifische dynamische Kurztextfunktion und sind **keine Pflichtgrenzen für Hab & Bewahr**. Bei Hab & Bewahr erfordern die neuen Pflichtbestandteile mehr nutzbaren Text. **Kein Pferde-Design/Code/CSS, keine Pferdetexte oder Kategorien kopieren.**

## 2. Nutzer-Hard-Rules für JEDEN fachlichen Kategorietext
1. Mindestens **zwei semantisch wirklich passende** interne Links zu **tatsächlich existierenden Kategorien**, nach Möglichkeit drei. Der sichtbare Linktext entspricht **exakt dem aktuellen vollständigen Namen der jeweiligen Zielkategorie aus dem zentralen WP-Kategoriebaum** (nicht dem verkürzten Megamenü-Anzeigenamen). Ziele dynamisch über aktive Node-ID/Mapping lesen, nie aus alten URLs geraten. Keine Self-Links, keine erfundenen Zielseiten, keine bloß beliebigen Links für die Quote; 1+ Ziel sollte wenn möglich aus einem sachlich benachbarten Gebiet zur Orientierung stammen.
2. Mindestens **eine fachlich echte Aufzählung**, sinnvoll eingeführt, vorzugsweise 3–5 konkrete Punkte. Keine Keywordstichwort-Sammlung.
3. Mindestens **ein** in den Lesefluss integriertes fachlich relevantes Foto auf allen 31+93+285 untergeordneten Kategorien; **mindestens zwei** in den langen Textabschnitten jeder der sechs Schutzwelten. Ein weiteres Foto nur mit echtem zusätzlichem Informationswert; Fotos nicht nur als externe Kartenbilder mitzählen.
4. Jede Bilddatei: passende reale Szene statt generische Deko, Nutzungsrechte vorhanden, eindeutige Bildrolle, sachlicher Alttext und bei Informationswert eine Bildunterschrift, sinnvolle Abmessungen/Responsivität, Lazy-Loading unterhalb des initialen Viewports. Keine wiederholten gleichen oder nahen Motive auf derselben Seite. Kein externes Hotlinking als Produktionslösung.
5. Falls nicht zwei reale passende Kategorieziele und ausreichend freigegebene Bilder verfügbar sind: Textmodul **NICHT ALS FERTIG FREIGEBEN**. Keine Platzhalter, Fake-Links oder Auto-Synonymspinnen.

## 3. Unterschiedliche redaktionelle Platzierung
### A – sechs Hauptwelten (Ebene 1): ausführlicher Informationsteil UNTEN
- Der obere Seitenkopf bleibt kurz; Artikel, Kategorienraster und primäre Nutzerwege bleiben oberhalb des Langtextes.
- Leseformat: eigenständiger, nützlicher Fachartikel mit **ca. 500–850 Wörtern als Orientierung**, individuellen H2/H3, verschiedenen kurzen Absätzen, 2 thematisch unterschiedlichen integrierten Bildern, 3 passenden internen Kategorienlinks, 1 echter Aufzählung, ggf. konkreter Gegenüberstellung in einer **semantisch sinnvollen und barrierearmen Tabelle**.
- 2–3 FAQs nur, wenn sie konkrete häufige Fragen präzise beantworten; kein erfundenes FAQ-Schema und kein SEO-Füllmaterial.
- Bild-/Textkomposition wie hochwertiges Editorial: breite Auftakt- und Zwischenüberschriften, ein erstes Bild in einer zweispaltigen Strecke neben Text, zweites Bild weiter unten mit anderem Motiv und ruhiger Bildunterschrift. Keine starre Pflicht-Wechselrichtung, keine Textwand, keine Kachelwiederholung.
- In Markdown/PHP geforderte verifizierte Links verwenden aktuelle, vollständige Zielkategorienamen.
- Erste in 0.1.9 installierbare, vorab geschriebene Kurz-Langtexte (~280–310 Wörter) gelten als **VOR-FREIGABE-WIP und explizit NICHT regelkonform**; nicht automatisch auf dem neuen Konzept aufbauen.

### B – Ebenen 2–4: kompakter, hochwertiger Infoblock OBEN
- Direkt **unter dem Seitentitel**, **vor** Karten/Artikelrastern. Allerdings eine kompakte Text/Bild-Komposition statt eines riesigen sichtbehindernden SEO-Blocks.
- Orientierungslängen: Ebene 2 (31 Bereiche) **150–230 Wörter**, Ebene 3 (93 Unterbereiche) **120–190**, Ebene 4 (285 Endkategorien) **100–170 Wörter**. Die tatsächliche Länge richtet sich nach Inhalt und Elementen, nicht mathematischem SEO-Füllzwang.
- Mindestens zwei semantisch passende Kategorie-Links im natürlichen Satz, 1 echte Aufzählung mit 3 Punkten, 1 relevantes Foto mit Alttext. Text/Bild desktop meist 2 Spalten (ungefähr 2:1), mobil 1 Spalte. Falls der Text weitere tatsächliche Tiefe erfordert, sinnvoll gliedern, nicht auf 70 Wörter zusammenpressen.
- Eine kompakte Vergleichstabelle **optional** bei echten unterschiedlichen Kriterien, aber nicht obligatorisch und nicht um ihrer selbst willen. Kein Tabellenersatz für Fließtext.
- Die Einleitung bildet eine lesbare Orientierung und verdeckt nicht den Zugang zu Kategorien/Artikeln. Gleiche zurückhaltende Farbpalette wie Hab & Bewahr, aber **kein Layout-Abklatsch** von Pferde-Atelier.

## 4. Inhalt, Technik, SEO, Pflege
- Exakte Nutzerfrage, Risikolage, typische Abgrenzungen und sinnvolle nächste Schritte ohne pauschale Versprechen. Normen/Brandschutz/Elektro/Gas/Recht/Versicherung nur mit belegbarer zuständiger Quelle und Prüfdatum. Keine Erfindungen.
- Metatitel/Beschreibung einzigartig; keine Keywordliste oder immer gleiche Satzstruktur; saubere Überschriftenhierarchie ohne zweite H1.
- Redaktionelle persönliche/WordPress-Texte haben Vorrang und werden bei Designpluginupdates nicht verändert. Sicht-/Renderlogik getrennt von Fach-/Kategoriewrites. Zentrale Kategorienverwaltung behält IDs, Slugs, Namen, Links und Zuordnungen.
- Bild-/Link-Daten dynamisch/strukturiert, fachliche Freigabe an reale Node-ID gebunden. Änderungen der Kategorien/URLs müssen ohne Hardcode-Plugin-Rebuild aufgefangen werden.
- Qualitätstests pro Seite: Inhalt fachlich geprüft; Text an korrekter Position; 2–3 **echte** Kategorie-Links mit Zielnamen und semantischer Passung; 1 sinnvolle Liste; 1–2 fachlich passende Bilder mit Rechten/Alt/Captions; mobil/Desktop saubere Abstände und keine Überläufe; individuelle Meta/kein Duplicate; keine unbelegten Aussagen.
- Der Designvorschlag ist nur eine Vorschau. **Keine erneute automatische Veröffentlichung oder ein Update-Plugin aus diesem unbestätigten Layout erstellen.**

## 5. Produktions-/Freigabegrenze
Fachliche Regeln gelten ab jetzt als Mindestvertrag. Das optische Layout wird vor technischer Umsetzung anhand der In-Chat-Vorschau vom Nutzer abgenommen. 409 untergeordnete Individualtexte und sechs hochwertige Langtexte sind erst nach Recherche, Bildzuordnung und Link-/Qualitätskontrolle „fertig“. Keine alten 0.1.9-Entwürfe als Erfüllung dieser Gates ausgeben.
