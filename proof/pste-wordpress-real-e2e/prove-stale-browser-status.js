#!/usr/bin/env node
"use strict";
const fs=require("fs");
const vm=require("vm");

async function main(){
  const html=fs.readFileSync(process.argv[2],"utf8");
  const scripts=[...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m=>m[1]);
  const src=scripts.find(s=>s.includes("pste_breadth_research_status")&&s.includes("pste-breadth-start"));
  if(!src) throw new Error("PSTE_BROWSER_RACE_SCRIPT_NOT_FOUND");

  class Elem{
    constructor(id){this.id=id;this.style={};this.className="";this.textContent="";this.value="";this.checked=false;this.listeners={};this.child=null;}
    addEventListener(type,fn){this.listeners[type]=fn;}
    querySelector(sel){if(sel==="p"){if(!this.child)this.child=new Elem(this.id+"-p");return this.child;}return null;}
  }
  const els={};
  for(const id of ["pste-research-feedback","pste-breadth-start","pste-breadth-confirm-cost","pste-breadth-target","pste-breadth-max","pste-driver-status","pste-driver-health","pste-driver-message"]) els[id]=new Elem(id);
  els["pste-breadth-confirm-cost"].checked=true;
  els["pste-breadth-target"].value="40";
  els["pste-breadth-max"].value="40";

  const actions=[];
  const response=(payload,delay=0)=>new Promise(resolve=>setTimeout(()=>resolve({
    ok:true,status:200,text:async()=>JSON.stringify(payload)
  }),delay));

  const ctx={
    document:{getElementById:(id)=>els[id]||null},
    fetch:async(_url,opts)=>{
      const body=new URLSearchParams(opts.body||"");
      const action=body.get("action")||"";
      actions.push(action);
      if(action==="pste_breadth_research_status"){
        return response({success:false,data:{error_code:"PSTE_BREADTH_QUEUE_NOT_FOUND"}},40);
      }
      if(action==="pste_breadth_research_start"){
        return response({success:true,data:{
          queue:{queue_uuid:"NEW-QUEUE",status:"RUNNING",completed_count:0,max_items:40,item_count:40,usable_candidate_count:0,blocked_count:0,items:[],current_index:0},
          driver:{status:"RUNNING",health_code:"PSTE_DRIVER_STEP_SAVED",message:"saved"}
        }},0);
      }
      throw new Error("UNEXPECTED_ACTION_"+action);
    },
    URLSearchParams,
    setTimeout,
    clearTimeout,
    setInterval:()=>0,
    clearInterval:()=>{},
    confirm:()=>true,
    console
  };
  vm.createContext(ctx);
  vm.runInContext(src,ctx,{timeout:2000});

  await new Promise(r=>setTimeout(r,5));
  const click=els["pste-breadth-start"].listeners.click;
  if(typeof click!=="function") throw new Error("PSTE_BROWSER_RACE_START_HANDLER_MISSING");
  await click();
  await new Promise(r=>setTimeout(r,80));

  const feedback=els["pste-research-feedback"];
  const text=(feedback.child&&feedback.child.textContent)||"";
  if(!actions.includes("pste_breadth_research_status")||!actions.includes("pste_breadth_research_start")) throw new Error("PSTE_BROWSER_RACE_SEQUENCE_NOT_EXECUTED");
  if(text.includes("PSTE_BREADTH_QUEUE_NOT_FOUND")||feedback.className.includes("notice-error")) throw new Error("PSTE_BROWSER_STALE_STATUS_OVERRIDES_NEW_QUEUE");
  if(!text.includes("Server-Driver gestartet")) throw new Error("PSTE_BROWSER_NEW_QUEUE_MESSAGE_LOST");
  console.log("PASS_BROWSER_STALE_STATUS_IGNORED_AFTER_NEW_QUEUE_START");
}
main().catch(e=>{console.error(e&&e.stack||e);process.exit(1);});
