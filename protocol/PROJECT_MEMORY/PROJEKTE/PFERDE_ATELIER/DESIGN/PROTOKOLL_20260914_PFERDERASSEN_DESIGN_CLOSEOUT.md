# DESIGN – PROTOKOLL PFERDERASSEN – 2026-09-14

ROLLE: AUSFÜHRUNGSPROTOKOLL; keine zweite CURRENT-/Fehler-/Zielwahrheit.

## Tatsächlich umgesetzte Designstrecke dieses Chats

Die Pferderassen-Übersicht und Einzelansicht wurden schrittweise im bestehenden `affiliate-portal-template-kit` erweitert.

Wesentliche dauerhaft gewordene Punkte:
- Übersicht nach Glossar-Prinzip;
- Hero `PFERDE IM PORTRÄT / Pferderassen / Charakter, Herkunft & Besonderheiten`;
- sechs Rassengruppen mit eigenem Icon-/Hover-/Klickverhalten;
- Karten-Hover: Überschrift + `zur Rasse` ocker;
- Startseite max. 8 Rassen;
- `Alle Rassen` als Vollansicht, später 24/Seite paginiert;
- Rückwege zur Pferderassen-Startseite aus Filter-/A–Z-/Gruppenansichten;
- Hauptsuche um eigene Welt `Pferderassen` erweitert;
- lokale Pferderassen-AJAX-Suche an `pa_breed` gebunden;
- Einzelrasse mit Breadcrumb, Autor entfernt, Beitragsbild als Hero-/Vorschaubildquelle;
- Factsheet-Layout: linker Icon-Steckbrief | Mitteltext | rechte Wissensspalte;
- normale WordPress-Beiträge bleiben außerhalb des Scopes.

## Pluginstände / wichtige reale Readbacks

### 1.50.502
- Suche und Hero vom Nutzer real bestätigt: PASS.
- Icons zunächst ohne brauchbare Klick-/Hoverfunktion: LIVE FAIL.

### 1.50.503 / 1.50.504
- Gruppenlinks/Pointer/Hover und Karten-CTA weiterentwickelt.
- zusätzliche Navigation `Alle Rassen` / Rückweg gebunden.

### 1.50.505
- Startseitenlimit 8;
- Breadcrumb Einzelrasse;
- Autor entfernt;
- erste eigene Single-Leseachse.

### 1.50.506
- Factsheet-Single mit linker Iconspalte und rechter Wissensspalte;
- erste lokale Pferderassen-AJAX-Strecke;
- lokal hart positiv/negativ/mutation geprüft;
- realer Readback: AJAX funktionierte nicht, `Alle Rassen` unpaginiert, Single sichtbar zu schmal.

### 1.50.507
Paket:
`PFERDE_ATELIER_DESIGN_V1.50.507_AJAX_PAGINATION_BODYWIDTH_INSTALLIEREN.zip`

SHA-256:
`b27898d26b32e9fe9910a2312b6bfbcec12c738f76290ed89304eca931353ec9`

Tatsächlich ausgeführt:
- Contract 28/28 PASS;
- PHP Runtime 28/28 PASS;
- PHP Syntax PASS;
- ZIP-Lesetest PASS;
- Dateibaum 501/501;
- 11/11 absichtlich gebrochene Defekte erkannt/ROT;
- Paginationtests inkl. Slice/Clamping/Navigation PASS;
- scoped Header-AJAX `pa_breed` PASS;
- normale Posts aus Rassensuche ausgeschlossen PASS;
- Featured Image als Hero-/Vorschaubildquelle PASS;
- normale Posts vom Single-Renderer unberührt PASS.

Realer Nutzer-Browserreadback:
- Pagination: PASS;
- lokale Pferderassen-AJAX-Suche: PASS;
- Einzelrassenbreite: FAIL.

## Neuer Fehler / Warum

Der lokale Breitentest war unzureichend realitätsnah: er prüfte Sollregeln, aber nicht die vollständige Astra/Kubio-Live-Containerkette. Historische Portalbreiten-Fixes wirken am Body-/Theme-Containerpfad, nicht nur am inneren Wrapper.

Dauerhafte Konsequenz:
- kein PASS allein aus `max-width`-/CSS-Codeansicht;
- Breitenänderung muss gegen den echten gerenderten Containerpfad geprüft werden;
- `single-pa_breed` soll den bewährten Portalbreitenmechanismus gezielt übernehmen.

## Nutzerentscheidung nach 1.50.507

Der generische Hero-Kurztext unter dem Rassentitel entfällt vollständig. Beispiel für zu entfernenden Text:
`Burguete stammt aus Spanien. Der Datensatz dokumentiert Herkunft, Nutzung, Zucht und zentrale Merkmale dieser Pferderasse.`

## Nicht ausgeführt

- kein finaler Breitenfix nach diesem LIVE FAIL;
- kein realer LIVE PASS der breiten Einzelrassenseite;
- kein isoliertes Plugin-`CURRENT.zip` im PLUGINS-Büro für 1.50.507;
- keine autoritative GitHub-Plugin-Sourcebindung der lokal erzeugten 1.50.500–1.50.507 Paketbytes.

Aktueller Fehlerstatus ausschließlich in `FEHLERQUELLEN.md`; aktueller Stand ausschließlich in `CURRENT_STATE.md`.