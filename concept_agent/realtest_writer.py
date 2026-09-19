from contracts import ArticleJob, Fact, Draft


class RealTestWriter:
    provider="concept-agent-realtest-writer"

    def run(self, job: ArticleJob, facts: list[Fact]) -> Draft:
        body=f"""# {job.title}

{job.keyword} lassen sich für unterschiedliche Trainingsaufgaben einsetzen. Die Auswahl sollte deshalb vom geplanten Einsatz ausgehen und nicht allein von Material oder Farbe.

## Einsatz und Training

{facts[0].statement}

{facts[1].statement}

Wer Stangen regelmäßig nutzt, sollte Aufbau und Schwierigkeit schrittweise an Pferd, Reiter und Trainingsziel anpassen. Sichtbarkeit, sichere Handhabung und ein passender Untergrund gehören dabei zur praktischen Auswahl.

## Auswahl im Überblick

[TABLE]

Kriterium | Worum es geht
Einsatz | Bodenarbeit, Cavaletti oder Springtraining
Handhabung | Gewicht, Transport und Lagerung
Sichtbarkeit | klare Erkennbarkeit im Training
Zustand | intakte Oberfläche und sichere Nutzung

## Weiterführende Bereiche

{job.internal_links[0]}
{job.internal_links[1]}
{job.internal_links[2]}

## Fazit

Passende Hindernisstangen für Pferde müssen zum konkreten Trainingszweck passen. Eine schrittweise Nutzung und die regelmäßige Kontrolle des Materials sind wichtiger als eine pauschale Empfehlung für eine einzige Ausführung.
"""
        return Draft(job.job_id,body)
