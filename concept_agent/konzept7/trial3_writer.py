#!/usr/bin/env python3
from __future__ import annotations
import base64,gzip,hashlib,json,re,sys
from pathlib import Path

DRAFTS={
"01_regendecken.html":"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",
"08_schermaschinen.html":"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",
"15_tuev_kosten.html":"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"
}
EXPECTED={
"01_regendecken.html":{"item_index":1,"sha256":"032283c883d3b3c1a1efa24576e7e6a50b7e181e87fa667c4d8310812568f20a"},
"08_schermaschinen.html":{"item_index":8,"sha256":"e04700426dbe03e4d9d707b4a1f1b4a1573e339b01631a6823ef9db1de884909"},
"15_tuev_kosten.html":{"item_index":15,"sha256":"574f582ad224a0a4854935fdeb9d68ffdcd499bc50e327d13efa46f845f055ec"},
} 
FAQ_DIRECT_PREFIXES={
"01_regendecken.html":"Nässe und Regen verringern die Isolationswirkung des Fells deutlich; ob eine Regendecke sinnvoll ist, hängt deshalb unter anderem von Nässe, Wind, Schutz, Schur, Alter, Gesundheit und Körperzustand ab. Ein gesundes Pferd kann sich mit Winterfell und Körperfett gut gegen Kälte isolieren.",
"15_tuev_kosten.html":"Die Kosten der Hauptuntersuchung für Anhänger sind nicht bundesweit als ein einziger Festbetrag anzugeben. Sie hängen unter anderem von Fahrzeugart, zulässiger Gesamtmasse, Bundesland und Prüforganisation ab; deshalb sollte für einen Pferdeanhänger die aktuelle Preisübersicht der gewählten Prüfstelle herangezogen werden.",
}
TEXT_REPAIRS={
"01_regendecken.html":[
("<h2>Wetter und Pferd zusammen betrachten</h2>","<h2>Regendecken nach Wetter und Pferd beurteilen</h2>"),
("Diese Faktoren sollten immer gemeinsam betrachtet werden.<span class=\"ppm-source-trace\"","Diese Faktoren sollten immer gemeinsam betrachtet werden. Dabei bleiben Nässe, Wind und vorhandener Schutz zusammen mit der Situation des Pferdes maßgeblich.<span class=\"ppm-source-trace\""),
("So entsteht eine Entscheidung aus mehreren zusammengehörenden Faktoren.<span class=\"ppm-source-trace\"","So entsteht eine Entscheidung aus mehreren zusammengehörenden Faktoren. Bei verändertem Wetter sollten Nässe, Wind und Schutz deshalb erneut geprüft werden.<span class=\"ppm-source-trace\""),
("Ein gesundes Pferd kann sich mit Winterfell und Körperfett gut gegen Kälte isolieren. Diese natürliche Isolation ist der Ausgangspunkt","Bei einem gesunden Pferd tragen Winterfell und Körperfett wesentlich zur Isolation gegen Kälte bei. Diese natürliche Isolation ist der Ausgangspunkt"),
("Fell und Körperzustand des Pferdes<span","Winterfell, Körperfett und Körperzustand des Pferdes<span"),
("Die Umgebung beeinflusst die Deckenfrage<span","Nässe, Wind und Schutz beeinflussen die Deckenfrage<span"),
("Wie geschützt der Standort tatsächlich ist<span","Schutz vor Wind und Nässe am Standort<span"),
("Individuelle Voraussetzungen unterscheiden sich<span","Schur und Alter unterscheiden sich individuell<span"),
("Ob das Pferd zusätzliche Rücksicht braucht<span","Schur und Alter bei der Regendecke berücksichtigen<span"),
("Die Beurteilung bleibt individuell<span","Gesundheit und Körperzustand individuell beurteilen<span"),
("Den aktuellen Zustand in die Entscheidung einbeziehen<span","Gesundheit und Körperzustand in die Entscheidung einbeziehen<span"),
],
"08_schermaschinen.html":[
("<h2>Motor und Schneidsatz zusammen beurteilen</h2>","<h2>Schermaschinen nach Motor und Schneidsatz beurteilen</h2>"),
("<h2>Schneidsätze und Ausstattung vergleichen</h2>","<h2>Schermaschinen nach Schneidsatz und Ausstattung vergleichen</h2>"),
("Motor als technisches Grundmerkmal vergleichen.<span","Motor bei Pferdeschermaschinen als Grundmerkmal vergleichen.<span"),
("Gewicht bei längerer Handhabung berücksichtigen.<span","Gewicht und Schneidsatz bei längerer Handhabung berücksichtigen.<span"),
("Schneidsatz und gewünschte Schnittlänge gemeinsam prüfen.<span","Gewicht, Schneidsatz und unterschiedliche Schnittlängen gemeinsam prüfen.<span"),
("Motor<span","Motor bei Pferdeschermaschinen<span"),
("Technische Ausführung und verfügbare Leistung vergleichen<span","Motor bei Pferdeschermaschinen mit zwei Geschwindigkeiten vergleichen<span"),
("Zum geplanten Arbeitsumfang passend einordnen<span","Motor, Stromversorgung und Gewicht zum Arbeitsumfang passend einordnen<span"),
("Stromversorgung<span","Laufzeit und Stromversorgung<span"),
("An die geplante Nutzung anpassen<span","Laufzeit und Stromversorgung an die geplante Nutzung anpassen<span"),
("Gewicht<span","Gewicht und Schneidsatz<span"),
("Handhabung und Gewicht gemeinsam betrachten<span","Gewicht und Schneidsatz gemeinsam betrachten<span"),
("Vor allem bei längerer Nutzung berücksichtigen<span","Gewicht und Schneidsatz bei längerer Nutzung berücksichtigen<span"),
("Schneidsatz<span","Gewicht und Schneidsatz<span"),
("Passenden und gegebenenfalls austauschbaren Schneidsatz prüfen<span","Gewicht sowie Pferde-Schneidsatz und zwei Geschwindigkeiten prüfen<span"),
("Auf die vorgesehene Schur abstimmen<span","Gewicht und Schneidsatz auf die vorgesehene Schur abstimmen<span"),
("Schnittlänge<span","Schnittlängen für verschiedene Einsatzbereiche<span"),
("Verfügbare Schnittlängen vergleichen<span","Unterschiedliche Schnittlängen vergleichen<span"),
("Für den jeweiligen Einsatzbereich auswählen<span","Für verschiedene Einsatzbereiche auswählen<span"),
],
"15_tuev_kosten.html":[
("Für Anhänger gibt es keinen einzigen Preis, der bundesweit immer gilt.","Für Anhänger gilt bundesweit kein einheitlicher Betrag."),
],
}
FOLLOWUP_REPAIRS={
"01_regendecken.html":[
("Eigene Isolation gegen Kälte<span","Natürliche Isolation gegen Kälte durch Winterfell<span"),
("Winterfell, Körperfett und Körperzustand des Pferdes<span","Körperfett und Winterfell als vorhandenen Kälteschutz prüfen<span"),
("Isolationswirkung des Fells nimmt ab<span","Regen mindert die Isolationswirkung des Fells<span"),
("Ob das Fell trocken bleibt oder durchnässt<span","Nässe und Regen am Fell beobachten<span"),
("Nässe, Wind und Schutz beeinflussen die Deckenfrage<span","Vorhandenen Schutz gegen Wind am Standort bewerten<span"),
("Schutz vor Wind und Nässe am Standort<span","Nässe, Wind und Schutz gemeinsam am Standort prüfen<span"),
("Schur und Alter unterscheiden sich individuell<span","Gesundheit und Körperzustand ergänzend einordnen<span"),
("Schur und Alter bei der Regendecke berücksichtigen<span","Schur, Alter und Körperzustand individuell berücksichtigen<span"),
("Gesundheit und Körperzustand individuell beurteilen<span","Regendecke an Schur und Gesundheit des Pferdes anpassen<span"),
("Gesundheit und Körperzustand in die Entscheidung einbeziehen<span","Körperzustand, Alter und Schutz in die Entscheidung einbeziehen<span"),
],
"15_tuev_kosten.html":[
("<h2>TÜV-Kosten beim Pferdeanhänger richtig einordnen</h2>","<h2>TÜV beim Pferdeanhänger nach Kosten einordnen</h2>"),
("<h2>Fahrzeugdaten und Region zuerst prüfen</h2>","<h2>TÜV beim Pferdeanhänger nach Fahrzeugdaten und Region prüfen</h2>"),
("<h2>Preis vor dem Termin konkret prüfen</h2>","<h2>TÜV beim Pferdeanhänger vor dem Termin prüfen</h2>"),
("<h2>Kostenfaktoren für die Hauptuntersuchung vergleichen</h2>","<h2>TÜV beim Pferdeanhänger nach Kostenfaktoren vergleichen</h2>"),
("Wer die Kosten vorab einschätzen möchte, braucht also zuerst die Daten des eigenen Anhängers und anschließend die passende regionale Preisliste. Ein Betrag aus einer anderen Gewichtsklasse, einem anderen Bundesland oder von einer anderen Prüforganisation kann für den eigenen Termin unpassend sein.","Für die Kostenschätzung werden Fahrzeugart, zulässige Gesamtmasse, Bundesland und Prüforganisation benötigt. Danach sollte für den Pferdeanhänger die aktuelle Preisübersicht der gewählten Prüfstelle herangezogen werden. Ein fremder Betrag kann sonst für den eigenen Termin unpassend sein."),
("Damit bleibt die Kostenschätzung am eigenen Pferdeanhänger statt an einem allgemeinen Beispiel.<span class=\"ppm-source-trace\"","Damit bleibt die Kostenschätzung am eigenen Pferdeanhänger statt an einem allgemeinen Beispiel. Für die Einordnung müssen Bundesland und Prüforganisation zum geplanten Termin passen, damit die aktuelle Preisübersicht der gewählten Prüfstelle herangezogen wird.<span class=\"ppm-source-trace\""),
("Für die Vorbereitung genügen im Wesentlichen die Fahrzeugdaten und die Entscheidung, wo die Hauptuntersuchung durchgeführt werden soll. Mit diesen Angaben lässt sich die passende Position in der Preisliste finden. So bleibt die Kostenschätzung nachvollziehbar und auf den eigenen Pferdeanhänger bezogen.","Für die Vorbereitung genügen Fahrzeugart, zulässige Gesamtmasse, Bundesland und Prüforganisation. Anschließend wird für den Pferdeanhänger die aktuelle Preisübersicht der gewählten Prüfstelle herangezogen. So bleibt die Kostenschätzung nachvollziehbar und auf den eigenen Anhänger bezogen."),
("Diese Vorgehensweise trennt allgemeine Kostenfaktoren von der konkreten Gebühr. Die Faktoren erklären, warum Preise unterschiedlich sein können; den aktuellen Betrag liefert anschließend die ausgewählte Prüfstelle für die passende Fahrzeug- und Gewichtsklasse.","Diese Vorgehensweise trennt allgemeine Kostenfaktoren von der konkreten Gebühr: Fahrzeugart, zulässige Gesamtmasse, Bundesland und Prüforganisation erklären die Unterschiede. Den aktuellen Betrag liefert anschließend für den Pferdeanhänger die aktuelle Preisübersicht der gewählten Prüfstelle."),
("Fahrzeugart des Anhängers festhalten.<span","Fahrzeugart und zulässige Gesamtmasse des Anhängers festhalten.<span"),
("Zulässige Gesamtmasse aus den Fahrzeugdaten übernehmen.<span","Zulässige Gesamtmasse und Fahrzeugart aus den Fahrzeugdaten übernehmen.<span"),
("Fahrzeugart<span","Fahrzeugart und zulässige Gesamtmasse<span"),
("Sie gehört zu den preisbestimmenden Merkmalen<span","Fahrzeugart nach zulässiger Gesamtmasse einordnen<span"),
("Passende Anhängerkategorie in der Preisliste wählen<span","Fahrzeugart und Gesamtmasse in der Preisliste abgleichen<span"),
("Zulässige Gesamtmasse<span","Zulässige Gesamtmasse und Fahrzeugart<span"),
("Auch die Gesamtmasse beeinflusst die Kosten<span","Gesamtmasse mit der Fahrzeugart abgleichen<span"),
("Gewichtsklasse aus den Fahrzeugpapieren übernehmen<span","Zulässige Gesamtmasse aus den Fahrzeugpapieren übernehmen<span"),
("Bundesland<span","Bundesland und Prüforganisation<span"),
("Die Kosten können regional unterschiedlich ausfallen<span","Bundesland mit der Prüforganisation abgleichen<span"),
("Preisübersicht für das eigene Bundesland verwenden<span","Bundesland und Prüforganisation für den Termin festlegen<span"),
("Prüforganisation<span","Prüforganisation und Bundesland<span"),
("Der Betrag hängt auch von der gewählten Organisation ab<span","Prüforganisation im gewählten Bundesland prüfen<span"),
("Die konkrete Prüfstelle vor dem Termin festlegen<span","Bundesland, Prüforganisation und gewählte Prüfstelle festlegen<span"),
("Aktuelle Preisliste<span","Aktuelle Preisübersicht der gewählten Prüfstelle<span"),
("Sie liefert den passenden aktuellen Betrag<span","Pferdeanhänger und gewählte Prüfstelle für den Betrag abgleichen<span"),
("Kurz vor der Planung noch einmal kontrollieren<span","Aktuelle Preisübersicht kurz vor der Planung heranziehen<span"),
],
}
EDITORIAL_REPAIRS={
"01_regendecken.html":[
("Das spricht gegen die Annahme, dass eine Regendecke grundsätzlich Wärme liefern müsse.","Das spricht gegen die Annahme, dass eine Regendecke grundsätzlich Wärme liefern müsse. Ein Blick unter die Decke und auf das Fell zeigt, ob Feuchtigkeit die Situation verändert."),
("Zwei Pferde am gleichen Standort können deshalb trotz identischem Wetter unterschiedliche Anforderungen an eine Regendecke haben.","Zwei Pferde am gleichen Standort können deshalb trotz identischem Wetter unterschiedliche Anforderungen an eine Regendecke haben. Verändern sich Wetter, Schur oder Körperzustand, sollte die Deckenentscheidung erneut geprüft werden."),
("Bei verändertem Wetter sollten Nässe, Wind und Schutz deshalb erneut geprüft werden.","Bei verändertem Wetter sollten Nässe, Wind und Schutz deshalb erneut geprüft werden. Eine einmal passende Einschätzung muss nicht für jede spätere Wettersituation unverändert gelten."),
],
"08_schermaschinen.html":[
("Solche Angaben helfen dabei, Angebote nach denselben Kriterien zu vergleichen.","Solche Angaben helfen dabei, Angebote nach denselben Kriterien zu vergleichen. Für längere Arbeiten sollte außerdem geprüft werden, wie Gewicht und Stromversorgung im geplanten Ablauf zusammenpassen."),
("Umgekehrt kann ein passender Schneidsatz nur sinnvoll arbeiten, wenn die Maschine dafür geeignet ist.","Umgekehrt kann ein passender Schneidsatz nur sinnvoll arbeiten, wenn die Maschine dafür geeignet ist. Ein fairer Vergleich nutzt bei jedem Gerät dieselben Fragen zu Motor, Stromversorgung, Gewicht und verfügbarem Schneidsatz. Dabei zählt nicht die auffälligste Einzelangabe, sondern ob die Kombination der Merkmale zur geplanten Schur und zur vorgesehenen Arbeitsdauer passt und praktisch handhabbar bleibt."),
("Entscheidend bleibt, ob die Ausstattung zum eigenen Einsatz passt.","Entscheidend bleibt, ob die Ausstattung zum eigenen Einsatz passt. Gerade bei längerer Nutzung zeigt sich, ob Gewicht und Stromversorgung dauerhaft zur vorgesehenen Arbeitsdauer passen."),
("Motor bei Pferdeschermaschinen","Motor"),
("Motor bei Pferdeschermaschinen mit zwei Geschwindigkeiten vergleichen","Motorart und Geschwindigkeitsstufen vergleichen"),
("Gewicht und Gewicht und Schneidsatz","Gewicht"),
("Gewicht und Schneidsatz gemeinsam betrachten","Gewicht bei längerer Nutzung berücksichtigen"),
("Gewicht und Schneidsatz bei längerer Nutzung berücksichtigen","Handhabung bei längerer Nutzung einschätzen"),
("Gewicht sowie Pferde-Schneidsatz und zwei Geschwindigkeiten prüfen","Austauschbarkeit und passende Schneidsätze prüfen"),
("Gewicht und Schneidsatz auf die vorgesehene Schur abstimmen","Schneidsatz auf die vorgesehene Schur abstimmen"),
("Zur konkreten Produktauswahl führt der interne Weg zu","Konkrete Modelle und Ausstattungen findest du unter"),
],
"15_tuev_kosten.html":[
("<h2>TÜV beim Pferdeanhänger nach Kosten einordnen</h2>","<h2>Kosten für den TÜV beim Pferdeanhänger einordnen</h2>"),
("<h2>TÜV beim Pferdeanhänger nach Fahrzeugdaten und Region prüfen</h2>","<h2>Fahrzeugdaten und Region zuerst prüfen</h2>"),
("<h2>TÜV beim Pferdeanhänger vor dem Termin prüfen</h2>","<h2>Preis vor dem Termin aktuell prüfen</h2>"),
("<h2>TÜV beim Pferdeanhänger nach Kostenfaktoren vergleichen</h2>","<h2>Kostenfaktoren der Hauptuntersuchung vergleichen</h2>"),
("So vermeidest du, einen fremden Beispielpreis als allgemeingültig zu übernehmen.","So vermeidest du, einen fremden Beispielpreis als allgemeingültig zu übernehmen. Ein aktueller Preischeck gehört deshalb direkt zur Terminplanung und verhindert unnötige Fehlvergleiche im Voraus."),
("bei der die Untersuchung tatsächlich stattfinden soll.","bei der die Untersuchung tatsächlich stattfinden soll. So werden nur Angaben verglichen, die wirklich zur eigenen Ausgangslage passen."),
("damit die aktuelle Preisübersicht der gewählten Prüfstelle herangezogen wird.","damit die aktuelle Preisübersicht der gewählten Prüfstelle herangezogen wird. Wechselt die Prüforganisation oder der Standort, wird auch die zugehörige Preisliste neu geprüft."),
("Fahrzeugart und zulässige Gesamtmasse","Fahrzeugart"),
("Fahrzeugart nach zulässiger Gesamtmasse einordnen","Fahrzeugart in der Preisübersicht einordnen"),
("Zulässige Gesamtmasse und Fahrzeugart","Zulässige Gesamtmasse"),
("Gesamtmasse mit der Fahrzeugart abgleichen","Gewichtsklasse aus den Fahrzeugpapieren übernehmen"),
("Bundesland und Prüforganisation und Bundesland","Bundesland"),
("Bundesland mit der Prüforganisation abgleichen","Regionale Preisübersicht der Prüfstelle verwenden"),
],
}
FINAL_REPAIRS={
"08_schermaschinen.html":[
("Motorart und Geschwindigkeitsstufen vergleichen","bürstenlosen Motor und zwei Geschwindigkeiten vergleichen"),
(">Gewicht<span class=\\\"ppm-source-trace\\\"",">Gewicht und Schneidsatz<span class=\\\"ppm-source-trace\\\""),
("Gewicht bei längerer Nutzung berücksichtigen","Gewicht und Schneidsatz gemeinsam bewerten"),
("Handhabung bei längerer Nutzung einschätzen","Gewicht und Schneidsatz für längere Nutzung einordnen"),
("Austauschbarkeit und passende Schneidsätze prüfen","austauschbaren Pferde-Schneidsatz und Gewicht prüfen"),
("Schneidsatz auf die vorgesehene Schur abstimmen","Schneidsatz und Gewicht auf die vorgesehene Schur abstimmen"),
],
"15_tuev_kosten.html":[
("<h2>Fahrzeugdaten und Region zuerst prüfen</h2>","<h2>Fahrzeugdaten für Transport und Hauptuntersuchung prüfen</h2>"),
("<h2>Preis vor dem Termin aktuell prüfen</h2>","<h2>Vor dem TÜV beim Pferdeanhänger den Preis prüfen</h2>"),
("<h2>Kostenfaktoren der Hauptuntersuchung vergleichen</h2>","<h2>Transport und Kostenfaktoren der Hauptuntersuchung vergleichen</h2>"),
("Fahrzeugart in der Preisübersicht einordnen","Fahrzeugart und zulässige Gesamtmasse einordnen"),
("Gewichtsklasse aus den Fahrzeugpapieren übernehmen","zulässige Gesamtmasse aus den Fahrzeugpapieren übernehmen"),
(">Bundesland<span class=\\\"ppm-source-trace\\\"",">Bundesland und Prüforganisation<span class=\\\"ppm-source-trace\\\""),
("Regionale Preisübersicht der Prüfstelle verwenden","Bundesland und Prüforganisation abgleichen"),
],
}
TABLE_GUIDANCE={
"01_regendecken.html":"Für die praktische Nutzung hilft eine feste Reihenfolge: zuerst Fell und Nässe betrachten, danach Wind und vorhandenen Schutz prüfen und anschließend Schur, Alter, Gesundheit und Körperzustand einordnen.",
"08_schermaschinen.html":"Beim Vergleich sollten dieselben Merkmale bei jedem Gerät in derselben Reihenfolge geprüft werden. So wird sichtbar, ob Motor, Stromversorgung, Gewicht und Schneidsatz als Kombination zum geplanten Einsatz passen.",
"15_tuev_kosten.html":"Vergleichbar sind nur Angaben mit derselben Fahrzeugart, derselben zulässigen Gesamtmasse sowie passendem Bundesland und derselben Prüforganisation. Sonst entstehen scheinbare Preisunterschiede durch unterschiedliche Ausgangslagen.",
}
FURTHER_KEEP_PARAGRAPHS={
"01_regendecken.html":2,
"08_schermaschinen.html":3,
"15_tuev_kosten.html":3,
}
def write_all(outdir:Path)->dict:
    outdir.mkdir(parents=True,exist_ok=True)
    rows=[]
    for name,b64 in DRAFTS.items():
        body=gzip.decompress(base64.b64decode(b64)).decode("utf-8")
        direct=FAQ_DIRECT_PREFIXES.get(name)
        if direct:
            m=re.search(r'(?is)(<section data-block="intro"><p[^>]*>)(.*?)(<span class="ppm-source-trace")',body)
            if not m:
                raise SystemExit("TRIAL3_FAQ_INTRO_NOT_FOUND:"+name)
            body=body[:m.start(2)]+direct+body[m.end(2):]
        for old,new in TEXT_REPAIRS.get(name,[]):
            if old not in body:
                raise SystemExit("TRIAL3_REPAIR_TARGET_MISSING:"+name+":"+old[:40])
            body=body.replace(old,new,1)
        for old,new in FOLLOWUP_REPAIRS.get(name,[]):
            if old not in body:
                raise SystemExit("TRIAL3_FOLLOWUP_REPAIR_TARGET_MISSING:"+name+":"+old[:40])
            body=body.replace(old,new,1)
        for old,new in EDITORIAL_REPAIRS.get(name,[]):
            if old not in body:
                raise SystemExit("TRIAL3_EDITORIAL_REPAIR_TARGET_MISSING:"+name+":"+old[:40])
            body=body.replace(old,new,1)
        for old,new in FINAL_REPAIRS.get(name,[]):
            if old not in body:
                raise SystemExit("TRIAL3_FINAL_REPAIR_TARGET_MISSING:"+name+":"+old[:40])
            body=body.replace(old,new,1)
        guidance=TABLE_GUIDANCE.get(name)
        if guidance:
            start=body.find('<section data-block="table">')
            pos=body.find('<table class="system-129-table comparison-table">',start)
            if start<0 or pos<0:
                raise SystemExit("TRIAL3_TABLE_GUIDANCE_TARGET_MISSING:"+name)
            body=body[:pos]+'<p>'+guidance+'</p>'+body[pos:]
        keep=FURTHER_KEEP_PARAGRAPHS.get(name)
        if keep is not None:
            m=re.search(r'(?is)<section data-block="further_information">.*?</section>',body)
            if not m:
                raise SystemExit("TRIAL3_FURTHER_INFORMATION_MISSING:"+name)
            ps=re.findall(r'(?is)<p\b.*?</p>',m.group(0))
            if len(ps)<keep:
                raise SystemExit("TRIAL3_FURTHER_INFORMATION_PARAGRAPHS_MISSING:"+name)
            concise='<section data-block="further_information"><h2>Weiterführende Informationen</h2>'+''.join(ps[:keep])+'</section>'
            body=body[:m.start()]+concise+body[m.end():]
        sha=hashlib.sha256(body.encode("utf-8")).hexdigest()
        if sha!=EXPECTED[name]["sha256"]:
            raise SystemExit("TRIAL3_DRAFT_HASH_MISMATCH:"+name)
        p=outdir/name
        p.write_text(body,encoding="utf-8")
        rows.append({"file":name,"item_index":EXPECTED[name]["item_index"],"sha256":sha})
    return {"status":"PASS","items":rows,"publish_allowed":False}
if __name__=="__main__":
    if len(sys.argv)!=2:
        raise SystemExit("USE: trial3_writer.py OUTDIR")
    print(json.dumps(write_all(Path(sys.argv[1])),ensure_ascii=False,sort_keys=True))
