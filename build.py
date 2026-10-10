"""index.html(아티팩트용 본문) -> docs/ 독립 실행 웹앱(PWA) 빌드"""
import json, hashlib, pathlib
from PIL import Image, ImageDraw, ImageFont

ROOT = pathlib.Path(__file__).parent
DOCS = ROOT / "docs"; DOCS.mkdir(exist_ok=True)
src = (ROOT / "index.html").read_text()

# ---------- icons ----------
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
def icon(size, maskable=False):
    s = size; im = Image.new("RGBA", (s, s), (42, 104, 212, 255)); d = ImageDraw.Draw(im)
    if not maskable:  # rounded square for plain icon
        im = Image.new("RGBA", (s, s), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.rounded_rectangle([0, 0, s - 1, s - 1], radius=int(s * .22), fill=(42, 104, 212, 255))
    safe = .60 if maskable else .74            # content area
    t = s * safe / 3.3; g = t * .15; ox = (s - (3 * t + 2 * g)) / 2
    f = ImageFont.truetype(FONT, int(t * .58))
    lane = (90, 140, 228, 255); pad = t * .1
    d.rounded_rectangle([ox - pad, ox - pad, ox + 3 * t + 2 * g + pad, ox + t + pad], radius=t * .3, fill=lane)
    d.rounded_rectangle([ox - pad, ox - pad, ox + t + pad, ox + 3 * t + 2 * g + pad], radius=t * .3, fill=lane)
    cells = {(0, 0): "2", (0, 1): "+", (0, 2): "3", (1, 0): "\u00d7", (2, 0): "4"}
    for (r, c), ch in cells.items():
        x, y = ox + c * (t + g), ox + r * (t + g)
        if ch in "+\u00d7":
            ink = (255, 255, 255, 255)
        else:
            d.rounded_rectangle([x, y + t * .08, x + t, y + t * 1.08], radius=t * .22, fill=(217, 154, 0, 255))
            d.rounded_rectangle([x, y, x + t, y + t], radius=t * .22, fill=(255, 200, 61, 255))
            ink = (58, 42, 0, 255)
        d.text((x + t / 2, y + t / 2), ch, font=f, fill=ink, anchor="mm")
    return im
for n in (192, 512):
    icon(n).save(DOCS / f"icon-{n}.png")
icon(512, True).save(DOCS / "icon-maskable-512.png")
icon(180, True).convert("RGB").save(DOCS / "apple-touch-icon.png")

# ---------- manifest ----------
(DOCS / "manifest.webmanifest").write_text(json.dumps({
    "name": "십자 셈놀이", "short_name": "셈놀이", "lang": "ko",
    "description": "가로세로 식을 숫자 블록으로 채우는 사칙연산 퍼즐",
    "start_url": "./", "scope": "./", "display": "standalone", "orientation": "any",
    "background_color": "#E8F1F8", "theme_color": "#2A68D4",
    "icons": [
        {"src": "icon-192.png", "sizes": "192x192", "type": "image/png"},
        {"src": "icon-512.png", "sizes": "512x512", "type": "image/png"},
        {"src": "icon-maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"}]
}, ensure_ascii=False, indent=1))

# ---------- fonts: subset to the characters this app actually uses (small + fully cacheable offline) ----------
import re, urllib.parse
OLD_FONT = re.search(r'<link rel="stylesheet" href="(https://fonts\.googleapis\.com/css2\?[^"]+)">', src).group(1)
chars = "".join(sorted(set(c for c in src if not c.isspace() and ord(c) < 0x10000))) + "0123456789"
FONT_URL = OLD_FONT.replace("&amp;", "&").replace("&display=swap", "") + "&text=" + urllib.parse.quote("".join(sorted(set(chars)))) + "&display=swap"
src = src.replace(OLD_FONT, FONT_URL.replace("&", "&amp;"))

# ---------- page ----------
i = src.index("<style>"); title = src[:i]; rest = src[i:]
j = rest.index("</style>") + len("</style>"); style, body = rest[:j], rest[j:]
style = style.replace("<style>", "<style>\nhtml{padding-block:env(safe-area-inset-top,0px) env(safe-area-inset-bottom,0px);overscroll-behavior:none}\nbody{margin:0}\nimg{max-width:100%}", 1)
head = f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#2A68D4">
<meta name="description" content="가로세로 식을 숫자 블록으로 채우는 사칙연산 퍼즐">
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" type="image/png" sizes="192x192" href="icon-192.png">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="apple-mobile-web-app-title" content="셈놀이">
"""
sw_reg = """<script>
if('serviceWorker' in navigator&&(location.protocol==='https:'||location.hostname==='localhost')){addEventListener('load',()=>{
  navigator.serviceWorker.register('sw.js').catch(()=>{});
  navigator.serviceWorker.ready.then(()=>{if(!store.get('offlineReady',false)){store.set('offlineReady',true);setTimeout(()=>toast('이제 인터넷 없이도 할 수 있어요'),1500)}})})}
</script>"""
page = head + title + style + "\n</head>\n<body>" + body + "\n" + sw_reg + "\n</body>\n</html>\n"
(DOCS / "index.html").write_text(page)

# ---------- service worker (version = content hash, so every build refreshes caches) ----------
ver = hashlib.sha1(page.encode()).hexdigest()[:10]
(DOCS / "sw.js").write_text(f"""const V='sem-{ver}';
const SHELL=['./','index.html','manifest.webmanifest','icon-192.png','icon-512.png','icon-maskable-512.png','apple-touch-icon.png'];
const FONT={json.dumps(FONT_URL)};
async function cacheFonts(c){{try{{const r=await fetch(FONT,{{mode:'cors'}});if(!r.ok)return;await c.put(FONT,r.clone());
  const urls=[...(await r.text()).matchAll(/url\\((https:[^)]+)\\)/g)].map(m=>m[1]);
  await Promise.all(urls.map(u=>fetch(u,{{mode:'cors'}}).then(x=>x.ok&&c.put(u,x)).catch(()=>{{}})))}}catch(e){{}}}}
self.addEventListener('install',e=>{{e.waitUntil(caches.open(V).then(async c=>{{await c.addAll(SHELL);await cacheFonts(c)}}).then(()=>self.skipWaiting()))}});
self.addEventListener('activate',e=>{{e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k!==V).map(k=>caches.delete(k)))).then(()=>self.clients.claim()))}});
self.addEventListener('fetch',e=>{{
  const r=e.request; if(r.method!=='GET')return;
  const u=new URL(r.url);
  if(r.mode==='navigate'){{ // 온라인이면 최신 버전, 오프라인이면 저장본
    e.respondWith(fetch(r).then(res=>{{caches.open(V).then(c=>c.put('index.html',res.clone()));return res}}).catch(()=>caches.match('index.html')));return}}
  if(u.origin===location.origin||/fonts\\.(googleapis|gstatic)\\.com$/.test(u.hostname)){{ // 저장본 먼저, 뒤에서 갱신
    e.respondWith(caches.open(V).then(async c=>{{const hit=await c.match(r.url)||await c.match(r);
      const net=fetch(r).then(res=>{{if(res.ok||res.type==='opaque')c.put(r,res.clone());return res}}).catch(()=>hit);
      return hit||net}}))}}
}});
""")
(DOCS / ".nojekyll").touch()
print("built", ver)
