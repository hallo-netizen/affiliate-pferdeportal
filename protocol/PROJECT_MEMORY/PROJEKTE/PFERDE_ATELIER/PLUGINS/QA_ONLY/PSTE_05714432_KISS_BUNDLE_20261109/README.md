# PSTE 0.57.144.32 – Gesamtänderung (nur WordPress TEST)

**Ausgang:** Echte private PSTE 0.57.144.31 (SHA und 121 Einträge verifiziert), bereits auf WP-Test vom Betreiber installiert. Kolik-Kategorie dort erfolgreich gespeichert. Dieses v32-ZIP ist **neu gebaut und lokal geprüft, aber noch nicht auf WordPress installiert**. K0, PSERC, PPM, LIVE und andere Portale unberührt.

## 1. Bedienbarkeit
- Vor der Kategorieauswahl Hauptnavigation oder Magazin auswählen; danach alphabetisch gefilterte Kategorieauswahl mit eindeutiger Term-ID.
- Für normale Zuordnung kein Begründungsfeld; Rückkehr nach Erfolg/Fehler in das vorhandene Redaktionsbüro.

## 2. Kategorieautomatik
- Im bestehenden Redaktionsbüro wird dessen vorhandener Datensatzbestand automatisch read-only gebündelt analysiert (max. 200 je Aufruf); eindeutige bereits existierende Fach-/Magazin-Kategorien, fehlende Kategorien und ungeklärte Fälle werden getrennt angezeigt.
- Für **nur eindeutig identifizierte bestehende Kategorien** gibt es einen einzigen Sammelübernahme-Knopf; der vorhandene geschützte Zuordnungs-/Wiederprüfungsweg wird wiederverwendet, ohne neue Tabelle/Worker. **Der Knopf muss vom Betreiber bewusst betätigt werden**. Keine selbsttätige Kategorieanlage und keine K0-Freigabe.
- Ursache des Kolik-Fehlwegs: Die bestehende Magazin-Klassifikation erkannte zwar das Gesundheitsthema, behandelte aber direkte medizinische Fragen oder das Kurzthema 'Kolik beim Pferd' nicht als ausreichend redaktionell. Der Original-Journal-Owner erkennt diese medizinischen Themen jetzt als Magazin-Kandidaten. Die konkrete Term-Bindung braucht weiterhin real vorhandene eindeutige WP-Kategorie. Harte Sperren bleiben geschützt.

## 3. Originaler MINI-Titel-Owner
- Ursprüngliche Governance und direkte Stapel-Instruktion verlangen eine Hauptsuchfrage je Titel. Zwei Suchfragen im selben Titel werden beim ursprünglichen MINI-Eingang **pro betroffenen Eintrag** zurückgestellt; korrektes Material im gleichen Stapel bleibt erhalten.
- Die neue Governance verändert bereits exportierte, eingefrorene MINI-Stapel nicht rückwirkend, und der gespeicherte Kolik-Titel wird nicht still geändert. Keine zweite Titelentscheidung in WordPress.

## Lokale Prüfungen
- 121/121 unveränderte Archivpfade, nur 5 bestehende Dateien verändert; 116 bytegleich; 83/83 PHP-Syntax; CRC und volles ZIP-Rücklesen bestanden.
- 17 gezielte smoke checks + 7 MINI-Import-/Kompatibilitätsprüfungen bestanden. Alte 6646 v31-Prüfungen **nicht** als neue v32-Abnahme ausgegeben.
- Kein echter v32-WordPress-Test, kein vollständiger WP/PSERC/PPM/K0-Endtest (FULL_WORKFLOW_PASSED=false).

**QA-Binärdatei (privater Plugin-Schrank):** `/pferdeatelier/PLUGINS/QA/PSTE-0.57.144.32-KISS-REDAKTIONSBUERO-AUTOMATIK-TITEL-NUR-TEST.zip`  
**SHA256:** `ab0231850a9b79b3c5f8b103b2700bc7f6b2a87d3adac38009f43c1bbe2f653f`  
**Quelländerungen:** [vollständiger Patch](PSTE_05714431_to_05714432_FULL_SOURCE.patch)  
**Maschinenbericht:** [QA_MANIFEST.json](QA_MANIFEST.json).

**PR #682 bleibt Draft/unmerged. Nicht mit altem PPA-005/CURRENT.zip gleichsetzen.**
