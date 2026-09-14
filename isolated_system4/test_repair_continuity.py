import contextlib,io,json,tempfile,unittest
from pathlib import Path
from unittest import mock

import batch_gate,controller
from live_route_test_support import start_to_context,valid_article


def write_text(path:Path,text:str)->Path:path.write_text(text,encoding='utf-8');return path

def run_main(argv):
    buf=io.StringIO()
    with contextlib.redirect_stdout(buf): rc=controller.main(argv)
    return rc,buf.getvalue()

def production_pass(state):
    d=state['draft_sha256']
    return {'contract':'SYSTEM4_FULL_PRODUCTION_CHECK_V1','status':'PASS','checked_draft_sha256':d,'publish_allowed':False,'evidence':{'no_legacy':{'status':'PASS','legacy_import_count':0},'no_external_links':{'status':'PASS','external_link_count':0},'languagetool':{'status':'PASS','engine':'LanguageTool 6.8 / Bestand 43','finding_count':0},'ppm679':{'status':'PASS','ppm_version':'6.7.9','technical_status':'TECHNICAL_CHECK_OK','content_quality_status':'CONTENT_QUALITY_CHECK_OK','fail_closed_aggregate_status':'PASS','content_sha256':d,'language_evidence_source':'REAL_LT68_FULLCHECK_REUSED'}}}

def enter_repair(workspace:Path):
    repair=controller.production_checks.RepairRequired('languagetool',[{'error_code':'LANGUAGETOOL_FINDING','rule_id':'GERMAN_SPELLER_RULE'}])
    with mock.patch.object(controller.production_checks,'run_all',side_effect=repair):
        rc,_=run_main(['controller.py','fullcheck',str(workspace)])
    if rc!=3:raise AssertionError('REPAIR_PHASE_NOT_REACHED')

class RepairContinuityTests(unittest.TestCase):
    def test_repairable_languagetool_finding_stays_same_draft_flow(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);workspace,_,state=start_to_context(root,0);draft=write_text(root/'draft.html',valid_article(state,0,'basis'))
            self.assertEqual(run_main(['controller.py','draft',str(workspace),str(draft)])[0],0)
            repair=controller.production_checks.RepairRequired('languagetool',[{'error_code':'LANGUAGETOOL_FINDING','rule_id':'GERMAN_SPELLER_RULE'}])
            def passed(repo,s,f,p):return production_pass(s)
            with mock.patch.object(controller.production_checks,'run_all',side_effect=[repair,passed(None,json.loads((workspace/'state.json').read_text()),None,None)]) as check:
                self.assertEqual(run_main(['controller.py','fullcheck',str(workspace)])[0],3)
                current=json.loads((workspace/'state.json').read_text());self.assertEqual(current['phase'],'REPAIR_REQUIRED');self.assertEqual(current['revision'],1)
                draft.write_text(valid_article(current,0,'korrigiert'),encoding='utf-8');self.assertEqual(run_main(['controller.py','repair',str(workspace),str(draft)])[0],0)
                check.side_effect=[production_pass(json.loads((workspace/'state.json').read_text()))]
                self.assertEqual(run_main(['controller.py','fullcheck',str(workspace)])[0],0)
            final=json.loads((workspace/'state.json').read_text());self.assertEqual(final['phase'],'OUTPUT_GATE_REQUIRED');self.assertEqual(final['revision'],2)

    def test_broad_repair_is_blocked(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);workspace,_,state=start_to_context(root,0);original=valid_article(state,0,'basis');draft=write_text(root/'draft.html',original);self.assertEqual(run_main(['controller.py','draft',str(workspace),str(draft)])[0],0);enter_repair(workspace)
            broad=original+'<section><p>'+('Vollständig neuer Ersatzinhalt mit fremdem Aufbau und anderer Aussage. '*200)+'</p></section>'
            draft.write_text(broad,encoding='utf-8');rc,out=run_main(['controller.py','repair',str(workspace),str(draft)]);self.assertEqual(rc,2);self.assertIn('REPAIR_SCOPE_FAIL:REPAIR_SCOPE_TOO_LARGE',out)

    def test_design_change_in_repair_is_blocked_not_normalized(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);workspace,_,state=start_to_context(root,0);draft=write_text(root/'draft.html',valid_article(state,0,'basis'));self.assertEqual(run_main(['controller.py','draft',str(workspace),str(draft)])[0],0);enter_repair(workspace)
            current=json.loads((workspace/'state.json').read_text());changed=valid_article(current,0,'korrigiert').replace('system-129-table comparison-table','comparison-table');draft.write_text(changed,encoding='utf-8');rc,out=run_main(['controller.py','repair',str(workspace),str(draft)]);self.assertEqual(rc,2);self.assertIn('ARTICLE_DESIGN_GUARD_FAIL:DESIGN_TABLE_SYSTEM129_CLASS_MISSING',out);self.assertIn('class="comparison-table"',draft.read_text())

    def test_real_tool_failure_remains_hard_fail_closed(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);workspace,_,state=start_to_context(root,0);draft=write_text(root/'draft.html',valid_article(state,0));self.assertEqual(run_main(['controller.py','draft',str(workspace),str(draft)])[0],0)
            hard=controller.production_checks.ProductionCheckError('LANGUAGETOOL_REAL_EXECUTION_FAILED')
            with mock.patch.object(controller.production_checks,'run_all',side_effect=hard):rc,out=run_main(['controller.py','fullcheck',str(workspace)])
            self.assertEqual(rc,2);self.assertIn('FULL_CHECK_HARD_BLOCK:LANGUAGETOOL_REAL_EXECUTION_FAILED',out);final=json.loads((workspace/'state.json').read_text());self.assertEqual(final['phase'],'CHECK_REQUIRED');self.assertNotEqual(final.get('checks',{}).get('status'),'PASS')

    def test_seven_item_batch_repairs_only_failed_item_and_collects_once(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);paths=[];snapshot_path=None;calls={}
            def fake_run_all(repo,state,fact_pack,plan):
                slot=state['article']['plan_slot'];count=calls.get(slot,0)+1;calls[slot]=count
                if state['article']['title']=='Mistcontainer mit Deckel wählen' and count==1:raise controller.production_checks.RepairRequired('languagetool',[{'error_code':'LANGUAGETOOL_FINDING','rule_id':'GERMAN_SPELLER_RULE'}])
                return production_pass(state)
            with mock.patch.object(controller.production_checks,'run_all',side_effect=fake_run_all) as check:
                for index in range(7):
                    workspace,snapshot,state=start_to_context(root,index);snapshot_path=snapshot;draft=write_text(root/f'draft-{index}.html',valid_article(state,index,'basis'));self.assertEqual(run_main(['controller.py','draft',str(workspace),str(draft)])[0],0);rc,_=run_main(['controller.py','fullcheck',str(workspace)])
                    if rc==3:
                        current=json.loads((workspace/'state.json').read_text());draft.write_text(valid_article(current,index,'korrigiert'),encoding='utf-8');self.assertEqual(run_main(['controller.py','repair',str(workspace),str(draft)])[0],0);self.assertEqual(run_main(['controller.py','fullcheck',str(workspace)])[0],0)
                    else:self.assertEqual(rc,0)
                    paths.append(workspace/'state.json')
                self.assertEqual(check.call_count,8)
            revisions=[json.loads(p.read_text())['revision'] for p in paths];self.assertEqual(revisions,[1,1,2,1,1,1,1]);out=root/'batch';result=batch_gate.collect_batch(snapshot_path,paths,out);self.assertEqual(result['status'],'SYSTEM4_BATCH_FULL_PASS_COLLECTED');self.assertEqual(result['article_count'],7);self.assertFalse(result['publish_allowed'])

if __name__=='__main__':unittest.main(verbosity=2)
