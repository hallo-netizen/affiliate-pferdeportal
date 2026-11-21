# Pferdeatelier – Suche / Relevanssi Audit

Stand: 2026-11-21

## Ziel
Prüfen, ob Relevanssi 4.28.8 und Relevanssi Live Ajax Search 2.6 für Hauptsuche, Glossar, Pferderassen und Anzeigensuche noch benötigt werden. Keine Entfernung ohne inhaltlichen Funktionsnachweis.

## Aktiver Stand
Live aktiv:
- Relevanssi 4.28.8
- Relevanssi Live Ajax Search 2.6
- Pferde Atelier Glossar Core 1.4.0
- Pferde Atelier HivePress Anzeigensuche 2.1.5-ajax-category-label
- Pferde Atelier – HivePress Anzeigensuche 1.0.1
- Pferde Atelier – Pferderassen Manager 0.2.6
- Affiliate Portal Template Kit 1.50.616

## Hauptsuche
Exakter Template-Kit-Stand 1.50.616 geprüft.
- Eigener AJAX-Eigentümer: pftk_header_search_v150426.
- Eigenes Ergebnislayout für Seiten, Beiträge, Glossar, Pferderassen und Anzeigen.
- Das Template entfernt am Header aktiv Relevanssi-Live-Attribute/Instanzen und unterdrückt dessen Ergebniscontainer.
- Relevanssi Live Ajax Search ist damit NICHT Eigentümer der Hauptsuche.
- Relevanssi Core wird serverseitig weiterhin bewusst als erste Rankingquelle benutzt: grouped_search_query_v150408() ruft relevanssi_do_query(), wenn vorhanden.
- Fallback ohne Relevanssi Core existiert über native WP_Query. Damit bricht die Suche technisch nicht, Ergebnisreihenfolge/-abdeckung kann sich aber ändern.
- In einem Ursachenprofil wurden im Header-Suchpfad 8 Zugriffe auf slfo_relevanssi mit zusammen ca. 23,28 ms gemessen. Relevanssi Core ist damit real beteiligt, aber kein Beleg für den mehrsekündigen Haupt-Performancefehler.

## Pferderassen
Exakter Template-Kit-Stand 1.50.616 geprüft.
- Eigene lokale Rassensuche.
- Eigener AJAX-Transport über pftk_header_search_v150426 mit scope=pa_breed.
- horse_breed_search_items_v150506() liest veröffentlichte pa_breed-Datensätze direkt.
- Relevanssi Live Ajax Search ist für die lokale Pferderassensuche nicht erforderlich.
- Die globale Hauptsuche zeigt Pferderassen ebenfalls an; dort kann Relevanssi Core weiterhin Ranking/Abdeckung beeinflussen.

## Glossar
Exakter Template-Kit-Stand 1.50.616 geprüft.
- Eigene Glossar-Suchoberfläche.
- Eigener AJAX-Aufruf action=uge_search an den Glossar-Core.
- Relevanssi Live Ajax Search ist dafür nicht der Transport/Eigentümer.
- Der exakte interne Quellcode des aktiven Glossar-Core 1.4.0 liegt im geprüften Ablagebestand derzeit nicht als installierbares Quellpaket vor. Deshalb wird NICHT behauptet, Relevanssi Core sei intern garantiert unbenutzt.
- Für eine Core-Entfernung ist daher zusätzlich ein inhaltlicher Alt/Neu-Treffertest nötig.

## Anzeigen
Aktiv sind zwei ausdrücklich eigenständige Pferdeatelier-Suchplugins:
- 2.1.5-ajax-category-label: eigenständige AJAX-Suche nur für veröffentlichte HivePress-Anzeigen und -Kategorien.
- 1.0.1: eigenständige globale Suche für veröffentlichte HivePress-Anzeigen auf hp_listing_category-Seiten; ersetzt dort die native HivePress-Suchform.
Template Kit 1.50.616 besitzt zusätzlich eigene Header-Anzeigenlogik:
- Anzeigenkategorien
- konkrete hp_listing
- native Volltextsuche
- Custom Fields
- Taxonomie
- Fuzzy-Titelfallback
Relevanssi Live Ajax Search ist dafür nicht erforderlich.
Relevanssi Core wird innerhalb der GLOBALEN Hauptsuche als eine erste Quelle für hp_listing genutzt; danach existieren native und eigene Fallbacks. Eine Entfernung darf daher erst nach Ergebnisgleichheitsprüfung erfolgen.

## Performancebeleg
Relevanssi Live Ajax Search lädt trotz eigener Sucharchitektur weiterhin 1 Frontend-Script und 1 Stylesheet:
- relevanssi-live-search-client
- relevanssi-live-search
Das ist reale, funktional für die vier geprüften Suchwege nicht mehr benötigte Zusatzlast. Sie ist NICHT als Hauptursache der mehrsekündigen Serverlast belegt.

## Entscheidung
### Relevanssi Live Ajax Search 2.6
Status: REMOVAL CANDIDATE / für die vier geprüften Suchwelten funktional redundant.
Noch nicht eigenmächtig deaktivieren. Vor endgültiger Entfernung einmal gebündelter Funktions-A/B über:
1. Hauptsuche
2. Glossar
3. Pferderassen
4. Anzeigenmarkt
Erwartung: identische Funktion; zusätzlich verschwinden das unnötige Script/Stylesheet.

### Relevanssi Core 4.28.8
Status: NOCH BEHALTEN.
Grund: Hauptsuche ruft den Core nachweislich als Rankingquelle auf. Technischer WP-Fallback existiert, aber gleiche Treffer/Reihenfolge/Abdeckung ist noch nicht bewiesen.
Entfernung nur, wenn ein breiter semantischer Alt/Neu-Treffertest 0 relevante Funktionsverluste beweist oder die noch benötigte Rankinglogik vollständig in den eigenen Suchcode übernommen und ebenfalls gegen den Iststand geprüft wurde.

## KISS-Folge
Kein neues Einzelplugin für diese Prüfung. Relevanssi-Aufräumen wird in den bestehenden gebündelten Performance-/Aufräumablauf aufgenommen. Zuerst Funktionsgleichheit, dann Entfernung; danach vollständiger PASSIV-Gesamtlauf.
