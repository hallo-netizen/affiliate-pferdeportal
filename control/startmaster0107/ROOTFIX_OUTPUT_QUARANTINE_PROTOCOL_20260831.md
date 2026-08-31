# STARTMASTER0107 – Rootfix Output Quarantine / Sichtbarkeits-Gate

Stand: 2026-08-31

## Zweck
Dieses Protokoll dokumentiert Status quo, Fehlerursachen, Optimierungen und die verbindliche Absicherung dafür, dass ausschließlich Ergebnisse aus der gebundenen Produktionsstraße sichtbar bzw. produktionswirksam werden.

## Unveränderliche Grundregeln
- Keine Änderung an Fach-, Inhalts-, Qualitäts-, SEO-, Design-, Recherche-, LanguageTool-, PPM-, PSERC-, PSTE-, Dubletten-/Kannibalisierungs- oder Publish-Regeln.
- Wächter/Gates bleiben fachblind und haben keinerlei Inhalts- oder Qualitätsautorität.
- Chat hat keine freie Navigations-, Produktions-, Status-, Ergebnis- oder Ausgabeautorität.
- Alles außerhalb der gebundenen Straße ist Quarantäne/Müll und darf niemals als Produktionsresultat gelten.
- Kein Auto-Publish.

## Status quo vor Rootfix
### Produktionsstraße
- STARTMASTER0107 ist gebunden.
- 107001–107006 sind abgeschlossen.
- einzig zulässiger äußerer Step: 107007 RUN_NEW_ARTICLE_BATCH_NO_STOP.
- danach ausschließlich 107008 FINAL_NEW_ARTICLE_BATCH_REVIEW_AWAIT_USER_PUBLISH.
- free_chat_execution_authority=false.
- hard_worker=CODEX_CLOUD.

### Fehler des vergangenen Laufs
1. Worker-/Workspace-State war nicht zuverlässig frisch gegen GitHub main gebunden; dadurch konnte ein veralteter Step materialisiert werden.
2. Der offizielle Workflow blieb zwar geschützt, aber der Chat konnte außerhalb der Straße eigene Artikel/ZIP-Dateien erzeugen und sichtbar ausgeben.
3. Dadurch entstand eine nicht autorisierte Parallelproduktion ohne gültigen 107007-Receipt.
4. Diese Ausgabe konnte fälschlich als 107008-Ergebnis erscheinen, obwohl die echte Produktionsstraße nicht vollständig durchlaufen war.
5. Spätere WordPress-Verpackung transportierte diese bereits ungültigen Texte nur weiter; sie war nicht die primäre Fehlerursache.

## Optimierungsanalyse vergangener Lauf
### Startphase
- Wiederholte Infrastruktur-/Komponentensuche trotz bereits hash-identischer PASS-Belege.
- unnötige erneute Suche nach bekannten Komponenten wie LanguageTool.
- zu wenig konsequente Wiederverwendung unveränderter, bereits bestandener Nachweise.
- Worker-Frische wurde nicht als zwingende Sekunde-1-Voraussetzung behandelt.

### Optimierungen
1. Hash-identische PASS-Belege werden wiederverwendet; keine erneute Vollprüfung unveränderter Infrastruktur.
2. Bekannte gebundene Komponenten werden direkt über feste Refs/Hashes angesprochen; keine freie Discovery-Schleife.
3. Nur batch-/artikelabhängige Prüfungen laufen neu.
4. Worker-Frischeprüfung wird vor jeder Materialisierung zwingend.
5. Sichtbarkeits-Gate wird strikt an gültigen Receipt + Batch + Output-Hash gebunden.
6. Alles ohne diese Bindung bleibt Quarantäne/Müll.

## Verbindliches Sicherheitsmodell
### A. Sekunde-1-Worker-Frische
Vor Ausführung muss der Worker nachweisen:
- aktueller Repository-HEAD entspricht der gebundenen GitHub-main-Autorität,
- CURRENT_STARTMASTER, CURRENT_STATE und Step-Bundle stammen aus genau diesem Stand,
- keine lokale/stale Abweichung.
Abweichung => kein Produktionsstart.

### B. Einzige sichtbare Ausgabe
Ein Projektergebnis darf nur sichtbar/freigegeben werden, wenn gleichzeitig vorliegen:
- gültiger aktueller Step-Receipt,
- Receipt gehört zum aktuell gebundenen Step/Batch,
- vollständiger Workflow-PASS,
- exakte Output-Datei(en) sind per SHA-256 im Receipt gebunden,
- kein nachträgliches Chat-Neuverpacken/Neuschreiben.

### C. Quarantäne-Regel
Jede Datei/jeder Artikel/jedes Paket, das außerhalb des gebundenen Workers entsteht, ist automatisch UNTRUSTED_QUARANTINE und darf:
- nicht als PASS gelten,
- nicht als 107008-Ergebnis gelten,
- nicht WordPress/Redaktionsplan/Runtime belegen,
- nicht in einen Produktionsordner verschoben werden,
- nicht als Nutzer-Download mit Projektstatus ausgegeben werden.

### D. Chat-Hardlock
Der Chat darf ausschließlich:
- aktuelle Autorität lesen,
- den gebundenen Step auslösen/weiterreichen,
- gültige Worker-Receipts lesen,
- nach bestandenem Sichtbarkeits-Gate exakt die gebundenen freigegebenen Outputs referenzieren.
Der Chat darf niemals selbst einen Ersatzartikel, Ersatz-Produktionsbatch, Ersatz-Receipt oder Ersatz-Endpaket erzeugen.

## Negativtests
1. Staler Worker-HEAD -> BLOCK.
2. falscher/alter Step -> BLOCK.
3. Chat-erzeugte ZIP ohne Receipt -> QUARANTINE, niemals freigeben.
4. Output-Hash weicht vom Receipt ab -> BLOCK.
5. gültiger Receipt, aber anderer Batch -> BLOCK.
6. nachträglich neu verpackte Datei mit anderem Hash -> BLOCK.
7. fehlender vollständiger Workflow-PASS -> BLOCK.
8. Versuch eines Gate-/Watcher-Eingriffs in Fach/Inhalt/Qualität -> BLOCK.

## Positivtest
Nur wenn aktueller Worker-Stand, aktueller Step, gebundener Batch, vollständige Prüfstraße, Receipt und Output-Hashes exakt zusammenpassen, darf das Endergebnis sichtbar werden.

## Status nach Umsetzung
- Grundregeln: UNVERÄNDERT.
- Inhalts-/Qualitätslogik: UNVERÄNDERT.
- Wächter: weiter fachblind.
- Ziel: Chat-Ausgabe außerhalb der Straße technisch wertlos; nur receipt-gebundene Outputs dürfen sichtbar/produktionswirksam werden.
