# MINI:start – Einstieg und Status (nur Mini-Titel; K0 unverändert)

**Regelquelle:** `mini-title-gate/TITELREGELN_V1.json`, die unveränderte zugrunde liegende Governance `contracts/intent-first-title-governance-v1.json`.

**Ziel:** Ein Titelworker → ein unabhängiger GitHub-Prüfer → Reparatur bei Fehlern → eine bestätigte Übergabe. **Keine KI-API, keine zweite Sprachprüfung beim WordPress-Import.**

## Aktuell geprüft
GitHub Actions im privaten `hallo-netizen/mini-titelpruefer`: negativer Echtlauf 42196709788 blockiert, positiver Echtlauf 42196918970 erfolgreich. LanguageTool 6.8. Der GitHub-Lauf erstellt eine **unsignierte** Freigabedatei. WordPress PSTE-Test 0.57.144.11 nimmt nur **signierte** Freigaben an. **Die Verbindung ist noch nicht kompatibel.**

## Verbindliche Grenze
Das private Repository bleibt ohne ChatGPT-Zugriff. K0 ist ausdrücklich tabu. Ohne nachweisbare Herkunft darf WordPress keine selbst deklarierte Freigabe akzeptieren. Ein fehlender Nachweis ist ein echter Blocker; nicht mit einem einfachen `status:PASS` umgehen. Ein Sprachtool allein kann natürliche Formulierungen und Suchabsichten nicht mit 100 % Sicherheit beurteilen.

## Weiterarbeit
Vor der nächsten WordPress-Installation beide Enden **gemeinsam** gegen eine einzige Herkunftsbindung testen. Erst danach ein kumuliertes, überprüftes Update. **Keine weiteren Einzelinstallationen und keine wiederholten Freigabe-/Sperrschritte für den Benutzer.**

Prüfnachweis: `mini-title-gate/E2E_GAP_AND_KISS_STATUS_20261106.md`.

Das ist Navigation/QA und **keine zweite Current-/NEXT-ACTION-Autorität**.
