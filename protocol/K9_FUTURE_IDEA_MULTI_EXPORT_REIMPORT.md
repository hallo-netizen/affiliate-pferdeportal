# K9 – spätere Designidee: mehrere Exporte, ein gemeinsamer Redaktionsplan

Status: IDEE / NICHT AKTIVE K9-REGEL / NICHT JETZT UMSETZEN

Grundgedanke:
- Der Herkunftsstempel gehört zum einzelnen Produktionsauftrag bzw. Artikel.
- Der Redaktionsplan bleibt die zentrale Gesamtwahrheit des Projekts.
- Mehrere WordPress-Exporte dürfen später gemeinsam verarbeitet und gemeinsam oder gemischt zurückimportiert werden.
- Beim Reimport wird jeder Artikel einzeln gegen seine Artikel-/Plan-Slot-Identität und seinen Herkunftsstempel geprüft, nicht der gesamte Rückimport gegen genau einen ursprünglichen Export.
- Der Redaktionsplan muss jederzeit erkennen können: erledigt, in Arbeit, offen, Kategorienabdeckung, Keyword-Abdeckung und mögliche Kannibalisierung.
- Neue Exporte müssen den jeweils aktuellen Redaktionsplan berücksichtigen, damit bereits erledigte oder laufende Slots nicht unkontrolliert erneut ausgegeben werden.
- Hat sich ein Slot zwischen Export und Reimport wesentlich verändert, darf der Artikel nicht blind importiert werden; der Konflikt muss sichtbar werden.

Zielbild:
Mehrere unabhängige Produktionspakete können zeitversetzt entstehen und später zusammengeführt werden, ohne die zentrale Prüfbarkeit des Redaktionsplans zu verlieren.

Wichtig:
Diese Notiz ist nur für die spätere Skalierung. Sie verändert den laufenden Fresh-Chat-Autotest und die bestehenden Qualitätsgates nicht.
