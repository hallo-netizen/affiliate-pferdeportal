# P1 – PFLICHTREGEL ALS FESTER MASCHINENBESTANDTEIL

Datum: 2026-09-08
Status: GO, ABER NUR ARCHITEKTUR-PROTOTYP

## Ziel

Prüfen, ob eine später hinzukommende Pflichtregel so eingebaut werden kann, dass sie NICHT als frei zuschaltbares Zusatz-Gate endet.

Wichtig:
Die verwendete Linkprüfung ist bewusst nur eine repräsentative Prototypregel.
Sie wird NICHT als autoritative Produktions-Linkregel ausgegeben.

## Umsetzung – KISS

Keine neue Schicht.

Die bestehende TEXT_SLOT-Prüfung wurde um genau eine fest verdrahtete Regel ergänzt:
Ein Prototyp-Draft mit `http://` oder `https://` wird BLOCKED.

Es gibt:
- keinen Runtime-Schalter
- keinen Regelparameter
- keinen separaten Link-Worker
- keinen zusätzlichen Controller
- kein neues Handoff
- keine vom Chat wählbare Prüfinstanz

## Lokaler Test

16/16 PASS.

Neu gegenüber P0:
- sauberer Draft -> PASS
- Draft mit externer URL -> BLOCKED
- Versuch, die Regel im Konstruktor abzuschalten -> technisch nicht möglich
- Versuch, `allow_external_links=true` im Worker-Output einzuschleusen -> BLOCKED

Alle P0-Tests bleiben gleichzeitig PASS.

## Gegenprüfung

### 0,0 Freiheit
PASS im Prototypmodell.
Die Regel ist nicht Teil des Workerauftrags, sondern Bestandteil der festen Maschine.

### Einfluss von außen
PASS für die geprüfte Schnittstelle.
Weder Aufrufer noch Worker können die Regel zur Laufzeit abschalten oder ersetzen.

### KISS
PASS.
Eine bestehende Prüffunktion wurde erweitert. Keine neue Architekturkomponente.

### Nachhaltigkeit
PASS für das Prinzip.
Pflichtregeln liegen an einer autoritativen technischen Stelle statt als Zusatzweg.

### Themenunabhängigkeit
PASS.
Das Architekturprinzip ist domänenfrei. Die konkrete P1-Regel ist nur Testrepräsentant.

### Automatisierung
PASS.
Kein manueller Freigabeschritt nötig; Regel ergibt deterministisch PASS/BLOCKED.

### Skalierung
PASS wie P0.
Keine Änderung am artikelweisen wiederholbaren Ablauf und kein festes Batchlimit.

### Weniger fehleranfällig?
VORLÄUFIG PASS.
Die historische Problemklasse „Regel später außen antackern“ lässt sich vermeiden, indem die Regel in denselben festen Schrittvertrag eingeht.
Es entstand weder ein neuer Raum noch ein neuer Übergabepunkt.

## Wichtige Grenze

Noch NICHT bewiesen:
- echte Tabellenregel
- echte Produktions-Linkregel
- echte Textmaschine
- Prozessisolation gegen feindlichen Code im Controllerprozess
- Persistenz/Restart
- externe Endsignatur und WordPress

Diese Punkte werden nicht vorgezogen.

## GO/STOP

GO.

Der Prototyp zeigt bisher keinen Hinweis, dass die neue Architektur die alte Übergabe-Komplexität nur unter anderem Namen wiederholt.

Nächster sinnvoller Schritt:
P2 = ausschließlich prüfen, ob die bestehende Textmaschine über EINE feste Schnittstelle angebunden werden kann, ohne sie zu ändern und ohne neue freie Workflowentscheidung zu erzeugen.

Vor tatsächlicher P2-Änderung zuerst reine Schnittstellenanalyse; wenn dafür mehrere neue Handoffs/Gates nötig wären -> STOP.
