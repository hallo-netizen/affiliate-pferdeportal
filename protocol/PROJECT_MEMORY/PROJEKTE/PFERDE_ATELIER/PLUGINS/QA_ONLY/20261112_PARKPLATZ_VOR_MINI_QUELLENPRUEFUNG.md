> **WICHTIGE KORREKTUR 12.11.2026 – VORHERIGE SCHLUSSFOLGERUNG ZURÜCKGENOMMEN:** Dieser Prüfbericht betrachtete nur den **ersten Rohkeyword-Export** (`selectNewRows/createBatch`) und behauptete daraus fälschlich, Kategorie, Artikelart und Suchintention seien im gesamten MINI-/PSTE-/PSERC-Übergabeweg nicht mitgegeben bzw. verlorengegangen. Das ist **NICHT belegt und in dieser Allgemeinheit falsch**. Der bestehende zweite MINI-Export (`exportResults` mit `include_parkhaus`) transportiert den umfangreichen `parkhaus_snapshot`; darin enthaltene PSTE-, PSERC- und WP-Planzeilen führen **`category`/`category_slug`, `article_type`, `intent_profile` und Beleg-/Planplätze**. Originaler PSERC-Gesamtplan vom 10.11.2026 enthält für alle drei READY-Aufträge Kategorie/Artikelart, getrennte `intent_profile` und signierten `plan_slot` und reicht die fünf Metadatenfelder nachweislich weiter. **Die Funktionen `selectNewRows` und `exportResults` sind in sieben physischen PSTE-ZIPs .40 bis .46 jeweils identisch**, es ist in diesem Versionsfenster KEIN Rückbau dieser Übergabefelder belegt. Die historische Begründung für Änderungen vor .40 ist hier nicht untersucht. Die ursprüngliche Schlussfolgerung `MISSING_EARLY_CATEGORY_TYPE_BINDING_CONFIRMED` bitte NICHT als behebungsbedürftige Ursache verwenden. Was separat noch geprüft werden müsste: Ob die konkrete **fertige Artikelplatz-Reservierung vor MINI** gewollt und vorhanden ist; ein `intent_slot` ist nicht automatisch `plan_slot`. **Keine neue Pluginänderung aus dem zurückgenommenen Befund ableiten.**

# Vorverlegung der Artikelplatz-Reservierung – harte Quellenprüfung am finalen QA-Paket

**Stand 12.11.2026.** Keine WordPress-Änderung und **keine neue Plugin-ZIP**. Originale QA-ZIPs geprüft: PSTE 0.57.144.46 `e3461e7bdf8a30eb30f16e445e02499dafaebb496171f53900c068564682352c`, PSERC 0.28.70 `0367fad3be41ac2a79e37397fb9b9e39f787956a887413c951b30f1dc2125c1a`.

## Quelle und eindeutiger Befund
1. PSTE `includes/class-pste-mini-workflow.php`, `selectNewRows` (Zeilen 332ff.): **MINI-Erstausgabe überträgt nur** `id`, `pool_key`, `raw_query`, `source_sha256`, `decision`, `titles`. Es werden auch schon im gespeicherten Themenpool vorhandene Kategorie- oder Artikeltypangaben **nicht** in diese erste Ausgabe übernommen. `createBatch` gibt genau diese Felder an die externen Worker.
2. Der endgültige K0-`plan_slot` ist allein ein Token aus der unveränderlichen `canonical_article_id` (`PSERC_Plan_Slot_Identity`). Die tatsächliche Zuteilung geschieht in `PSERC_Plan_Compile_Job::tickSlot` (Zeilen 217–223), **nach der externen MINI-Bearbeitung**.
3. Derselbe bestehende, nicht geänderte `PSERC_Slot_Allocator::allocate` benötigt für die konkrete Belegung `category_slug` und `article_type`, damit er nur Plätze der richtigen Fachkategorie/Artikelart verwendet. **Kein Titel erforderlich.**
4. `intent_slot` des MINI-SEO-Receipts ist eine eigenständige Kennung der inhaltlichen Suchabsicht; **nicht** die spätere `plan_slot`-Kennung. Vorab-Reservierung darf nicht durch ein Umetikettieren von `intent_slot` vorgetäuscht werden.

## Echte PHP-Gegenproben an den frisch ausgepackten finalen ZIP-Klassen
- Original-PSTE-Methode `PSTE_Mini_Workflow::selectNewRows` mit zwei unterschiedlichen gespeicherten Ausgangszeilen: **PASS**. Beide Erstausgaben enthalten keinerlei endgültige Artikelplatzkennung oder `category_slug`/`article_type`, **selbst wenn die Quelldaten diese Kategorie/Art bereits besitzen**.
- Original-`PSERC_Slot_Allocator::allocate` mit einer klar definierten Testkategorie und zwei bestehenden signierten Kapazitätsplätzen: **3/3 PASS**:
  - Nur rohes Keyword ohne Kategorie/Art -> kein Platz, Status `HELD_UNSUPPORTED_ARTICLE_TYPE`.
  - Dasselbe Keyword mit schon feststehender Kategorie/Art -> genau erster freier Artikelplatz 12, ohne Titel.
  - Platz 12 vorher belegt -> deterministisch Platz 13.
- Die bisherigen fünf Original-PHP-Gegenproben von QA-.46/.70 gegen unveränderte ZIP-Extraktion erneut erfolgreich.
- Diese Daten sind **lokale Testbeispiele**, keine Behauptung über den aktuell gespeicherten kompletten 5.016er-WordPress-Bestand.

## Wichtig für den vorhandenen verbindlichen Parkplatzvertrag
Eine endgültige physische Reservierung von Artikelplatz 12 **vor MINI** ist im aktuellen ersten Exportvertrag nicht möglich, ohne vorher die **bereits autoritativ bestimmten** Kategorie und Artikelart zu binden. Einen Platz blind aus *irgendeiner* Kategorie zu nehmen, würde die schon belegten Fachplätze falsch vergeben und das KISS-Konzept verletzen.

**Es ist KEIN Problem der späteren Titelbearbeitung:** Sobald Kategorie/Artikelart zuverlässig vorliegen, kann der **vorhandene** PSERC-Allocator die technische Vergabe ohne Titel bereits durchführen. Es fehlt im tatsächlichen MINI-Ausgangsvertrag die Anbindung der beiden nötigen Angaben samt bestehendem zentralem Eigentümer. Das ist die konkret identifizierte strukturelle Lücke; **keine neue semantische Prüfstufe darf improvisiert werden**.

### Sicherer Umsetzungsweg an bestehenden Teilen
1. Für die **bereits vom vorgesehenen Eigentümer klassifizierten** Themen vor MINI `category_slug` und `article_type` als unveränderte Originalfelder mitgeben; nicht aus Titeln oder SEO-Absicht neu raten. Bei unklassifizierten Rohkeywords muss dieselbe *bereits vorhandene* zuständige Kategorie-/Artikelartbestimmung erst abgeschlossen sein. Keine zweite Einstufung im PSERC.
2. **Einmal** den bestehenden technischen PSERC-Allocator gegen den vollständigen vorhandenen Plan laufen lassen; die so eindeutig zugeteilte `canonical_article_id` als **reservierten Auftrag** in der vorhandenen Produktionsstatus-Ablage festhalten, nicht in einer neuen Tabelle.
3. Bei MINI-Rückkehr unverändert denselben Platz dem bereits einmal entschiedenen Keyword zuordnen, ohne zweite Vergabe/semantische Kontrolle. K0 erhält den daraus abgeleiteten `plan_slot` wie bisher.
4. Nach WordPress-Import PPM-Platz auf erledigt setzen; bei Abbruch Auftrag/Status sichtbar halten, nicht erneut zuweisen.
5. Vor einer tatsächlichen Neu-ZIP diesen vorhandenen Eingangsvertrag plus kategorielose Fälle mit der realen MINI/PSERC/PPM-Schnittstelle durchlaufen. **Die bestehende Testseite ist schon vorhanden.**

**Abnahmestatus:** MISSING_EARLY_CATEGORY_TYPE_BINDING_CONFIRMED. EARLY_PHYSICAL_SLOT_RESERVATION_NOT_IMPLEMENTED. NO_RELEASE. Die bereits installierten Plugins, die frühere .46/.70 QA und K0 nicht verändern.
