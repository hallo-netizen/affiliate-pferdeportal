# QA74 – Pferdeatelier eBay: KISS-Gesamtkette, überprüfte Originalfunktionen und echter GitHub-Lauf

**14.11.2026 – Keine Live-Abnahme, keine Installationsfreigabe.** Grundlage: vollständiges QA71-Originalplugin 6.72.350, QA72- und QA73-Quellpatches sowie 2.769 originale Laufereignisse und 278 reale Fehlfamilien. Keine neuen Worker, keine Tabelle, kein Core- oder Frontend-Umbau.

## 1. Zwei belegte Abschlussfehler korrigiert (ein bestehender Besitzer)

- **QA73-Fehlannahme nachgewiesen:** Sein Prüfungshilfsprogramm hatte `ebay_public_checkpoint_is_safe` und `ebay_public_checkpoint_business_ids` vereinfacht. Im **unveränderten echten PHP** gilt ein Kandidat *vor* seiner Speicherung noch nicht als `safe`; die alte QA73-Wiederholsperre vergleicht deshalb eine leere Kandidatenliste mit dem bestehenden sicheren Bestand. Im originalen PHP-Vorher-Nachher-Test werden nach einem Phasen-Speicherfehler **3 statt 2** öffentliche Checkpoint-Schreibvorgänge ausgelöst. QA74 normalisiert ausschließlich die bereits fachlich bestätigten Kandidaten-IDs und vergleicht sie mit dem einen bestehenden sicheren Checkpoint: **2 statt 3**, ohne zweite Fachauswahl.
- **Direkte Original-Helfertests:** Gleiches Laufkennzeichen + gleicher Kandidatenbestand: Original **1 unnötige Schreibung**, QA74 **0**. Tatsächlich neuer Bestand, anderes Laufkennzeichen oder andere Quelle: weiterhin je **1** zulässige Schreibung. Der vorherige sichere 578er-Bestand wird beim Wiederverwenden nicht gelöscht.
- **Zweiter falscher Erfolg:** Bei unbestätigter Recherche und einem verlorenen Speicherstand für den Aufschub endete der Original-PHP-Lauf trotzdem als `completed`. Mit einer einzelnen nachgestellten WordPress-Speicherstörung ergibt QA74 jetzt `failed / unverified_search_deferred_state_save_failed`, ohne den öffentlichen 580er-Bestand zu verändern. In demselben bestehenden `ebay_run_tick_public_verify`-Pfad, **keine neue Prüfung**, sondern notwendige Beachtung des Ergebnisses der einen vorhandenen Speicherung.
- **QA73-Schutz bleibt erhalten:** Gezielter letzter Bereinigungs-Speicherfehler gibt `failed / checkpoint_business_cleanup_state_save_failed` und keinen falschen Abschluss. Kein Verlust des sicheren Altbestands.

## 2. Verifizierte Gesamtkette

- Bisherige QA73-Gesamtkette mit **5.627 lokalen Prüfungen**, einschließlich **sieben durchgängiger Original-PHP-Abläufe mit simulierten eBay-/WordPress-Daten**, der 2.769 **echten** historischen Protokollereignisse, 278 echten Fehlfamilien, 50 weiterer PHP-Fälle, neun gezielter Frischefälle und 23 PHP-Syntaxprüfungen: **0 lokale Fehler**.
- Neue **102** gezielte Prüfungen mit Original-PHP-Sicherheits- und Mitgliedschaftshelfern, acht Kontrollszenarien, veränderten echten Speicherantworten und Schlussbereinigung: **0 lokale Fehler**. Kein Anspruch auf 5.729 echte Einzelproduktergebnisse.
- Gegenüber QA73 **nur** `includes/trait-ppar-ebay-run.php` verändert; das QA72-Fachentscheidungsverhalten bleibt unangetastet. Kein neues Plugin zum Installieren.

## 3. Frische GitHub-Laufprotokolle – tatsächliche Betriebsursache

Aus dem verbundenen Original-GitHub-Repository `hallo-netizen/affiliate-pferdeportal` und den tatsächlichen Job-Logs:

- Geplanter Lauf **43612828861**, erstellt 14.11. **15:56:10 UTC** (16:56 MEZ): Job **132501390005** führt genau **einen** POST-Tick aus, erhält **`status=idle`** und beendet den Runner **erfolgreich**; keine weitere Verarbeitung. Das ist **kein Beweis** für einen abgeschlossenen WordPress-eBay-Run.
- Lauf **43580485610**, erstellt **09:25:28 UTC**, aber tatsächlich erst **12:24:30 UTC** ausgeführt (rund **2 h 59 min** nach Auslösung), Job **132446527797**: ebenfalls `idle`, sofortiger Exit nach dem ersten Tick. Die Wartezeit ist anhand der tatsächlichen GitHub-Zeitstempel nachgewiesen, ihre Ursache nicht.
- Lauf **43547142784**, **02:35 UTC**, Job **132300989202**: alle **30** Ticks melden `advanced`; danach `successor heartbeat runner dispatched`. Ein echter Laufabschluss folgt daraus nicht.
- Lauf **43518738389**, 13.11. **22:22 UTC**, Job **132207303870**: fünf aufeinanderfolgende **45-Sekunden-HTTP-Timeouts**; GitHub beendet nachvollziehbar mit Fehler.

**Geschützter Zeitgeber:** In der ursprünglichen Main-Datei stehen weiter `*/15` und Selbstverkettung. Der bestehende Entwurf PR **#759** wurde auf seinem isolierten Kopfzweig auf `*/5`, **4 Ticks / 4 Fehler** und **keine automatische Selbstverkettung** vereinheitlicht; Workflow-Strukturprüfung im PR-Lauf **43617527215** bestanden. Allerdings meldet sein echter Immutable-Hardlock-Lauf **43617525262** weiterhin `IMMUTABLE_SECURITY_PATH_CHANGE_BLOCKED`. **PR nicht gemergt, Main nicht verändert**, keine Umgehung, keine Liveauswirkung.

## 4. Grenzen / nächster Schritt

Das Originalprotokoll endet bei `running / gapfill_discovery / 5 von 283 Familien`. Es enthält weder historische individuelle eBay-Antworten noch den echten öffentlichen Endbestand oder den Abschluss der Bereinigung. Die lokalen Modelle können dies nicht ersetzen. **Gesamtzielvertrag: NICHT ABGENOMMEN.** Für einen tatsächlichen, automatischen Endlauf müssen der eine GitHub-Zeitgeber autorisiert freigegeben und ein unverändert fortgesetzter realer WordPress-Lauf bis zum gesicherten Endzustand beobachtet werden. QA74 selbst ist ausschließlich ein dokumentierter Quell-/Prüfstand, kein installierbares Release.