const V='sem-e465a10c55';
const SHELL=['./','index.html','manifest.webmanifest','icon-192.png','icon-512.png','icon-maskable-512.png','apple-touch-icon.png'];
const FONT="https://fonts.googleapis.com/css2?family=Jua&family=Gowun+Dodum&family=Fredoka:wght@500;600;700&text=%21%22%23%24%25%26%27%28%29%2A%2B%2C-./0123456789%3A%3B%3C%3D%3E%3F%40ABCDEFGHIJKLMNOPRSTVWXY%5B%5D%5E%60abcdefghijklmnopqrstuvwxyz%7B%7C%7D%C2%B7%C3%97%C3%B7%E2%86%90%E2%86%B6%E2%88%92%E2%8C%AB%E2%8F%B1%E2%97%90%E2%98%80%E2%98%85%E2%98%BE%E2%9C%93%EA%B0%80%EA%B0%84%EA%B0%9C%EA%B1%B8%EA%B2%8C%EA%B3%84%EA%B3%A0%EA%B3%B1%EA%B3%B3%EA%B3%B5%EA%B3%BC%EA%B5%AC%EA%B8%80%EA%B8%88%EA%B8%B0%EA%B8%B4%EA%B9%8C%EB%82%98%EB%82%A8%EB%84%A3%EB%86%80%EB%86%93%EB%88%84%EB%88%8C%EB%88%97%EB%8A%94%EB%8A%98%EB%8B%A4%EB%8B%A8%EB%8B%B5%EB%8D%94%EB%8D%98%EB%8F%84%EB%8F%8C%EB%8F%99%EB%90%98%EB%91%90%EB%91%A1%EB%92%A4%EB%95%8C%EB%9E%98%EB%9F%AC%EB%A0%87%EB%A0%88%EB%A0%A4%EB%A1%9C%EB%A1%9D%EB%A3%8C%EB%A5%AD%EB%A5%B4%EB%A5%BC%EB%A6%AC%EB%A6%B0%EB%A7%9E%EB%A7%A4%EB%A8%BC%EB%A9%8B%EB%A9%B4%EB%AA%87%EB%AA%A8%EB%AA%A9%EB%AC%B4%EB%AC%B8%EB%B0%9D%EB%B2%88%EB%B2%A8%EB%B2%BD%EB%B3%B4%EB%B8%94%EB%B9%88%EB%B9%A8%EB%B9%BC%EC%82%B0%EC%83%88%EC%84%9C%EC%84%B1%EC%84%B8%EC%85%88%EC%86%8C%EC%86%8D%EC%88%98%EC%88%AB%EC%89%AC%EC%8B%9C%EC%8B%9D%EC%8B%A4%EC%8B%AD%EC%94%A8%EC%94%A9%EC%95%84%EC%95%8A%EC%95%8C%EC%95%98%EC%95%BC%EC%96%B4%EC%97%90%EC%97%B0%EC%98%88%EC%98%A4%EC%99%84%EC%9A%94%EC%9A%B0%EC%9A%B4%EC%9B%80%EC%9B%8C%EC%9B%94%EC%9C%BC%EC%9D%84%EC%9D%8C%EC%9D%98%EC%9D%B4%EC%9D%BC%EC%9E%84%EC%9E%90%EC%9E%98%EC%A0%80%EC%A0%84%EC%A0%90%EC%A0%95%EC%A0%9C%EC%A0%B8%EC%A3%BC%EC%A4%84%EC%A6%90%EC%A7%80%EC%A7%84%EC%A7%B8%EC%B1%84%EC%B2%98%EC%B5%9C%EC%B6%9C%EC%B9%B8%ED%81%B0%ED%86%A0%ED%86%B5%ED%8A%B8%ED%8B%80%ED%8C%90%ED%8D%BC%ED%92%80%ED%95%98%ED%95%9C%ED%95%A0%ED%95%B4%ED%96%88%ED%99%94%ED%9B%8C%ED%9E%8C%ED%9E%90&display=swap";
async function cacheFonts(c){try{const r=await fetch(FONT,{mode:'cors'});if(!r.ok)return;await c.put(FONT,r.clone());
  const urls=[...(await r.text()).matchAll(/url\((https:[^)]+)\)/g)].map(m=>m[1]);
  await Promise.all(urls.map(u=>fetch(u,{mode:'cors'}).then(x=>x.ok&&c.put(u,x)).catch(()=>{})))}catch(e){}}
self.addEventListener('install',e=>{e.waitUntil(caches.open(V).then(async c=>{await c.addAll(SHELL);await cacheFonts(c)}).then(()=>self.skipWaiting()))});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k!==V).map(k=>caches.delete(k)))).then(()=>self.clients.claim()))});
self.addEventListener('fetch',e=>{
  const r=e.request; if(r.method!=='GET')return;
  const u=new URL(r.url);
  if(r.mode==='navigate'){ // 온라인이면 최신 버전, 오프라인이면 저장본
    e.respondWith(fetch(r).then(res=>{caches.open(V).then(c=>c.put('index.html',res.clone()));return res}).catch(()=>caches.match('index.html')));return}
  if(u.origin===location.origin||/fonts\.(googleapis|gstatic)\.com$/.test(u.hostname)){ // 저장본 먼저, 뒤에서 갱신
    e.respondWith(caches.open(V).then(async c=>{const hit=await c.match(r.url)||await c.match(r);
      const net=fetch(r).then(res=>{if(res.ok||res.type==='opaque')c.put(r,res.clone());return res}).catch(()=>hit);
      return hit||net}))}
});
