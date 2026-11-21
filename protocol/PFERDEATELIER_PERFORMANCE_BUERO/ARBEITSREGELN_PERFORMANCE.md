# Pferdeatelier Performance – verbindliche Arbeitsregeln

Stand: 21.11.2026

1. Möglichst viele sinnvolle Arbeitsschritte werden gebündelt. Kein Plugin-Takt mit ständig neuen Einzelversionen.
2. Vor jeder Plugin-Ausgabe muss die Änderung lokal/simuliert geprüft sein.
3. Jede Performance-Änderung braucht einen Kausalitätsbeweis:
   - konkrete gemessene oder reproduzierte Ursache,
   - Nachweis, dass genau die geänderte Stelle diese Ursache reduziert,
   - kein Fix allein aufgrund von Vermutung, Korrelation oder allgemeiner Optimierungsidee.
4. Jede Plugin-Ausgabe braucht einen Funktionsschutz, der über Byte-/Dateivergleiche hinausgeht:
   - inhaltliche Alt/Neu-Vergleichstests der betroffenen Funktionswege,
   - identische Entscheidungen/Ausgaben bei relevanten Normal-, Rand- und Wechselzuständen,
   - Prüfung von Ranking, Auswahl, Provider, Fallback, Veto, Health, Bilder, Tracking, Rendering und Schreibwegen, soweit vom geänderten Pfad berührt,
   - bei dynamischen/unsicheren Zuständen muss der historische sichere Pfad erhalten bleiben.
5. Byte-, Datei-, Hook- und Schreibprimitive-Vergleiche sind nur Zusatzbelege, niemals alleiniger Freigabebeweis.
6. Kein vorhandener Funktionsumfang darf zur Performanceverbesserung zurückgebaut werden.
7. Ein neues Installationspaket wird erst ausgegeben, wenn mehrere belegte sichere Änderungen soweit sinnvoll zusammengeführt und gemeinsam regressionsgeprüft wurden.
