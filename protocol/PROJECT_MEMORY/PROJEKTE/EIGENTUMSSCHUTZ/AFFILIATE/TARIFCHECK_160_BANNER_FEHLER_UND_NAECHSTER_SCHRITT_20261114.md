# Hab & Bewahr – Tarifcheck-Banner: verbindliche Fehlerübergabe
**Stand: 14.11.2026 · Status: NICHT erledigt · keine neue Pluginfreigabe**

## 1. Wo stehen wir?
- Letzter durch WordPress-Screenshots bestätigter Live-Stand nach Installation **RC40**: **160** Tarifcheck-Banner vorhanden, **80 aktiv/zugeordnet**, **80 ohne erkanntes Ziel**, **0** wegen Bildformat gesperrt. „Aktiv“ beweist nicht automatisch die sichtbare Veröffentlichung auf einer bestimmten Frontend-Seite.
- Der Benutzer hat die identischen Werte nach RC39 **und** RC40 nachgewiesen. Diese beiden Versionen lösten das verbleibende Problem nicht.
- **RC41** wurde ausschließlich auf GitHub gebaut und im vollständigen PHP-Workflow getestet, **nicht** zur Installation freigegeben, nicht live gemessen und nicht als Lösung für 80 Altbestände auszugeben.
- Ursprünglicher HTML-Sammelimport besteht aus insgesamt 160 Werbemitteln; keine vollständige private Original-Sammeldatei in GitHub auffindbar. Ein direkter Zugriff auf die laufende WordPress-Datenbank war bei dieser Prüfung nicht vorhanden.
- Die WordPress-Ablage bewahrt unabhängig von HTML-Attributen jedenfalls Felder für `tracking_url`, `image_url`, `destination_url`, gespeicherten Payload und Zuordnungen. Welche weiteren Felder im konkreten 80er-Block noch enthalten sind, **ist noch nicht nachgewiesen**.

## 2. Nachgewiesene Fehler (keine Vermutungen)
1. **Reihenfolge des Imports verletzt KISS:** `creative_library_parse_html_codes()` liest zunächst Original-HTML, `creative_library_normalize_row()` überträgt `html` dann über `sanitize_text_field()` und entfernt dabei Tags und deren Attribute. Dadurch können originäre Hinweise wie `<a title="Hausratversicherung">` verloren gehen, **bevor** RC40 den Quelltext auswertet. **Mit echten Original-PHP-Methoden reproduziert:** https://github.com/hallo-netizen/affiliate-pferdeportal/actions/runs/43582129807
2. **Künstlicher Titel als scheinbarer Quellhinweis:** Wenn kein echter Bildtitel/Alt vorhanden ist, entsteht der Ersatztitel `Tarifcheck Banner`. Vorher wurde fehlende Originalherkunft nicht zuverlässig gekennzeichnet.
3. **Falsche Vollständigkeitsmarkierung:** RC40 markierte Datensätze als bereits ausgelesen, obwohl die HTML-Attribute vor dem Auslesen schon zerstört waren. Eine spätere Verarbeitung konnte sie nicht zurückholen.
4. **Falsches Abnahmekriterium:** Frühere RC39-/RC40-Tests lieferten grüne Ergebnisse auf synthetischen Eingaben, ohne den **wirklichen Pfad von Original-HTML bis Datenbankablage** abzudecken. 160 Testfälle ersetzten nicht den Nachweis mit den 160 gespeicherten Bannerquellen. Die echten 80/80-Zahlen blieben unverändert.
5. **Wiederholte unproduktive Fix-Versionen:** RC39 ergänzte feste Versicherungssynonyme/Oberkategorien, ohne die fehlende Quelle zu reparieren; RC40 versuchte die Quellenauswertung erst nach deren destruktiver Verarbeitung. Beide wurden vor echtem Live-Nachweis zur Installation empfohlen. **Diesen Ablauf nicht wiederholen.**
6. **Nicht erwiesene fachliche Veröffentlichung:** Der Bericht meldet 80 aktiv, enthält aber keinen belastbaren Nachweis einer konkreten öffentlichen Seite mit einem tatsächlich sichtbaren Banner.
7. **Unerledigter Bestandsabgleich:** Die 80 gespeicherten Original-Werbelinks, Bildadressen, Datenfelder und tatsächlichen WordPress-Kategorieziele wurden bisher **nicht als vollständiger read-only Datensatz** exportiert und gegengeprüft. Daher ist weder „alle 80 ohne Information“ noch „alle 80 sind nur Kategorienfehler“ bewiesen.

## 3. Was bereits funktioniert / Schutzregeln
- RC38 beseitigte nach den WordPress-Screenshots die 40 früheren Bildformatsperren: von 40 aktiv/40 formatgesperrt/80 ohne Ziel auf 80 aktiv/0 formatgesperrt/80 ohne Ziel.
- Bildgrößen **nie vergrößern**, Seitenverhältnis erhalten, nicht verzerren, nicht beschneiden. Vorhandene Werbeflächen flexibel.
- Eine fachliche Ziel- und Platzentscheidung **einmalig nach dem Auslesen** im bestehenden zentralen Besitzer, danach gespeichert. Frontend nur lesen; keine zweite Prüfung, kein zweiter Worker, keine neue Tabelle und keine unabhängigen Entscheidungen.
- Nur belegte Versicherungsarten konkret zuordnen; fehlt eine konkrete Seite, darf ein belegter passender Elternzweig seinen Baum abdecken. Allgemeines Banner nur bei tatsächlich belegtem allgemeinem Versicherungsinhalt. Finanzprodukte nicht pauschal unter Versicherung.
- Andere Portale und übrige Affiliate-Partner unverändert lassen; keine Banner neu importieren, keine Frontend-Änderung ohne Freigabe.

## 4. RC41, nur Quellkorrektur, noch keine Lösung der alten 80
- Im vorhandenen Import wird jetzt Original-HTML **vor** der Bereinigung einmal in Arbeitsspeicher ausgelesen; gespeichert werden nur sichere extrahierte Herkunftsdaten. Künftige Quellverluste dieser Art unterbindet die Korrektur.
- **Test erfolgreich**: https://github.com/hallo-netizen/affiliate-pferdeportal/actions/runs/43582511129 (Original PHP vollständiger Import; erhaltene `<a title>`-Angabe; Altbestand mit bereits entfernten Angaben nicht künstlich wiederhergestellt; alte Tests bestanden).
- **Wichtig:** RC41 stellt ehemals vernichtete Original-Attribute aus dem Altbestand nicht wieder her. **RC41 nicht als „80 gelöst“ ausgeben und nicht auf Verdacht installieren lassen.**

## 5. Verbindlicher nächster Schritt – EINMALIGER BESTANDS-EXPORT, OHNE BANNERSCREENSHOTS
**Wer macht was:** Der Assistent setzt im **bereits vorhandenen HAB-004/Affiliate-Zentrale-Plugin** (kein zweites Plugin) genau eine **schreibgeschützte Exportfunktion** für die 160 gespeicherten Tarifcheck-Banner um. Eine einzige Datei (vorzugsweise CSV mit UTF-8 oder JSON) soll je Datensatz enthalten:
- vorhandene ID (zur eindeutigen Bestandszuordnung), Partner, tatsächlicher Originaltitel und seine Herkunft, tatsächlicher Status/Fehler;
- gespeicherte `tracking_url`, `destination_url`, `image_url`, sichere eventuell vorhandene HTML-/Anker-/Alt-/Titel-/Anbieterangaben und kanonisch bereits extrahierte Quellenhinweise;
- bisherige echte Zielpfade/Versicherungs-Kategorien und Quellen-/Versionsstatus; verfügbare R2/R3-Zielnamen aus dem einen aktuellen WordPress-Baum (separater Abschnitt/zweites Tabellenblatt innerhalb derselben JSON-Datei).
**Keine Zugangsdaten, Cookies oder Affiliate-Geheimnisse exportieren; Admin-only, geschützter Aufruf, keine Änderung an Daten oder Zuordnungen.** Für einen privaten lokalen Diagnoseexport können Affiliate-Werbelinks enthalten sein, sollten aber nicht im öffentlichen GitHub-Repository veröffentlicht werden.
**Abnahme vor ZIP:** Ein echter Test auf dem vollständig gepackten Originalplugin muss belegen: 160 vorhandene Datensätze werden exportiert, der Originalbestand bleibt unverändert, bereits fehlende Felder werden als fehlend gekennzeichnet (nicht mit Testdaten ergänzt), korrekte Filterung auf Tarifcheck, keine Exportfunktion im Frontend, keine Auswirkungen auf andere Partner/Portale. Tests mit synthetischen Eingaben sind dafür nur technische Tests – noch kein Nachweis des echten 80er-Bestands.
**Danach einzige Nutzerhandlung:** aktuelle Affiliate-Zentrale ersetzen/aktualisieren, im WordPress-Backend **einen Export-Button** drücken, die **eine erzeugte Datei** im Chat hochladen. **Nicht** tausend Screenshots und **kein Neuimport**.
**Erst nach Einsicht in diese echte Datei:** für jeden der 80 Fälle die Ursache festhalten (Quellinfo vorhanden, aber nicht gelesen / Quelle fehlt / passende Kategorie fehlt / passende Oberkategorie vorhanden), den **einen bestehenden Zielentscheider** gezielt korrigieren, komplette End-to-End-Abnahme, dann genau eine Version freigeben.

## 6. Verbindliche Arbeitsregel ab sofort
**Nicht erneut um eine alte HTML-Sammeldatei bitten, solange ein einzelner vorhandener Datenbankexport den Ist-Stand liefern kann. Keine neue Zuordnungs-Version ohne genau diese Quelldaten. Keine unbewiesenen Erfolgsmeldungen oder erneuten Zwischenstopps mit Kleinreparaturen.**

**Büro-Quelle:** `protocol/PROJECT_MEMORY/PROJEKTE/EIGENTUMSSCHUTZ/AFFILIATE/CURRENT_STATE.md`. Diese Akte dient als kompakte Chat-Übergabe.
