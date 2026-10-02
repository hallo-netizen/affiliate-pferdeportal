import hashlib
import unittest
from unittest.mock import patch

from engine import k0_production_gate as g


def sha(s):
    return hashlib.sha256(s.encode('utf-8')).hexdigest()


def portal(identity):
    return {
        'contract':'K0_PORTAL_ASSIGNMENT_V1',
        'status':'PASS',
        'items':[{
            'portal_id':'pferdeatelier',
            'portal_name':'Pferdeatelier',
            'status':'AUTO_DETECTED',
            'job_identity':identity,
        }],
    }


def package(identity, body, intent, table_exception='NUANCE_LOSS'):
    return {
        'contract':'K0_ARTICLE_PACKAGE_V1',
        'identity':identity,
        'html':body,
        'final_draft_sha256':sha(body),
        'content_profile':{'search_intent':intent},
        'table_decision':{'exception_code':table_exception},
        'publish_allowed':False,
    }


GOOD_SCHABRACKE = """<article data-article-type="FAQ">
<h2>Woher kommt das Wort Schabracke?</h2>
<p>Schabracke bezeichnet ursprünglich eine verzierte Sattel- oder Pferdedecke. Der Begriff wurde später auch übertragen verwendet.</p>
<h2>Wie entstand die abwertende Bedeutung?</h2>
<p>In der übertragenen Verwendung kann Schabracke abwertend für eine alte oder als unattraktiv bezeichnete Person sowie für eine abgenutzte Sache stehen.</p>
<h2>Ist alte Schabracke eine Beleidigung?</h2>
<p>Wird eine Person so bezeichnet, ist die Wendung salopp und abwertend. Der konkrete Ton hängt vom Zusammenhang ab.</p>
<h2>Was bedeutet das heute?</h2>
<p>Im Pferdesport bleibt Schabracke ein neutraler Fachbegriff. Die abwertende Redewendung und die sachliche Bezeichnung sollten klar getrennt werden.</p>
</article>"""

BAD_K9_SCHABRACKE = """<article data-article-type="FAQ">
<h2>Schabracken verständlich eingeordnet</h2>
<p>Für die Praxis heißt das: Betrachte ursprüngliche Bedeutung im konkreten Einsatz und vergleiche das Ergebnis anschließend mit den übrigen Anforderungen.</p>
<p>Betrachte übertragene Bedeutung gemeinsam mit Nutzung, Passform und den weiteren gebundenen Kriterien.</p>
<h2>Sattel im Alltag prüfen</h2>
<p>Beim nächsten Schritt steht abwertender Sprachgebrauch im Mittelpunkt. Trenne Muss-Kriterien von bloßen Zusatzmerkmalen.</p>
<h2>Ausrüstung praktisch kontrollieren</h2>
<p>Ein guter Vergleich beginnt mit einer klaren Reihenfolge. Die praktische Kontrolle sollte direkt am vorgesehenen Einsatz ansetzen.</p>
<h2>Sattel kompakt vergleichen</h2>
<p>Die Tabelle ordnet vier praktische Prüfpunkte knapp. Vor der Entscheidung lohnt sich eine bewusste Gewichtung von mögliche Wortherkunft.</p>
</article>"""


class TestK0SemanticGuard(unittest.TestCase):
    def setUp(self):
        self.identity={
            'article_type':'FAQ',
            'category':'magazin-unnuetzes-wissen',
            'plan_slot':'a554b0f86f23cda760d2a03f839934cbc4dda269d961ff891e763a684283352b',
            'target_keyword':'Warum sagt man du alte Schabracke',
            'title':'Warum sagt man du alte Schabracke?',
        }

    @patch('engine.k0_production_gate.verify_ppm', return_value={'status':'PASS','legacy_rule_count':104})
    def test_good_informational_faq_passes(self, _):
        r=g.verify(package(self.identity,GOOD_SCHABRACKE,'INFORMATIONAL_DIRECT_QUESTION'), portal(self.identity))
        self.assertEqual(r['status'],'PASS')
        self.assertEqual(r['semantic_intent_status'],'PASS')
        self.assertEqual(r['anti_boilerplate_status'],'PASS')

    def test_exact_k9_failure_family_is_blocked(self):
        with self.assertRaisesRegex(g.Blocked,'K0_TEMPLATE_BOILERPLATE_CONTAMINATION'):
            g.verify(package(self.identity,BAD_K9_SCHABRACKE,'INFORMATIONAL_DIRECT_QUESTION'), portal(self.identity))

    def test_faq_cannot_be_misbound_as_commercial_advice(self):
        with self.assertRaisesRegex(g.Blocked,'K0_SEARCH_INTENT_MISMATCH'):
            g.verify(package(self.identity,GOOD_SCHABRACKE,'DECISION_SUPPORT'), portal(self.identity))

    def test_informational_faq_decision_contamination_blocks_even_without_exact_fingerprint(self):
        body="""<article>
<h2>Herkunft</h2><p>Die Passform ist hier kein Thema.</p>
<h2>Bedeutung</h2><p>Vor der Entscheidung sollte der tatsächliche Bedarf geklärt werden.</p>
<h2>Gebrauch</h2><p>Die praktische Kontrolle am vorgesehenen Einsatz ist wichtig.</p>
<h2>Heute</h2><p>Die Wortbedeutung bleibt sprachlich zu erklären.</p>
</article>"""
        with self.assertRaisesRegex(g.Blocked,'K0_INFORMATIONAL_FAQ_DECISION_CONTAMINATION'):
            g.verify(package(self.identity,body,'INFORMATIONAL_DIRECT_QUESTION'), portal(self.identity))


if __name__=='__main__':
    unittest.main()
