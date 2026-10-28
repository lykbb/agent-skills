#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const references=['background-systems.md','category-cookbook.md','components.md','content-planning.md','image-overlay.md','layout-recipes.md','live-photo-production.md','map-component.md','platform-specs.md','portrait-fill.md','production-workflow.md','qa-checklist.md','screenshot-treatment.md','style-system.md','theme-presets.md','title-shortener.md'];
const assets=['magazine-bg-webgl.js','template-editorial-card.html','template-swiss-card.html','screenshot-backgrounds/style-a/dune.webp','screenshot-backgrounds/style-a/forest-ink.webp','screenshot-backgrounds/style-a/indigo-porcelain.webp','screenshot-backgrounds/style-a/kraft-paper.webp','screenshot-backgrounds/style-a/monocle-classic.webp','screenshot-backgrounds/style-b/ikb-dot-gradient.webp','screenshot-backgrounds/style-b/lemon-green-dot-shadow.webp','screenshot-backgrounds/style-b/lemon-grid.webp','screenshot-backgrounds/style-b/safety-orange-halftone.webp'];
const scripts=['add-livephoto-maker-note.swift','add-livephoto-mov-metadata.swift','make-video-contact-sheet.py','package-live-photo.py','browser-runtime.mjs','render-social-card.mjs','check-skill-docs.mjs'];
const localRefs=['production-manual.md','workflow-and-review.md','rendering-environment.md','series-and-revisions.md','upstream-source.md'];
const required=['SKILL.md','LICENSE','COMMERCIAL_LICENSING.md','package.json','package-lock.json','agents/openai.yaml','validate-social-deck.mjs',...references.map(n=>'references/'+n),...localRefs.map(n=>'references/'+n),...assets.map(n=>'assets/'+n),...scripts.map(n=>'scripts/'+n)];
const failures=[];
for(const file of required)if(!fs.existsSync(path.join(root,file)))failures.push('Missing '+file);
const text=file=>fs.readFileSync(path.join(root,file),'utf8');
let checkedLinks=0;
for(const file of ['SKILL.md','references/workflow-and-review.md','references/rendering-environment.md','references/series-and-revisions.md']){
 for(const m of text(file).matchAll(/\[[^\]]+\]\(([^)]+)\)/g)){
  const target=m[1];if(/^(https?:|\/|#)/.test(target))continue;
  checkedLinks++;
  if(!fs.existsSync(path.resolve(root,path.dirname(file),target.split('#')[0])))failures.push('Broken link '+file+' -> '+target);
 }
}
const recipeText=text('references/layout-recipes.md');
const editorial=new Set([...recipeText.matchAll(/^### (M\d{2})\b/gm)].map(m=>m[1]));
const swiss=new Set([...recipeText.matchAll(/^### (S\d{2})\b/gm)].map(m=>m[1]));
if(editorial.size!==16||swiss.size!==12)failures.push('Incomplete recipe library');
for(const file of ['assets/template-editorial-card.html','assets/template-swiss-card.html'])if(text(file).includes('../assets/screenshot-backgrounds/'))failures.push('Project asset path not adapted: '+file);
const pkg=JSON.parse(text('package.json')),lock=JSON.parse(text('package-lock.json'));
if(pkg.name!=='social-image-studio'||lock.name!==pkg.name||lock.packages[''].name!==pkg.name)failures.push('Manifest name mismatch');
if(pkg.license!=='AGPL-3.0-only'||!text('LICENSE').includes('GNU AFFERO GENERAL PUBLIC LICENSE'))failures.push('License mismatch');
const main=text('SKILL.md');
if(!/^name: social-image-studio$/m.test(main))failures.push('Skill name mismatch');
if(!text('agents/openai.yaml').includes('$social-image-studio'))failures.push('UI invocation mismatch');
const runningFiles=['SKILL.md','references/workflow-and-review.md','references/rendering-environment.md','scripts/browser-runtime.mjs','scripts/render-social-card.mjs','validate-social-deck.mjs'];
for(const file of runningFiles)if(text(file).includes('/skills/guizang-social-card-skill'))failures.push('Runtime still depends on original skill: '+file);
console.log(JSON.stringify({ok:failures.length===0,requiredFiles:required.length,originalReferences:references.length,assets:assets.length,scripts:scripts.length,editorialRecipes:editorial.size,swissRecipes:swiss.size,checkedLinks,failures}));
process.exit(failures.length?1:0);
