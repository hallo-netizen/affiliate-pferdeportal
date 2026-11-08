# Pferdeatelier: PSTE↔PSERC 0.28.55 mit echtem WordPress-Datenbanklauf – 08.11.2026

**Zwischenstand A, tatsächlich geprüft** – GitHub Actions [42477141370](https://github.com/hallo-netizen/affiliate-pferdeportal/actions/runs/42477141370) **SUCCESS**.

**Originaldaten/Schutz:** Wegwerf-WordPress 7.1.4 mit MySQL 8.0, originaler PSTE-v22-Quellcode plus bestehende QA-Funktionen; vorhandene PSTE-`createSchema()` **nur einmal auf leerer QA-DB**. Das bei lokalen Quellen wirklich aus der Original-PSERC-0.28.55-PHP-Klasse `PSERC_Plan_Snapshot_Store` erzeugte, SHA-gebundene Testdatensatzpaar ist im Büro `QA_ONLY/PSERC_02855_REAL_STORE_ENVELOPE_SYNTHETIC_ARTICLES_20261108.json` abgelegt (ein READY- und ein HELD-Artikelplatz). Das ist ein **echtes PSERC-Ausgabeformat**, aber ausdrücklich **synthetischer Artikelinhalt**. Im GitHub-WordPress-Test läuft ein einmaliger PSERC-**Testadapter**, nicht die vollständige PSERC-Plugin-Installation. Keinerlei Benutzer-WordPress-/K0-/PPM679-Produktionsdaten verwendet.

**Nachweise direkt gegen den originalen PSTE-Parkhausleser `readParkhausForMini()`:**
- Vor dem Einspielen des PSERC-Testplans: Export korrekt STOP, `PSERC_PLAN_NOT_PROVEN_COMPLETE`.
- Mit PSERC-Originalhülle und synthetischem **gespeicherten PPM679-Testplan**: `complete=true`, `wp_count=4`, `pste_count=0`, `pserc_count=2`, `runtime_count=1`, `runtime_status=PRESENT`.
- **Beide** PSERC-Plätze überstanden die echte PSTE-DB-Auslese: `READY_FOR_METADATA_HANDOFF` **und** `HELD`. Kein verstecktes Weglassen des gesperrten Themas.
- Die Original-SHA-256-Bindung der beiden PSERC-Record-Envelope-Daten wurde bei der Datenauslese geprüft. Absichtlich manipulierte PSERC-Daten und ungültiger aktiver Snapshot: **STOP** (`complete=false`).
- Wiederherstellung der unveränderten Original-Testdatensätze: Export wieder vollständig.

**NEUER ECHTER ROOT-FEHLER:** Nach **Entfernen des gespeicherten PPM679-Testplans** meldete dieselbe PHP-Funktion `WP_REAL_PPM679_MISSING_PLAN_SAFETY complete=YES status=NOT_PRESENT`. Damit könnte eine unvollständige Quelle fälschlich als `parkhaus_complete=true` an den einen SEO-Owner gehen. Die gesonderte **einmalige** Offline-Preflightkontrolle würde sie zwar bislang abweisen, aber der **zentrale Export muss selbst wahrheitsgemäß sperren**. Der bestehende Haupt-KISS-Vertrag verlangt alle gespeicherten Redaktionspläne.

**Verbindliche Korrektur:** In der **vorhandenen** PSTE-Klasse `readParkhausForMini` einmalig die Unvollständigkeit bei fehlendem oder leerem bestehenden PPM679-Runtime-Plan markieren; kein neuer Prüfer, keine Extratabelle, keine Änderung an PSERC oder K0. Danach Original-Gesamttests und den **echten WordPress-Datenbanklauf** einschließlich Manipulationsfällen wiederholen. Kein Merge oder Portal-Installationsrecht aus diesem Test.

**Offen bleibt ehrlich:** Vollständiges installiertes WordPress-PSERC-0.28.55-Paket (der GitHub-Lauf nutzt sein originales von PHP erzeugtes, übergebundenes **Testformat**), tatsächliche komplette Portal-/Plan-Kopie, echte externe einmalige SEO-Owner-Entscheidung und WordPress→K0-Durchlauf.
