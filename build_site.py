# -*- coding: utf-8 -*-
"""Monta o site de compartilhamento (en/ e pt/) + ZIPs. Uso: python3 build_site.py"""
import sys, re, shutil, pathlib, zipfile
SRC = pathlib.Path.home() / "Desktop/claude/scale-criativos"
sys.path.insert(0, str(SRC / "estaticos-en"))
import gen, gen_pt
ROOT = pathlib.Path(__file__).resolve().parent
REL = "https://github.com/Guga-Marion/mydose-scale-ads/releases/download/v1"
strip = lambda h: re.sub(r"<[^>]+>", "", h)
L = {
 "en": dict(dir="estaticos-en", fin="finais-en", title="MyDose Scale · English ads", lead="24 concepts × 4:5 (feed) and 9:16 (Stories/Reels). Static JPG + animated MP4 (7.5 s). Ready for Ads Manager.",
            all="Download everything (ZIP)", st="Statics only (ZIP)", vd="Videos only (ZIP)", other="Versão em português →", otherhref="../pt/", jpg="JPG", mp4="MP4", play="Play animation", feed="Feed 4:5", story="Stories 9:16",
            name=lambda a: strip(a["h1"])),
 "pt": dict(dir="estaticos-pt", fin="finais-pt", title="MyDose Scale · Anúncios em português", lead="24 conceitos × 4:5 (feed) e 9:16 (Stories/Reels). Estático em JPG + animado em MP4 (7,5 s). Prontos para o gerenciador.",
            all="Baixar tudo (ZIP)", st="Só os estáticos (ZIP)", vd="Só os vídeos (ZIP)", other="English version →", otherhref="../en/", jpg="JPG", mp4="MP4", play="Ver animação", feed="Feed 4:5", story="Stories 9:16",
            name=lambda a: strip(gen_pt.COPY[a["id"][:2]][0])),
}
CSS = """*{box-sizing:border-box}body{margin:0;font-family:-apple-system,'Segoe UI',Roboto,Arial,sans-serif;background:#F6F4F2;color:#1E1D1D}
header{padding:48px 24px 28px;text-align:center;background:linear-gradient(180deg,#D6DDFF,#F5E3F6 60%,#F6F4F2)}
h1{font-family:Georgia,serif;font-weight:400;font-size:clamp(30px,4.4vw,52px);letter-spacing:-.02em;margin:0 0 10px}
header p{max-width:720px;margin:0 auto 22px;color:#565452;font-size:17px;line-height:1.5}
.bar{display:flex;gap:10px;justify-content:center;flex-wrap:wrap}
.btn{display:inline-flex;align-items:center;gap:8px;text-decoration:none;font-weight:600;border-radius:999px;padding:10px 18px;font-size:14px;border:1.5px solid rgba(30,29,29,.18);color:#1E1D1D;background:#fff}
.btn:hover{border-color:#415FF5;color:#2741C9}.btn.pri{background:linear-gradient(100deg,#415FF5,#C64FCA 52%,#F56442);color:#fff;border:0;padding:14px 26px;font-size:16px;box-shadow:0 14px 30px -14px rgba(198,79,202,.8)}
.btn.lang{background:#191E47;color:#fff;border:0}
main{max-width:1320px;margin:0 auto;padding:12px 24px 80px;display:grid;grid-template-columns:repeat(auto-fill,minmax(380px,1fr));gap:28px}
.card{background:#fff;border-radius:22px;padding:16px;box-shadow:0 16px 40px -24px rgba(25,30,71,.4)}
.card h2{font-size:17px;margin:2px 4px 12px;font-weight:700}.card h2 small{color:#848484;font-weight:600;margin-right:6px}
.media{display:grid;grid-template-columns:1.42fr 1fr;gap:10px;align-items:start}
.media img,.media video{width:100%;display:block;border-radius:12px;background:#eee}
.slot{position:relative;cursor:pointer}.slot .pl{position:absolute;left:8px;bottom:8px;background:rgba(25,30,71,.82);color:#fff;font-size:12px;font-weight:700;border-radius:999px;padding:6px 11px}
.dl{display:grid;grid-template-columns:1fr 1fr;gap:8px 10px;margin-top:12px}.dl span{grid-column:1/-1;font-size:12px;font-weight:700;color:#848484;letter-spacing:.06em;text-transform:uppercase;margin-top:4px}
.dl .btn{justify-content:center;padding:8px 10px;font-size:13px}
footer{text-align:center;color:#848484;font-size:13px;padding:0 24px 40px}"""
JS = """document.querySelectorAll('.slot').forEach(function(s){s.addEventListener('click',function(){var v=document.createElement('video');v.src=s.dataset.v;v.autoplay=v.loop=v.muted=v.playsInline=true;v.controls=true;s.replaceWith(v)})})"""

def build(lang):
    c = L[lang]; src = SRC / c["dir"]; out = ROOT / lang
    if out.exists(): shutil.rmtree(out)
    (out / "static").mkdir(parents=True); (out / "video").mkdir()
    for f in sorted((src / c["fin"]).glob("*.jpg")): shutil.copy(f, out / "static" / f.name)
    for f in sorted((src / "animados").glob("*.mp4")): shutil.copy(f, out / "video" / f.name)
    (ROOT / "zips").mkdir(exist_ok=True)
    for kind, pats in (("all", ("static", "video")), ("static", ("static",)), ("video", ("video",))):
        with zipfile.ZipFile(ROOT / "zips" / f"mydose-scale-ads-{lang}-{kind}.zip", "w", zipfile.ZIP_STORED) as z:
            for p in pats:
                for f in sorted((out / p).iterdir()): z.write(f, f"mydose-scale-ads-{lang}/{p}/{f.name}")
    cards = ""
    for a in gen.ADS:
        i = a["id"]
        cards += (f'<div class="card"><h2><small>{i[:2]}</small>{c["name"](a)}</h2><div class="media">'
                  f'<div class="slot" data-v="video/{i}-45.mp4"><img loading="lazy" src="static/{i}-45.jpg" alt=""><span class="pl">▶ {c["play"]}</span></div>'
                  f'<div class="slot" data-v="video/{i}-916.mp4"><img loading="lazy" src="static/{i}-916.jpg" alt=""><span class="pl">▶</span></div></div>'
                  f'<div class="dl"><span>{c["feed"]}</span><a class="btn" download href="static/{i}-45.jpg">↓ {c["jpg"]}</a><a class="btn" download href="video/{i}-45.mp4">↓ {c["mp4"]}</a>'
                  f'<span>{c["story"]}</span><a class="btn" download href="static/{i}-916.jpg">↓ {c["jpg"]}</a><a class="btn" download href="video/{i}-916.mp4">↓ {c["mp4"]}</a></div></div>')
    html = (f'<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>{c["title"]}</title><style>{CSS}</style></head><body>'
            f'<header><h1>{c["title"]}</h1><p>{c["lead"]}</p><div class="bar"><a class="btn pri" href="{REL}/mydose-scale-ads-{lang}-all.zip">↓ {c["all"]}</a></div>'
            f'<div class="bar" style="margin-top:12px"><a class="btn" href="{REL}/mydose-scale-ads-{lang}-static.zip">↓ {c["st"]}</a><a class="btn" href="{REL}/mydose-scale-ads-{lang}-video.zip">↓ {c["vd"]}</a><a class="btn lang" href="{c["otherhref"]}">{c["other"]}</a></div></header>'
            f'<main>{cards}</main><footer>MyDose Scale · example brands are fictional / marcas de exemplo são fictícias</footer><script>{JS}</script></body></html>')
    (out / "index.html").write_text(html, encoding="utf-8")
    print(lang, len(list((out/"static").iterdir())), "jpg", len(list((out/"video").iterdir())), "mp4")

for l in sys.argv[1:] or ["en", "pt"]: build(l)
(ROOT / "index.html").write_text('<!doctype html><meta charset="utf-8"><meta name="robots" content="noindex"><title>MyDose Scale ads</title><style>body{font-family:-apple-system,Arial,sans-serif;background:#F6F4F2;display:flex;min-height:100vh;align-items:center;justify-content:center;gap:16px;margin:0}a{background:#191E47;color:#fff;text-decoration:none;font-weight:600;padding:16px 28px;border-radius:999px}</style><a href="en/">English ads</a><a href="pt/">Anúncios em português</a>', encoding="utf-8")
