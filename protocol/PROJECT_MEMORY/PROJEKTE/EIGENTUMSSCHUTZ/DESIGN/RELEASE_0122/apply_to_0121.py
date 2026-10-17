#!/usr/bin/env python3
"""Apply exactly the Hab & Bewahr Design 0.1.22 mega-menu fix to intact 0.1.21 source.
Pure design; no WP category writes. Abort on unexpected source.
"""
from pathlib import Path
import sys
root=Path(sys.argv[1]) if len(sys.argv)>1 else Path("hab-bewahr-design-vorschau")
def change(rel,old,new):
 p=root/rel
 text=p.read_text(encoding="utf-8")
 assert text.count(old)==1, "unexpected original content: "+rel
 p.write_text(text.replace(old,new),encoding="utf-8")

change("templates/site.php",
        "        $all_areas=$areas;\n        $areas=array_slice($areas,0,5);",
        "        // Five desktop columns PER ROW, not a five-area content limit.\n        // All additional areas form subsequent rows; never hide valid children.")
change("templates/site.php",
        '<div class="hbdp-mega-heading"><div class="hbdp-mega-intro"><strong>\'.esc_html($world[\'name\']).\'</strong><p>\'.esc_html(hbdp_world_explanation($world[\'id\'])).\'</p></div><a href="\'.esc_url(hbdp_url($world)).\'">Alle Themen <span aria-hidden="true">→</span></a></div>',
        '<div class="hbdp-mega-heading"><div class="hbdp-mega-intro"><strong>\'.esc_html($world[\'name\']).\'</strong><p>\'.esc_html(hbdp_world_explanation($world[\'id\'])).\'</p></div></div>')
change("templates/site.php",
        "            $nlinks=0;\n            foreach(hbdp_nav_children($area['id']) as $subarea){\n                if($nlinks>=4)break;\n                $url=hbdp_nav_url($subarea);if($url==='')continue;",
        "            $nlinks=0;$available_links=0;\n            foreach(hbdp_nav_children($area['id']) as $subarea){\n                $url=hbdp_nav_url($subarea);if($url==='')continue;\n                $available_links++;\n                if($nlinks>=4)continue;")
change("templates/site.php",
        '            echo \'<a class="hbdp-mega-more" href="\'.esc_url($area_url).\'" aria-label="Alle Themen in \'.esc_attr($area[\'name\']).\'">Alle Themen <span aria-hidden="true">→</span></a></section>\';',
        '            if($available_links>$nlinks){\n                echo \'<a class="hbdp-mega-more" href="\'.esc_url($area_url).\'" aria-label="Alle Themen in \'.esc_attr($area[\'name\']).\'">Alle Themen <span aria-hidden="true">→</span></a>\';\n            }\n            echo \'</section>\';')
change("templates/site.php","0.1.21|","0.1.22|")
change("assets/style.css",
       ".hbdp-megagrid--6{grid-template-columns:repeat(6,minmax(0,1fr))}",
       ".hbdp-megagrid--6{grid-template-columns:repeat(5,minmax(0,1fr))}")
css=root/"assets/style.css"
with css.open("a",encoding="utf-8") as f:
 f.write("\n/* 0.1.22: maximum five area columns per desktop row, overflow wraps. */\n")
 f.write("@media (min-width:1141px) {.hbdp-megagrid,.hbdp-megagrid--6{grid-template-columns:repeat(5,minmax(0,1fr))}}\n")
p=root/"hab-bewahr-design-vorschau.php"
text=p.read_text(encoding="utf-8")
assert text.count("0.1.21")==6
p.write_text(text.replace("0.1.21","0.1.22"),encoding="utf-8")
with (root/"README.txt").open("a",encoding="utf-8") as f:
 f.write("\nVersion 0.1.22: Show all mega menu areas in rows of max five columns; ")
 f.write("show Alle Themen only where more than four valid topic links remain. ")
 f.write("No WP category changes.\n")
print("Updated existing Hab & Bewahr Design plugin to 0.1.22 without WP writes")
