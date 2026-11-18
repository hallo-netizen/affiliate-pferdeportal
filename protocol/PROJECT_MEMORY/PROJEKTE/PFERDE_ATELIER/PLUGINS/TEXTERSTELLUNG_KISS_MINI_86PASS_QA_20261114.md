# Pferdeatelier – MINI/K0 KISS: 86 QA-Tests nach tatsächlichen Wiederanlauffehlern

**Stand 14.11.2026. Status: QA_ONLY, NICHT installationsreif.** Frühere Entscheidungen nicht erneut öffnen. Der jüngste Betreiber-Zielvertrag bleibt `TEXTERSTELLUNG_KISS_ENDGUELTIGER_WORKFLOW_20261114.md`. Ein zentraler WordPress-Auftrag, ein externer MINI-Gesamtworkflow, eine Entscheidung pro Fachfrage, danach unverändertes K0 und Entwurfsimport.

## Drei im bereits vorhandenen Code tatsächlich behobene technische Übergabe-Fehler
1. **Magazin/JOURNAL wurde nicht über den Original-PSERC-Platzverteiler geleitet.** Die unveränderte vorhandene signierte Erweiterungsregistrierung `PSERC_Article_Type_Extension_Registry` liefert den Original-Plan-Kategorieschlüssel an den unveränderten `PSERC_Slot_Allocator`. Auch WordPress-Aliasnamen werden ausschließlich über die vorhandenen signierten Regeln abgebildet. **Keine neue Kategorieentscheidung, kein zusätzlicher Worker.**
2. **Bei einem Absturz nach Anlage des fertigen WordPress-Entwurfs, aber vor dem TXE-Auftragsstatus, wurde ein identisch signierter eigener Entwurf irrtümlich als fremder Platz blockiert.** Die bestehende technische Import-Sicherung lässt nun genau einen bereits vom unveränderten Original-PSERC-Importer angelegten, unveröffentlichten Entwurf mit identischer Artikel-ID, Planplatz und Sperrmarkierung zur Wiederaufnahme zu. Die originale importseitige Prüfung auf identischen Inhalt, Titel und Kategorie bleibt alleiniger Eigentümer. Kein zweiter Artikel und keine fachliche Nachprüfung.
3. **Magazin-Alias vs. Original-PPM-Kategorieschlüssel:** Ein einziger vorhandener technischer Kategorien-Abgleich für Zuweisung und Wiederlesen. Keine eigene fachliche Route.

## Ausgeführte aktuelle lokale Prüfungen
- **86/86** zielgerichtete Tests PASS: Original-PPM-Schutz 13, Originalplatzvergabe/Checkpoint 12, Journal-Routing 8, Magazin-Alias 8, Import-Abbruch genau nach gespeichertem Entwurf plus 3 manipulierte/fremde Entwürfe 14, 87 historische MINI-Entscheidungen und Crash-Reentry 14, 61 unveränderte Alt-FREI 11, 144 historische PPM-Identitäten 6.
- **117/117** PHP-Syntaxprüfungen PASS.
- Originale PSTE-/PSERC-Dateien bleiben gegenüber der ursprünglichen 0.4.3-ZIP **vollständig bytegleich**. Alle Änderungen liegen ausschließlich in der bereits vorhandenen Texterstellung-Hauptdatei; die vorherige Legacy-Brücke bleibt unverändert gegenüber der letzten QA.
- Aktuelle private QA-ZIP im **vorhandenen Plugin-Büro**: `/pferdeatelier/PLUGINS/ARBEITSRAUM_PSTE_KISS/TEXTERSTELLUNG_KISS_MINI_86PASS_QA_NICHT_INSTALLIEREN.zip`
- ZIP SHA256 `7dd7d6d5b9735c343354e971d330910611a86b9822b4a8f339e94ae3b65fd2e2`; 1.938.069 Bytes, 193 Einträge, CRC-PASS, aus der Library nach Upload **byteidentisch** zurückgelesen. Passender Bericht und exakter Kleinstpatch (gegen den vorherigen QA-Hauptdateistand) unter `.../TEXTERSTELLUNG_KISS_MINI_86PASS_QA_BERICHT.md` und `.../TEXTERSTELLUNG_KISS_MINI_86PASS_DELTA.patch`.

## Verbindliche Grenze für eine echte Installationsfreigabe
- WordPress-Bestands- und Testserver-Laufzeit sowie original signierter echter PPM-6.7.9-Plan **nicht** administrativ verbunden; in den lokalen Tests durch echte historische Eingabedaten und simulierte WordPress-Datenbank / signierte PPM-Kapazität ersetzt.
- **Externer** MINI-Teilworker-Checkpoint (Kategorieworker, Redaktionsworker, Titelworker) mit automatischer Fortsetzung nach einem beliebigen GitHub-/KI-Abbruch ist **nicht im realen Betrieb nachgewiesen**. WordPress-Rückimport pro Einzelzeile und Original-PSERC-Importabbruch sind getestet, aber ersetzen den Nachweis für externe KI-Zwischenschritte nicht.
- Echter K0-Schreibworker und WordPress-Entwurf auf isoliertem Testserver **nicht** ausgeführt. Daher ausdrücklich **keine 100%-Garantie und kein Produktionspaket** behaupten.
- Keinen neuen Plan, keine neue WP-Tabelle, keinen neuen Worker oder paralleles System bauen. **NEXT ACTION:** vorhandenen verbundenen WordPress-Testserver und den real laufenden externen GitHub-MINI-Weg für den einen identischen Auftrag unterbrechen und fortsetzen; erst danach installationsreifen Release freigeben.

`release_allowed=false`; keine Änderungen auf WordPress-Live oder am Original-K0.
