# -*- coding: utf-8 -*-
"""Coloca os 3 filmes de 60 s no topo das páginas en/ e pt/ (rodar DEPOIS do build_site.py). Uso: python3 build_films.py"""
import shutil, pathlib, zipfile, subprocess, re
SRC = pathlib.Path.home() / "mydose-scale-video/out/filmes"; ROOT = pathlib.Path(__file__).resolve().parent
REL = "https://github.com/Guga-Marion/mydose-scale-ads/releases/download/v1"
F = {"pt": dict(h="Filmes de 60 s", p="Três histórias para anunciar: dor, virada, produto real, prova científica e chamada. Vertical 1080×1920, legíveis no mudo.", zip="Baixar os 3 filmes (ZIP)", dl="Baixar MP4",
               t=[("A página em branco", "São 23h e ainda falta postar. O conteúdo já está escrito na ciência."), ("Sem medo de parecer charlatão", "O medo real de quem é sério, e a ciência como vantagem."), ("Do post ao paciente fiel", "Curtida não paga o aluguel: os 3 passos do funil ACP.")]),
     "en": dict(h="60-second films", p="Three stories to advertise: pain, turn, real product, scientific proof and call to action. Vertical 1080×1920, readable on mute.", zip="Download the 3 films (ZIP)", dl="Download MP4",
               t=[("The blank page", "It's 11 pm and you still have to post. The content is already written, in science."), ("No fear of looking like a quack", "The real fear of serious professionals, and science as the advantage."), ("From post to loyal patient", "Likes don't pay the rent: the 3 steps of the ACP funnel.")])}
CSS = ".films{max-width:1320px;margin:0 auto;padding:8px 24px 36px}.films h2.s{font-family:Georgia,serif;font-weight:400;font-size:34px;margin:18px 0 6px;text-align:center}.films>p{text-align:center;color:#565452;margin:0 auto 18px;max-width:720px}.fg{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:24px;max-width:1100px;margin:0 auto 20px}.fg video{width:100%;border-radius:14px;display:block;background:#191E47}.fg .card p{font-size:14px;color:#565452;line-height:1.45;margin:0 4px 12px}.fg .btn{width:100%;justify-content:center;margin-top:12px}h2.s2{font-family:Georgia,serif;font-weight:400;font-size:34px;text-align:center;margin:10px 0 18px}"
(ROOT / "zips").mkdir(exist_ok=True)
for l, c in F.items():
    out = ROOT / l / "films"
    if out.exists(): shutil.rmtree(out)
    out.mkdir()
    cards = ""
    with zipfile.ZipFile(ROOT / f"zips/mydose-scale-films-{l}.zip", "w", zipfile.ZIP_STORED) as z:
        for n, (ttl, desc) in enumerate(c["t"], 1):
            f = SRC / f"Filme{n}{l.upper()}.mp4"; name = f"mydose-scale-film{n}-{l}.mp4"
            shutil.copy(f, out / name); z.write(f, f"mydose-scale-films-{l}/{name}")
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "4", "-i", str(f), "-frames:v", "1", "-vf", "scale=540:-1", str(out / f"poster{n}.jpg")])
            cards += f'<div class="card"><h2><small>0{n}</small>{ttl}</h2><p>{desc}</p><video controls preload="none" playsinline poster="films/poster{n}.jpg" src="films/{name}"></video><a class="btn" download href="films/{name}">↓ {c["dl"]}</a></div>'
    sec = (f'<!--films--><style>{CSS}</style><section class="films"><h2 class="s">{c["h"]}</h2><p>{c["p"]}</p><div class="fg">{cards}</div>'
           f'<div class="bar"><a class="btn" href="{REL}/mydose-scale-films-{l}.zip">↓ {c["zip"]}</a></div></section><h2 class="s2">{"Anúncios" if l == "pt" else "Ads"} · 4:5 + 9:16</h2><!--/films-->')
    p = ROOT / l / "index.html"; s = p.read_text(encoding="utf-8")
    s = re.sub(r"<!--films-->[\s\S]*?<!--/films-->", "", s).replace("</header><main>", "</header>" + sec + "<main>", 1)
    p.write_text(s, encoding="utf-8"); print("ok", l)
