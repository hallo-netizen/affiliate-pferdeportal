# HAB & BEWAHR – KATEGORIENTEXT-VERTRAG V2.1
Stand: 2026-10-14
Status: **NUR 6 HAUPTWELTEN: UNTERER EDITORIAL-BEREICH UND KEINE FAQ FREIGEGEBEN / TEXTE NOCH WIP / UNTERGEORDNETE KATEGORIEN: LAYOUT UND PLATZIERUNG NICHT ENTSCHIEDEN**.

Dies ist der verbindliche FACHVERTRAG im Konzeptbüro, **keine weitere Current-Autorität**. Autoritativer Status weiterhin in `KONZEPT/CURRENT_STATE.md`, Designfortschritt in `DESIGN/CURRENT_STATE.md`.

## Präzisierung nach Nutzerabnahme / Live-Screenshots vom 14.10.2026 (Version 0.1.11)
- Sechs Welt-Langtexte unten sollen **jede ihrer 5–6 unmittelbar untergeordneten Hauptbereichskategorien behandeln**: insgesamt 31 eigenständige Themenabschnitte. Kein bloßer kurzer Dreipunktüberblick, kein erzwungener FAQ-Baustein.
- **Sämtliche Links im erklärenden Fließtext**, keine am Schluss angehängte reine Linkliste. Der sichtbare Ankertext ist 1:1 der aktuelle vollständige Name der Zielkategorie aus dem zentralen Live-Kategoriebaum; Menü-Kurzlabel ist NICHT zulässig.
- Redaktionelles Layout mit durchgehender linker Textkante, nicht plötzlich zentrierten Schlussblöcken. Bilder **flaches Panorama, max. ca. 148 px Ansichtshöhe**, nur scharfe und semantisch zutreffende Motive; dies ist Voraussetzung für Fach-/Design-Endfreigabe, nicht bloß CSS-Korrektur.
- Screenshot 19:52: Mobil-Brandbogen möglichst hoch, durch korrekt beschnittenes SVG viewBox statt negativen Margin-Scheinficks; Breadcrumb **unmittelbar unter dem Schutzwelten-Menü**, nicht durch globalen Abschnittspadding nach unten gedrückt.
- Diese Anforderungen gelten derzeit **nur für die sechs Welt-Langtexte**. Die übrigen 31+93+285 Kategorie-Textlayouts sind weiterhin NICHT beschlossen.
- Version 0.1.11 setzt die Layout- und Inhaltsstruktur lokal um (562–746 Wörter, 31 Bereichsabschnitte, 12 flache Bilder, 31 echte Bereichslinks), bleibt aber vor echten Quellen-/Bildrechten-Prüfungen und WordPress-Liveprüfung **WIP**, keinesfalls ein SEO-Garantieversprechen.

## 0. Aktuelle verbindliche Nutzerentscheidung vom 14.10.2026 (nach Entwurfsansicht)
- **ZUERST ausschließlich sechs Hauptkategorien / Schutzwelten.** Der ausführliche Text steht ausnahmslos **UNTEN** unter Kategorien und Artikeln. Die vorgeschlagene hochwertige Editorial-Anmutung, zweispaltige Text-Bild-Strecken, zwei Bilder, Liste und exakt beschriftete interne Kategorielinks sind als Gestaltungsrichtung angenommen.
- **KEINE FAQ und keine „Häufige Fragen“-Module in diesen Texten.** Ob und wo später FAQ-Beiträge erscheinen, ist redaktionell ungeklärt; nicht mit automatischen FAQ-Texten vorweggreifen.
- **Alle weiteren 31+93+285 Kategorien: Entscheidung zu Textumfang, Position und Design VERTAGT.** Der bisher unten im Dokument beschriebene Vorschlag B ist ausdrücklich **nur eine nicht freigegebene Option**, kein bindender Layout- oder Produktionsauftrag. Bestehende Texte/Intros nicht ohne neuen Beschluss überschreiben oder massenhaft produzieren.
- Die erst zu Beginn dieses Tages ohne abgestimmte Regeln geschriebenen 0.1.9-Texte und die 0.1.10-redaktionellen Erstfassungen sind **nicht fachlich quellengeprüfte SEO-Endfassungen**. 0.1.10 liefert die lokal getestete Struktur/HTML mit bisherigen WIP-Absätzen, 2 eingebundenen Lokalfotos, mindestens 1 Liste und 3 dynamischen echten Bereichslinks bei jeder der sechs Hauptwelten; keine Behauptung fertiger langformatiger Artikel (aktueller Einbruch-WIP ca. 287 Wörter).
- Textfelder mit bereits manuell eingegebenen Inhalten behalten Vorrang; Installation überschreibt diese Daten nicht.

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

### B – Ebenen 2–4: VORLÄUFIGER, NICHT FREIGEGEBENER ENTWURF; LAYOUT UND TEXTLÄNGEN UNENTSCHIEDEN
- **Bisherige Idee, ausdrücklich noch NICHT beschlossen:** Direkt unter dem Seitentitel vor Karten/Artikelrastern als kompakte Text/Bild-Komposition. Alternativ andere Position/Präsentation möglich.
- **Nur unverbindliche Richtwert-Idee, noch NICHT geltend:** Ebene 2 (31 Bereiche) **150–230 Wörter**, Ebene 3 (93 Unterbereiche) **120–190**, Ebene 4 (285 Endkategorien) **100–170 Wörter**. Die tatsächliche Länge richtet sich nach Inhalt und Elementen, nicht mathematischem SEO-Füllzwang.
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
Mindestanforderungen an fachliche Qualität bleiben Leitplanken. Verbindliche Layout-/Platzierungsentscheidung ausschließlich sechs Hauptwelten unten und ohne FAQ. 409 weitere Kategorietexte/Formate sind zurückgestellt, bis ausdrücklich entschieden. Die sechs hochwertigen Hauptwelt-Langtexte gelten erst nach echter Recherche, Bild-/Linkprüfung und redaktioneller Freigabe als fertig. Alte 0.1.9-Entwürfe nicht als Erfüllung der Gates ausgeben.
