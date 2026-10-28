#!/usr/bin/env node
import {parseArgs} from 'node:util';
import fs from 'node:fs';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
import {launchBrowser} from './browser-runtime.mjs';
const {values}=parseArgs({options:{html:{type:'string'},selector:{type:'string',default:'section.poster'},output:{type:'string'},width:{type:'string'},height:{type:'string'},browser:{type:'string'},'check-only':{type:'boolean',default:false},'allow-network':{type:'boolean',default:false},help:{type:'boolean',default:false}}});
if(values.help){console.log('render-social-card.mjs --html /absolute/page.html --selector #poster [--output /absolute/card.png] [--width 1086 --height 1448] [--check-only] [--browser /absolute/chrome] [--allow-network]');process.exit(0);}
if(!values.html||!path.isAbsolute(values.html)||!fs.existsSync(values.html))throw new Error('--html must be an existing absolute file path');
if(!values['check-only']&&(!values.output||!path.isAbsolute(values.output)))throw new Error('--output must be absolute unless --check-only');
if(values.output&&fs.existsSync(values.output))throw new Error('Output already exists; choose a new version: '+values.output);
for(const key of ['width','height'])if(values[key]&&(!/^\d+$/.test(values[key])||Number(values[key])<1||Number(values[key])>10000))throw new Error('Invalid --'+key);
const browser=await launchBrowser({executablePath:values.browser});
try{
 const context=await browser.newContext({viewport:{width:Math.max(1400,Number(values.width||0)+32),height:Math.max(1700,Number(values.height||0)+32)},deviceScaleFactor:1,reducedMotion:'reduce'});
 const page=await context.newPage();
 const localFailures=[];
 page.on('requestfailed',r=>{if(r.url().startsWith('file:'))localFailures.push(r.url());});
 if(!values['allow-network'])await page.route(/^https?:\/\//,route=>route.abort());
 await page.goto(pathToFileURL(values.html).href,{waitUntil:'load'});
 await page.evaluate(()=>document.fonts.ready);
 await page.waitForTimeout(120);
 const poster=page.locator(values.selector);
 const count=await poster.count();
 if(count!==1)throw new Error('Selector must identify exactly one poster; found '+count);
 const state=await poster.evaluate(el=>{
  const b=el.getBoundingClientRect();
  const invisible=n=>{const s=getComputedStyle(n);return s.display==='none'||s.visibility==='hidden';};
  const overflow=[...el.querySelectorAll('*')].filter(n=>!(n instanceof SVGElement)&&!invisible(n)).filter(n=>{const r=n.getBoundingClientRect();return r.width>0&&r.height>0&&(r.left<b.left-.5||r.right>b.right+.5||r.top<b.top-.5||r.bottom>b.bottom+.5)}).map(n=>({tag:n.tagName,class:n.className,text:n.textContent?.slice(0,70)}));
  const brokenImages=[...el.querySelectorAll('img')].filter(n=>!invisible(n)&&(!n.complete||!n.naturalWidth)).map(n=>n.getAttribute('src'));
  return {width:b.width,height:b.height,overflow,brokenImages};
 });
 if(state.overflow.length||state.brokenImages.length||localFailures.length)throw new Error(JSON.stringify({...state,localFailures}));
 for(const key of ['width','height'])if(values[key]&&state[key]!==Number(values[key]))throw new Error('Poster '+key+' is '+state[key]+', expected '+values[key]+'. Source was not resized.');
 const png=await poster.screenshot({animations:'disabled'});
 const actual={width:png.readUInt32BE(16),height:png.readUInt32BE(20)};
 if(actual.width!==Math.round(state.width)||actual.height!==Math.round(state.height))throw new Error('Exported dimensions differ from poster');
 if(!values['check-only']){fs.mkdirSync(path.dirname(values.output),{recursive:true});fs.writeFileSync(values.output,png,{flag:'wx'});}
 console.log(JSON.stringify({mode:values['check-only']?'check-only':'export',...actual,localFailures,brokenImages:state.brokenImages,overflow:state.overflow,output:values['check-only']?null:values.output}));
}finally{await browser.close();}
