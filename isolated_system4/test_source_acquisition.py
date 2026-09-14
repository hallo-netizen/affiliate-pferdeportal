import copy,unittest

import source_acquisition as sa


def public_resolver(host,port,**kwargs):
    mapping={
        'a.example':['93.184.216.34'],
        'b.example':['151.101.1.69'],
        'c.example':['104.16.132.229'],
        'd.example':['8.8.8.8'],
        'dup.example':['1.1.1.1'],
        'private.example':['127.0.0.1'],
    }
    return [(2,1,6,'',(ip,port)) for ip in mapping.get(host,['93.184.216.34'])]


def response(items):
    return {'status_code':20000,'tasks':[{'status_code':20000,'result':[{'items':items}]}]}

def organic(url,title,rank,domain=None):
    return {'type':'organic','url':url,'title':title,'domain':domain or url.split('/')[2],'rank_absolute':rank,'rank_group':rank}

def page_fetch(url):
    text=('Fachlicher Quellentext zu Material Nutzung Sicherheit Pflege Eignung Vergleich Anwendung Praxis. '*12).encode()
    return 200,'text/html',b'<html><body><main>'+text+b'</main><script>ignore</script></body></html>',url


class SourceAcquisitionTests(unittest.TestCase):
    def test_positive_rank_order_dedupe_hash_and_projection(self):
        payload=response([
            organic('https://b.example/z','B',2),
            organic('https://a.example/a','A',1),
            organic('https://c.example/c','C',3),
            organic('https://dup.example/one','D1',4),
            organic('https://dup.example/two','D2',5),
        ])
        out=sa.acquire('Hindernisstangen für Pferde',login='x',password='y',serp_fetch=lambda *a:payload,page_fetch=page_fetch,resolver=public_resolver)
        self.assertEqual(out['contract'],sa.CONTRACT)
        self.assertEqual([r['source_title'] for r in out['sources'][:3]],['A','B','C'])
        self.assertEqual(len([r for r in out['sources'] if 'dup.example' in r['source_url']]),1)
        self.assertEqual(out['source_count'],len(out['sources']))
        self.assertEqual(len(sa.point0_sources(out)),out['source_count'])
        bad=copy.deepcopy(out);bad['sources'][0]['evidence']+='tamper'
        with self.assertRaisesRegex(sa.SourceAcquisitionError,'SOURCE_ACQUISITION_HASH_INVALID'):sa.point0_sources(bad)

    def test_own_private_and_nonorganic_are_not_bound(self):
        payload=response([
            organic('https://pferde-atelier.de/x','Own',1),
            organic('https://private.example/x','Private',2),
            {'type':'people_also_ask','url':'https://d.example/paa','title':'PAA','rank_absolute':3,'rank_group':3},
            organic('https://a.example/a','A',4),
            organic('https://b.example/b','B',5),
            organic('https://c.example/c','C',6),
        ])
        out=sa.acquire('Test',login='x',password='y',serp_fetch=lambda *a:payload,page_fetch=page_fetch,resolver=public_resolver)
        urls=[r['source_url'] for r in out['sources']]
        self.assertEqual(len(urls),3)
        self.assertFalse(any('pferde-atelier.de' in u or 'private.example' in u for u in urls))
        reasons=' '.join(row['reason'] for row in out['fetch_failures'])
        self.assertIn('SOURCE_URL_OWN_DOMAIN_BLOCKED',reasons)
        self.assertIn('SOURCE_URL_PRIVATE_ADDRESS_BLOCKED',reasons)

    def test_too_few_successful_sources_blocks(self):
        payload=response([organic('https://a.example/a','A',1),organic('https://b.example/b','B',2)])
        with self.assertRaisesRegex(sa.SourceAcquisitionError,'RESEARCH_SOURCE_POOL_INSUFFICIENT:2'):
            sa.acquire('Test',login='x',password='y',serp_fetch=lambda *a:payload,page_fetch=page_fetch,resolver=public_resolver)

    def test_bad_provider_status_blocks(self):
        with self.assertRaisesRegex(sa.SourceAcquisitionError,'DATAFORSEO_RESPONSE_NOT_OK'):
            sa.acquire('Test',login='x',password='y',serp_fetch=lambda *a:{'status_code':50000},page_fetch=page_fetch,resolver=public_resolver)

    def test_short_or_bad_content_cannot_count(self):
        payload=response([organic('https://a.example/a','A',1),organic('https://b.example/b','B',2),organic('https://c.example/c','C',3),organic('https://d.example/d','D',4)])
        def fetch(url):
            if 'a.example' in url:return 200,'text/html',b'<p>short</p>',url
            if 'b.example' in url:return 200,'application/pdf',b'x'*1000,url
            return page_fetch(url)
        with self.assertRaisesRegex(sa.SourceAcquisitionError,'RESEARCH_SOURCE_POOL_INSUFFICIENT:2'):
            sa.acquire('Test',login='x',password='y',serp_fetch=lambda *a:payload,page_fetch=fetch,resolver=public_resolver)

    def test_credentials_missing_on_real_provider_path(self):
        with self.assertRaisesRegex(sa.SourceAcquisitionError,'DATAFORSEO_CREDENTIALS_MISSING'):
            sa._default_serp_fetch('Test','','')

if __name__=='__main__':unittest.main(verbosity=2)
