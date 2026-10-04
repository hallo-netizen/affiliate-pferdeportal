# K0 START — ARTICLE PRODUCTION ONLY

Bei `K0:start` gilt ausschließlich:

1. `K0_CURRENT_STATE.json` auf dem K0-Branch lesen.
2. `K0_GOAL_CONTRACT.json` lesen.
3. Den aktuellen Upload als neuen Produktionsauftrag behandeln.
4. Ausschließlich die Artikelproduktion ausführen:
   `Upload -> frische Recherche dieses Runs -> Writer -> vollständige Regeln -> LanguageTool 6.8 -> PPM 6.7.9 -> finale Regeln -> SYSTEM4_WORDPRESS_HANDOFF_V1 -> Verifikation -> Chat-Datei`.
5. Fehlt eine notwendige Lauf-Evidence oder blockiert ein Gate, sofort mit dem exakten terminalen Blocker stoppen.
6. Während eines Artikellaufs sind keine Änderungen an Code, Workflows, Konfiguration, Plugins oder Darstellung zulässig.
7. Keine andere Current-Autorität, kein anderer Produktionsweg und keine historische Laufquelle darf als Start- oder Arbeitsweg verwendet werden.
8. Frühere Artikel, Drafts, Fact-Packs, Research-Pakete und Laufoutputs dürfen nicht als Inhaltsquelle verwendet werden.
9. `publish_allowed=false`.

Sichtbares Chatverhalten:
- keine Vorrede;
- keine Statusmeldung;
- keine Prüfankündigung;
- keine Prozessbeschreibung;
- keine Zwischenmeldung;
- keine Bitte um `weiter`.

Die erste sichtbare Antwort ist ausschließlich:
- die fertig verifizierte WordPress-Datei als echte Chat-Datei; oder
- ein echter terminaler Produktionsblocker.
