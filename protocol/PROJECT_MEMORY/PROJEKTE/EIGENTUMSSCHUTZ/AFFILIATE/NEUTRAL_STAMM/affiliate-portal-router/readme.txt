=== Portalneutraler Affiliate-Stamm ===
Contributors: neutral
Requires at least: 6.0
Requires PHP: 7.4
Stable tag: development

== Status ==

neutralen Affiliate-Stamm ist eine laufende Portierung der bestehenden Affiliate-Zentrale.
Noch kein Release und nicht installierbar.

== Architektur ==

* Zentrale Affiliate-/Provider-Engine bleibt erhalten.
* Portal-Ziele sind im neutralen Stamm nicht gebunden und müssen projektseitig über den vorgesehenen Zielquellen-Adapter geliefert werden.
* eBay und idealo besitzen reale Adapter.
* Amazon ist im übernommenen Quellstand nur vorbereitet; ein realer Amazon-Adapter wird nicht behauptet.
* Provider-Secrets werden ausschließlich über die vorhandenen Laufzeit-/Optionsschnittstellen verwendet und nicht in diese Quelle dokumentiert.
* Projektfremde Portal-, Produkt-, Recovery- und Fachbestände werden nicht übernommen.

== Release-Regel ==

Erst nach vollständiger Bereinigung sowie Positiv-, Negativ- und Regressionstests darf ein Installationskandidat entstehen.
