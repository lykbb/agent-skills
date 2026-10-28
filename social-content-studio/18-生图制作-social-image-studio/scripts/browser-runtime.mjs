import {createRequire} from 'node:module';
import {existsSync} from 'node:fs';
import {homedir} from 'node:os';
import path from 'node:path';
const require=createRequire(import.meta.url);
export function loadChromium(){
 const candidates=['playwright',process.env.SOCIAL_IMAGE_PLAYWRIGHT,path.join(homedir(),'.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright')].filter(Boolean);
 for(const candidate of candidates){try{const lib=require(candidate);if(lib.chromium)return lib.chromium;}catch{}}
 throw new Error('Playwright not found in existing dependencies. Check workspace runtime or SOCIAL_IMAGE_PLAYWRIGHT; no software was installed.');
}
export async function launchBrowser(options={}){
 const chromium=loadChromium();
 const explicit=options.executablePath||process.env.SOCIAL_IMAGE_BROWSER;
 if(explicit&&!existsSync(explicit))throw new Error('Configured browser does not exist: '+explicit);
 const installed=['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome','/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge',chromium.executablePath()];
 const executablePath=explicit||installed.find(p=>existsSync(p));
 if(!executablePath)throw new Error('No existing Chrome/Chromium found. Configure SOCIAL_IMAGE_BROWSER; no browser was downloaded.');
 return chromium.launch({executablePath,headless:true,args:['--use-angle=swiftshader','--enable-unsafe-swiftshader']});
}
