# VERBINDLICHER EBAY-ZIELVERTRAG – KISS / Einzelarbeiter / ein Entscheidungsort
Stand: 14.11.2026 · Pferde Atelier · QA69 · verbindlich für die Fortsetzung

## 1. Das Ziel – schlicht

Ein gespeicherter eBay-Auftrag soll ohne Neubeginn bis zu einem **belegbaren** Ergebnis geführt werden. Das Ergebnis muss **für jede der 283 aktuellen Pflicht-Produktfamilien** sagen, welche aktuellen, zulässigen Artikel öffentlich sichtbar sind oder **mit welchem echten Nachweis** keine zulässige Ware gefunden werden konnte. **283 Prüfergebnisse sind Pflicht, 283 positive Produkte dürfen nicht erfunden werden.** Der letzte öffentlich gültige Bestand bleibt bestehen, bis ein überprüfter Ersatz oder eine belegte Sperre vorliegt.

## 2. Genau eine Zuständigkeit pro Aufgabe

**Ein vorhandener externer Zeitgeber:** GitHub löst ausschließlich den **einen vorhandenen kanonischen WordPress-Arbeitslauf** aus. Kein neuer WP-Cron, kein zusätzlicher Importer, keine selbstständigen konkurrierenden Suchläufe. *Eine technische Arbeitspaket-Phase ist kein neuer autonomer Worker.*

**A. Recherche:** Einmal reale eBay-Angebote mit Artikel-/Quellkennungen lesen und dauerhaft speichern. **Keine Freigabe, keine Artikel-Rangentscheidung.** Wiederaufnahme am gespeicherten Cursor.

**B. Fachauswahl:** Einmal je Artikel/Familien-Entscheidung Thema, Eignung, Ziel, Rang und maximal drei Produkte **am selben fachlichen Entscheidungsort** festlegen. Die Entscheidung als verbindlichen Auswahlstand speichern. Nachfolgende Arbeit darf nur das Ergebnis benutzen. Eine echte Änderung der Eingabedaten ist ein **neuer belegter Sachverhalt**, keine heimliche Zweitentscheidung.

**C. Aktualität:** Nur **ausgewählte** Artikel, deren Quellnachweis abgelaufen ist, vor Nutzung beim Anbieter gezielt neu bestätigen. Dieser Teil darf **keine Kategorien, Rangplätze oder Ersatzprodukte wählen**. Eine identisch gebliebene Quelle behält die fachliche Auswahl; eine geänderte/gesperrte Quelle wird mit Grund markiert, nicht stillschweigend neu zugeordnet. Keine stundenlangen zweiten Gesamt-Abgleiche nach frischer Vollrecherche.

**D. Öffentlichkeit:** Ein einziger verbindlicher Freigabeort verwendet die gespeicherte Fachauswahl und aktuelle Anbieterfakten. **Bereits unverändert öffentlich geprüfte Produkte werden nicht bei jedem Arbeitstakt nochmals komplett geprüft.** Für wirklich neue Artikel erfolgt genau die eine dafür nötige Sicherheitsprüfung. Eine beim langen Lauf zeitlich veraltete Anbieterbestätigung darf **nicht blind veröffentlicht** werden; ein nötiger Frischebeleg ist eine Quellenprüfung, **keine neue Fachentscheidung**.

**E. Endbestand und Bereinigung:** **Ein** verifizierter öffentlicher Bestand ist die Quelle für Freigabe, Anzeige und Bereinigung. Die Auswahlphase darf den gesamten Warenbestand **nicht vorzeitig aufräumen oder erneut durchscannen**. Der bestehende Schluss-Arbeiter räumt **einmal nach gespeichertem, nachweislich geprüftem öffentlichem Ergebnis** auf. Er darf keine eigene Produktentscheidung treffen und keine gültigen Altprodukte allein wegen fehlender Neu-Suchergebnisse entfernen.

**F. Abschluss:** Nur nach belegtem öffentlichen Endbestand. Suche fertig ≠ Gesamtauftrag fertig. Folgelauffrist erst ab tatsächlichem Gesamtabschluss. Ein manueller Stopp wird nie übergangen, der gespeicherte Lauf nicht unbemerkt neu gestartet.

## 3. Harte Verbote

- **Keine** weitere Themen-/Rang-/Partner-Entscheidung durch Aktualisierung, Materialisierung, Bereinigung oder Ausgabe.
- **Keine** Wiederholung derselben öffentlichen Vollprüfung ohne neue, prüfpflichtige Kandidaten.
- **Keine** Voraus-Bereinigung während der Auswahl; **keine** vorzeitige Entfernung nachweislich gültiger Veröffentlichungen.
- **Keine** doppelten Zeitgeber, zusätzlichen Jobs/Tabellen, konkurrierenden Auswahlpfade oder zusätzliche Pluginarchitektur.
- **Keine** „erfolgreich“-Behauptung allein wegen PHP-Simulation, Testzählern, einer gespeicherten Freigabeanzahl oder einem grünen GitHub-Job.

## 4. Echte Ursachen aus dem vorhandenen Originalprotokoll

Das echte eBay-Protokoll (Run `97507628-4f4d-4527-bd77-fa573bce7067`) enthält **2.769 lückenlos nachgespielte Ereignisse**, am Ende **5/283** und **153** verworfene bei **155** gewählten Angeboten. Darin sind **395 Protokolleinträge beziehungsweise 196 unterschiedliche Arbeitstakte** mit dem Zwischenstand `business_prune` belegt, über **3 Stunden 38 Minuten 38 Sekunden**. Der echte Originalcode führt dort einen weiteren Gesamtdurchgang aus, obwohl nach dem endgültigen öffentlichen Ergebnis erneut aufgeräumt wird.

Die fehlenden Familien stehen im zweiten echten Export: **278 einzelne Familien**, davon **215 ohne zugeordneten Einzelabruf im aktuellen Teilstand**, **32 mit angenommenen Angeboten ohne öffentliche Abdeckung** und **31 mit Abruf ohne akzeptiertes Angebot**. Daraus darf **nicht** abgeleitet werden, die 215 seien grundsätzlich nie recherchiert oder alle 578 alten Freigaben öffentlich gültig.

## 5. Im vorhandenen Plugin umgesetzt – QA69, nur Prüfkandidat

- In der originalen Auswahlphase wird der **vorzeitige BUSINESS-Gesamtdurchgang** unter dem einen kanonischen Arbeitslauf ausgelassen, sowohl bei frischer Materialisierung als auch bei übernommenem `business_prune`-Checkpoint. Die vorhandene einmalige Schluss-Bereinigung bleibt bestehen. Ein eigenständig laufender Alt-Auswahlauftrag behält seinen ursprünglichen Weg.
- Wenn ein Produkt bereits im gespeicherten sicheren öffentlichen Bestand steht, entfällt seine **unnötige erneute Gesamt-Freigabeprüfung** bei einem unveränderten Auswahlpaket. Ein **neuer** Artikel muss weiter durch das bestehende Sicherheitsgate.
- Unverändert: Produkt-Ranking, zielgerichtete Aktualität, öffentliche Abschlussprüfung und Schutz-/Speicherregeln, Stopp/Pause, der GitHub-Workflow, andere Partner, WordPress-Core und sichtbares Frontend.
- Die neue **6.72.348** enthält das vollständige bestehende Plugin, lediglich die zwei eigentlichen eBay-PHP-Methoden-Dateien sowie Versions-/Update-Einträge wurden geändert. **Noch nicht live freigegeben.**

## 6. Beweisgrenze: eine echte 1:1-Simulation ist bisher NICHT möglich

**Mit echten Dateien wurde jeder der 2.769 Original-Protokolleinträge in Reihenfolge nachgespielt.** Damit sind der reale Verlauf, die 196 verzögernden Arbeitstakte und die 278 offenen Familien belegt. **Das ist aber nur ein 1:1-Protokoll-Replay, keine 1:1-Simulation der Produktauswahl.**

Die beiden echten CSVs enthalten **keine** individuellen Artikelkennungen mit zugehörigen vollständigen Original-eBay-Antworten, aktuellen WordPress-Produkt-/Creative-/Output-Datensätzen, versioniertem öffentlichen Checkpoint und relevanten Provider-Zeitpunkten. Ohne genau diese **Original-Eingaben** wäre jede angebliche 1:1-Nachberechnung eine erfundene Simulation. Die Tests des Original-PHP mit nachgestellten Daten sind lediglich **Regressionstests**, kein Nachweis für reale 283 Familien oder aktualisierte 153 Angebote.

**Verbindlicher Abnahmestatus: NICHT BESTANDEN / NICHT FREIGEGEBEN.** Auch wenn alle lokalen Codeprüfungen bestehen, darf keine Abnahme gemeldet werden. Eine wirkliche 1:1-Gesamtabnahme benötigt einen unveränderten echten Datenbank-/Quell-Snapshot und die dazu gehörigen Original-Provider-Antworten sowie einen real eingelieferten GitHub-Takt und öffentlich sichtbar geprüften Endbestand. Alles muss sich **derselben Run-ID** zuordnen lassen.

## 7. Abnahme – ausschließlich gemeinsam, nicht schrittweise scheinbar grün

Ein Test gilt erst als bestanden, wenn die folgenden Fakten **gleichzeitig** aus **echten** Daten belegt sind: derselbe gespeicherte Lauf/Cursor nach Wiederaufnahme; tatsächlich eingehende GitHub-Takte; pro Familie **ein** Fachentscheid mit Beleg; 153 alte Fehlergegenbeispiele korrekt verarbeitet bzw. real begründet gesperrt; erhaltene tatsächlich gültige Altprodukte; nur eine verbindliche öffentliche Freigabe und spätere Bereinigung aus **derselben** verifizierten Liste; alle 283 Familien mit echtem Status und öffentlich stimmiger Anzeige; nachgewiesener terminaler Abschluss; kein zweiter Zeitgeber/Worker.

Wenn **ein** Beweis fehlt, lautet das Gesamtergebnis **NICHT BESTANDEN**. Keine erneute Minifixes- oder Installationsfreigabe aus Einzelsimulationen.