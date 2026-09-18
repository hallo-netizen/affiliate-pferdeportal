# SYSTEM 4 vs. SYSTEM 4A — HARTE GEGENPRÜFUNG

STAND: 2026-09-13

## Vergleichsbasis

System 4:
- PR #238
- Branch `hobbyroom/system4-true-single-room-v1`
- Head bei Prüfung: `77c02a9df1745a28157fcc27f65f74e9c4fb1153`
- Status: BLOCKED / isolierter Prototyp; aktueller Gesamt-E2E-Beweis noch offen.

System 4A:
- PR #255
- Branch `hobbyroom/system4a-capsule-v1-20260913`
- isolierter Gegenprototyp; keine Produktionsfreigabe.

Die feste 7er-/`Beratung`-Bindung von System 4 wird ausdrücklich als behebbarer Implementierungsfehler behandelt und **nicht** als Vorteil von 4A gewertet.

---

## 1. Inhalt / Design / Qualität

### System 4

Stark:
- nutzt bereits die vorhandenen realen Prüfer;
- PPM/LT sowie Content-/Design-Guards sind im aktuellen Weg eingebunden;
- Same-Article-Repair existiert;
- Design-Guard prüft, verändert aber nicht.

### System 4A

Darf hier **keinen eigenen Vorteil erfinden**.

Verbindliches Ziel:
- dieselben bestehenden Fach-/Design-/Qualitätsautoritäten READ-ONLY nutzen;
- keinerlei eigene Text-, Design-, PPM-, LT-, PSERC-/PSTE- oder SEO-Regel;
- keinerlei Vereinfachung der Qualitätsanforderungen.

**Urteil:** Aktuell klarer Vorteil System 4, weil die realen Prüfer dort bereits angeschlossen sind. 4A darf erst weitergewertet werden, wenn dieselben Prüfer unverändert funktionieren.

---

## 2. Freiheit von außen / Ein-Tür-ein-Wächter

### System 4 aktuell

Der Controller persistiert `state.json` im Workspace und liest ihn bei jedem CLI-Schritt erneut ein.

`verify_state()` authentifiziert nur den `immutable_core` (`contract`, Snapshot, Batch, Artikel) über einen normalen SHA-Hash. Mutable Felder wie `phase`, `checks`, `last_error`, `release_prepared` oder `released` sind nicht durch eine geheime Controller-Autorität authentifiziert. Sie werden auf Konsistenz geprüft, aber der persistierte Gesamtzustand ist kein ausschließlich vom Wächter signierter Zustand.

Das bedeutet **nicht**, dass ein erfolgreicher Bypass des gesamten aktuellen Releasewegs bereits bewiesen ist. Es bedeutet aber: Die Zustandsauthentizität selbst wird aktuell nicht exklusiv vom Controller garantiert.

### System 4A V2

- echter Workflow-State bleibt innerhalb eines laufenden Supervisors;
- außen wird kein State zur erneuten Eingabe ausgegeben;
- außen existieren nur `capsule_id`, Arbeitsinhalt und read-only Status;
- Crash-/Resume-Checkpoint ist HMAC-authentifiziert;
- geänderter Checkpoint wird blockiert.

**Urteil:** 4A hat hier einen echten strukturellen Ansatzpunkt — aber nur dann, wenn Supervisor/HMAC-Autorität für Codex/Worker tatsächlich nicht frei erreichbar oder ersetzbar ist.

Wenn Codex den Supervisor selbst starten, dessen Schlüssel frei wählen oder dessen interne Daten manipulieren kann, verschwindet dieser Vorteil vollständig.

---

## 3. Übergaben

### System 4

Der Einzelartikelkern ist inzwischen bereits deutlich besser als ältere Raum-/Handoff-Konzepte:
- Recherche → Fakten → Kontext → Draft → Fullcheck → Same-Article-Repair;
- Content-/Design-Prüfung erfolgt intern;
- der Artikel bleibt an eine kanonische Identität gebunden.

Es existieren aber weiterhin persistierte Datei-/Prozessgrenzen zwischen CLI-Aufrufen, Batch-Gate und finalem Handoff.

### System 4A

Ziel:
- logische Schritte bleiben bestehen;
- keine Übergabe des Steuerzustands zwischen Worker/Prüfer/Chat;
- Prüfer werden vom Supervisor aufgerufen und geben nur Ergebnis zurück;
- Artikelzustand bleibt beim Supervisor.

**Urteil:** möglicher Vorteil 4A, aber noch nicht vollständig bewiesen. Querschnitts-/WordPress-Ausgang fehlen noch.

---

## 4. Flexibilität / neue Beitragsarten

Beide Konzepte müssen am Ende gleich gut sein.

Verbindliches Ziel:
- `article_type` kommt autoritativ aus dem Produktionsanstoß;
- der Controller kennt keine fest codierte Liste von Beitragsarten;
- neue Beitragsart bedeutet neue/erweiterte Fachregel in der zuständigen Fachautorität, **nicht** Controller-Umbau.

**Urteil:** kein zulässiger Vorteil für 4A. Ein bereinigtes System 4 muss dasselbe leisten.

---

## 5. Automatisierung / 1–∞ Artikel

### System 4

Grundsätzlich automatisierbar; aktueller 7er-Hardcode wird als reparierbarer Fehler gewertet.

### System 4A

Der V2-Prototyp führt viele unabhängige Kapseln im selben Supervisor. Lokal wurden 1.000 Kapseln mit Mock-Prüfern ohne Zustandsvermischung vollständig durch den Architekturweg geführt.

Der reine Zustandslauf lag lokal bei rund 0,13 Sekunden. Das ist kein Produktions-/Recherche-/PPM-Geschwindigkeitsbeleg.

**Urteil:** 4A zeigt, dass die Kapselverwaltung selbst skalierbar ist. Das ist aber kein entscheidender Vorteil gegenüber einem korrekt universellen System 4.

---

## 6. Nachhaltigkeit

### möglicher Vorteil 4A

Weniger externe Zustandsobjekte und weniger Stellen, an denen ein fremder Prozess den Workflow interpretieren darf.

### echter Nachteil 4A

Ein langlebiger Supervisor bringt neue Betriebsfragen:
- Wo lebt die Supervisor-Autorität?
- Wer darf den HMAC-Schlüssel besitzen?
- Wie wird sicher neu gestartet?
- Wie werden Checkpoints gespeichert, ohne eine zweite Zustandswahrheit zu erzeugen?
- Was passiert bei Prozessabbruch mitten in Recherche/PPM?
- Wie wird verhindert, dass Codex/Chat den Supervisor ersetzt oder mit eigener Konfiguration startet?

Wenn dafür wieder mehrere Signer, Token, Räume oder Recovery-Pakete nötig werden, wiederholt 4A exakt die alte Sackgasse und muss gestoppt werden.

---

## 7. Historische Sackgassen, die 4A nicht wiederholen darf

Aus den früheren Konzepten ergeben sich klare Verbote:

1. **Textregeln allein sind keine technische Sperre.** Frühere Chat-/STARTMASTER-Regeln konnten Verhalten beschreiben, aber nicht jede freie Host-/Chat-Aktion technisch verhindern.
2. **Mehr Sicherheitsschichten können selbst zum Projekt werden.** H7/Room-/Token-/Receipt-Modelle schützten Übergaben, erzeugten aber viele neue Übergabegrenzen.
3. **Test-PASS ist nicht Live-PASS.** Lokale/Regressionsläufe haben reale Produktionsblocker mehrfach nicht vorhergesagt.
4. **Signer-/Receipt-/Package-Grenzen waren wiederholt Fehlerquellen.** Beispiele: fehlende Bindings/Receipts, falsche Übergabeform, Wiederaufnahmeprobleme.
5. **Qualität darf nicht nur einzelartikelweise geprüft werden.** Der schlechte 7er-Lauf zeigte generische Recherche/Fact-Packs und artikelübergreifende Schablonenwiederholung.
6. **Repair muss denselben Artikel reparieren.** Kein Neubau, keine neue Route, keine neue Fachwahrheit.
7. **WordPress-Ausgang ist Teil des Workflows.** Ein guter Artikel ohne exakt kompatible finale Importdatei ist kein End-to-End-PASS.

---

# Zwischenurteil

4A hat nach der aktuellen Gegenprüfung **genau einen legitimen Grund**, weiter untersucht zu werden:

> Kann ein außerhalb des Codex-Workers liegender Supervisor den kompletten Workflow-State exklusiv besitzen, während Codex nur die jeweils erlaubte Facharbeit ausführt und die bestehenden echten Prüfer nur PASS/FAIL zurückgeben?

Wenn JA, könnte 4A näher am ursprünglichen **Ein-Tür-ein-Wächter**-Ideal liegen als das dateibasierte System 4.

Wenn NEIN, gibt es keinen ausreichenden Grund für ein eigenes System 4A. Dann sollte die gefundene Zustandsauthentizitätsidee als Härtung in System 4 übernommen und 4A beendet werden.

## Nächster Beweis

Nicht weiter an Texten oder neuen Guards bauen.

Zuerst technisch beweisen:
1. Supervisor-Autorität liegt außerhalb der Worker-Freiheit;
2. Worker erhält nur den gerade erlaubten Arbeitsauftrag;
3. Worker kann Phase/PASS/Route/Publish nicht setzen;
4. bestehende reale Prüfer können vom Supervisor unverändert aufgerufen werden;
5. Resume benötigt keinen neuen Raum/Signer/Receipt-Zirkus.
