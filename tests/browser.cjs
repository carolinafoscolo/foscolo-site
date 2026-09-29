// Optional visual/browser verification. Requires Playwright and a Chromium binary.
const { chromium } = require('playwright');
const http = require('http'), fs = require('fs'), path = require('path'), assert = require('assert');
const root = path.resolve(__dirname, '..');
const mime = {'.html':'text/html; charset=utf-8','.css':'text/css','.js':'text/javascript','.png':'image/png','.webp':'image/webp','.ttf':'font/ttf'};
const server = http.createServer((req,res) => {
 let p = path.join(root, decodeURI(req.url.split('?')[0]));
 if (!p.startsWith(root+path.sep) && p!==root) {res.writeHead(403);return res.end();}
 if (fs.existsSync(p) && fs.statSync(p).isDirectory()) p += '/index.html';
 if (!fs.existsSync(p)) {res.writeHead(404);return res.end();}
 res.setHeader('Content-Type',mime[path.extname(p)]||'application/octet-stream');fs.createReadStream(p).pipe(res);
});
(async()=>{
 await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
 const base = `http://127.0.0.1:${server.address().port}`;
 const browser = await chromium.launch({headless:true,...(process.env.CHROMIUM_PATH?{executablePath:process.env.CHROMIUM_PATH}:{}),args:['--no-sandbox']});
 try {
  const page = await browser.newPage(); const errors=[]; page.on('pageerror',e=>errors.push(e.message));
  const paths=fs.readFileSync(path.join(root,'sitemap.xml'),'utf8').match(/<loc>(.*?)<\/loc>/g).map(x=>new URL(x.replace(/<\/?loc>/g,'')).pathname);
  for (const width of [390,1440]) {
   await page.setViewportSize({width,height:900});
   for (const url of paths) {
    const response=await page.goto(base+url);assert.equal(response.status(),200,url);
    await page.evaluate(async()=>{document.querySelectorAll('img').forEach(img=>img.loading='eager');await document.fonts.ready;await Promise.all(Array.from(document.images).map(img=>img.decode().catch(()=>{})));});
    const checks=await page.evaluate(()=>({overflow:document.documentElement.scrollWidth>innerWidth+1,badImages:[...document.images].filter(i=>!i.naturalWidth).map(i=>i.src),h1:document.querySelectorAll('h1').length}));
    assert(!checks.overflow,`${url} overflows at ${width}px`);assert.equal(checks.badImages.length,0,`${url} broken images`);assert.equal(checks.h1,1);
   }
  }
  await page.setViewportSize({width:390,height:844});await page.goto(base+'/pt/index.html');
  const menu=page.locator('.menu-toggle');await menu.click();assert.equal(await menu.getAttribute('aria-expanded'),'true');assert(await page.locator('#main-nav').isVisible());await page.keyboard.press('Escape');assert.equal(await menu.getAttribute('aria-expanded'),'false');
  await page.setViewportSize({width:320,height:800});await page.goto(base+'/fr/index.html');assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),'320px home overflow');
  const nojs=await browser.newContext({javaScriptEnabled:false,viewport:{width:390,height:844}});const p=await nojs.newPage();await p.goto(base+'/pt/index.html');assert(await p.locator('#main-nav').isVisible());await nojs.close();
  if (process.env.SCREENSHOT_DIR) {
   fs.mkdirSync(process.env.SCREENSHOT_DIR,{recursive:true});
   for (const [url,width,name] of [['/pt/index.html',1440,'home-desktop'],['/pt/index.html',390,'home-mobile'],['/pt/notes-on-care.html',1440,'notes'],['/pt/todos-ou-nenhum.html',390,'todos-mobile'],['/fr/index.html',1440,'french'],['/zh/index.html',1440,'chinese']]) {
    await page.setViewportSize({width,height:1000});await page.goto(base+url);await page.evaluate(async()=>{document.querySelectorAll('img').forEach(i=>i.loading='eager');await document.fonts.ready;await Promise.all([...document.images].map(i=>i.decode().catch(()=>{})));});await page.screenshot({path:path.join(process.env.SCREENSHOT_DIR,name+'.png'),fullPage:true});
   }
  }
  assert.equal(errors.length,0,errors.join('\n'));console.log(`PASS: ${paths.length} routes at 390px and 1440px; mobile menu, Escape, 320px layout, no-JS navigation; zero broken images or JS errors.`);
 } finally {await browser.close();server.close();}
})().catch(e=>{console.error(e);server.close();process.exitCode=1});
