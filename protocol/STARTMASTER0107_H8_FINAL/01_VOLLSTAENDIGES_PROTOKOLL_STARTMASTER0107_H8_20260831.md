# STARTMASTER0107 / H8 – VOLLSTÄNDIGES PROTOKOLL

Stand: 2026-08-31  
Repository: `hallo-netizen/affiliate-pferdeportal`  
Aktueller `main`: `a3708a322f493578596c374736ef328d0caba504`

## 1. Ausgangslage

Der erste reale 7er-Artikeltest nach Einführung des Single-Door-/Wächtersystems war fachlich unbrauchbar. Die Artikel waren u. a. wegen fehlender bzw. nicht zuverlässig durchlaufener Fach-/Qualitätsstufen nicht als gültiger Produktionsnachweis verwendbar.

Wichtig: Die Ursache war nicht, dass der Wächter fachlich falsch geprüft hätte. Der Wächter soll und darf Fachqualität überhaupt nicht prüfen. Die Ursache lag vor der wirksamen Single-Door-Kette: Beim Runtime-Zustand `READY_WAITING_PACKAGE` wurde bereits ein fertiges signiertes Produktionspaket verlangt. Dadurch existierte vor der ersten wirksamen Pakettür ein Raum, in dem freie Chat-Arbeit stattfinden konnte.

## 2. Bereinigung des alten 7er-Laufs

Lokal wurden 81 erzeugte/fehlerhafte 7er-Artefakte entfernt. Der alte vollständige Produktionsplan mit den fehlerhaften Artikelkörpern wurde ausschließlich forensisch quarantänisiert und darf nicht als Produktionsquelle verwendet werden.

Nicht gelöscht oder verändert wurden:
- bestehende Wächter-/STARTMASTER-Systemquellen,
- bestehende Fachregeln,
- bestehende GitHub-Systemdateien,
- WordPress-Inhalte des Nutzers.

Die WordPress-Artikel selbst konnten durch diesen Chat nicht gelöscht werden.

Als saubere Neustartbasis bleibt ausschließlich die aktuelle metadata-only Generation-1-Bindung mit 7 Themen bestehen.

## 3. Harte Ursachenanalyse

Geprüfte Varianten:

1. Nur härterer Prompt → VERWORFEN. Ein Prompt ist keine technische Akzeptanzsperre.
2. Nur bisherige `R_PRE_001`-Pakettür → VERWORFEN. Paketentstehung läge weiter vor der Tür.
3. Zusätzliche Tür ohne technische Herkunftsbindung → VERWORFEN. Ein frei erzeugtes Paket könnte theoretisch eingeschleust werden.
4. Gewählt → `R_BOOT_001` vor `R_PRE_001`, plus signierte H8-Herkunftsbindung und erneute Provenance-Prüfung vor `R_001`.

## 4. H8-Zwangsjacke – technische Zielkette

`Sekunde 1 -> R_BOOT_001 -> H8-gebundene Paketerzeugung -> R_PRE_001 -> Herkunftsprüfung -> R_001 -> bestehender unveränderter Fachworkflow`

Grundsatz:
- Der Wächter ist fachblind.
- Der Wächter bewertet keine Artikelqualität.
- Der Wächter kennt keine SEO-/Text-/Tabellen-/Link-/LanguageTool-/PPM-/PSERC-/PSTE-Qualität.
- Er prüft nur mechanisch Raum, Aktion, Beleg, Hash/Signatur, Batch-/Snapshot-Bindung und Herkunft.
- Kein gültiger technischer Beleg → kein Weiterkommen.

## 5. Umgesetzte H8-Komponenten

Produktiv gemergt mit PR #58, Merge-Commit `298711faf3a17ff3faeed53de8276f812523c96d`:
- `control/CURRENT_STARTMASTER.json` → `project_single_door_entry_v2.py`
- neue erste Tür `R_BOOT_001`
- H8 Boundary Manifest
- H8-Provenance-Guard
- H8 Runtime-Guard
- H8-positive/negative Tests
- 107007-Hardlock auf H8-Einstieg
- Notfall-Einlass für neue Chats

Dokumentationsnachführung PR #59 wurde ebenfalls gemergt; aktueller `main` ist `a3708a322f493578596c374736ef328d0caba504`.

## 6. Testnachweise

Vor Produktivmerge:
- H8 positive/negative: 8/8 PASS
- Legacy Single-Door Regression: PASS
- Codex Cloud Entrance: PASS
- Production Continuity: PASS
- Realer Repository-Testzustand: `R_BOOT_001`
- `quality_authority = NONE`
- `content_semantics_inspected = false`

Nach Produktivmerge:
- Deterministic Entrance Gate Run 104: SUCCESS
- Nach Dokumentationsmerge auf aktuellem `main`: Deterministic Entrance Gate Run 106: SUCCESS

Der bekannte alte Umgehungsweg wurde negativ nachgestellt: Ein altes/frei erzeugtes Paket ohne gültige signierte H8-Herkunft darf `R_001` nicht erreichen.

## 7. Was ausdrücklich NICHT verändert wurde

Keine Änderung an:
- Recherche-/Fact-Pack-Regeln
- Textmaschinenvertrag
- Artikeltypen
- Titel-/Keyword-Regeln
- internen Links
- Tabellenregeln
- LanguageTool
- PPM
- PSERC
- PSTE
- Dubletten-/Kannibalisierungsschutz
- SEO
- Design/Format
- Publish-Regeln
- Auto-Publish bleibt verboten

## 8. Aktueller echter Runtime-Stand

- STARTMASTER: `STARTMASTER0107`
- nächster äußerer Step: `RUN_NEW_ARTICLE_BATCH_NO_STOP` / 107007
- `free_chat_execution_authority = false`
- Runtime: `BATCH_READY_PACKAGE_PENDING`
- Generation: 1
- Batch SHA-256: `7f2e3290b6ac78ac7df1644395e57ac72f02dc1373e390eb2e532e57a8ce916a`
- Runtime Source Snapshot SHA-256: `be73a986124fc80429c0c0d85fba94636a0ff5a506d23a6cff68f291e3645027`
- Produktionspaket-Ref: leer
- Produktionspaket-SHA: leer
- `publish_allowed = false`

Damit muss der aktuelle Lauf an `R_BOOT_001` beginnen.

## 9. Noch NICHT bewiesener/gebundener Restpunkt

Die serverseitige Producer-/Signer-Capability, die aus `R_BOOT_001` heraus das H8-gebundene signierte Paket erzeugt, ist im Repository nicht als verfügbare produktive Capability nachgewiesen.

Das ist bewusst fail-closed:
- keine Capability → keine Paketerzeugung,
- kein Paket → kein `R_PRE_001`-PASS,
- kein Herkunfts-PASS → kein `R_001`,
- kein Chat-Fallback,
- keine Ersatzsignatur,
- keine selbstgebaute Zwischenlösung.

Das ist der aktuell einzige bekannte technische Restpunkt vor einem echten neuen 7er-End-to-End-Lauf.

## 10. Nächster zulässiger Arbeitsauftrag

Im neuen Chat zuerst und ausschließlich:

`python3 control/single-door-boundary/project_single_door_entry_v2.py status`

Dann:
- bei `R_BOOT_001`: ausschließlich die gebundene Bootstrap-Capability ausführen;
- ist sie nicht verfügbar: exakt dort fail-closed bleiben und die fehlende Capability/Bindung nachweisen;
- keine Recherche, kein Artikeltext, kein Fact-Pack, kein Produktionsplan, kein eigenes Paket vor `R_001`;
- sobald `R_001` autorisiert ist, ausschließlich den bestehenden Fachworkflow ausführen;
- unmittelbar vor erster tatsächlicher Artikel-Texterzeugung Nutzer um den verbindlichen Artikel-Prompt bitten.

## 11. Protokollregel ab jetzt

Jede weitere Änderung muss dokumentieren:
- Was wurde geändert?
- Was wurde ausdrücklich nicht geändert?
- Welcher positive Test wurde bestanden?
- Welche negativen Bypass-Tests wurden bestanden?
- Welcher GitHub-PR/Commit ist autoritativ?
- Welcher Runtime-State ist aktuell?
- Gibt es einen offenen fail-closed Restpunkt?
