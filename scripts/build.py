#!/usr/bin/env python3
"""Build the five-language static site. Python 3, standard library only."""
from pathlib import Path
from html import escape
import json
import re
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
ORIGIN = 'https://www.foscolo.com.br'
EMAIL = 'contato@foscolo.com'
BR = 'https://www.amazon.com.br/dp/6502080553'
INSTAGRAM = 'https://www.instagram.com/foscolocompany/'
ROUTES = {
 'pt': ['index','publicacoes','caderno','repertorio','sobre','autora','contato','projetos','manifesto','imprensa'],
 'en': ['index','publications','journal','repertoire','about','author','contact','projects','manifesto','press'],
 'es': ['index','publicaciones','cuaderno','repertorio','sobre','autora','contacto','proyectos','manifiesto','prensa'],
 'fr': ['index','publications','carnet','repertoire','a-propos','autrice','contact','projets','manifeste','presse'],
 'zh': ['index','publications','journal','repertoire','about','author','contact','projects','manifesto','press']
}
KEYS = ['home','catalog','journal','repertoire','about','author','contact','projects','manifesto','press']
for lang in ROUTES:
 ROUTES[lang] = dict(zip(KEYS, ROUTES[lang])) | {'notes':'notes-on-care', 'todos':'todos-ou-nenhum', 'essay':'caderno-01', 'article':'por-dentro-da-edicao'}
DATA = {lang:json.loads((ROOT/'content'/f'{lang}.json').read_text()) for lang in ROUTES if (ROOT/'content'/f'{lang}.json').exists()}
LEGACY = json.loads((ROOT/'content/legacy.json').read_text())
TITLES = ['A matéria aprende a respirar','Reconhecimentos emprestados','Tratado sobre a arte de não sangrar em vão','NICE AND EASY','Receituário de Morfina','Acolher não é ficar','Arquitetura da continuidade','O ar que a chama não via','A pressão não basta','Sobre permanecer em fusão','O tempo do recozimento','Entre o fogo e a colher','Como chegamos até aqui?','A largura das coisas','Não é só luminosidade','Recomeço em órbita própria']

def e(value): return escape(str(value), quote=True)
def path(lang,key): return f'/{lang}/{ROUTES[lang][key]}.html'
def nl(value): return e(value).replace('\n','<br>')
def paragraphs(values): return ''.join(f'<p>{e(v)}</p>' for v in values)
def link(href,label,cls='text-link',external=False):
 return f'<a class="{cls}" href="{e(href)}"'+(' rel="noopener noreferrer"' if external else '')+f'>{e(label)}<span aria-hidden="true"> ↗</span></a>'
def image(name,alt,cls='',eager=False):
 sizes={'notes-brasil.webp':(994,1536),'todos-forest.webp':(766,1191),'todos-title.webp':(766,1191),'todos-prologue.webp':(766,1191),'notes-international.webp':(600,900)}
 w,h=sizes.get(name,(1000,1000))
 return f'<img src="/assets/images/{name}" alt="{e(alt)}" class="{cls}" width="{w}" height="{h}" decoding="async" '+('fetchpriority="high"' if eager else 'loading="lazy"')+'>'
def section_head(number,title,intro=''):
 return f'<div class="section-head"><span class="index-number" aria-hidden="true">{number}</span><div><h2>{nl(title)}</h2>'+ (f'<p>{e(intro)}</p>' if intro else '')+'</div></div>'
def tiles(items):
 return '<div class="three-columns">'+''.join(f'<div class="text-card"><span class="eyebrow" aria-hidden="true">0{i+1}</span><h3>{e(a)}</h3><p>{e(b)}</p></div>' for i,(a,b) in enumerate(items))+'</div>'
def hero(d,title,intro='',eyebrow='',small=False):
 return f'<section class="page-hero wrap {"compact" if small else ""}"><p class="eyebrow">{e(eyebrow or d["ui"]["edition"])}</p><h1>{nl(title)}</h1>'+ (f'<p class="lead">{e(intro)}</p>' if intro else '')+'</section>'
def bookcards(lang,d):
 u=d['ui'];cards=[]
 for key,art,title in [('notes','notes-brasil.webp','Notes on Care, Risk & Knowledge'),('todos','todos-forest.webp','Todos ou nenhum?')]:
  b=d[key]; status=u['published'] if key=='notes' else u['forthcoming']
  cards.append(f'<article class="book-card {key}"><a class="book-art" href="{path(lang,key)}">'+image(art,title)+f'</a><div class="book-copy"><p class="eyebrow">{e(status)}</p><h3><a href="{path(lang,key)}">{e(title)}</a></h3><p class="subtitle">{e(b["subtitle"])}</p><p>{e(b["description"])}</p>'+link(path(lang,key),u['discover'])+'</div></article>')
 return '<div class="book-grid">'+''.join(cards)+'</div>'
def journalcards(lang,d):
 j=d['journal'];u=d['ui']
 return '<div class="journal-grid">'+f'<article class="journal-card"><a class="journal-art forest" href="{path(lang,"article")}">'+image('todos-prologue.webp',d['article']['caption'])+f'</a><p class="eyebrow">{e(j["newMeta"])}</p><h3><a href="{path(lang,"article")}">{e(j["newTitle"])}</a></h3><p>{e(j["newDesc"])}</p>'+link(path(lang,'article'),u['read'])+'</article>'+f'<article class="journal-card"><a class="journal-art notes-art" href="{path(lang,"essay")}">'+image('notes-brasil.webp','Notes on Care, Risk & Knowledge')+f'</a><p class="eyebrow">{e(u["previous"])}</p><h3><a href="{path(lang,"essay")}">{e(j["originalTitle"])}</a></h3><p>{e(j["originalDesc"])}</p>'+link(path(lang,'essay'),u['read'])+'</article></div>'
def contactband(lang,d,text=None):
 return f'<section class="contact-band"><div class="wrap split"><h2>{e(d["ui"]["contact"])}</h2><div><p>{e(text or d["contact"]["intro"])}</p>'+link('mailto:'+EMAIL,EMAIL,'button gold')+'</div></div></section>'
def content(lang,key,d):
 u=d['ui'];h=d['home'];n=d['notes'];t=d['todos']
 if key=='home':
  return f'<section class="home-hero wrap"><div class="hero-copy"><p class="eyebrow">{e(h["eyebrow"])} · BH / BR</p><h1>{nl(h["title"])}</h1><p class="lead">{e(h["intro"])}</p><div class="actions">'+link(path(lang,'catalog'),u['catalog'],'button dark')+link(path(lang,'about'),d['nav'][4])+'</div></div><div class="hero-feature"><a class="hero-art" href="'+path(lang,'todos')+'">'+image('todos-forest.webp',u['proof'],'',True)+f'</a><div class="feature-caption"><p class="eyebrow">{e(h["feature"])}</p><h2><a href="{path(lang,"todos")}">Todos ou nenhum?</a></h2><p>{e(t["subtitle"])}</p></div></div></section><div class="ticker" aria-hidden="true"><span>FÓSCOLO & COMPANY</span><span>{e(h["eyebrow"])}</span><span>BELO HORIZONTE · BRASIL</span></div><section class="wrap section">'+section_head('01',h['catalogTitle'],h['catalogIntro'])+bookcards(lang,d)+'</section><section class="ink-section"><div class="wrap section">'+section_head('02',h['journalTitle'],h['journalIntro'])+journalcards(lang,d)+'</div></section><section class="wrap section split about-teaser"><div><p class="eyebrow">Fóscolo & Company Edições</p><h2>'+nl(h['aboutTitle'])+'</h2></div><div><p class="lead">'+e(h['aboutText'])+'</p>'+link(path(lang,'about'),u['more'])+'</div></section>'+contactband(lang,d)
 if key=='catalog':
  c=d['catalog'];return hero(d,c['title'],c['intro'],d['nav'][1])+f'<section class="wrap section top-line">{bookcards(lang,d)}</section><section class="wrap section">'+section_head('02',c['linesTitle'])+tiles(c['lines'])+'</section>'
 if key in ('notes','todos'):
  b=d[key];isnotes=key=='notes';title='Notes on Care, Risk & Knowledge' if isnotes else 'Todos ou nenhum?'
  art='notes-brasil.webp' if isnotes else 'todos-forest.webp'
  body=f'<section class="wrap book-hero"><div class="book-hero-image {key}">'+image(art,title,'',True)+f'<p class="caption">{e(n["brTitle"] if isnotes else u["proof"])}</p></div><div><p class="eyebrow">{e(u["published"] if isnotes else u["forthcoming"])}</p><h1>{e(title)}</h1><p class="book-subtitle">{e(b["subtitle"])}</p><p class="byline">Maria Carolina Fóscolo'+(' Gomes' if isnotes else '')+f'</p><p class="lead">{e(b["description"])}</p><div class="actions">'+(link('#editions',u['formats'],'button dark')+link('/assets/press/notes-on-care-sample.pdf',u['download']) if isnotes else link('#excerpt',u['read'],'button dark'))+'</div>'
  if not isnotes: body+=f'<p class="status-note">{e(t["status"])}</p>'
  body+='</div></section>'
  if isnotes:
   body+='<section class="wrap section top-line">'+tiles(n['sections'])+'</section><section class="paper-deep" id="editions"><div class="wrap section">'+section_head('02',u['formats'])+f'<div class="edition-grid"><article class="edition-card"><p class="eyebrow">BR</p><h3>{e(n["brTitle"])}</h3><p>{e(n["brText"])}</p><dl class="facts">'
   for a,bv in [(n['languageLabel'],n['languageValue']),(n['pagesLabel'],n['pagesValue']),(n['sizeLabel'],'10 × 15 cm'),(n['publisherLabel'],'Fóscolo & Company Edições')]:body+=f'<div><dt>{e(a)}</dt><dd>{e(bv)}</dd></div>'
   body+='</dl>'+link(BR,u['buyBR'],'button dark',True)+f'</article><article class="edition-card"><p class="eyebrow">KDP</p><h3>{e(n["internationalTitle"])}</h3><p>{e(n["internationalText"])}</p><ul class="edition-links">'
   for label,asin in [('Kindle','B0H7L24BDH'),('Paperback','6502080553'),('Hardcover','6502203957')]:body+='<li>'+link('https://www.amazon.com/dp/'+asin,label,external=True)+'</li>'
   body+=f'</ul><p class="caption">{e(u["availability"])}</p></article></div></div></section><section class="wrap section split"><h2>{e(n["sampleTitle"])}</h2><div><p>{e(n["sampleText"])}</p>'+link('/assets/press/notes-on-care-sample.pdf',u['download'],'button dark')+'</div></section>'
  else:
   body+=f'<section class="ink-section"><div class="wrap section split"><h2>{e(t["question"])}</h2><div><p class="lead">{e(t["body"])}</p><p>{e(t["body2"])}</p></div></div></section><section class="wrap section excerpt" id="excerpt"><p class="eyebrow">{e(u["original"])}</p><h2>{e(t["excerptTitle"])}</h2><p>{e(t["excerptIntro"])}</p><blockquote lang="pt-BR">{e(t["excerpt"])}</blockquote><blockquote class="excerpt-lines" lang="pt-BR">{nl(t["excerpt2"])}</blockquote><p class="caption">{e(t["excerptCredit"])}</p></section><section class="paper-deep"><div class="wrap section"><h2>{e(u["contents"])}</h2><ol class="contents" lang="pt-BR">'+''.join(f'<li>{e(v)}</li>' for v in TITLES)+f'</ol><p class="caption">{e(t["formValue"])} · {e(t["languageValue"])}</p></div></section><section class="wrap section split"><h2>{e(t["inside"])}</h2><div><p>{e(t["insideText"])}</p>'+link(path(lang,'article'),u['read'],'button dark')+'</div></section>'
  return body
 if key=='journal':
  j=d['journal'];return hero(d,j['title'],j['intro'])+'<section class="wrap section top-line">'+journalcards(lang,d)+f'</section><section class="wrap section split"><h2>{e(d["repertoire"]["title"])}</h2><div><p>{e(j["instagramText"])}</p>'+link(path(lang,'repertoire'),d['nav'][3],'button dark')+'</div></section>'
 if key=='article':
  a=d['article'];return hero(d,a['title'],a['intro'],d['journal']['newMeta'],True)+f'<article class="prose wrap"><p class="byline">Fóscolo & Company Edições</p>'+paragraphs(a['paragraphs'][:2])+f'<figure class="page-proof">'+image('todos-prologue.webp',a['caption'])+f'<figcaption>{e(a["caption"])}</figcaption></figure>'+paragraphs(a['paragraphs'][2:])+'<div class="actions">'+link(path(lang,'todos'),u['discover'],'button dark')+link(path(lang,'journal'),u['back'])+'</div></article>'
 if key=='essay':
  old=LEGACY[lang]['essay'];match=re.search(r'<div class="article-body">([\s\S]*?)</div>',old)
  article=match.group(1) if match else ''.join(re.findall(r'<p[^>]*>[\s\S]*?</p>',old))
  return hero(d,d['journal']['originalTitle'],'',u['previous'],True)+'<article class="prose wrap"><p class="byline">Maria Carolina Fóscolo Gomes</p>'+article+'<div class="actions">'+link(path(lang,'notes'),u['discover'],'button dark')+link(path(lang,'journal'),u['back'])+'</div></article>'
 if key=='repertoire':
  r=d['repertoire'];return hero(d,r['title'],r['intro'])+f'<section class="ink-section"><div class="wrap section split"><h2>{e(r["heading"])}</h2><div>'+paragraphs(r['paragraphs'])+'</div></div></section><section class="wrap section">'+tiles(r['lenses'])+f'<p class="lead section-end">{e(r["closing"])}</p>'+link(INSTAGRAM,u['instagram'],'button dark',True)+'</section>'
 if key=='about':
  a=d['about'];return hero(d,a['title'],a['intro'])+'<section class="wrap section split top-line"><div class="seal-block">'+image('seal.png','Fóscolo & Company Edições')+'</div><div class="lead">'+paragraphs(a['paragraphs'])+'</div></section><section class="wrap section">'+tiles(a['values'])+f'</section><section class="ink-section"><div class="wrap section split"><h2>{e(a["manifestoTitle"])}</h2><div><p>{e(a["manifestoText"])}</p>'+link(path(lang,'manifesto'),d['nav'][8],'button gold')+'</div></div></section>'
 if key=='projects':
  p=d['projects'];return hero(d,p['title'],p['intro'])+'<section class="wrap section top-line">'+bookcards(lang,d)+'</section><section class="wrap section">'+tiles(p['steps'])+'</section>'+contactband(lang,d,p['contactText'])
 if key=='author':
  a=d['author'];return hero(d,a['title'],a['intro'])+'<section class="wrap section split top-line"><div class="monogram" aria-hidden="true">MCF<span>Belo Horizonte / Brasil</span></div><div class="prose-inline">'+paragraphs(a['paragraphs'])+link('https://orcid.org/0009-0000-6000-2751',a['orcid'],'button dark',True)+f'</div></section><section class="paper-deep"><div class="wrap section split"><h2>{e(a["researchTitle"])}</h2><p class="lead">{e(a["researchText"])}</p></div></section><section class="wrap section">'+bookcards(lang,d)+'</section>'
 if key=='press':
  p=d['press'];return hero(d,p['title'],p['intro'])+f'<section class="wrap section top-line"><div class="edition-grid"><article class="edition-card"><h2>Notes on Care, Risk & Knowledge</h2><p>{e(n["description"])}</p><div class="stack-links">'+link('/assets/press/notes-on-care-sample.pdf',u['download'])+link('/assets/images/notes-brasil.webp',u['cover'])+link(path(lang,'notes'),u['formats'])+f'</div><p class="caption">{e(u["sampleNote"])}</p></article><article class="edition-card"><p class="eyebrow">{e(u["forthcoming"])}</p><h2>Todos ou nenhum?</h2><p>{e(t["description"])}</p><p class="caption">{e(p["todosNote"])}</p>'+link('/assets/images/todos-title.webp',p['todosAsset'])+f'</article></div></section><section class="wrap section split"><h2>{e(p["bioTitle"])}</h2><p class="lead">{e(p["bio"])}</p></section>'+contactband(lang,d,p['request'])
 if key=='contact':
  c=d['contact'];return hero(d,c['title'],c['intro'])+f'<section class="wrap section split top-line"><div><p class="eyebrow">{e(c["location"])}</p><a class="contact-email" href="mailto:{EMAIL}?subject={quote(c["subject"])}">{EMAIL}</a><p>{e(c["socialText"])}</p>'+link(INSTAGRAM,'@foscolocompany',external=True)+f'</div><div class="text-card"><h2>{e(c["tipsTitle"])}</h2><ul class="plain-list">'+''.join(f'<li>{e(v)}</li>' for v in c['tips'])+f'</ul></div></section><div class="wrap privacy-note"><p>{e(u["privacy"])}</p></div>'
 if key=='manifesto':
  old=LEGACY[lang]['manifesto'].replace('Fóscolo & Company Editora','Fóscolo & Company Edições')
  blocks=re.findall(r'<(?:p|h2|blockquote)\b[^>]*>[\s\S]*?</(?:p|h2|blockquote)>',old)
  return hero(d,d['manifestoTitle'],'',d['nav'][8],True)+'<article class="prose wrap manifesto-prose">'+''.join(blocks)+'</article>'
 raise ValueError(key)

def page(lang,key,body,d,root=False):
 u=d['ui']; nav=d['nav']; canonical=ORIGIN+('/' if root else path(lang,key))
 titles={'home':'Fóscolo & Company Edições','notes':'Notes on Care, Risk & Knowledge','todos':'Todos ou nenhum? — Livro I','essay':d['journal']['originalTitle'],'article':d['article']['title']}
 title=titles.get(key,nav[KEYS.index(key)] if key in KEYS else key)
 desc=d[key].get('intro',d[key].get('description','')) if key in d and isinstance(d[key],dict) else d['home']['intro']
 desc=desc or d['home']['intro']
 navhtml=''.join(f'<a href="{path(lang,k)}"'+(' aria-current="page"' if k==key else '')+f'>{e(nav[KEYS.index(k)])}</a>' for k in ['catalog','journal','repertoire','about','author','contact'])
 languages=''.join(f'<a href="{path(l,key)}" lang="{DATA[l]["lang"]}" hreflang="{DATA[l]["lang"]}"'+(' aria-current="true"' if l==lang else '')+f'>{e({"pt":"PT","en":"EN","es":"ES","fr":"FR","zh":"中文"}[l])}</a>' for l in DATA)
 alternates=''.join(f'<link rel="alternate" hreflang="{DATA[l]["lang"]}" href="{ORIGIN+path(l,key)}">' for l in DATA)
 ogimg=ORIGIN+'/assets/images/'+('todos-forest.webp' if key in ['todos','article'] else 'notes-brasil.webp')
 schema={'@context':'https://schema.org','@type':'WebPage','name':title,'description':desc,'url':canonical,'inLanguage':d['lang'],'publisher':{'@type':'Organization','name':'Fóscolo & Company Edições','url':ORIGIN,'email':EMAIL,'sameAs':[INSTAGRAM]}}
 if key in ['notes','todos']:
  schema['mainEntity']={'@type':'Book','name':titles[key],'author':{'@type':'Person','name':'Maria Carolina Fóscolo'},'inLanguage':'en' if key=='notes' else 'pt-BR','publisher':{'@type':'Organization','name':'Fóscolo & Company Edições'}}
  if key=='notes': schema['mainEntity']['bookFormat']='https://schema.org/Paperback';schema['mainEntity']['numberOfPages']=64
 footerlinks=''.join(link(path(lang,k),nav[KEYS.index(k)],'footer-link') for k in ['catalog','projects','manifesto','press','contact'])
 return f'''<!doctype html>
<html lang="{d['lang']}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(title)}{' | Fóscolo & Company' if key!='home' else ''}</title><meta name="description" content="{e(desc)}"><meta name="theme-color" content="#F5F2EB"><link rel="icon" href="/favicon.png"><link rel="canonical" href="{canonical}">{alternates}<link rel="alternate" hreflang="x-default" href="{ORIGIN+path('pt',key)}"><meta property="og:type" content="website"><meta property="og:site_name" content="Fóscolo & Company Edições"><meta property="og:locale" content="{d['locale']}"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{canonical}"><meta property="og:image" content="{ogimg}"><meta name="twitter:card" content="summary_large_image"><link rel="stylesheet" href="/assets/fonts/fonts.css"><link rel="stylesheet" href="/assets/fonts/chinese.css"><link rel="stylesheet" href="/assets/site.css"><script src="/assets/site.js" defer></script><script type="application/ld+json">{json.dumps(schema,ensure_ascii=False).replace('</','<\\/')}</script></head>
<body><a class="skip-link" href="#main">{e(u['skip'])}</a><header class="site-header"><div class="wrap header-inner"><a class="brand" href="{path(lang,'home')}" aria-label="Fóscolo & Company — {e(nav[0])}"><img src="/assets/images/logo.png" width="240" height="85" alt="Fóscolo & Company Edições"></a><button class="menu-toggle" aria-expanded="false" aria-controls="main-nav" data-open="{e(u['open'])}" data-close="{e(u['close'])}" aria-label="{e(u['open'])}" hidden>{e(u['menu'])}<span aria-hidden="true"> +</span></button><nav id="main-nav" class="main-nav" aria-label="{e(u['menu'])}">{navhtml}</nav></div><div class="wrap language-bar"><span>{e(u['edition'])}</span><nav aria-label="{e(u['languages'])}">{languages}</nav></div></header>
<main id="main">{body}</main><footer class="site-footer"><div class="wrap footer-grid"><div><p class="footer-wordmark">FÓSCOLO<br>& COMPANY<span>EDIÇÕES</span></p><p>{nl(d['home']['title'])}</p></div><nav aria-label="{e(u['more'])}">{footerlinks}</nav><div><p class="eyebrow">{e(d['contact']['location'])}</p><p><a href="mailto:{EMAIL}">{EMAIL}</a></p>{link(INSTAGRAM,'Instagram','footer-link',True)}</div></div><div class="wrap footer-bottom"><span>© 2026 Fóscolo & Company Edições. {e(u['rights'])}</span><span>{e(u['updated'])}</span></div></footer></body></html>'''

def build():
 outputs=[]
 for lang,d in DATA.items():
  for key,slug in ROUTES[lang].items():
   dest=ROOT/lang/(slug+'.html');dest.parent.mkdir(exist_ok=True);dest.write_text(page(lang,key,content(lang,key,d),d));outputs.append(path(lang,key))
 (ROOT/'index.html').write_text(page('pt','home',content('pt','home',DATA['pt']),DATA['pt'],root=True))
 # The existing language selector is replaced by a complete Portuguese home.
 (ROOT/'404.html').write_text('<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>Página não encontrada | Fóscolo & Company</title><link rel="stylesheet" href="/assets/fonts/chinese.css"><link rel="stylesheet" href="/assets/site.css"></head><body><main class="wrap page-hero"><p class="eyebrow">404</p><h1>Esta página mudou de lugar.</h1><p>Encontre livros, leituras e informações da editora a partir da página inicial.</p><a class="button dark" href="/pt/index.html">Ir para o início</a><p><a href="/en/index.html" lang="en">English</a> · <a href="/es/index.html" lang="es">Español</a> · <a href="/fr/index.html" lang="fr">Français</a> · <a href="/zh/index.html" lang="zh-CN">中文</a></p></main></body></html>')
 sitemap='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'<url><loc>{ORIGIN+p}</loc><lastmod>2026-09-28</lastmod></url>\n' for p in ['/']+outputs)+'</urlset>\n'
 (ROOT/'sitemap.xml').write_text(sitemap)
 (ROOT/'robots.txt').write_text(f'User-agent: *\nAllow: /\nSitemap: {ORIGIN}/sitemap.xml\n')
 (ROOT/'.nojekyll').touch()
 print(f'Built {len(outputs)+2} HTML pages in {len(DATA)} languages.')

if __name__=='__main__': build()
