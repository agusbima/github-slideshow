const {chromium}=require('playwright');const fs=require('fs');const path=require('path');
(async()=>{const D=process.argv[2];const tl=JSON.parse(fs.readFileSync(D+'/timeline.json'));
const only=process.argv[3];
const b=await chromium.launch();const p=await b.newPage({viewport:{width:720,height:1280}});
await p.goto('file://'+D+'/src/scene.html');await p.evaluate(t=>setTimeline(t),tl);
fs.mkdirSync(D+'/frames',{recursive:true});
const N=Math.ceil(tl.total*tl.fps);
const list=only?only.split(',').map(Number):[...Array(N).keys()];
for(const i of list){await p.evaluate(t=>render(t),i/tl.fps);await p.screenshot({path:`${D}/frames/${String(i).padStart(5,'0')}.png`});}
await b.close();console.log('frames',list.length);})();
