#!/usr/bin/env python3
"""Build the five static documentation pages from complete local translations."""
from pathlib import Path
from html import escape
import json

ROOT = Path(__file__).resolve().parent
LANGUAGES = ('en', 'zh-Hans', 'zh-Hant', 'ja', 'es', 'de', 'fr')
PAGES = ('index', 'faq', 'support', 'privacy', 'terms')
BASE = 'https://gl-technologies.github.io/app-docs/repost-reset/'
EMAIL = 'GL.Tech@icloud.com'
ICONS = {
 'faq': '<path d="M9.1 9a3 3 0 0 1 5.8 1c0 2-3 2-3 4m0 3h.01"/><circle cx="12" cy="12" r="9"/>',
 'support': '<rect x="3" y="5" width="18" height="14" rx="3"/><path d="m3 6 9 7 9-7"/>',
 'privacy': '<path d="M12 3 4 6v6c0 4 8 9 8 9s8-5 8-9V6z"/><path d="m8 12 3 3 5-6"/>',
 'terms': '<path d="M14 3H6a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"/><path d="M14 3v6h6M8 13h8M8 17h5"/>'
}

def svg(name):
 return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>'

def translated(items):
 return '\n'.join(f'<span data-lang="{lang}"'+(' hidden' if lang != 'en' else '')+f'>{escape(text)}</span>' for lang,text in items)

def render_sections(page):
 result=[]
 for section in page['sections']:
  body=section.get('body','')
  if 'items' in section:
   body='\n'.join(f'<details>\n<summary>{escape(item["question"])}</summary>\n<div class="answer"><p>{item["answer"]}</p></div>\n</details>' for item in section['items'])
  result.append(f'<section class="card">\n<h2>{escape(section["title"])}</h2>\n{body}\n</section>')
 return '\n'.join(result)

locales={lang:json.loads((ROOT/'locales'/f'{lang}.json').read_text()) for lang in LANGUAGES}
# Translation parity is a publication requirement, including every FAQ item.
reference=locales['en']
for lang,data in locales.items():
 assert data['language']==lang and set(data['pages'])==set(PAGES),lang
 assert len(data['nav'])==4 and len(data['resources'])==4,lang
 for page in PAGES:
  a,b=reference['pages'][page],data['pages'][page]
  assert len(a['sections'])==len(b['sections']),(lang,page)
  for original,translated_section in zip(a['sections'],b['sections']):
   assert translated_section['title'] and (translated_section.get('body') or translated_section.get('items')),(lang,page)
   if 'items' in original:
    assert len(original['items'])==len(translated_section['items']),(lang,page)
    assert all(x['question'] and x['answer'] for x in translated_section['items']),(lang,page)

options='\n'.join(f'<option value="{lang}">{escape(locales[lang]["name"])}</option>' for lang in LANGUAGES)
for page in PAGES:
 navigation=[]
 for i,name in enumerate(PAGES[1:]):
  label=translated((lang,locales[lang]['nav'][i]) for lang in LANGUAGES)
  current=' aria-current="page"' if page==name else ''
  navigation.append(f'<a href="{name}.html"{current}>{label}</a>')
 content=[]
 for lang,data in locales.items():
  p=data['pages'][page]
  portal=''
  if page=='index':
   portal='<div class="resource-grid">\n'+ '\n'.join(f'<a class="resource" href="{name}.html"><span class="resource-icon">{svg(name)}</span><span class="resource-copy"><strong>{escape(data["nav"][i])}</strong><span>{escape(data["resources"][i])}</span></span><span class="chevron" aria-hidden="true">›</span></a>' for i,name in enumerate(PAGES[1:]))+'\n</div>'
  content.append(f'''<div data-lang="{lang}"{'' if lang=='en' else ' hidden'}>
<div class="doc-header">
<img class="app-icon {'portal-icon' if page=='index' else 'document-icon'}" src="app-icon.png" width="96" height="96" alt="" decoding="async">
<h1>{escape(p['title'])}</h1>
<p class="lead">{p['subtitle']}</p>
</div>
{portal}
<div class="reading-content">{render_sections(p)}</div>
</div>''')
 output=f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light dark">
<meta name="description" content="{escape(reference['description'])}">
<title>Repost Reset · {escape(reference['pages'][page]['title'])}</title>
<link rel="canonical" href="{BASE}{page}.html">
<meta property="og:title" content="Repost Reset · {escape(reference['pages'][page]['title'])}">
<meta property="og:description" content="{escape(reference['description'])}">
<meta property="og:image" content="{BASE}app-icon.png">
<link rel="icon" type="image/png" href="app-icon.png">
<link rel="apple-touch-icon" href="app-icon.png">
<link rel="stylesheet" href="style.css">
<script src="language.js" defer></script>
</head>
<body>
<a class="skip" href="#main">{translated((lang,data['skip']) for lang,data in locales.items())}</a>
<div class="container {'portal' if page=='index' else 'document'}">
<header class="top-navbar">
<a class="brand" href="index.html"><img class="app-icon brand-icon" src="app-icon.png" alt="" width="32" height="32"><span>Repost Reset</span></a>
<div class="lang-capsule">
<svg class="globe" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><circle cx="12" cy="12" r="9"/><ellipse cx="12" cy="12" rx="4" ry="9"/><path d="M3 12h18"/></svg>
<span id="current-language">English</span><span class="lang-arrow" aria-hidden="true">⌄</span>
<select id="language-select" aria-label="Language">{options}</select>
</div>
</header>
<nav class="segmented-control" aria-label="Documentation">{''.join(navigation)}</nav>
<main id="main">{''.join(content)}</main>
<footer>
<p>{translated((lang,data['independent']) for lang,data in locales.items())}</p>
<a href="mailto:{EMAIL}">{EMAIL}</a>
<p>© 2026 GL Technologies. {translated((lang,data['allRights']) for lang,data in locales.items())}</p>
</footer>
</div>
</body>
</html>
'''
 (ROOT/f'{page}.html').write_text(output)
print('Built five pages with seven complete language versions.')
