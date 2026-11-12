# Pferdeatelier – Stand 12.11.2026: K0, Themenengine und Redaktionsplan

## Nachgewiesener Stand
- K0: die Änderungen vom 10. November sind im aktiven Zweig `konzept0-portal-neutral-20261002`, die vier doppelt gewordenen K0-Regeln und die dortige zweite Suchintententscheidung sind entfernt; der vollständige GitHub-Selbsttest war erfolgreich: https://github.com/hallo-netizen/affiliate-pferdeportal/actions/runs/43190083815 .
- Themenengine: getestete Test-ZIP `PSTE-0.57.144.42-EINMALIGER-INTENT-OWNER-NUR-TEST.zip`, WordPress-Plugin-Header `0.57.144.42`. Korrigiert die fehlende Abschlussbindung einer vorhandenen Themenentscheidung. Lokale Tests bestanden, nicht als erfolgreich installierter WordPress-Livelauf nachgewiesen.
- Redaktionsplan: zuvor trotz geänderter Paketbindung weiter als `0.28.67` verpackt, deshalb zeigte WordPress dieselbe Versionsnummer. **Das war ein Verpackungsfehler.**
- Redaktionsplan neu verpackt: `Redaktionsplan-PSERC-0.28.68-TEST.zip`; Header und interne Versionskennung `0.28.68`, dazu erneuerte vorhandene Paketbindung. **Ausschließlich zwei Dateien gegenüber der .67-Testversion geändert:** Plugin-Hauptdatei (Versionszeilen) und bestehender Paketvertrag (Version/Hash). Keine zusätzlichen Plugins, Klassen, Prüfungen oder Abläufe. SHA-256 ZIP `83ce255385a631cf382b9e8e7212eec5990af2baca65e3b797aeae198be05c89`.
- PHP-Original-Integritätsprüfung der .68-ZIP: `PSERC_COMPILER_PACKAGE_INTEGRITY_PASS`, alle 61 Paketdateien geprüft; PHP-Lint 43/43 erfolgreich.
- Die .68 ist eine **Testversion**, noch kein nachgewiesener WordPress-Installations- oder dreifacher K0-Endlauf.
- Die drei ursprünglichen Redaktionsaufträge sind im bisherigen GitHub-Sicherungsbestand vorhanden. Artikel 1 besitzt bereits eine historisch geprüfte WordPress-Datei; für Artikel 2 und 3 fehlt der fertige Text. Keine WordPress-Schreibzugriffe nötig; Standardweg ist GitHub → verifizierte WordPress-Importdatei.

## Nächster tatsächlicher Test
1. **Nur auf isolierter WordPress-Testinstallation** die vorhandene PSTE-Testversion .42 und die PSERC-Testversion .68 installieren/ersetzen.
2. Im Backend nach erfolgreicher Aktivierung **die normalen vorhandenen** Themen- und Redaktionsplan-Menüs prüfen; keine Massen-Neubewertung aller etwa 5.000 Themen und keine automatische Neuvergabe historischer Freigaben.
3. Nur die drei gesicherten Artikelidentitäten über den vorhandenen Redaktionsplan-Export und den aktiven GitHub-K0-Weg führen; danach genau drei echte geprüfte WordPress-Importdateien als Erfolg werten.
4. Scheitert bereits Schritt 1 oder 2: konkret sichtbaren Backend-Fehler beziehungsweise einen einzigen normalen Export liefern, **keine weitere Annahme über die Ursache**.

**Wichtig:** Die 0.28.68-Testversion ist nicht in WordPress installiert oder im produktiven Betrieb nachgewiesen. Status und Grenzen sind ausdrücklich Teil dieses Protokolls.
