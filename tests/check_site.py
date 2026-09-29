#!/usr/bin/env python3
"""Validate generated pages, local destinations, metadata and translation coverage."""
import json
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
import build

class Document(HTMLParser):
 def __init__(self, text):
  super().__init__(); self.ids=set();self.links=[];self.images=[];self.h1=0;self.lang=None;self.canonical=[];self.alternates=[];self.feeds=[];self.feed(text)
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a: self.ids.add(a['id'])
  if tag=='html':self.lang=a.get('lang')
  if tag=='h1':self.h1+=1
  if tag in ['a','link','script','img']:
   v=a.get('href') or a.get('src')
   if v:self.links.append(v)
  if tag=='img':self.images.append(a)
  if tag=='link' and a.get('rel')=='canonical':self.canonical.append(a['href'])
  if tag=='link' and a.get('rel')=='alternate' and a.get('hreflang'):self.alternates.append(a)
  if tag=='link' and a.get('rel')=='alternate' and a.get('type')=='application/rss+xml':self.feeds.append(a)

def fields(value,prefix=''):
 if isinstance(value,dict):
  return {k for key,v in value.items() for k in fields(v,prefix+'/'+key)}
 return {prefix}

def main():
 errors=[]; documents={p:Document(p.read_text()) for p in ROOT.rglob('*.html') if '.git' not in p.parts}
 for p,d in documents.items():
  if d.h1!=1:errors.append(f'{p}: {d.h1} h1 elements')
  if not d.lang:errors.append(f'{p}: missing language')
  if p.name!='404.html' and len(d.canonical)!=1:errors.append(f'{p}: canonical missing/duplicated')
  if p.name!='404.html' and len(d.alternates)!=6:errors.append(f'{p}: missing language alternates')
  if p.name!='404.html' and len(d.feeds)!=1:errors.append(f'{p}: RSS alternate missing/duplicated')
  for a in d.images:
   if not a.get('alt'):errors.append(f'{p}: image lacks alternative text')
  for href in d.links:
   url=urlsplit(href)
   if url.scheme or url.netloc:continue
   dest=ROOT/unquote(url.path).lstrip('/') if url.path.startswith('/') else p.parent/unquote(url.path)
   if not url.path:dest=p
   if dest.is_dir():dest=dest/'index.html'
   dest=dest.resolve()
   if not dest.exists():errors.append(f'{p.relative_to(ROOT)}: missing {href}')
   elif url.fragment and dest in documents and unquote(url.fragment) not in documents[dest].ids:errors.append(f'{p}: missing fragment {href}')
 for lang,data in build.DATA.items():
  if fields(data)!=fields(build.DATA['pt']):errors.append(f'{lang}: translation schema differs')
  for key in build.ROUTES[lang]:
   route_file=ROOT/build.path(lang,key).lstrip('/')
   if not route_file.is_file():errors.append(f'{lang}: missing {key}')
  for key in build.DISCOVERY_MAP:
   route_file=ROOT/build.path(lang,key).lstrip('/')
   if route_file.is_file():
    html=route_file.read_text()
    if html.count('class="discovery-card"')!=3:errors.append(f'{lang}/{key}: expected three discovery cards')
    if data['ui']['continueExploring'] not in html:errors.append(f'{lang}/{key}: discovery heading missing')
  todos=(ROOT/build.path(lang,'todos').lstrip('/')).read_text()
  if 'Uma folha sozinha quase não oferece resistência.' in todos or 'class="excerpt"' in todos:
   errors.append(f'{lang}: unpublished Todos excerpt returned')
  notes=(ROOT/build.path(lang,'notes').lstrip('/')).read_text()
  if build.BR not in notes:errors.append(f'{lang}: Brazilian Amazon link missing from Notes')
  search_page=(ROOT/build.path(lang,'search').lstrip('/')).read_text()
  if 'data-search-page' not in search_page:errors.append(f'{lang}: archive search UI missing')
  if search_page.count('class="path-card"')!=4:errors.append(f'{lang}: expected four curated archive paths')
  if '"@type": "CollectionPage"' not in search_page:errors.append(f'{lang}: archive CollectionPage schema missing')
  index_file=ROOT/'assets'/'search'/f'{lang}.json'
  if not index_file.is_file():errors.append(f'{lang}: search index missing')
  else:
   try: index=json.loads(index_file.read_text())
   except Exception: errors.append(f'{lang}: invalid search index');index=[]
   expected=len(build.ROUTES[lang])-2
   if len(index)!=expected:errors.append(f'{lang}: search index has {len(index)} docs; expected {expected}')
   serialized=json.dumps(index,ensure_ascii=False)
   if 'Uma folha sozinha quase não oferece resistência.' in serialized:errors.append(f'{lang}: unpublished Todos excerpt leaked into search')
   if not any(item.get('key')=='repertoire2' for item in index):errors.append(f'{lang}: public Repertoire content absent from search')
   if not any(item.get('key')=='place' for item in index):errors.append(f'{lang}: public place content absent from search')
  feed_file=ROOT/'feeds'/f'{lang}.xml'
  if not feed_file.is_file():errors.append(f'{lang}: RSS feed missing')
  else:
   feed=feed_file.read_text()
   if feed.count('<item>')!=6:errors.append(f'{lang}: RSS feed should contain six items')
   if '<rss version="2.0">' not in feed:errors.append(f'{lang}: invalid RSS root')
  article_page=(ROOT/build.path(lang,'circulation').lstrip('/')).read_text()
  if '"@type": "Article"' not in article_page:errors.append(f'{lang}: Article schema missing')
  notes_schema=(ROOT/build.path(lang,'notes').lstrip('/')).read_text()
  if '"@type": "Book"' not in notes_schema or build.BR not in notes_schema:errors.append(f'{lang}: Book schema missing Amazon identity')
 if len(build.DATA)!=5:errors.append('Expected five languages')
 if errors:print('\n'.join(errors));raise SystemExit(1)
 print(f'PASS: {len(documents)} pages, five languages, local links, fragments, image labels and metadata.')

if __name__=='__main__':main()
