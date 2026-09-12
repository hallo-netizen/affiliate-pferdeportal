# UNIVERSAL GLOSSAR ENGINE – CURRENT_STATE

STAND: 2026-09-12
STATUS: KONZEPT GEBUNDEN / PROTOTYP NOCH NICHT GEBAUT

## Belastbarer Stand

- Geplanter Modulname: `MOD-008 – Universal Glossar Engine`.
- Ziel: ein einziger projektunabhängiger WordPress-Core für mehrere Portale.
- Erste Projektanwendung: Pferde Atelier.
- Pferde-spezifische Begriffe, Oberbereiche, Texte, URL-Basis und SEO-Schemata dürfen nicht im Core hart verdrahtet werden.
- Projektkonfiguration liegt außerhalb des Core.
- Ein eigener WordPress-Backendbereich `Glossar` ist vorgesehen.
- Glossarbegriffe sollen als eigener WordPress-Inhalt verwaltet werden, aber nicht als normale Beiträge oder Seiten erscheinen.
- Oberbegriffe sollen getrennt von normalen WordPress-Kategorien verwaltet werden.
- Eine vorhandene WordPress-Seite kann als Glossar-Hauptseite ausgewählt werden.
- Jeder veröffentlichte Begriff soll eine eigene Zieladresse sowie eigene SEO-Titel-/Meta-Description-Werte erhalten können.
- SEO-Ausgabe soll providerneutral bleiben; Yoast kann über offizielle Filter integriert werden, darf aber keine Pflichtabhängigkeit des Core werden.
- Kein Bildzwang.
- Kein Auto-Publish.
- Keine große Textmaschine im Core.

## Modulklasse

Formal noch `UNGEKLÄRT / ZIEL ALLGEMEINGÜLTIG`.

Grund:
Allgemeingültigkeit ist erst bewiesen, wenn derselbe Core ohne Codeänderung mit mindestens einer zweiten fachlich anderen Projektkonfiguration funktioniert.

## Kritische Entscheidung

Aktuell **keine parallele Pluginentwicklung**.

Begründung:
Die Trennung `Core + Projektkonfiguration` reicht konzeptionell aus. Eine zweite Codebasis würde unnötige Wartung und Versionsdrift erzeugen.

Falls eine spätere zweite Portalprüfung echte unkonfigurierbare Fachabhängigkeiten zeigt:
- Core bleibt neutral;
- projektspezifischer Adapter wird separat ergänzt;
- kein Fork des gesamten Plugins.

## Nächster technischer Schritt

Minimalen V1-Prototyp des neutralen Core definieren und isoliert gegen zwei Konfigurationen testen:
1. Pferde Atelier real;
2. fachlich neutrale Testkonfiguration ohne Pferdebegriffe.

Erst bei beiden PASS darf die Modulklasse auf ALLGEMEINGÜLTIG hochgestuft werden.
