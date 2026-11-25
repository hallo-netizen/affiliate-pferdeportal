# Hab & Bewahr – 20.11.2026, 17:57 – Dritter Recherchelauf: Echtdaten, aber 0 verwendbar

## Echte Quelle
Benutzer-Screenshot 17:57 Uhr und hochgeladene Diagnose `texterstellung-diagnose-20261120-165710.json` (16:57:10 UTC). Live installiert: **Texterstellung 0.4.31.12**. Effektiver DataForSEO-Modus `production`, Host `api.dataforseo.com`, Login und Passwort vorhanden. 2125 offene Kategorien, 3 recherchierte, 0 gesperrte/Fehler.

Neue abgeschlossene Recherche: `Alarm & Kamera ohne Netz: Häufige Fragen`, **100 Rohkeywords, 98 gespeicherte Kandidaten, 0 verwendbar**. Die 100 sichtbaren Rohkeywords stammen aus `KEYWORD_IDEA` und einem einzigen Anbieter-Antwortbeleg; keine Datenzeilen aus Suggestions, Related oder PAA im in der Diagnose dargestellten Rohkeywordbestand (das allein beweist noch keine API-Fehler).

Original-Familienfilter: 100 Eingaben, 99 Aliasgruppen, **99/99 `NO_MATCH`**. Die Gründe in allen 99 Gruppen: `PSTE_FAMILY_V2_REQUIRED_DISCRIMINATOR_MISSING` und `PSTE_FAMILY_V2_SUBJECT_HEAD_MISSING`. 98 gespeicherte Kandidaten `BLOCKED/SANDBOX_REQUIRED`; `PSTE_KEYWORD_IDEA_ORIGIN_FAMILY_NO_MATCH_NOT_USABLE` und Portalrelevanz nicht belegt. Reale Keywords sind teils allgemein oder fachfremd, etwa `ip kamera`, `nistkasten kamera`, `kamera für streaming`; `ip kamera ohne cloud` ist nicht automatisch dasselbe wie `ohne Netz`. **Keine Filterung lockern oder solche Daten als valide Artikel freigeben.**

## Nachweisbarer Unterschied der Original-ZIPs
Erneut direkt aus ZIP-Dateien geprüft:
- Pferdeatelier v0.4.39 `original/pste/includes/class-pste-breadth-research-queue.php::openFamilies()`: `seed = topic_family_name`, `family = topic_family_name`.
- Hobbydepot v0.4.24.17: dieselbe Bindung von Suchseed und Kategorie-Familie.
- Hab v0.4.31.12: absichtlich abweichende Sonderregel verwendet `portal_ancestor_page_names[2]` (R3) als **breiten** Seed, während `family = topic_family_name` der **engen C23** bleibt. Nur bei exakt bestimmter Produkt-Präfix-Bedingung wird der Seed gekürzt. Das nachgelagerte `PSTE_Family_Membership::evaluate(...,$familyKey)` prüft die Raw-Keywords ausschließlich gegen die enge C23-Familie, bevor sie als geeignet zählen. Für `Alarm & Kamera ohne Netz: Häufige Fragen` wurden 99/99 Gruppen als nicht zugehörig verworfen. Der präzise tatsächlich gespeicherte R3-Seed ist in der vorliegenden Diagnose **nicht enthalten** und darf nicht geraten werden.

**Ursache im Ablauf:** Die Hab-Sonderregel ermittelt die Suchbegriffe auf einer anderen Themenebene als die anschließende Passungsentscheidung. Dass sie bei dieser dritten Kategorie zu null geeigneten Kandidaten führt, ist durch 99/99 NO_MATCH direkt belegt. Kein Hinweis auf falschen DataForSEO-Host. Nicht mit einer bloßen Lockerung der Filter kaschieren. Zuerst eine einheitliche Such-/Zuordnungsebene festlegen und gegen echte C23-Struktur testen, einschließlich redaktioneller Anweisungen.

## Reset-Version 0.4.31.13 ist für den neuen Stand unvollständig
Das vorbereitete ZIP 0.4.31.13 setzt nur zwei **Sandbox**-Nullergebnisse `Abholbox ...` und `Abluftanlagen & Unterdruck` zurück. Der **dritte** später entstandene Produktions-Nullergebnis-Lauf wird davon nicht erfasst. **0.4.31.13 derzeit nicht als vollständige Lösung installieren.** Vor weiteren kostenpflichtigen Recherchen beide Fehlerklassen zusammen bearbeiten: die eigentliche breit/eng-Ursache mit Originalfunktionstest, anschließend einmalige sichere Wiederfreigabe aller drei nachgewiesenen Nullergebnisse unter unveränderter Historie.

## Nächster Schritt
Keine neuen kostenpflichtigen DataForSEO-Läufe. Kein weiterer Plugin-Zyklus nur für die Rücksetzung. Bündelreparatur erst nach nachgewiesenem funktionalen Abgleich mit dem Pferdeatelier und dem echten Hab-Strukturvertrag; keine Änderung am originalen K0. Eine reale WordPress- oder Provider-Abnahme wurde in dieser Analyse nicht durchgeführt.
