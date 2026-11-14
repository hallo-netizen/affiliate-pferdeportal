from pathlib import Path
import json,subprocess
base=Path('/mnt/data/ebay_kiss_final')
orig=base/'qa/QA67_ORIGINAL_V346.php'
old_automation=''
import zipfile
with zipfile.ZipFile('/mnt/data/Affiliate_6.72.346_EBAY_GESAMTWORKFLOW_TEST.zip') as z:
    old_automation=z.read('affiliate-portal-router/includes/trait-ppar-automation-suite.php').decode()
new_automation=(base/'affiliate-portal-router/includes/trait-ppar-automation-suite.php').read_text()
start='    public function ensure_full_pool_automation() {'
end='    public function run_full_pool_automation_worker() {'
php_prefix='''<?php
error_reporting(E_ALL & ~E_DEPRECATED);
$GLOBALS['opts'] = [];
$GLOBALS['schedule'] = [];
function get_option($k,$default=null){return array_key_exists($k,$GLOBALS['opts'])?$GLOBALS['opts'][$k]:$default;}
function update_option($k,$v,$autoload=false){$GLOBALS['opts'][$k]=$v;return true;}
function delete_option($k){unset($GLOBALS['opts'][$k]);return true;}
function wp_schedule_single_event($time,$hook,$args=[]){$GLOBALS['schedule'][]=[$hook,$args];return true;}
function wp_next_scheduled($hook){foreach($GLOBALS['schedule'] as $x) if($x[0]===$hook)return true;return false;}
function wp_clear_scheduled_hook($hook){return 0;}
'''
php_class='''class POOLTEST {
const VERSION = '__VERSION__';
const OPTION_FULL_POOL_AUTOMATION_VERSION = 'pool_version';
const OPTION_FULL_POOL_AUTOMATION_CURSOR = 'pool_cursor';
const FULL_POOL_WORKER_HOOK = 'full_pool_cron';
const AUTOMATION_CRON_HOOK = 'partner_sync_cron';
__METHOD__
}
'''
php_test='''
$cases = [
 ['name'=>'upgrade_completed','opts'=>['pool_version'=>'6.72.345']],
 ['name'=>'upgrade_in_progress','opts'=>['pool_version'=>'running:6.72.346','pool_cursor'=>217]],
 ['name'=>'upgrade_old_cursor','opts'=>['pool_version'=>'6.72.345','pool_cursor'=>83]],
 ['name'=>'upgrade_no_previous_state','opts'=>[]],
 ['name'=>'already_current','opts'=>['pool_version'=>'__VERSION__']],
];
$out=[];
foreach($cases as $case){
 $GLOBALS['opts']=$case['opts'];$GLOBALS['schedule']=[];
 $o=new POOLTEST();$o->ensure_full_pool_automation();$first=['opts'=>$GLOBALS['opts'],'schedule'=>$GLOBALS['schedule']];
 $o->ensure_full_pool_automation();
 $out[]=['name'=>$case['name'],'first'=>$first,'second'=>['opts'=>$GLOBALS['opts'],'schedule'=>$GLOBALS['schedule']]];
}
echo json_encode($out,JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES);
'''
results={}
for label,body,version in [('before',old_automation,'6.72.346'),('after',new_automation,'6.72.347')]:
  assert body.count(start)==1
  section=body[body.index(start):body.index(end,body.index(start))]
  src=php_prefix+php_class.replace('__METHOD__',section).replace('__VERSION__',version)+php_test.replace('__VERSION__',version)
  dest=base/'qa68'/f'POOLTEST_{version}.php';dest.write_text(src)
  x=subprocess.run(['php',str(dest)],capture_output=True,text=True,timeout=15)
  if x.returncode:raise RuntimeError(x.stderr)
  results[label]=json.loads(x.stdout)
assert len(results['before'])==len(results['after'])==5
checks=[]
for old,new in zip(results['before'],results['after']):
  assert old['name']==new['name']
  old_ops=old['first']['schedule'];new_ops=new['first']['schedule']
  if new['name'] in ('upgrade_completed','upgrade_no_previous_state'):
    assert len(old_ops)==2 and len(new_ops)==0
    assert new['first']['opts']['pool_version']=='6.72.347'
  if new['name'] in ('upgrade_in_progress','upgrade_old_cursor'):
    assert len(new_ops)==0
    assert new['first']['opts']=={'upgrade_in_progress':{'pool_version':'running:6.72.346','pool_cursor':217},'upgrade_old_cursor':{'pool_version':'6.72.345','pool_cursor':83}}[new['name']]
  if new['name']=='already_current':assert new['first']['opts']['pool_version']=='6.72.347'
  assert new['first']==new['second']
  checks.append({'scenario':new['name'],'before_automatic_jobs':len(old_ops),'after_automatic_jobs':len(new_ops),'state_after':new['first']['opts'],'idempotent':new['first']==new['second']})
results={'passed':len(checks),'cases':checks,'before':'actual original v346 WordPress init hook','after':'actual v347 code','comment':'Real WordPress DB/network not used.'}
(base/'qa68'/'POOL_UPDATE_RESULTS.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(results,ensure_ascii=False,indent=2))