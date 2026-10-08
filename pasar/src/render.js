// pemakaian: node render.js <scene.html> <timeline.json> <folder_frames> [daftar_frame_koma]
const {chromium}=require('playwright');const fs=require('fs');const path=require('path');
(async()=>{const [html,tlf,out,only]=process.argv.slice(2);const tl=JSON.parse(fs.readFileSync(tlf));
const b=await chromium.launch();const p=await b.newPage({viewport:{width:720,height:1280}});
const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.goto('file://'+path.resolve(html));await p.evaluate(t=>setTimeline(t),tl);
fs.mkdirSync(out,{recursive:true});
const N=Math.ceil(tl.total*tl.fps);
const list=only?only.split(',').map(Number):[...Array(N).keys()];
for(const i of list){await p.evaluate(t=>render(t),i/tl.fps);await p.screenshot({path:`${out}/${String(i).padStart(5,'0')}.png`});}
await b.close();if(errs.length)console.log('ERR',errs);console.log('frames',list.length);})();
