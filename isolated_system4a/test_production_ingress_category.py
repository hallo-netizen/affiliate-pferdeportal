import json
import tempfile
import unittest
from pathlib import Path

from production_ingress import bind_external_snapshot, ProductionIngressError


class ProductionIngressCategoryTests(unittest.TestCase):
    def payload(self, category):
        return {
            'contract':'SYSTEM4_WORDPRESS_LIVE_INPUT_FIXTURE_V1',
            'next_textmachine_metadata_batch':{
                'contract':'PSERC_TEXTMACHINE_METADATA_BATCH_V2',
                'status':'READY_FOR_TEXTMACHINE_METADATA_INTAKE',
                'batch_sha256':'b'*64,
                'item_count':1,
                'items':[{ 
                    'article_type':'Beratung',
                    'category':category,
                    'plan_slot':'a'*64,
                    'target_keyword':'Checklisten für Pferdeanhänger',
                    'title':'Checklisten für Pferdeanhänger auswählen die wichtigsten Entscheidungskriterien',
                }],
                'publish_allowed':False,
            },
        }

    def run_payload(self, payload):
        with tempfile.TemporaryDirectory(prefix='s4a-ingress-cat-', dir='/tmp') as td:
            root=Path(td); root.chmod(0o755)
            inp=root/'input.json'; inp.write_text(json.dumps(payload,ensure_ascii=False,sort_keys=True,separators=(',',':')),encoding='utf-8')
            return bind_external_snapshot(inp, root/'authority')

    def test_positive_canonical_beratung_category_passes_ingress(self):
        out=self.run_payload(self.payload('checklisten-fuer-pferdeanhaenger-beratung'))
        self.assertEqual(len(out.system4_manifest_sha256),64)

    def test_negative_last_real_noncanonical_category_blocks_before_research(self):
        with self.assertRaisesRegex(ProductionIngressError, '^PPM679_CATEGORY_NOT_CANONICAL:pferdeanhaenger-beratung$'):
            self.run_payload(self.payload('pferdeanhaenger-beratung'))


if __name__=='__main__': unittest.main(verbosity=2)
