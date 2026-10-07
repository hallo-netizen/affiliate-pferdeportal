# HOBBY DEPOT – 3-SÄULEN-ZIELBAUM / NEUER KATEGORIENVERTRAG

STAND: 2026-10-07
STATUS: VERBINDLICHE NEUAUSRICHTUNG

## 1. Grundsatz

Die Informationsarchitektur wird NICHT aus DataForSEO erzeugt.

Reihenfolge:
1. fachliche Struktur definieren;
2. Hobbys eindeutig normalisieren und einer Rolle zuordnen;
3. Monetarisierung prüfen;
4. Dubletten/Kannibalisierung über alle drei Säulen prüfen;
5. DataForSEO liefert danach die besten Suchbegriffe für bereits definierte Knoten;
6. erst danach WordPress/HivePress synchronisieren.

DataForSEO darf:
- Suchbegriff, Synonyme und Varianten belegen;
- SEO-Titel/Keywordvorschläge liefern;
- Keywordüberschneidungen sichtbar machen.

DataForSEO darf NICHT:
- Hauptwelt wählen;
- Zwischenkategorie erfinden;
- Magazinrubrik erfinden;
- HivePress-Struktur erfinden;
- aus einer Keywordphrase automatisch einen sichtbaren Kategorienamen machen.

## 2. Allgemeingültige Engine / Projektprofil

Die technische Engine darf keine Hobby-Depot-Fachbegriffe voraussetzen.

Sie kennt nur drei konfigurierbare Rollen:
- CORE = fachlicher/kommerzieller Hauptbereich;
- EDITORIAL = Magazin/Journal/SEO-/Inspirationsbereich;
- DIRECTORY = Anbieter/Kurse/Dienstleistungen/Verzeichnis.

Ein Projektprofil liefert dazu lediglich die projektspezifischen Namen, Bäume, Tiefenregeln und Routingregeln. Hobby Depot ist ein solches Profil; Gaumen Atelier oder jedes andere Thema kann ein anderes Profil verwenden, ohne die Engine umzubauen.

Die Engine muss daher können:
- beliebige Root- und Zwischenknoten aus einem versionierten Zielbaum übernehmen;
- beliebige projektspezifische Rollenbezeichnungen anzeigen;
- Add / Move / Rename / Merge / Archive / Delete per Soll/Ist-Diff;
- projektübergreifend dieselbe Dubletten-/Intent-/Keyword-Ownership-Logik anwenden;
- Monetarisierungsregeln als Projektregel auswerten, ohne Themen zu verlieren;
- DataForSEO ausschließlich als Keyword-/SEO-Evidenzadapter verwenden, niemals als Strukturautorität.

## 3. Drei Säulen – Hobby-Depot-Profil

### Säule A – Hauptportal / Hobbywelten
Zweck: bekannte Hobbys, Wissen, Ausrüstung, Produkte.

Feste Hauptwelten:
- Gestalten
- Fertigen
- Technik
- Forschen
- Pflanzen
- Tiere
- Bewegen
- Sammeln

Maximale Tiefenregel bleibt:
SEITE → SEITE → SEITE → KATEGORIE → BEITRÄGE.

Zwischenbereiche sind bewusst redaktionell/fachlich definiert. Keine automatische Taxonomie aus Rohliste oder Keyworddaten.

Arbeitsstruktur:

Gestalten:
- Malen & Zeichnen
- Druck & Fotografie
- Schrift & Lettering
- Papierkunst
- Textilgestaltung
- Oberfläche & Deko
- Miniaturen & Szenen

Fertigen:
- Holz
- Metall
- Textil
- Leder
- Buch & Papier
- Keramik & Glas
- Guss & Form
- Schmuck
- Genuss

Technik:
- Elektronik
- Funk
- Robotik
- Computer & Retro
- Digitale Fertigung
- RC & Drohnen
- Audio
- Mechanik
- Smart Home

Forschen:
- Astronomie
- Mikroskopie
- Wetter
- Naturbeobachtung
- Messen & Analysieren
- Citizen Science

Pflanzen:
- Bonsai
- Zimmerpflanzen
- Kakteen & Sukkulenten
- Orchideen
- Hydroponik
- Pilze
- Saatgut & Zucht
- Moos & Miniaturgärten
- Essbare Pflanzen

Tiere:
- Aquaristik
- Terraristik
- Ameisen & Insekten
- Wirbellose
- Imkerei
- Gehegegestaltung
- Zucht & Futtertiere

Bewegen:
- Outdoor
- Rollen & Balance
- Wurf & Ziel
- Wasser
- Klettern & Seil
- Wind & Drachen
- Team & Wettkampf
- Geschick & Tricks

Sammeln:
- Münzen & Geld
- Papier & Dokumente
- Technik & Medien
- Spielzeug & Spiele
- Naturfunde
- Werbung & Design
- Werkzeuge & Geräte
- Alltagsobjekte

Keine starre universelle Maximalzahl direkter Kinder wird erfunden. Die Ebene muss übersichtlich und logisch bleiben. Ein zu breiter Ast wird fachlich geteilt; ein zu dünner Ast wird nicht künstlich aufgefüllt.

## 4. Hobby-Ebene / Content-Kategorien

Ein Hobby ist ein stabiler eigener Knoten mit eigener hobby_id.

Beispiel:
Fertigen → Buch & Papier → Buchbinden.

Darunter werden nur tatsächlich benötigte Content-Kategorien geführt. Prüfbereiche:
- Einstieg
- Ausrüstung
- Material
- Techniken & Praxis
- Fragen & Probleme
- FAQ
- optional Lernen & Kurse

Nicht jeder Prüfbereich wird automatisch angelegt.
Keyword ≠ Kategorie.

## 5. Monetarisierungs-Gate

Ein Hobby darf nur als eigenständiges Hauptportal-Hobby veröffentlicht werden, wenn:
- monetization_fit = DIRECT oder ASSISTED;
- mindestens ein konkreter monetization_path belegt ist;
- die Begründung gespeichert ist.

Erlaubte Pfade:
- Produkte/Ausrüstung
- Zubehör/Verbrauch
- Kurse
- Anbieter/Dienstleistungen
- Verleih
- Reparatur/Service

NONE oder UNKNOWN dürfen NICHT in das Hauptportal promoviert werden.

Sie werden NICHT verworfen. Jeder fachlich gültige Kandidat bleibt im zentralen Bestand erhalten. Wenn kein DIRECT/ASSISTED-Fit vorliegt, gehört sein veröffentlichbarer SEO-/Inspirationsraum grundsätzlich in die redaktionelle Säule (Magazin/Journal) oder bleibt dort als geplanter redaktioneller Kandidat erhalten. Monetarisierung entscheidet damit über die SÄULE, nicht über das Behalten oder Löschen des Themas.

Beispiel:
Treibholz und Treibholz sammeln werden zuerst zu EINER hobby_id zusammengeführt.
Ohne belegten DIRECT/ASSISTED-Fit darf dieser Datensatz nicht als Hauptportal-Hobby unter Sammeln erscheinen.

## 6. Säule B – Magazin

Zweck: Inspiration, Hobbywahl, Situationen, Saison, ungewöhnliche/kleine Themen, Trends und Longtails.

Feste Magazin-Navigation:

Magazin
→ Hobby finden
   → Hobbyfinder
   → Hobbywelten
→ Nach Situation
   → Zuhause
   → Draußen
   → Alleine
   → Zu zweit
   → Wenig Platz
   → Wenig Zeit
→ Nach Jahreszeit
   → Winter
   → Sommer
→ Entdecken
   → Ungewöhnliche Hobbys
   → Verrückte Hobbys
   → Neue Hobbys
   → Trends

Hobbyfinder und Hobbywelten sind damit Bestandteil der Magazin-Navigation, bleiben aber eigenständige Seiten/Funktionen.

Magazinartikel leiten in:
Magazin → Hobbyfinder/Hobby → Hauptportal → Ausrüstung/Produkte/Anbieter.

Das Magazin besitzt keine Kopie des Hauptportalbaums.

## 7. Säule C – HivePress / Anbieter

HivePress ist eine eigene Anbieterstruktur und KEINE Kopie des Content-Baums.

Feste Anbieterarten:
- Kurse & Workshops
- Trainer & Coaches
- Vereine & Gruppen
- Werkstätten & Studios
- Fachgeschäfte
- Verleih
- Reparatur & Service
- Events & Reisen

Listings können zusätzlich über hobby_id mit einem Hobby verbunden werden.
Die hobby_id ist Verbindung, aber erzeugt keine zweite SEO-Hobbyseite in HivePress.

Eine HivePress-Kategorie wird nur aktiviert, wenn reale Anbieter-/Kurs-/Dienstleistungsnutzung vorgesehen ist.

## 8. Globale Dubletten- und Kannibalisierungsregel

Die Prüfung gilt GEMEINSAM über:
- Hauptportal;
- Magazin;
- HivePress.

Vor WordPress-Write muss ein globales Ownership-Register existieren.

Jeder primäre Suchintent und jedes Primärkeyword hat genau EINEN Owner.

Pflichtprüfung:
- gleiche normalisierte Hobbyidentität;
- gleiche/nahe Synonyme;
- gleicher Primärkeyword-Owner;
- gleicher Intent-Key;
- semantisch stark überlappende Zielseiten;
- Alias-/Dubletten wie Treibholz / Treibholz sammeln.

Exakte Primärkeyword-Dubletten über zwei Säulen sind BLOCKED.
Semantisch gleiche Intentionen über zwei Säulen sind BLOCKED.
Eine andere Säule darf denselben Hobbybegriff nur als Relation/Filter/Verweis benutzen, nicht als konkurrierende SEO-Zielseite.

## 9. DataForSEO-Rolle

Für jeden bereits definierten Strukturknoten gibt es:
- display_name = kurzer Navigationsname;
- seo_seed = fachlich vorgegebener Ausgangsbegriff;
- primary_keyword = von DataForSEO gewählter/bestätigter Suchbegriff;
- aliases/synonyms = Recherchevarianten.

display_name und primary_keyword dürfen verschieden sein.

Beispiel:
display_name: Outdoor
primary_keyword: Outdoor Hobbys

Ein langer Suchbegriff darf niemals automatisch zum Menünamen werden.

## 10. Flexible Änderungen

Die Struktur ist versioniert, aber nicht starr.

Jeder Knoten besitzt stabile node_id/hobby_id.

Änderungen:
- hinzufügen → neuer Knoten;
- umbenennen → gleiche ID, neuer Name;
- verschieben → gleiche ID, neuer parent;
- löschen → zuerst Abhängigkeiten prüfen, dann archivieren/löschen;
- zusammenführen → Alias auf Gewinner-ID, keine zweite Seite;
- aufteilen → neue IDs, explizite Ownership-Verteilung.

WordPress wird immer per Soll/Ist-Diff synchronisiert.

## 11. Sichtbarkeit / atomarer Import

Ein halbfertiger Baum darf nicht minutenlang öffentlich sichtbar sein.

Ablauf:
1. Zielbaum vollständig bauen;
2. global validieren;
3. Dry-Run Soll/Ist;
4. Änderungen schreiben;
5. kompletten Readback prüfen;
6. erst danach Navigation/Cache auf neue Revision umschalten.

Bei Fehler:
Rollback bzw. alte sichtbare Revision bleibt aktiv.

## 12. Abnahme

Kein PASS ohne:
- Hauptportal-Struktur;
- Magazin-Struktur;
- HivePress-Struktur;
- Monetarisierungs-Gate;
- Hobby-Dublettenprüfung;
- globale Keyword-/Intent-Kannibalisierungsprüfung über alle drei Säulen;
- Add/Move/Rename/Delete-Simulation;
- bestehende IDs erhalten, soweit Objektidentität gleich bleibt;
- Positiv- und Negativ-E2E;
- WordPress-/Frontend-Readback.
