# Pferdeatelier – echter WordPress-/MySQL-Test, 08.11.2026

**Isolierter GitHub-Actions-Teststand**, kein Zugriff auf `pferde-atelier.de`, keine Installation auf `oliver-beil.de`, keine Veränderung an K0, PPM679-Redaktionsplan oder Live.

## Checkpoint 1: tatsächlicher WP-Core + MySQL + PSTE-Pluginstart – PASS

- In GitHub Actions **[42474691320](https://github.com/hallo-netizen/affiliate-pferdeportal/actions/runs/42474691320)** lief ein echter MySQL 8.0-Server mit einer **frisch angelegten Datenbank** und einer echten WordPress-Core-Installation **7.1.4**.
- PSTE wurde direkt aus dem **ursprünglichen gespeicherten PSTE-0.57.144.22-ZIP** über die bereits vorhandenen **zwei QA-Patchskripte** neu gebaut. Genau diese Fassung wurde mit `wp plugin install --activate` im echten WordPress geladen.
- Tatsächliche WordPress-Meldungen: `Success: WordPress installed successfully.`, `Plugin installed successfully.`, `Plugin 'Portal SEO Topic Engine' activated.`, `WP_REAL_PSTE_BOOT_OK WordPress=7.1.4 PSTE=0.57.144.22`.
- **Wichtig:** Der GitHub-Workflow selbst endete danach mit `FAIL` beim nachgeschalteten **nicht entscheidenden** Auflisten eines `PSERC-FIX.zip`-Archivpfades. Es war **kein** WordPress- oder PSTE-Aktivierungsfehler, aber der gesamte Testlauf ist daher **nicht** als `SUCCESS` zu markieren.

**Noch nicht bewiesen:** Das echte `readParkhausForMini` mit tatsächlichen WordPress-Seiten und PSERC-Komplettbestand, der echte unveränderte PPM679-Redaktionsplan, die tatsächliche externe SEO-Entscheidung und ein echter WP→PSERC→K0-Test. Die Authentifizierungs-/MySQL-Daten im GitHub-Lauf sind nur lokale Testwerte, kein Portalzugang.

**Nächster Schritt:** Im **gleichen Wegwerf-WordPress-Testverfahren** einen echten WordPress-Beitrag und den vorhandenen PSTE-Bestand technisch auslesen; statt des nicht vorhandenen `PSERC-FIX.zip`-Dateinamens keine Partner-Version behaupten. Das Testsystem muss fehlende PSERC-Planquellen **sicher sperren**, nicht fälschlich `FREI` melden. Der reguläre GitHub-Sicherheits-Hardlock ist bereits separat **PASS**; kein neuer Prüfworker.
