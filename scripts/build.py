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
 'pt': {
  'home':'index','catalog':'publicacoes','journal':'caderno','repertoire':'repertorio','about':'sobre','author':'autora','contact':'contato','projects':'projetos','manifesto':'manifesto','press':'imprensa',
  'notes':'notes-on-care','todos':'todos-ou-nenhum','essay':'caderno-01','article':'por-dentro-da-edicao','research':'pesquisa',
  'circulation':'publicar-nao-encerra','place':'de-que-lugar-esta-mesa-olha-o-mundo','space':'o-vazio-tambem-e-uma-decisao-editorial','repertoire2':'repertorio-02-missa-do-galo'
 },
 'en': {
  'home':'index','catalog':'publications','journal':'journal','repertoire':'repertoire','about':'about','author':'author','contact':'contact','projects':'projects','manifesto':'manifesto','press':'press',
  'notes':'notes-on-care','todos':'todos-ou-nenhum','essay':'caderno-01','article':'por-dentro-da-edicao','research':'research',
  'circulation':'publishing-does-not-end','place':'where-does-this-table-look-from','space':'empty-space-is-an-editorial-decision','repertoire2':'repertoire-02-missa-do-galo'
 },
 'es': {
  'home':'index','catalog':'publicaciones','journal':'cuaderno','repertoire':'repertorio','about':'sobre','author':'autora','contact':'contacto','projects':'proyectos','manifesto':'manifiesto','press':'prensa',
  'notes':'notes-on-care','todos':'todos-ou-nenhum','essay':'caderno-01','article':'por-dentro-da-edicao','research':'investigacion',
  'circulation':'publicar-no-termina','place':'desde-que-lugar-mira-el-mundo-esta-mesa','space':'el-vacio-tambien-es-una-decision-editorial','repertoire2':'repertorio-02-missa-do-galo'
 },
 'fr': {
  'home':'index','catalog':'publications','journal':'carnet','repertoire':'repertoire','about':'a-propos','author':'autrice','contact':'contact','projects':'projets','manifesto':'manifeste','press':'presse',
  'notes':'notes-on-care','todos':'todos-ou-nenhum','essay':'caderno-01','article':'por-dentro-da-edicao','research':'recherche',
  'circulation':'publier-ne-clot-pas','place':'depuis-quel-endroit-cette-table-regarde-le-monde','space':'le-vide-est-aussi-une-decision-editoriale','repertoire2':'repertoire-02-missa-do-galo'
 },
 'zh': {
  'home':'index','catalog':'publications','journal':'journal','repertoire':'repertoire','about':'about','author':'author','contact':'contact','projects':'projects','manifesto':'manifesto','press':'press',
  'notes':'notes-on-care','todos':'todos-ou-nenhum','essay':'caderno-01','article':'por-dentro-da-edicao','research':'research',
  'circulation':'publishing-does-not-end','place':'where-does-this-table-look-from','space':'empty-space-editorial-decision','repertoire2':'repertoire-02-missa-do-galo'
 }
}
NAV_KEYS = ['home','catalog','journal','repertoire','about','author','contact','projects','manifesto','press']
NAV_INDEX = {k:i for i,k in enumerate(NAV_KEYS)}
DATA = {lang:json.loads((ROOT/'content'/f'{lang}.json').read_text()) for lang in ROUTES}
LEGACY = json.loads((ROOT/'content/legacy.json').read_text())
ARTICLE_DATA = {'circulation':'circulationArticle','place':'placeArticle','space':'spaceArticle','repertoire2':'repertoireArticle'}

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
def researchcards(d):
 return '<div class="research-grid">'+''.join(f'<article class="research-card"><p class="eyebrow">0{i+1}</p><h3>{e(a)}</h3><p>{e(b)}</p></article>' for i,(a,b) in enumerate(d['research']['questions']))+'</div>'
def circulationlist(d):
 return '<div class="circulation-list">'+''.join(f'<article class="circulation-item"><p class="eyebrow">{e(meta)}</p><div><h3>{e(title)}</h3><p>{e(body)}</p></div></article>' for meta,title,body in d['research']['circulation'])+'</div>'
def hero(d,title,intro='',eyebrow='',small=False):
 return f'<section class="page-hero wrap {"compact" if small else ""}"><p class="eyebrow">{e(eyebrow or d["ui"]["edition"])}</p><h1>{nl(title)}</h1>'+ (f'<p class="lead">{e(intro)}</p>' if intro else '')+'</section>'
def bookcards(lang,d):
 u=d['ui'];cards=[]
 for key,art,title in [('notes','notes-brasil.webp','Notes on Care, Risk & Knowledge'),('todos','todos-forest.webp','Todos ou nenhum?')]:
  b=d[key];status=u['published'] if key=='notes' else u['forthcoming']
  cards.append(f'<article class="book-card {key}"><a class="book-art" href="{path(lang,key)}">'+image(art,title)+f'</a><div class="book-copy"><p class="eyebrow">{e(status)}</p><h3><a href="{path(lang,key)}">{e(title)}</a></h3><p class="subtitle">{e(b["subtitle"])}</p><p>{e(b["description"])}</p>'+link(path(lang,key),u['discover'])+'</div></article>')
 return '<div class="book-grid">'+''.join(cards)+'</div>'
def journalcards(lang,d,limit=None):
 entries=d['journal']['entries'][:limit] if limit else d['journal']['entries']
 cards=[]
 for entry in entries:
  key=entry['key'];href=path(lang,key)
  if key=='article':
   visual=f'<a class="journal-art forest" href="{href}">'+image('todos-forest.webp',entry['title'])+'</a>'
  elif key=='essay':
   visual=f'<a class="journal-art notes-art" href="{href}">'+image('notes-brasil.webp','Notes on Care, Risk & Knowledge')+'</a>'
  else:
   visual=f'<a class="journal-art journal-text-art" href="{href}"><span class="journal-text-mark">F&amp;C</span><strong>{e(entry["title"])}</strong></a>'
  cards.append(f'<article class="journal-card">{visual}<p class="eyebrow">{e(entry["meta"])}</p><h3><a href="{href}">{e(entry["title"])}</a></h3><p>{e(entry["desc"])}</p>'+link(href,d['ui']['read'])+'</article>')
 return '<div class="journal-grid archive-grid">'+''.join(cards)+'</div>'
def contactband(lang,d,text=None):
 return f'<section class="contact-band"><div class="wrap split"><h2>{e(d["ui"]["contact"])}</h2><div><p>{e(text or d["contact"]["intro"])}</p>'+link('mailto:'+EMAIL,EMAIL,'button gold')+'</div></div></section>'
def generic_article(lang,d,key):
 a=d[ARTICLE_DATA[key]]
 target={'circulation':'notes','place':'about','space':'journal'}[key]
 actions=link(path(lang,target),a['cta'],'button dark')
 if target!='journal': actions+=link(path(lang,'journal'),d['ui']['back'])
 return hero(d,a['title'],a['intro'],a['meta'],True)+f'<article class="prose wrap"><p class="byline">Fóscolo & Company Edições</p>'+paragraphs(a['paragraphs'])+f'<div class="actions">{actions}</div></article>'

def content(lang,key,d):
 u=d['ui'];h=d['home'];n=d['notes'];t=d['todos']
 if key=='home':
  sale=f'<section class="wrap section home-sale">'+section_head('01',h['saleTitle'],h['saleIntro'])+f'<div class="home-sale-panel top-line"><div><p class="eyebrow">{e(h["saleEyebrow"])}</p><h2>Notes on Care, Risk & Knowledge</h2></div><div><p class="lead">{e(n["description"])}</p><div class="actions">'+link(BR,u['buyBR'],'button dark',True)+link('/assets/press/notes-on-care-sample.pdf',u['download'])+'</div></div></div></section>'
  research=f'<section class="paper-deep"><div class="wrap section">'+section_head('02',h['researchTitle'],h['researchIntro'])+researchcards(d)+f'<div class="actions">'+link(path(lang,'research'),d['research']['nav'],'button dark')+'</div></div></section>'
  editorial=f'<section class="wrap section split top-line"><h2>{e(d["editorial"][0][0])}</h2><div><p class="lead">{e(d["editorial"][0][1])}</p>'+link(path(lang,'journal'),d['nav'][2])+'</div></section>'
  return f'<section class="home-hero wrap"><div class="hero-copy"><p class="eyebrow">{e(h["eyebrow"])} · BH / BR</p><h1>{nl(h["title"])}</h1><p class="lead">{e(h["intro"])}</p><div class="actions">'+link(BR,u['buyBR'],'button dark',True)+link(path(lang,'catalog'),u['catalog'])+'</div></div><div class="hero-feature"><a class="hero-art" href="'+path(lang,'notes')+'">'+image('notes-brasil.webp','Notes on Care, Risk & Knowledge','',True)+f'</a><div class="feature-caption"><p class="eyebrow">{e(u["published"])}</p><h2><a href="{path(lang,"notes")}">Notes on Care, Risk & Knowledge</a></h2><p>{e(n["subtitle"])}</p></div></div></section><div class="ticker" aria-hidden="true"><span>FÓSCOLO & COMPANY</span><span>{e(h["eyebrow"])}</span><span>BELO HORIZONTE · BRASIL</span></div>'+sale+research+'<section class="wrap section">'+section_head('03',h['catalogTitle'],h['catalogIntro'])+bookcards(lang,d)+'</section><section class="ink-section"><div class="wrap section">'+section_head('04',h['journalTitle'],h['journalIntro'])+journalcards(lang,d,3)+'</div></section>'+editorial+'<section class="wrap section split about-teaser"><div><p class="eyebrow">Fóscolo & Company Edições</p><h2>'+nl(h['aboutTitle'])+'</h2></div><div><p class="lead">'+e(h['aboutText'])+'</p>'+link(path(lang,'about'),u['more'])+'</div></section>'+contactband(lang,d)
 if key=='catalog':
  c=d['catalog'];return hero(d,c['title'],c['intro'],d['nav'][1])+'<section class="wrap section top-line">'+bookcards(lang,d)+'</section><section class="wrap section">'+section_head('02',c['linesTitle'])+tiles(c['lines'])+'</section>'
 if key=='notes':
  body=f'<section class="wrap book-hero"><div class="book-hero-image notes">'+image('notes-brasil.webp','Notes on Care, Risk & Knowledge','',True)+f'<p class="caption">{e(n["brTitle"])}</p></div><div><p class="eyebrow">{e(u["published"])}</p><h1>Notes on Care, Risk & Knowledge</h1><p class="book-subtitle">{e(n["subtitle"])}</p><p class="byline">Maria Carolina Fóscolo Gomes</p><p class="lead">{e(n["description"])}</p><div class="actions">'+link(BR,u['buyBR'],'button dark',True)+link('/assets/press/notes-on-care-sample.pdf',u['download'])+link('#editions',u['formats'])+'</div></div></section>'
  body+='<section class="wrap section top-line">'+tiles(n['sections'])+'</section><section class="wrap section notes-reader">'+section_head('02',n['readerTitle'])+tiles(n['readerItems'])+'</section><section class="paper-deep" id="editions"><div class="wrap section">'+section_head('03',u['formats'])+f'<div class="edition-grid"><article class="edition-card"><p class="eyebrow">BR</p><h3>{e(n["brTitle"])}</h3><p>{e(n["brText"])}</p><dl class="facts">'
  for a,bv in [(n['languageLabel'],n['languageValue']),(n['pagesLabel'],n['pagesValue']),(n['sizeLabel'],'10 × 15 cm'),(n['publisherLabel'],'Fóscolo & Company Edições')]: body+=f'<div><dt>{e(a)}</dt><dd>{e(bv)}</dd></div>'
  body+='</dl>'+link(BR,u['buyBR'],'button dark',True)+f'</article><article class="edition-card"><p class="eyebrow">KDP</p><h3>{e(n["internationalTitle"])}</h3><p>{e(n["internationalText"])}</p><ul class="edition-links">'
  for label,asin in [('Kindle','B0H7L24BDH'),('Paperback','6502080553'),('Hardcover','6502203957')]: body+='<li>'+link('https://www.amazon.com/dp/'+asin,label,external=True)+'</li>'
  body+=f'</ul><p class="caption">{e(u["availability"])}</p></article></div></div></section><section class="wrap section split"><h2>{e(n["sampleTitle"])}</h2><div><p>{e(n["sampleText"])}</p>'+link('/assets/press/notes-on-care-sample.pdf',u['download'],'button dark')+f'</div></section><section class="buy-band"><div class="wrap split"><h2>{e(n["buyTitle"])}</h2><div><p>{e(n["buyText"])}</p>'+link(BR,u['buyBR'],'button gold',True)+'</div></div></section>'
  return body
 if key=='todos':
  return f'<section class="wrap book-hero"><div class="book-hero-image todos">'+image('todos-forest.webp','Todos ou nenhum?','',True)+f'<p class="caption">{e(u["proof"])}</p></div><div><p class="eyebrow">{e(u["forthcoming"])}</p><h1>Todos ou nenhum?</h1><p class="book-subtitle">{e(t["subtitle"])}</p><p class="byline">Maria Carolina Fóscolo</p><p class="lead">{e(t["description"])}</p><div class="actions">'+link('#process',t['processCta'],'button dark')+f'</div><p class="status-note">{e(t["status"])}</p></div></section><section class="ink-section" id="process"><div class="wrap section split"><h2>{e(t["question"])}</h2><div><p class="lead">{e(t["body"])}</p><p>{e(t["body2"])}</p></div></div></section><section class="wrap section">'+section_head('02',t['processTitle'],t['processIntro'])+tiles(t['processItems'])+f'</section><section class="paper-deep"><div class="wrap section split"><h2>{e(t["inside"])}</h2><div><p class="lead">{e(t["insideText"])}</p>'+link(path(lang,'article'),u['read'],'button dark')+'</div></div></section>'
 if key=='research':
  r=d['research'];return hero(d,r['title'],r['intro'],r['eyebrow'])+'<section class="wrap section">'+section_head('01',r['questionsTitle'])+researchcards(d)+'</section><section class="paper-deep"><div class="wrap section">'+section_head('02',r['circulationTitle'])+circulationlist(d)+'</div></section><section class="wrap section split top-line"><h2>'+e(r['bridgeTitle'])+'</h2><div><p class="lead">'+e(r['bridgeText'])+'</p><p class="status-note">'+e(r['privateNote'])+'</p><div class="actions">'+link(path(lang,'notes'),r['cta'],'button dark')+link(path(lang,'catalog'),u['catalog'])+'</div></div></section>'
 if key=='journal':
  j=d['journal'];return hero(d,j['title'],j['intro'])+'<section class="wrap section top-line">'+section_head('01',j['archiveTitle'],j['archiveIntro'])+journalcards(lang,d)+'</section><section class="paper-deep"><div class="wrap section split"><h2>'+e(d['repertoire']['title'])+'</h2><div><p>'+e(j['instagramText'])+'</p>'+link(path(lang,'repertoire'),d['nav'][3],'button dark')+'</div></div></section>'
 if key=='article':
  a=d['article'];return hero(d,a['title'],a['intro'],d['journal']['newMeta'],True)+f'<article class="prose wrap"><p class="byline">Fóscolo & Company Edições</p>'+paragraphs(a['paragraphs'])+'<div class="actions">'+link(path(lang,'todos'),u['discover'],'button dark')+link(path(lang,'journal'),u['back'])+'</div></article>'
 if key=='essay':
  old=LEGACY[lang]['essay'];match=re.search(r'<div class="article-body">([\s\S]*?)</div>',old)
  article=match.group(1) if match else ''.join(re.findall(r'<p[^>]*>[\s\S]*?</p>',old))
  return hero(d,d['journal']['originalTitle'],'',u['previous'],True)+'<article class="prose wrap"><p class="byline">Maria Carolina Fóscolo Gomes</p>'+article+'<div class="actions">'+link(path(lang,'notes'),u['discover'],'button dark')+link(path(lang,'journal'),u['back'])+'</div></article>'
 if key in ('circulation','place','space'): return generic_article(lang,d,key)
 if key=='repertoire':
  r=d['repertoire'];f=d['repertoireFeature']
  feature=f'<section class="wrap section repertoire-feature"><p class="eyebrow">{e(f["meta"])}</p><div class="split"><h2>{e(f["title"])}</h2><div><p class="lead">{e(f["desc"])}</p>'+link(path(lang,'repertoire2'),f['cta'],'button dark')+'</div></div></section>'
  return hero(d,r['title'],r['intro'])+f'<section class="ink-section"><div class="wrap section split"><h2>{e(r["heading"])}</h2><div>'+paragraphs(r['paragraphs'])+'</div></div></section>'+feature+'<section class="paper-deep"><div class="wrap section">'+tiles(r['lenses'])+f'<p class="lead section-end">{e(r["closing"])}</p></div></section>'
 if key=='repertoire2':
  a=d['repertoireArticle']
  return hero(d,a['title'],a['intro'],a['meta'],True)+f'<article class="prose wrap"><p class="byline">Fóscolo & Company Edições</p><blockquote lang="pt-BR">{e(a["quote"])}</blockquote><p class="caption quote-source">{e(a["source"])}</p>'+paragraphs(a['paragraphs'])+'<div class="actions">'+link(path(lang,'repertoire'),a['back'],'button dark')+'</div></article>'
 if key=='about':
  a=d['about'];return hero(d,a['title'],a['intro'])+'<section class="wrap section split top-line"><div class="seal-block">'+image('seal.png','Fóscolo & Company Edições')+'</div><div class="lead">'+paragraphs(a['paragraphs'])+'</div></section><section class="wrap section">'+tiles(a['values'])+f'</section><section class="ink-section"><div class="wrap section split"><h2>{e(a["manifestoTitle"])}</h2><div><p>{e(a["manifestoText"])}</p>'+link(path(lang,'manifesto'),d['nav'][8],'button gold')+'</div></div></section>'
 if key=='projects':
  p=d['projects'];return hero(d,p['title'],p['intro'])+'<section class="wrap section top-line">'+bookcards(lang,d)+'</section><section class="wrap section">'+tiles(p['steps'])+'</section>'+contactband(lang,d,p['contactText'])
 if key=='author':
  a=d['author'];return hero(d,a['title'],a['intro'])+'<section class="wrap section split top-line"><div class="monogram" aria-hidden="true">MCF<span>Belo Horizonte / Brasil</span></div><div class="prose-inline">'+paragraphs(a['paragraphs'])+link('https://orcid.org/0009-0000-6000-2751',a['orcid'],'button dark',True)+f'</div></section><section class="wrap section">'+section_head('02',a['workTitle'])+tiles(a['workItems'])+f'</section><section class="paper-deep"><div class="wrap section split"><h2>{e(a["circulationTitle"])}</h2><div><p class="lead">{e(a["circulationText"])}</p>'+link(path(lang,'research'),d['research']['nav'],'button dark')+f'</div></div></section><section class="wrap section">'+bookcards(lang,d)+'</section>'
 if key=='press':
  p=d['press'];return hero(d,p['title'],p['intro'])+f'<section class="wrap section top-line"><div class="edition-grid"><article class="edition-card"><h2>Notes on Care, Risk & Knowledge</h2><p>{e(n["description"])}</p><div class="stack-links">'+link('/assets/press/notes-on-care-sample.pdf',u['download'])+link('/assets/images/notes-brasil.webp',u['cover'])+link(path(lang,'notes'),u['formats'])+f'</div><p class="caption">{e(u["sampleNote"])}</p></article><article class="edition-card"><p class="eyebrow">{e(u["forthcoming"])}</p><h2>Todos ou nenhum?</h2><p>{e(t["description"])}</p><p class="caption">{e(p["todosNote"])}</p>'+link('/assets/images/todos-title.webp',p['todosAsset'])+f'</article></div></section><section class="wrap section split"><h2>{e(p["bioTitle"])}</h2><p class="lead">{e(p["bio"])}</p></section>'+contactband(lang,d,p['request'])
 if key=='contact':
  c=d['contact'];return hero(d,c['title'],c['intro'])+f'<section class="wrap section split top-line"><div><p class="eyebrow">{e(c["location"])}</p><a class="contact-email" href="mailto:{EMAIL}?subject={quote(c["subject"])}">{EMAIL}</a><p>{e(c["socialText"])}</p>'+link(INSTAGRAM,'@foscolocompany',external=True)+f'</div><div class="text-card"><h2>{e(c["tipsTitle"])}</h2><ul class="plain-list">'+''.join(f'<li>{e(v)}</li>' for v in c['tips'])+f'</ul></div></section><div class="wrap privacy-note"><p>{e(u["privacy"])}</p></div>'
 if key=='manifesto':
  old=LEGACY[lang]['manifesto'].replace('Fóscolo & Company Editora','Fóscolo & Company Edições')
  blocks=re.findall(r'<(?:p|h2|blockquote)\b[^>]*>[\s\S]*?</(?:p|h2|blockquote)>',old)
  return hero(d,d['manifestoTitle'],'',d['nav'][8],True)+'<article class="prose wrap manifesto-prose">'+''.join(blocks)+'</article>'
 raise ValueError(key)

def title_for(key,d):
 if key=='home': return 'Fóscolo & Company Edições'
 if key=='notes': return 'Notes on Care, Risk & Knowledge'
 if key=='todos': return 'Todos ou nenhum? — Livro I'
 if key=='essay': return d['journal']['originalTitle']
 if key=='article': return d['article']['title']
 if key=='research': return d['research']['title']
 if key in ARTICLE_DATA: return d[ARTICLE_DATA[key]]['title']
 return d['nav'][NAV_INDEX[key]]

def desc_for(key,d):
 if key in ARTICLE_DATA: return d[ARTICLE_DATA[key]]['intro']
 if key=='essay': return d['journal']['originalDesc']
 if key=='article': return d['article']['intro']
 if key=='research': return d['research']['intro']
 if key in d and isinstance(d[key],dict): return d[key].get('intro',d[key].get('description',d['home']['intro']))
 return d['home']['intro']

def page(lang,key,body,d,root=False):
 u=d['ui'];nav=d['nav'];canonical=ORIGIN+('/' if root else path(lang,key));title=title_for(key,d);desc=desc_for(key,d)
 navhtml=''.join(f'<a href="{path(lang,k)}"'+(' aria-current="page"' if k==key else '')+f'>{e(nav[NAV_INDEX[k]])}</a>' for k in ['catalog','journal','repertoire','about','author','contact'])
 languages=''.join(f'<a href="{path(l,key)}" lang="{DATA[l]["lang"]}" hreflang="{DATA[l]["lang"]}"'+(' aria-current="true"' if l==lang else '')+f'>{e({"pt":"PT","en":"EN","es":"ES","fr":"FR","zh":"中文"}[l])}</a>' for l in DATA)
 alternates=''.join(f'<link rel="alternate" hreflang="{DATA[l]["lang"]}" href="{ORIGIN+path(l,key)}">' for l in DATA)
 ogimg=ORIGIN+'/assets/images/'+('todos-forest.webp' if key in ['todos','article'] else 'notes-brasil.webp')
 schema={'@context':'https://schema.org','@type':'WebPage','name':title,'description':desc,'url':canonical,'inLanguage':d['lang'],'publisher':{'@type':'Organization','name':'Fóscolo & Company Edições','url':ORIGIN,'email':EMAIL,'sameAs':[INSTAGRAM]}}
 if key in ['notes','todos']:
  schema['mainEntity']={'@type':'Book','name':title,'author':{'@type':'Person','name':'Maria Carolina Fóscolo'},'inLanguage':'en' if key=='notes' else 'pt-BR','publisher':{'@type':'Organization','name':'Fóscolo & Company Edições'}}
  if key=='notes': schema['mainEntity']['bookFormat']='https://schema.org/Paperback';schema['mainEntity']['numberOfPages']=64
 footerlinks=''.join(link(path(lang,k),nav[NAV_INDEX[k]],'footer-link') for k in ['catalog','projects','manifesto','press','contact'])
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
 (ROOT/'404.html').write_text('<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>Página não encontrada | Fóscolo & Company</title><link rel="stylesheet" href="/assets/fonts/chinese.css"><link rel="stylesheet" href="/assets/site.css"></head><body><main class="wrap page-hero"><p class="eyebrow">404</p><h1>Esta página mudou de lugar.</h1><p>Encontre livros, leituras e informações da editora a partir da página inicial.</p><a class="button dark" href="/pt/index.html">Ir para o início</a></main></body></html>')
 sitemap='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'<url><loc>{ORIGIN+p}</loc><lastmod>2026-09-29</lastmod></url>\n' for p in ['/']+outputs)+'</urlset>\n'
 (ROOT/'sitemap.xml').write_text(sitemap)
 (ROOT/'robots.txt').write_text(f'User-agent: *\nAllow: /\nSitemap: {ORIGIN}/sitemap.xml\n')
 (ROOT/'.nojekyll').touch()
 print(f'Built {len(outputs)+2} HTML pages in {len(DATA)} languages.')

if __name__=='__main__': build()
