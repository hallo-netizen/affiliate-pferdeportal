# Pferdeatelier – ein Weg bis zum ersten echten neuen Artikel
Stand: 11.11.2026. Arbeits- und Abnahmeplan, **keine** Behauptung einer fertigen Reparatur. Gilt nur für den isolierten QA-Zweig PR #682. K0 und Live bleiben unverändert.

## Ziel / Erfolg
Ein **frisch recherchiertes** Keyword aus realen Daten → genau eine gültige SEO-/Titel-/Kategorie-Entscheidung durch PSTE → PSERC-Redaktionsplan mit mindestens einem belegten READY → identitäts- und suchintentgebundener Original-Export → **echter K0-Writer mit den geltenden Qualitätsprüfungen** → fertige .txt- und WordPress-Importdatei → überprüfter WordPress-Entwurf in TEST. Kein künstlicher Artikel, kein nur simulierter PASS. Danach drei weitere aufeinanderfolgende reale Einzelaufträge ohne erneute Gesamtrecherche; erst dann Live-Freigabe.

## Belegter Iststand
- GitHub PR #682, letzter Eintrag 11.11.2026 15:11 UTC: PSTE .40 / PSERC .67 sind der dokumentierte WordPress-Teststand. PSTE .41 ist ein lokaler, nicht in WordPress abgenommener QA-Kandidat; 20 lokale Simulationen bestanden, nicht die reale Produktionskette.
- WordPress-Flugschreiber dokumentiert den alten 5.013er Wiederanlauf, veränderte/gesperrte Themen und anschließend null planbare/READY-Themen. Frühere drei Original-READY-Metadaten sind separat gesichert, aber weder aktuelle WP-Freigabe noch geschriebene Artikel.
- Nachweis im .41-Diff: drei historische Vollbestands-Audit-Pflichten in Automatik, READY-Status und Export entfernt; abgeschlossene/abgebrochene Altqueue blockiert neuen Einzelworker nicht mehr; **laufende/unklare Altqueue bleibt geschützt**. Vollständiger aktueller WP-/Datenbanktest offen.
- Die .41-Simulation prüft PSERC-Quellenbindung nur mit Mock-WordPress; der PSERC-Frischeabdruck erfasst nicht jede in-place-Änderung einer alten Themenzeile. Historischer READY-Status darf daher nicht ohne echten Prüfnachweis freigegeben werden.

## Festgelegter Ablauf: Keine weiteren parallelen Reparaturrunden

### A – Bestehenden QA-Stand einfrieren und echte Schnittstellen prüfen
1. Quellstand .40 → .41 einmalig gegen Original-ZIPs/Diff/Signaturen prüfen; dokumentieren, was tatsächlich im TEST installiert ist. **Kein** Upgrade auf LIVE, keine Datenbankänderung, kein Restore, kein Reset.
2. Quellen- und Zustandsrollen festlegen: PSTE entscheidet Recherche/Fachfreigabe genau einmal; PSERC prüft Planplätze, aktuelle Quellen und exportiert die unveränderten fünf Felder; K0 schreibt und kontrolliert Texte. Kein zusätzlicher SEO-Entscheider in PSERC/K0. Der originale Suchintent-Nachweis muss auf die fünf Felder bezogen mitübergeben werden, ohne ein sechstes Feld zu erfinden.
3. Vor dem Test die nachgewiesenen Schutzfälle an den echten bestehenden Funktionen prüfen: 0 READY darf kein aktiver Plan werden; beschädigtes/veraltetes signiertes Profil darf nicht freigegeben werden; unklare laufende Altqueue darf nicht heimlich gestartet oder umgangen werden.

### B – Ein echter durchgängiger WordPress-TEST, kein 5.013er Replay
4. **Einmalig** PSTE .41 nur in der vorhandenen getrennten WP-Testinstallation installieren, PSERC .67 unangetastet lassen. Eine frische, noch nicht als neues manuelles Thema missbrauchte Keyword-Anfrage über den bestehenden Standardweg ausführen.
5. Beobachtbar nachweisen: echte DataForSEO-Antwort, gespeichertes planbares Einzelthema, **null** neue Vollbestands-Neubewertungen und **null** unnötige 5k-Scans, gültige PSTE-Herkunft, PSERC READY>0, gültiger aktueller Plan und echter JSON-Export. Nicht den gesicherten Drei-Artikel-Export fälschlich als frischen Erfolg zählen.
6. **Dasselbe** Einzelthema mit echter, unverändert gebundener SEO-Recherche an den vorhandenen K0-QA-Eingang übergeben. Einen **neuen** vollständigen Artikel mit echten Sprach-/Fakten-/Linkprüfungen produzieren, TXT und WP-Datei prüfen und als WP-Testentwurf einlesen und zurücklesen.
7. Negativtest **im selben Testpaket**, keine neuen Plugins: alter COMPLETE/CANCELLED-Job blockiert nicht; RUNNING/PAUSED_ERROR/OUTCOME_UNKNOWN wird nicht umgangen; 0 READY überschreibt nichts; veraltete bzw. veränderte Fachfreigabe wird gesperrt; mehrfacher Klick/Unterbrechung produziert keine Doppelarbeit; ein einzelner ungültiger Kandidat legt nicht andere neue Einzelaufträge lahm. Keine automatische Neusignatur alter Daten.

### C – Freigabe erst nach echter Abnahme
8. Ein echter vollständig importierbarer Artikel einschließlich gültigem SEO-Nachweis = erstes Ziel. Anschließend drei frische Artikel nacheinander, unveränderte Regeln, reproduzierbare Quellen; erst danach eine einzelne, identisch getestete Pluginfreigabe für LIVE. Die bislang alten drei Artikel bleiben separat geschützt; keine Schein-Wiederherstellung per WP-Dummy-Import.
9. Bei einem Fehlschlag **genau eine** gespeicherte konkrete Fehlstelle verwenden und den ursächlichen bestehenden Quellweg korrigieren; denselben E2E-Test vollständig wiederholen. Keine neuen Worker, Tabellen, zusätzliche Abnahmeregeln, Patch-Kaskaden oder erneuter 5k-Audit.

## Verantwortung / nächster Schritt
**Assistent:** Originalquellen und .41-Paket/Änderungsumfang auf Abweichung prüfen, ein einziges vollständiges TEST-Szenario inklusive Negativfällen vorbereiten und Ergebnis mit echter Quelle dokumentieren. **Nutzer:** Erst wenn diese Vorprüfung abgeschlossen ist, höchstens die bestehende **TEST**-WP-Installation für genau einen gebündelten Durchlauf bedienen. Keine Dateianforderungen/Installation auf Verdacht.

**Aktueller Status:** Konzept dokumentiert; WP-E2E, echter K0-Neuartikel und echte WordPress-Importabnahme **offen**. Kein Live-Freigabevermerk.

### GitHub-Belege
- [PR #682](https://github.com/hallo-netizen/affiliate-pferdeportal/pull/682)
- [Checkpoint B, 11.11.](20261111_KISS_CHECKPOINT_B_AUTOMATIK_NEUER_EINZELWORKER_EXPORT_QA.md)
- [Hauptursachen und Verantwortlichkeiten](20261111_KISS_GRUNDURSACHE_WORKER_AGENT_KONZEPTPRUEFUNG.md)
- [Drei alte Original-READY sind nur Metadaten](PSTE_PSERC_3_READY_LETZTER_GUELTIGER_ORIGINALSTAND_20261111.md)
