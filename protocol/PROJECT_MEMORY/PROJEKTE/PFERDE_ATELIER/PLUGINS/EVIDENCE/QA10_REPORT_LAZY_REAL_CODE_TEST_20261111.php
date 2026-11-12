<?php
error_reporting(E_ALL);
$file=$argv[1]??'';
$source=(string)file_get_contents($file);
$start=strpos($source,"\$ppar_missing_requested = isset(\$_GET['ppar_ebay_report'])");
$end=$start===false?false:strpos($source,"\$ppar_missing_rows = (array)(\$ppar_missing_report['rows'] ?? array());",$start);
if($start===false||$end===false)throw new RuntimeException('Source lazy section not found');
$end+=strlen("\$ppar_missing_rows = (array)(\$ppar_missing_report['rows'] ?? array());");
$snippet=substr($source,$start,$end-$start);
class LazyProbe {
 private string $code;public int $calls=0;
 public function __construct(string $source){$this->code=$source;}
 private function ebay_missing_family_diagnostic_rows($a,$b,$c){$this->calls++;return ['valid'=>true,'rows'=>[['id'=>'mock']]];}
 public function run($query){ $_GET=$query;$canonical_run=[];$selection_state=[];$job_summary=[];eval($this->code);return [$ppar_missing_requested,count($ppar_missing_rows),$this->calls]; }
}
$p=new LazyProbe($snippet);
$tests=[
 [['other'=>'1'],[false,0,0]],
 [['ppar_ebay_report'=>'0'],[false,0,0]],
 [['ppar_ebay_report'=>['1']],[false,0,0]],
 [['ppar_ebay_report'=>'1'],[true,1,1]],
 [['ppar_ebay_report'=>'1'],[true,1,2]],
 [['ppar_ebay_report'=>'2'],[false,0,2]],
];
foreach($tests as [$input,$expected]){$actual=$p->run($input);if($actual!==$expected)throw new RuntimeException('bad lazy result '.json_encode($actual).' expected '.json_encode($expected));}
echo "PASS 6 real extracted PHP calls: no expensive report work for normal backend page, explicit report request only; bad array query ignored\n";