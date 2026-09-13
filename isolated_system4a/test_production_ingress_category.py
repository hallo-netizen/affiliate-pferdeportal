import hashlib
import json
import tempfile
import unittest
import zipfile
from pathlib import Path

from production_ingress import bind_external_snapshot, ProductionIngressError, REPO


def stable(v):
    return hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def canonical_slot():
    package=REPO/'control/startmaster0107/runtime_packages/PORTAL_PRODUCTION_MACHINE_V6.7.9_SIGNED_ARTICLE_TYPE_EXTENSION_ROOTFIX_FINAL.zip'
    with zipfile.ZipFile(package) as z:
        plan=json.loads(z.read('portal-production-machine/contracts/canonical-complete-editorial-plan-v1.json'))
    hits=[s for s in plan['slots'] if s.get('canonical_article_id')=='article:fe39320b47c1ba40194c8d69']
    assert len(hits)==1
    return hits[0]


class ProductionIngressCategoryTests(unittest.TestCase):
    def payload(self, category='checklisten-fuer-pferdeanhaenger-beratung', *, title=None, plan_slot=None):
        slot=canonical_slot()
        title=title or slot['working_title']
        plan_slot=plan_slot or stable(slot)
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
                    'plan_slot':plan_slot,
                    'target_keyword':'Checklisten für Pferdeanhänger',
                    'title':title,
                }],
                'publish_allowed':False,
            },
        }

    def run_payload(self, payload):
        with tempfile.TemporaryDirectory(prefix='s4a-ingress-cat-', dir='/tmp') as td:
            root=Path(td); root.chmod(0o755)
            inp=root/'input.json'; inp.write_text(json.dumps(payload,ensure_ascii=False,sort_keys=True,separators=(',',':')),encoding='utf-8')
            return bind_external_snapshot(inp, root/'authority')

    def test_positive_canonical_beratung_category_and_slot_pass_ingress(self):
        out=self.run_payload(self.payload())
        self.assertEqual(len(out.system4_manifest_sha256),64)

    def test_negative_last_real_noncanonical_category_blocks_before_research(self):
        with self.assertRaisesRegex(ProductionIngressError, '^PPM679_CATEGORY_NOT_CANONICAL:pferdeanhaenger-beratung$'):
            self.run_payload(self.payload('pferdeanhaenger-beratung'))

    def test_negative_arbitrary_64hex_plan_slot_blocks_against_canonical_slot(self):
        expected=stable(canonical_slot())
        with self.assertRaisesRegex(ProductionIngressError, '^PPM679_PLAN_SLOT_HASH_MISMATCH:'+expected+':'+('f'*64)+'$'):
            self.run_payload(self.payload(plan_slot='f'*64))

    def test_negative_noncanonical_title_cannot_resolve_slot(self):
        with self.assertRaisesRegex(ProductionIngressError, '^PPM679_CANONICAL_PLAN_SLOT_NOT_UNIQUE:'):
            self.run_payload(self.payload(title='Checklisten für Pferdeanhänger auswählen die wichtigsten Entscheidungskriterien'))

if __name__=='__main__': unittest.main(verbosity=2)
