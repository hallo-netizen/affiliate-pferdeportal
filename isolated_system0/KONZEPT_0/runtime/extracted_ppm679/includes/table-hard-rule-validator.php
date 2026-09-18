<?php
if (!defined('ABSPATH')) { return; }
final class PPM679_Table_Hard_Rule_Validator {
    const CONTRACT_FILE='contracts/table-contract-v1.json';
    private static function err($code,$rule,$path,$expected,$actual,$reason,$context){return PPM679_Diagnostic::error($code,$rule,$path,$expected,$actual,$reason,$context,'',__CLASS__,null,array(self::CONTRACT_FILE));}
    public static function validate_source_html($html,$context='table_hard_rule_source'){
        $errors=array(); $html=(string)$html;
        if(!preg_match('/<table\b[^>]*class=("|\')[^"\']*\bsystem-129-table\b[^"\']*\bcomparison-table\b[^"\']*\1[^>]*>/iu',$html,$m)){$errors[]=self::err('BLOCKED_TABLE_CANONICAL_SELECTOR','TABLE_MUST_USE_SYSTEM_129_AND_COMPARISON_CLASSES','content.table.class','system-129-table comparison-table',$m[0]??null,'Die sichtbare Tabelle ist nicht an den harten Tabellenvertrag gebunden.',$context);}
        if(preg_match('/<table\b[^>]*style=("|\')[^"\']*(?:border|background|outline|box-shadow)[^"\']*\1/iu',$html,$m)){$errors[]=self::err('BLOCKED_TABLE_INLINE_CONFLICT','TABLE_MUST_NOT_OVERRIDE_CANONICAL_TRANSPARENT_BORDER_RULES_INLINE','content.table.style','no conflicting inline styles',$m[0],'Inline-CSS darf die kanonischen Tabellenlinien nicht überschreiben.',$context);}
        $contract=json_decode((string)@file_get_contents(PPM679_PLUGIN_DIR.self::CONTRACT_FILE),true);
        if(!is_array($contract)||($contract['rules']['no_outer_lines']??null)!==true||(int)($contract['rules']['header_separator_px']??0)!==2||(int)($contract['rules']['other_inner_lines_px']??0)!==1||($contract['rules']['transparent_table_and_cells']??null)!==true){$errors[]=self::err('BLOCKED_TABLE_CONTRACT','CANONICAL_TABLE_CONTRACT_MUST_RETAIN_ALL_HARD_RULES','contract.table','transparent/no outer/2px header/1px inner',$contract,'Der Tabellenvertrag ist unvollständig oder abgeschwächt.',$context);}
        return $errors;
    }
    public static function validate_computed_evidence($evidence,$context='table_hard_rule_dom'){
        $e=is_array($evidence)?$evidence:array();$errors=array();
        $required=array('table_background'=>'transparent','cell_backgrounds_all_transparent'=>true,'outer_top_px'=>0,'outer_right_px'=>0,'outer_bottom_px'=>0,'outer_left_px'=>0,'header_separator_px'=>2,'inner_vertical_px'=>1,'inner_horizontal_px'=>1);
        foreach($required as $k=>$v){$a=$e[$k]??null;if($a!==$v){$errors[]=self::err('BLOCKED_TABLE_RENDERED_STYLE','RENDERED_TABLE_STYLE_MUST_MATCH_HARD_RULE','rendered_dom.table_style_evidence.'.$k,$v,$a,'Die gerenderte Tabelle verletzt den harten Tabellenvertrag.',$context);}}
        return $errors;
    }
}
