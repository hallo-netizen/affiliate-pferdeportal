# NOTFALL-TRESOR – REALTEST V4

STAND: 2026-09-07
STATUS: VORBEREITET / REALE AUSFÜHRUNG OFFEN

## Ziel

Den vollständigen Ein-Datei-Tresor testen, ohne den produktiven Campus oder das produktive WordPress zu gefährden.

## Testphasen

### Phase A – Bereitschaft
`TEST_VORBEREITUNG_PRUEFEN.command`

PASS:
`TRESOR_TEST_READY`

### Phase B – sichere lokale Gesamtprüfung
`TEST_ALLES.command`

PASS:
`TRESOR_LOCAL_ONEFILE_TEST_PASS`

### Phase C – echter GitHub-Neuaufbau
`TEST_GITHUB_NEUAUFBAU.command`

Nur separates privates Test-Repository.

PASS:
`GITHUB_RESTORE_TEST_PASS`

### Phase D – WordPress-Neuaufbau
Aus exakt derselben Recovery-Kapsel in eine leere isolierte WordPress-/Serverumgebung.

Pflicht:
- Dateien wiederherstellen;
- Datenbank importieren;
- Konfiguration/Rechte prüfen;
- Website technisch starten;
- notwendige Plugins/Themes/Uploads vorhanden;
- keine weitere Projektdatei als Quelle.

### Phase E – Endabnahme

Nur wenn A–D real PASS sind und Recovery/Secrets vollständig funktionieren:

`TRESOR_PASS`

Andernfalls:
`TRESOR_FAIL:<ERSTER_FEHLER>`

## Sicherheitsgrenze

Der produktive Campus, das produktive Repository und die produktive WordPress-Seite werden für den Test nicht gelöscht.

Die Totalverlust-Situation wird ausschließlich mit leeren isolierten Testzielen nachgestellt.
