# QA68 – Pferdeatelier eBay: Ein gesamtes KISS-Paket 6.72.347

**Status:** 14.11.2026, vollständiges installierbares Plugin als **Teststand**, nicht auf der echten WordPress-/eBay-Installation abgenommen. Keine neuen GitHub-Scheduler, WordPress-Crons oder Worker hinzugefügt. Bestands- und Frontend-Strukturen unverändert.

## Gesamter Ablauf (ein Eigentümer je Entscheidung)

1. **GitHub** liefert lediglich den bestehenden eBay-Arbeitsaufruf. Kein zweites automatisches Recherche-Wecksystem.
2. **Kanonischer WordPress-Lauf** verwaltet exakt dieselbe UUID, Laufstatus, Cursor, Lease und Pause-/Fortsetzungsmarkierung; keine neue Suche bei inkonsistentem Zustand.
3. **Vollständige eBay-Suche**; nach deren tatsächlichem Abschluss direkt in bestehende Auswahlvorbereitung. Im Vollsync entfällt der globale Bestandsrefresh *zwischen* gerade abgeschlossener Recherche und Auswahl. Die vorhandene eigenständige Verfügbarkeitsaktualisierung bleibt unverändert.
4. **Einzelne, bereits ausgewählte Artikel** werden nur bei Bedarf direkt vor der Übernahme über die bereits vorhandene eBay-getItem-Abfrage erneut überprüft; gesperrte/geänderte Quellen werden nicht blind übernommen.
5. **Eine verbindliche öffentliche Prüfung** über Quelle, gültige Produktfamilie, Bild, Anbieter und bisher verifizierte SAFE-Kandidaten; exakt der verifizierte Endbestand bestimmt Veröffentlichung und Bereinigung. Die alten Freigaben sind kein pauschaler Gültigkeitsnachweis und werden nicht durch erfolglose Nachsuche ungerechtfertigt ersetzt.
6. **Erst nach tatsächlich abgeschlossener Veröffentlichung/Bereinigung** beginnt die Frist für den nächsten automatischen Gesamtauftrag (Korrektur aus QA63 bleibt erhalten).
7. **Plugin-Update**: Der bestehende WordPress-Initialisierungsaufruf darf keine unabhängige Voll-Pool-Verarbeitung samt Partner-Neusync starten, nur weil die technische eBay-Pluginversion geändert wurde. V345–347 sind jetzt in der vorhandenen Provider-Routing-Ausnahme enthalten. Bereits laufende ältere Pool-Cursor bleiben unverändert – kein automatischer Abbruch/Reset.

## Nachweis aus echten Quellen – und eindeutige Grenzen

- Echte vorliegende CSV 14.11.: 2.769 protokollierte Ereignisse ein und derselben UUID, 5/283 Familien, 155 ursprünglich ausgewählte Kandidaten, davon nur 2 materialisiert und 153 mit Einzelproblemen.
- Die früher als "3 Stunden 40 Minuten *Bestandsrefresh*" bezeichnete Zeit ist **korrigiert**: Die 1.692 Ereignisse zwischen 13.11. 16:48 und 20:28 UTC liegen alle in `refresh_remote`, einem Abschnitt, der sowohl die **vollständige Suche** als auch den anschließenden **globalen Refresh** enthält. Die CSV enthält kein `remote_subphase`; daraus lässt sich die genaue Dauer nur der globalen Refresh-Unterphase **nicht exakt** beweisen. Nach Erreichen des letzten Suchzählers um 18:40:49 UTC liefen noch weitere Ereignisse bis 20:28:06 UTC. Die unnötige Doppelarbeit ist im Original-PHP nachweisbar, die exakte eingesparte Zeit im Livebetrieb noch nicht.
- Originales v346-PHP in `ensure_full_pool_automation`: Versionen 345/346 waren nicht in der technischen Schutz-Ausnahmeliste. Ein Wechsel von v345 auf v346 mit abgeschlossenem Pool-Zustand konnte deshalb neue Provider-Sync- und Komplett-Pool-Aufgaben einplanen. Originalmethode im reproduzierbaren Vorher/Nachher-WP-Test belegt: 2 zusätzliche Aufgaben alt, 0 neu; alte offene Cursor bleiben erhalten.

## Zusammengefasste Prüfung aus dem *fertig gepackten* v347-Quellstand

- **7/7** originale PHP-Gesamtphasenketten mit exakt gleichem Endbestand und sicheren Fehlerausgängen vor/nach Vereinfachung (u.a. DB-Ausfall, gesperrte Ware, fehlende Treffer, SAVE-Fehler, Änderung während Nachsuche).
- **16/16** Original-PHP-REST/Laufstatus-Zustände; keine automatische neue Suche bei beschädigtem Lauf, SAFE-Bestand unverändert.
- **11/11** Zeit-/Folgelauf-Verträge mit wirklichem kanonischen Endzeitpunkt.
- **9/9** selektive Quellenfrische inkl. 153 synthetischen abgelaufenen getItem-Kandidaten (echte Methode, **nachgestellte** eBay-Antworten).
- **5/5** WordPress-Initialisierungsfälle für automatische Pool-Arbeit; bei Upgrade entstehen 0 neue Komplettjobs; alte Cursor behalten.
- **23/23** PHP-Syntaxprüfungen, **66/66** ZIP-Dateien CRC/Byte-Rückleseprüfung. Gegenüber vollständigem 6.72.346-Paket sind **nur vier Dateien verändert**, die übrigen **62/66 byteidentisch**.
- ZIP: `Affiliate_6.72.347_EBAY_KISS_GESAMTABLAUF_NUR_TEST.zip`, SHA256 `fc1cc1f76947a617ec7cb24ddd4899750f85a83eca0ab11fc88a37babb35258e`, 5.387.380 Bytes.

## Verbindliche offene Live-Abnahme

**Nicht als produktiv behoben melden.** Der lokale Test verwendet echte Plugin-PHP-Verarbeitung, aber simulierte WordPress-Datenbank, eBay-Anbieterantworten und erzwungene GitHub-Ticks. Die tatsächliche WordPress-Installation wurde nicht geändert. Ob der bisherige GitHub-Zeitgeber regelmäßig tatsächlich startet, bleibt unabhängig davon offen, insbesondere mit geschütztem/ungeklärtem PR #759. Ein zuvor manuell pausierter Lauf darf nicht heimlich neu gestartet werden.

Eine echte Gesamtabnahme muss bei der **gleichen gespeicherten UUID** beweisen: eingehende GitHub-Arbeitsaufrufe, Fortschritt und Behandlung des Pausemarkers, Materialisierung realer validierter Angebote, sichere bisherige Freigaben, öffentlich verifizierte HivePress-Anzeigen, Familienabdeckung und eindeutiger Abschluss. Nur danach kann Live-PASS behauptet werden.

### Dateien

`QA68_GESAMTABNAHME.py` führt das lokale Gesamttestbündel aus; `QA68_GESAMTABNAHME_ERGEBNIS.json` liefert Rohwerte; `test_pool_update.py` verwendet den unveränderten Original-PHP-Update-Aufruf und vergleicht fünf alte/neue Zustände. `QA67_REAL_SYNC_FULL_PHASE_CHAIN.php` und `qa67_matrix.py` sind die bereits dokumentierten vollständigen PHP-Phasen-Tests.