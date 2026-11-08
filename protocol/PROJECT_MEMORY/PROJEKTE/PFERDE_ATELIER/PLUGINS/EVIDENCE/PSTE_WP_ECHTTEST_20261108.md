# Pferdeatelier – echter WordPress-/MySQL-Test, 08.11.2026

**Isolierter GitHub-Actions-Teststand**, kein Zugriff auf `pferde-atelier.de`, keine Installation auf `oliver-beil.de`, keine Veränderung an K0, PPM679-Redaktionsplan oder Live.

## Checkpoint 1: tatsächlicher WP-Core + MySQL + PSTE-Pluginstart – PASS

- In GitHub Actions **[42474691320](https://github.com/hallo-netizen/affiliate-pferdeportal/actions/runs/42474691320)** lief ein echter MySQL 8.0-Server mit einer **frisch angelegten Datenbank** und einer echten WordPress-Core-Installation **7.1.4**.
- PSTE wurde direkt aus dem **ursprünglichen gespeicherten PSTE-0.57.144.22-ZIP** über die bereits vorhandenen **zwei QA-Patchskripte** neu gebaut. Genau diese Fassung wurde mit `wp plugin install --activate` im echten WordPress geladen.
- Tatsächliche WordPress-Meldungen: `Success: WordPress installed successfully.`, `Plugin installed successfully.`, `Plugin 'Portal SEO Topic Engine' activated.`, `WP_REAL_PSTE_BOOT_OK WordPress=7.1.4 PSTE=0.57.144.22`.
- **Wichtig:** Der GitHub-Workflow selbst endete danach mit `FAIL` beim nachgeschalteten **nicht entscheidenden** Auflisten eines `PSERC-FIX.zip`-Archivpfades. Es war **kein** WordPress- oder PSTE-Aktivierungsfehler, aber der gesamte Testlauf ist daher **nicht** als `SUCCESS` zu markieren.

**Noch nicht bewiesen:** Das echte `readParkhausForMini` mit tatsächlichen WordPress-Seiten und PSERC-Komplettbestand, der echte unveränderte PPM679-Redaktionsplan, die tatsächliche externe SEO-Entscheidung und ein echter WP→PSERC→K0-Test. Die Authentifizierungs-/MySQL-Daten im GitHub-Lauf sind nur lokale Testwerte, kein Portalzugang.

**Nächster Schritt:** Im **gleichen Wegwerf-WordPress-Testverfahren** einen echten WordPress-Beitrag und den vorhandenen PSTE-Bestand technisch auslesen; statt des nicht vorhandenen `PSERC-FIX.zip`-Dateinamens keine Partner-Version behaupten. Das Testsystem muss fehlende PSERC-Planquellen **sicher sperren**, nicht fälschlich `FREI` melden. Der reguläre GitHub-Sicherheits-Hardlock ist bereits separat **PASS**; kein neuer Prüfworker.


## Checkpoint 2: echter WP-Quellenleser – erstmals überprüft, ERSTER REPRODUZIERBARER FEHLER

GitHub-Actions-Gesamtlauf **[42474876008](https://github.com/hallo-netizen/affiliate-pferdeportal/actions/runs/42474876008) SUCCESS** in Wegwerf-WordPress **7.1.4** mit **MySQL 8.0**; Original-PSTE-0.57.144.22 mit den vorhandenen QA-Änderungen erfolgreich installiert und aktiviert. Ein eigener echter veröffentlichter WordPress-Beitrag wurde erzeugt.

**Direkt im echten WordPress ausgeführtes `PSTE_Mini_Workflow::readParkhausForMini()`:**

```text
WP_REAL_PARKHAUS complete=NO reason=PSTE_PLAN_COUNT_FAILED wp_count=4 pste_count=-1
```

Vier echte WordPress-Inhalte wurden vom bestehenden WP/MySQL-Quellenleser korrekt aufgenommen. Danach scheiterte die erste PSTE-Plan-Zählabfrage **vor** dem PSERC-Bestand. `complete=NO` ist **korrekt gesperrt**, es gibt keine fälschliche SEO-FREI-Entscheidung. Die tatsächliche SQL-Ursache ist noch **nicht** nachgewiesen; der nächste Schritt liest die verwendete Tabelle, die tatsächlichen Tabellen und den echten SQL-Fehler im selben isolierten WP-Test, **bevor** ein Code-Fix erwogen wird. Kein zusätzlicher Runtime-Checker, kein SEO-Durchlauf pro Keyword.

**Wichtig:** Das ist ein **realer WordPress-Datenbankbefund**, deutlich aussagekräftiger als die früheren reinen Mocks. Er beweist noch keine mögliche Ursache oder einen WP→PSERC→K0-Real-PASS. Live/K0 und gespeicherter Redaktionsplan wurden nicht berührt.


## Checkpoint 3: tatsächliche SQL-Ursache exakt festgestellt

GitHub Actions **[42475021844](https://github.com/hallo-netizen/affiliate-pferdeportal/actions/runs/42475021844) SUCCESS**; im isolierten echten WordPress/MySQL dieselbe PSTE-v22-QA-Fassung gestartet, vier echte WP-Inhalte gelesen. Direkte WordPress-DB-Diagnose (keine Vermutung):

```text
WP_REAL_PLAN_TABLE=wp_pste_topic_pool
WP_REAL_PSTE_TABLES=[]
WP_REAL_PLAN_COUNT=null
ERROR="Table 'pste_genuine_wp.wp_pste_topic_pool' doesn't exist"
```

**Root Cause des konkreten Testlaufabbruchs:** Eine **brandneue** WordPress-Wegwerfinstallation hat zwar das PSTE-Plugin aktiviert, aber die **bestehende erwartete** PSTE-Plantabelle nicht eingerichtet. Das ist ein **Setup-/Initialisierungsproblem im frischen Testsystem**, kein Hinweis auf falsche SEO-Auslegung. `readParkhausForMini()` reagiert korrekt mit **`complete=NO`** und darf deshalb keine externe SEO-FREI-Freigabe erzeugen.

**Nächster Schritt:** Die bereits vorhandenen PSTE-Installations-/Schemafunktionen aus dem unveränderten Original-Plugin identifizieren und im Testsystem genau einmal ausführen. Keine neue Produktiv-Tabelle konzipieren, kein ad-hoc-Datenbank-Reparatursystem, keine veränderten K0-Daten, keine semantische Zweitprüfung. Danach den echten Parkhausleser erneut prüfen.


## Checkpoint 4: Ursache nach Lesen des ORIGINALEN Plugin-Codes – keine neue Plugin-Architektur

In echtem WP 7.1.4 direkt über PHP-Reflection `PSTE_Plugin::activate()`, `PSTE_Plugin::maybeMigrate()`, `PSTE_Repository::createSchema()` gelesen (GitHub Actions **[42475393088](https://github.com/hallo-netizen/affiliate-pferdeportal/actions/runs/42475393088)**).

**Belegte Ursache:** `PSTE_Plugin::activate()` ist **absichtlich passiv**: Der Originalkommentar lautet `Dormant activation: no cleanup, migration, scheduling, portal scan or retry.` Bei fehlender Schema-Version wird ausdrücklich `PENDING/AWAITING_MANUAL_MIGRATION` gespeichert. `PSTE_Plugin::maybeMigrate()` ist ein **absichtlicher No-op**, weil die vorhandene sichere Migration separat läuft. Darum wird bei einer leeren Wegwerf-WordPress-Installation trotz erfolgreicher Pluginaktivierung noch keine PSTE-Tabelle angelegt. **Kein fälschlich diagnostizierter Exportcode-Bug!**

Die ursprüngliche vorhandene Routine `PSTE_Repository::createSchema()` legt die **bereits im Plugin definierten** PSTE-Tabellen an, darunter `wp_pste_topic_pool` mittels WordPress `dbDelta`. Die echten Portal-Sicherheits-/Migrationsregeln werden nicht durch eine neue Auto-Installation verändert.

**Nächster isolierter Test:** In der **frisch angelegten und nachweislich leeren** MySQL-Testdatenbank die **bestehende** `PSTE_Repository::createSchema()` genau einmal ausführen. **Nur für den disposable CI-Test, niemals als Empfehlung für Produktions-/Staging-Daten mit vorhandenem Bestand**. Dann `readParkhausForMini()` erneut; der WP+PSTE-Teil muss vollständig gelesen werden, der mangels PSERC immer noch fehlende aktive PSERC-Plan muss **sicher blockieren**. `42475393088` war ein reiner Quell-Inspektionslauf und endete aufgrund einer falschen `migrationBootStatus()`-Test-Hilfsabfrage, nicht aufgrund eines PSTE-Produktfehlers.
