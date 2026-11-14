# Pferdeatelier Texterstellung – Original-K0-/PPM-Platzbindung, Prüfung 14.11.2026

**Status:** Isolierte QA; **NICHT installieren; kein WordPress/K0-Live-Eingriff.** Verbindlicher Sollvertrag: [TEXTERSTELLUNG_KISS_ENDGUELTIGER_WORKFLOW_20261114.md](TEXTERSTELLUNG_KISS_ENDGUELTIGER_WORKFLOW_20261114.md).

## Nachgewiesener kritischer Fehler in vorheriger KISS-Testkopie
Eine neue externe MINI-FREI-Entscheidung erhielt über `TXE_Workshop::enqueue` zuvor automatisch eine selbst gebildete Artikel-ID `TXE-…` und einen daraus berechneten Planplatz. Der ursprüngliche K0-/PPM-6.7.9-Vertrag verlangt dagegen eine echte kanonische PPM-Artikel-ID aus dem bestehenden signierten PPM-Plan. Das lokale fünfteilige K0-Feldformat allein **belegt keine echte ursprüngliche PPM-Zuordnung**. Der alte Offline-20er-Test hatte die falsche Kompatibilität in einer simulierten PPM-freien Umgebung nicht bemerkt.

## Gezielte KISS-Sicherung am vorhandenen Code
- Nur die vorhandene `texterstellung.php` der bisherigen KISS-QA-Kopie geändert; keine neue Klasse, Tabelle, Worker, Fach-Entscheidung, K0-, PPM-, PSERC- oder WordPress-Core-Änderung.
- Ein neuer FREI-Auftrag erhält **keine lokal erfundene PPM-Artikel-ID und keinen PPM-Planplatz**. Die einmalige SEO-/Kategorie-/Titelentscheidung bleibt im bestehenden WP-Auftragsregal gespeichert; `METADATEN_OFFEN`, bis die echte technische Zuordnung vom ursprünglichen PPM/PSERC-Besitzer verfügbar ist.
- K0-Export und späterer WP-Entwurfsimport lesen nun `PSERC_Production_Reader::snapshot()` (den **vorhandenen signierten PPM-6.7.9-Kapazitätsleser**) und verlangen den unverändert passenden ursprünglichen `canonical_article_id`, K0-`plan_slot`, `category_slug`, `article_type` und eine für Entwürfe freigegebene Slot-Kapazität. **Das ist nur die technische Bindung, keine nachgelagerte SEO-/Inhaltsprüfung.**
- Die Kapazitätskontrolle verlangt zusätzlich den bereits vorhandenen originalen PSTE-FREI-/PPM-Vorbuchungsbeleg für exakt diesen Auftragsinhaber und verwirft eine von einem anderen Beitrag bereits belegte PPM-Planstelle. Die signierte Planliste allein genügt nicht als Buchungsnachweis.\n- Das bestehende eine Regal verhindert denselben gebuchten Platz für zwei unterschiedliche Aufträge. Alte selbst erfundene Kennungen dürfen nicht mehr nach K0 durchrutschen. Bei fehlendem signierten Originalplan wird der betroffene Auftrag sicher gehalten, nicht blind freigegeben. Es wird **keine alternative PPM-Reservierung** gebaut.

## Wirkliche lokale Tests
- **13/13** neue Quell-Gegenproben für originale PPM-Identität, gefälschte TXE-ID, ungültige/fehlende PPM-Signaturquelle und Erhalt des gespeicherten MINI-Ergebnisses nach einem blockierten Export.
- **14/14** echter 87-Fälle-Originaldaten-Replay: MINI-WordPress-Rückimport mit einem simulierten Abbruch nach neun persistierten Ergebnissen und unveränderte Wiederaufnahme (nicht echte externe GitHub/KI-Worker-Wiederaufnahme).
- **11/11** Sicherung der 61 ursprünglich freigegebenen Themen ohne erneute SEO-/Titelentscheidung.
- **6/6** Originalbestandskontrollen von **144 historischen PPM-Laufzeitzeilen** (09.11.2026): 144 eindeutige IDs; 128 `article:`-IDs und 16 ältere UUID-IDs, 99 Planplatzwerte gemäß aktueller PSERC-Formel und 45 abweichende historische. Die abweichenden alten Werte sind **kein** Beweis eines heutigen Serverfehlers, sondern dürfen nicht blind mit der aktuellen K0-Zuordnung verwechselt werden.
- Summe **44/44 neue Gegenproben**, **117/117** PHP-Syntaxprüfungen PASS. Quellen sind echte archivierte WordPress-/MINI-Daten und unveränderte originale PSTE/PSERC-PHP-Klassen; die WordPress-Datenbank, der echte laufende PPM-Platzbesitzer und der externe MINI-/K0-Schreibworker wurden **nicht** auf einem echten Server ausgeführt.

## Verifizierte Artefakte
Privates bestehendes Plugin-Büro:
`/pferdeatelier/PLUGINS/ARBEITSRAUM_PSTE_KISS/TEXTERSTELLUNG_KISS_PPM_BRUECKE_QA_20261114_NICHT_INSTALLIEREN.zip`
SHA256: `779e287d69878d1799db13dcfefbf48aee61269dc1a64faceb45f7767e153f98`. **Nach Library-Upload bytegleich zurückgelesen, ZIP-CRC PASS**, 180 Einträge; Root `QA_ONLY/`, deshalb kein installierbares WordPress-Plugin.
Bericht: `/pferdeatelier/PLUGINS/ARBEITSRAUM_PSTE_KISS/TEXTERSTELLUNG_KISS_PPM_BRUECKE_QA_BERICHT_20261114.md`. Das Paket enthält einen 153-Zeilen-Exaktdiff der vorhandenen Hauptdatei und sanitisierte Testergebnisse, **keine privaten Rohkeywords/Artikeltexte**.

## Erster belegter noch offener Blocker / Weiterarbeit
**Der echte, dauerhaft reservierte Original-PPM-Artikelplatz muss für jeden neuen MINI-FREI-Auftrag vom bestehenden PSERC/PPM-Slotbesitzer gebucht und bestätigt werden.** Die jetzige QA verhindert die falsche Eigenvergabe, kann eine fehlende Original-Reservierung aber nicht durch eine erfundene ersetzen. Der Original-PPM-6.7.9-Laufzeitbestand sowie WordPress-Verwaltungszugriff der isolierten Testinstallation sind in dieser Sitzung nicht zugänglich. Deshalb **kein echter WordPress-/K0-End-to-End-Test**, kein Beweis einer unterbrechungsfreien externen MINI-Workerkette, kein neues Installationspaket. Bereits erledigte SEO-/Titelentscheidungen dürfen bei einer Nachrüstung nicht neu bewertet werden.

**NEXT ACTION:** Am unveränderten bestehenden WordPress-Testportal die echte PPM-6.7.9-/PSERC-Platzreservierung für denselben freigegebenen Auftrag auslesen, nicht nachbauen; danach echten MINI→WP-Regal→K0→WP-Entwurf mit künstlichem Abbruch und Wiederanlauf testen. Solange diese zwei Belege fehlen: `release_allowed=false`.
