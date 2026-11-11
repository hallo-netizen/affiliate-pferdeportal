# Pferdeatelier eBay – QA21: echter Checkpoint-Abgleich und gespeicherte Kandidaten

**Stand 11.11.2026. Ausschließlich Beweis-/Codeprüfung, keine Plugin- oder Liveänderung.**

## 1. Echte Run-Ereignisse und Ursache der schrumpfenden Freigabeliste

Originaldatei: `pferdeatelier-ebay-lauf-alle.csv`, 1990 Zeilen. Beim selben echten Run `09c34988-7c9f-4090-945c-fdcff6b3393e`:

| Ereignis | Phase | öffentlich zugelassene Kampagnen | abgedeckte Familien |
|---|---|---:|---:|
| 1417 | gapfill_select | 493 | 147/298 |
| 1481 | public_verify | 365 | 161/298 |

**Differenz:** -128 Kampagnen in der finalen Freigabeliste, +14 abgedeckte Familien. Beide Werte **aus den realen CSV-Ereignissen**, keine Prognose.

Der echte QA19-Code `includes/trait-ppar-ebay-run.php` führt beim normalen vollständigen Auswahlabschnitt in `ebay_run_checkpoint_business_ids_from_selection` ausdrücklich `$ids = array()` aus; die anschließende Abschlussmethode `ebay_run_commit_public_checkpoint` schreibt die Kampagnen-IDs des **neu errechneten Auswahlkandidaten** als neue gesamte öffentliche Liste. Dagegen fügt `ebay_public_checkpoint_add_verified_business_ids` im Zwischenschritt nur geprüfte IDs hinzu. Damit ist die **Art der Veränderung (früh addieren, am Schluss komplett ersetzen)** im Code belegt, nicht nur gemutmaßt.

Die eigentlichen Quellen werden beim bloßen Überschreiben der öffentlichen Freigabeliste **nicht gelöscht**. Nach dem finalen Commit versetzt `ebay_selection_prune_business_batch` nicht mehr ausgewählte Bestandsquellen kontrolliert auf Reserve oder Kandidat durch `ebay_business_pause_output_for_capacity`. **Das sind unterschiedliche Stufen**. Ob die 128 kampagnenweise fachlich korrekt herausfielen, ist **nicht belegt**, weil das CSV nur Summen, keine 493er/365er Kampagnen-IDs liefert. Keine Änderung der bewussten Drei-Produkt-Auswahlgrenze pro Warenfamilie ohne tatsächliche Evidenz.

## 2. Wieso einzelne Seiten weiterhin ohne sichtbare Kacheln sein können

Der vorhandene Ausgabefilter erfordert **beides**: (a) Kampagne steht im zuletzt gespeicherten öffentlichen Checkpoint und (b) ihre Quelle ist weiterhin fachlich erlaubt und frisch. Dadurch können gespeicherte Angebote und öffentlich gezeigte Angebote auseinanderfallen. **Welches Gate auf der konkreten Schabracken-Seite greift, ist ohne echten WP-Bestand nicht belegbar**. Ohne nachgewiesene Datenlage deshalb **kein** Eingriff in die SAFE-/Frischeprüfung.

## 3. Alte 138er Auswertung mit QA18/QA19 abgeglichen

Der QA10-Datensatz enthält 55 untersuchungswürdige Altfamilien. Von diesen sind mit QA18 genau **3** zu redaktionellen Themen statt eBay-Pflichtwaren geworden: **Waschplatz für Pferde, Reithallenbau, Heulagerung**. Bei den 39 alten ausschließlich fremdmarktplatzgefilterten Familien sind es weitere genau **3**: **Mistlagerung, Offenstallbau, Satteltransport**. Die alte QA10-Fokusliste ist damit **52 statt 55** für die damalige Teilmenge, ohne diese Gruppen pauschal freizugeben. Von den übrigen 9 redaktionellen Ausschlüssen fehlt die sichere Zuordnung zum aktuellen 137er Zustand; daraus **keine fiktive 137-15-Rechnung** machen. Die damaligen 43 Nulltreffer sind weiterhin nur Nulltreffer eines **begrenzten** Suchausschnitts.

## 4. Was jetzt wirklich fehlt

**Kein weiterer Programmfix auf Verdacht.** Auf der getrennten WordPress-Kopie muss genau einmal die **bereits gespeicherte Auswahl** mit dem **QA19-Klassifikator** und den **tatsächlichen Anzeigen** abgeglichen werden. Für alle ausgeschlossenen Kampagnen muss das bestehende Programm zeigen, **welche Kampagnen-IDs** nicht mehr ausgewählt sind und warum (abgelaufen / schlechte Produktidentität / Auswahlgrenze / fehlende Freigabe / fehlende Frische). Bereits gespeicherte Quellen nicht löschen oder vollständig erneut recherchieren. Nur danach eine falsche Ablehnung in derselben einen Klassifikation oder Ausgabe korrigieren.

**Harte Grenze:** Aus den 1990 echten Auditzeilen folgt nicht, dass QA19 live installiert wurde; QA19 ist bisher Patch/Teststand. Kein Zugriff auf die privaten WordPress-/MariaDB-Datensätze in dieser Prüfung, kein Freigabenvergleich einzelner Kampagnen, keine echte eBay-API-Prüfung und **keine Live-Freigabe**. Kein Release, keine neue ZIP, kein ungefragter Neustart.