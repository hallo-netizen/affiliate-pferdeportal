# Pferdeatelier – Stand 12. November 2026 (QA, nicht LIVE)

**Bereits umgesetzt:** K0-Regeln vom 10. November aktiv: 81 Artikelregeln, vorgelagerte Titel-/Suchintententscheidung nicht nochmals in K0. GitHub-Lauf https://github.com/hallo-netizen/affiliate-pferdeportal/actions/runs/43201428924 erfolgreich. PSTE .43/PSERC .68 haben die ursprünglichen drei Aufträge im lokalen Übergabetest akzeptiert; das war **kein** echter vollständiger Drei-Artikel-Lauf.

**Zusätzlich nachgewiesene systemweite Ursachen:** (1) Ein neuer PSTE-Kontextabgleich setzte beim START alle bisherigen Themenfreigaben pauschal auf PENDING/BLOCKED, bei Fehler auf BLOCKED. (2) Bei Freigaben wurde im späteren Kontextlauf die redaktionelle Entscheidung nochmals berechnet. (3) PSERC und der PSTE-Leser verwendeten den früheren Kontextfehler zusätzlich als pauschale Sperre, selbst für noch gültige, vorher freigegebene Themen. Die echten WP-Daten wurden nicht ausgelesen; Ursache des konkreten 0-READY-Zustands ist weiterhin nicht endgültig bestätigt.

**QA-Korrektur an vorhandenen Stellen:** PSTE 0.57.144.44 erhält die gespeicherte Einzelentscheidung bei der neuen Kontextprüfung, ohne alle Themen zurückzusetzen. Sie verwendet für unveränderte, nachgewiesene Entscheidungen keine zweite SEO-/Titelbewertung. Bei veränderten Themen bleiben die ursprünglichen Prüfung und die Strukturbindung erhalten. PSERC 0.28.69 und der PSTE-Leser lassen bei einem historischen Kontextfehler weiter nur die gültigen, zur aktuellen Website passenden, freigegebenen Themen durch. Keine zweite Entscheidungsinstanz, keine zusätzliche WordPress-Tabelle und kein neuer Exportweg.

**Geprüft:** PHP-Syntax PSTE 83/83, PSERC 43/43, interne PSERC-Integrität 61/61. Originale drei Titel/Quellen mit künstlicher WP-Bestandsliste: 35/35. Bestehende gemeinsame PSTE/PSERC-Simulation: 64/64 mit simulierten Artikelentwürfen, nicht mit fertig geschriebenen K0-Texten. Gegenchecks: 5.016 Themen und 8 freigegebene, fehlgeschlagener unveränderter Refresh hält 8; geänderte Struktur oder ungültige Einzel-Freigabe blockiert nur die betroffenen Einträge. Tests der PSERC- und PSTE-Lesefunktion bestanden. Ohne Live-WordPress und ohne echte Provider-Aufrufe.

**QA-Dateien (noch NICHT installieren/produktiv):**
- `PSTE-0.57.144.44-KISS-EINMALFREIGABE-QA.zip`, SHA256 `036cda6fad43722a842067f34930602d6d61e93dfc79fa46d39b30840363acfc`
- `PSERC-0.28.69-KISS-EINMALFREIGABE-QA.zip`, SHA256 `576e58b51db3f348210dc3d47a894d6551558acc0c6900505be5e11257d2e41b`
- `PFERDEATELIER_QA_BELEG_20261112.zip` enthält die nachvollziehbaren lokalen Tests.

**Offen:** Lauf mit der echten WordPress-Testseite und den gespeicherten 5.016 Datensätzen, Nachweis der drei gültigen aktuellen Quellfreigaben, danach echter K0-Writer/LanguageTool 6.8/WordPress-Import für alle drei Artikel. Bis dahin keinerlei Behauptung eines abgeschlossenen vollständigen Betriebs. Bei unverändertem Stand sollen die Artikel einmalig freigegeben, geschrieben und beim Rückimport als erledigt verbucht werden; bestandserhaltende Kontextprüfungen dürfen keine Freigaben pauschal entwerten.
