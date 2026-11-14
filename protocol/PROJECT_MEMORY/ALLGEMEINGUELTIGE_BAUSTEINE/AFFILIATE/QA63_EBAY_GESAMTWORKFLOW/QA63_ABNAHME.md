# eBay Pferdeatelier: QA63 gesamter Ablauf – geprüfte TIS/KISS-Korrektur
**Stand:** 14.11.2026 | **Plugin:** 6.72.346, Testkandidat – NICHT live freigegeben.

## 1. Ursache – nicht nur ein Einzelfehler
Der echte eBay-Protokollexport vom 14.11. liefert 2.769 Ereignisse, zuletzt 5/283 öffentlich nachgewiesene Familien, 153 von 155 gewählten Produkten nicht materialisiert, u.a. wegen `business_selected_stale_during_apply`. Die alte Suche schloss teils >6h vor der eigentlichen Materialisierung ab. Diesen Quelle-Frische-Übergang hatte das vorhandene QA58/QA62-System bereits mit selektiver `getItem`-Neubestätigung korrigiert (noch nicht real live nachgewiesen).

Ein ZWEITER nachweisbarer Gesamtverarbeitungsfehler blieb im vorhandenen 6.72.345-Code: Der automatische nächste Vollsuchlauf wird nach `settings.last_sync.finished_at` begonnen, der bei Abschluss der **untergeordneten eBay-Suche** gespeichert wird, NICHT bei Abschluss des kanonischen Gesamtlaufs inklusive Materialisierung, Quellenprüfung, öffentlichen Checkpoint und Bereinigung. Dauert der restliche Lauf länger als drei Stunden, gilt bei seinem tatsächlichen Ende sofort ein neuer Vollsuchlauf als fällig. Die Einzelphase wird damit irrtümlich als Abschluss des Gesamtauftrags behandelt.

## 2. Eine zentrale Lösung, kein Neubau
- Der bestehende kanonische Gesamtlauf bleibt einziger Entscheider für `running / paused / completed / failed`, Cursor, sichere Produktfreigaben und öffentlichen Abschluss.
- Der bestehende GitHub-Taktgeber bleibt unverändert. Das neue Plugin fügt weder zweiten Zeitgeber, neue Datenbank noch Produkt-Auswahl-/Publishing-Entscheidung hinzu.
- **Nur der vorhandene `ebay_external_tick_due_operation()`-Abschnitt** nutzt für einen tatsächlich `completed`/`completed` gespeicherten kanonischen Gesamtsuchlauf dessen `finished_at` als **maßgeblichen** Anfang der nächsten vorhandenen 3-Stunden-Frist. Die alte untergeordnete `last_sync`-Zeit gilt lediglich für Altstände ohne vollständigen kanonischen Abschluss.
- Für echte `refresh`-Gesamtläufe gilt dieselbe Regel für den unveränderten 1-Stunden-Refresh-Zyklus. Gesonderte `gaps`-Läufe ersetzen keine vollständige `sync`-Prüfung.
- Bereits ausgewählte Produkte mit abgelaufener Frische werden durch die bestehende 6.72.345-Regel gezielt erneut bei eBay validiert; ansonsten keine neue Suche/Rangordnung. Der geprüfte öffentliche Checkpoint ist weiterhin Grundlage für das Bereinigen. Nicht nachweislich gültige Angebote werden nicht freigegeben.
- Kein künstlicher Stopp oder erneuter Suchlauf nur wegen 0/283-Anzeige. Bestehende Begrenzungen für einzelne Such-/Auswahlphasen und monotone Lückenerweiterung bleiben erhalten.

## 3. Simulierte gesamte Kette – Original-PHP, echte Phasen

**Originale kanonische PHP-Methoden** ausgeführt: Bestand → eBay-Remote-Phase → Vorbereitung → BUSINESS-Auswahl/Materialisierung → öffentliche Abdeckung → gezielte Lückensuche → Auswahl → öffentliche Quellenprüfung → atomarer Checkpoint → originale BUSINESS-Bereinigung → `completed` beziehungsweise eindeutiger Fehler. Die originale Cleanup-Methode ist byteidentisch im Harness eingebettet.

| Test mit simulierten Quellen/WordPress | Ergebnis | Alte SAFE-Produkte unbegründet verloren |
| --- | --- | ---: |
| Normal, 2 neue passende Produkte | abgeschlossen, 580 SAFE, 259/283 Modellfamilien | 0 |
| 1 altes wirklich gesperrt | abgeschlossen, 579 SAFE | 0 (1 belegbar ungültiges entfernt) |
| 1 neues Angebot gesperrt | abgeschlossen, 579 SAFE | 0 |
| Datenbank-Leseausfall | eindeutiger Fehler, alte Freigabe unverändert | 0 |
| Produkt ändert Status während der Nachsuche | abgeschlossen, 579 SAFE | 0 (1 belegbar ungültiges entfernt) |
| Kein neuer Treffer | abgeschlossen, 578 SAFE | 0 |
| Speicherfehler beim Checkpoint | eindeutiger Fehler, kein unbestätigter neuer Gesamtstand | 0 |

**Weitere Original-PHP-Prüfungen:** 153 ursprünglich ausgewählte, aber in der Wartezeit veraltete Modellangebote gezielt je einmal durch bestehende `getItem`-Abfrage bestätigt: 153 erneut bestätigt und 153 materialisiert (simulierte Anbieterantwort). Andere Grenzfälle inklusive abgelaufen/beendet/veränderte Produktidentität/Transportfehler: 9/9. Bestehende echte REST-Laufstatus-Funktion mit WordPress-Testzuständen: 16 Fälle; keine neue Suche bei widersprüchlichem Zustand. **Neue reale fällige-Zeitpunkt-Funktion:** Vorher 5/11, jetzt 11/11 einschließlich „nach langem Lauf NICHT sofort Vollsuche neu starten“ und „nach 3h ab tatsächlichem Gesamtlauf-Ende fällig“.

**Testgesamtstand:** 130/130 Assertions PASS, davon 7 vollständige Original-PHP-Phasenketten; 23/23 PHP-Dateien syntaktisch einwandfrei. ZIP: 66/66 Einträge, CRC korrekt, gegenüber 6.72.345 exakt 2 geänderte Dateien (Laufzeit-Trait + Plugin-Versionskopf), sonst 64 unverändert. SHA256 des vollständigen ZIPs `2528ebfa053172cebaa0140200ce4681d0582257a91844a24f1044d6e30d7404`.

## 4. Unveränderliche Grenze und echte Freigabe
Diese Simulation führt die **echten Phasenfunktionen des Pakets** aus, ersetzt jedoch WordPress-Datenbank, externe eBay-Netzwerkantworten und die untergeordneten Recherche-/Auswahl-Dienste durch kontrollierte Testantworten. Sie ist deshalb **kein echter Live-Gesamtdurchlauf** und kann die tatsächliche Zahl der aktuell gültigen 578 alten Freigaben oder die Erreichbarkeit aller 283 Familien nicht beweisen. Die jüngste echte Anzeige stand weiterhin bei 5/283; sie wurde nicht durch diesen Test verändert.

Das Plugin kann einen bereits gestoppten GitHub-Zeitgeber nicht nachträglich allein wecken. Bestehendes GitHub-Schedule läuft auf eigener Planung weiter. Keine Änderungen auf Main/GitHub-Workflow, kein Live-Reset, keine neue Katalogsuche, keine bestehende Seite verändert.

**Notwendige kontrollierte Endabnahme:** Live-Installation nur mit gesicherter vorhandener WordPress-Version/Backup und überprüfbarer alter Lauf-UUID, einmaliger vollständiger echter Lauf mit anschließend nachweisbaren öffentlichen Produktkacheln, realen eBay-Produkten, Abschlusszeit, Abdeckung und Erhaltung aller weiterhin gültigen SAFE-Produkte. Erst das wäre eine echte Freigabe. Vorher QA-Plugin nicht als „repariert im Livebetrieb“ ausgeben.