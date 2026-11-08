# Hobby Depot – Bildzentrale HD-006 – Zwischenprotokoll 2.8.14

**Stand:** 08.11.2026 | **Status:** Vollständiges Plugin lokal geprüft, echter WordPress-/Magnific-Hero-Test offen.

## Ausgangspunkt und Ursache

Die Bildübernahme wurde vom Betreiber bei **Arduino** bereits im Live-Frontend bestätigt. Der neu erzeugte Bildausschnitt war aber weiterhin zu nah. Das weitere Beispiel **3D-Scanning** zeigt dasselbe Problem: die Tätigkeit und das entscheidende Gerät lassen sich im sehr flachen Hero nicht deutlich genug erkennen.

Die frühere Bildzentrale 2.8.13 verlangte nur eine *mittlere Weitaufnahme*. Außerdem übernahm der Hobbyregister-Prompt den **allgemeinen Bildstil**, der ausdrücklich Nahaufnahmen von Händen und natürlichen Oberkörper-Ausschnitten empfahl. Diese widersprüchlichen Vorgaben waren die eigentliche Fehlerquelle.

## 2.8.14: nur Hobbyregister-Grundprompt geändert

- Statt mittlerer Weitaufnahme nun **deutlich weiter entfernte Gesamtaufnahme**, Anweisung: Kamera etwa zwei- bis dreimal weiter entfernt als bei einem üblichen mittleren Bildausschnitt.
- Das **tatsächliche Hobby samt Handlung, Werkzeug/Gerät, Arbeitsobjekt und Umgebung** soll als zusammenhängende Szene erkennbar sein.
- Native Bilddatei weiter 3:2, mindestens 1500 × 1000 Pixel. Das Ergebnis muss vor allem als sehr flacher **4:1 bis etwa 5:1 Hero-Zuschnitt** funktionieren.
- Entscheidende Handlung mitsamt Gerät im **mittleren 35–65 % der Bildhöhe** und **rechts der Mitte (55–80 % Bildbreite)**. Links 35 % ruhige Fläche für die eingeblendete Überschrift. Oben und unten viel entbehrliche Umgebung, damit der schmale Hero nichts Wichtiges abschneidet.
- Ausdrücklich **keine Makro-/Nahaufnahme, keine großen Gesichter, keine nur Hände, keine halben Oberkörper als Hauptmotiv, keine übergroßen Geräte im Vordergrund**. Technische Hobbys wie Arduino oder 3D-Scanning zeigen Person, vollständiges Gerät, Werkstück und Arbeitsplatz gemeinsam.
- Der widersprüchliche **allgemeine** Fotostil wird **nur für den Hobbyregister-Prompt** durch einen knappen, passenden redaktionellen Stil ersetzt. Der allgemeine Fotostil anderer Funktionen bleibt unberührt.
- Motivwünsche bis 400 Zeichen und ausdrücklich ausgeschlossene Motive (z. B. **„kein Tier“ beim 3D-Bogenschießen**) bleiben vollständig enthalten, auch bei langen Eingaben. Kein unbemerkter Abbruch am Anbieterlimit 3000 Zeichen.
- Alle bestehenden Bilder, redaktionellen Freigaben und Zuordnungen bleiben **unverändert**. Kein kostenpflichtiger Auftrag wird automatisch gestartet.

## Beweis und Abnahmegrenze

**Vollständiges Plugin:** `Bildzentrale-2.8.14.zip` (86.568 Bytes, SHA-256 `06ffeac81f37d5d20a424e1d93dd74c597b0bf1cb7d472da391337d5c49c529e`). Genau zwei PHP-Dateien und exakt derselbe Plugin-Aufbau wie 2.8.13.

**Quellvergleich:** Hauptdatei nur von Version 2.8.13 auf 2.8.14 geändert; in der Hobbyregister-Datei **genau zwei PHP-Zeilen** geändert (allgemeinen Stil im Hobbyregister ersetzen, Hero-Komposition strenger machen). Keine anderen Funktionen verändert.

**Positive und negative lokale Tests:**

- **149/149 Backendtests** bestanden: beide Promptrouten mit/ohne Motivwunsch, Zoom-/Hero-Geometrie, Ausschlüsse, unveränderte Bestandsbilder, Freigaben und Bildübernahme samt absichtlich abgetrennter Frontend-Bildauflösung.
- **27/27 Menütests** bestanden: ursprüngliches Bilderzeugungsplugin **Bildzentrale**, anderes Plugin **Bilder zuordnen**, unterschiedliche Klickpfade.
- **39/39 Browser-Klicktests** bestanden: 862 Hobbys, tatsächliche Klickfolge, Erzeugung, Entwurf, Übernahme, Fehleranzeigen.
- Ein zweiter Durchlauf **aus frisch entpacktem eigenständigem Testarchiv** hat alle drei Testgruppen erneut bestanden.
- PHP-Syntax beider Dateien und ZIP-Integrität erfolgreich.

**Grenze:** Die automatischen Tests rufen kein echtes kostenpflichtiges Magnific-Bild ab. Ob sich das Modell beim nächsten echten Bild tatsächlich ausreichend weit entfernt, ist noch **nicht** bewiesen. Die reale Browserdarstellung muss nach einer bewussten neuen Bilderzeugung beurteilt werden.

## Noch offen

1. Version 2.8.14 in WordPress installieren, ohne Design-Plugin oder Hobbyregister-Plugin zu verändern.
2. Bei einem *ausdrücklich gewünschten* neuen Motiv (beispielsweise 3D-Scanning) Bild erzeugen und vor Übernahme die Vorschau auf Hero-Tauglichkeit beurteilen. **Kann Geld kosten.**
3. Beim gleichzeitigen bereits richtig zugeordneten Foto **keine erneute Erstellung** auslösen; die händische Bestandszuordnung durch den Betreiber bleibt bestehen.
4. Älterer systematischer Bestand 2.8.13: 862 vorhandene Dateien, 24 verifizierte HD007-Finals und 62 besondere Design-Master, 775 weitere allgemeine Zuordnungen noch offen. Kein pauschaler Autoersatz.

**Ablage:** vollständiges ZIP, Testnachweise, dieses Zwischenprotokoll und CURRENT im dauerhaften `/Hobby Depot/Plugin-Büro/`. GitHub-Vertragsdokumentation separat, nicht behaupten, die binäre ZIP sei auf GitHub.