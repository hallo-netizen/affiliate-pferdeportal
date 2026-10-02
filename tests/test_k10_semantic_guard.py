import unittest
from engine.checkers import editorial_receipts


def status(article, rule_id):
    rows=editorial_receipts(article)
    hit=[r for r in rows if r['rule_id']==rule_id]
    assert len(hit)==1, (rule_id,hit)
    return hit[0]


def article(body,title='Warum sagt man du alte Schabracke?'):
    return {
      'article_id':'k10-semantic-guard-test',
      'article_type':'FAQ',
      'title':title,
      'target_keyword':'Warum sagt man du alte Schabracke',
      'heading_intent_terms':['Schabracke','Bedeutung','Herkunft','Gebrauch'],
      'html':body,
    }


GOOD="""<article>
<section data-block="intro"><p>Die Redewendung alte Schabracke ist salopp und abwertend, während Schabracke im Pferdesport ein neutraler Fachbegriff bleibt.</p></section>
<section data-block="answer"><h2>Woher kommt das Wort Schabracke?</h2><p>Der Begriff bezeichnet ursprünglich eine Pferde- oder Satteldecke und wurde später zusätzlich übertragen verwendet.</p></section>
<section data-block="details"><h2>Wie entstand die abwertende Bedeutung?</h2><p>Die übertragene Verwendung kann Personen oder alte, abgenutzte Dinge abwertend bezeichnen.</p></section>
<section data-block="checklist"><h2>Was bedeutet der Ausdruck heute?</h2><p>Im heutigen Sprachgebrauch hängt die Wirkung vom Zusammenhang ab; als Personenbezeichnung ist die Wendung nicht neutral.</p></section>
<section data-block="conclusion"><h2>Fazit</h2><p>Sachbegriff und Schimpfwort sollten klar getrennt werden.</p></section>
<section data-block="further_information"><h2>Weiterführende Informationen</h2><p>Weitere Sprachgeschichte lässt sich über Wörterbuchquellen nachvollziehen.</p></section>
</article>"""

BAD="""<article>
<section data-block="intro"><p>Die Wendung ist abwertend gemeint.</p></section>
<section data-block="answer"><h2>Schabracken verständlich eingeordnet</h2><p>Für die Praxis heißt das: Betrachte ursprüngliche Bedeutung im konkreten Einsatz und vergleiche das Ergebnis anschließend mit den übrigen Anforderungen.</p></section>
<section data-block="details"><h2>Sattel im Alltag prüfen</h2><p>Trenne Muss-Kriterien von bloßen Zusatzmerkmalen und beachte die Passform.</p></section>
<section data-block="checklist"><h2>Ausrüstung praktisch kontrollieren</h2><p>Ein guter Vergleich beginnt mit einer klaren Reihenfolge und der praktischen Kontrolle am vorgesehenen Einsatz.</p></section>
<section data-block="table"><h2>Sattel kompakt vergleichen</h2><p>Die Tabelle ordnet vier praktische Prüfpunkte knapp.</p></section>
<section data-block="conclusion"><h2>Fazit</h2><p>Der letzte Schritt ist die praktische Kontrolle am konkreten Fall.</p></section>
</article>"""


class K10SemanticGuardTests(unittest.TestCase):
    def test_old_k9_schabracke_family_is_blocked(self):
        r=status(article(BAD),'surface.non_template_language')
        self.assertEqual(r['status'],'FAIL')

    def test_clean_informational_faq_is_not_blocked_by_semantic_guard(self):
        r=status(article(GOOD),'surface.non_template_language')
        self.assertEqual(r['status'],'PASS')

    def test_decision_support_faq_is_not_misclassified_as_direct_info(self):
        body=GOOD.replace('Schabracke','Magnetfelddecke')
        r=status(article(body,'Welche Magnetfelddecke ist besser geeignet?'),'surface.non_template_language')
        self.assertEqual(r['status'],'PASS')


if __name__=='__main__':
    unittest.main()
