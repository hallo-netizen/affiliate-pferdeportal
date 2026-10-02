import unittest
from engine.writer_contract_guard import (
    WriterContractBlocked, bind_receipt, verify_package
)

def words(n, seed):
    return " ".join([seed] * n)

def good_article():
    html = f"""<article>
<section data-block="intro"><p>{words(75,'Einleitung')}</p></section>
<section data-block="criteria"><h2>Kriterien sinnvoll einordnen</h2><p>{words(135,'Kriterium')}</p></section>
<section data-block="decision"><h2>Unterschiede im Zusammenhang betrachten</h2><p>{words(135,'Zusammenhang')}</p></section>
<section data-block="types"><h2>Passende Varianten unterscheiden</h2><p>{words(135,'Variante')}</p></section>
<section data-block="practical"><h2>Praxis verständlich zusammenführen</h2><p>{words(135,'Praxis')}</p></section>
<section data-block="table"><h2>Übersicht</h2><p>{words(30,'Tabelle')}</p></section>
<section data-block="conclusion"><h2>Fazit</h2><p>{words(88,'Fazitwort')}</p></section>
<section data-block="further_information"><h2>Weiterführende Informationen</h2><p>{words(38,'Hinweis')}</p></section>
</article>"""
    return {'article_id':'article:1234567890abcdef12345678','html':html}

class WriterContractGuardTests(unittest.TestCase):
    def test_good_writer_bound_article_passes(self):
        a=bind_receipt(good_article())
        m=verify_package(a)
        self.assertEqual(m['status'],'PASS')
        self.assertGreaterEqual(m['conclusion_ratio'],0.10)

    def test_direct_article_without_writer_receipt_is_blocked(self):
        with self.assertRaisesRegex(WriterContractBlocked,'WRITER_PROVENANCE_MISSING'):
            verify_package(good_article())

    def test_short_h2_sections_are_blocked_before_receipt(self):
        a=good_article()
        a['html']=a['html'].replace(words(135,'Kriterium'),words(35,'Kriterium'))
        a['html']=a['html'].replace(words(75,'Einleitung'),words(180,'Einleitung'))
        with self.assertRaisesRegex(WriterContractBlocked,'WRITER_H2_WORD_RANGE'):
            bind_receipt(a)

    def test_short_conclusion_is_blocked_before_receipt(self):
        a=good_article()
        a['html']=a['html'].replace(words(88,'Fazitwort'),words(20,'Fazitwort'))
        a['html']=a['html'].replace(words(75,'Einleitung'),words(150,'Einleitung'))
        with self.assertRaisesRegex(WriterContractBlocked,'WRITER_CONCLUSION_TOO_SHORT'):
            bind_receipt(a)

    def test_missing_further_information_is_blocked(self):
        a=good_article()
        start=a['html'].index('<section data-block="further_information">')
        end=a['html'].index('</section>',start)+len('</section>')
        a['html']=a['html'][:start]+a['html'][end:]
        with self.assertRaisesRegex(WriterContractBlocked,'WRITER_REQUIRED_SECTION_COUNT:further_information'):
            bind_receipt(a)

if __name__=='__main__':
    unittest.main()
