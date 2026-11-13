# Pferdeatelier: Erledigte bekannte MINI-Fehlerstelle – nur ein vorhandener Codepfad

**13.11.2026 | Ausschließlich QA, NICHT installieren.**

## Verbindlicher Ausgangsstand
`PFERDEATELIER_KISS_KEINE_NACHGELAGERTE_THEMENPRUEFUNG_NUR_QA_20261113.zip`, SHA-256 `8e7b032c9e56d37a95700afe0e8c043c387510a4e055b0970f7bd36671887193`, 216 Einträge. Im Arbeitsarchiv bleiben beide Original-Plugins unverändert. Erzeugtes neues Archiv: `PFERDEATELIER_KISS_MINI_NUR_TITEL_VORAB_FREIGABE_QA_20261113.zip`, SHA-256 `489ca173ea7be9e5c88cdbfc8ef9f8182575ad04a0c6e893aa754a5432111439`, 216 Einträge.

**Nur eine einzige vorhandene Quell-PHP-Datei geändert:** `arbeit/Portal SEO Topic Engine/includes/class-pste-mini-workflow.php`. Kein neuer Worker, keine neue Option oder Tabelle, keine weitere fachliche Prüfung, kein WordPress-Frontend-Code.

## Ursprüngliche, seit Tagen feststehende Ursache
Das Original ließ MINI neue Rohkeywords inklusive `Worker 1 entscheidet JA/NEIN/VIELLEICHT` bearbeiten. Der externe einzige SEO-Bescheid ließ sich als `FREI` nur nach einem schon von MINI geschriebenen Titel speichern. Dieser Zirkel erzwang die falsche Reihenfolge.

## Konkrete KISS-Korrektur
1. Der vorhandene externe SEO-Import akzeptiert die endgültige Freigabe jetzt **ohne** vorgängigen MINI-Titel. Die Originalfrage kommt bindend aus der bestehenden WordPress-Themenpool-Zeile; Quelle, Eigentümer, Parkhaus-Vollständigkeit, Doppelung und belegte Suchabsicht bleiben geprüft. Der Bescheid liegt **in derselben bisherigen WordPress-Option**.
2. Die vorhandene MINI-Exportfunktion wählt **nur** bereits endgültig freigegebene, noch nicht betitelte Themen und stellt **einen** Titelauftrag pro freigegebenem Thema. Die Freigabe und Suchabsicht sind eingefroren. **Kein Ja/Nein/Vielleicht-Worker** wird für neue Stapel erzeugt.
3. Der vorhandene MINI-Import darf ausschließlich diesen einen Titel ergänzen. Veränderte Suchabsicht, Freigabe, Dokument-ID oder alte Quelle werden abgewiesen; die bereits bestehende Freigabe wird nur mit dem Titel vervollständigt. Dieselbe bestehende atomare WordPress-Option-Speicherung wird weiterverwendet.
4. Die bestehende Verwaltungsoberfläche führt **eine** eindeutige Reihenfolge vor: einmaliger SEO-Entscheid → Titelauftrag → Redaktionsplan. Frühere, noch offene Ja/Nein-Stapel werden nicht erneut ausgegeben und lassen sich über den **bestehenden** Abbruchknopf beenden. Gespeicherte alte Freigaben bleiben kompatibel.

## Echte Gegenproben
- **22/22** direkter Original-PHP-Methodentest am neuen Titelweg: Freigabe vor MINI; Titel unverändert gesperrte Felder; Täuschungsversuche bei Freigabe, Intent, Identität und Slot abgewiesen; geänderte Datenbankfrage und doppelte Reservierung blockiert; Quittung nach Titel weiterhin lesbar.
- **159/159** gegen die **tatsächlichen gesicherten 87 SEO-Entscheidungen** vom 09.11., einschließlich 61 FREI, 20 BELEGT, 6 KLÄRUNG. Historischer Importvertrag unverändert kompatibel.
- **18/18** bisheriger Offline-Gesamtweg (WordPress, echte PPM-Schreibfunktion, MINI-Titel, K0-Texterstellung jeweils teils **simuliert**, keine reale Produktionsfreigabe).
- **126/126** PHP-Dateien syntaxfehlerfrei, ZIP-Prüfung vollständig, **215/216 Einträge byteidentisch** zum Ausgangsarchiv; genau die genannte MINI-PHP ist verändert.

## Weiterhin gesperrt / nicht vortäuschen
Der bestehende externe `intent_slot` ist eine **Suchabsichtsreservierung und nicht der feste `canonical_article_id` des Redaktionsplans**. Die endgültige technische Reservierung des **wirklichen Artikelplatzes vor MINI** ist in dieser Änderung **noch nicht vorhanden**. Deshalb das ZIP **nicht** auf WordPress installieren. Auch K0 und echter PPM-WordPress-Endlauf nicht produktiv getestet. Keine zusätzliche Architektur anlegen und keine Platzreservierung behaupten.