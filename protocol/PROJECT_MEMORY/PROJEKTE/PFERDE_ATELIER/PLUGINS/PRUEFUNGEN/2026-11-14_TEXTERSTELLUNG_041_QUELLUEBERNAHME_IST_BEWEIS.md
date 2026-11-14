# Beweisakte: Texterstellung 0.4.1 ist KEINE 1:1-Übernahme der Altplugins

**Prüfdatum:** 14.11.2026. **Messbasis:** tatsächlich vorliegende unveränderte ZIP-Dateien, direkte Extraktion sämtlicher PHP-Dateien und Vergleich der Datei-Bytes. Das ist ein rückblickender **Ist-Nachweis**, **keine neue Pluginentwicklung** und **keine Produkt-/Livefreigabe**.

## Originaldateien – Bezug
- PSTE QA 0.57.144.50: `Pferdeatelier_PSTE_0.57.144.50_KISS_NUR_QA_NICHT_INSTALLIEREN.zip`, SHA-256 `7fc98a17e4c2319a66afd23c0ad944a07b4492e7a9982933205f29069fdcd121`, **83** PHP-Dateien.
- PSERC QA 0.28.71: `Pferdeatelier_PSERC_0.28.71_KISS_NUR_QA_NICHT_INSTALLIEREN.zip`, SHA-256 `fd80f7ec3451b437be0eaeedabf2142c5eb1b5130939f7b8dba3b3a2f9d2b59f`, **42** PHP-Dateien.
- Beide sind alte **QA**-Quellen und daher kein behaupteter Nachweis, dass der aktuelle Live-Server exakt diese Fassungen enthält.
- Texterstellung 0.4.1 Test: `Texterstellung_0.4.1_TEST_INSTALLIEREN.zip`, SHA-256 `f34fe278eaca382ca99c7f537463644dbd1508b9fb4198980e173df59edae280`, **6** PHP-Dateien.

## Nachprüfbare Gegenüberstellung
**Zahl der PHP-Dateien der Texterstellung, deren Inhalt bytegenau einer der 125 alten PHP-Dateien entspricht: 0 / 6.**

| Texterstellung 0.4.1 Datei | Byte-identischer Originaltreffer | Beste Zeilenähnlichkeit im direkten Einzeldatei-Vergleich |
|---|---|---|
| `includes/class-txe-credentials.php` | **NEIN** | rund 19 % (keine belegte unveränderte Übernahme) |
| `includes/class-txe-dataforseo-client.php` | **NEIN** | rund **95,7 %** zu `PSTE/includes/class-pste-dataforseo-client.php`; offenbar weitgehend abgeleitet, **aber geändert** |
| `includes/class-txe-diagnose.php` | **NEIN** | rund 13 % (keine belegte unveränderte Übernahme) |
| `includes/class-txe-normalizer.php` | **NEIN** | rund 30 % (keine belegte unveränderte Übernahme) |
| `includes/class-txe-secret-store.php` | **NEIN** | rund **98,2 %** zu `PSTE/includes/class-pste-secret-store.php`; weitgehend abgeleitet, **aber geändert** |
| `texterstellung.php` | **NEIN** | rund 5,7 % zur ähnlichsten einzelnen Original-PHP-Datei (massiv neu strukturiert) |

Die Ähnlichkeitswerte sind **nur** ein Hinweis auf Textübernahme aus einer **jeweils einzelnen** alten Datei; sie können nicht beweisen, dass Ausschnitte aus mehreren anderen Dateien unverändert zusammengesetzt wurden. Nur der SHA-/Bytevergleich beweist fehlende Dateiidentität. „Kein Code aus dem Original verwendet“ wäre ebenfalls falsch: zwei Dateien zeigen klare Wiederverwendung mit Änderungen.

## Belegbare Zielvertragsverletzung / Abnahmekonsequenz

- Original-PSTE recherchierte `peopleAlsoAsk` im Recherche-Job. Die Texterstellung 0.4.1 hat zwar die DataForSEO-Clientmethode, aber der normale Rechercheknopf ruft die Google-Fragen-Funktion nicht auf.
- Die automatisierte fachliche SEO-Entscheidung (Suchintention, Kategorien, Abdeckung, Dopplungen) ist nicht vollwertig übernommen, sondern durch Handfelder/externe Entscheidungsdatei teilweise ersetzt.
- Damit ist **keine vollständige Funktionsgleichheit** belegt. Die bisherige Angabe „voller Workflow“ oder „alles unverändert übernommen“ wäre unzutreffend. **0.4.1 darf nicht als vollständiger Ersatz freigegeben werden.**
- Auch `0 / 6` identische Dateien allein zeigt nicht, welche Funktionsweise erhalten oder verändert ist. Dazu muss die künftig verpflichtende **1:1-Funktionsliste** mit Originalaufrufen, Ein-/Ausgabedaten und echtem WordPress-E2E-Test vorliegen.

## Pflicht für JEDES kommende Plugin-Release
1. Original-Quelle mit SHA fixieren (QA und tatsächlicher Livebestand getrennt).
2. **Alle** Funktionen und Automatismen aus alten Plugins inventarisieren; Quelle/Originalfunktion → Zielfunktion zuordnen.
3. Pro PHP-Datei **SHA-Identität oder vollständigen Zeilen-Diff**, dazu Herkunft und jede neue Adapterzeile sichtbar machen.
4. Jede unersetzte alte Funktion, entfernte Google-Fragen-Abfrage, nachgelagerte SEO-Entscheidung oder neue fachliche Implementierung = **BLOCKIERT**; kein Installer.
5. Ohne echten Alt-Neu-Lauf (Recherche, vorhandener Bestand, Titel, K0, Sofortauftrag, Rückimport) keine Aussage „vollständig“.
6. Messprotokoll mit konkreten Zahlen und vollständiger Nachweisdatei auf GitHub **vor** Download. Bisheriges Live und Plugins nicht verändern.

**Status:** 0.4.1 retrospektiv geprüft, **NICHT vertragskonform als Altplugin-Ersatz**. Kein neuer Installer gebaut. Zielvertrag Regel 23 ergänzt.
