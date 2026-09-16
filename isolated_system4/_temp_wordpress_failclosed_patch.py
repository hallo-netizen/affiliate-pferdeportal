from pathlib import Path


def replace_once(path, old, new):
    p=Path(path); text=p.read_text(encoding='utf-8')
    count=text.count(old)
    if count!=1:
        raise SystemExit(f'{path}:EXPECTED_ONE_MATCH:GOT_{count}: {old[:120]!r}')
    p.write_text(text.replace(old,new,1),encoding='utf-8')

replace_once('isolated_system4/handoff_transport.py',
    "DIRECT_IMPORT_PLUGIN_VERSION='0.28.23'\n",
    "WORDPRESS_IMPORT_PLUGIN_BUILD='0.28.18-endstempel-import-envelope-binding-ppm679'\nWORDPRESS_DIRECT_BLOCK_REASON='REQUIRES_SIGNED_ENDSTEMPEL_PACKAGE_AND_PSERC_IMPORT_ENVELOPE'\nWORDPRESS_REQUIRED_DOWNSTREAM_COMPONENTS=('PSERC_APPROVED_PRODUCTION_PACKAGE_V1','PFERDE_ATELIER_ENDSTEMPEL_RELEASE_V1')\n\ndef wordpress_review() -> dict:\n    return {\n        'file_format':'JSON',\n        'mime_type':'application/json',\n        'intended_next_step':'WORDPRESS_PREIMPORT_REVIEW',\n        'plugin_name':'Portal SEO Editorial Plan Compiler',\n        'plugin_version_verified_against':WORDPRESS_IMPORT_PLUGIN_BUILD,\n        'ppm_version_verified_against':'6.7.9',\n        'direct_wordpress_upload_ready':False,\n        'direct_upload_block_reason':WORDPRESS_DIRECT_BLOCK_REASON,\n        'required_downstream_components':list(WORDPRESS_REQUIRED_DOWNSTREAM_COMPONENTS),\n    }\n")
replace_once('isolated_system4/handoff_transport.py',
    "    _require(wr['intended_next_step']=='WORDPRESS_DIRECT_IMPORT','HANDOFF_WORDPRESS_NEXT_STEP_INVALID')\n    _require(wr['plugin_name']=='Portal SEO Editorial Plan Compiler','HANDOFF_WORDPRESS_PLUGIN_INVALID')\n    _require(wr['plugin_version_verified_against']==DIRECT_IMPORT_PLUGIN_VERSION,'HANDOFF_WORDPRESS_PLUGIN_VERSION_INVALID')\n    _require(wr['ppm_version_verified_against']=='6.7.9','HANDOFF_WORDPRESS_PPM_VERSION_INVALID')\n    _require(wr['direct_wordpress_upload_ready'] is True,'HANDOFF_WORDPRESS_DIRECT_UPLOAD_REQUIRED')\n    _require(wr['direct_upload_block_reason'] is None,'HANDOFF_WORDPRESS_BLOCK_REASON_MUST_BE_EMPTY')\n    _require(wr['required_downstream_components']==[],'HANDOFF_WORDPRESS_DOWNSTREAM_MUST_BE_EMPTY')\n",
    "    _require(wr['intended_next_step']=='WORDPRESS_PREIMPORT_REVIEW','HANDOFF_WORDPRESS_NEXT_STEP_INVALID')\n    _require(wr['plugin_name']=='Portal SEO Editorial Plan Compiler','HANDOFF_WORDPRESS_PLUGIN_INVALID')\n    _require(wr['plugin_version_verified_against']==WORDPRESS_IMPORT_PLUGIN_BUILD,'HANDOFF_WORDPRESS_PLUGIN_VERSION_INVALID')\n    _require(wr['ppm_version_verified_against']=='6.7.9','HANDOFF_WORDPRESS_PPM_VERSION_INVALID')\n    _require(wr['direct_wordpress_upload_ready'] is False,'HANDOFF_WORDPRESS_DIRECT_UPLOAD_MUST_BE_BLOCKED')\n    _require(wr['direct_upload_block_reason']==WORDPRESS_DIRECT_BLOCK_REASON,'HANDOFF_WORDPRESS_BLOCK_REASON_INVALID')\n    _require(wr['required_downstream_components']==list(WORDPRESS_REQUIRED_DOWNSTREAM_COMPONENTS),'HANDOFF_WORDPRESS_DOWNSTREAM_INVALID')\n")

replace_once('isolated_system4/live_parity_v2.py',"from pathlib import Path\n\nHERE=Path(__file__).resolve().parent\n","from pathlib import Path\n\nimport handoff_transport\n\nHERE=Path(__file__).resolve().parent\n")
old_meta="'wordpress_review':{'file_format':'JSON','mime_type':'application/json','intended_next_step':'WORDPRESS_DIRECT_IMPORT','plugin_name':'Portal SEO Editorial Plan Compiler','plugin_version_verified_against':'0.28.23','ppm_version_verified_against':'6.7.9','direct_wordpress_upload_ready':True,'direct_upload_block_reason':None,'required_downstream_components':[]},'articles':rows"
replace_once('isolated_system4/live_parity_v2.py',old_meta,"'wordpress_review':handoff_transport.wordpress_review(),'articles':rows")
old_full="'wordpress_review':{'file_format':'JSON','mime_type':'application/json','intended_next_step':'WORDPRESS_DIRECT_IMPORT','plugin_name':'Portal SEO Editorial Plan Compiler','plugin_version_verified_against':handoff_transport.DIRECT_IMPORT_PLUGIN_VERSION,'ppm_version_verified_against':'6.7.9','direct_wordpress_upload_ready':True,'direct_upload_block_reason':None,'required_downstream_components':[]},'articles':["
replace_once('isolated_system4/full_local_acceptance.py',old_full,"'wordpress_review':handoff_transport.wordpress_review(),'articles':[")

old_local="""        'wordpress_review': {
            'file_format': 'JSON',
            'mime_type': 'application/json',
            'intended_next_step': 'WORDPRESS_DIRECT_IMPORT',
            'plugin_name': 'Portal SEO Editorial Plan Compiler',
            'plugin_version_verified_against': handoff_transport.DIRECT_IMPORT_PLUGIN_VERSION,
            'ppm_version_verified_against': '6.7.9',
            'direct_wordpress_upload_ready': True,
            'direct_upload_block_reason': None,
            'required_downstream_components': [],
        },
"""
replace_once('isolated_system4/test_local_end_to_end_chat_handoff.py',old_local,"        'wordpress_review': handoff_transport.wordpress_review(),\n")
replace_once('isolated_system4/test_local_end_to_end_chat_handoff.py',"            self.assertTrue(final_payload['wordpress_review']['direct_wordpress_upload_ready'])\n","            self.assertFalse(final_payload['wordpress_review']['direct_wordpress_upload_ready'])\n            self.assertEqual(final_payload['wordpress_review']['intended_next_step'], 'WORDPRESS_PREIMPORT_REVIEW')\n            self.assertEqual(final_payload['wordpress_review']['direct_upload_block_reason'], handoff_transport.WORDPRESS_DIRECT_BLOCK_REASON)\n")

old_test_meta="""            'wordpress_review':{
                'file_format':'JSON','mime_type':'application/json','intended_next_step':'WORDPRESS_DIRECT_IMPORT','plugin_name':'Portal SEO Editorial Plan Compiler',
                'plugin_version_verified_against':ht.DIRECT_IMPORT_PLUGIN_VERSION,'ppm_version_verified_against':'6.7.9','direct_wordpress_upload_ready':True,
                'direct_upload_block_reason':None,'required_downstream_components':[]
            },
"""
replace_once('isolated_system4/test_handoff_transport.py',old_test_meta,"            'wordpress_review':ht.wordpress_review(),\n")
old_tests="""    def test_negative_direct_upload_not_ready(self):
        p=self.payload(); p['wordpress_review']['direct_wordpress_upload_ready']=False
        with self.assertRaisesRegex(ht.HandoffError,'HANDOFF_WORDPRESS_DIRECT_UPLOAD_REQUIRED'): ht.validate_handoff(p)
    def test_negative_preimport_route(self):
        p=self.payload(); p['wordpress_review']['intended_next_step']='WORDPRESS_PREIMPORT_REVIEW'
        with self.assertRaisesRegex(ht.HandoffError,'HANDOFF_WORDPRESS_NEXT_STEP_INVALID'): ht.validate_handoff(p)
    def test_negative_block_reason_present(self):
        p=self.payload(); p['wordpress_review']['direct_upload_block_reason']='ANY_BLOCK'
        with self.assertRaisesRegex(ht.HandoffError,'HANDOFF_WORDPRESS_BLOCK_REASON_MUST_BE_EMPTY'): ht.validate_handoff(p)
    def test_negative_downstream_components_present(self):
        p=self.payload(); p['wordpress_review']['required_downstream_components']=['workflow_release']
        with self.assertRaisesRegex(ht.HandoffError,'HANDOFF_WORDPRESS_DOWNSTREAM_MUST_BE_EMPTY'): ht.validate_handoff(p)
"""
new_tests="""    def test_negative_false_direct_upload_ready(self):
        p=self.payload(); p['wordpress_review']['direct_wordpress_upload_ready']=True
        with self.assertRaisesRegex(ht.HandoffError,'HANDOFF_WORDPRESS_DIRECT_UPLOAD_MUST_BE_BLOCKED'): ht.validate_handoff(p)
    def test_negative_direct_import_route(self):
        p=self.payload(); p['wordpress_review']['intended_next_step']='WORDPRESS_DIRECT_IMPORT'
        with self.assertRaisesRegex(ht.HandoffError,'HANDOFF_WORDPRESS_NEXT_STEP_INVALID'): ht.validate_handoff(p)
    def test_negative_block_reason_missing(self):
        p=self.payload(); p['wordpress_review']['direct_upload_block_reason']=None
        with self.assertRaisesRegex(ht.HandoffError,'HANDOFF_WORDPRESS_BLOCK_REASON_INVALID'): ht.validate_handoff(p)
    def test_negative_downstream_components_missing(self):
        p=self.payload(); p['wordpress_review']['required_downstream_components']=[]
        with self.assertRaisesRegex(ht.HandoffError,'HANDOFF_WORDPRESS_DOWNSTREAM_INVALID'): ht.validate_handoff(p)
    def test_negative_fake_direct_import_plugin_version(self):
        p=self.payload(); p['wordpress_review']['plugin_version_verified_against']='0.28.23'
        with self.assertRaisesRegex(ht.HandoffError,'HANDOFF_WORDPRESS_PLUGIN_VERSION_INVALID'): ht.validate_handoff(p)
"""
replace_once('isolated_system4/test_handoff_transport.py',old_tests,new_tests)

old_print="          print('SYSTEM4_FRESH_1_AND_3_ROUTE_PASS_PENDING_WORDPRESS_CHAT')\n"
new_print="""          handoff=json.loads((root/'SYSTEM4_ARTICLE_BATCH_CHAT_HANDOFF_V2.json').read_text())
          wr=handoff['wordpress_review']
          assert wr['intended_next_step']=='WORDPRESS_PREIMPORT_REVIEW'
          assert wr['plugin_version_verified_against']=='0.28.18-endstempel-import-envelope-binding-ppm679'
          assert wr['direct_wordpress_upload_ready'] is False
          assert wr['direct_upload_block_reason']=='REQUIRES_SIGNED_ENDSTEMPEL_PACKAGE_AND_PSERC_IMPORT_ENVELOPE'
          assert wr['required_downstream_components']==['PSERC_APPROVED_PRODUCTION_PACKAGE_V1','PFERDE_ATELIER_ENDSTEMPEL_RELEASE_V1']
          importer=Path('/tmp/system4-wordpress-import-contract.txt').read_text()
          assert '0.28.18-endstempel-import-envelope-binding-ppm679' in importer
          assert "ENDSTAMP_CONTRACT='PFERDE_ATELIER_ENDSTEMPEL_RELEASE_V1'" in importer
          assert 'SYSTEM4_ARTICLE_BATCH_CHAT_HANDOFF_V2' not in importer
          print('SYSTEM4_FRESH_1_AND_3_ROUTE_PASS_WORDPRESS_DIRECT_IMPORT_BLOCK_PROVEN_CHAT_PENDING')
"""
replace_once('.github/workflows/system4a-real-acceptance.yml',old_print,new_print)

for path in [Path('isolated_system4/handoff_transport.py'),Path('isolated_system4/live_parity_v2.py'),Path('isolated_system4/full_local_acceptance.py'),Path('isolated_system4/test_local_end_to_end_chat_handoff.py')]:
    text=path.read_text(encoding='utf-8')
    if 'DIRECT_IMPORT_PLUGIN_VERSION' in text:
        raise SystemExit(f'STALE_DIRECT_IMPORT_VERSION:{path}')
    if "'direct_wordpress_upload_ready':True" in text or "'direct_wordpress_upload_ready': True" in text:
        raise SystemExit(f'STALE_DIRECT_IMPORT_READY:{path}')

print('SYSTEM4_WORDPRESS_FAILCLOSED_PATCH_READY')
