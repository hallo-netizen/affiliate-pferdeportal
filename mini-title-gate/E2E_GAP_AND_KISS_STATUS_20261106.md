# Pferdeatelier MINI – Quell-/Laufzeitabgleich 06.11.2026

**K0 nicht geändert. Dieser Nachweis betrifft ausschließlich den MINI-Workflow.**

## Bestätigte Ergebnisse

- GitHub: `hallo-netizen/mini-titelpruefer` (privat, nach Abschluss kein ChatGPT-Zugriff). Reale GitHub-Action mit absichtlich fehlerhaftem Titel erzeugte Reparaturstatus, Run [42196709788](https://github.com/hallo-netizen/mini-titelpruefer/actions/runs/42196709788). Reale GitHub-Action nach Korrektur erfolgreich, Run [42196918970](https://github.com/hallo-netizen/mini-titelpruefer/actions/runs/42196918970). Beide Läufe prüfen gegen feste Regeln und LanguageTool 6.8. Kein externer KI-API-Aufruf.
- WordPress-PSTE Teststand `0.57.144.11`: In `includes/class-pste-mini-workflow.php` akzeptieren `importKeywords` und `importTitleCorrections` nur `PSTE_MINI_APPROVED_DELIVERY_V1` mit gültiger RSA-Signatur, Regel-/Batchbindung und fest hinterlegtem öffentlichem Schlüssel.
- Der derzeitige GitHub-Gate-Lauf erstellt **keine passende signierte Freigabe**. **Daher ist die GitHub→WordPress-Verbindung nicht funktionsfähig.** Keine Freigabe und kein weiteres Zwischenplugin ausgeben.
- Titelqualität (natürliches Deutsch, Suchabsicht) wird nicht vollständig durch feste Muster und LanguageTool garantiert. Die textliche Reparatur muss der Titelworker weiterhin leisten; GitHub erstellt Reparaturbericht, aber noch keine automatische Neutextung.
- K0, PSERC, LIVE und Campus Current wurden nicht geändert.

## KISS: verbindliche Zielgrenze

**EIN** Start, **EIN** verbindlicher Regelsatz, Titelworker als Vorschlag, **EIN** separater Prüfer mit Reparaturschleife, **EIN** aus dessen Freigabe hervorgehender verifizierbarer Import. WordPress darf keine zweite Titelqualität durchführen; muss aber Herkunft und Dateibindung überprüfen können.

Keine neuen APIs, kein manuelles Schlüsselerzeugen, keine wiederholten GitHub-Zugriff-Umschaltungen. **Technische Grenze:** Ein vom Chat selbst erzeugtes identisches JSON kann ohne separat überprüfbaren Herkunftsnachweis nicht sicher von einer echten GitHub-Ausgabe unterschieden werden. Eine Prüfung der Datei *allein* kann die geforderte Unabhängigkeit nicht erzwingen. Signaturzwang deshalb nicht still entfernen.

**Nächste Arbeit als EIN Paket:** Eine nachweislich kompatible, schlüssellos für den Nutzer funktionierende Herkunftsbindung bis WordPress auswählen, beide Enden vor Installationsanforderung vollständig gegentesten, dann erst ein kumuliertes Testupdate zur Freigabe vorlegen. Bis dahin keine Vollzugsmeldung.

Diese Notiz ist QA-Evidence und **keine zweite Current-/NEXT-ACTION-Autorität**, keine Produktionserlaubnis.
