# QA80 – Pferdeatelier eBay: echte Stauursache und gebündelte lokale Ein-Arbeiter-Korrektur

Stand 16.11.2026. **Nur lokale Tests, NICHT INSTALLIEREN.** QA69-Zielvertrag bleibt unverändert.

## 1. HARTE URSACHE aus den originalen Nutzerdateien

Aus `pferdeatelier-ebay-lauf-574cb003b132(2).csv` und `pferdeatelier-ebay-lauf-bc17b83a168e.csv` sind **24 echte Ereignisse `availability_saved`** extrahiert. Die 23 Ereignisse des vorangehenden Laufs zeigen:
- **Jedes** gespeichert geprüfte Quellenpaket erhöht den Kumulativzähler um **exakt 5**.
- **21 von 22 Zeitabständen**: **7.186–7.219 Sekunden**, Median **7.199 Sekunden**, also beinahe exakt zwei Stunden. **Eine** Ausnahme 14 Sekunden.
- Alle 24 gespeicherten Zustände `running=1`, letzter bekannter kumulativer Zähler **403**, Cursor **10664** am 15.11. 16:22 MEZ. **Kein bestätigter Abschluss** des laufenden Frische-Gesamtpasses in den exportierten Ereignissen.
- Echte Rate im normalen Muster: **5 je 2h = 2,5/h**. Eine Modellannahme `634 gleichzeitig fällige Produktquellen` würde **253,6h = 10,6 Tage** benötigen; die 634 stammen jedoch aus einer Freigabezählung, **nicht** aus einem gemessenen aktuellen Produkt-/Fristbestand.
- Original-PHP: `ebay_public_availability_tick` bearbeitet `LIMIT 5`, `ebay_public_availability_continue` versucht eine WordPress-Fortsetzung **nach 90 Sekunden** zu planen, doch die protokollierten Ereignisse zeigen überwiegend nur den Zwei-Stunden-Rhythmus. **Warum** WP-Cron die Fortsetzung nicht regelmäßig ausgeführt hat, ist ohne echte WP-Cron-Daten nicht belegt.

Diese Ursache erklärt den extrem langsamen Aktualitätsdurchlauf; sie ist mehr als eine willkürliche theoretische Lastannahme. Sie beweist **nicht**, wie viele der 153 einzelnen früheren Übernahmefehler direkt daraus entstanden sind.

## 2. Eine KISS-Korrektur in denselben zwei bestehenden PHP-Dateien (QA80 NUR LOKAL)

Basierend auf QA79, ohne neuen Worker, Cron, Tabelle, Klasse, fachlichen Entscheider, Pluginarchitektur, K0-Eingriff oder GitHub-Workflow-Änderung:

1. Der **eine vorhandene GitHub-Arbeiter** bearbeitet die Frischekontrolle innerhalb des bestehenden kanonischen Laufs. Eine kleine Markierung **in der bereits bestehenden gespeicherten Quellenzustandsoption** sorgt dafür, dass nach jedem Frischepaket mindestens das nächste echte Such-/Verarbeitungspaket drankommt. Die vorherige gerade/ungerade-Transportzählung versagte bei langsamem Anbieter und konnte die Suche verdrängen.
2. Verfügbarkeit: **bis zu 20** statt starr 5 fällige Quellen je Aufruf, aber mit **22 Sekunden Zeitbudget vor jedem neuen Anbieterabruf**. Der Cursor bestätigt nur wirklich bearbeitete Quellen; bei vorzeitigem Stopp keine übersprungenen ID.
3. Beim Auftreten eines eBay-Anmeldefehlers **nach bereits erledigten abgelaufenen Quellen** bleiben deren Cursor und Zähler erstmals korrekt gespeichert. Alte QA79-Version konnte bereits erledigte Arbeit wiederholen.
4. **Während eines aktiven Suchlaufs**: bei leerem fälligem Quellenpaket frühestens nach 10 Minuten erneut eine **leichte DB-Fälligkeitsabfrage**. Keine neue eBay-Suche, kein autonomer WP-Cron. Außerhalb aktiver Suche bleibt der vorhandene stündliche reine Refresh zuständig.
5. Einmalige Fachauswahl, wöchentliche volle Suche, Frische ohne Neuzuordnung, öffentlicher SAFE-Checkpoint und Abschluss-Bereinigung sind aus dem QA77/79-Kandidaten unverändert.

## 3. Reproduzierbarer RED/GREEN-Beweis im echten PHP mit fehlender WP/eBay-I/O ausdrücklich simuliert

| Probe | QA79 vorher | QA80 lokal |
|---|---|---|
| 41 fällige IDs, jeweils nur ein Anbietercheck je ID | **9 Pakete (5er)** | **3 Pakete (20/20/1)** |
| Langsame Quellenkontrolle, bestehende kanonische UUID | **8 Frische / 0 echte Controller-Pakete** | **4 Frische / 4 Controller-Pakete** |
| Ein bereits beendetes Produkt, danach Auth-Fehler | **Cursor/Zähler NICHT gespeichert** | **Cursor/Zähler gespeichert, kein doppeltes Ende** |
| Beide Original-PHP-Traits gemeinsam, eine Controller-UUID, 21 fällige Modellquellen | — | **21/21 nur einmal, 2 Controller-Pakete, SAFE erhalten** |
| Künstlich kurz gesetztes Testzeitbudget, Cursor-Abbruch | — | **41/41 ohne Verlust/Wiederholung** |
| Alte vollständige PHP-/Originalprotokollregression | — | **26.967/26.967 Assertions, 0 Fehler** |

Die Zeitbudget-Testkopie ist ausdrücklich **nicht** das Produktionszeitlimit: dort 0,04s, in QA80-Quelle 22s. Die 26.967 Tests sind weit überwiegend Protokollzeilen-Konsistenz, keine unabhängigen Produkttests. Die echte historische 283er-Pflichtfamilienliste und 95 der 153 historischen Fehler-Item-IDs bleiben enthalten, jedoch kein aktueller realer WP/Provider-Snapshot.

## 4. Ein noch offener Gesamtstopper, keine neue Mini-Reparatur

Mit 22s Zeitbudget können je nach GetItem-Latenz auch **weniger als 20** Quellen geprüft werden. Bei unterstellten 634 gleichzeitig fälligen Quellen binnen zwei Stunden wären beim gemessenen 70–72s-GitHub-Takt im Mittel mindestens **13 pro Frischepaket** erforderlich, d.h. ungefähr **unter 1,7 Sekunden je GetItem**. Das ist **keine nachgewiesene reale Providerleistung**. Die tatsächliche Zahl gleichzeitig fälliger gültiger Kampagnen, die echten GetItem-Laufzeiten und die vollständige öffentliche 283er-Familienliste sind ohne WordPress/Provider-Momentaufnahme unbekannt. Daher wurde der bisherige WP-Cron **nicht live abgeschaltet** und **keine Installationsversion erstellt**.

Gesamtvertragsabnahme **QA69: NICHT BESTANDEN**. Einmalige verbleibende reale Gesamtabnahme ist klar: derselbe verifizierte heutige SAFE-/283-Familienbestand, Fälligkeitsverteilung, GetItem-Dauer und bestätigter Endcheckpoint. Nicht nochmals lokale grüne Tests als echte Fertigstellung ausgeben.

**Original-/Test- und Codepaket dieser Gesprächsrunde:** `QA80_GESAMTURSACHE_ORIGINALDATEN_KISS_NUR_LOKAL_KEIN_PLUGIN.zip` (SHA256: `d03d60a61f3330ab101a912516055b7a164b897b1b4d4e6e77b84d4d5a3fc1d4`). Enthält beide vollständigen QA80-PHP-Quelldateien, QA79-zu-QA80-Patches, QA69-Vertrag, originale CSV, alle Tests und das 24er-Ursachenregister. **Nicht als Plugin installieren.**