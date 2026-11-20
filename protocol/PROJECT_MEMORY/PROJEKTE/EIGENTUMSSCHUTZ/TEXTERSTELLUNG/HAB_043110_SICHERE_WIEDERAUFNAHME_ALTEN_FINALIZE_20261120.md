# 20.11.2026 – Hab 0.4.31.10 – den bereits bezahlten ALT-FINALIZE sicher fortsetzen

## 1. Nachgewiesene Ursache, warum Kopieren allein nicht genügte
Live-Screenshot 13:41 (bereits mit Hab 0.4.31.9): Queue `RUNNING`, Item `BLOCKED_PENDING_PARK`, Child `PAUSED_ERROR` in Phase `FINALIZE:SANDBOX_STORE_READY`. Letzter Fehler `PSTE_SANDBOX_RECORD_STORE_LEGACY_OPTION_MISSING`. 9 Rohkeywords empfangen und 0 fertige Kandidaten.

Pferdeatelier-Originalcode und Hobbydepot-Fehlerliste wurden bereits vollständig in `HAB_04319_HOBBY_GESAMTFEHLERLISTE_PFERDEATELIER_ORIGINALTEST_20261120.md` verglichen; der Original-Pferdeatelier-Code erwartet beim ersten Lauf einen früheren Datenspeicher, Hobbydepot 0.4.24.15 hatte das bereits repariert. Hab 0.4.31.9 enthält den Fix für neue Speicherinitialisierung, **nicht aber eine Wiederaufnahme bereits PAUSIERTER alter signierter Queue/Job-Datensätze**. `Status aktualisieren` ist nur Anzeige; der Original-Driver würde `BLOCKED_PENDING_PARK` archivieren, statt nochmals zur alten lokalen Abschlussprüfung zu springen.

## 2. Gebündelte gezielte Reparatur (kein Forschungs-Neubau)
Im Original Hab 0.4.31.9 als **0.4.31.10** ausschließlich 4 von 87 Dateien geändert:
- `original/pste/includes/class-pste-research-job.php`: ausdrückliche einmalige Wiederaufnahme allein bei `PAUSED_ERROR`, dem exakten Speicherfehler, `FINALIZE`, `SANDBOX_STORE_READY`, korrekt signiertem Child-Owner und vollständig vorliegenden ursprünglichen 3 Keyword-Providerergebnissen plus Originalfragen. Nutzt die **bereits bestehende Originalfunktion** `recoverReplaySafeLocalFinalizePause` mit Original-Replay-Receipt.
- `original/pste/includes/class-pste-breadth-research-queue.php`: unter der bisherigen originalen Queue-Sperre prüft derselbe bereits gespeicherte Queue-UUID, Kind-UUID, Kategorie-ID, ursprünglicher Seed und Index; nur den alten Auftrag freigeben, keine neue Kategorie/Fachentscheidung.
- `texterstellung.php`: ein einmaliger Admin-Button `Vorhandenen Abschluss ohne neue Kosten fortsetzen` in `Texterstellung → Recherche` ausschließlich bei exakt diesem Problem. Original-Driver wird mit der vorhandenen `kick`-Methode neu angestoßen, **keine** neue DataForSEO-Bestellung; Version 0.4.31.10.
- README: Installationsschritt.

Die übrigen **83 Dateien bitidentisch**. Alle bestehenden DataForSEO-Methoden (Suggestions, Related, Ideas, PAA), Original-MINI, K0-Fünffelder und PSERC-Import unverändert. **Original-K0 in GitHub unverändert, K-Multi unangetastet.**

## 3. Beweise aus realen PHP-Methoden (alle nach Entpacken des endgültigen ZIP erneut ausgeführt)
- **9/9** Original `PSTE_Research_Job` mit signiertem alten LOCAL-FINALIZE, inklusive neun empfangenen Keywords und harten Sperren bei unvollständigem PAA, falschem Phasenstand, beschädigter Hashsumme.
- **11/11** Original `PSTE_Breadth_Research_Queue`: richtiger und falscher Besitzer/Kategorie/Seed/Job/Queue, Queue-Hash, kein neuer bezahlter Auftrag.
- **5/5** beide tatsächlichen Original-PHP-Klassen gemeinsam: 1 positiver Wiederanlauf und 4 negative, alte Anbieterfakten unverändert; Testfall exakt `RUNNING` + `BLOCKED_PENDING_PARK` + `PAUSED_ERROR` + `FINALIZE:SANDBOX_STORE_READY`.
- **48/48** originale vier Keyword-Recherchewege, **11/11** originale PAA-GETs, **8/8** originale PAA-Queue-Rettung, **11/11** PAA-Originaljob, **17/17** Hab-MINI und **14/14** Hab-K0-/simulierter WordPress-Import.
- **134/134** bestandene lokale Positiv-/Negativprüfungen, **78/78 PHP-Lints**, **87/87 ZIP-CRC**.
- **Keine reale DataForSEO- oder WordPress-Schreiboperation in diesen Tests.** Echte Rechterschalter/gespeicherte Daten können weiterhin korrekt ablehnen, wenn der Originalstatus vom Screenshot abweicht.

**ZIP:** `Texterstellung_HAB_UND_BEWAHR_0.4.31.10_BESTEHENDEN_ABSCHLUSS_FORTSETZEN.zip`, SHA256 `a63bd75a9a4d2a127299477bf2c78742a156da63932bab4574f050c233a27b99`, 523842 Bytes. Alle Ausführungsprotokolle, Testquellen, Originaldiff und Prüfergebnis tatsächlich im Hab-Büro unter `/hab-und-bewahr/TEXTERSTELLUNG/PRUEFUNG_ALTABSCHLUSS_20261120/` gespeichert; ZIP unter `/hab-und-bewahr/TEXTERSTELLUNG/PLUGIN_FREIGABEKANDIDATEN/`.

## 4. Präzise Grenze und nächste Aktion
**Noch kein vollständiger Live-E2E-Erfolg**, keine reale K-Multi-Texterstellung und kein fertiger WordPress-Draft. Es ist gezielt der bereits nachgewiesene **Alt-Auftrag-Fortsetzungsfehler** korrigiert und getestet.

1. WordPress-Backup.
2. Vorhandenes Hab-Plugin 0.4.31.9 mit 0.4.31.10 als vorhandenes Plugin **ersetzen**, nicht deinstallieren oder Auftragsoption löschen.
3. `Texterstellung → Recherche`, **`Vorhandenen Abschluss ohne neue Kosten fortsetzen` genau einmal klicken.**
4. Keine neue kostenpflichtige Recherche starten. Anschließend aktuelle `Texterstellung → Diagnose`-JSON herunterladen und nachweisen, ob der ursprüngliche Schritt `FINALIZE` beendet wurde; erst dann folgt originaler MINI-Export.
5. Fehlt die Schaltfläche oder meldet der Originalauftrag einen nicht passenden Status: nicht blind neu starten; Diagnose sichern.

**Keine vollständige Produktionsfreigabe behaupten.**
