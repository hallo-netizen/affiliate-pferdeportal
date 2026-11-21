# Hobbydepot Original-Workflow-Übertragung 0.4.24.15 (20.11.2026)

**Originale direkt byteverglichen:** Pferdeatelier-Texterstellung 0.4.34 vs. Hobbydepot 0.4.24.14.

## Nachgewiesene Ursache
Im Hobbydepot fehlten gegenüber dem funktionierenden Pferdeatelier die vorhandenen Originalfunktionen für MINI-Wiederaufnahme und technischen Abschluss nach dem letzten gültigen MINI-Worker-Receipt. Dadurch blieb ein Auftrag trotz CATEGORY/EDITORIAL/TITLE ohne vollwertige automatische K0-Übergabe hängen. Außerdem fehlten der redownload des gespeicherten MINI, die konkrete MAGAZIN-Unterkategorie-Bindung und der originale CATEGORY-Checkpoint-Aufbau. Der ursprüngliche Research-Audit-Fehler aus dem Benutzerscreenshot wird bereits durch 0.4.24.14 behoben und bleibt unverändert in 0.4.24.15 erhalten.

## Übertragung
Originale aus Pferdeatelier 0.4.34 an die übereinstimmende Stelle übernommen: `checkedMiniCategory`, `finishProvenMiniRow`, `finishSavedMiniRows`, `savedMiniChoices`, `savedMiniDownload`, `miniWorkerCheckpoint`, `k0Package`, `export`, `seoImport`, `miniResumeReceipt` sind nach der Übertragung **je byteidentisch**. Dazu gehören die Original-Arbeitsschritte und UI-Eingänge für gespeicherte MINI-Aufträge. MAGAZIN benötigt für Hobbydepot andere existierende WordPress-Kategorien als Pferdeatelier; in der bestehenden CATEGORY-Bindung werden ausschließlich konkrete Leaf-Kategorien unter einem vorhandenen eindeutigen WordPress-`magazin`-Term zugelassen. Es werden keine Kategorien erfunden oder angelegt. Der originale PSTE-Rechercheengine-Quelltext bleibt zu 0.4.24.14 byteidentisch.

## Ausführbare lokale Tests
- **21 Testläufe / 165 positive explizite Prüfausgaben**, zusätzlich 78 PHP-Syntaxprüfungen, 8 JSON-Validierungen, 87 ZIP-CRC, 86/87 Originaldateien unverändert.
- ORIGINAL Research-Gate -> original MINI CATEGORY -> EDITORIAL -> TITLE -> automatische ursprüngliche Order/Slot-Buchung -> signierter 5-Felder-K0-Eingang -> originaler WordPress-Entwurfsimport erfolgreich am isolierten Fixture.
- ORIGINAL MINI-MAGAZIN-Workflow ebenfalls erfolgreich, einschließlich negativer Fälle (unzulässige Root, andere Kategorie, unklare Rootstruktur, duplicate, kein Originalkontext).
- 7 originale Recherche-/Abbruchzustände, 5 Original-AJAX-Zustände, 4 Original-Admin-Ansichten und Saved-MINI-Adminansicht; keine DataForSEO-Provider-POSTs.
- Original Retained Backlog Audit: 92 positive und negative Prüfungen; 15 echte Abhängigkeiten; fehlende und veränderte Dateien blockieren.
- Zwei tatsächlich früher K0-verifizierte Pferdeatelier-Artikel aus Nutzerdaten mit ORIGINAL PSERC-Importer zu Entwürfen angelegt, keine Duplikate. Kein neuer K0-Schreibnachweis für Hobby.

## Ehrliche Nachweisgrenze
Kein direkter Zugriff auf den WordPress-Datenbankbestand mit 223 Rohkeywords, keine Live-Reanalyse. Der externe original K0-Writer/LanguageTool 6.8 wurde für ein **neues** Hobbythema nicht wirklich ausgeführt; allein die Datei- und Importgrenzen wurden mit simuliertem Artikelinhalt geprüft. Ein vollständiger echter Hobby-Artikel ist deshalb **nicht nachgewiesen**.

## Ablage
**Genau eine neue WordPress-ZIP**, im persönlichen Hobbydepot-Plugin-Büro unter
`/Hobby Depot/Plugin-Büro/Texterstellung_Hobbydepot_0.4.24.15_PFERDEATELIER_ORIGINAL_WORKFLOW.zip`,
SHA256 `22048ef1850d44d922d6738a40c5cebcd4a6a474a393c26b5d1f86888510092b`, 518807 Bytes, root `texterstellung-hobbydepot/`. Daneben der gesamte Original-PHP-Testoutput in `Hobbydepot_0.4.24.15_ORIGINAL_GESAMTTEST_NACHWEISE.json`, lesbarer Prüfbericht, ausführbare Tests und aktualisierte `Texterstellung-CURRENT.md`.

Nächster Betriebsschritt: Backup -> ZIP über bestehendes Plugin ersetzen -> unter Recherche nur die bestehenden kostenlosen Keywords fortsetzen (keine neue bezahlte Recherche) -> MINI-Redaktionsplan und K0-Originalweg im echten WordPress prüfen.
