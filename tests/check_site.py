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
  super().__init__(); self.ids=set();self.links=[];self.images=[];self.h1=0;self.lang=None;self.canonical=[];self.alternates=[];self.feed(text)
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
  if tag=='link' and a.get('rel')=='alternate':self.alternates.append(a)

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
   if not (ROOT/build.path(lang,key).lstrip('/')).is_file():errors.append(f'{lang}: missing {key}')
 if len(build.DATA)!=5:errors.append('Expected five languages')
 if errors:print('\n'.join(errors));raise SystemExit(1)
 print(f'PASS: {len(documents)} pages, five languages, local links, fragments, image labels and metadata.')

if __name__=='__main__':main()
