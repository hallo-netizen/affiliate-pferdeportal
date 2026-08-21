# V100 – Journal-Unterkategorien: Root-Card Owner Fix

## Ausgangslage
V99 war live sichtbar falsch. Der Nutzer-Screenshot vom 21.08.2026 11:38 zeigte weiterhin das native blaue Astra-Kategorielabel sowie einen linksbündigen nativen Auszug. Damit war die behauptete Journal-Root-Gleichheit nicht gegeben.

## Warum V94–V99 scheiterten
Die früheren Versionen versuchten, die native Astra-Archivkarte mit immer spezifischeren CSS-Regeln und Teil-Hooks an den Journal-Root anzupassen. Das war die falsche Architektur für diesen Scope: sichtbare Teile blieben abhängig vom tatsächlich aktiven Astra-DOM, von Theme-Hookpositionen und von nativen Meta-/Content-Wrappern. Lokale Fixtures, die dieses konkurrierende Nativmarkup nicht hart genug enthielten, konnten deshalb einen falschen PASS erzeugen.

## V100 Ursachenfix
Nur im exakt registrierten Journal-Kategorie-Scope wird die sichtbare Beitragskarte jetzt vollständig serverseitig am Astra-Entry-Top erzeugt. Die Ausgabe verwendet direkt die bereits vorhandenen Journal-Root-Klassen und dieselbe sichtbare Reihenfolge: Bild, ockerfarbenes Termlabel, Titel, Auszug, Weiterlesen.

Das danach von Astra bzw. weiteren Entry-Hooks erzeugte native Innenmarkup wird nicht gelöscht. Es bleibt technisch im DOM, ist aber als direktes Nicht-Owner-Kind ausschließlich innerhalb der V100-Journal-Karte `display:none`. Dadurch kann es die sichtbare Karte nicht mehr mit blauem Meta, abweichendem Padding, Rundungen oder linksbündigem Theme-Auszug überschreiben.

## Scope
Freigabe nur über die bestehende registrierte Journal-Kategorieauflösung. Nicht registrierte Kategorien erhalten weder Owner-Klasse noch Renderer noch V100-CSS. Journal-Root und Tabellen-CSS wurden byteidentisch zu V99 gehalten.

## Allgemeingültige Ableitung
Der allgemeine V100-Vertrag verbietet für spezialisierte Journal-/Magazin-Termkarten das partielle Nachstylen unbekannten Theme-Nativmarkups. Die Universal Portal Design Suite besitzt ihr Kartenmarkup bereits selbst; V100 markiert Journal-Term-Postkarten zusätzlich explizit mit `upds-journal-term-card` und lässt generische Karten unverändert.

## Testvertrag
Der Browser-Harness enthält absichtlich feindliches Astra-artiges Nativmarkup nach der Owner-Ausgabe. V100 muss dieses nur im Journal-Scope ausblenden, während dieselbe Native-Struktur in einer Fremdkategorie sichtbar bleibt. Zusätzlich muss die V100-Zielkarte bei identischem Inhalt gegen die Root-Referenz geometrisch und pixelbasiert identisch sein.
